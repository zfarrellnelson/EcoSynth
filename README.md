# EcoSynth

> An Environmentally-Influenced Synthesizer using the Zynthian Engine and Sensor-Dependent Effects.

## Project Overview

**Project Type:** Interactive Hardware / Music Technology Project  
**Timeline:** [ ]   
**Status:** In-Development

## Concept

[What is EcoSynth?]

EcoSynth stands for Ecological Synthesizer; As Ecology is the relation of an organism to its environment, EcoSynth simulates a musician's connection to their surroundings. Running the Zynthian frontend, EcoSynth uses the outputs of various sensors to receive an environmental influence, such as Magnetic Fields, Ambient Light, Humidity, and Temperature. EcoSynth also receives data from physical changes in the musician/instruments position, such as Gyroscopic Movement, Acceleration, and Proximity. By using these inputs, EcoSynth can output a sound that is truly unique to a person's surroundings, representing their position and relation to the world around them.


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
