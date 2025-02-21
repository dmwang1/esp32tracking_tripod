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

   '''
   # Erase flash
   esptool.py --port /dev/tty.usbserial-A5069RR4 erase_flash

    # Flash firmware
   esptool.py --port /dev/tty.usbserial-A5069RR4 --baud 460800 write_flash -z 0x1000 ESP32_GENERIC_S3-20231227-v1.22.0-544-g03032bd36.bin


   esptool.py --port /dev/tty.usbserial-A5069RR4 erase_flash
esptool.py --port /dev/tty.usbserial-A5069RR4 --baud 460800 write_flash -z 0x1000 firmware/esp32-20240105-v1.22.1.bin
'''
ls /dev/tty.*     

3. Upload code:
   ```bash
   ampy --port COM3 put src/boot.py
   ampy --port COM3 put src/main.py
   ```

# esp32tracking_tripod


# To activate (run this whenever you start working)
source venv/bin/activate

# To deactivate (when you're done)
deactivate

# To see what packages are installed
pip list
