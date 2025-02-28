# camera_test.py - Very basic ESP32-CAM test for MicroPython v1.11
import camera
import time
import machine
import os

# Define LED pin for status indication
status_led = machine.Pin(4, machine.Pin.OUT)

def blink_led(times=1, delay=0.2):
    """Blink the status LED a specified number of times"""
    for _ in range(times):
        status_led.value(1)
        time.sleep(delay)
        status_led.value(0)
        time.sleep(delay)

def setup_camera():
    """Initialize the ESP32-CAM camera module with basic settings"""
    print("Setting up camera...")
    
    # Flash the LED to indicate camera setup is starting
    blink_led(1, 0.5)
    
    try:
        # Initialize camera with default settings
        # Different ESP32-CAM firmware versions have different camera.init parameters
        # Try the common variations
        try:
            camera.init()  # Simplest form, often works
        except:
            try:
                camera.init(0)  # Try with camera ID
            except:
                print("Trying alternate camera initialization methods...")
                # If both failed, let's try a more specific approach
                camera.init(0, 0)  # Some versions use (id, format)
        
        print("Camera initialized!")
        
        # Try to set frame size if available
        # Common frame size values: 0-10 where larger numbers are higher resolution
        # 0=QQVGA(160x120), 5=CIF(400x296), 8=VGA(640x480), 10=UXGA(1600x1200)
        try:
            print("Setting resolution...")
            camera.framesize(8)  # Try VGA resolution (640x480)
        except:
            print("Could not set resolution, using default")
        
        # Try to set quality if available
        try:
            print("Setting quality...")
            camera.quality(12)  # Quality (10-63, lower is better)
        except:
            print("Could not set quality, using default")
        
        print("Camera setup complete!")
        blink_led(2, 0.2)  # Double blink for success
        return True
    
    except Exception as e:
        print("Error initializing camera:", e)
        blink_led(5, 0.1)  # Rapid blink for error
        return False

def capture_image(filename="test.jpg"):
    """Capture an image and save it to the filesystem"""
    print("Capturing image as", filename)
    
    try:
        # Signal capture with LED
        blink_led(1, 0.1)
        
        # Capture the image
        buf = camera.capture()
        
        # Save the image to filesystem
        with open(filename, 'wb') as f:
            f.write(buf)
        
        print("Image captured and saved as", filename)
        print("Image size:", len(buf), "bytes")
        
        # Success signal - longer blink
        blink_led(1, 0.5)
        return True
    
    except Exception as e:
        print("Error capturing image:", e)
        blink_led(3, 0.1)  # Error signal
        return False

def list_images():
    """List all JPEG images on the device"""
    print("\nImages on device:")
    count = 0
    for file in os.listdir():
        if file.endswith('.jpg'):
            try:
                size = os.stat(file)[6]  # Get file size
                print("  -", file, "(", size, "bytes )")
            except:
                print("  -", file)
            count += 1
    
    if count == 0:
        print("  No image files found.")
    
    return count

def cleanup():
    """Release the camera if possible"""
    try:
        camera.deinit()
        print("Camera released.")
    except:
        print("Note: Could not explicitly release camera.")

# Main test script
print("\n" + "="*40)
print("ESP32-CAM BASIC TEST")
print("="*40)

print("Testing camera initialization and capture...")

# Step 1: Setup camera
if setup_camera():
    # Step 2: Take a picture
    capture_image("test_photo.jpg")
    
    # Step 3: List all images
    list_images()
else:
    print("Camera setup failed. Please check your connections and firmware.")

# Always try to clean up
cleanup()
print("Test completed.")