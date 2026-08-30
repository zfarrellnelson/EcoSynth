#T1 stands for Terminal 1. TU stands for a unique terminal for the individual sensed property. There is one TU per sensed property. Z stands for Zynthian (within the Zynthian interface).

---------------------

TU:

python3 mpu_mag_to_midi.py

T1:

sudo jack_connect "a2j:RtMidiOut Client [130] (capture): MPU9250 Magnetometer" "ZynMidiRouter:dev0_in"
sudo jack_connect "a2j:RtMidiOut Client [130] (capture): MPU9250 Magnetometer" "ZynMidiRouter:ctrl_in"

Z:

Learn

TU:

^Z

---------------------

TU:

python3 mpu_accel_to_midi.py

T1:

sudo jack_connect "a2j:RtMidiOut Client [131] (capture): MPU9250 Accelerometer" "ZynMidiRouter:dev0_in"
sudo jack_connect "a2j:RtMidiOut Client [131] (capture): MPU9250 Accelerometer" "ZynMidiRouter:ctrl_in"

Z:

Learn

TU:

^Z

---------------------
