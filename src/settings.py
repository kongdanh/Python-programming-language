import pygame
import os
import random
import sys
sys.stdout.reconfigure(encoding='utf-8')

# Khởi tạo pygame
pygame.init()

# Kích thước màn hình
SCREEN_WIDTH, SCREEN_HEIGHT = 500, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Đồ án Python")

# Màu sắc
WHITE = (255,255,255)
BLACK = (0,0,0)
GRAY = (200,200,200)

# Chữ
font = pygame.font.Font(None, 36)

# Trạng thái
game_state = "home"

# Định nghĩa các nút
button_start = pygame.Rect(SCREEN_WIDTH // 2 - 100 , 250, 200, 50)
button_setting = pygame.Rect(SCREEN_WIDTH // 2 - 100, 320, 200, 50)
button_account = pygame.Rect(SCREEN_WIDTH // 2 - 100, 390, 200, 50)

# Vẽ các nút
def draw_button(button, text):
    pygame.draw.rect(screen, GRAY, button, border_radius=10)
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center = button.center)
    screen.blit(text_surface, text_rect)

# Đường dẫn cố định
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__)))

# Icon và hình nền
icon = pygame.image.load(os.path.join(base_dir, "..", "assets", "icon_screen.jpg"))
pygame.display.set_icon(icon)
background = pygame.image.load(os.path.join(base_dir, "..", "assets", "icon_screen.jpg"))
resized_background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Thiết lập lưới
cols, rows = 1,1
square_size = 30
spacing = 5

# Hình ảnh cho khối
image_list = []
image_file = [os.path.join(base_dir, "..", "assets", f"img{i}.jpg") for i in range(1, 5)]
for img_f in image_file:
    img = pygame.image.load(img_f)
    img = pygame.transform.scale(img, (square_size, square_size))
    image_list.append(img)
    
def home_page():
    while True:
        screen.fill(WHITE)  # Đặt nền trắng cho trang chủ

        text = font.render("Tiledom", True, BLACK)
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2,SCREEN_HEIGHT // 2 - text.get_height() // 2 - 200))

        draw_button(button_start, "START")
        draw_button(button_setting, "SETTING")
        draw_button(button_account, "ACCOUNT")
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_start.collidepoint(event.pos):
                    print("Đã nhấn vào bắt đầu")
                    game_state = "play"
                    return
                if button_setting.collidepoint(event.pos):
                    print("Đã nhấn cài đặt")
                    
                if button_account.collidepoint(event.pos):
                    print("Đã nhấn tài khoản")