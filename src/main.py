#import the libary
import pygame
import math
import random

#initialization init -> pygame
pygame.init()

#size of frame ((width, height), option)
screen = pygame.display.set_mode((500,600), pygame.RESIZABLE)

#title
pygame.display.set_caption("Đồ án Python")

#icon for title 
icon = pygame.image.load("C:/Users/danhc/Documents/K2N2/PYTHON/DO_AN/assets/icon_screen.jpg")
pygame.display.set_icon(icon)

#background
background = pygame.image.load("C:/Users/danhc/Documents/K2N2/PYTHON/DO_AN/assets/icon_screen.jpg")

#editing background -> get width & height at screen size
resized_background = pygame.transform.scale(background, (500, 600))

#variable
cols, rows = 5, 8
square_size = 30
spacing = 5

moving_square = []
speed = 0.01

dragging = None

#current location
original_pos = None

#current cursor position
offset_x, offset_y = 0,0

#list
squares = []
image_list = []

#path
image_file =["C:/Users/danhc/Documents/K2N2/PYTHON/DO_AN/assets/img1.jpg",
             "C:/Users/danhc/Documents/K2N2/PYTHON/DO_AN/assets/img2.jpg",
             "C:/Users/danhc/Documents/K2N2/PYTHON/DO_AN/assets/img3.jpg",
             "C:/Users/danhc/Documents/K2N2/PYTHON/DO_AN/assets/img4.jpg"]

#input image
for img_f in image_file:
    img = pygame.image.load(img_f)
    img = pygame.transform.scale(img, (square_size, square_size))
    image_list.append(img)

#edit frames and obj as they change width & height
def update_grid_position(width, height):
    
    #create new list
    squares.clear()
    
    #variable -> center screen
    grid_width = cols * square_size + (cols - 1) * spacing
    grid_height = rows * square_size + (rows - 1) * spacing
    start_x = (width - grid_width) //2
    start_y = (height - grid_height) //2
    
    #content initialization
    for row in range(rows):
        for col in range(cols):
            x = start_x + col * (square_size + spacing)
            y = start_y + row * (square_size + spacing)
            
            #component of squares (obj list)
            squares.append({"rect": pygame.Rect(x,y, square_size, square_size),
                            "pos": (col, row),
                            "image": random.choice(image_list)
                            })

#original frame
update_grid_position(500,600)

#function changed location
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

def get_square_clicked(target):
    clicked_square = []
    
    
    return 

#start the program
running = True
while running:
    
    #draw background at (0,0)
    screen.blit(resized_background,(0,0))
    
    #get event from user
    for event in pygame.event.get():
        
        #click on x
        if event.type == pygame.QUIT:
            running = False
        
        #stretch frame
        if event.type == pygame.VIDEORESIZE:
            
            #get new width & height
            width, height = event.w, event.h
            
            #create new frame size
            screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
            resized_background = pygame.transform.scale(background, (width, height))
            update_grid_position(width, height)
        
        #when user click
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            for square in squares:
                if square["rect"].collidepoint(mx,my):
                    
                    #get current location, square
                    dragging = square
                    original_pos = square["rect"].topleft
                    offset_x = mx - square["rect"].x
                    offset_y = my - square["rect"].y
                    break
        
        #user move mouse
        if event.type == pygame.MOUSEMOTION and dragging:
            mx, my = event.pos
            # dragging["rect"].x = mx - offset_x
            # dragging["rect"].y = my - offset_y
        
        #user release the mouse button
        if event.type == pygame.MOUSEBUTTONUP and dragging:
            
            #call function
            nearest_square = find_nearest_square(dragging,original_pos, dragging["rect"].topleft)
            square_choice = get_square_clicked(target)
            
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
    
    #
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
    
    #create content
    for square in squares:
        pygame.draw.rect(screen, (255,255,255), square["rect"])
        screen.blit(square["image"], square["rect"].topleft)
    
    # oval = pygame.draw.rect(screen, (255, 255, 255), (400, 300), 100)
    # screen.blit(oval,(300,200))
    pygame.display.update()
    
pygame.quit()