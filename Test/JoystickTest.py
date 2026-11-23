from sense_hat import SenseHat
from time import sleep
sense = SenseHat()
def handle_event(event):
    if event.action == 'pressed':
        if event.direction == 'up':
            print("Joystick moved up")
        elif event.direction == 'down':
            print("Joystick moved down")
        elif event.direction == 'left':
            print("Joystick moved left")
        elif event.direction == 'right':
            print("Joystick moved right")
        elif event.direction == 'middle':
            print("Joystick pressed in")
try:
    print("Testing joystick movements. Press Ctrl+C to exit.")
    while True:
        for event in sense.stick.get_events():
            handle_event(event)
        sleep(0.1)  # Reduce CPU usage
except KeyboardInterrupt:
    print("Test ended.")