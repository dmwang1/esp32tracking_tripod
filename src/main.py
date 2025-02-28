# main.py - Automatically runs on ESP32 boot after boot.py
import time
import gc
import os
import machine

def print_header():
    """Print a header with system info"""
    print("\n" + "="*40)
    print("ESP32 AUTO-RUN SCRIPT")
    print("="*40)
   
    try:
        print("Files on device:")
        for file in os.listdir():
            print(f"  - {file}")
    except:
        print("Could not list files")
    print("="*40 + "\n")

def run_led_test():
    """Run the LED test if esp_led.py is available"""
    print("Running LED test...")
    try:
        from esp_led import LED
        
        # Create an LED instance using pin 4
        led = LED(4)
        
        # Test basic on/off functionality
        print("Testing basic on/off...")
        led.on()
        time.sleep(1)
        led.off()
        time.sleep(1)
        
        # Test blinking
        print("Testing blink pattern...")
        for _ in range(5):
            led.toggle()
            time.sleep(0.2)
            
        # Test PWM brightness control (using direct PWM if available)
        print("Testing brightness variation...")
        
        try:
            # Try using PWM for brightness control
            led_pwm = machine.PWM(machine.Pin(4))
            led_pwm.freq(1000)
            
            # Gradually increase brightness
            for i in range(0, 1024, 100):
                led_pwm.duty(i)
                time.sleep(0.1)
                
            time.sleep(0.5)
            
            # Gradually decrease brightness
            for i in range(1023, -1, -100):
                led_pwm.duty(i)
                time.sleep(0.1)
                
            # Turn off PWM
            led_pwm.deinit()
        except Exception as e:
            print(f"PWM brightness test skipped: {e}")
            # Fall back to simple blinking as alternative
            for _ in range(10):
                led.toggle()
                time.sleep(0.1)
            
        # Turn off LED when done
        led.off()
        print("LED test completed successfully!")
        return True
    except ImportError:
        print("esp_led.py module not found. Please upload it first.")
        return False
    except Exception as e:
        print(f"Error running LED test: {e}")
        return False

def run_camera_test():
    """Run the camera test if esp_camera.py is available"""
    print("Running camera test...")
    try:
        from esp_camera import Camera
        
        # Create a camera instance
        camera = Camera()
        
        # Run the camera hardware test
        camera.test_camera()
        
        # Try to capture a test image
        result = camera.capture_test_image("camera_test.jpg")
        
        if result:
            print("Camera test completed successfully!")
        else:
            print("Camera test failed")
            
        return True
    except ImportError:
        print("esp_camera.py module not found. Please upload it first.")
        return False
    except Exception as e:
        print(f"Error running camera test: {e}")
        return False

def run_custom_script(filename):
    """Run a custom script if it exists"""
    try:
        if filename in os.listdir():
            print(f"Running custom script: {filename}")
            with open(filename, 'r') as f:
                exec(f.read())
            return True
        return False
    except Exception as e:
        print(f"Error running {filename}: {e}")
        return False

def main():
    """Main function that runs on boot"""
    print_header()
    
    # Try to run custom scripts in priority order
    if run_custom_script("user_script.py"):
        print("Custom user_script.py executed")
    elif run_camera_test():
        print("Camera test executed")
    elif run_led_test():
        print("LED test executed")
    else:
        print("No valid scripts found to run")
    
    print("\nSystem running. Upload 'user_script.py' to run your own code on next boot.")
    print("Or connect via WebREPL to interact manually.")

# Run the main function
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error in main: {e}")