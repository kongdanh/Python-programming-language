
import pygame
import random
import os
import math
from settings import draw_button, screen, resized_background, SCREEN_WIDTH, SCREEN_HEIGHT, home_page, reset_game, font, image_list, play_click_sound, play_match_sound, play_complete_sound, play_gameover_sound, base_dir, square_size, spacing
from player import squares, update_grid_position

# Khởi tạo Pygame
pygame.init()

# Tải hình ảnh
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

    def draw(self, is_top_layer=True):
        scaled_image = pygame.transform.scale(self.image, (square_size, square_size))
        if not is_top_layer:
            scaled_image.set_alpha(128)  # Làm mờ nếu không phải lớp trên cùng
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
        frame_width = 7 * square_size + 6 * spacing
        frame_x = (SCREEN_WIDTH - frame_width) // 2
        frame_y = SCREEN_HEIGHT - (square_size + 40)
        start_x = frame_x + 5
        start_y = frame_y + 5
        for i, square in enumerate(self.selected_squares):
            square.rect.x = start_x + i * (square_size + spacing)
            square.rect.y = start_y
            square.rect.width = square_size
            square.rect.height = square_size

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
            square.draw(is_top_layer=True)

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

def draw_ui():
    frame_width = 7 * square_size + 6 * spacing
    frame_height = square_size + 10
    frame_x = (SCREEN_WIDTH - frame_width) // 2
    frame_y = SCREEN_HEIGHT - frame_height - 30
    pygame.draw.rect(screen, (255, 255, 255), (frame_x, frame_y, frame_width, frame_height), 2)

def lose():
    global game_state
    game_state = "lose"
    play_gameover_sound()

square_manager = SquareManager()
reset_available = True

def generate_random_squares(num_squares):
    global squares
    squares = []
    available_positions = set()
    grid_width = 5
    grid_height = 6
    max_layers = 2  # Chỉ có hai lớp: 0 (dưới), 1 (trên)
    for r in range(grid_height):
        for c in range(grid_width):
            for layer in range(max_layers):
                available_positions.add((c, r, layer))

    image_choices = random.choices(image_list, k=num_squares)

    grid_pixel_width = grid_width * square_size + (grid_width - 1) * spacing
    grid_pixel_height = grid_height * square_size + (grid_height - 1) * spacing
    offset_x = (SCREEN_WIDTH - grid_pixel_width) // 2
    offset_y = (SCREEN_HEIGHT - grid_pixel_height) // 2 - 50

    layer_offset = 10  # Lệch 10px cho lớp trên

    for img in image_choices:
        if not available_positions:
            break
        position = random.choice(list(available_positions))
        col, row, layer = position
        x = offset_x + col * (square_size + spacing)
        y = offset_y + row * (square_size + spacing)
        if layer == 1:  # Lớp trên lệch vị trí
            x += layer_offset
            y += layer_offset
        squares.append({
            "rect": pygame.Rect(x, y, square_size, square_size),
            "image": img,
            "layer": layer,
            "col": col,
            "row": row
        })
        available_positions.discard(position)
        print(f"Generated square: layer={layer}, col={col}, row={row}, x={x}, y={y}")

def move_square_to_selected(square_data, target_rect, squares_state, animation_duration=500):
    global is_animating
    is_animating = True
    start_rect = pygame.Rect(square_data["rect"])
    end_rect = pygame.Rect(target_rect)
    start_time = pygame.time.get_ticks()
    moving_square = Square(square_data["image"], start_rect)

    control_point_x = (start_rect.x + end_rect.x) / 2
    control_point_y = min(start_rect.y, end_rect.y) - 100

    running = True
    while running:
        current_time = pygame.time.get_ticks()
        time_elapsed = current_time - start_time
        if time_elapsed >= animation_duration:
            moving_square.rect = end_rect
            running = False
            for i in range(3):
                screen.blit(resized_background, (0, 0))
                for sq in squares_state:
                    if sq != square_data:
                        scaled_image = pygame.transform.scale(sq["image"], (square_size, square_size))
                        screen.blit(scaled_image, sq["rect"].topleft)
                draw_ui()
                square_manager.draw_selected_squares()
                moving_square.rect.x += (1 if i % 2 == 0 else -1) * 5
                scaled_image = pygame.transform.scale(moving_square.image, (square_size, square_size))
                screen.blit(scaled_image, moving_square.rect.topleft)
                pygame.display.flip()
                pygame.time.wait(50)
            moving_square.rect.x = end_rect.x
        else:
            progress = time_elapsed / animation_duration
            t = progress
            x = (1 - t) ** 2 * start_rect.x + 2 * (1 - t) * t * control_point_x + t ** 2 * end_rect.x
            y = (1 - t) ** 2 * start_rect.y + 2 * (1 - t) * t * control_point_y + t ** 2 * end_rect.y
            moving_square.rect.x = int(x)
            moving_square.rect.y = int(y)

            scale = 1.0 + 0.2 * math.sin(math.pi * progress)
            scaled_size = int(square_size * scale)
            scaled_image = pygame.transform.scale(moving_square.image, (scaled_size, scaled_size))

            rotation = 360 * progress
            rotated_image = pygame.transform.rotate(scaled_image, rotation)
            rotated_rect = rotated_image.get_rect(center=(moving_square.rect.centerx, moving_square.rect.centery))

            alpha = 255 * (1 - 0.3 * math.sin(math.pi * progress))
            rotated_image.set_alpha(int(alpha))

            screen.blit(resized_background, (0, 0))
            for sq in squares_state:
                if sq != square_data:
                    scaled_image = pygame.transform.scale(sq["image"], (square_size, square_size))
                    screen.blit(scaled_image, sq["rect"].topleft)
            draw_ui()
            square_manager.draw_selected_squares()
            screen.blit(rotated_image, rotated_rect.topleft)
            pygame.display.flip()
            pygame.time.Clock().tick(120)
    is_animating = False

