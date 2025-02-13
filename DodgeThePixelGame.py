from sense_hat import SenseHat
import time
import random
import keyboard

# Initialize Sense HAT
sense = SenseHat()
sense.clear()

# Colors
ship_color = (0, 255, 0)      # Green spaceship
asteroid_color = (255, 0, 0)  # Red asteroids
bg_color = (0, 0, 0)          # Black background

# Game variables
ship_position = 3            # Initial spaceship position (bottom row, center)
asteroids = []               # List to track asteroids
score = 0                    # Initial score
level = 1                    # Initial level of the game
max_level = 5                # Maximum level
level_speeds = [0.5, 0.4, 0.3, 0.2, 0.1]  # Speed thresholds for each level

# Function to draw spaceship and asteroids on the LED matrix
def draw():
    sense.clear(bg_color)
    # Draw spaceship
    sense.set_pixel(ship_position, 7, ship_color)
    # Draw asteroids
    for asteroid in asteroids:
        sense.set_pixel(asteroid[0], asteroid[1], asteroid_color)

# Function to update asteroid positions and check for collisions
def update_asteroids():
    global score, level
    new_asteroids = []
    for asteroid in asteroids:
        # Move asteroid down by one row
        asteroid[1] += 1
        # Check for collision with spaceship
        if asteroid[1] == 7 and asteroid[0] == ship_position:
            sense.show_message("Game Over!", text_colour=(255, 0, 0))
            sense.show_message("Score: " + str(score), text_colour=(255, 255, 255))
            return False
        # Only keep asteroids that are still on the screen
        if asteroid[1] < 8:
            new_asteroids.append(asteroid)
        else:
            # Increase score when asteroid is dodged
            score += 1
    # Add a new asteroid at the top with random x position
    if random.random() < 0.3:  # 30% chance to spawn a new asteroid each update
        new_asteroids.append([random.randint(0, 7), 0])
    # Update the list of asteroids
    asteroids.clear()
    asteroids.extend(new_asteroids)
    return True

# Function to check if the player should level up
def check_level_up():
    global level
    if score >= level * 10 and level < max_level:
        level += 1
        sense.show_message(f"Level {level}", text_colour=(0, 255, 255))

# Main game loop
sense.show_message("Dodge the Pixel", text_colour=(0, 255, 0))
running = True
while running:
    # Draw everything
    draw()
    # Update asteroid positions and check for collisions
    running = update_asteroids()
    # Check if the player should level up
    check_level_up()
    # Wait for a brief moment based on game speed
    time.sleep(level_speeds[level - 1])
    # Check for keyboard input to move spaceship
    if keyboard.is_pressed("left") and ship_position > 0:
        ship_position -= 1
        time.sleep(0.1)  # Add delay to prevent rapid movement
    elif keyboard.is_pressed("right") and ship_position < 7:
        ship_position += 1
        time.sleep(0.1)

# Clear screen at the end of the game
sense.clear()
