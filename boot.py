import esp
esp.osdebug(None)
import gc
import webrepl
import network

# Set up the WiFi access point with a distinctive name
ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid='ESP32_first', password='micropython', authmode=network.AUTH_WPA_WPA2_PSK)
print("Access Point configured. Connect to WiFi network ESP32_TEST_AP")
print("IP address:", ap.ifconfig()[0])

# Start WebREPL
webrepl.start()
gc.collect()