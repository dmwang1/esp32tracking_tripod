import machine
import time

led = machine.Pin(4, machine.Pin.OUT)  # Initialize the LED pin as output
servo = machine.PWM(machine.Pin(12), freq=50)  # Initialize the PWM on pin 12 for servo control

while True:
    servo.duty(26)  # Set servo to position 1 (e.g., 0 degrees)
    led.value(1)  # Turn LED on
    time.sleep(2)  # Wait for 2 second
    
    servo.duty(123)  # Set servo to position 3 (e.g., 180 degrees)
    led.value(0)  # Turn LED on
    time.sleep(2)  # Wait for 2 second
