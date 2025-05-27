import pygame
import os
from collections import deque
import random

# Initialize pygame
pygame.init()

# Game constants
WIDTH, HEIGHT = 1300, 700
GRID_SIZE = 64  # Sesuai dengan ukuran asset 64x64
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
FPS = 20

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Create game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pac-Man with BFS Ghosts")
clock = pygame.time.Clock()

# Load assets
def load_image(name, colorkey=None, scale=1):
    try:
        full_path = os.path.join("assets", name)
        image = pygame.image.load(full_path)
        # Karena gambar sudah 64x64, kita bisa langsung menggunakan convert_alpha
        # tanpa scaling tambahan
        if colorkey is not None:
            image = image.convert()
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey)
        else:
            image = image.convert_alpha()
        
        # Skala hanya jika diperlukan (untuk dot yang mungkin lebih kecil)
        if scale != 1:
            target_size = int(GRID_SIZE * scale)
            image = pygame.transform.scale(image, (target_size, target_size))
        return image
    except Exception as e:
        print(f"Couldn't load image: {name}, error: {e}")
        surf = pygame.Surface((GRID_SIZE, GRID_SIZE))
        surf.fill(WHITE if "dot" in name else BLACK)
        return surf

def generate_random_maze(width, height, wall_prob=0.2):
    maze = []
    for y in range(height):
        row = ""
        for x in range(width):
            if x == 0 or y == 0 or x == width-1 or y == height-1:
                row += "1"  # wall at border
            else:
                row += "1" if random.random() < wall_prob else "0"
        maze.append(row)
    return maze

def find_random_empty(maze):
    height = len(maze)
    width = len(maze[0])
    while True:
        x = random.randint(1, width-2)
        y = random.randint(1, height-2)
        if maze[y][x] == "0":
            return (x, y)

def find_far_empty(maze, avoid_pos, min_dist=6):
    height = len(maze)
    width = len(maze[0])
    tries = 0
    while True:
        x = random.randint(1, width-2)
        y = random.randint(1, height-2)
        if maze[y][x] == "0":
            dist = abs(x - avoid_pos[0]) + abs(y - avoid_pos[1])
            if dist >= min_dist:
                return (x, y)
        tries += 1
        if tries > 1000:  # fallback if stuck
            return find_random_empty(maze)

# Maze layout
maze_layout = [
    "11111111111111111111",
    "10000000000000000001",
    "1011101110111011101",
    "10000000000000000001",
    "1011101110111011101",
    "10000000000000000001",
    "1011101110111011101",
    "10000000000000000001",
    "1011101110111011101",
    "10000000000000000001",
    "11111111111111111111"
]

