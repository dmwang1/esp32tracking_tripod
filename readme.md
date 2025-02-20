# ESP32-CAM Tracking Tripod

## Description
Computer vision-based tracking tripod using ESP32-CAM and MicroPython.

## Setup
1. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

2. Flash MicroPython:
   ```bash
   esptool.py --port COM3 erase_flash
   esptool.py --port COM3 --baud 460800 write_flash -z 0x1000 esp32-cam-micropython.bin
   ```

3. Upload code:
   ```bash
   ampy --port COM3 put src/boot.py
   ampy --port COM3 put src/main.py
   ```

# esp32tracking_tripod