def reset_board():
    global squares, reset_available
    if reset_available:
        play_click_sound()
        print("Resetting board")
        squares = []
        generate_random_squares(30)
        square_manager.selected_squares = []
        square_manager.history = []
        square_manager.undo_count = 0
        reset_available = False

def run_game():
    global game_state, squares, reset_available, is_animating
    running = True
    dragging = None
    offset_x, offset_y = 0, 0
    mouse_moved = False
    game_state = "home"
    selected_a_square = None
    dragging_original_index = None
    is_animating = False
    mouse_start_pos = None
    mouse_move_threshold = 5

    undo_button_center_x = CENTER_X - BUTTON_RADIUS - BUTTON_SPACING // 2
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
                if event.type == pygame.MOUSEBUTTONDOWN and dragging is None and not is_animating:
                    print("Mouse down at:", event.pos)
                    mouse_pos = event.pos
                    mouse_moved = False
                    mouse_start_pos = mouse_pos
                    if reset_image and reset_button_rect.collidepoint(mouse_pos) and reset_available:
                        print("Calling reset_board from MOUSEBUTTONDOWN")
                        reset_board()
                        continue
                    if undo_image and undo_button_rect.collidepoint(mouse_pos) and square_manager.undo_count < square_manager.undo_limit:
                        play_click_sound()
                        square_manager.undo()
                        continue
                    colliding_squares = [
                        (i, square) for i, square in enumerate(squares)
                        if square["rect"].collidepoint(mouse_pos)
                    ]
                    if colliding_squares:
                        top_square = max(colliding_squares, key=lambda x: x[1]["layer"])
                        i, square = top_square
                        dragging = Square(square["image"], square["rect"].copy())
                        dragging_original_index = i
                        offset_x = mouse_pos[0] - square["rect"].x
                        offset_y = mouse_pos[1] - square["rect"].y
                        selected_a_square = {
                            "rect": square["rect"].copy(),
                            "image": square["image"],
                            "layer": square["layer"],
                            "col": square["col"],
                            "row": square["row"]
                        }
                        print(f"Selected square: index={i}, layer={square['layer']}, col={square['col']}, row={square['row']}")

                if event.type == pygame.MOUSEMOTION and dragging:
                    mouse_pos = event.pos
                    distance = ((mouse_pos[0] - mouse_start_pos[0]) ** 2 + (mouse_pos[1] - mouse_start_pos[1]) ** 2) ** 0.5
                    if distance > mouse_move_threshold:
                        mouse_moved = True
                    dragging.rect.x = mouse_pos[0] - offset_x
                    dragging.rect.y = mouse_pos[1] - offset_y

                if event.type == pygame.MOUSEBUTTONUP and dragging:
                    print("Mouse up, mouse_moved:", mouse_moved)
                    if not mouse_moved:
                        if len(square_manager.selected_squares) < square_manager.max_selected and selected_a_square is not None and dragging_original_index is not None and 0 <= dragging_original_index < len(squares):
                            play_click_sound()
                            frame_width = 7 * square_size + 6 * spacing
                            frame_x = (SCREEN_WIDTH - frame_width) // 2
                            target_x = frame_x + 5 + len(square_manager.selected_squares) * (square_size + spacing)
                            target_y = SCREEN_HEIGHT - (square_size + 35)
                            target_rect = pygame.Rect(target_x, target_y, square_size, square_size)
                            print("Squares count before removal:", len(squares))
                            move_square_to_selected(selected_a_square, target_rect, squares.copy())
                            print(f"Removing square at index={dragging_original_index}, layer={selected_a_square['layer']}, col={selected_a_square['col']}, row={selected_a_square['row']}")
                            del squares[dragging_original_index]
                            print("Squares count after removal:", len(squares))
                            if not square_manager.add_square(Square(selected_a_square["image"], target_rect)):
                                lose()
                    dragging = None
                    selected_a_square = None
                    dragging_original_index = None
                    mouse_start_pos = None

                if not squares and event.type == pygame.MOUSEBUTTONDOWN:
                    if box_rect.collidepoint(mouse_pos):
                        game_state = "home"

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

        if game_state == "play":
            squares_copy = squares.copy()
            max_layer_at_position = {}
            for square in squares_copy:
                pos = (square["col"], square["row"])
                current_layer = square["layer"]
                if pos not in max_layer_at_position or current_layer > max_layer_at_position[pos]:
                    max_layer_at_position[pos] = current_layer

            for square in sorted(squares_copy, key=lambda x: x["layer"]):
                pos = (square["col"], square["row"])
                is_top_layer = square["layer"] == max_layer_at_position.get(pos, 0)
                square_obj = Square(square["image"], square["rect"])
                square_obj.draw(is_top_layer)
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

                button_height = 40
                button_margin_bottom = 20
                button_spacing = 20
                button_width = 100

                home_button_rect = pygame.Rect(
                    SCREEN_WIDTH // 2 - button_width - button_spacing // 2,
                    SCREEN_HEIGHT - button_height - button_margin_bottom,
                    button_width,
                    button_height
                )
                draw_button(home_button_rect, "Home")

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
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - 20))
            button_retry = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 20, 200, 50)
            draw_button(button_retry, "Retry")

        pygame.display.flip()
        pygame.time.Clock().tick(120)

    pygame.quit()
