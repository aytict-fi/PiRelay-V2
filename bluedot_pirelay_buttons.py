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



from bluedot import BlueDot
from signal import pause
from PiRelay import Relay

# Relay labels as per PiRelay.py
RELAY_LABELS = ["RELAY1", "RELAY2", "RELAY3", "RELAY4"]
relays = [Relay(label) for label in RELAY_LABELS]
relay_states = [False] * len(relays)

# BlueDot grid: 2 columns, 3 rows (enough for 5 buttons)
bd = BlueDot(cols=2, rows=3)


# Set text for each button
bd.buttons[0,0].text = "All Relays"
bd.buttons[0,1].text = "Relay 1"
bd.buttons[1,1].text = "Relay 2"
bd.buttons[0,2].text = "Relay 3"
bd.buttons[1,2].text = "Relay 4"


def set_relay(index, state):
    relay_states[index] = state
    if state:
        relays[index].on()
    else:
        relays[index].off()
    print(f"Relay {index+1} {'ON' if state else 'OFF'}")

def toggle_relay(index):
    set_relay(index, not relay_states[index])

def set_all_relays(state):
    for i in range(len(relays)):
        set_relay(i, state)
    print(f"All relays {'ON' if state else 'OFF'}")

def toggle_all_relays():
    new_state = not all(relay_states)
    set_all_relays(new_state)


# Button mapping:
# (0,0): All relays
# (0,1): Relay 1
# (1,1): Relay 2
# (0,2): Relay 3
# (1,2): Relay 4

def pressed(pos):
    print("button {}.{} pressed".format(pos.col, pos.row))
    if (pos.col, pos.row) == (0, 0):
        toggle_all_relays()
    elif (pos.col, pos.row) == (0, 1):
        toggle_relay(0)
    elif (pos.col, pos.row) == (1, 1):
        toggle_relay(1)
    elif (pos.col, pos.row) == (0, 2):
        toggle_relay(2)
    elif (pos.col, pos.row) == (1, 2):
        toggle_relay(3)
    else:
        print("Unknown button pressed.")

bd.when_pressed = pressed

print("BlueDot PiRelay (5 buttons, grid mode) started. Use the BlueDot app to control relays.")

pause()
