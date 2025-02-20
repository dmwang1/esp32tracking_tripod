# boot.py - runs on boot-up
import esp
import esp32
from machine import Pin, UART
import camera
import time

# Initialize the camera
def init_camera():
    # Camera pins for ESP32-CAM
    camera_config = {
        "framesize": camera.FRAME_VGA,
        "format": camera.JPEG,
        "xclk_freq": 20000000,
        "fb_location": camera.PSRAM,
        "jpeg_quality": 12,
        "fb_count": 2,
        "pin_pwdn": 32,
        "pin_reset": -1,
        "pin_xclk": 0,
        "pin_sscb_sda": 26,
        "pin_sscb_scl": 27,
        "pin_d7": 35,
        "pin_d6": 34,
        "pin_d5": 39,
        "pin_d4": 36,
        "pin_d3": 21,
        "pin_d2": 19,
        "pin_d1": 18,
        "pin_d0": 5,
        "pin_vsync": 25,
        "pin_href": 23,
        "pin_pclk": 22
    }
    
    try:
        camera.init(camera_config)
        print("Camera initialized successfully")
        return True
    except Exception as e:
        print("Camera initialization failed:", str(e))
        return False

# LED for status indication
status_led = Pin(33, Pin.OUT)

def blink_led(times=1):
    for _ in range(times):
        status_led.on()
        time.sleep(0.2)
        status_led.off()
        time.sleep(0.2)
        #comment

# Main setup
def setup():
    print("Starting ESP32-CAM setup...")
    
    # Initialize camera
    if init_camera():
        blink_led(2)  # Two blinks for success
    else:
        blink_led(5)  # Five blinks for failure
        return False
    
    print("Setup completed successfully")
    return True

if __name__ == "__main__":
    setup()