class Maze:
    def __init__(self):
        width, height = 20, 11  # sesuai layout lama
        self.walls = []
        self.dots = []
        self.player_pos = None
        self.ghost_positions = []

        # Generate random maze
        maze = generate_random_maze(width, height)
        self.maze = maze  # simpan untuk referensi

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
                (8, 5),    # Tengah maze
                (18, 1),   # Pojok kanan atas
                (1, 9)     # Pojok kiri bawah
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
            # Cek apakah block ini bagian dari wall horizontal
            is_horizontal = ((x-1, y) in self.walls) or ((x+1, y) in self.walls)
            if is_horizontal:
                block_img = pygame.transform.rotate(block_img, 90)
            screen.blit(block_img, (x * GRID_SIZE, y * GRID_SIZE))

        for x, y in self.dots:
            dot_img = load_image("dot.png", scale=0.5)  # Skala dot lebih kecil
            screen.blit(dot_img, (x * GRID_SIZE + (GRID_SIZE - dot_img.get_width()) // 2,
                                y * GRID_SIZE + (GRID_SIZE - dot_img.get_height()) // 2))

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.direction = (0, 0)
        self.next_direction = (0, 0)
        self.image = load_image("pac.png")  # Tidak perlu scale karena sudah 64x64
    
    def update(self, maze):
        new_x, new_y = self.x + self.next_direction[0], self.y + self.next_direction[1]
        if not maze.is_wall((new_x, new_y)):
            self.direction = self.next_direction
        
        new_x, new_y = self.x + self.direction[0], self.y + self.direction[1]
        if not maze.is_wall((new_x, new_y)):
            self.x, self.y = new_x, new_y
    
    def draw(self, screen):
        angle = 0
        if self.direction == (1, 0): angle = 0
        elif self.direction == (-1, 0): angle = 180
        elif self.direction == (0, -1): angle = 90
        elif self.direction == (0, 1): angle = 270
        
        rotated_img = pygame.transform.rotate(self.image, angle)
        x_offset = (GRID_SIZE - rotated_img.get_width()) // 2
        y_offset = (GRID_SIZE - rotated_img.get_height()) // 2
        screen.blit(rotated_img, (self.x * GRID_SIZE + x_offset, self.y * GRID_SIZE + y_offset))

class Ghost:
    def __init__(self, x, y, image_name):
        self.x = x
        self.y = y
        self.image = load_image(image_name)  # Tidak perlu scale karena sudah 64x64
    
    def bfs_move(self, maze, target):
        queue = deque([(self.x, self.y, [])])
        visited = {(self.x, self.y)}
        
        while queue:
            x, y, path = queue.popleft()
            if (x, y) == target:
                return path[0] if path else (0, 0)
            
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                nx, ny = x + dx, y + dy
                if (0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT and 
                    not maze.is_wall((nx, ny)) and (nx, ny) not in visited):
                    visited.add((nx, ny))
                    queue.append((nx, ny, path + [(dx, dy)]))
        
        return (0, 0)
    
    def update(self, maze, player_pos):
        dx, dy = self.bfs_move(maze, player_pos)
        new_x, new_y = self.x + dx, self.y + dy
        if not maze.is_wall((new_x, new_y)):
            self.x, self.y = new_x, new_y
    
    def draw(self, screen):
        x_offset = (GRID_SIZE - self.image.get_width()) // 2
        y_offset = (GRID_SIZE - self.image.get_height()) // 2
        screen.blit(self.image, (self.x * GRID_SIZE + x_offset, self.y * GRID_SIZE + y_offset))

def main():
    maze = Maze()
    player = Player(maze.player_pos[0], maze.player_pos[1])
    ghosts = [
        Ghost(maze.ghost_positions[0][0], maze.ghost_positions[0][1], "ghost1.png"),
        Ghost(maze.ghost_positions[1][0], maze.ghost_positions[1][1], "ghost2.png"),
        Ghost(maze.ghost_positions[2][0], maze.ghost_positions[2][1], "ghost3.png")
    ]
    
    if len(maze.ghost_positions) > 3:
        ghosts.append(Ghost(maze.ghost_positions[3][0], maze.ghost_positions[3][1], "ghost4.png"))
    
    running = True
    score = 0
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player.next_direction = (0, -1)
                elif event.key == pygame.K_DOWN:
                    player.next_direction = (0, 1)
                elif event.key == pygame.K_LEFT:
                    player.next_direction = (-1, 0)
                elif event.key == pygame.K_RIGHT:
                    player.next_direction = (1, 0)
        
        player.update(maze)
        if maze.eat_dot((player.x, player.y)):
            score += 10
        
        for ghost in ghosts:
            ghost.update(maze, (player.x, player.y))
            if ghost.x == player.x and ghost.y == player.y:
                print(f"Game Over! Score: {score}")
                running = False
        
        if not maze.dots:
            print(f"You Win! Score: {score}")
            running = False
        
        screen.fill(BLACK)
        maze.draw(screen)
        player.draw(screen)
        for ghost in ghosts:
            ghost.draw(screen)
        
        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()

if __name__ == "__main__":
    main()