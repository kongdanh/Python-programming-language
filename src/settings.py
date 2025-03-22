import pygame
import os
import random

# Khởi tạo pygame
pygame.init()

# Kích thước màn hình
SCREEN_WIDTH, SCREEN_HEIGHT = 500, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Đồ án Python")

# Đường dẫn cố định
base_dir = os.path.dirname(os.path.abspath(__file__))

# Icon và hình nền
icon = pygame.image.load(os.path.join(base_dir, "..", "assets", "icon_screen.jpg"))
pygame.display.set_icon(icon)
background = pygame.image.load(os.path.join(base_dir, "..", "assets", "icon_screen.jpg"))
resized_background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Thiết lập lưới
cols, rows = 2, 3
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
        screen.fill((255, 255, 255))  # Đặt nền trắng cho trang chủ

        font = pygame.font.Font(None, 36)
        text = font.render("Tiledom", True, (0, 0, 0))
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            # if event.type == pygame.MOUSEBUTTONDOWN:
            #     return  # Quay lại game khi nhấn chuột
