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

# --- CC assignments ---
CC_LUX = 105
CC_PROXIMITY = 106
MIDI_CHANNEL = 0  # channel 1

# --- Calibration ranges (adjust based on your environment) ---
LUX_MIN, LUX_MAX = 0, 1000       # tune after observing your room's range
PROX_MIN, PROX_MAX = 0, 2047     # LTR-559 proximity is typically 0-2047

def scale_to_midi(value, in_min, in_max):
    value = max(in_min, min(in_max, value))
    return int((value - in_min) / (in_max - in_min) * 127)

last_lux_cc = -1
last_prox_cc = -1

print("Running. Move your hand / change light to see CC output. Ctrl+C to stop.")

try:
    while True:
        lux = sensor.get_lux()
        prox = sensor.get_proximity()

        lux_cc = scale_to_midi(lux, LUX_MIN, LUX_MAX)
        prox_cc = scale_to_midi(prox, PROX_MIN, PROX_MAX)

        # Only send on change to avoid flooding the MIDI bus
        if lux_cc != last_lux_cc:
            outport.send(mido.Message('control_change', channel=MIDI_CHANNEL,
                                       control=CC_LUX, value=lux_cc))
            print(f"Lux: {lux} -> CC{CC_LUX}={lux_cc}")
            last_lux_cc = lux_cc

        if prox_cc != last_prox_cc:
            outport.send(mido.Message('control_change', channel=MIDI_CHANNEL,
                                       control=CC_PROXIMITY, value=prox_cc))
            print(f"Prox: {prox} -> CC{CC_PROXIMITY}={prox_cc}")
            last_prox_cc = prox_cc

        time.sleep(0.05)  # ~20Hz poll rate

except KeyboardInterrupt:
    print("\nStopped.")
    outport.close()
