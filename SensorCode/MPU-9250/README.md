# MAGNETOMETER

channel: 102

sudo jack_connect "a2j:RtMidiOut Client [130] (capture): MPU9250 Magnetometer" "ZynMidiRouter:dev0_in"  
sudo jack_connect "a2j:RtMidiOut Client [130] (capture): MPU9250 Magnetometer" "ZynMidiRouter:ctrl_in"

# ACCELEROMETER

channel: 103

sudo jack_connect "a2j:RtMidiOut Client [131] (capture): MPU9250 Accelerometer" "ZynMidiRouter:dev0_in"  
sudo jack_connect "a2j:RtMidiOut Client [131] (capture): MPU9250 Accelerometer" "ZynMidiRouter:ctrl_in"

# GYROSCOPE

channel: 104

sudo jack_connect "a2j:RtMidiOut Client [132] (capture): MPU9250 Accelerometer" "ZynMidiRouter:dev0_in"  
sudo jack_connect "a2j:RtMidiOut Client [132] (capture): MPU9250 Accelerometer" "ZynMidiRouter:ctrl_in"
