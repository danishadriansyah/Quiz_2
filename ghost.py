import pygame
from utils import load_image, bfs_path
from constants import GRID_SIZE, GRID_WIDTH, GRID_HEIGHT

class Ghost:
    def __init__(self, x, y, image_name, ghost_type="blinky"):
        self.grid_x = x
        self.grid_y = y
        self.image = load_image(image_name)
        self.ghost_type = ghost_type
        self.direction = (0, 0)
        self.move_counter = 0

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
            blinky = next((g for g in ghosts if g.ghost_type == "blinky"), None)
            if blinky:
                dx, dy = player.direction
                px = player.grid_x + 2 * dx
                py = player.grid_y + 2 * dy
                vx = px - blinky.grid_x
                vy = py - blinky.grid_y
                tx = blinky.grid_x + 2 * vx
                ty = blinky.grid_y + 2 * vy
                if 0 <= tx < GRID_WIDTH and 0 <= ty < GRID_HEIGHT and not maze.is_wall((tx, ty)):
                    return (tx, ty)
            return (player.grid_x, player.grid_y)
        elif self.ghost_type == "clyde":
            dist = abs(self.grid_x - player.grid_x) + abs(self.grid_y - player.grid_y)
            if dist >= 5:
                return (player.grid_x, player.grid_y)
            else:
                return (1, GRID_HEIGHT - 2)
        else:
            return (player.grid_x, player.grid_y)

    def update(self, maze, player, ghosts):
        self.move_counter += 1
        if self.move_counter >= 5:
            self.move_counter = 0
            target = self.get_target(maze, player, ghosts)
            dx, dy = bfs_path(maze, (self.grid_x, self.grid_y), target)
            new_x, new_y = self.grid_x + dx, self.grid_y + dy
            if not maze.is_wall((new_x, new_y)):
                self.grid_x, self.grid_y = new_x, new_y

    def draw(self, screen):
        x_offset = (GRID_SIZE - self.image.get_width()) // 2
        y_offset = (GRID_SIZE - self.image.get_height()) // 2
        screen.blit(self.image, (self.grid_x * GRID_SIZE + x_offset, self.grid_y * GRID_SIZE + y_offset))