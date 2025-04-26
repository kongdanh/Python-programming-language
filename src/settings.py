import pygame
import os
import pygame.freetype
import random
import sys
import json
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

# Khởi tạo pygame
pygame.init()

# Kích thước màn hình
SCREEN_WIDTH, SCREEN_HEIGHT = 500, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Đồ án Python")

# Màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (50, 50, 50)
GREEN = (0, 128, 0)  # Màu xanh lá cho trạng thái bật âm lượng
RED = (255, 0, 0)    # Màu đỏ cho trạng thái tắt âm lượng
square_manager = None

# Chữ
font = pygame.font.Font(None, 36)

# Định nghĩa các nút
button_start = pygame.Rect(SCREEN_WIDTH // 2 - 100, 250, 200, 50)
button_music = pygame.Rect(SCREEN_WIDTH // 2 - 100, 320, 200, 50)

# Nút trong trạng thái "Lose"
button_retry = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 70, 200, 50)
button_home_lose = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 130, 200, 50)

# Biến trạng thái âm lượng (True: bật, False: tắt)
sound_enabled = True

# Đường dẫn cố định
current_dir = os.path.dirname(__file__)
base_dir = os.path.abspath(os.path.join(current_dir, '..', 'assets'))
HIGHSCORE_FILE = os.path.join(base_dir, "highscores.json")
MAX_HIGHSCORES = 5

# Vẽ các nút
def draw_button(button, text, color=GRAY):
    pygame.draw.rect(screen, color, button, border_radius=10)
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=button.center)
    screen.blit(text_surface, text_rect)

# Icon và hình nền
icon = pygame.image.load(os.path.join(base_dir, "images", "icon_screen.jpg"))
pygame.display.set_icon(icon)
background = pygame.image.load(os.path.join(base_dir, "images", "icon_screen.jpg"))
resized_background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Thiết lập lưới
cols, rows = 6, 5
square_size = 50
spacing = 5

# Âm thanh
background_music = pygame.mixer.Sound(os.path.join(base_dir, "sounds", "startms.mp3"))
click_sound = pygame.mixer.Sound(os.path.join(base_dir, "sounds", "click.mp3"))
match_sound = pygame.mixer.Sound(os.path.join(base_dir, "sounds", "match.mp3"))
complete_sound = pygame.mixer.Sound(os.path.join(base_dir, "sounds", "complete.wav"))
game_over_sound = pygame.mixer.Sound(os.path.join(base_dir, "sounds", "gameover.wav")) 

# Chạy âm thanh
def play_background_music():
    if sound_enabled:
        pygame.mixer.Sound.play(background_music, loops=-1)
        pygame.mixer.Sound.set_volume(background_music, 0.5)

def play_click_sound():
    if sound_enabled:
        pygame.mixer.Sound.play(click_sound)
        pygame.mixer.Sound.set_volume(click_sound, 0.7)

def play_match_sound():
    if sound_enabled:
        pygame.mixer.Sound.play(match_sound)
        pygame.mixer.Sound.set_volume(match_sound, 0.7)

def play_complete_sound():
    if sound_enabled:
        pygame.mixer.Sound.play(complete_sound)
        pygame.mixer.Sound.set_volume(complete_sound, 0.7)

def play_gameover_sound():
    if sound_enabled:
        pygame.mixer.Sound.play(game_over_sound)
        pygame.mixer.Sound.set_volume(game_over_sound, 0.7)

def stop_background_music():
    pygame.mixer.Sound.stop(background_music)

# Hình ảnh cho khối
image_list = []
image_file = [os.path.join(base_dir, "images", f"img{i+1}.png") for i in range(1, 5)]
for img_f in image_file:
    img = pygame.image.load(img_f)
    img = pygame.transform.scale(img, (square_size, square_size))
    image_list.append(img)

def reset_game():
    from player import update_grid_position
    global rows, cols
    update_grid_position(SCREEN_WIDTH, SCREEN_HEIGHT)

# # Hàm để lưu high score
# def save_highscore(score):
#     try:
#         # Đọc danh sách high score hiện có
#         if os.path.exists(HIGHSCORE_FILE):
#             with open(HIGHSCORE_FILE, 'r') as f:
#                 highscores = json.load(f)
#         else:
#             highscores = []
        
#         # Thêm score mới
#         highscores.append({
#             "score": score,
#             "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#         })
        
#         # Sắp xếp và giữ lại chỉ MAX_HIGHSCORES bản ghi
#         highscores.sort(key=lambda x: x["score"], reverse=True)
#         highscores = highscores[:MAX_HIGHSCORES]
        
#         # Lưu lại file
#         with open(HIGHSCORE_FILE, 'w') as f:
#             json.dump(highscores, f, indent=4)
            
