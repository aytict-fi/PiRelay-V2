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
import time
import threading

# Relay labels as per PiRelay.py
RELAY_LABELS = ["RELAY1", "RELAY2", "RELAY3", "RELAY4"]
relays = [Relay(label) for label in RELAY_LABELS]
relay_states = [False] * len(relays)

# For logging relay on/off times and counts
relay_on_times = [0.0] * len(relays)  # Timestamp when relay was last turned on
relay_on_durations = [0.0] * len(relays)  # Total ON duration for each relay
relay_on_counts = [0] * len(relays)  # Number of times each relay has been turned on

log_lock = threading.Lock()

# Background logger thread to log ON durations while running
def background_duration_logger(interval=5):
    while True:
        time.sleep(interval)
        with log_lock:
            with open("relay_on.log", "a") as f:
                now = time.time()
                for i in range(len(relays)):
                    if relay_states[i] and relay_on_times[i] > 0:
                        current_duration = relay_on_durations[i] + (now - relay_on_times[i])
                        f.write(f"Relay {i+1} ON (running) at {time.strftime('%Y-%m-%d %H:%M:%S')} (count: {relay_on_counts[i]}, duration: {current_duration:.2f} sec)\n")

# Start the background logger thread
threading.Thread(target=background_duration_logger, args=(5,), daemon=True).start()

def log_relay_event(index, event, duration=None):
    with log_lock:
        with open("relay_on.log", "a") as f:
            if event == "on":
                f.write(f"Relay {index+1} ON at {time.strftime('%Y-%m-%d %H:%M:%S')} (count: {relay_on_counts[index]})\n")
            elif event == "off" and duration is not None:
                f.write(f"Relay {index+1} OFF at {time.strftime('%Y-%m-%d %H:%M:%S')} (duration: {duration:.2f} sec, total: {relay_on_durations[index]:.2f} sec)\n")

# BlueDot grid: 2 columns, 3 rows (enough for 5 buttons)
bd = BlueDot(cols=2, rows=3)

def set_relay(index, state):
    if state and not relay_states[index]:
        # Turning ON
        relay_on_times[index] = time.time()
        relay_on_counts[index] += 1
        log_relay_event(index, "on")
    elif not state and relay_states[index]:
        # Turning OFF
        if relay_on_times[index] > 0:
            duration = time.time() - relay_on_times[index]
            relay_on_durations[index] += duration
            log_relay_event(index, "off", duration)
        relay_on_times[index] = 0.0
    relay_states[index] = state
    if state:
        relays[index].on()
    else:
        relays[index].off()
    print(f"Relay {index+1} {'ON' if state else 'OFF'}")

def toggle_relay(index):
    set_relay(index, not relay_states[index])

def set_two_relays(state):
    relay_states[0] = state
    relay_states[1] = state
    if state:
        relays[0].on()
        relays[1].on()
    else:
        relays[0].off()
        relays[1].off()
    print(f"Relays 1 and 2 {'ON' if state else 'OFF'}")

def toggle_two_relays():
    # Toggle both relays 1 and 2 together
    new_state = not (relay_states[0] and relay_states[1])
    set_two_relays(new_state)

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
    # (1,0): Relays 1 & 2 (top right)
    # (1,1): Relay 2
    # (0,2): Relay 3
    # (1,2): Relay 4

def pressed(pos):
    print("button {}.{} pressed".format(pos.col, pos.row))
    if (pos.col, pos.row) == (0, 0):
        toggle_all_relays()
    elif (pos.col, pos.row) == (0, 1):
        toggle_relay(0)
    elif (pos.col, pos.row) == (1, 0):
        toggle_two_relays()
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
