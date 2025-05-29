import pygame
import os
import random
from collections import deque
from constants import GRID_SIZE, GRID_WIDTH, GRID_HEIGHT, WHITE, BLACK

def load_image(name, colorkey=None, scale=1):
    try:
        full_path = os.path.join("assets", name)
        image = pygame.image.load(full_path)
        image = image.convert_alpha()
        if scale != 1 or name.endswith('.png'):
            image = pygame.transform.scale(image, (GRID_SIZE, GRID_SIZE))
        if "dot" in name and scale != 1:
            target_size = int(GRID_SIZE * scale)
            image = pygame.transform.scale(image, (target_size, target_size))
        return image
    except Exception as e:
        print(f"Couldn't load image: {name}, error: {e}")
        surf = pygame.Surface((GRID_SIZE, GRID_SIZE))
        surf.fill(WHITE if "dot" in name else BLACK)
        return surf

def generate_random_maze(width, height, wall_prob=0.38):
    maze = []
    for y in range(height):
        row = ""
        for x in range(width):
            if x == 0 or y == 0 or x == width - 1 or y == height - 1:
                row += "1"  # wall at border
            else:
                if (y % 5 == 0 or x % 7 == 0) and random.random() > 0.35:
                    row += "0"
                else:
                    row += "1" if random.random() < wall_prob else "0"
        maze.append(row)
    return maze

def find_random_empty(maze):
    height = len(maze)
    width = len(maze[0])
    while True:
        x = random.randint(1, width - 2)
        y = random.randint(1, height - 2)
        if maze[y][x] == "0":
            return (x, y)

def find_far_empty(maze, avoid_pos, min_dist=6):
    height = len(maze)
    width = len(maze[0])
    tries = 0
    while True:
        x = random.randint(1, width - 2)
        y = random.randint(1, height - 2)
        if maze[y][x] == "0":
            dist = abs(x - avoid_pos[0]) + abs(y - avoid_pos[1])
            if dist >= min_dist:
                return (x, y)
        tries += 1
        if tries > 1000:  # fallback if stuck
            return find_random_empty(maze)

def bfs_path(maze, start, target):
    queue = deque([(start[0], start[1], [])])
    visited = {start}
    while queue:
        x, y, path = queue.popleft()
        if (x, y) == target:
            return path[0] if path else (0, 0) # Return the first step
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nx, ny = x + dx, y + dy
            if (0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT and
                not maze.is_wall((nx, ny)) and (nx, ny) not in visited):
                visited.add((nx, ny))
                queue.append((nx, ny, path + [(dx, dy)]))
    return (0, 0) # No path found