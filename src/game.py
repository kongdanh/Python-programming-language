import pygame
import random
import os
from settings import draw_button, screen, resized_background, SCREEN_WIDTH, SCREEN_HEIGHT, home_page, reset_game, font, image_list, play_click_sound, play_match_sound, play_complete_sound, play_gameover_sound, base_dir
from player import squares, update_grid_position

# Khởi tạo Pygame
pygame.init()

#
UNDO_IMAGE_PATH = os.path.join(base_dir, "images", "undo.jpg")
RESET_IMAGE_PATH = os.path.join(base_dir, "images", "Reset.jpg")

try:
    undo_image = pygame.image.load(UNDO_IMAGE_PATH).convert_alpha()
    reset_image = pygame.image.load(RESET_IMAGE_PATH).convert_alpha()
except pygame.error as e:
    print(f"Không thể tải hình ảnh: {e}")
    undo_image = None
    reset_image = None

# Cấu hình nút tròn
BUTTON_RADIUS = 20
BUTTON_SPACING = 20
CENTER_X = SCREEN_WIDTH // 2
BUTTON_Y = SCREEN_HEIGHT - 120

# Cấu hình chữ số lượt
COUNTER_TEXT_COLOR = (255, 255, 255)
COUNTER_FONT_SIZE = 20
counter_font = pygame.font.Font(None, COUNTER_FONT_SIZE)

class Square:
    def __init__(self, image, rect):
        self.image = image
        self.rect = pygame.Rect(rect)

    def draw(self):
        # Vẽ hình ảnh với kích thước 30x30
        scaled_image = pygame.transform.scale(self.image, (30, 30))
        screen.blit(scaled_image, self.rect.topleft)

class SquareManager:
    def __init__(self):
        self.selected_squares = []
        self.max_selected = 7
        self.history = []
        self.undo_limit = 3
        self.undo_count = 0

    def add_square(self, square):
        if square not in self.selected_squares and len(self.selected_squares) < self.max_selected:
            self.history.append(("add", square))
            self.selected_squares.append(square)
            self.update_selected_position()
            if len(self.selected_squares) == self.max_selected and not self.check_match():
                print("Khung đầy và không có match, thua game!")
                return False
            self.check_match()
            return True
        return True

    def update_selected_position(self):
        start_x, start_y, spacing = 115, 540, 40
        for i, square in enumerate(self.selected_squares):
            square.rect.x = start_x + i * spacing
            square.rect.y = start_y

    def check_match(self):
        img_count = {}
        for square in self.selected_squares:
            img_count[square.image] = img_count.get(square.image, 0) + 1

        matched_images = {img for img, count in img_count.items() if count >= 3}

        if matched_images:
            play_match_sound()
            removed_squares = [sq for sq in self.selected_squares if sq.image in matched_images]
            self.history.append(("remove", list(removed_squares)))
            self.selected_squares = [sq for sq in self.selected_squares if sq.image not in matched_images]
            self.update_selected_position()
            self.undo_count = max(0, self.undo_count - len(removed_squares))
            return True
        return False

    def draw_selected_squares(self):
        for square in self.selected_squares:
            square.draw()

    def undo(self):
        if self.history and self.undo_count < self.undo_limit:
            last_action, data = self.history.pop()
            if last_action == "add":
                if self.selected_squares and self.selected_squares[-1] == data:
                    self.selected_squares.pop()
                    self.update_selected_position()
                    self.undo_count += 1
            elif last_action == "remove":
                self.selected_squares.extend(data)
                self.update_selected_position()
                self.undo_count += len(data)

def draw_circular_button(screen, image, center_x, center_y, radius, active=True, counter_text=None):
    if image:
        scaled_image = pygame.transform.scale(image, (radius * 2, radius * 2))
        rect = scaled_image.get_rect(center=(center_x, center_y))
        mask = pygame.mask.from_surface(scaled_image)
        surface_to_blit = pygame.Surface(rect.size, pygame.SRCALPHA)
        for x in range(rect.width):
            for y in range(rect.height):
                if mask.get_at((x, y)):
                    surface_to_blit.set_at((x, y), scaled_image.get_at((x, y)))
        screen.blit(surface_to_blit, rect)

    if active and counter_text is not None:
        text_surface = counter_font.render(counter_text, True, COUNTER_TEXT_COLOR)
        text_rect = text_surface.get_rect(center=(center_x, center_y + radius + 15))
        screen.blit(text_surface, text_rect)
    elif not active and counter_text is not None:
        text_surface = counter_font.render(counter_text, True, (128, 128, 128))
        text_rect = text_surface.get_rect(center=(center_x, center_y + radius + 15))
        screen.blit(text_surface, text_rect)

def lose():
    global game_state
    game_state = "lose"
    play_gameover_sound()

