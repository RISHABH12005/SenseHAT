# Sense HAT 

An advanced add-on board for the Raspberry Pi, equipped with environmental sensors, motion detection capabilities, an *8×8 RGB LED matrix*. It is widely used in *IoT, weather monitoring, robotics, space projects (like Astro Pi on the ISS)*.  

---

## Features  

| Feature | Description |
|---------|------------|
| *Environmental Sensors* | Measures *temperature, humidity, atmospheric pressure* when connected to a Raspberry Pi. |
| *Motion Sensors* | Built-in *gyroscope, accelerometer, magnetometer* for orientation & movement detection when used with a Raspberry Pi. |
| *LED Matrix* | 8×8 *RGB display* for visuals & messages, controlled via Raspberry Pi. |
| *Joystick* | A *5-way joystick* for user interaction, integrated with Raspberry Pi functions. |
| *Python API* | Easy-to-use *Python library* for accessing all sensors & display when used on a Raspberry Pi. |
| *Sense HAT Emulator* | A software tool that simulates the Sense HAT, allowing testing and development on a Raspberry Pi OS emulator without physical hardware. |

---

## Installation  
```bash
sudo raspi-config
```
```bash
sudo reboot
```
```bash
sudo apt install sense-hat -y
```
```bash
pip install sense-hat
```
```bash
sudo apt install sense-emu-tools -y
```
```bash
sense_emu_gui
```
