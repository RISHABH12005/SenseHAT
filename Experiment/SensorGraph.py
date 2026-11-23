from sense_hat import SenseHat
import time
from datetime import datetime
import matplotlib.pyplot as plt
sense = SenseHat()
TEMP_CORRECTION = -2.0
timestamps = []
temperatures = []
humidities = []
pressures = []
plt.ion()
fig, ax = plt.subplots(figsize=(10, 6))
try:
    while True:
        raw_temp = sense.get_temperature()
        temperature = raw_temp + TEMP_CORRECTION
        humidity = sense.get_humidity()
        pressure = sense.get_pressure()
        timestamps.append(datetime.now())
        temperatures.append(temperature)
        humidities.append(humidity)
        pressures.append(pressure)
        if len(timestamps) > 50:
            timestamps = timestamps[-50:]
            temperatures = temperatures[-50:]
            humidities = humidities[-50:]
            pressures = pressures[-50:]
        ax.clear()
        ax.plot(timestamps, temperatures, 'r-', label="Temperature (°C)")
        ax.plot(timestamps, humidities, 'b-', label="Humidity (%)")
        ax.plot(timestamps, pressures, 'g-', label="Pressure (hPa)")
        ax.set_title("Sense HAT Live Data")
        ax.set_xlabel("Time")
        ax.set_ylabel("Values")
        ax.legend()
        ax.grid(True)
        plt.tight_layout()
        plt.pause(1)
except KeyboardInterrupt:
    print("Stopped")
    plt.ioff()
    plt.show()
