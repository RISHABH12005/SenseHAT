from sense_hat import SenseHat
from time import sleep
sense = SenseHat()
r = 120
g = 0
b = 0
name = "Resberry Pi 4"
for i in name:   
    sense.show_letter(i,(r,g,b),(255,255,255))
    sleep(2)
sense.clear((0,0,255)) #indicating end