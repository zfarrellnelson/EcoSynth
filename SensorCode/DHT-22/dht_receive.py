# Runs on the Pi4 (Zynthian). Listens for UDP lines from the Pi3's
# DHT22 sender and splits them into temperature/humidity floats.
import socket

# ---- CONFIGURATION ----
LISTEN_IP = "192.168.2.64"   # listen on all interfaces (or set to the Pi4's ethernet IP)
LISTEN_PORT = 5005      # must match PI4_PORT in the sender script

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


try:
    while True:
        data, addr = sock.recvfrom(1024)  # buffer size in bytes, plenty for this payload
        line = data.decode("utf-8").strip()

        temperature, humidity = parse_line(line)

        if temperature is not None:
            print(f"From {addr[0]}: Temp={temperature:.1f}C  Humidity={humidity:.1f}%")
            # temperature and humidity are now separate floats here -
            # this is the point where you'd map either one to a MIDI CC,
            # same pattern as the MPU9250 -> CC script.
        else:
            print(f"Malformed line from {addr[0]}: {line!r}")

except KeyboardInterrupt:
    print("\nStopped.")
    sock.close()
