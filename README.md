# EcoSynth

> An environmentally-influenced synthesizer using the zynthian engine and sensor-dependent effects.

## Project Overview

**Project Type:** Interactive Hardware / Music Technology Project  
**Timeline:** [ ]   
**Status:** In-Development

## Concept

[What is EcoSynth?]

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
