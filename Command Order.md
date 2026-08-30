#T1 stands for Terminal 1. TU stands for a unique terminal for the individual sensed property. There is one TU per sensed property. Z stands for Zynthian (within the Zynthian interface).

VIEW ALL CHANNELS:
sudo jack_lsp -A | grep -i DHT22

---------------------

# MPU-9250

TU:

python3 mpu_mag_to_midi.py

T1:

sudo jack_connect "a2j:RtMidiOut Client [130] (capture): MPU9250 Magnetometer" "ZynMidiRouter:dev0_in"  
sudo jack_connect "a2j:RtMidiOut Client [130] (capture): MPU9250 Magnetometer" "ZynMidiRouter:ctrl_in"  

Z:

Learn

TU:

^Z

(at end, use fg to unpause)

#

TU:

python3 mpu_accel_to_midi.py

T1:

sudo jack_connect "a2j:RtMidiOut Client [131] (capture): MPU9250 Accelerometer" "ZynMidiRouter:dev0_in"  
sudo jack_connect "a2j:RtMidiOut Client [131] (capture): MPU9250 Accelerometer" "ZynMidiRouter:ctrl_in"  

Z:

Learn

TU:

^Z

(at end, use fg to unpause)

#

TU:

python3 mpu_gyro_to_midi.py

T1:

sudo jack_connect "a2j:RtMidiOut Client [132] (capture): MPU9250 Gyroscope" "ZynMidiRouter:dev0_in"  
sudo jack_connect "a2j:RtMidiOut Client [132] (capture): MPU9250 Gyroscope" "ZynMidiRouter:ctrl_in"  

Z:

Learn

TU:

^Z

(at end, use fg to unpause)

#

# DHT-22

Now using Pi3 and Pi4:

PI3_U:

python3 dht_send_v2.py

PI4_U:

dht_temp_to_midi.py


