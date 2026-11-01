# Problems and Process

## Connecting DHT-22

After connecting the DHT-22 chip, (which manages Humidity and Temperature), I noticed that I was getting Checksum Errors extremely frequently. After doing some research, I learned that Checksum errors are a result of any of the 40 'pings' of the chip getting interrupted, with the 'pings' being the polling of a chip's bit. Since I wasn't actively engaging any other sensors on my raspi4, I knew that a process it was running had to be the culprit of the interruptions. Seeing as the raspi was running the Zynthian engine, I first decided to test that, (as it seemed the most likely culprit), and that ended up being correct. 

> Found by testing 'dht_test.py' before and after halting the Zynthian engine with 'sudo systemctl stop zynthian'.

My solution is to implement an unused Raspberry Pi 3B that I already own. Is it overkill? Absolutely. Is it better to use it than ordering an Arduino? Also absolutely. After getting the script working on the Pi 3B, (named 'testpi3b'), I connected it to the DHT-22. I connected the Raspi3B and Raspi4, (shortened to pi3 and pi4 respectively), and allocated them static IP addresses (192.168.2.63/64). After using Claude to generate a basic version of communication for the two pis as a test, (dht_test.py), I adapted the MPU-9250 code to allow the pi4 to send midi based on the received humidity and temperature data from the pi3. I later split the code into ___ and ____, allowing the pausing of one script to midi learn the other.

[insert image].<img width="2557" height="1386" alt="image" src="https://github.com/user-attachments/assets/d34783f6-8eaa-407c-a2ce-7632951d3ab7" />
