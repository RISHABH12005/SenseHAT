# By Rishabh Jain
from sense_hat import SenseHat
from time import sleep
import random

sense = SenseHat()
sense.low_light = True

GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
START_DELAY = 3
MATRIX_MIN_VALUE = 0
MATRIX_MAX_VALUE = 7
MATRIX_SIZE = 8

while True:
    gameOverFlag = False
    growSnakeFlag = False
    generateRandomFoodFlag = False
    snakeMovementDelay = 0.5
    snakeMovementDelayDecrease = -0.02
    score = 0

    sense.clear()
    sense.show_message("SNAKE GAME")

    # Set default snake starting position (values are chosen by preference)
    snakePosX = [3]
    snakePosY = [6]

    # Generate random food position
    while True:
        foodPosX = random.randint(0, 7)
        foodPosY = random.randint(0, 7)
        if foodPosX != snakePosX[0] or foodPosY != snakePosY[0]:
            break

    # Set default snake starting direction (values are chosen by preference)
    movementX = 0
    movementY = -1

    while not gameOverFlag:
        # Check if snake eats food
        if foodPosX == snakePosX[0] and foodPosY == snakePosY[0]:
            growSnakeFlag = True
            generateRandomFoodFlag = True
            snakeMovementDelay += snakeMovementDelayDecrease
            score = score + 1

        # Check if snake bites itself
        for i in range(1, len(snakePosX)):
            if snakePosX[i] == snakePosX[0] and snakePosY[i] == snakePosY[0]:
                gameOverFlag = True

        # Check if game-over
        if gameOverFlag:
            break

        # Check joystick events
        for event in sense.stick.get_events():
            if event.direction == "left" and movementX != 1:
                movementX = -1
                movementY = 0
            elif event.direction == "right" and movementX != -1:
                movementX = 1
                movementY = 0
            elif event.direction == "up" and movementY != 1:
                movementY = -1
                movementX = 0
            elif event.direction == "down" and movementY != -1:
                movementY = 1
                movementX = 0

        # Grow snake
        if growSnakeFlag:
            growSnakeFlag = False
            snakePosX.append(0)
            snakePosY.append(0)

        # Move snake
        for i in range((len(snakePosX) - 1), 0, -1):
            snakePosX[i] = snakePosX[i - 1]
            snakePosY[i] = snakePosY[i - 1]

        snakePosX[0] += movementX
        snakePosY[0] += movementY

        # Check game borders
        if snakePosX[0] > MATRIX_MAX_VALUE:
            snakePosX[0] -= MATRIX_SIZE
        elif snakePosX[0] < MATRIX_MIN_VALUE:
            snakePosX[0] += MATRIX_SIZE
        if snakePosY[0] > MATRIX_MAX_VALUE:
            snakePosY[0] -= MATRIX_SIZE
        elif snakePosY[0] < MATRIX_MIN_VALUE:
            snakePosY[0] += MATRIX_SIZE

        # Spawn random food
        if generateRandomFoodFlag:
            generateRandomFoodFlag = False
            retryFlag = True
            while retryFlag:
                foodPosX = random.randint(0, 7)
                foodPosY = random.randint(0, 7)
                retryFlag = False
                for x, y in zip(snakePosX, snakePosY):
                    if x == foodPosX and y == foodPosY:
                        retryFlag = True
                        break

        # Update matrix
        sense.clear()
        sense.set_pixel(foodPosX, foodPosY, RED)
        for x, y in zip(snakePosX, snakePosY):
            sense.set_pixel(x, y, GREEN)

        # Snake speed (game loop delay)
        sleep(snakeMovementDelay)

    # Blink the dead snake
    for loop in range (5):
        sense.clear()
        sense.set_pixel(foodPosX, foodPosY, RED)
        for x, y in zip(snakePosX, snakePosY):
            sense.set_pixel(x, y, RED)
        sleep(0.5)
        
        sense.clear()
        sense.set_pixel(foodPosX, foodPosY, RED)
        for x, y in zip(snakePosX, snakePosY):
            sense.set_pixel(x, y, GREEN)
        sleep(0.5)


    sense.clear()

# Display 
    while score:
        sense.show_message("Score: {}".format(score), text_colour=YELLOW)
        # Press joystick middle button to play again
        for event in sense.stick.get_events():
            if event.direction == "middle":
                score = 0
            