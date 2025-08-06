import math
import random
import time
import pygame
from config import *
from audio import audio_manager

class Hunter:
    def __init__(self, hunter_id):
        self.id = hunter_id
        self.radius = HUNTER_RADIUS
        self.max_stamina = HUNTER_MAX_STAMINA
        self.stamina = self.max_stamina
        self.stamina_regen_rate = HUNTER_STAMINA_REGEN_RATE
        
        self.walk_speed = HUNTER_WALK_SPEED
        self.run_speed = HUNTER_RUN_SPEED  # 跑步速度
        self.charge_speed = HUNTER_CHARGE_SPEED
        self.stop_speed = 0
        
        self.normal_rotation_speed = HUNTER_NORMAL_ROTATION_SPEED
        self.run_rotation_speed = HUNTER_RUN_ROTATION_SPEED  # 跑步旋转速度
        self.charge_rotation_speed = HUNTER_CHARGE_ROTATION_SPEED
        self.current_rotation_speed = self.normal_rotation_speed
        
        self.angle = 0
        self.charge_distance = HUNTER_CHARGE_DISTANCE
        self.charge_stamina_cost = HUNTER_CHARGE_STAMINA_COST
        self.charge_stamina_per_pixel = HUNTER_CHARGE_STAMINA_PER_PIXEL
        self.run_stamina_cost_per_second = HUNTER_RUN_STAMINA_COST_PER_SECOND  # 跑步耐力消耗
        self.is_charging = False
        self.is_running = False  # 是否在跑步状态
        self.charge_progress = 0  # 已冲锋的距离（像素）
        self.state = "walking"  # 包含"running"状态
        
        self.charge_cooldown = HUNTER_CHARGE_COOLDOWN
        self.last_spawn_time = time.time()
        self.last_charge_time = 0  # 记录上次冲锋时间
        
        # 随机游走属性
        self.wander_target = None
        self.wander_range = HUNTER_WANDER_AREA
        self.last_wander_change = time.time()
        self.wander_change_interval = random.uniform(*HUNTER_WANDER_CHANGE_INTERVAL)
        
        # 策略性追逐相关
        self.last_seen_player_pos = None  # 上次看到玩家的位置
        self.lost_sight_time = 0  # 失去玩家视野的时间
        self.pursuit_memory_time = 8  # 记忆玩家位置的时间（秒）
        
        # 冲锋目标跟踪
        self.charge_target = None  # 冲锋目标位置
        self.charge_prediction_updated = False  # 是否已更新过预测
        
        self.map_x = 0
        self.map_y = 0
        self.accelerate_approach = False  # 接近阶段加速标记
        
        # 新增：体力管理参数
        self.critical_stamina_ratio = 0.3  # 30%体力以下视为关键状态
        self.reserve_stamina_ratio = 0.2   # 保留20%体力用于紧急情况
        
    def initialize_position(self, existing_hunters, player_center_x, player_center_y):
        """初始化位置（避免与其他狩猎者过近）"""
        while True:
            # 在玩家周围1000-3000像素范围内生成
            distance = random.randint(1000, 3000)
            angle = random.uniform(0, math.pi * 2)
            
            self.map_x = player_center_x + math.cos(angle) * distance
            self.map_y = player_center_y + math.sin(angle) * distance
            
            # 确保在地图范围内
            self.map_x = max(self.radius, min(MAP_WIDTH - self.radius, self.map_x))
            self.map_y = max(self.radius, min(MAP_HEIGHT - self.radius, self.map_y))
            
            # 确保与其他狩猎者保持距离
            too_close = False
            for hunter in existing_hunters:
                dx = self.map_x - hunter.map_x
                dy = self.map_y - hunter.map_y
                if math.sqrt(dx*dx + dy*dy) < 500:
                    too_close = True
                    break
            if not too_close:
                break
        
        self.set_new_wander_target()
        self.is_charging = False
        self.is_running = False  # 初始化跑步状态
        self.charge_progress = 0
        self.stamina = self.max_stamina
        self.state = "walking"
        self.last_spawn_time = time.time()
        
    def set_new_wander_target(self):
        """设置新的随机游走目标点"""
        angle = random.uniform(0, math.pi * 2)
        distance = random.randint(300, self.wander_range // 2)
        self.wander_target = (
            self.map_x + math.cos(angle) * distance,
            self.map_y + math.sin(angle) * distance
        )
        # 确保目标点在地图范围内
        self.wander_target = (
            max(self.radius, min(MAP_WIDTH - self.radius, self.wander_target[0])),
            max(self.radius, min(MAP_HEIGHT - self.radius, self.wander_target[1]))
        )
        self.wander_change_interval = random.uniform(*HUNTER_WANDER_CHANGE_INTERVAL)
        self.last_wander_change = time.time()
        
    def regenerate_stamina(self, delta_time):
        # 耐力恢复 = 每秒恢复量 * 时间（秒）
        regen_amount = self.stamina_regen_rate * delta_time
        self.stamina = min(self.max_stamina, self.stamina + regen_amount)
            
        if self.stamina < HUNTER_STAMINA_THRESHOLD and self.state != "charging" and self.state != "running":
            self.state = "stopping"
        elif self.stamina >= HUNTER_STAMINA_THRESHOLD and self.state == "stopping":
            self.state = "walking"
    
    def get_nearby_hunters(self, all_hunters):
        """获取附近的其他狩猎者"""
        nearby = []
        for hunter in all_hunters:
            if hunter.id != self.id:
                dx = self.map_x - hunter.map_x
                dy = self.map_y - hunter.map_y
                distance = math.sqrt(dx*dx + dy*dy)
                if distance < HUNTER_GROUP_BEHAVIOR_RADIUS:
                    nearby.append((hunter, distance))
        return nearby
    
    def avoid_other_hunters(self, all_hunters):
        """避免与其他狩猎者碰撞"""
        avoidance_x, avoidance_y = 0, 0
        
        for hunter in all_hunters:
            if hunter.id != self.id:
                dx = self.map_x - hunter.map_x
                dy = self.map_y - hunter.map_y
                distance = math.sqrt(dx*dx + dy*dy)
                
                if distance < HUNTER_AVOID_COLLISION_RADIUS and distance > 0:
                    # 计算远离其他狩猎者的方向
                    force = (HUNTER_AVOID_COLLISION_RADIUS - distance) / HUNTER_AVOID_COLLISION_RADIUS
                    avoidance_x += dx * force
                    avoidance_y += dy * force
        
        # 归一化并应用避开力
        if avoidance_x != 0 or avoidance_y != 0:
            dist = math.sqrt(avoidance_x**2 + avoidance_y**2)
            if dist > 0:
                avoidance_x /= dist
                avoidance_y /= dist
                return avoidance_x * 0.5, avoidance_y * 0.5
        
        return 0, 0
    
    def calculate_intercept_point(self, player, lead_time_factor=1.0):
        """计算拦截玩家的点，基于玩家实际移动轨迹预测"""
        # 获取玩家实际移动向量（基于历史位置）
        player_dx, player_dy = player.get_movement_vector()
        
        # 计算狩猎者到玩家的距离
        dx = player.map_x - self.map_x
        dy = player.map_y - self.map_y
        distance = math.sqrt(dx*dx + dy*dy)
        
        # 如果距离太近，直接返回玩家当前位置
        if distance < HUNTER_MIN_CHARGE_DISTANCE * 1.5:
            return (player.map_x, player.map_y)
            
        # 计算相对速度
        rel_speed_x = player_dx
        rel_speed_y = player_dy
        
        # 计算相遇时间 - 考虑双方移动
        a = rel_speed_x**2 + rel_speed_y**2 - self.charge_speed**2
        b = 2 * (dx * rel_speed_x + dy * rel_speed_y)
        c = dx**2 + dy**2
        
        # 解二次方程 at² + bt + c = 0
        discriminant = b**2 - 4 * a * c
        
        if discriminant < 0:
            # 无实根，使用简单预测
            intercept_time = distance / (self.charge_speed - math.sqrt(rel_speed_x**2 + rel_speed_y**2) * 0.8)
        else:
            sqrt_discriminant = math.sqrt(discriminant)
            t1 = (-b + sqrt_discriminant) / (2 * a)
            t2 = (-b - sqrt_discriminant) / (2 * a)
            
            # 选择最小的正时间
            intercept_time = min(t for t in [t1, t2] if t > 0) if any(t > 0 for t in [t1, t2]) else distance / self.charge_speed
        
        # 应用时间因子调整预测超前量
        intercept_time *= lead_time_factor
        
        # 限制在合理范围内
        intercept_time = max(0.5, min(30, intercept_time))
        
        # 预测玩家未来位置
        predicted_x = player.map_x + player_dx * intercept_time
        predicted_y = player.map_y + player_dy * intercept_time
        
        # 确保预测位置在地图范围内
        predicted_x = max(self.radius, min(MAP_WIDTH - self.radius, predicted_x))
        predicted_y = max(self.radius, min(MAP_HEIGHT - self.radius, predicted_y))
        
        return (predicted_x, predicted_y)
    
    def update_charge_direction(self, player, delta_time):
        """在冲锋过程中动态调整方向"""
        if not self.charge_target:
            return
            
        # 计算到目标的角度
        dx = self.charge_target[0] - self.map_x
        dy = self.charge_target[1] - self.map_y
        target_angle = math.degrees(math.atan2(dy, dx)) % 360
        
        # 计算角度差
        angle_diff = (target_angle - self.angle) % 360
        
        # 限制转向幅度，保留一定惯性
        max_rotate = self.charge_rotation_speed * delta_time * HUNTER_CHARGE_TURN_RATIO
        
        if angle_diff < 180:
            rotate_amount = min(max_rotate, angle_diff)
            self.angle += rotate_amount
        else:
            rotate_amount = min(max_rotate, 360 - angle_diff)
            self.angle -= rotate_amount
            
        self.angle %= 360
    
    def start_charge(self, player):
        """开始冲锋的方法"""
        self.is_charging = True
        self.is_running = False  # 冲锋时结束跑步状态
        self.charge_progress = 0
        self.state = "charging"
        self.stamina -= self.charge_stamina_cost
        self.stamina = max(0, self.stamina)
        self.last_charge_time = time.time()
        
        # 计算拦截点而不是直接冲向玩家当前位置
        self.charge_target = self.calculate_intercept_point(player)
        self.charge_prediction_updated = False
        
        # 设置初始冲锋角度
        dx = self.charge_target[0] - self.map_x
        dy = self.charge_target[1] - self.map_y
        self.angle = math.degrees(math.atan2(dy, dx)) % 360
        audio_manager.play_sound('run') 
    
    def end_charge(self):
        """结束冲锋的方法"""
        self.is_charging = False
        self.state = "stopping"
        self.current_rotation_speed = self.normal_rotation_speed
        self.charge_target = None
        self.charge_prediction_updated = False
        self.set_new_wander_target()
    
    # 开始跑步方法（无冷却）
    def start_running(self):
        # 新增：体力过低时即使有耐力也减少跑步（保留体力用于冲刺）
        current_stamina_ratio = self.stamina / self.max_stamina
        if (self.state != "running" and 
            not self.is_charging and 
            self.stamina >= HUNTER_RUN_STAMINA_THRESHOLD and
            current_stamina_ratio > self.reserve_stamina_ratio):  # 高于保留阈值才允许跑步
            
            self.is_running = True
            self.state = "running"
            self.current_rotation_speed = self.run_rotation_speed
    
    # 结束跑步方法（无冷却）
    def stop_running(self):
        if self.state == "running":
            self.is_running = False
            self.state = "walking"
            self.current_rotation_speed = self.normal_rotation_speed
        
    def update(self, player, all_hunters, all_foods, delta_time):
        self.regenerate_stamina(delta_time)
        current_time = time.time()
        current_stamina_ratio = self.stamina / self.max_stamina  # 当前体力比例（0-1）
        
        # 计算与玩家的距离
        dx = player.map_x - self.map_x
        dy = player.map_y - self.map_y
        distance_to_player = math.sqrt(dx * dx + dy * dy)
        in_detection_range = distance_to_player < HUNTER_DETECTION_RANGE
        
        # 更新最后看到的玩家位置
        if in_detection_range:
            self.last_seen_player_pos = (player.map_x, player.map_y)
        else:
            if self.last_seen_player_pos and current_time - self.lost_sight_time > self.pursuit_memory_time:
                self.last_seen_player_pos = None  # 超过记忆时间，忘记玩家位置
            elif not in_detection_range and self.last_seen_player_pos:
                self.lost_sight_time = current_time  # 更新失去视野的时间
        
        # 获取附近的狩猎者
        nearby_hunters = self.get_nearby_hunters(all_hunters)
        nearby_charging = any(hunter.is_charging for hunter, _ in nearby_hunters)
        nearby_running = any(hunter.is_running for hunter, _ in nearby_hunters)
        
        # 处理跑步状态的耐力消耗
        if self.is_running:
            # 新增：体力低于保留阈值时自动停止跑步
            if current_stamina_ratio <= self.reserve_stamina_ratio:
                self.stop_running()
            else:
                # 跑步时持续消耗耐力
                self.stamina -= self.run_stamina_cost_per_second * delta_time
                self.stamina = max(0, self.stamina)
                
                # 耐力不足时自动停止跑步
                if self.stamina < HUNTER_RUN_STAMINA_THRESHOLD:
                    self.stop_running()
        
        # 感知范围内的行为
        if in_detection_range and not self.is_charging:
            # 计算冲锋总成本（基础消耗+距离消耗）
            estimated_total_cost = self.charge_stamina_cost + (self.charge_distance * self.charge_stamina_per_pixel)
            # 计算冲锋后剩余体力比例（用于决策）
            remaining_stamina_after_charge = (self.stamina - estimated_total_cost) / self.max_stamina
            
            # 冲锋条件（优化：加入体力安全检查）
            can_charge = (
                not self.is_charging
                # 体力要求：确保冲锋后仍有安全余量（至少保留10%）
                and remaining_stamina_after_charge > 0.1
                and current_time - self.last_spawn_time >= self.charge_cooldown
                and current_time - self.last_charge_time >= self.charge_cooldown
                # 距离要求：仅在冲刺有效范围内（100-300像素）
                and 100 < distance_to_player < 300
                and distance_to_player < self.charge_distance * 0.8
            )
            
            # 冲锋决策（优化：根据体力动态调整概率）
            if can_charge:
                # 基础概率：距离越近概率越高
                base_charge_prob = 2.5 * (1 - (distance_to_player / 300))
                
                # 体力系数：体力越低，概率系数越小（避免低体力时冲锋）
                if current_stamina_ratio < self.critical_stamina_ratio:
                    # 体力低于30%时，大幅降低冲锋概率
                    stamina_factor = current_stamina_ratio / self.critical_stamina_ratio  # 0-1之间
                else:
                    stamina_factor = 1.0  # 体力充足时不降低
                
                # 群体系数：附近有冲锋时降低概率
                group_factor = 0.2 if nearby_charging else 1.0
                
                # 最终冲锋概率 = 基础概率 * 体力系数 * 群体系数 * 时间因子
                charge_chance = base_charge_prob * stamina_factor * group_factor * delta_time
                
                if random.random() < charge_chance:
                    self.start_charge(player)
            
            # 跑步决策逻辑（优化：根据体力调整跑步意愿）
            if HUNTER_RUN_RANGE_MIN < distance_to_player < HUNTER_RUN_RANGE_MAX:
                # 基础跑步概率：距离适中时最高
                base_run_prob = 0.9 * (1 - (abs(distance_to_player - 500) / 500))
                
                # 体力系数：体力越低，跑步概率越低（保留体力）
                run_stamina_factor = min(1.0, current_stamina_ratio / (self.critical_stamina_ratio + 0.2))
                
                # 群体系数：附近有跑步时提高概率
                run_group_factor = 1.5 if nearby_running else 1.0
                
                # 最终跑步概率
                run_chance = base_run_prob * run_stamina_factor * run_group_factor * delta_time
                
                if random.random() < run_chance and self.stamina >= HUNTER_RUN_STAMINA_THRESHOLD:
                    self.start_running()
            # 距离过近时（<200像素）停止跑步，准备冲锋
            elif distance_to_player <= 200 and self.is_running:
                self.stop_running()
        
        # 处理冲锋状态
        if self.is_charging:
            # 冲锋时结束跑步状态
            self.is_running = False
            
            if not self.charge_prediction_updated and self.charge_progress > self.charge_distance * 0.3:
                self.charge_target = self.calculate_intercept_point(player, 0.7)
                self.charge_prediction_updated = True
                
            self.update_charge_direction(player, delta_time)
            
            move_distance = self.charge_speed * delta_time
            self.charge_progress += move_distance
            
            self.stamina -= self.charge_stamina_per_pixel * move_distance
            self.stamina = max(0, self.stamina)
            
            if self.charge_progress >= self.charge_distance or self.stamina <= 0 or distance_to_player < self.radius + player.radius:
                self.end_charge()
        
        # 移动逻辑
        if in_detection_range or self.is_charging:
            self.move_towards_player(player, all_hunters, delta_time)
        elif self.last_seen_player_pos:
            # 追击记忆中的玩家位置时也可以跑步
            self.move_towards_position(self.last_seen_player_pos, all_hunters, delta_time)
        else:
            self.move_intelligently(current_time, all_hunters, all_foods, delta_time)
        
        # 限制在地图范围内
        self.map_x = max(self.radius, min(MAP_WIDTH - self.radius, self.map_x))
        self.map_y = max(self.radius, min(MAP_HEIGHT - self.radius, self.map_y))
        
    def move_towards_player(self, player, all_hunters, delta_time):
        # 根据状态设置速度和旋转速度
        if self.is_charging:
            current_speed = self.charge_speed
            self.current_rotation_speed = self.charge_rotation_speed
        elif self.is_running:
            current_speed = self.run_speed  # 使用跑步速度
            self.current_rotation_speed = self.run_rotation_speed
        elif self.accelerate_approach:
            current_speed = self.walk_speed * 1.5
            self.current_rotation_speed = self.normal_rotation_speed * 1.2
        elif self.state == "walking":
            current_speed = self.walk_speed
            self.current_rotation_speed = self.normal_rotation_speed
        else:
            current_speed = self.stop_speed * 0.5
            self.current_rotation_speed = self.normal_rotation_speed * HUNTER_STOP_ROTATION_SPEED_RATIO
        
        if not self.is_charging:
            dx = player.map_x - self.map_x
            dy = player.map_y - self.map_y
            target_angle = math.degrees(math.atan2(dy, dx)) % 360
            
            angle_diff = (target_angle - self.angle) % 360
            if angle_diff < 180:
                rotate_amount = min(self.current_rotation_speed * delta_time, angle_diff)
                self.angle += rotate_amount
            else:
                rotate_amount = min(self.current_rotation_speed * delta_time, 360 - angle_diff)
                self.angle -= rotate_amount
            self.angle %= 360
        
        # 计算移动向量
        rad = math.radians(self.angle)
        move_x = math.cos(rad) * current_speed * delta_time
        move_y = math.sin(rad) * current_speed * delta_time
        
        # 添加避开其他狩猎者的向量
        avoid_x, avoid_y = self.avoid_other_hunters(all_hunters)
        move_x += avoid_x
        move_y += avoid_y
        
        # 应用移动
        self.map_x += move_x
        self.map_y += move_y
        
    def move_towards_position(self, target_pos, all_hunters, delta_time):
        """向指定位置移动（用于追击记忆中的玩家位置）"""
        # 记忆追击时可以使用跑步状态，但受体力限制
        if self.is_running and self.stamina >= HUNTER_RUN_STAMINA_THRESHOLD:
            current_speed = self.run_speed
            self.current_rotation_speed = self.run_rotation_speed
        elif self.state == "walking":
            current_speed = self.walk_speed * 0.8
            self.current_rotation_speed = self.normal_rotation_speed * 0.9
        elif self.state == "stopping":
            current_speed = self.walk_speed * 0.3
            self.current_rotation_speed = self.normal_rotation_speed * 0.5
        
        target_angle = math.degrees(math.atan2(target_pos[1] - self.map_y, target_pos[0] - self.map_x)) % 360
        
        angle_diff = (target_angle - self.angle) % 360
        if angle_diff < 180:
            rotate_amount = min(self.current_rotation_speed * delta_time, angle_diff)
            self.angle += rotate_amount
        else:
            rotate_amount = min(self.current_rotation_speed * delta_time, 360 - angle_diff)
            self.angle -= rotate_amount
        self.angle %= 360
        
        # 计算移动向量
        rad = math.radians(self.angle)
        move_x = math.cos(rad) * current_speed * delta_time
        move_y = math.sin(rad) * current_speed * delta_time
        
        # 添加避开其他狩猎者的向量
        avoid_x, avoid_y = self.avoid_other_hunters(all_hunters)
        move_x += avoid_x
        move_y += avoid_y
        
        # 应用移动
        self.map_x += move_x
        self.map_y += move_y
    
    def move_intelligently(self, current_time, all_hunters, all_foods, delta_time):
        """智能游走逻辑，包括群体行为和食物吸引"""
        # 未追踪玩家时不跑步，节省体力
        if self.is_running:
            self.stop_running()
            
        # 定期更换游走目标
        if (self.wander_target is None or 
            current_time - self.last_wander_change > self.wander_change_interval):
        
            # 获取附近的食物
            nearby_food = self.get_nearby_food(all_foods)
        
            # 60%概率被最近的食物吸引，40%保持随机游走
            if nearby_food and random.random() < 0.6:
                # 选择最近的食物作为目标点
                target_food = nearby_food[0][0]
                angle_offset = random.uniform(-0.5, 0.5)
                distance_offset = random.randint(100, 300)
            
                rad = math.radians(math.atan2(
                    target_food.map_y - self.map_y,
                    target_food.map_x - self.map_x
                ) + angle_offset)
            
                target_x = target_food.map_x + math.cos(rad) * distance_offset
                target_y = target_food.map_y + math.sin(rad) * distance_offset
            
                # 确保目标在地图范围内
                self.wander_target = (
                    max(self.radius, min(MAP_WIDTH - self.radius, target_x)),
                    max(self.radius, min(MAP_HEIGHT - self.radius, target_y))
                )
            else:
                # 原随机游走逻辑
                self.set_new_wander_target()

        # 移动逻辑
        dx = self.wander_target[0] - self.map_x
        dy = self.wander_target[1] - self.map_y
        distance_to_target = math.sqrt(dx * dx + dy * dy)
    
        if distance_to_target < 100:
            self.set_new_wander_target()
            return
    
        if self.state == "walking":
            current_speed = self.walk_speed * 0.9
            target_angle = math.degrees(math.atan2(dy, dx)) % 360
        
            angle_diff = (target_angle - self.angle) % 360
            if angle_diff < 180:
                rotate_amount = min(self.normal_rotation_speed * 0.8 * delta_time, angle_diff)
                self.angle += rotate_amount
            else:
                rotate_amount = min(self.normal_rotation_speed * 0.8 * delta_time, 360 - angle_diff)
                self.angle -= rotate_amount
            self.angle %= 360
        
            rad = math.radians(self.angle)
            move_x = math.cos(rad) * current_speed * delta_time
            move_y = math.sin(rad) * current_speed * delta_time
        
            avoid_x, avoid_y = self.avoid_other_hunters(all_hunters)
            move_x += avoid_x
            move_y += avoid_y
        
            self.map_x += move_x
            self.map_y += move_y
        elif self.state == "stopping":
            current_speed = self.walk_speed * 0.3
            rad = math.radians(self.angle)
            self.map_x += math.cos(rad) * current_speed * delta_time
            self.map_y += math.sin(rad) * current_speed * delta_time

    def get_nearby_food(self, all_foods, max_distance=1500):
        """获取一定范围内的食物"""
        nearby_food = []
        for food in all_foods:
            dx = self.map_x - food.map_x
            dy = self.map_y - food.map_y
            distance = math.sqrt(dx*dx + dy*dy)
            if distance < max_distance:
                nearby_food.append((food, distance))
        # 按距离排序（最近的食物优先）
        nearby_food.sort(key=lambda x: x[1])
        return nearby_food

    def draw(self, surface, player):
        screen_x = self.map_x - player.map_x + WINDOW_WIDTH // 2
        screen_y = self.map_y - player.map_y + WINDOW_HEIGHT // 2
        
        # 只绘制屏幕范围内的狩猎者
        if -self.radius <= screen_x <= WINDOW_WIDTH + self.radius and -self.radius <= screen_y <= WINDOW_HEIGHT + self.radius:
            # 根据状态设置颜色
            if self.is_charging:
                color = ORANGE
            elif self.is_running:
                color = CYAN  # 跑步状态使用青色
            elif self.state == "stopping":
                color = GRAY
            else:
                color = PURPLE
                
            pygame.draw.circle(surface, color, (int(screen_x), int(screen_y)), self.radius)
            
            # 绘制眼睛
            rad = math.radians(self.angle)
            eye_offset = self.radius * 0.6
            left_eye = (screen_x + math.cos(rad - 0.2) * eye_offset, 
                       screen_y + math.sin(rad - 0.2) * eye_offset)
            right_eye = (screen_x + math.cos(rad + 0.2) * eye_offset, 
                        screen_y + math.sin(rad + 0.2) * eye_offset)
            pygame.draw.circle(surface, WHITE, (int(left_eye[0]), int(left_eye[1])), 4)
            pygame.draw.circle(surface, WHITE, (int(right_eye[0]), int(right_eye[1])), 4)
            
            # 绘制耐力条（优化：低体力时显示警告色）
            bar_width = self.radius * 2
            # 体力低于30%时耐力条底色变为黄色警告
            bg_color = YELLOW if (self.stamina / self.max_stamina) < self.critical_stamina_ratio else RED
            pygame.draw.rect(surface, bg_color, (screen_x - self.radius, screen_y - self.radius - 10, 
                                            bar_width, 5))
            pygame.draw.rect(surface, GREEN, (screen_x - self.radius, screen_y - self.radius - 10, 
                                            bar_width * (self.stamina / self.max_stamina), 5))
            
            # 状态视觉提示
            if self.is_charging:
                pygame.draw.circle(surface, (255, 100, 100), (int(screen_x), int(screen_y)), self.radius + 5, 2)
            elif self.is_running:
                pygame.draw.circle(surface, (100, 255, 255), (int(screen_x), int(screen_y)), self.radius + 3, 2)
