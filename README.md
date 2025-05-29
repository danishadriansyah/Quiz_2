# Pac-Man with BFS Ghosts

![image](https://github.com/user-attachments/assets/66d6cb76-4d6a-476d-a0be-31b1610feecd)


This is a Pac-Man game implemented using Pygame, featuring dynamically generated mazes and intelligent ghost AI powered by the Breadth-First Search (BFS) algorithm. Each ghost has a unique targeting strategy, making the gameplay challenging and engaging.

-----

## Features

  * **Dynamic Maze Generation**: Every time you start the game, a new, randomized maze is created, ensuring fresh gameplay with each run.
  * **Player Control**: Navigate Pac-Man using the arrow keys to eat dots and avoid ghosts.
  * **Intelligent Ghost AI**: Four distinct ghosts (Blinky, Pinky, Inky, and Clyde) chase Pac-Man using the BFS algorithm to find the shortest path.
  * **Ghost Personalities**:
      * **Blinky (Red)**: Always targets Pac-Man's current position directly.
      * **Pinky (Pink)**: Tries to ambush Pac-Man by targeting a few tiles in front of Pac-Man's current direction.
      * **Inky (Cyan)**: A more complex ghost that targets a point based on Pac-Man's position and Blinky's position, aiming to "sandwich" Pac-Man.
      * **Clyde (Orange)**: Chases Pac-Man when far away but retreats to his corner if he gets too close to Pac-Man.
  * **Score Tracking**: Earn points for every dot Pac-Man eats.
  * **Game Over/Win Conditions**: The game ends if Pac-Man is caught by a ghost or if all dots are eaten.

-----

## Algorithms Explained

### Breadth-First Search (BFS) for Ghost Movement

The core of the ghost AI is the **Breadth-First Search (BFS)** algorithm. BFS is a graph traversal algorithm that finds the shortest path between a starting node and a target node in an unweighted graph (like our maze grid).

**How it works here**:

1.  **Queue Initialization**: When a ghost needs to move, it starts a BFS from its current position. A queue is initialized with the ghost's current coordinates and an empty path.
2.  **Exploration**: The algorithm explores neighboring empty cells (not walls) level by level, adding them to the queue along with the path taken to reach them.
3.  **Path Reconstruction**: When the target cell (determined by each ghost's personality) is reached, the algorithm reconstructs the path from the starting position to the target.
4.  **First Step**: The ghost then takes the *first step* in that shortest path. This ensures that ghosts always take the most direct route to their target, avoiding walls and finding optimal paths.

This approach makes the ghosts seem intelligent and provides a good challenge for the player, as they are always pursuing Pac-Man efficiently based on their target.

-----

## Getting Started

### Prerequisites

Make sure you have Python 3 installed. You'll also need the Pygame library:

```bash
pip install pygame
```

### Installation and Setup

1.  **Clone the repository (or download the files)**:

    ```bash
    git clone https://github.com/yourusername/pacman-bfs-ghosts.git
    cd pacman-bfs-ghosts
    ```

    *(Replace `https://github.com/yourusername/pacman-bfs-ghosts.git` with the actual link to your repository if you host it on GitHub/GitLab/etc.)*

2.  **Ensure Asset Folder**: Make sure you have an `assets` folder in the root directory of the game, containing all the necessary image files (`pac.png`, `blinky.png`, `pinky.png`, `inky.png`, `clyde.png`, `dot.png`, `block1.png`).

3.  **Run the game**:

    ```bash
    python main.py
    ```

-----

## Game Structure

The project is organized into several modules for clarity and maintainability:

  * `main.py`: The main game loop and entry point. Initializes game objects and handles events.
  * `constants.py`: Stores all global constants like screen dimensions, colors, and FPS.
  * `utils.py`: Contains utility functions such as image loading, maze generation, and the BFS pathfinding algorithm.
  * `maze.py`: Defines the `Maze` class, responsible for generating and rendering the game environment (walls and dots).
  * `player.py`: Implements the `Player` (Pac-Man) class, handling movement and drawing.
  * `ghost.py`: Defines the `Ghost` class, including their unique AI targeting logic and movement using BFS.

-----

## How to Play

  * **Move Pac-Man**: Use the **Arrow Keys** (Up, Down, Left, Right) to control Pac-Man's movement.
  * **Eat Dots**: Guide Pac-Man to eat all the small dots scattered throughout the maze to gain points.
  * **Avoid Ghosts**: Do not let any of the four ghosts catch Pac-Man.
  * **Win**: Clear the entire maze by eating all the dots.
  * **Lose**: Get caught by a ghost.
---

## Acknowledgments

* Inspired by the classic Pac-Man game.
* Pygame for simplifying game development in Python.
* **Assets from**:
    * [Pacman Tiles by arcanecrow](https://opengameart.org/content/pacman-tiles) (OpenGameArt.org)
    * [Pac-Man Game Art by Pixelaholic](https://pixelaholic.itch.io/pac-man-game-art) (itch.io)
    * Inspired by the classic Pac-Man game.
    * Pygame for simplifying game development in Python.

-----
