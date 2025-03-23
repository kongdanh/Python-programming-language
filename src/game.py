import pygame
from settings import screen, resized_background, SCREEN_WIDTH, SCREEN_HEIGHT, home_page
from player import squares, update_grid_position
from config.config import game_state
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

running = True
dragging = None
offset_x, offset_y = 0, 0
mouse_moved = False  
game_state = "home"

while running:
    screen.blit(resized_background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # gọi trang chủ nếu nhấn vào box -> thay đổi giá trị game_state
        if game_state == "play":
            if event .type == pygame.MOUSEBUTTONDOWN:
                if not squares:
                    if box_rect.collidepoint(event.pos):
                        game_state = "home"
        elif game_state == "home":
            home_page()
            game_state = "play"
         
        if event.type == pygame.VIDEORESIZE:
            width, height = event.w, event.h
            screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
            resized_background = pygame.transform.scale(resized_background, (width, height))  
            update_grid_position(width, height)

        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            mouse_moved = False
            for square in squares:
                if square["rect"].collidepoint(mx, my):
                    dragging = Square(square["image"], square["rect"])  # Chuyển đổi thành đối tượng Square
                    offset_x = mx - square["rect"].x
                    offset_y = my - square["rect"].y
                    break

        if event.type == pygame.MOUSEMOTION and dragging:
            mouse_moved = True

        if event.type == pygame.MOUSEBUTTONUP and dragging:
            if not mouse_moved:  
                square_manager.remove_square_after_onclick(dragging)
                square_manager.add_square(dragging)


    # Vẽ các square có trên màn hình
    for square in squares:
        pygame.draw.rect(screen, (255, 255, 255), square["rect"])
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
