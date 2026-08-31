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
time.sleep(0.5)  # settle delay before first read

# --- CC assignment ---
CC_PROXIMITY = 108
MIDI_CHANNEL = 0  # channel 1

# --- Calibration range (LTR-559 proximity is typically 0-2047) ---
PROX_MIN, PROX_MAX = 0, 2047

def scale_to_midi(value, in_min, in_max):
    value = max(in_min, min(in_max, value))
    return int((value - in_min) / (in_max - in_min) * 127)

last_prox_cc = -1

print("Running. Move hand near sensor to see CC output. Ctrl+C to stop.")

try:
    while True:
        prox = sensor.get_proximity()
        prox_cc = scale_to_midi(prox, PROX_MIN, PROX_MAX)

        if prox_cc != last_prox_cc:
            outport.send(mido.Message('control_change', channel=MIDI_CHANNEL,
                                       control=CC_PROXIMITY, value=prox_cc))
            print(f"Prox: {prox} -> CC{CC_PROXIMITY}={prox_cc}")
            last_prox_cc = prox_cc

        time.sleep(0.05)  # ~20Hz poll rate

except KeyboardInterrupt:
    print("\nStopped.")
    outport.close()
