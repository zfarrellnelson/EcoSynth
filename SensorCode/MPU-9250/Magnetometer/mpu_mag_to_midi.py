from mpu9250_jmdev.registers import *
from mpu9250_jmdev.mpu_9250 import MPU9250
import mido
import time
import math

# ---- CONFIGURATION ----
CC_NUMBER = 102       # undefined/free CC range is 102-119, safe from conflicts
MIDI_CHANNEL = 0      # 0 = channel 1 in MIDI terms
MIN_MAG = 20          # magnitude value that maps to CC 0  
MAX_MAG = 80          # magnitude value that maps to CC 127 
SEND_INTERVAL = 0.05  # seconds between MIDI sends (20 times/sec)

# ---- LIST AVAILABLE PORTS (uncomment to check) ----
# print(mido.get_output_names())

# ---- OPEN MIDI PORT ----
# Create my own virtual MIDI port rather than connecting directly to
# FluidSynth. This lets Zynthian's MIDI router (and Global Learn) see
# the port as a proper MIDI input source, the same way a hardware controller
# would show up.
PORT_NAME = "MPU9250 Magnetometer"
outport = mido.open_output(PORT_NAME, virtual=True)
print(f"Created virtual MIDI port: {PORT_NAME}")
print("Now connect it to Zynthian's MIDI input using aconnect (see README/instructions).")

# ---- SENSOR SETUP ----
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


def scale_to_midi(value, in_min, in_max):
    """Map a value to the 0-127 MIDI CC range, clamped at the edges."""
    if value < in_min:
        value = in_min
    if value > in_max:
        value = in_max
    scaled = (value - in_min) / (in_max - in_min) * 127
    return int(scaled)


print("Streaming magnetometer -> MIDI CC. Ctrl+C to stop.")

last_cc_value = -1  # track last sent value to avoid flooding identical CCs

try:
    while True:
        mag = mpu.readMagnetometerMaster()
        magnitude = math.sqrt(mag[0]**2 + mag[1]**2 + mag[2]**2)

        cc_value = scale_to_midi(magnitude, MIN_MAG, MAX_MAG)

        # only send if the value actually changed, keeps MIDI traffic clean
        if cc_value != last_cc_value:
            msg = mido.Message('control_change',
                                channel=MIDI_CHANNEL,
                                control=CC_NUMBER,
                                value=cc_value)
            outport.send(msg)
            print(f"Magnitude: {magnitude:6.2f}  ->  CC{CC_NUMBER}: {cc_value}")
            last_cc_value = cc_value

        time.sleep(SEND_INTERVAL)

except KeyboardInterrupt:
    print("\nStopped.")
    outport.close()
