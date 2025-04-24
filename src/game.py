import pygame
import random
from settings import screen, resized_background, SCREEN_WIDTH, SCREEN_HEIGHT, home_page, game_state, reset_game
from player import squares, update_grid_position
from settings import image_list

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
        # Thêm square vào danh sách nếu chưa đầy
        if square not in self.selected_squares and len(self.selected_squares) < self.max_selected:
            self.selected_squares.append(square)
            self.update_selected_position()
            self.check_match()

    def update_selected_position(self):
        # Cập nhật vị trí hiển thị của các square trong danh sách
        start_x, start_y, spacing = 115, 540, 40
        for i, square in enumerate(self.selected_squares):
            square.rect.x = start_x + i * spacing
            square.rect.y = start_y

    def check_match(self):
        # Kiểm tra và xóa nếu có ít nhất 3 ô vuông giống nhau
        img_count = {}
        for square in self.selected_squares:
            img_count[square.image] = img_count.get(square.image, 0) + 1

        matched_images = {img for img, count in img_count.items() if count >= 3}

        if matched_images:
            # Xóa các square có hình ảnh thuộc matched_images
            self.selected_squares = [sq for sq in self.selected_squares if sq.image not in matched_images]
            self.update_selected_position()  # Cập nhật lại vị trí

    def draw_selected_squares(self):
        # Vẽ lại danh sách ô đã chọn
        for square in self.selected_squares:
            square.draw()

    def remove_square_after_onclick(self, square):
        #Xóa sau khi nhấn chọn square vì square đc chọn đã thêm vào selected_square
        global squares
        squares = [s for s in squares if s["rect"] != square.rect]

def draw_ui():
    # Vẽ khung chứa các square đã chọn
    pygame.draw.rect(screen, (255, 255, 255), (105, 530, 290, 50), 2)

# Khởi tạo quản lý ô vuông
square_manager = SquareManager()

def generate_random_squares(num_squares):
    global squares
    squares = []
    available_positions = set()
    grid_width = 5  # Số cột ảo cho việc xếp lớp
    grid_height = 6 # Số hàng ảo
    for r in range(grid_height):
        for c in range(grid_width):
            available_positions.add((c, r, 0)) # (col, row, layer)

    image_choices = random.choices(image_list, k=num_squares)

    for img in image_choices:
        if not available_positions:
            break  # Không còn vị trí trống

        position = random.choice(list(available_positions))
        col, row, layer = position

        # Tính toán vị trí x, y dựa trên cột, hàng và lớp
        x = (SCREEN_WIDTH - (5 * 30 + 4 * 5)) // 2 + col * (30 + 5)
        y = (SCREEN_HEIGHT - (6 * 30 + 5 * 5)) // 3 + row * (30 + 5)

        squares.append({"rect": pygame.Rect(x, y, 30, 30),
                        "image": img})

        # Loại bỏ vị trí đã chọn và vị trí lớp trên nếu lớp hiện tại là 0
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
            progress = time_elapsed / animation_duration  # Giá trị từ 0 đến 1

            # Tính toán vị trí x, y mới dựa trên tiến độ
            new_x = start_rect.x + (end_rect.x - start_rect.x) * progress
            new_y = start_rect.y + (end_rect.y - start_rect.y) * progress

            moving_square.rect.x = int(new_x)
            moving_square.rect.y = int(new_y)

        screen.blit(resized_background, (0, 0))  # Vẽ lại background
        for sq in squares:
            screen.blit(sq["image"], sq["rect"].topleft)
        draw_ui()
        square_manager.draw_selected_squares()
        moving_square.draw() # Vẽ ô đang di chuyển
        pygame.display.flip()

        pygame.time.Clock().tick(120) # Tăng tốc độ khung hình cho mượt

def run_game():
    running = True
    dragging = None
    offset_x, offset_y = 0, 0
    mouse_moved = False
    game_state = "home"
    selected_a_square = None # Lưu trữ ô vuông được chọn để di chuyển xuống
    dragging_original_index = None # Lưu trữ index của ô đang được kéo

    while running:
        screen.blit(resized_background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Gọi trang chủ nếu nhấn vào box -> thay đổi giá trị game_state
            if game_state == "play":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if not squares:
                        if box_rect.collidepoint(event.pos):
                            game_state = "home"
            elif game_state == "home":
                reset_game()
                home_page()
                generate_random_squares(30) # Tạo ngẫu nhiên các square khi bắt đầu chơi
                game_state = "play"

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                mouse_moved = False
                # Duyệt các square theo thứ tự ngược lại để chọn square trên cùng
                for i, square in enumerate(reversed(squares)):
                    if square["rect"].collidepoint(mouse_pos):
                        dragging = Square(square["image"], square["rect"].copy()) # Tạo bản sao để di chuyển
                        dragging_original_index = len(squares) - 1 - i # Lưu index để xóa sau
                        offset_x = mouse_pos[0] - square["rect"].x
                        offset_y = mouse_pos[1] - square["rect"].y
                        selected_a_square = squares[dragging_original_index].copy() # Lưu trữ dữ liệu ô được chọn
                        break

            if event.type == pygame.MOUSEMOTION and dragging:
                mouse_moved = True
                dragging.rect.x = event.pos[0] - offset_x
                dragging.rect.y = event.pos[1] - offset_y

            if event.type == pygame.MOUSEBUTTONUP and dragging:
                if not mouse_moved:
                    # Nếu không di chuyển, coi như click để chọn xuống khung
                    if len(square_manager.selected_squares) < square_manager.max_selected and selected_a_square is not None and dragging_original_index is not None and 0 <= dragging_original_index < len(squares):
                        target_x = 115 + len(square_manager.selected_squares) * 40
                        target_y = 540
                        target_rect = pygame.Rect(target_x, target_y, 30, 30)
                        move_square_to_selected(selected_a_square, target_rect)
                        del squares[dragging_original_index] # Xóa ô khỏi sàn sau khi di chuyển xuống
                        square_manager.add_square(Square(selected_a_square["image"], target_rect))
                dragging = None
                selected_a_square = None
                dragging_original_index = None

        # Vẽ các square có trên màn hình
        for square in squares:
            screen.blit(square["image"], square["rect"].topleft)

        draw_ui()  # Vẽ khung UI
        square_manager.draw_selected_squares()  # Vẽ danh sách ô đã chọn

        # Khi hoàn thành màn chơi -> không còn square trên sàn
        if not squares:
            # Tạo mờ màn hình chính
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0,0,0, 180))
            screen.blit(overlay, (0,0))

            # Tạo box chứa thông tin hoàn thành màn đè lên screen
            box_rect = pygame.Rect(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 3, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)
            pygame.draw.rect(screen, (255,255,255), box_rect, border_radius=10)
            pygame.draw.rect(screen, (0,0,0), box_rect, 3, border_radius=10)

            # Thông tin màn hoàn thành -> text, animation,...
            font = pygame.font.Font(None, 36)
            text = font.render("Level complete!", True, (0,0,0))
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - 20))

        pygame.display.flip()
        pygame.display.update()

    pygame.quit()


def draw_ui():
    # Vẽ khung chứa các square đã chọn
    pygame.draw.rect(screen, (255, 255, 255), (105, 530, 290, 50), 2)
