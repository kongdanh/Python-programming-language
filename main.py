import pygame
import math
import random
pygame.init()

#screen, width, height
screen = pygame.display.set_mode((800,600), pygame.RESIZABLE)

#caption
pygame.display.set_caption("Đồ án Python")

#icon
icon = pygame.image.load("icon_screen.png")
pygame.display.set_icon(icon)

#background
background = pygame.image.load("icon_screen.jpg")
resized_background = pygame.transform.scale(background, (800, 600))

#number in square
font = pygame.font.Font(None, 36)

#candy
cols, rows = 5, 8
square_size = 50
spacing = 10

#drag
dragging = None

#default
original_pos = None

#offset
offset_x, offset_y = 0,0

squares = []
image_list = []

#image file
image_file =["img1.jpg","img2.jpg", "img3.jpg", "img4.jpg"]
for img_f in image_file:
    img = pygame.image.load(img_f)
    img = pygame.transform.scale(img, (square_size, square_size))
    image_list.append(img)
#
def update_grid_position(width, height):
    squares.clear()
    grid_width = cols * square_size + (cols - 1) * spacing
    grid_height = rows * square_size + (rows - 1) * spacing
    start_x = (width - grid_width) //2
    start_y = (height - grid_height) //2
    for row in range(rows):
        for col in range(cols):
            x = start_x + col * (square_size + spacing)
            y = start_y + row * (square_size + spacing)
            squares.append({"rect": pygame.Rect(x,y, square_size, square_size),
                            "pos": (col, row),
                            "image": random.choice(image_list)
                            })

update_grid_position(800,600)

#changed square
def find_nearest_square(target):
    nearest_square = None
    min_distance = square_size *2
    
    for square in squares:
        if square == target:
            continue
        
        dist = math.dist(target["rect"].center, square["rect"].center)
        if dist < min_distance:
            min_distance = dist
            nearest_square = square
    
    return nearest_square

#run code
running = True
while running:
    screen.blit(resized_background,(0,0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.VIDEORESIZE:
            width, height = event.w, event.h
            screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
            resized_background = pygame.transform.scale(background, (width, height))
            update_grid_position(width, height)
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            for square in squares:
                if square["rect"].collidepoint(mx,my):
                    dragging = square
                    original_pos = square["rect"].topleft
                    offset_x = mx - square["rect"].x
                    offset_y = my - square["rect"].y
                    break
        
        if event.type == pygame.MOUSEMOTION and dragging:
            mx, my = event.pos
            dragging["rect"].x = mx - offset_x
            dragging["rect"].y = my - offset_y
        
        if event.type == pygame.MOUSEBUTTONUP and dragging:
            nearest_square = find_nearest_square(dragging)
            if nearest_square:
                print(f"Swapping {dragging['pos']} with {nearest_square['pos']}")
                dragging["rect"].topleft, nearest_square["rect"].topleft = nearest_square["rect"].topleft, original_pos
                dragging["pos"], nearest_square["pos"] = nearest_square["pos"], dragging["pos"]
                #dragging["image"], nearest_square["image"] = nearest_square["image"], dragging["image"]
            else:
                print("chua swap")
                dragging["rect"].topleft = original_pos

            dragging = None
    
    for square in squares:
        pygame.draw.rect(screen, (255,255,255), square["rect"])
        screen.blit(square["image"], square["rect"].topleft)
    
    pygame.display.update()
    
pygame.quit()