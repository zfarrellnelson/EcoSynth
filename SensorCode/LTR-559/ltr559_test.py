import time
import ltr559

sensor = ltr559.LTR559()
time.sleep(0.5)
print(sensor.get_lux(), sensor.get_proximity())
