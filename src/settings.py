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
current_dir = os.path.dirname(__file__)
base_dir = os.path.abspath(os.path.join(current_dir, '..', 'assets'))

# Icon và hình nền
icon = pygame.image.load(os.path.join(base_dir, "images", "icon_screen.jpg"))
pygame.display.set_icon(icon)
background = pygame.image.load(os.path.join(base_dir, "images", "icon_screen.jpg"))
resized_background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Thiết lập lưới
cols, rows = 6,5
square_size = 30
spacing = 5

# Âm thanh
background_music = pygame.mixer.Sound(os.path.join(base_dir, "sounds", "startms.mp3"))
click_sound = pygame.mixer.Sound(os.path.join(base_dir, "sounds", "click.mp3"))
match_sound = pygame.mixer.Sound(os.path.join(base_dir, "sounds", "match.mp3"))
complete_sound = pygame.mixer.Sound(os.path.join(base_dir, "sounds", "complete.wav"))
game_over_sound = pygame.mixer.Sound(os.path.join(base_dir, "sounds", "gameover.wav")) 

# Chạy âm thanh
def play_background_music():
    pygame.mixer.Sound.play(background_music, loops=-1)  # loops=-1 để lặp vô hạn
    pygame.mixer.Sound.set_volume(background_music, 0.5)

# Phát âm thanh khi nhấn nút
def play_click_sound():
    pygame.mixer.Sound.play(click_sound)
    pygame.mixer.Sound.set_volume(click_sound, 0.7)  # Âm lượng 70%

# Phát âm thanh khi match
def play_match_sound():
    pygame.mixer.Sound.play(match_sound)
    pygame.mixer.Sound.set_volume(match_sound, 0.7)  # Âm lượng 70%

# Phát âm thanh khi thắng
def play_complete_sound():
    pygame.mixer.Sound.play(complete_sound)
    pygame.mixer.Sound.set_volume(complete_sound, 0.7)  # Âm lượng 70%

# Phát âm thanh khi thua
def play_gameover_sound():
    pygame.mixer.Sound.play(game_over_sound)
    pygame.mixer.Sound.set_volume(game_over_sound, 0.7)  # Âm lượng 70%
    
# Dừng nhạc nền
def stop_background_music():
    pygame.mixer.Sound.stop(background_music)

# Hình ảnh cho khối
image_list = []
image_file = [os.path.join(base_dir, "images", f"img{i}.jpg") for i in range(1, 5)]
for img_f in image_file:
    img = pygame.image.load(img_f)
    img = pygame.transform.scale(img, (square_size, square_size))
    image_list.append(img)

def reset_game():
    from player import update_grid_position
    global rows, cols
    rows, cols = 5, 6  # Reset số hàng, cột
    update_grid_position(SCREEN_WIDTH, SCREEN_HEIGHT)  # Cập nhật lại vị trí grid


def home_page():
    play_background_music()
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
                    play_click_sound()
                    print("Đã nhấn vào bắt đầu")
                    reset_game()  # Reset màn chơi trước khi bắt đầu
                    game_state = "play"
                    return
                if button_setting.collidepoint(event.pos):
                    play_click_sound()
                    print("Đã nhấn cài đặt")
                    
                if button_account.collidepoint(event.pos):
                    play_click_sound()
                    print("Đã nhấn tài khoản")