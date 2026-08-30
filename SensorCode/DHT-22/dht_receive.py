# Runs on the Pi4 (Zynthian). Listens for UDP lines from the Pi3's
# DHT22 sender and sends temperature and humidity out as MIDI CC through
# two SEPARATE virtual MIDI ports (so each can be MIDI-learned to a
# different parameter independently, same as the MPU9250 -> CC script):
#   Temperature -> "DHT22 Temperature" port, CC 105
#   Humidity    -> "DHT22 Humidity"    port, CC 106
import socket
import mido

# ---- CONFIGURATION ----
LISTEN_IP = "0.0.0.0"   # listen on all interfaces (only one to receive on over the direct cable)
LISTEN_PORT = 5005      # must match PI4_PORT in the sender script

MIDI_CHANNEL = 0         # 0 = channel 1 in MIDI terms

TEMP_CC = 105             # undefined/free CC range is 102-119, safe from conflicts
MIN_TEMP = 15.0           # temperature that maps to CC 0   (tune after watching real readings)
MAX_TEMP = 35.0           # temperature that maps to CC 127 (tune after watching real readings)
TEMP_PORT_NAME = "DHT22 Temperature"

HUMIDITY_CC = 106
MIN_HUMIDITY = 20.0       # humidity that maps to CC 0   (tune after watching real readings)
MAX_HUMIDITY = 80.0       # humidity that maps to CC 127 (tune after watching real readings)
HUMIDITY_PORT_NAME = "DHT22 Humidity"

# ---- OPEN MIDI PORTS ----
# Same approach as the MPU9250 script: create our own virtual MIDI ports
# rather than connecting directly to FluidSynth, so Zynthian's MIDI
# router (and Global Learn) sees each as its own separate input source.
temp_outport = mido.open_output(TEMP_PORT_NAME, virtual=True)
humidity_outport = mido.open_output(HUMIDITY_PORT_NAME, virtual=True)
print(f"Created virtual MIDI ports: '{TEMP_PORT_NAME}' and '{HUMIDITY_PORT_NAME}'")
print("Now connect them to Zynthian's MIDI input using aconnect (see README/instructions).")

# ---- SOCKET SETUP ----
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((LISTEN_IP, LISTEN_PORT))

print(f"Listening for DHT22 data on {LISTEN_IP}:{LISTEN_PORT}. Ctrl+C to stop.")


def parse_line(line):
    """Turn 'Temp:23.4,Humidity:45.6' into (23.4, 45.6). Returns (None, None) on bad input."""
    try:
        parts = dict(item.split(":") for item in line.split(","))
        temperature = float(parts["Temp"])
        humidity = float(parts["Humidity"])
        return temperature, humidity
    except (ValueError, KeyError):
        return None, None


def scale_to_midi(value, in_min, in_max):
    """Map a value to the 0-127 MIDI CC range, clamped at the edges."""
    if value < in_min:
        value = in_min
    if value > in_max:
        value = in_max
    scaled = (value - in_min) / (in_max - in_min) * 127
    return int(scaled)


def send_cc_if_changed(outport, cc_number, cc_value, last_value, label, unit):
    """Send a CC on the given port only if it changed from last time, keeps MIDI traffic clean."""
    if cc_value != last_value:
        msg = mido.Message('control_change',
                            channel=MIDI_CHANNEL,
                            control=cc_number,
                            value=cc_value)
        outport.send(msg)
        print(f"{label}: {cc_value:>3} ({unit})  ->  CC{cc_number}")
    return cc_value


last_temp_cc = -1
last_humidity_cc = -1

try:
    while True:
        data, addr = sock.recvfrom(1024)  # buffer size in bytes, plenty for this payload
        line = data.decode("utf-8").strip()

        temperature, humidity = parse_line(line)

        if temperature is not None:
            temp_cc = scale_to_midi(temperature, MIN_TEMP, MAX_TEMP)
            humidity_cc = scale_to_midi(humidity, MIN_HUMIDITY, MAX_HUMIDITY)

            last_temp_cc = send_cc_if_changed(temp_outport, TEMP_CC, temp_cc, last_temp_cc,
                                               "Temp", f"{temperature:.1f}C")
            last_humidity_cc = send_cc_if_changed(humidity_outport, HUMIDITY_CC, humidity_cc, last_humidity_cc,
                                                   "Humidity", f"{humidity:.1f}%")
        else:
            print(f"Malformed line from {addr[0]}: {line!r}")

except KeyboardInterrupt:
    print("\nStopped.")
    temp_outport.close()
    humidity_outport.close()
    sock.close()
