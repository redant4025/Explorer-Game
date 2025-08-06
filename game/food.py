# food.py
import random
import math
import pygame
from config import *

class Food:
    def __init__(self):
        self.radius = FOOD_RADIUS
        self.value = random.randint(FOOD_MIN_VALUE, FOOD_MAX_VALUE)
        self.map_x = 0
        self.map_y = 0
        
    def respawn(self, player=None):
        """在整个10000x10000地图范围内随机生成"""
        # 随机生成全地图范围内的坐标
        self.map_x = random.randint(self.radius, MAP_WIDTH - self.radius)
        self.map_y = random.randint(self.radius, MAP_HEIGHT - self.radius)
        
        # 如果传入了玩家，确保不会生成在玩家身上
        if player:
            while True:
                dx = self.map_x - player.map_x
                dy = self.map_y - player.map_y
                if math.sqrt(dx*dx + dy*dy) > player.radius + self.radius:
                    break
                # 太近则重新生成
                self.map_x = random.randint(self.radius, MAP_WIDTH - self.radius)
                self.map_y = random.randint(self.radius, MAP_HEIGHT - self.radius)
        
    def draw(self, surface, player):
        screen_x = self.map_x - player.map_x + WINDOW_WIDTH // 2
        screen_y = self.map_y - player.map_y + WINDOW_HEIGHT // 2
        
        if -self.radius <= screen_x <= WINDOW_WIDTH + self.radius and -self.radius <= screen_y <= WINDOW_HEIGHT + self.radius:
            color = (255, 255 - min(self.value * 10, 255), 0)
            pygame.draw.circle(surface, color, (int(screen_x), int(screen_y)), self.radius)