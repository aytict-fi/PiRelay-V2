"""
bluedot_pirelay.py

Control a relay connected to a Raspberry Pi using the BlueDot app.
- Press the BlueDot button to toggle the relay on/off.
- Requires: bluedot, RPi.GPIO

Install dependencies:
    pip install bluedot RPi.GPIO

Connect relay IN pin to GPIO 17 (default).
"""

from bluedot import BlueDot
import RPi.GPIO as GPIO
import signal

# GPIO pin where the relay is connected
RELAY_PIN = 17

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(RELAY_PIN, GPIO.OUT)
GPIO.output(RELAY_PIN, GPIO.LOW)  # Start with relay off

# Track relay state
relay_on = False

def toggle_relay():
    global relay_on
    relay_on = not relay_on
    GPIO.output(RELAY_PIN, GPIO.HIGH if relay_on else GPIO.LOW)
    print(f"Relay {'ON' if relay_on else 'OFF'}")

# Setup BlueDot
bd = BlueDot()
bd.when_pressed = toggle_relay

print("BlueDot PiRelay started. Press the BlueDot button to toggle the relay.")

try:
    signal.pause()  # Wait for events
finally:
    GPIO.cleanup()
    print("GPIO cleaned up.")
