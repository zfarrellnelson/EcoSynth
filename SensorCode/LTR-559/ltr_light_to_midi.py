#!/usr/bin/env python3
import time
import re
import mido
import ltr559

# --- MIDI setup: find snd-virmidi port dynamically (card numbers shift on reboot) ---
def find_virmidi_port():
    for name in mido.get_output_names():
        if re.search(r'VirMIDI \d+-0\b', name):
            return name
    raise RuntimeError("No VirMIDI port found. Check /etc/modules has snd-virmidi loaded.")

port_name = find_virmidi_port()
outport = mido.open_output(port_name)
print(f"Using MIDI port: {port_name}")

# --- Sensor setup ---
sensor = ltr559.LTR559()
time.sleep(0.5)  # a little delay before first read

# --- CC assignment ---
CC_LUX = 107
MIDI_CHANNEL = 0  # channel 1

# --- Calibration range ---
LUX_MIN, LUX_MAX = 0, 1000  # tune depending on room

def scale_to_midi(value, in_min, in_max):
    value = max(in_min, min(in_max, value))
    return int((value - in_min) / (in_max - in_min) * 127)

last_lux_cc = -1

print("Running. Change light to see CC output. Ctrl+C to stop.")

try:
    while True:
        lux = sensor.get_lux()
        lux_cc = scale_to_midi(lux, LUX_MIN, LUX_MAX)

        if lux_cc != last_lux_cc:
            outport.send(mido.Message('control_change', channel=MIDI_CHANNEL,
                                       control=CC_LUX, value=lux_cc))
            print(f"Lux: {lux} -> CC{CC_LUX}={lux_cc}")
            last_lux_cc = lux_cc

        time.sleep(0.05)  # ~20Hz poll rate

except KeyboardInterrupt:
    print("\nStopped.")
    outport.close()
