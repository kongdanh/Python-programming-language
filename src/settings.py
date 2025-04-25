import pygame
import os
import pygame.freetype
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
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (50, 50, 50)
GREEN = (0, 128, 0)  # Màu xanh lá cho trạng thái bật âm lượng
RED = (255, 0, 0)    # Màu đỏ cho trạng thái tắt âm lượng

# Chữ
font = pygame.font.Font(None, 36)

# Định nghĩa các nút
button_start = pygame.Rect(SCREEN_WIDTH // 2 - 100, 250, 200, 50)
button_setting = pygame.Rect(SCREEN_WIDTH // 2 - 100, 320, 200, 50)
button_highscore = pygame.Rect(SCREEN_WIDTH // 2 - 100, 390, 200, 50)
button_about = pygame.Rect(SCREEN_WIDTH // 2 - 150, 460, 300, 50)

# Nút trong trạng thái "Lose"
button_retry = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 70, 200, 50)
button_home_lose = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 130, 200, 50)

# Biến trạng thái âm lượng (True: bật, False: tắt)
sound_enabled = True

# Vẽ các nút
def draw_button(button, text, color=GRAY):
    pygame.draw.rect(screen, color, button, border_radius=10)
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=button.center)
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
cols, rows = 6, 5
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
image_file = [os.path.join(base_dir, "images", f"img{i}.jpg") for i in range(1, 5)]
for img_f in image_file:
    img = pygame.image.load(img_f)
    img = pygame.transform.scale(img, (square_size, square_size))
    image_list.append(img)

def reset_game():
    from player import update_grid_position
    global rows, cols
    update_grid_position(SCREEN_WIDTH, SCREEN_HEIGHT)

def settings_page():
    global sound_enabled, rows, cols

    setting_font = pygame.freetype.SysFont('Times New Roman', 24)
    title_font = pygame.freetype.SysFont('Times New Roman', 32)

    box_rect = pygame.Rect(50, 50, SCREEN_WIDTH - 100, SCREEN_HEIGHT - 100)
    close_button = pygame.Rect(box_rect.right - 40, box_rect.top + 10, 30, 30)

    # Nút bật/tắt âm lượng
    sound_button = pygame.Rect(box_rect.left + 50, box_rect.top + 120, 200, 40)
    # Nút chọn kích cỡ lưới
    size_button_5x6 = pygame.Rect(box_rect.left + 50, box_rect.top + 200, 100, 40)
    size_button_6x7 = pygame.Rect(box_rect.left + 170, box_rect.top + 200, 100, 40)
    size_button_7x8 = pygame.Rect(box_rect.left + 290, box_rect.top + 200, 100, 40)

    while True:
        # Lớp phủ mờ
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 100))
        screen.blit(overlay, (0, 0))

        # Vẽ hộp
        pygame.draw.rect(screen, (245, 245, 245), box_rect, border_radius=20)
        pygame.draw.rect(screen, GRAY, box_rect, width=3, border_radius=20)

        # Vẽ nút đóng X
        pygame.draw.rect(screen, (220, 220, 220), close_button, border_radius=8)
        pygame.draw.rect(screen, BLACK, close_button, width=1, border_radius=8)
        x_text, _ = setting_font.render("X", BLACK)
        screen.blit(x_text, x_text.get_rect(center=close_button.center))

        # Tiêu đề
        title_text, _ = title_font.render("CÀI ĐẶT")
        title_rect = title_text.get_rect(center=(box_rect.centerx, box_rect.top + 50))
        screen.blit(title_text, title_rect)

        # Vẽ nhãn và nút âm lượng
        sound_label, _ = setting_font.render("Âm lượng:", DARK_GRAY)
        screen.blit(sound_label, (box_rect.left + 50, box_rect.top + 90))
        sound_status = "ON" if sound_enabled else "OFF"
        sound_color = GREEN if sound_enabled else RED
        draw_button(sound_button, sound_status, sound_color)
        
        pygame.display.flip()

        # Xử lý sự kiện
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if close_button.collidepoint(event.pos):
                    play_click_sound()
                    print("Đã đóng cài đặt")
                    return
                if sound_button.collidepoint(event.pos):
                    play_click_sound()
                    sound_enabled = not sound_enabled
                    if sound_enabled:
                        play_background_music()
                    else:
                        stop_background_music()

def show_guide():
    guide_text = """Tiledom là trò chơi xếp gạch thú vị với lối chơi đơn giản nhưng đầy thách thức. \
Phiên bản rút gọn này giữ nguyên cốt lõi: ghép các ô giống nhau để tạo ô mới và ghi điểm cao nhất. \
Phù hợp để giải trí hoặc rèn luyện tư duy nhanh nhạy!"""

    guide_font = pygame.freetype.SysFont('Times New Roman', 24)
    title_font = pygame.freetype.SysFont('Times New Roman', 32)

    box_rect = pygame.Rect(50, 50, SCREEN_WIDTH - 100, SCREEN_HEIGHT - 100)
    close_button = pygame.Rect(box_rect.right - 40, box_rect.top + 10, 30, 30)

    while True:
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 50))
        screen.blit(overlay, (0, 0))

        pygame.draw.rect(screen, (245, 245, 245), box_rect, border_radius=20)
        pygame.draw.rect(screen, GRAY, box_rect, width=3, border_radius=20)

        pygame.draw.rect(screen, (220, 220, 220), close_button, border_radius=8)
        pygame.draw.rect(screen, BLACK, close_button, width=1, border_radius=8)
        x_text, _ = guide_font.render("X", BLACK)
        screen.blit(x_text, x_text.get_rect(center=close_button.center))

        title_text, _ = title_font.render("HƯỚNG DẪN CHƠI")
        title_rect = title_text.get_rect(center=(box_rect.centerx, box_rect.top + 50))
        screen.blit(title_text, title_rect)

        def draw_text_wrapped(text, rect, font, color):
            words = text.split(' ')
            lines = []
            line = ''
            for word in words:
                test_line = line + word + ' '
                text_surf, _ = font.render(test_line, color)
                if text_surf.get_width() < rect.width - 40:
                    line = test_line
                else:
                    lines.append(line.strip())
                    line = word + ' '
            if line:
                lines.append(line.strip())

            total_height = len(lines) * 35
            y_start = rect.centery - (total_height // 2) + 30

            for i, line in enumerate(lines):
                line_surf, _ = font.render(line, color)
                line_rect = line_surf.get_rect(center=(rect.centerx, y_start + i * 35))
                screen.blit(line_surf, line_rect)

        content_rect = box_rect.inflate(-40, -120)
        draw_text_wrapped(guide_text, content_rect, guide_font, DARK_GRAY)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if close_button.collidepoint(event.pos):
                    play_click_sound()
                    print("Đã nhấn nút đóng")
                    return

def home_page():
    play_background_music()
    while True:
        screen.fill(WHITE)

        text = font.render("Tiledom", True, BLACK)
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2 - 200))

        draw_button(button_start, "START")
        draw_button(button_setting, "SETTING")
        draw_button(button_highscore, "HIGH SCORE")
        draw_button(button_about, "ABOUT THIS GAME")
        
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
                if button_setting.collidepoint(event.pos):
                    play_click_sound()
                    print("Đã nhấn cài đặt")
                    settings_page()
                if button_highscore.collidepoint(event.pos):
                    play_click_sound()
                    print("Đã nhấn high score")
                if button_about.collidepoint(event.pos):
                    play_click_sound()
                    print("Đã nhấn ABOUT THIS GAME")
                    show_guide()

def lose():
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