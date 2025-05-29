import pygame
from constants import screen, clock, FPS, BLACK, WHITE
from maze import Maze
from player import Player
from ghost import Ghost

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