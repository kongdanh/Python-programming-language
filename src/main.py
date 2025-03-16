#Thêm thư viện để chạy các hàm cần thiết
import pygame   #chạy chương trình
import math
import random   #sinh ngẫu nhiên các đối tượng
import os       #dùng  để lấy đường dẫn từ thư mục các máy (riêng biệt)

#khởi tạo pygame
pygame.init()

#Độ lớn của cửa sổ width: rộng, height: cao và option: các điều khác tương tác với cửa sổ
# RESIZABLE -> cho phép thay đổi độ lớn cửa sổ game
screen = pygame.display.set_mode((500,600), pygame.RESIZABLE)

#Tiêu đề
pygame.display.set_caption("Đồ án Python")

#Đường dẫn cố định
base_dir = os.path.dirname(os.path.abspath(__file__))


#icon cho tiêu đề
icon = pygame.image.load(os.path.join(base_dir, "..", "assets", "icon_screen.jpg"))
pygame.display.set_icon(icon)

#Hình nền
background = pygame.image.load(os.path.join(base_dir, "..", "assets", "icon_screen.jpg"))

#Chỉnh sửa độ lớn hình nền cho khớp với độ lớn cửa sổ
resized_background = pygame.transform.scale(background, (500, 600))

#variable
cols, rows = 5, 8   #Số lượng hàng, cột
square_size = 30    #Độ lớn 1 khối
spacing = 5         #Khoảng cách giữa các khối

moving_square = []  #...
speed = 0.01        #...(2)

dragging = None     #Khối hiện tại

#vị trí hiện tại
original_pos = None

#vị trí trỏ chuột mở đầu 0,0 
offset_x, offset_y = 0,0

#list
squares = []
image_list = []

#Mảng đường dẫn tới hình ảnh
image_file =[os.path.join(base_dir, "..", "assets", "img1.jpg"),
             os.path.join(base_dir, "..", "assets", "img2.jpg"),
             os.path.join(base_dir, "..", "assets", "img3.jpg"),
             os.path.join(base_dir, "..", "assets", "img4.jpg")]

#Thêm hình ảnh từ mảng đường dẫn vào mảng hình ảnh và độ lớn = độ lớn khối
for img_f in image_file:
    img = pygame.image.load(img_f)
    img = pygame.transform.scale(img, (square_size, square_size))
    image_list.append(img)

#Cập nhật lại hình ảnh khung hình nếu có thay đổi về độ lớn cửa sổ
def update_grid_position(width, height):
    
    #....(3)
    squares.clear()
    
    #Lấy thông số giữa cửa sổ
    grid_width = cols * square_size + (cols - 1) * spacing
    grid_height = rows * square_size + (rows - 1) * spacing
    start_x = (width - grid_width) //2
    start_y = (height - grid_height) //2
    
    #Tạo các khối
    for row in range(rows):
        for col in range(cols):
            x = start_x + col * (square_size + spacing)
            y = start_y + row * (square_size + spacing)
            
            #Thêm các khối vào mảng (gồm các thông tin cụ thể)
            squares.append({"rect": pygame.Rect(x,y, square_size, square_size),
                            "pos": (col, row),
                            "image": random.choice(image_list)
                            })

#độ lớn cửa sổ mặc định
update_grid_position(500,600)

#... sẽ sửa đổi ...
def find_nearest_square(target, start_pos, end_pos):
    
    direction = pygame.Vector2(end_pos) - pygame.Vector2(start_pos)
    
    if (abs(direction.x) > abs(direction.y)):
        if (direction.x) > 0:
            move_direction = (1,0)
        else:
            move_direction = (-1,0)
    else:
        if direction.y > 0:
            move_direction = (0,1)
        else:
            move_direction = (0,-1)
    
    for square in squares:
        if square == target:
            continue
        if (square["pos"][0] - target["pos"][0], square["pos"][1] - target["pos"][1]) == move_direction:
            return square
    return None
    # #variable
    # nearest_square = None
    # min_distance = square_size *2
    
    # for square in squares:
        
    #     #current location
    #     if square == target:
    #         continue
        
    #     #else: calculate distance between 2 obj (center obj1 -> center obj2) -> Euclid
    #     #distance = sqrt((x2 - x1** 2 + (y2 - y1)**2)
    #     dist = math.dist(target["rect"].center, square["rect"].center)
    #     if dist < min_distance:
    #         min_distance = dist
    #         nearest_square = square
    
    # return nearest_square

