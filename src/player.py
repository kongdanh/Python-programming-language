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
            