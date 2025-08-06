import math
import pygame
import sys
import time
from config import *
from player import Player
from hunter import Hunter
from food import Food
from audio import audio_manager
from map import MinMap,Map


class Game:
    def __init__(self):
        """初始化游戏核心组件"""
        # 游戏状态
        self.game_over = False
        self.score = 0
        self.clock = pygame.time.Clock()
        
        # 实体初始化
        self.player = Player()
        self.hunters = self._initialize_hunters()
        self.foods = [Food() for _ in range(FOOD_COUNT)]
        for food in self.foods:
            food.respawn(self.player)
        
        # 输入控制状态
        self.mouse_forward = False
        
        # 音频初始化
        self._init_audio()

        #地图
        self.minimap = MinMap(MAP_WIDTH, MAP_HEIGHT)
        self.map = Map();

    def _init_audio(self):
        """初始化音频系统并加载背景音乐"""
        try:
            pygame.mixer.init()
            pygame.mixer.music.load(BACKGROUND_MUSIC_PATH)
            pygame.mixer.music.set_volume(MUSIC_VOLUME)
            pygame.mixer.music.play(-1)  # 循环播放

        except FileNotFoundError:
            print(f"警告: 未找到背景音乐文件 {BACKGROUND_MUSIC_PATH}，将无背景音乐运行")
        except pygame.error as e:
            print(f"音频初始化错误: {e}")

    def _initialize_hunters(self):
        """初始化狩猎者群体，确保生成位置合理"""
        hunters = []
        existing_hunters = []
        player_center = (MAP_WIDTH // 2, MAP_HEIGHT // 2)
        
        for hunter_id in range(HUNTER_COUNT):
            hunter = Hunter(hunter_id)
            hunter.initialize_position(
                existing_hunters,
                player_center[0],
                player_center[1]
            )
            hunters.append(hunter)
            existing_hunters.append(hunter)
        
        return hunters

    def _handle_mouse_input(self, delta_time):
        """处理鼠标输入控制的移动和旋转"""
        # 鼠标移动控制
        if self.mouse_forward:
            self.player.move_forward(delta_time)
        
        # 鼠标旋转控制
        self.player.rotate_towards_mouse(delta_time)

    def _update_mouse_target_angle(self):
        """更新玩家朝向鼠标指针的目标角度"""
        mouse_x, mouse_y = pygame.mouse.get_pos()
        center_x, center_y = WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2
        
        # 计算鼠标相对屏幕中心的角度
        dx = mouse_x - center_x
        dy = mouse_y - center_y
        self.player.mouse_target_angle = math.degrees(math.atan2(dy, dx)) % 360

    def _check_food_collisions(self):
        """检测玩家与食物的碰撞（吃食物）"""
        for food in self.foods:
            # 使用平方距离优化碰撞检测（避免开方运算）
            dx = self.player.map_x - food.map_x
            dy = self.player.map_y - food.map_y
            if dx * dx + dy * dy < (self.player.radius + food.radius) ** 2:
                self.player.eat(food.value)
                self.score += food.value
                self.foods.remove(food)  # 从列表中彻底删除食物
                audio_manager.play_sound('eat') 

    def _check_hunter_collisions(self):
        """检测玩家与狩猎者的碰撞（游戏结束）"""
        for hunter in self.hunters:
            dx = self.player.map_x - hunter.map_x
            dy = self.player.map_y - hunter.map_y
            if dx * dx + dy * dy < (self.player.radius + hunter.radius) ** 2:
                self.game_over = True
                audio_manager.play_sound('lost') 
                return

    def _draw_game_hud(self, screen, font):
        """绘制游戏头部信息（分数、位置等）"""
        # 分数和位置信息
        score_pos_text = font.render(
            f"分数: {self.score} | 位置: ({int(self.player.map_x)},{int(self.player.map_y)})",
            True, WHITE
        )
        screen.blit(score_pos_text, (10, 10))
        
        # 附近狩猎者数量
        nearby_hunters = sum(
            1 for hunter in self.hunters
            if abs(hunter.map_x - self.player.map_x) < WINDOW_WIDTH//2 + hunter.radius
            and abs(hunter.map_y - self.player.map_y) < WINDOW_HEIGHT//2 + hunter.radius
        )
        hunter_text = font.render(
            f"附近狩猎者: {nearby_hunters}/{HUNTER_COUNT}",
            True, WHITE
        )
        screen.blit(hunter_text, (10, 40))
        
        # 操作说明 - 添加了冲刺提示
        control_text = font.render(
            "鼠标左键: 前进 | 鼠标右键: 冲刺 | ESC: 退出 | R: 重新开始",
            True, WHITE
        )
        screen.blit(control_text, (10, WINDOW_HEIGHT - 30))

    def handle_events(self):
        """处理游戏事件（输入、窗口关闭等）"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                if self.game_over and event.key == pygame.K_r:
                    self.__init__()  # 重启游戏
            
            # 鼠标按键控制 - 新增右键冲刺支持
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # 左键前进
                    self.mouse_forward = True

                if self.mouse_forward and event.button == 3:  # 右键冲刺
                    self.player.start_dash()  # 触发冲刺
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.mouse_forward = False
        
        return True

    def update(self, delta_time):
        """更新游戏状态（每帧调用）"""
        if self.game_over:
            return

        # 新增：检查食物是否已耗尽
        if not self.foods:  # 如果食物列表为空
            self.game_over = True
            # 可以添加胜利音效
            audio_manager.play_sound('win')
            return
        
        # 更新输入相关状态
        self._update_mouse_target_angle()
        
        # 玩家控制与状态更新
        self._handle_mouse_input(delta_time)
        self.player.lose_energy_over_time(delta_time)
        self.player.update_dash_state(delta_time)  # 新增：更新冲刺状态
        
        # 狩猎者AI更新
        for hunter in self.hunters:
            hunter.update(self.player, self.hunters, self.foods, delta_time)
        
        # 碰撞检测
        self._check_food_collisions()
        self._check_hunter_collisions()
        
        # 能量耗尽判定
        if not self.player.is_alive():
            self.game_over = True
            audio_manager.play_sound('lost')

    def draw(self, screen, font):
        """绘制游戏画面（每帧调用）"""
        # 清空屏幕
        screen.fill(BLACK)
        
        # 绘制背景与实体
        self.map.draw(screen, self.player)
        for food in self.foods:
            food.draw(screen, self.player)
        for hunter in self.hunters:
            hunter.draw(screen, self.player)
        self.player.draw(screen)
        # 绘制小地图
        self.minimap.draw(self.foods, self.player, screen)
        # 绘制HUD
        self._draw_game_hud(screen, font)
         # 游戏结束画面（修改部分）
        if self.game_over:
            if not self.foods:  # 检查是否是食物耗尽导致的结束
                over_text = font.render(
                    f"游戏胜利! 分数: {self.score} 按R重开",
                    True, GREEN  # 胜利用绿色
                )
            else:
                over_text = font.render(
                    f"游戏结束! 分数: {self.score} 按R重开",
                    True, RED  # 失败用红色
                )
            text_rect = over_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
            screen.blit(over_text, text_rect)
    
        pygame.display.flip()

    def run(self, screen, font):
        """游戏主循环"""
        running = True
        while running:
            delta_time = self.clock.tick(60) / 1000.0  # 转换为秒
            running = self.handle_events()
            self.update(delta_time)
            self.draw(screen, font)
    