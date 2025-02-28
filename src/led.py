# File: esp_led.py
# ESP32 LED control module for MicroPython

import machine

class LED:
    """
    Class to control an LED connected to an ESP32 GPIO pin.
    Supports basic on/off functionality and PWM brightness control.
    """
    
    def __init__(self, pin_number):
        """
        Initialize the LED with the given pin number
        
        Args:
            pin_number: GPIO pin number the LED is connected to
        """
        self.pin_number = pin_number
        self.pin = machine.Pin(pin_number, machine.Pin.OUT)
        self.pwm = None
        self.is_pwm_mode = False
        
    def on(self):
        """Turn the LED on"""
        if self.is_pwm_mode:
            # If in PWM mode, stop PWM first
            self.pwm.deinit()
            self.is_pwm_mode = False
            self.pin = machine.Pin(self.pin_number, machine.Pin.OUT)
        self.pin.on()  # Modern MicroPython uses on() instead of value(1)
        
    def off(self):
        """Turn the LED off"""
        if self.is_pwm_mode:
            # If in PWM mode, stop PWM first
            self.pwm.deinit()
            self.is_pwm_mode = False
            self.pin = machine.Pin(self.pin_number, machine.Pin.OUT)
        self.pin.off()  # Modern MicroPython uses off() instead of value(0)
        
    def toggle(self):
        """Toggle the LED state"""
        if self.is_pwm_mode:
            # If in PWM mode, stop PWM first
            self.pwm.deinit()
            self.is_pwm_mode = False
            self.pin = machine.Pin(self.pin_number, machine.Pin.OUT)
        self.pin.value(not self.pin.value())
        
    def set_brightness(self, level):
        """
        Set LED brightness using PWM
        
        Args:
            level: Brightness level (0-1023)
        """
        # Ensure level is within valid range
        level = max(0, min(1023, level))
        
        # Initialize PWM if not already in PWM mode
        if not self.is_pwm_mode:
            self.pwm = machine.PWM(self.pin)
            self.pwm.freq(5000)  # Set PWM frequency to 5kHz
            self.is_pwm_mode = True
            
        # Convert 0-1023 to 0-65535 (16-bit duty cycle)
        # Modern MicroPython ESP32 uses duty_u16 with range 0-65535
        duty_value = int(level * 64)  # 65535/1023 ≈ 64
        self.pwm.duty_u16(duty_value)