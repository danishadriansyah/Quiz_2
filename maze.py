import pygame
from utils import load_image, generate_random_maze, find_random_empty, find_far_empty
from constants import GRID_SIZE, GRID_WIDTH, GRID_HEIGHT

class Maze:
    def __init__(self):
        self.walls = []
        self.dots = []
        self.player_pos = None
        self.ghost_positions = []

        # Generate random maze
        maze = generate_random_maze(GRID_WIDTH, GRID_HEIGHT)
        self.maze = maze

        # Tempatkan player di posisi acak
        self.player_pos = find_random_empty(maze)

        # Tempatkan 3 ghost di posisi acak, jauh dari player
        for _ in range(3):
            ghost_pos = find_far_empty(maze, self.player_pos, min_dist=6)
            self.ghost_positions.append(ghost_pos)

        # Isi walls dan dots
        for y, row in enumerate(maze):
            for x, char in enumerate(row):
                if char == "1":
                    self.walls.append((x, y))
                elif char == "0":
                    self.dots.append((x, y))

        if not self.player_pos:
            self.player_pos = (1, 1)
        if not self.ghost_positions:
            self.ghost_positions = [
                (GRID_WIDTH // 2, GRID_HEIGHT // 2),
                (GRID_WIDTH - 2, 1),
                (1, GRID_HEIGHT - 2)
            ]

    def is_wall(self, pos):
        return pos in self.walls
    
    def is_dot(self, pos):
        return pos in self.dots
    
    def eat_dot(self, pos):
        if pos in self.dots:
            self.dots.remove(pos)
            return True
        return False
    
    def draw(self, screen):
        for x, y in self.walls:
            block_img = load_image("block1.png")
            is_horizontal = ((x - 1, y) in self.walls) or ((x + 1, y) in self.walls)
            if is_horizontal:
                block_img = pygame.transform.rotate(block_img, 90)
            screen.blit(block_img, (x * GRID_SIZE, y * GRID_SIZE))

        for x, y in self.dots:
            dot_img = load_image("dot.png", scale=0.5)
            screen.blit(dot_img, (x * GRID_SIZE + (GRID_SIZE - dot_img.get_width()) // 2,
                                  y * GRID_SIZE + (GRID_SIZE - dot_img.get_height()) // 2))