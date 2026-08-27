# use pin 7
import time
import board
import adafruit_dht

# if switching pins, change board.D4 to the applicable board
dht_device = adafruit_dht.DHT22(board.D4)

while True:
    try:
        temperature = dht_device.temperature
        humidity = dht_device.humidity
        print(f"Temp: {temperature:.1f}°C  Humidity: {humidity:.1f}%")
    except RuntimeError as e:
        # try again if error
        print(f"Reading error: {e.args[0]}")
    # if acting weird at 3, change to 5  
    time.sleep(5)