#hàm nhận khối được nhấn -> trả về khối được nhấn
def get_square_clicked(target):
    clicked_square = []
    
    
    return 

#khởi chạy chương trình
running = True
while running:
    
    #vẽ hình nền 
    screen.blit(resized_background,(0,0))
    
    #lấy sự kiện từ người dùng
    for event in pygame.event.get():
        
        #khi nhấn nút x...
        if event.type == pygame.QUIT:
            running = False
        
        #thay đổi độ lớn cửa sổ
        if event.type == pygame.VIDEORESIZE:
            
            #lấy w, h mới
            width, height = event.w, event.h
            
            #tạo lại cửa sổ, đang bị lỗi tạo lại cả các khối
            screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
            resized_background = pygame.transform.scale(background, (width, height))
            update_grid_position(width, height)
        
        #khi người dùng nhấn
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            for square in squares:
                if square["rect"].collidepoint(mx,my):
                    
                    #lấy địa chỉ hiện tại của trỏ chuột
                    dragging = square
                    original_pos = square["rect"].topleft
                    offset_x = mx - square["rect"].x
                    offset_y = my - square["rect"].y
                    break
        
        #khi người dùng di chuyển chuột
        if event.type == pygame.MOUSEMOTION and dragging:
            mx, my = event.pos
            # dragging["rect"].x = mx - offset_x
            # dragging["rect"].y = my - offset_y
        
        #sự kiện thả chuột
        if event.type == pygame.MOUSEBUTTONUP and dragging:
            
            #gọi hàm ... sẽ sửa
            nearest_square = find_nearest_square(dragging,original_pos, dragging["rect"].topleft)
            #square_choice = get_square_clicked(target)
            
            if nearest_square:
                
                moving_square.append({
                    "square": dragging,
                    "start_pos": pygame.Vector2(dragging["rect"].topleft),
                    "end_pos": pygame.Vector2(nearest_square["rect"].topleft)
                })
                
                moving_square.append({
                    "square": nearest_square,
                    "start_pos": pygame.Vector2(nearest_square["rect"].topleft),
                    "end_pos": pygame.Vector2(dragging["rect"].topleft)
                })
                
                #nearest != None -> swap info dragging and nearest_square
                #this line for debugging if drag and drop event fails
                #print(f"Swapping {dragging['pos']} with {nearest_square['pos']}")
                #rect
                #dragging["rect"].topleft, nearest_square["rect"].topleft = nearest_square["rect"].topleft, original_pos
                #pos
                dragging["pos"], nearest_square["pos"] = nearest_square["pos"], dragging["pos"]
            else:
                #line 153
                #print("no change")
                #back original position
                dragging["rect"].topleft = original_pos

            dragging = None
    
    #animation chuyển động giữa các khối -> sẽ thay đổi bằng di chuyển khối vào ô chứa
    for move in moving_square[:]:
        square = move["square"]
        start = move["start_pos"]
        end = move["end_pos"]
        
        new_pos = start.lerp(end,speed)
        square["rect"].topleft = (round(new_pos.x), round(new_pos.y))
        
        if new_pos.distance_to(end) < 1:
            square["rect"].topleft = end
            moving_square.remove(move)
        else:
            move["start_pos"] = new_pos
    
    #tạo các khối mặc định
    for square in squares:
        pygame.draw.rect(screen, (255,255,255), square["rect"])
        screen.blit(square["image"], square["rect"].topleft)
    
    rect = pygame.draw.rect(screen, (255, 255, 255), (50, 550, 400, 50))  # (x, y, width, height)
    
    pygame.display.update()
    
pygame.quit()