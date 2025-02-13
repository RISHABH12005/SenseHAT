import keyboard
from sense_hat import SenseHat
import time
import random

# Initialize Sense HAT emulator
sense = SenseHat()

# Define colors
LIGHT_BLUE = (173, 216, 230)  # Light blue color for alive cells
BLACK = (0, 0, 0)  # Black for dead cells

# Define grid size
GRID_SIZE = 8

def initialize_grid():
    """Create a random initial grid"""
    grid = []
    for i in range(GRID_SIZE):
        row = []
        for j in range(GRID_SIZE):
            # Randomly make a cell alive or dead
            row.append(LIGHT_BLUE if random.choice([True, False]) else BLACK)
        grid.append(row)
    return grid

def display_grid(grid):
    """Convert the grid to a color array for the Sense HAT"""
    color_grid = []
    for row in grid:
        for cell in row:
            color_grid.append(cell)
    sense.set_pixels(color_grid)

def get_neighbors(x, y):
    """Get the neighbors of a given cell (including diagonal neighbors)"""
    neighbors = []
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue  # Skip the cell itself
            nx, ny = (x + dx) % GRID_SIZE, (y + dy) % GRID_SIZE
            neighbors.append((nx, ny))
    return neighbors

def count_alive_neighbors(grid, x, y):
    """Count the number of live neighbors for a cell"""
    neighbors = get_neighbors(x, y)
    alive_count = 0
    for nx, ny in neighbors:
        if grid[nx][ny] == LIGHT_BLUE:
            alive_count += 1
    return alive_count

def next_generation(grid):
    """Generate the next generation grid based on the current grid"""
    new_grid = [[BLACK for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            alive_neighbors = count_alive_neighbors(grid, x, y)
            if grid[x][y] == LIGHT_BLUE:
                if alive_neighbors in [2, 3]:
                    new_grid[x][y] = LIGHT_BLUE  # Cell stays alive
                else:
                    new_grid[x][y] = BLACK  # Cell dies
            else:
                if alive_neighbors == 3:
                    new_grid[x][y] = LIGHT_BLUE  # Cell becomes alive
                else:
                    new_grid[x][y] = BLACK  # Cell stays dead
    return new_grid

def is_all_dead(grid):
    """Check if all cells are dead"""
    for row in grid:
        if any(cell == LIGHT_BLUE for cell in row):
            return False
    return True

def is_static(grid, previous_grid):
    """Check if the current grid is the same as the previous grid (static)"""
    return grid == previous_grid

def display_end_message():
    """Display end message on Sense HAT"""
    sense.show_message("Game Over! Press Any Key to Restart", text_colour=(255, 0, 0))

def wait_for_restart():
    """Wait for keyboard input to restart the game"""
    display_end_message()
    # Wait for any key press to restart
    keyboard.wait('space')  # Press 'space' to restart
    sense.clear()

def main():
    while True:
        grid = initialize_grid()
        previous_grid = None
        
        while True:
            display_grid(grid)
            
            # Check if all cells are dead
            if is_all_dead(grid):
                wait_for_restart()
                break  # Restart the game loop
            
            # Check if the grid is static (no changes between generations)
            if previous_grid and is_static(grid, previous_grid):
                wait_for_restart()
                break  # Restart the game loop
            
            # Update the grid for the next generation
            previous_grid = [row[:] for row in grid]  # Deep copy of the grid
            grid = next_generation(grid)
            
            time.sleep(0.5)  # Pause for a moment before the next generation

if __name__ == "__main__":
    main()
