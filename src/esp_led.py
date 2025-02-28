# esp_led.py - Simple LED control module
import machine
import time

class LED:
    """Class for controlling an LED"""
    
    def __init__(self, pin=4, pwm_enabled=False):
        """Initialize LED on the specified pin
        
        Args:
            pin: GPIO pin number for the LED (default: 4)
            pwm_enabled: Whether to enable PWM for brightness control
        """
        self.pin_num = pin
        self.pwm_enabled = pwm_enabled
        
        # Set up the pin
        self.pin = machine.Pin(pin, machine.Pin.OUT)
        
        # Set up PWM if enabled
        if pwm_enabled:
            self.pwm = machine.PWM(self.pin)
            self.pwm.freq(1000)  # 1kHz frequency
            self.pwm.duty(0)     # Start with LED off
        
        self._is_on = False
    
    def on(self):
        """Turn LED on"""
        if self.pwm_enabled:
            self.pwm.duty(1023)  # Max brightness
        else:
            self.pin.value(1)
        self._is_on = True
    
    def off(self):
        """Turn LED off"""
        if self.pwm_enabled:
            self.pwm.duty(0)
        else:
            self.pin.value(0)
        self._is_on = False
    
    def toggle(self):
        """Toggle LED state"""
        if self._is_on:
            self.off()
        else:
            self.on()
    
    def blink(self, count=1, delay=0.5):
        """Blink LED specified number of times
        
        Args:
            count: Number of blinks
            delay: Delay between on and off (seconds)
        """
        original_state = self._is_on
        
        for _ in range(count):
            self.on()
            time.sleep(delay)
            self.off()
            time.sleep(delay)
        
        # Restore original state
        if original_state:
            self.on()