def draw_ui():
    pygame.draw.rect(screen, (255, 255, 255), (105, 530, 290, 50), 2)

square_manager = SquareManager()
reset_available = True

def generate_random_squares(num_squares):
    global squares
    squares = []
    available_positions = set()
    grid_width = 5
    grid_height = 6
    for r in range(grid_height):
        for c in range(grid_width):
            available_positions.add((c, r, 0))

    image_choices = random.choices(image_list, k=num_squares)

    for img in image_choices:
        if not available_positions:
            break
        position = random.choice(list(available_positions))
        col, row, layer = position
        x = (SCREEN_WIDTH - (5 * 30 + 4 * 5)) // 2 + col * (30 + 5)
        y = (SCREEN_HEIGHT - (6 * 30 + 5 * 5)) // 3 + row * (30 + 5)
        squares.append({"rect": pygame.Rect(x, y, 30, 30), "image": img})
        available_positions.discard(position)
        if layer == 0:
            available_positions.discard((col, row, 1))

def move_square_to_selected(square_data, target_rect, animation_duration=500):
    start_rect = pygame.Rect(square_data["rect"])
    end_rect = pygame.Rect(target_rect)
    start_time = pygame.time.get_ticks()
    moving_square = Square(square_data["image"], start_rect)

    running = True
    while running:
        # Xóa các sự kiện chuột để ngăn nhấn mới
        pygame.event.clear([pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION])
        current_time = pygame.time.get_ticks()
        time_elapsed = current_time - start_time
        if time_elapsed >= animation_duration:
            moving_square.rect = end_rect
            running = False
        else:
            progress = time_elapsed / animation_duration
            new_x = start_rect.x + (end_rect.x - start_rect.x) * progress
            new_y = start_rect.y + (end_rect.y - start_rect.y) * progress
            moving_square.rect.x = int(new_x)
            moving_square.rect.y = int(new_y)

        screen.blit(resized_background, (0, 0))
        for sq in squares:
            if sq != square_data:
                screen.blit(sq["image"], sq["rect"].topleft)
        draw_ui()
        square_manager.draw_selected_squares()
        moving_square.draw()
        pygame.display.flip()
        pygame.time.Clock().tick(120)

def reset_board():
    global squares, reset_available, game_state
    if reset_available:
        play_click_sound()
        squares = []
        generate_random_squares(30)
        square_manager.selected_squares = []
        square_manager.history = []
        square_manager.undo_count = 0
        reset_available = False
        game_state = "play"

