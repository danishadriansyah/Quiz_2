import pygame
import os
from collections import deque
import random

# Initialize pygame
pygame.init()

# Game constants
WIDTH, HEIGHT = 1792, 1024  # 28 cols * 64, 16 rows * 64
GRID_SIZE = 64
GRID_WIDTH = WIDTH // GRID_SIZE  # 28
GRID_HEIGHT = HEIGHT // GRID_SIZE  # 16
FPS = 60
MOVE_SPEED = 0.15  # Kecepatan pergerakan smooth (0.1 = lambat, 0.2 = cepat)

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
        image = image.convert_alpha()
        # Jika gambar ghost (atau apapun selain dot), scale ke GRID_SIZE (64x64)
        if scale != 1 or name.endswith('.png'):
            image = pygame.transform.scale(image, (GRID_SIZE, GRID_SIZE))
        # Untuk dot, tetap gunakan scale kecil jika diperlukan
        if "dot" in name and scale != 1:
            target_size = int(GRID_SIZE * scale)
            image = pygame.transform.scale(image, (target_size, target_size))
        return image
    except Exception as e:
        print(f"Couldn't load image: {name}, error: {e}")
        surf = pygame.Surface((GRID_SIZE, GRID_SIZE))
        surf.fill(WHITE if "dot" in name else BLACK)
        return surf

def generate_random_maze(width, height, wall_prob=0.38):  # lebih banyak wall, lebih kompleks
    maze = []
    for y in range(height):
        row = ""
        for x in range(width):
            if x == 0 or y == 0 or x == width-1 or y == height-1:
                row += "1"  # wall at border
            else:
                # Jalur utama lebih jarang, maze lebih random
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
        width, height = GRID_WIDTH, GRID_HEIGHT  # Now uses updated values
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
                (width // 2, height // 2),
                (width - 2, 1),
                (1, height - 2)
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
        self.grid_x = x
        self.grid_y = y
        self.x = float(x)  # Posisi pixel smooth
        self.y = float(y)
        self.direction = (0, 0)
        self.next_direction = (0, 0)
        self.image = load_image("pac.png")
        self.moving = False
    
    def update(self, maze):
        # Cek jika bisa berubah arah
        next_grid_x = self.grid_x + self.next_direction[0]
        next_grid_y = self.grid_y + self.next_direction[1]
        
        if not maze.is_wall((next_grid_x, next_grid_y)):
            self.direction = self.next_direction
        
        # Smooth movement
        if self.direction != (0, 0):
            target_grid_x = self.grid_x + self.direction[0]
            target_grid_y = self.grid_y + self.direction[1]
            
            if not maze.is_wall((target_grid_x, target_grid_y)):
                # Bergerak smooth ke target
                self.x += self.direction[0] * MOVE_SPEED
                self.y += self.direction[1] * MOVE_SPEED
                
                # Cek jika sudah sampai grid berikutnya
                if abs(self.x - target_grid_x) < 0.1 and abs(self.y - target_grid_y) < 0.1:
                    self.grid_x = target_grid_x
                    self.grid_y = target_grid_y
                    self.x = float(target_grid_x)
                    self.y = float(target_grid_y)
    
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
    def __init__(self, x, y, image_name, ghost_type="blinky"):
        self.grid_x = x
        self.grid_y = y
        self.x = float(x)  # Posisi pixel smooth
        self.y = float(y)
        self.image = load_image(image_name)
        self.ghost_type = ghost_type
        self.direction = (0, 0)
        self.move_timer = 0

    def get_target(self, maze, player, ghosts):
        if self.ghost_type == "blinky":
            return (player.grid_x, player.grid_y)
        elif self.ghost_type == "pinky":
            dx, dy = player.direction
            tx = player.grid_x + 4 * dx
            ty = player.grid_y + 4 * dy
            if 0 <= tx < GRID_WIDTH and 0 <= ty < GRID_HEIGHT and not maze.is_wall((tx, ty)):
                return (tx, ty)
            else:
                return (player.grid_x, player.grid_y)
        elif self.ghost_type == "inky":
            blinky = next(g for g in ghosts if g.ghost_type == "blinky")
            dx, dy = player.direction
            px = player.grid_x + 2 * dx
            py = player.grid_y + 2 * dy
            vx = px - blinky.grid_x
            vy = py - blinky.grid_y
            tx = blinky.grid_x + 2 * vx
            ty = blinky.grid_y + 2 * vy
            if 0 <= tx < GRID_WIDTH and 0 <= ty < GRID_HEIGHT and not maze.is_wall((tx, ty)):
                return (tx, ty)
            else:
                return (player.grid_x, player.grid_y)
        elif self.ghost_type == "clyde":
            dist = abs(self.grid_x - player.grid_x) + abs(self.grid_y - player.grid_y)
            if dist >= 5:
                return (player.grid_x, player.grid_y)
            else:
                return (1, GRID_HEIGHT - 2)
        else:
            return (player.grid_x, player.grid_y)

    def bfs_move(self, maze, target):
        queue = deque([(self.grid_x, self.grid_y, [])])
        visited = {(self.grid_x, self.grid_y)}
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

    def update(self, maze, player, ghosts):
        # Update setiap beberapa frame agar ghost tidak terlalu cepat
        self.move_timer += 1
        if self.move_timer < 15:  # Ghost bergerak lebih lambat
            return
        self.move_timer = 0
        
        target = self.get_target(maze, player, ghosts)
        dx, dy = self.bfs_move(maze, target)
        new_x, new_y = self.grid_x + dx, self.grid_y + dy
        if not maze.is_wall((new_x, new_y)):
            self.grid_x, self.grid_y = new_x, new_y
            self.x, self.y = float(new_x), float(new_y)

    def draw(self, screen):
        x_offset = (GRID_SIZE - self.image.get_width()) // 2
        y_offset = (GRID_SIZE - self.image.get_height()) // 2
        screen.blit(self.image, (self.x * GRID_SIZE + x_offset, self.y * GRID_SIZE + y_offset))

def main():
    maze = Maze()
    player = Player(maze.player_pos[0], maze.player_pos[1])
    ghosts = [
        Ghost(maze.ghost_positions[0][0], maze.ghost_positions[0][1], "blinky.png", "blinky"),
        Ghost(maze.ghost_positions[1][0], maze.ghost_positions[1][1], "pinky.png", "pinky"),
        Ghost(maze.ghost_positions[2][0], maze.ghost_positions[2][1], "inky.png", "inky"),
        Ghost(maze.ghost_positions[2][0], maze.ghost_positions[2][1], "clyde.png", "clyde"),
    ]
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
                elif event.key == pygame.K_ESCAPE:
                    running = False
        
        player.update(maze)
        if maze.eat_dot((player.grid_x, player.grid_y)):
            score += 10
        
        for ghost in ghosts:
            ghost.update(maze, player, ghosts)
            if ghost.grid_x == player.grid_x and ghost.grid_y == player.grid_y:
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