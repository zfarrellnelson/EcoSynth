# Runs on the Pi4 (Zynthian). Listens for UDP lines from the Pi3's
# DHT22 sender and sends HUMIDITY ONLY.
import socket
import mido

# ---- CONFIGURATION ----
LISTEN_IP = "0.0.0.0"    # listen on all interfaces (only one to receive on over the direct cable)
LISTEN_PORT = 5006       # must match PI4_PORT_HUMIDITY in dht_send.py

MIDI_CHANNEL = 0          # 0 = channel 1 in MIDI terminology

HUMIDITY_CC = 106
MIN_HUMIDITY = 20.0        # humidity that maps to CC 0
MAX_HUMIDITY = 80.0        # humidity that maps to CC 127
HUMIDITY_PORT_NAME = "DHT22 Humidity"

# ---- OPEN MIDI PORT ----
# Own virtual MIDI port rather than connecting directly to FluidSynth,
# so Zynthian's MIDI router (and Global Learn) sees this as its own
# separate input source, doing it the same way as mpu-9250.
humidity_outport = mido.open_output(HUMIDITY_PORT_NAME, virtual=True)
print(f"Created virtual MIDI port: '{HUMIDITY_PORT_NAME}'")
print("Next step is to connect it to Zynthian's MIDI input using jack_connect/aconnect.")

# ---- SOCKET SETUP ----
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((LISTEN_IP, LISTEN_PORT))

print(f"Listening for DHT22 data on {LISTEN_IP}:{LISTEN_PORT}. Ctrl+C to stop.")


def parse_humidity(line):
    """Pull only the humidity out of 'Temp:23.4,Humidity:45.6'. Returns None on bad input."""
    try:
        parts = dict(item.split(":") for item in line.split(","))
        return float(parts["Humidity"])
    except (ValueError, KeyError):
        return None


def scale_to_midi(value, in_min, in_max):
    """Map a value to the 0-127 MIDI CC range, clamp at the edges."""
    if value < in_min:
        value = in_min
    if value > in_max:
        value = in_max
    scaled = (value - in_min) / (in_max - in_min) * 127
    return int(scaled)


last_humidity_cc = -1

try:
    while True:
        data, addr = sock.recvfrom(1024)  # buffer size in bytes
        line = data.decode("utf-8").strip()

        humidity = parse_humidity(line)

        if humidity is not None:
            humidity_cc = scale_to_midi(humidity, MIN_HUMIDITY, MAX_HUMIDITY)

            # only send if the value actually changed, don't want to flood midi traffic
            if humidity_cc != last_humidity_cc:
                msg = mido.Message('control_change',
                                    channel=MIDI_CHANNEL,
                                    control=HUMIDITY_CC,
                                    value=humidity_cc)
                humidity_outport.send(msg)
                print(f"Humidity: {humidity_cc:>3} ({humidity:.1f}%)  ->  CC{HUMIDITY_CC}")
                last_humidity_cc = humidity_cc
        else:
            print(f"Messed up line from {addr[0]}: {line!r}")

except KeyboardInterrupt:
    print("\nStopped.")
    humidity_outport.close()
    sock.close()
