import keyboard
from sense_hat import SenseHat
import time
import random

sense = SenseHat()

# Initialize the Game
def initialize_game():
    sense.show_message("Snake", scroll_speed=0.08, text_colour=[0, 255, 0])
    sense.clear()

def wait_for_start():
    sense.show_message("Ready?", scroll_speed=0.08, text_colour=[0, 255, 255])
    while True:
        # Wait for keyboard input to start with W, A, S, or D
        if keyboard.is_pressed('w'):
            return "up"
        elif keyboard.is_pressed('s'):
            return "down"
        elif keyboard.is_pressed('a'):
            return "left"
        elif keyboard.is_pressed('d'):
            return "right"

def start_game():
    initialize_game()
    initial_direction = wait_for_start()
    sense.clear()
    
    # Initial snake position
    snake_x, snake_y = 4, 4
    direction = initial_direction
    game_loop(snake_x, snake_y, direction)

def time_seq():
    time.sleep(1)
    sense.show_letter("3")
    time.sleep(1)
    sense.show_letter("2")
    time.sleep(1)
    sense.show_letter("1")
    time.sleep(1)
    sense.clear()

def update_apple(random_x, random_y):
    sense.set_pixel(random_x, random_y, 255, 255, 255)
    random_x = random.randint(0, 7)
    random_y = random.randint(0, 7)
    sense.set_pixel(random_x, random_y, 0, 255, 0)
    return random_x, random_y

def game_loop(snake_x, snake_y, direction):
    time_seq()
    sense.clear(255, 255, 255)
    sense.set_pixel(snake_x, snake_y, 0, 0, 255)
    
    snake_body = [(snake_x, snake_y)]  # Start with the snake's head
    random_x, random_y = random.randint(0, 7), random.randint(0, 7)
    sense.set_pixel(random_x, random_y, 0, 255, 0)
    
    snake_alive = True
    points = 0
    action = direction  # Start with the initial direction
    
    while snake_alive:
        time.sleep(0.5)  # Adjusted delay for slower movement (0.3 seconds)

        # Check for keyboard input and update direction if a valid key is pressed
        if keyboard.is_pressed('w') and action != "down":
            action = "up"
        elif keyboard.is_pressed('s') and action != "up":
            action = "down"
        elif keyboard.is_pressed('a') and action != "right":
            action = "left"
        elif keyboard.is_pressed('d') and action != "left":
            action = "right"
        
        # Move the snake in the current direction
        if action == "up":
            snake_y -= 1
        elif action == "down":
            snake_y += 1
        elif action == "left":
            snake_x -= 1
        elif action == "right":
            snake_x += 1

        # Handle wrapping around the screen
        snake_x %= 8
        snake_y %= 8
        
        # Check if the snake has eaten the apple
        if snake_x == random_x and snake_y == random_y:
            random_x, random_y = update_apple(random_x, random_y)
            points += 1
        else:
            # Remove the last segment of the snake if no apple is eaten
            tail_x, tail_y = snake_body.pop(0)
            sense.set_pixel(tail_x, tail_y, 255, 255, 255)

        # Update the snake's body
        snake_body.append((snake_x, snake_y))
        sense.set_pixel(snake_x, snake_y, 0, 0, 255)

        # Draw the snake's body
        for segment in snake_body[:-1]:  # Don’t draw the head again
            sense.set_pixel(segment[0], segment[1], 0, 0, 255)

        # Check for self-collision (snake runs into itself)
        if (snake_x, snake_y) in snake_body[:-1]:
            snake_alive = False

    # Game over handling
    sense.show_message("Game Over", text_colour=[255, 0, 0])

# Starting the Game
start_game()
