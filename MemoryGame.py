import time
import random
import keyboard
from sense_hat import SenseHat

sense = SenseHat()

# Colors
empty = (0, 0, 0)
selected_color = (0, 255, 0)
tile_color = (255, 0, 0)

# Helper Functions
def clear_screen():
    sense.clear()

def display_tiles(tiles):
    grid = [empty] * 64
    for (x, y) in tiles:
        for dx in range(2):
            for dy in range(2):
                grid[(y + dy) * 8 + (x + dx)] = tile_color
    sense.set_pixels(grid)

def highlight_player_selection(position, selected_tiles):
    grid = [empty] * 64
    
    # Highlight selected tiles
    for (x, y) in selected_tiles:
        for dx in range(2):
            for dy in range(2):
                grid[(y + dy) * 8 + (x + dx)] = selected_color

    # Highlight current selector
    for dx in range(2):
        for dy in range(2):
            grid[(position[1] + dy) * 8 + (position[0] + dx)] = (0, 0, 255)  # Blue for selector
    
    sense.set_pixels(grid)

def move_selector(position, direction):
    """Moves the selector based on keyboard input."""
    x, y = position
    if direction == "up" and y > 0:
        y -= 2
    elif direction == "down" and y < 6:
        y += 2
    elif direction == "left" and x > 0:
        x -= 2
    elif direction == "right" and x < 6:
        x += 2
    return x, y

# Main Game Loop
def memory_tile_game():
    level = 1
    while True:
        # Generate random 2x2 tiles
        num_tiles = level + 2
        tiles = random.sample([(x, y) for x in range(0, 8, 2) for y in range(0, 8, 2)], num_tiles)
        
        # Display the tiles
        display_tiles(tiles)
        time.sleep(1)
        clear_screen()

        # Player interaction
        position = (0, 0)
        selected_tiles = set()

        while len(selected_tiles) < num_tiles:
            highlight_player_selection(position, selected_tiles)
            if keyboard.is_pressed("up"):  # Move up
                position = move_selector(position, "up")
                time.sleep(0.2)  # Delay to prevent rapid input
            elif keyboard.is_pressed("down"):  # Move down
                position = move_selector(position, "down")
                time.sleep(0.2)
            elif keyboard.is_pressed("left"):  # Move left
                position = move_selector(position, "left")
                time.sleep(0.2)
            elif keyboard.is_pressed("right"):  # Move right
                position = move_selector(position, "right")
                time.sleep(0.2)
            elif keyboard.is_pressed("space"):  # Select tile
                if position not in selected_tiles:
                    selected_tiles.add(position)
                time.sleep(0.2)

        # Check results
        if set(tiles) == selected_tiles:
            sense.show_message("You Win!", text_colour=(0, 255, 0))
            level += 1  # Increase difficulty
        else:
            sense.show_message("You Lose!", text_colour=(255, 0, 0))
            

# Run the game
try:
    memory_tile_game()
except KeyboardInterrupt:
    clear_screen()
    print("Game stopped.")
