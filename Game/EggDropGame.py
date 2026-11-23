from sense_hat import SenseHat
import random
import time

sense = SenseHat()
x = 3
y = 7
score = 0
egg_speed = 0.7
egg_x = random.randint(0, 7)
egg_y = 0
lives = 3
red= [255,0,0]
sense.show_message("You Have 3 Lives!", text_colour=[255,0,0], scroll_speed = 0.05)
while True:
    # Clear the LED matrix
    #egg_speed+=0.1
    sense.clear()
   
    # Draw the basket
    sense.set_pixel(x, y, 255, 255, 0)
   
    # Draw the egg
    if egg_y >7:
        egg_y=0
        egg_x = random.randint(0, 7)
    
    sense.set_pixel(egg_x, egg_y, 255, 0, 0)
    
    events = sense.stick.get_events()
    for event in events:
            # Update the basket's position based on the joystick direction
        if event.direction == "left" and event.action == "pressed":
            x = max(x - 1, 0)
            #print(x)
        elif event.direction == "right" and event.action == "pressed":
            x = min(x + 1, 7)
            #print(x)
    
    if x == egg_x and y == egg_y:
        score += 1
    elif egg_y == 7:
        lives -=1
        print("Lives:",lives)
        
    if lives == 0:
        sense.show_message("GAME OVER", scroll_speed = 0.05)
        s = (f"Your Score is :-{score}")
        sense.show_message(s,scroll_speed = 0.1)
        print("Score:",score)
        time.sleep(4)
        sense.clear()
        score = 0
        lives = 3

    # print(score)
    egg_y += 1
    time.sleep(egg_speed)