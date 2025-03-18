import pygame
from settings import screen, resized_background, SCREEN_WIDTH, SCREEN_HEIGHT
from player import squares, find_nearest_square, update_grid_position

running = True
dragging = None
original_pos = None
offset_x, offset_y = 0, 0
moving_square = []
speed = 0.01

while running:
    screen.blit(resized_background, (0, 0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.VIDEORESIZE:
            width, height = event.w, event.h
            screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
            resized_background = pygame.transform.scale(background, (width, height)) # type: ignore
            update_grid_position(width, height)
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            for square in squares:
                if square["rect"].collidepoint(mx, my):
                    dragging = square
                    original_pos = square["rect"].topleft
                    offset_x = mx - square["rect"].x
                    offset_y = my - square["rect"].y
                    break
        
        if event.type == pygame.MOUSEMOTION and dragging:
            mx, my = event.pos
        
        if event.type == pygame.MOUSEBUTTONUP and dragging:
            nearest_square = find_nearest_square(dragging, original_pos, dragging["rect"].topleft)
            if nearest_square:
                moving_square.append({"square": dragging, "start_pos": pygame.Vector2(dragging["rect"].topleft), "end_pos": pygame.Vector2(nearest_square["rect"].topleft)})
                moving_square.append({"square": nearest_square, "start_pos": pygame.Vector2(nearest_square["rect"].topleft), "end_pos": pygame.Vector2(dragging["rect"].topleft)})
                dragging["pos"], nearest_square["pos"] = nearest_square["pos"], dragging["pos"]
            else:
                dragging["rect"].topleft = original_pos
            dragging = None
    
    for move in moving_square[:]:
        square = move["square"]
        start = move["start_pos"]
        end = move["end_pos"]
        new_pos = start.lerp(end, speed)
        square["rect"].topleft = (round(new_pos.x), round(new_pos.y))
        if new_pos.distance_to(end) < 1:
            square["rect"].topleft = end
            moving_square.remove(move)
        else:
            move["start_pos"] = new_pos
    
    for square in squares:
        pygame.draw.rect(screen, (255, 255, 255), square["rect"])
        screen.blit(square["image"], square["rect"].topleft)
    
    pygame.display.update()
pygame.quit()
