import pygame
from settings import screen, image_list, square_size, spacing, cols, rows
import random

squares = []

def update_grid_position(width, height):
    squares.clear()
    grid_width = cols * square_size + (cols - 1) * spacing
    grid_height = rows * square_size + (rows - 1) * spacing
    start_x = (width - grid_width) // 2
    start_y = (height - grid_height) // 2
    
    for row in range(rows):
        for col in range(cols):
            x = start_x + col * (square_size + spacing)
            y = start_y + row * (square_size + spacing)
            squares.append({"rect": pygame.Rect(x, y, square_size, square_size),
                            "pos": (col, row),
                            "image": random.choice(image_list)})

update_grid_position(500, 600)

def find_nearest_square(target, start_pos, end_pos):
    direction = pygame.Vector2(end_pos) - pygame.Vector2(start_pos)
    move_direction = (1, 0) if abs(direction.x) > abs(direction.y) else (0, 1)
    move_direction = (-move_direction[0], -move_direction[1]) if direction.x < 0 or direction.y < 0 else move_direction
    
    for square in squares:
        if square == target:
            continue
        if (square["pos"][0] - target["pos"][0], square["pos"][1] - target["pos"][1]) == move_direction:
            return square
    return None