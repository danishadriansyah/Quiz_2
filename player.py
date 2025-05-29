import pygame
from utils import load_image
from constants import GRID_SIZE

class Player:
    def __init__(self, x, y):
        self.grid_x = x
        self.grid_y = y
        self.direction = (0, 0)
        self.next_direction = (0, 0)
        self.image = load_image("pac.png")
    
    def update(self, maze):
        next_grid_x = self.grid_x + self.next_direction[0]
        next_grid_y = self.grid_y + self.next_direction[1]
        
        if not maze.is_wall((next_grid_x, next_grid_y)):
            self.direction = self.next_direction
        
        if self.direction != (0, 0):
            target_grid_x = self.grid_x + self.direction[0]
            target_grid_y = self.grid_y + self.direction[1]
            
            if not maze.is_wall((target_grid_x, target_grid_y)):
                self.grid_x = target_grid_x
                self.grid_y = target_grid_y

    def draw(self, screen):
        angle = 0
        if self.direction == (1, 0): angle = 0      # Kanan
        elif self.direction == (-1, 0): angle = 180 # Kiri
        elif self.direction == (0, -1): angle = 90  # Atas
        elif self.direction == (0, 1): angle = 270  # Bawah
        
        rotated_img = pygame.transform.rotate(self.image, angle)
        x_offset = (GRID_SIZE - rotated_img.get_width()) // 2
        y_offset = (GRID_SIZE - rotated_img.get_height()) // 2
        screen.blit(rotated_img, (self.grid_x * GRID_SIZE + x_offset, self.grid_y * GRID_SIZE + y_offset))