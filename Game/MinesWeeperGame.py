from sense_hat import SenseHat
import keyboard
import random
import time

# Initialize Sense HAT
sense = SenseHat()

# Constants
GRID_SIZE = 8
NUM_MINES = 10

# Colors
WHITE = [255, 255, 255]
BLACK = [0, 0, 0]
GREEN = [0, 255, 0]
YELLOW = [255, 255, 0]
RED = [255, 0, 0]
MINE = [255, 0, 0]  # Red for game over

# Game state
grid = [['HIDDEN' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
mines = set()
cursor_x, cursor_y = 0, 0  # Starting cursor position

def initialize_mines():
    """Place mines randomly on the grid."""
    global mines
    mines = set()
    while len(mines) < NUM_MINES:
        x, y = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
        mines.add((x, y))

def count_adjacent_mines(x, y):
    """Count the number of mines around a cell."""
    count = 0
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            nx, ny = x + dx, y + dy
            if (nx, ny) in mines and (dx, dy) != (0, 0):
                count += 1
    return count

def draw_grid():
    """Render the grid on the Sense HAT."""
    pixels = []
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            if (x, y) == (cursor_x, cursor_y):
                pixels.append(BLACK)  # Show cursor position
            elif grid[y][x] == 'HIDDEN':
                pixels.append(WHITE)
            elif grid[y][x] == 'FLAGGED':
                pixels.append(BLACK)
            elif grid[y][x] == 'MINE':
                pixels.append(MINE)
            else:
                # Color based on adjacent mine count
                count = grid[y][x]
                if count == 1:
                    pixels.append(GREEN)
                elif count == 2:
                    pixels.append(YELLOW)
                elif count >= 3:
                    pixels.append(RED)
    sense.set_pixels(pixels)

def reveal(x, y):
    """Reveal cell and adjacent cells if it's empty."""
    if grid[y][x] != 'HIDDEN':
        return

    if (x, y) in mines:
        # Game over condition
        for mx, my in mines:
            grid[my][mx] = 'MINE'
        draw_grid()
        sense.show_message("Game Over!", text_colour=[255, 0, 0])
        reset_game()
        return

    mine_count = count_adjacent_mines(x, y)
    grid[y][x] = mine_count

    # Reveal adjacent cells if no adjacent mines
    if mine_count == 0:
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                    reveal(nx, ny)

    draw_grid()
    check_win()

def flag_cell(x, y):
    """Mark or unmark a cell as flagged."""
    if grid[y][x] == 'HIDDEN':
        grid[y][x] = 'FLAGGED'
    elif grid[y][x] == 'FLAGGED':
        grid[y][x] = 'HIDDEN'
    draw_grid()

def check_win():
    """Check if all non-mine cells have been revealed."""
    unrevealed = sum(row.count('HIDDEN') + row.count('FLAGGED') for row in grid)
    if unrevealed == NUM_MINES:
        sense.show_message("You Win!", text_colour=[0, 255, 0])
        reset_game()

def reset_game():
    """Reset the game to its initial state."""
    global grid, cursor_x, cursor_y
    grid = [['HIDDEN' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    cursor_x, cursor_y = 0, 0
    initialize_mines()
    draw_grid()

def move_cursor(dx, dy):
    """Move the cursor by (dx, dy) within bounds."""
    global cursor_x, cursor_y
    cursor_x = max(0, min(GRID_SIZE - 1, cursor_x + dx))
    cursor_y = max(0, min(GRID_SIZE - 1, cursor_y + dy))
    draw_grid()

# Initialize game
initialize_mines()
draw_grid()

# Keyboard controls
while True:
    if keyboard.is_pressed('up'):
        move_cursor(0, -1)
        time.sleep(0.2)
    elif keyboard.is_pressed('down'):
        move_cursor(0, 1)
        time.sleep(0.2)
    elif keyboard.is_pressed('left'):
        move_cursor(-1, 0)
        time.sleep(0.2)
    elif keyboard.is_pressed('right'):
        move_cursor(1, 0)
        time.sleep(0.2)
    elif keyboard.is_pressed('space'):
        reveal(cursor_x, cursor_y)
        time.sleep(0.2)
    elif keyboard.is_pressed('f'):
        flag_cell(cursor_x, cursor_y)
        time.sleep(0.2)
