# Runs on the Pi4 (Zynthian). Listens for UDP lines from the Pi3's
# DHT22 sender and sends TEMPERATURE ONLY out as MIDI CC through its
# own virtual MIDI port. Deliberately a separate process from the
# humidity receiver, so you can stop this one (e.g. to isolate it for
# Zynthian's MIDI Learn) without taking down the humidity port too.
import socket
import mido

# ---- CONFIGURATION ----
LISTEN_IP = "0.0.0.0"    # listen on all interfaces (only one to receive on over the direct cable)
LISTEN_PORT = 5005       # must match PI4_PORT_TEMP in dht_send.py

MIDI_CHANNEL = 0          # 0 = channel 1 in MIDI terms

TEMP_CC = 105              # undefined/free CC range is 102-119, safe from conflicts
MIN_TEMP = 15.0            # temperature that maps to CC 0   (tune after watching real readings)
MAX_TEMP = 35.0            # temperature that maps to CC 127 (tune after watching real readings)
TEMP_PORT_NAME = "DHT22 Temperature"

# ---- OPEN MIDI PORT ----
# Own virtual MIDI port rather than connecting directly to FluidSynth,
# so Zynthian's MIDI router (and Global Learn) sees this as its own
# separate input source - same approach as the MPU9250 script.
temp_outport = mido.open_output(TEMP_PORT_NAME, virtual=True)
print(f"Created virtual MIDI port: '{TEMP_PORT_NAME}'")
print("Now connect it to Zynthian's MIDI input using jack_connect/aconnect (see README/instructions).")

# ---- SOCKET SETUP ----
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((LISTEN_IP, LISTEN_PORT))

print(f"Listening for DHT22 data on {LISTEN_IP}:{LISTEN_PORT}. Ctrl+C to stop.")


def parse_temp(line):
    """Pull just the temperature out of 'Temp:23.4,Humidity:45.6'. Returns None on bad input."""
    try:
        parts = dict(item.split(":") for item in line.split(","))
        return float(parts["Temp"])
    except (ValueError, KeyError):
        return None


def scale_to_midi(value, in_min, in_max):
    """Map a value to the 0-127 MIDI CC range, clamped at the edges."""
    if value < in_min:
        value = in_min
    if value > in_max:
        value = in_max
    scaled = (value - in_min) / (in_max - in_min) * 127
    return int(scaled)


last_temp_cc = -1

try:
    while True:
        data, addr = sock.recvfrom(1024)  # buffer size in bytes, plenty for this payload
        line = data.decode("utf-8").strip()

        temperature = parse_temp(line)

        if temperature is not None:
            temp_cc = scale_to_midi(temperature, MIN_TEMP, MAX_TEMP)

            # only send if the value actually changed, keeps MIDI traffic clean
            if temp_cc != last_temp_cc:
                msg = mido.Message('control_change',
                                    channel=MIDI_CHANNEL,
                                    control=TEMP_CC,
                                    value=temp_cc)
                temp_outport.send(msg)
                print(f"Temp: {temp_cc:>3} ({temperature:.1f}C)  ->  CC{TEMP_CC}")
                last_temp_cc = temp_cc
        else:
            print(f"Malformed line from {addr[0]}: {line!r}")

except KeyboardInterrupt:
    print("\nStopped.")
    temp_outport.close()
    sock.close()
