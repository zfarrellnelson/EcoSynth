# Runs on the Pi3. Reads the DHT22 (data pin on physical pin 7 / GPIO4)
# and sends each reading as a line of text over UDP to the Pi4.
import time
import socket
import board
import adafruit_dht

# ---- CONFIGURATION ----
PI4_IP = "192.168.2.64"   # Pi4's static IP (direct Ethernet link)
PI4_PORT = 5005           # make sure it matches the receiver, port num itself is arbitrary
SEND_INTERVAL = 2         # seconds between reads (bump if I get checksummed)

# ---- SENSOR + SOCKET SETUP ----
# if switching pins, change board.D4 to the new pin
dht_device = adafruit_dht.DHT22(board.D4)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP, no connection to maintain

print(f"Reading DHT22 on pin 7, sending to {PI4_IP}:{PI4_PORT}. Ctrl+C to stop.")

try:
    while True:
        try:
            temperature = dht_device.temperature
            humidity = dht_device.humidity

            if temperature is not None and humidity is not None:
                line = f"Temp:{temperature:.1f},Humidity:{humidity:.1f}"
                sock.sendto(line.encode("utf-8"), (PI4_IP, PI4_PORT))
                print(f"Sent -> {line}")
            else:
                print("Sensor returned None, skipping this cycle.")

        except RuntimeError as e:
            # DHT22 read glitches are gonna happen, retry when it doesn't work
            print(f"Reading error: {e.args[0]}")

        time.sleep(SEND_INTERVAL)

except KeyboardInterrupt:
    print("\nStopped.")
    dht_device.exit()
    sock.close()
