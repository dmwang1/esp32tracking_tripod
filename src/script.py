# user_script.py - Upload this file for your custom code
import time
from esp_led import LED

def run():
    """Your custom function that will be executed"""
    print("Running custom user script...")
    
    # Create LED on pin 4
    led = LED(4)
    
    # Custom blinking pattern - SOS in Morse code
    def blink_sos():
        # S: three short blinks
        for _ in range(3):
            led.on()
            time.sleep(0.2)
            led.off()
            time.sleep(0.2)
        time.sleep(0.4)
        
        # O: three long blinks
        for _ in range(3):
            led.on()
            time.sleep(0.6)
            led.off()
            time.sleep(0.2)
        time.sleep(0.4)
        
        # S: three short blinks again
        for _ in range(3):
            led.on()
            time.sleep(0.2)
            led.off()
            time.sleep(0.2)
        
        time.sleep(1)
    
    # Repeat the SOS pattern a few times
    print("Blinking SOS pattern...")
    for _ in range(3):
        blink_sos()
    
    # Turn off LED when done
    led.off()
    print("Custom script completed!")

# This will be executed when the script is run
run()