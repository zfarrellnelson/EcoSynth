import ltr559
sensor = ltr559.LTR559()
print(sensor.get_lux(), sensor.get_proximity())
