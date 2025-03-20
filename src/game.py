import pygame
from settings import screen, resized_background, SCREEN_WIDTH, SCREEN_HEIGHT
from player import squares, update_grid_position

running = True
dragging = None
original_pos = None
offset_x, offset_y = 0, 0
moving_square = []
speed = 0.01
selected_squares = []
max_selected = 7
mouse_moved = False  # Kiểm tra xem chuột có di chuyển khi kéo không

def draw_ui():
    rect_x, rect_y = 105, 530
    rect_width, rect_height = 290, 50
    border_color = (255, 255, 255)

    pygame.draw.rect(screen, border_color, (rect_x, rect_y, rect_width, rect_height), 2)

# Khi nhấn, thêm square vào khung chọn
def on_square_click(square):
    global selected_squares

    if square not in selected_squares:
        if len(selected_squares) < max_selected:
            selected_squares.append(square)
            update_selected_position()

# Cập nhật vị trí các square trong khung chọn
def update_selected_position():
    start_x, start_y, spacing = 115, 540, 40  # Điều chỉnh vị trí và khoảng cách

    for i, square in enumerate(selected_squares):
        square["rect"].x = start_x + i * spacing
        square["rect"].y = start_y

while running:
    screen.blit(resized_background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.VIDEORESIZE:
            width, height = event.w, event.h
            screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
            resized_background = pygame.transform.scale(resized_background, (width, height))  
            update_grid_position(width, height)

        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            mouse_moved = False  # Đánh dấu chưa di chuyển
            for square in squares:
                if square["rect"].collidepoint(mx, my):
                    dragging = square
                    original_pos = square["rect"].topleft
                    offset_x = mx - square["rect"].x
                    offset_y = my - square["rect"].y
                    break

        if event.type == pygame.MOUSEMOTION and dragging:
            mouse_moved = True  # Đánh dấu đã di chuyển
            # nếu cần thiết khi người chơi được quyền kéo thả 
            # khóa sự kiện kéo thả
            # mx, my = event.pos
            # dragging["rect"].x = mx - offset_x
            # dragging["rect"].y = my - offset_y

        if event.type == pygame.MOUSEBUTTONUP and dragging:
            if not mouse_moved:  # Nếu không kéo, thêm vào khung chọn
                on_square_click(dragging)

    # Vẽ squares
    for square in squares:
        pygame.draw.rect(screen, (255, 255, 255), square["rect"])
        screen.blit(square["image"], square["rect"].topleft)

    draw_ui()

    pygame.display.update()

pygame.quit()
