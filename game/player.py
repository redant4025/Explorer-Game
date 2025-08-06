import math
import pygame
from config import *
from audio import audio_manager

class Player:
    def __init__(self):
        self.map_x = MAP_WIDTH // 2
        self.map_y = MAP_HEIGHT // 2
        self.angle = 0
        self.base_speed = PLAYER_SPEED  # 基础速度，用于动态计算
        self.speed = self.base_speed    # 当前速度
        self.rotation_speed = PLAYER_ROTATION_SPEED
        self.energy = PLAYER_INIT_ENERGY
        self.max_energy = PLAYER_MAX_ENERGY  # 已修改为400
        self.base_radius = PLAYER_RADIUS  # 基础半径，用于动态计算
        self.radius = self.base_radius    # 当前半径
        # 鼠标控制相关
        self.mouse_target_angle = 0  # 鼠标指向的目标角度
        # 移动轨迹记录
        self.last_positions = []
        self.max_position_history = 5
        
        # 冲刺相关属性
        self.is_dashing = False  # 冲刺状态标记
        self.dash_timer = 0      # 冲刺计时器
        
        # 初始化时更新一次体型和速度
        self.update_size_and_speed()
            
    def update_position_history(self):
        """记录玩家位置历史，用于狩猎者预测移动轨迹"""
        self.last_positions.append((self.map_x, self.map_y))
        if len(self.last_positions) > self.max_position_history:
            self.last_positions.pop(0)
            
    def get_movement_vector(self):
        """获取玩家移动向量（基于最近位置）"""
        if len(self.last_positions) < 2:
            # 没有足够历史，使用当前角度计算
            rad = math.radians(self.angle)
            return (math.cos(rad) * self.get_current_speed(), math.sin(rad) * self.get_current_speed())
            
        # 计算平均移动向量
        total_dx = 0
        total_dy = 0
        for i in range(1, len(self.last_positions)):
            total_dx += self.last_positions[i][0] - self.last_positions[i-1][0]
            total_dy += self.last_positions[i][1] - self.last_positions[i-1][1]
            
        avg_dx = total_dx / (len(self.last_positions) - 1)
        avg_dy = total_dy / (len(self.last_positions) - 1)
        
        # 归一化并应用速度
        speed = math.sqrt(avg_dx**2 + avg_dy**2)
        if speed > 0:
            avg_dx = (avg_dx / speed) * self.get_current_speed()
            avg_dy = (avg_dy / speed) * self.get_current_speed()
            
        return (avg_dx, avg_dy)
    
    def update_size_and_speed(self):
        """根据当前能量更新体型（半径）和速度
           能量=200时：体型是初始的2倍，速度是初始的75%
           能量=400时：体型是初始的3倍，速度是初始的50%
           能量=0时：体型是初始的1倍，速度是初始的150%"""
        # 计算能量比例（0-1之间，基于最大能量400）
        energy_ratio = self.energy / self.max_energy
        energy_ratio = max(0, min(1, energy_ratio))  # 限制在0-1范围
        
        # 体型（半径）计算：基础半径 * (1 + 2 * 能量比例)
        # 能量0时：1倍基础半径，能量200时：2倍，能量400时：3倍
        self.radius = self.base_radius * (1 + 2 * energy_ratio)
        
        # 速度计算：基础速度 * (1.5 - 1 * 能量比例)
        # 能量0时：150%基础速度，能量200时：75%，能量400时：50%
        self.speed = self.base_speed * (SPEED_ENERGY_BASE - SPEED_ENERGY_SCALE * energy_ratio)
    
    def start_dash(self):
        """开始冲刺（能量足够时）"""
        # 能量小于20时无法冲刺
        if self.energy >= 20 and self.energy >= PLAYER_DASH_ENERGY_COST and not self.is_dashing:
            self.is_dashing = True
            self.dash_timer = PLAYER_DASH_DURATION
            self.energy -= PLAYER_DASH_ENERGY_COST  # 消耗冲刺能量
            self.energy = max(0, self.energy)  # 确保不小于0
            audio_manager.play_sound('run') 
            
    
    def update_dash_state(self, delta_time):
        """更新冲刺状态（每帧调用）"""
        if self.is_dashing:
            self.dash_timer -= delta_time
            if self.dash_timer <= 0:
                self.is_dashing = False
    
    def get_current_speed(self):
        """获取当前速度（考虑冲刺状态）"""
        if self.is_dashing:
            return self.speed * PLAYER_DASH_SPEED_MULTIPLIER
        return self.speed
        
    def rotate(self, direction, delta_time):
        # 旋转角度 = 旋转速度（度/秒）* 方向 * 时间（秒）
        self.angle += direction * self.rotation_speed * delta_time
        self.angle %= 360
        
    def rotate_towards_mouse(self, delta_time):
        """朝着鼠标指针方向旋转（基于时间）"""
        angle_diff = (self.mouse_target_angle - self.angle) % 360
        
        # 选择最短旋转方向
        if angle_diff < 180:
            rotate_amount = min(self.rotation_speed * delta_time, angle_diff)
            self.angle += rotate_amount
        else:
            rotate_amount = min(self.rotation_speed * delta_time, 360 - angle_diff)
            self.angle -= rotate_amount
            
        self.angle %= 360
        
    def move_forward(self, delta_time):
        # 移动距离 = 速度（像素/秒）* 时间（秒）
        rad = math.radians(self.angle)
        # 使用冲刺速度或普通速度
        current_speed = self.get_current_speed()
        dx = math.cos(rad) * current_speed * delta_time
        dy = math.sin(rad) * current_speed * delta_time
        
        self.map_x = max(self.radius, min(MAP_WIDTH - self.radius, self.map_x + dx))
        self.map_y = max(self.radius, min(MAP_HEIGHT - self.radius, self.map_y + dy))
        
        # 能量消耗 = 每秒消耗 * 时间（秒）
        self.energy -= PLAYER_FORWARD_ENERGY_COST * delta_time
        self.energy = max(0, self.energy)
        
        self.update_position_history()
        self.update_size_and_speed()  # 更新体型和速度
                
    def eat(self, food_value):
        self.energy = min(self.max_energy, self.energy + food_value)
        self.update_size_and_speed()  # 更新体型和速度
            
    def lose_energy_over_time(self, delta_time):
        # 随时间消耗能量
        self.energy -= PLAYER_ENERGY_LOSS_RATE * delta_time
        self.energy = max(0, self.energy)
        self.update_size_and_speed()  # 更新体型和速度
            
    def is_alive(self):
        return self.energy > 0
        

    def draw(self, surface):
        screen_x = WINDOW_WIDTH // 2
        screen_y = WINDOW_HEIGHT // 2
        
        # 冲刺状态的视觉效果
        if self.is_dashing:
            # 绘制冲刺轨迹/特效
            trail_color = (200, 200, 255, 100)  # 半透明白色
            for i in range(1, len(self.last_positions)):
                # 转换历史位置到屏幕坐标
                prev_screen_x = WINDOW_WIDTH // 2 + (self.last_positions[i-1][0] - self.map_x)
                prev_screen_y = WINDOW_HEIGHT // 2 + (self.last_positions[i-1][1] - self.map_y)
                curr_screen_x = WINDOW_WIDTH // 2 + (self.last_positions[i][0] - self.map_x)
                curr_screen_y = WINDOW_HEIGHT // 2 + (self.last_positions[i][1] - self.map_y)
                
                # 绘制轨迹线
                pygame.draw.line(
                    surface,
                    trail_color,
                    (prev_screen_x, prev_screen_y),
                    (curr_screen_x, curr_screen_y),
                    int(self.radius * 0.5)
                )
        
        # 绘制探索者主体 - 可爱的圆形身体
        body_color = (100, 180, 255)  # 浅蓝色身体
        if self.is_dashing:
            body_color = (150, 200, 255)  # 冲刺时颜色更亮
            
        pygame.draw.circle(surface, body_color, (screen_x, screen_y), self.radius)
        
        # 绘制高光，增加立体感
        highlight_radius = self.radius * 0.3
        highlight_offset_x = self.radius * 0.2
        highlight_offset_y = -self.radius * 0.2
        pygame.draw.circle(
            surface, 
            (200, 220, 255),  # 高光颜色
            (screen_x + highlight_offset_x, screen_y + highlight_offset_y), 
            highlight_radius
        )
        
        # 绘制眼睛 - 随旋转方向看
        eye_size = self.radius * 0.25
        eye_offset = self.radius * 0.5
        
        # 计算眼睛位置（基于当前角度）
        rad = math.radians(self.angle)
        left_eye_x = screen_x + math.cos(rad + math.radians(30)) * eye_offset
        left_eye_y = screen_y + math.sin(rad + math.radians(30)) * eye_offset
        right_eye_x = screen_x + math.cos(rad - math.radians(30)) * eye_offset
        right_eye_y = screen_y + math.sin(rad - math.radians(30)) * eye_offset
        
        # 白色眼白
        pygame.draw.circle(surface, (255, 255, 255), (left_eye_x, left_eye_y), eye_size)
        pygame.draw.circle(surface, (255, 255, 255), (right_eye_x, right_eye_y), eye_size)
        
        # 黑色瞳孔（看向移动方向）
        pupil_size = eye_size * 0.6
        pupil_offset = eye_size * 0.3
        left_pupil_x = left_eye_x + math.cos(rad) * pupil_offset
        left_pupil_y = left_eye_y + math.sin(rad) * pupil_offset
        right_pupil_x = right_eye_x + math.cos(rad) * pupil_offset
        right_pupil_y = right_eye_y + math.sin(rad) * pupil_offset
        
        pygame.draw.circle(surface, (0, 0, 0), (left_pupil_x, left_pupil_y), pupil_size)
        pygame.draw.circle(surface, (0, 0, 0), (right_pupil_x, right_pupil_y), pupil_size)
        
        # 绘制小亮点，让眼睛更有神
        pygame.draw.circle(
            surface, 
            (255, 255, 255), 
            (left_pupil_x - pupil_size * 0.3, left_pupil_y - pupil_size * 0.3), 
            pupil_size * 0.2
        )
        pygame.draw.circle(
            surface, 
            (255, 255, 255), 
            (right_pupil_x - pupil_size * 0.3, right_pupil_y - pupil_size * 0.3), 
            pupil_size * 0.2
        )
        
        # 绘制可爱的小嘴巴（根据方向变化）
        mouth_size = self.radius * 0.3
        mouth_offset = self.radius * 0.4
        mouth_x = screen_x + math.cos(rad) * mouth_offset
        mouth_y = screen_y + math.sin(rad) * mouth_offset
        
        # 微笑的弧线
        mouth_start_angle = rad + math.radians(30)
        mouth_end_angle = rad - math.radians(30)
        pygame.draw.arc(
            surface, 
            (255, 100, 100),  # 粉红色嘴巴
            (
                mouth_x - mouth_size/2, 
                mouth_y - mouth_size/2, 
                mouth_size, 
                mouth_size/2
            ), 
            mouth_start_angle, 
            mouth_end_angle, 
            int(self.radius * 0.08)
        )
        
        # 绘制天线/触角，增加可爱度
        antenna_length = self.radius * 0.6
        antenna_x = screen_x + math.cos(rad) * (self.radius * 0.3)
        antenna_y = screen_y + math.sin(rad) * (self.radius * 0.3)
        
        # 天线主干
        pygame.draw.line(
            surface, 
            (80, 80, 180),  # 深蓝色天线
            (antenna_x, antenna_y),
            (
                antenna_x + math.cos(rad) * antenna_length,
                antenna_y + math.sin(rad) * antenna_length
            ),
            int(self.radius * 0.1)
        )
        
        # 天线顶端小球
        pygame.draw.circle(
            surface, 
            (255, 200, 100),  # 黄色小球
            (
                antenna_x + math.cos(rad) * antenna_length,
                antenna_y + math.sin(rad) * antenna_length
            ),
            self.radius * 0.15
        )
        
        # 绘制头顶能量条（保持原样）
        bar_x = screen_x - PLAYER_ENERGY_BAR_WIDTH // 2
        bar_y = screen_y - self.radius - PLAYER_ENERGY_BAR_OFFSET  # 能量条位置随体型调整
        
        pygame.draw.rect(
            surface, 
            ENERGY_BAR_BACKGROUND, 
            (bar_x, bar_y, PLAYER_ENERGY_BAR_WIDTH, PLAYER_ENERGY_BAR_HEIGHT)
        )
        
        energy_ratio = self.energy / self.max_energy
        energy_ratio = max(0, min(1, energy_ratio))
        
        if energy_ratio > 0.5:
            red = int(255 * (1 - (energy_ratio - 0.5) * 2))
            green = 255
        else:
            red = 255
            green = int(255 * (energy_ratio * 2))
        
        bar_color = (red, green, 0)
        pygame.draw.rect(
            surface, 
            bar_color, 
            (bar_x, bar_y, PLAYER_ENERGY_BAR_WIDTH * energy_ratio, PLAYER_ENERGY_BAR_HEIGHT)
        )
