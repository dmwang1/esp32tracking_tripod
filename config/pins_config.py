"""Pin configuration for ESP32-CAM"""

# Camera pins
CAMERA_PINS = {
    "PWDN_GPIO_NUM": 32,
    "RESET_GPIO_NUM": -1,
    "XCLK_GPIO_NUM": 0,
    "SIOD_GPIO_NUM": 26,
    "SIOC_GPIO_NUM": 27,
    "Y9_GPIO_NUM": 35,
    "Y8_GPIO_NUM": 34,
    "Y7_GPIO_NUM": 39,
    "Y6_GPIO_NUM": 36,
    "Y5_GPIO_NUM": 21,
    "Y4_GPIO_NUM": 19,
    "Y3_GPIO_NUM": 18,
    "Y2_GPIO_NUM": 5,
    "VSYNC_GPIO_NUM": 25,
    "HREF_GPIO_NUM": 23,
    "PCLK_GPIO_NUM": 22
}

# Control pins
LED_PIN = 33  # Status LED
FLASH_PIN = 4  # Flash LED