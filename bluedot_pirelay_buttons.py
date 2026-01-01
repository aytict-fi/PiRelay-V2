"""
bluedot_pirelay_buttons.py

Control 4 relays and all relays at once using 5 BlueDot buttons.
- Button 1: Toggle all relays on/off
- Button 2: Toggle relay 1
- Button 3: Toggle relay 2
- Button 4: Toggle relay 3
- Button 5: Toggle relay 4

Requires: bluedot, RPi.GPIO

Install dependencies:
    pip install bluedot RPi.GPIO

Connect relay IN pins to GPIO 17, 27, 22, 23 (default).
"""

from bluedot import BlueDot, Button
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

# BlueDot setup
bd = BlueDot()

# Create 5 buttons
bd.clear_buttons()

# Button 0: All relays
bd.add_button("All", position=(0, 0), color="blue")
# Button 1-4: Individual relays
bd.add_button("Relay 1", position=(1, 0), color="green")
bd.add_button("Relay 2", position=(2, 0), color="red")
bd.add_button("Relay 3", position=(3, 0), color="yellow")
bd.add_button("Relay 4", position=(4, 0), color="orange")

# Helper functions
def set_relay(index, state):
    relay_states[index] = state
    GPIO.output(RELAY_PINS[index], GPIO.HIGH if state else GPIO.LOW)
    print(f"Relay {index+1} {'ON' if state else 'OFF'}")

def toggle_relay(index):
    set_relay(index, not relay_states[index])

def set_all_relays(state):
    for i in range(len(RELAY_PINS)):
        set_relay(i, state)
    print(f"All relays {'ON' if state else 'OFF'}")

def toggle_all_relays():
    # If any relay is off, turn all on; else, turn all off
    new_state = not all(relay_states)
    set_all_relays(new_state)

# Button handlers
def handle_button(pos):
    if pos.button.text == "All":
        toggle_all_relays()
    elif pos.button.text == "Relay 1":
        toggle_relay(0)
    elif pos.button.text == "Relay 2":
        toggle_relay(1)
    elif pos.button.text == "Relay 3":
        toggle_relay(2)
    elif pos.button.text == "Relay 4":
        toggle_relay(3)
    else:
        print("Unknown button pressed.")

bd.when_pressed = handle_button

print("BlueDot PiRelay (5 buttons) started. Use the BlueDot app to control relays.")

try:
    signal.pause()  # Wait for events
finally:
    GPIO.cleanup()
    print("GPIO cleaned up.")
