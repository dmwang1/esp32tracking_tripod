"""Camera configuration settings"""

CAMERA_SETTINGS = {
    "framesize": "VGA",  # Options: QVGA (320x240), VGA (640x480)
    "quality": 12,       # 10-63, lower means higher quality
    "brightness": 0,     # -2 to 2
    "contrast": 0,       # -2 to 2
    "saturation": 0,     # -2 to 2
    "special_effect": 0, # 0=none, 1=negative, 2=grayscale
    "wb_mode": 0,       # 0=auto, 1=sunny, 2=cloudy, 3=office, 4=home
    "fps": 20
}
