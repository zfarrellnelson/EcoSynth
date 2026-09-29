from mpu9250_jmdev.registers import *
from mpu9250_jmdev.mpu_9250 import MPU9250
import plotext as plt
from collections import deque
import time
import math

mpu = MPU9250(
    address_ak=AK8963_ADDRESS,
    address_mpu_master=MPU9050_ADDRESS_68,
    address_mpu_slave=None,
    bus=1,
    gfs=GFS_1000,
    afs=AFS_8G,
    mfs=AK8963_BIT_16,
    mode=AK8963_MODE_C100HZ
)
mpu.configure()

WINDOW = 30  # fewer points = smaller/faster redraw, less flicker

mag_vals = deque(maxlen=WINDOW)

plt.plotsize(80, 20)  # fixed size keeps terminal from reflowing/jumping

print("Reading MPU9250... Ctrl+C to stop")
time.sleep(1)

try:
    while True:
        mag = mpu.readMagnetometerMaster()
        magnitude = math.sqrt(mag[0]**2 + mag[1]**2 + mag[2]**2)
        mag_vals.append(magnitude)

        plt.clt()  # clear terminal in-place instead of full clf scroll
        plt.cld()  # clear previous data
        plt.plot(list(mag_vals), label="Mag Magnitude")

        plt.ylim(0, 150)  # magnitude is always positive
        plt.title("MPU9250 Live Magnetometer Magnitude")
        plt.xlabel("Sample")
        plt.ylabel("uT")

        plt.show()

        time.sleep(0.25)  # slower refresh = less visible jumpiness

except KeyboardInterrupt:
    print("\nStopped.")