def run_game():
    global game_state, squares, reset_available
    running = True
    dragging = None
    offset_x, offset_y = 0, 0
    mouse_moved = False
    game_state = "home"
    selected_a_square = None
    dragging_original_index = None

    # Vị trí nút Undo (bên trái)
    undo_button_center_x = CENTER_X - BUTTON_RADIUS - BUTTON_SPACING // 2
    # Vị trí nút Reset (bên phải)
    reset_button_center_x = CENTER_X + BUTTON_RADIUS + BUTTON_SPACING // 2
    undo_button_center_y = BUTTON_Y
    reset_button_center_y = BUTTON_Y

    undo_button_rect = pygame.Rect(undo_button_center_x - BUTTON_RADIUS, undo_button_center_y - BUTTON_RADIUS, BUTTON_RADIUS * 2, BUTTON_RADIUS * 2)
    reset_button_rect = pygame.Rect(reset_button_center_x - BUTTON_RADIUS, reset_button_center_y - BUTTON_RADIUS, BUTTON_RADIUS * 2, BUTTON_RADIUS * 2)

    while running:
        screen.blit(resized_background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if game_state == "home":
                reset_game()
                home_page()
                generate_random_squares(30)
                square_manager.undo_count = 0
                reset_available = True
                game_state = "play"

            elif game_state == "play":
                if event.type == pygame.MOUSEBUTTONDOWN and dragging is None:
                    mouse_pos = event.pos
                    mouse_moved = False
                    # Lặp qua squares theo thứ tự ngược để ưu tiên ô trên cùng
                    for i, square in enumerate(reversed(squares)):
                        if square["rect"].collidepoint(mouse_pos):
                            dragging = Square(square["image"], square["rect"].copy())
                            dragging_original_index = len(squares) - 1 - i
                            offset_x = mouse_pos[0] - square["rect"].x
                            offset_y = mouse_pos[1] - square["rect"].y
                            selected_a_square = {
                                "rect": square["rect"].copy(),
                                "image": square["image"]
                            }
                            break
                    # Kiểm tra nút Reset
                    if reset_image and reset_button_rect.collidepoint(mouse_pos) and reset_available:
                        reset_board()
                    # Kiểm tra nút Undo
                    if undo_image and undo_button_rect.collidepoint(mouse_pos) and square_manager.undo_count < square_manager.undo_limit:
                        play_click_sound()
                        square_manager.undo()

                if event.type == pygame.MOUSEMOTION and dragging:
                    mouse_moved = True
                    dragging.rect.x = event.pos[0] - offset_x
                    dragging.rect.y = event.pos[1] - offset_y

                if event.type == pygame.MOUSEBUTTONUP and dragging:
                    if not mouse_moved:
                        if len(square_manager.selected_squares) < square_manager.max_selected and selected_a_square is not None and dragging_original_index is not None and 0 <= dragging_original_index < len(squares):
                            play_click_sound()
                            target_x = 115 + len(square_manager.selected_squares) * 40
                            target_y = 540
                            target_rect = pygame.Rect(target_x, target_y, 30, 30)
                            move_square_to_selected(selected_a_square, target_rect)
                            del squares[dragging_original_index]
                            if not square_manager.add_square(Square(selected_a_square["image"], target_rect)):
                                lose()
                    # Đặt lại trạng thái
                    dragging = None
                    selected_a_square = None
                    dragging_original_index = None

            elif game_state == "lose":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if button_retry.collidepoint(event.pos):
                        play_click_sound()
                        reset_game()
                        square_manager.selected_squares = []
                        square_manager.history = []
                        square_manager.undo_count = 0
                        reset_available = True
                        generate_random_squares(30)
                        game_state = "play"

        # Vẽ giao diện theo trạng thái
        if game_state == "play":
            for square in squares:
                # Vẽ hình ảnh với kích thước 30x30
                scaled_image = pygame.transform.scale(square["image"], (30, 30))
                screen.blit(scaled_image, square["rect"].topleft)
            draw_ui()
            square_manager.draw_selected_squares()
            if undo_image:
                draw_circular_button(screen, undo_image, undo_button_center_x, undo_button_center_y, BUTTON_RADIUS, square_manager.undo_count < square_manager.undo_limit, str(square_manager.undo_limit - square_manager.undo_count))
            if reset_image:
                draw_circular_button(screen, reset_image, reset_button_center_x, reset_button_center_y, BUTTON_RADIUS, reset_available)

            if not squares:
                overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 180))
                screen.blit(overlay, (0, 0))
                box_rect = pygame.Rect(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 3, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)
                pygame.draw.rect(screen, (255, 255, 255), box_rect, border_radius=10)
                pygame.draw.rect(screen, (0, 0, 0), box_rect, 3, border_radius=10)
                play_complete_sound()
                text = font.render("Level complete!", True, (0, 0, 0))
                text_rect = text.get_rect(center=(box_rect.centerx, box_rect.top + 40))
                screen.blit(text, text_rect)

                # Chiều cao dự kiến của nút
                button_height = 40
                # Khoảng cách từ đáy màn hình
                button_margin_bottom = 20
                # Khoảng cách giữa hai nút
                button_spacing = 20
                # Chiều rộng mỗi nút (có thể điều chỉnh)
                button_width = 100

                # Vị trí nút Home (bên trái)
                home_button_rect = pygame.Rect(
                    SCREEN_WIDTH // 2 - button_width - button_spacing // 2,
                    SCREEN_HEIGHT - button_height - button_margin_bottom,
                    button_width,
                    button_height
                )
                draw_button(home_button_rect, "Home")

                # Vị trí nút Reset (bên phải)
                reset_level_button_rect = pygame.Rect(
                    SCREEN_WIDTH // 2 + button_spacing // 2,
                    SCREEN_HEIGHT - button_height - button_margin_bottom,
                    button_width,
                    button_height
                )
                draw_button(reset_level_button_rect, "Reset")

                mouse_pos = pygame.mouse.get_pos()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if home_button_rect.collidepoint(mouse_pos):
                        play_click_sound()
                        game_state = "home"
                    elif reset_level_button_rect.collidepoint(mouse_pos):
                        play_click_sound()
                        reset_board()

        elif game_state == "lose":
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            screen.blit(overlay, (0, 0))
            box_rect = pygame.Rect(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 3, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)
            pygame.draw.rect(screen, (255, 255, 255), box_rect, border_radius=10)
            pygame.draw.rect(screen, (0, 0, 0), box_rect, 3, border_radius=10)
            text = font.render("Game Over", True, (0, 0, 0))
            text_rect = text.get_rect(center=(box_rect.centerx, box_rect.top + 40))
            screen.blit(text, text_rect)
            # Lưu ý: Nút "Retry" vẫn là hình chữ nhật với chữ nhỏ
            button_retry = pygame.Rect(box_rect.centerx - 100, box_rect.centery + 20, 200, 50)
            draw_button(button_retry, "Retry")

        pygame.display.flip()

    pygame.quit()

