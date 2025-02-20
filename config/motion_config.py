"""Motion control settings"""

MOTION_SETTINGS = {
    "min_movement_threshold": 20,  # Minimum pixel difference to trigger movement
    "max_angle_per_frame": 30,     # Maximum degrees to move per frame
    "smoothing_factor": 0.5,       # Motion smoothing (0-1)
    "frame_skip": 2               # Process every nth frame
}