#     except Exception as e:
#         print(f"Error saving highscore: {e}")

# # Hàm để hiển thị bảng high score
# def show_highscores():
#     try:
#         # Đọc high scores từ file
#         if os.path.exists(HIGHSCORE_FILE):
#             with open(HIGHSCORE_FILE, 'r') as f:
#                 highscores = json.load(f)
#         else:
#             highscores = []
            
#         # Tạo surface cho popup
#         popup_width = 400
#         popup_height = 400
#         popup = pygame.Surface((popup_width, popup_height), pygame.SRCALPHA)
#         popup.fill((50, 50, 50, 200))
#         pygame.draw.rect(popup, (200, 200, 200), (0, 0, popup_width, popup_height), border_radius=10)
#         pygame.draw.rect(popup, (0, 0, 0), (0, 0, popup_width, popup_height), 2, border_radius=10)
        
#         # Vẽ tiêu đề
#         title_font = pygame.font.Font(None, 36)
#         title_text = title_font.render("HIGH SCORES", True, (0, 0, 0))
#         popup.blit(title_text, (popup_width//2 - title_text.get_width()//2, 20))
        
#         # Vẽ từng high score
#         score_font = pygame.font.Font(None, 28)
#         if not highscores:
#             no_scores = score_font.render("No highscores yet!", True, (0, 0, 0))
#             popup.blit(no_scores, (popup_width//2 - no_scores.get_width()//2, 100))
#         else:
#             for i, entry in enumerate(highscores):
#                 score_text = score_font.render(f"{i+1}. {entry['score']} - {entry['date']}", True, (0, 0, 0))
#                 popup.blit(score_text, (40, 80 + i*40))
        
#         # Vẽ nút đóng
#         close_button = pygame.Rect(popup_width//2 - 50, popup_height - 60, 100, 40)
#         pygame.draw.rect(popup, (150, 150, 150), close_button, border_radius=5)
#         pygame.draw.rect(popup, (0, 0, 0), close_button, 2, border_radius=5)
#         close_text = score_font.render("Close", True, (0, 0, 0))
#         popup.blit(close_text, (close_button.centerx - close_text.get_width()//2, 
#                                close_button.centery - close_text.get_height()//2))
        
#         # Hiển thị popup
#         popup_rect = popup.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
#         screen.blit(popup, popup_rect)
#         pygame.display.flip()
        
#         # Chờ người dùng nhấn nút đóng
#         waiting = True
#         while waiting:
#             for event in pygame.event.get():
#                 if event.type == pygame.QUIT:
#                     pygame.quit()
#                     exit()
#                 if event.type == pygame.MOUSEBUTTONDOWN:
#                     mouse_pos = pygame.mouse.get_pos()
#                     # Tính toán lại vị trí nút đóng trên màn hình
#                     screen_close_button = close_button.move(popup_rect.topleft)
#                     if screen_close_button.collidepoint(mouse_pos):
#                         play_click_sound()
#                         waiting = False
    
#     except Exception as e:
#         print(f"Error showing highscores: {e}")

def home_page():
    global sound_enabled
    play_background_music()
    while True:
        screen.fill(WHITE)
        screen.blit(resized_background, (0, 0))

        text = font.render("Tiledom", True, BLACK)
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2 - 200))

        draw_button(button_start, "START")
        
        # Vẽ nút music với trạng thái hiện tại (ON/OFF)
        music_text = "MUSIC: ON" if sound_enabled else "MUSIC: OFF"
        music_color = GREEN if sound_enabled else RED
        draw_button(button_music, music_text, music_color)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_start.collidepoint(event.pos):
                    play_click_sound()
                    print("Đã nhấn vào bắt đầu")
                    reset_game()
                    game_state = "play"
                    return
                if button_music.collidepoint(event.pos):
                    play_click_sound()
                    # Bật/tắt âm thanh
                    sound_enabled = not sound_enabled
                    if sound_enabled:
                        play_background_music()
                    else:
                        stop_background_music()

def lose():
    global game_state
    game_state = "lose"
    play_gameover_sound()
    #save_highscore(square_manager.score)  # Lưu điểm khi thua

    box_rect = pygame.Rect(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 3, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)

    while True:
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        pygame.draw.rect(screen, (255, 255, 255), box_rect, border_radius=10)
        pygame.draw.rect(screen, (0, 0, 0), box_rect, 3, border_radius=10)

        text = font.render("Game Over", True, (0, 0, 0))
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - 20))

        draw_button(button_retry, "Chơi lại")
        draw_button(button_home_lose, "Trang chủ")

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_retry.collidepoint(event.pos):
                    play_click_sound()
                    reset_game()
                    return "play"
                if button_home_lose.collidepoint(event.pos):
                    play_click_sound()
                    return "home"