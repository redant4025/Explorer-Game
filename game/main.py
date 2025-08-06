import pygame
import sys
import pygame.draw
from config import *
from game import Game

class Button:
    """按钮类，用于创建可交互的按钮"""
    def __init__(self, x, y, width, height, text, font, 
                 bg_color=(100, 100, 100), hover_color=(150, 150, 150), 
                 text_color=(255, 255, 255)):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.text_color = text_color
        self.is_hovered = False

    def draw(self, screen):
        """绘制按钮到屏幕上"""
        # 根据是否悬停选择颜色
        color = self.hover_color if self.is_hovered else self.bg_color
        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2, border_radius=10)  # 边框
        
        # 绘制文本
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def check_hover(self, pos):
        """检查鼠标是否悬停在按钮上"""
        self.is_hovered = self.rect.collidepoint(pos)

    def is_clicked(self, pos):
        """检查按钮是否被点击"""
        return self.rect.collidepoint(pos)

def show_start_screen(screen, font, font_options):
    """显示开始界面，返回用户选择（进入游戏或退出）"""
    # 创建按钮
    button_width = 200
    button_height = 60
    button_y = WINDOW_HEIGHT * 2 // 3
    
    start_button = Button(
        (WINDOW_WIDTH - button_width) // 2,
        button_y,
        button_width,
        button_height,
        "进入游戏",
        font
    )
    
    exit_button = Button(
        (WINDOW_WIDTH - button_width) // 2,
        button_y + button_height + 20,
        button_width,
        button_height,
        "退出游戏",
        font
    )
    
    buttons = [start_button, exit_button]
    
    while True:
        screen.fill((30, 30, 50))  # 深色背景
        
        # 绘制标题
        # 使用传递过来的font_options
        title_font = pygame.font.SysFont(font_options[0], 64) if font_options else pygame.font.Font(None, 64)
        title_surf = title_font.render("探索者", True, (255, 215, 0))  # 金色标题
        title_rect = title_surf.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3))
        screen.blit(title_surf, title_rect)
        
        # 处理事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.MOUSEMOTION:
                # 检查鼠标悬停
                for button in buttons:
                    button.check_hover(event.pos)
                    
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # 左键点击
                    if start_button.is_clicked(event.pos):
                        return "start"
                    if exit_button.is_clicked(event.pos):
                        return "exit"
        
        # 绘制按钮
        for button in buttons:
            button.draw(screen)
        
        pygame.display.flip()

def main():
    # 初始化Pygame
    pygame.init()
    pygame.font.init()
    # 可选添加 pygame.HWSURFACE 硬件加速，或 pygame.DOUBLEBUF 双缓冲
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT),  pygame.HWSURFACE | pygame.DOUBLEBUF, vsync=1)#pygame.FULLSCREEN |

    pygame.display.set_caption("探索者")

    # 字体设置（支持中文）
    font_options = ["SimHei", "WenQuanYi Micro Hei", "Heiti TC", pygame.font.get_default_font()]
    font = None
    for font_name in font_options:
        try:
            font = pygame.font.SysFont(font_name, 24)
            # 测试字体是否支持中文
            if font.render("测试", True, (255, 255, 255)).get_width() > 10:
                break
        except:
            continue
    if not font:
        font = pygame.font.Font(None, 24)

    # 游戏主循环：显示开始界面 -> 运行游戏 -> 回到开始界面
    while True:
        # 将font_options作为参数传递给show_start_screen
        choice = show_start_screen(screen, font, font_options)
        if choice == "start":
            # 启动游戏
            game = Game()
            game.run(screen, font)  # 当game.run()结束时，会返回到开始界面
        elif choice == "exit":
            pygame.quit()
            sys.exit()

if __name__ == "__main__":
    main()
    