import pygame
import random
from settings import screen, resized_background, SCREEN_WIDTH, SCREEN_HEIGHT, home_page, reset_game, font
from player import squares, update_grid_position
from settings import image_list, play_click_sound, play_match_sound, play_complete_sound, play_gameover_sound

# Khởi tạo Pygame
pygame.init()

class Square:
    def __init__(self, image, rect):
        self.image = image
        self.rect = pygame.Rect(rect)  # Đảm bảo rect là đối tượng pygame.Rect

    def draw(self):
        screen.blit(self.image, self.rect.topleft)

class SquareManager:
    def __init__(self):
        self.selected_squares = []
        self.max_selected = 7

    def add_square(self, square):
        if square not in self.selected_squares and len(self.selected_squares) < self.max_selected:
            self.selected_squares.append(square)
            self.update_selected_position()
            if len(self.selected_squares) == self.max_selected and not self.check_match():
                print("Khung đầy và không có match, thua game!")
                return False  # Trả về False để báo hiệu thua game
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
            self.selected_squares = [sq for sq in self.selected_squares if sq.image not in matched_images]
            self.update_selected_position()
            return True
        return False

    def draw_selected_squares(self):
        for square in self.selected_squares:
            square.draw()

def draw_button(button, text):
    pygame.draw.rect(screen, (200, 200, 200), button, border_radius=10)
    text_surface = font.render(text, True, (0, 0, 0))
    text_rect = text_surface.get_rect(center=button.center)
    screen.blit(text_surface, text_rect)

def lose():
    global game_state
    game_state = "lose"  # Chuyển sang trạng thái thua
    play_gameover_sound()

def draw_ui():
    pygame.draw.rect(screen, (255, 255, 255), (105, 530, 290, 50), 2)

square_manager = SquareManager()

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
            screen.blit(sq["image"], sq["rect"].topleft)
        draw_ui()
        square_manager.draw_selected_squares()
        moving_square.draw()
        pygame.display.flip()
        pygame.time.Clock().tick(120)

def run_game():
    global game_state, squares
    running = True
    dragging = None
    offset_x, offset_y = 0, 0
    mouse_moved = False
    game_state = "home"
    selected_a_square = None
    dragging_original_index = None

    # Nút "Chơi lại" cho màn hình Game Over
    button_retry = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 20, 200, 50)

    while running:
        screen.blit(resized_background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if game_state == "home":
                reset_game()
                home_page()
                generate_random_squares(30)
                game_state = "play"

            elif game_state == "play":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    mouse_moved = False
                    for i, square in enumerate(reversed(squares)):
                        if square["rect"].collidepoint(mouse_pos):
                            dragging = Square(square["image"], square["rect"].copy())
                            dragging_original_index = len(squares) - 1 - i
                            offset_x = mouse_pos[0] - square["rect"].x
                            offset_y = mouse_pos[1] - square["rect"].y
                            selected_a_square = squares[dragging_original_index].copy()
                            break

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
                                lose()  # Chuyển sang trạng thái thua
                    dragging = None
                    selected_a_square = None
                    dragging_original_index = None

                # Xử lý khi nhấn vào box "Level complete"
                if not squares and event.type == pygame.MOUSEBUTTONDOWN:
                    if box_rect.collidepoint(event.pos):
                        game_state = "home"

            elif game_state == "lose":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if button_retry.collidepoint(event.pos):
                        play_click_sound()
                        reset_game()
                        square_manager.selected_squares = []  # Xóa danh sách ô đã chọn
                        generate_random_squares(30)
                        game_state = "play"

        # Vẽ giao diện theo trạng thái
        if game_state == "play":
            for square in squares:
                screen.blit(square["image"], square["rect"].topleft)
            draw_ui()
            square_manager.draw_selected_squares()

            if not squares:
                overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 180))
                screen.blit(overlay, (0, 0))
                box_rect = pygame.Rect(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 3, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)
                pygame.draw.rect(screen, (255, 255, 255), box_rect, border_radius=10)
                pygame.draw.rect(screen, (0, 0, 0), box_rect, 3, border_radius=10)
                text = font.render("Level complete!", True, (0, 0, 0))
                screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - 20))

        elif game_state == "lose":
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            screen.blit(overlay, (0, 0))
            box_rect = pygame.Rect(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 3, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)
            pygame.draw.rect(screen, (255, 255, 255), box_rect, border_radius=10)
            pygame.draw.rect(screen, (0, 0, 0), box_rect, 3, border_radius=10)
            text = font.render("Game Over", True, (0, 0, 0))
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - 20))
            draw_button(button_retry, "Retry")

        pygame.display.flip()

    pygame.quit()