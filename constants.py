import pygame

# Initialize pygame (needed for colors)
pygame.init()

# Game constants
WIDTH, HEIGHT = 1792, 1024  # 28 cols * 64, 16 rows * 64
GRID_SIZE = 64
GRID_WIDTH = WIDTH // GRID_SIZE  # 28
GRID_HEIGHT = HEIGHT // GRID_SIZE  # 16
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Game window setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pac-Man with BFS Ghosts")
clock = pygame.time.Clock()