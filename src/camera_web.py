# camera_web.py - ESP32-CAM capture and web server
import camera
import time
import machine
import os
import socket
import network
import gc

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
        camera.init()
        print("Camera initialized!")
        
        # Success signal
        blink_led(2, 0.2)
        return True
    
    except Exception as e:
        print("Error initializing camera:", e)
        blink_led(5, 0.1)  # Rapid blink for error
        return False

def capture_image(filename="capture.jpg"):
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
    images = []
    for file in os.listdir():
        if file.endswith('.jpg'):
            try:
                size = os.stat(file)[6]  # Get file size
                print("  -", file, "(", size, "bytes )")
                images.append(file)
            except:
                print("  -", file)
                images.append(file)
    
    if len(images) == 0:
        print("  No image files found.")
    
    return images

def cleanup():
    """Release the camera if possible"""
    try:
        camera.deinit()
        print("Camera released.")
    except:
        print("Note: Could not explicitly release camera.")

def setup_ap():
    """Set up the ESP32 as an access point if it isn't already"""
    ap = network.WLAN(network.AP_IF)
    if not ap.active():
        print("Activating access point...")
        ap.active(True)
        ap.config(essid='ESP32-CAM', password='micropython', authmode=network.AUTH_WPA_WPA2_PSK)
        time.sleep(1)
    
    print("Access Point active")
    print("SSID: ESP32-CAM")
    print("Password: micropython")
    print("IP Address:", ap.ifconfig()[0])
    return ap.ifconfig()[0]

def start_web_server():
    """Start a simple web server to view images and capture new ones"""
    # Set up access point
    ip = setup_ap()
    
    # Create a socket server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('', 80))
    s.listen(5)
    
    print("Web server started at http://{}".format(ip))
    print("Connect to the ESP32-CAM WiFi network to access it")
    
    while True:
        try:
            # Garbage collection to free memory
            gc.collect()
            
            # Accept connection
            conn, addr = s.accept()
            print("Connection from:", addr)
            
            # Get request
            request = conn.recv(1024).decode()
            print("Request:", request.split('\r\n')[0])
            
            # Parse request
            if "GET /capture" in request:
                # Capture a new image
                print("Capturing image from web request")
                capture_image("webcam.jpg")
                
                # Redirect to the main page
                response = "HTTP/1.1 303 See Other\r\nLocation: /\r\n\r\n"
                conn.send(response)
                
            elif "GET /image.jpg" in request:
                # Serve the latest image
                try:
                    with open("webcam.jpg", "rb") as f:
                        jpg = f.read()
                    
                    # Send HTTP response
                    conn.send("HTTP/1.1 200 OK\r\n")
                    conn.send("Content-Type: image/jpeg\r\n")
                    conn.send("Content-Length: {}\r\n".format(len(jpg)))
                    conn.send("\r\n")
                    
                    # Send the image in chunks (important for larger images)
                    chunk_size = 1024
                    for i in range(0, len(jpg), chunk_size):
                        conn.send(jpg[i:i+chunk_size])
                    
                    print("Image sent")
                except:
                    # If no image available, send error
                    conn.send("HTTP/1.1 404 Not Found\r\n\r\n")
                    conn.send("Image not found")
            
            else:
                # Serve the main page
                images = list_images()
                
                html = """<!DOCTYPE html>
<html>
<head>
<title>ESP32-CAM Web Server</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body {
    font-family: Arial, sans-serif;
    text-align: center;
    margin: 0;
    padding: 20px;
}
img {
    max-width: 100%;
    height: auto;
    margin: 10px 0;
    border: 1px solid #ddd;
}
.button {
    background-color: #4CAF50;
    border: none;
    color: white;
    padding: 15px 32px;
    text-align: center;
    display: inline-block;
    font-size: 16px;
    margin: 10px 2px;
    cursor: pointer;
    border-radius: 4px;
}
</style>
</head>
<body>
<h1>ESP32-CAM Web Server</h1>
<a href="/capture" class="button">Capture Image</a>
<div>
<h2>Current Image:</h2>
<img src="/image.jpg" id="cam-image">
<script>
// Auto-refresh the image every 5 seconds if auto-refresh is enabled
var imageElement = document.getElementById('cam-image');
imageElement.onload = function() {
    console.log('Image loaded');
};
imageElement.onerror = function() {
    console.log('Image failed to load');
    this.src = '';
};
</script>
</div>
<div>
<h2>Available Images:</h2>
"""
                for img in images:
                    html += "<p>{} ({} bytes)</p>".format(
                        img, os.stat(img)[6]
                    )
                
                html += """
</div>
</body>
</html>
"""
                # Send HTTP response
                conn.send("HTTP/1.1 200 OK\r\n")
                conn.send("Content-Type: text/html\r\n")
                conn.send("Connection: close\r\n\r\n")
                conn.send(html)
            
            # Close connection
            conn.close()
            
        except Exception as e:
            print("Web server error:", e)
            try:
                conn.close()
            except:
                pass
            
            # Flash error pattern
            blink_led(2, 0.1)

# Main function
def run():
    print("\n" + "="*40)
    print("ESP32-CAM WEB SERVER")
    print("="*40)
    
    # Setup camera
    if not setup_camera():
        print("Camera setup failed. Check connections.")
        return
    
    # Capture initial image
    capture_image("webcam.jpg")
    
    # Start web server
    print("\nStarting web server...")
    start_web_server()

# Run the main function
if __name__ == "__main__":
    try:
        run()
    except KeyboardInterrupt:
        print("\nServer stopped.")
        cleanup()
    except Exception as e:
        print("Error:", e)
        cleanup()