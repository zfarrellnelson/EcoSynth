# Runs on the Pi3. Reads the DHT22 (data pin on physical pin 7 / GPIO4)
# and sends each reading as a line of text over UDP to the Pi4.
import time
import socket
import board
import adafruit_dht

# ---- CONFIGURATION ----
PI4_IP = "192.168.2.64"   # Pi4's static IP (direct Ethernet link)
PI4_PORT = 5005           # arbitrary port, just make sure it matches the receiver
SEND_INTERVAL = 2         # seconds between reads (bump to 5-10 if you see checksum errors)

# ---- SENSOR + SOCKET SETUP ----
# if switching pins, change board.D4 to the applicable board pin
dht_device = adafruit_dht.DHT22(board.D4)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP, no connection to maintain

print(f"Reading DHT22 on pin 7, sending to {PI4_IP}:{PI4_PORT}. Ctrl+C to stop.")

try:
    while True:
        try:
            temperature = dht_device.temperature
            humidity = dht_device.humidity

            if temperature is not None and humidity is not None:
                # Keep this format simple and stable - the Pi4 side parses it directly.
                line = f"Temp:{temperature:.1f},Humidity:{humidity:.1f}"
                sock.sendto(line.encode("utf-8"), (PI4_IP, PI4_PORT))
                print(f"Sent -> {line}")
            else:
                print("Sensor returned None, skipping this cycle.")

        except RuntimeError as e:
            # DHT22 read glitches are normal, just retry next cycle
            print(f"Reading error: {e.args[0]}")

        time.sleep(SEND_INTERVAL)

except KeyboardInterrupt:
    print("\nStopped.")
    dht_device.exit()
    sock.close()
