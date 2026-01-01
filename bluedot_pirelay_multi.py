"""
bluedot_pirelay_multi.py

Control multiple relays connected to a Raspberry Pi using the BlueDot app.
- Tap different regions of the BlueDot button to control different relays.
- Requires: bluedot, RPi.GPIO

Install dependencies:
    pip install bluedot RPi.GPIO

Connect relay IN pins to GPIO 17, 27, 22, 23 (default).
"""

from bluedot import BlueDot
import RPi.GPIO as GPIO
import signal

# GPIO pins for relays
RELAY_PINS = [17, 27, 22, 23]  # You can change these as needed

# Setup GPIO
GPIO.setmode(GPIO.BCM)
for pin in RELAY_PINS:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)  # Start with relays off

# Track relay states
relay_states = [False] * len(RELAY_PINS)

def toggle_relay(relay_index):
    relay_states[relay_index] = not relay_states[relay_index]
    GPIO.output(RELAY_PINS[relay_index], GPIO.HIGH if relay_states[relay_index] else GPIO.LOW)
    print(f"Relay {relay_index+1} {'ON' if relay_states[relay_index] else 'OFF'}")

def handle_press(pos):
    # Divide BlueDot into 4 quadrants for 4 relays
    if pos.top and pos.left:
        toggle_relay(0)  # Top left
    elif pos.top and pos.right:
        toggle_relay(1)  # Top right
    elif pos.bottom and pos.left:
        toggle_relay(2)  # Bottom left
    elif pos.bottom and pos.right:
        toggle_relay(3)  # Bottom right
    else:
        print("Press in a quadrant to toggle a relay.")

# Setup BlueDot
bd = BlueDot()
bd.when_pressed = handle_press

print("BlueDot PiRelay (multi-relay) started. Tap each quadrant to toggle a relay.")

try:
    signal.pause()  # Wait for events
finally:
    GPIO.cleanup()
    print("GPIO cleaned up.")
