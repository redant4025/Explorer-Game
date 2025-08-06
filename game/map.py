
import math
import pygame
from config import *


class MinMap:
    def __init__(self, width, height):
        if width > height:
            s = MIN_MAP_SIZE / width;
            self.width = MIN_MAP_SIZE
            self.height = height * s;
        else:
            s = MIN_MAP_SIZE / height;
            self.width = width * s
            self.height = MIN_MAP_SIZE 

        self.margin = 10  # 距离屏幕边缘的边距
        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)



    # 添加小地图绘制方法
    def draw(self, foods, player, screen):
        """绘制小地图，显示玩家和食物位置"""
        # 清空小地图
        self.surface.fill((255, 255, 255, 128))  # 半透黑色背景
       
        # 计算坐标转换比例（游戏世界到小地图）
        scale_x = self.width / MAP_WIDTH
        scale_y = self.height / MAP_HEIGHT

        # 绘制所有食物位置
        for food in foods:
            food_minimap_x = food.map_x * scale_x
            food_minimap_y = food.map_y * scale_y
            # 食物颜色与实际游戏中保持一致
            color = (255, 255 - min(food.value * 10, 255), 0)
            pygame.draw.circle(self.surface, color,
                              (int(food_minimap_x), int(food_minimap_y)), 2)    
        # 绘制玩家位置
        player_minimap_x = player.map_x * scale_x
        player_minimap_y = player.map_y * scale_y
        pygame.draw.circle(self.surface, (0, 255, 255),
                          (int(player_minimap_x), int(player_minimap_y)), 4)

        # 将小地图绘制到屏幕右上角
        screen.blit(self.surface,(WINDOW_WIDTH - self.width - self.margin,self.margin))
    

class Map:
    def draw(self, surface, player):
        """绘制地图网格背景，包含完整边界"""
        player_grid_x = int(player.map_x // GRID_SIZE)
        player_grid_y = int(player.map_y // GRID_SIZE)
    
        # 计算可见网格范围
        half_width = WINDOW_WIDTH // 2
        half_height = WINDOW_HEIGHT // 2
        visible_x_range = half_width // GRID_SIZE + 2
        visible_y_range = half_height // GRID_SIZE + 2
    
        # 绘制水平线（包含地图下边界）
        for i in range(-visible_y_range, visible_y_range + 1):
            grid_y = (player_grid_y + i) * GRID_SIZE
            # 只绘制地图范围内的水平线
            if 0 <= grid_y < MAP_HEIGHT:
                screen_y = grid_y - player.map_y + half_height
                # 计算线的水平范围（限制在地图左右边界内）
                line_start_x = max(0, -player.map_x + half_width)
                line_end_x = min(WINDOW_WIDTH, MAP_WIDTH - player.map_x + half_width)
                pygame.draw.line(
                    surface,
                    GRID_COLOR,
                    (line_start_x, screen_y),
                    (line_end_x, screen_y),
                    GRID_LINE_WIDTH
                )
    
        # 绘制垂直线（包含地图右边界）
        for i in range(-visible_x_range, visible_x_range + 1):
            grid_x = (player_grid_x + i) * GRID_SIZE
            # 只绘制地图范围内的垂直线
            if 0 <= grid_x < MAP_WIDTH:
                screen_x = grid_x - player.map_x + half_width
                # 计算线的垂直范围（限制在地图上下边界内）
                line_start_y = max(0, -player.map_y + half_height)
                line_end_y = min(WINDOW_HEIGHT, MAP_HEIGHT - player.map_y + half_height)
                pygame.draw.line(
                    surface,
                    GRID_COLOR,
                    (screen_x, line_start_y),
                    (screen_x, line_end_y),
                    GRID_LINE_WIDTH
                )
    
        # 绘制地图边界线（确保封边完整）
        # 右边界
        right_boundary_x = MAP_WIDTH - player.map_x + half_width
        if 0 <= right_boundary_x <= WINDOW_WIDTH:
            pygame.draw.line(
                surface,
                BOUNDARY_COLOR,  # 建议用比网格线更深的颜色
                (right_boundary_x, max(0, -player.map_y + half_height)),
                (right_boundary_x, min(WINDOW_HEIGHT, MAP_HEIGHT - player.map_y + half_height)),
                GRID_LINE_WIDTH * 2  # 边界线稍粗
            )
    
        # 下边界
        bottom_boundary_y = MAP_HEIGHT - player.map_y + half_height
        if 0 <= bottom_boundary_y <= WINDOW_HEIGHT:
            pygame.draw.line(
                surface,
                BOUNDARY_COLOR,
                (max(0, -player.map_x + half_width), bottom_boundary_y),
                (min(WINDOW_WIDTH, MAP_WIDTH - player.map_x + half_width), bottom_boundary_y),
                GRID_LINE_WIDTH * 2
            )
