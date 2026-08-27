# Problems and Process

## Connecting DHT-22

After connecting the DHT-22 chip, (which manages Humidity and Temperature), I noticed that I was getting Checksum Errors extremely frequently. After doing some research, I learned that Checksum errors are a result of any of the 40 'pings' of the chip getting interrupted, with the 'pings' being the polling of a chip's bit. Since I wasn't actively engaging any other sensors on my raspi4, I knew that a process it was running had to be the culprit of the interruptions. Seeing as the raspi was running the Zynthian engine, I first decided to test that, (as it seemed the most likely culprit), and that ended up being correct. (testpi3b@192.168.1.63)


> Found by testing 'dht_test.py' before and after halting the Zynthian engine with 'sudo systemctl stop zynthian'.

My solution is to use an unused Raspberry Pi 3B that I already own. Is it overkill? Absolutely. Is it better to use it than ordering an Arduino? Also yes. After getting the script working on the Pi 3B, (named 'testpi3b'), I connected it to the DHT-22.

[insert image].

## Talking To Zynthian With Sensors

By far the biggest hurdle with the project was the Sensor -> Zynthian connection. Note that at one point I 


> Found by testing 'dht_test.py' before and after halting the Zynthian engine with 'sudo systemctl stop zynthian'.

My solution is to use an unused Raspberry Pi 3B that I already own. Is it overkill? Absolutely. Is it better to use it than ordering an Arduino? Also yes. After getting the script working on the Pi 3B, (named 'testpi3b'), I connected it to the DHT-22.

[insert image].



[What problem/question inspired the project?]

## Goals

- [ ]
- [ ]
- [ ]
- [ ]

## System Architecture

[Insert system diagram]

[Brief explanation of signal/data flow]

## Hardware

- [ ]
- [ ]
- [ ]
- [ ]

[Link to hardware documentation]

## Sensors

### MPU 9250
**Purpose:** Track Movement and Magnetism  

**Input:** Magnetic Field, Acceleration, Gyroscopic Movement    

**Processing:** Read raw value -> Normalize X Y Z inputs -> map to 0-127  

**MIDI Channels:**   
- Magnetometer: Channel 1, CC 102  
- Accelerometer: Channel 1, CC 103  
- Gyroscope: Channel 1, CC 104  

**Controlled Parameter:**  
- Magnetometer: [ ]  
- Accelerometer: [ ]  
- Gyroscope: [ ] 

### Sensor 2
**Purpose:** [ ]  
**Input:** [ ]  
**Processing:** [ ]  
**MIDI Output:** [ ]  
**Controlled Parameter:** [ ]

[Repeat as necessary]

## Sensor → MIDI Pipeline

[Explain how raw sensor data becomes MIDI]

Using the Mido (Midi Objects For Python) plugin, I'm able to 

```text
Sensor
  ↓
Raw Data
  ↓
Processing
  ↓
Mapping
  ↓
MIDI
  ↓
Zynthian
