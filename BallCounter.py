"""
Ball Counter System
Raspberry Pi and 2 Banner Sensors
Counts scored balls from two single-file lanes
"""

import RPi.GPIO as GPIO
import time
from threading import Lock 

# Configure GPIO pins for the two sensors
SENSOR_1_PIN = 17  # GPIO pin for sensor 1
SENSOR_2_PIN = 27  # GPIO pin for sensor 2

# Glabal variables
ball_count = 0
lock = Lock()  # Lock for thread-safe access to ball_count

# Callback function
def ball_detected(channel):
    global ball_count
    with lock:  # Ensure thread-safe access to ball_count
        ball_count += 1
        print(f"Ball scored! Total count: {ball_count}")

# Main setup
def main(): 
    GPIO.setmode(GPIO.BCM) # Use BCM pin numbering

    GPIO.setup(SENSOR_1_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Set sensor 1 pin as input with pull-up resistor
    GPIO.setup(SENSOR_2_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Set sensor 2 pin as input with pull-up resistor

    # Add event detection for both sensors -------- ADJUST BOUNCETIME AS NEEDED
    GPIO.add_event_detect(SENSOR_1_PIN, GPIO.FALLING, callback=ball_detected, bouncetime=100) # Detect falling edge for sensor 1
    GPIO.add_event_detect(SENSOR_2_PIN, GPIO.FALLING, callback=ball_detected, bouncetime=100) # Detect falling edge for sensor 2

    print ("Ball Counter System Initialized. Waiting for balls to be scored...")
    print ("Press Ctrl+C to exit.")

    try:
        while True:
            time.sleep(1) # Keep the program running

    except KeyboardInterrupt:
        print("\nExiting Ball Counter System.") 

    finally:
        GPIO.cleanup() # Clean up GPIO settings
        print("GPIO cleaned up. Program terminated.")

# Run program 
if __name__ == "__main__":
    main()  # The main logic is already in the try-except block above