# WhoIsTalking

Python program with voice recognition and audio source geolocation.
Spots the microphones connected to PC (or Raspberry), make voice recognition on a few known commands and determine where the source is the higher.

## Microphones
All the tests had been made with Samson UB1 micros. They are omnidirectional surface microphones, perfect for home automation use.

## Voice recognition
The voice recognition system is based on CMU Sphinx and it recognizes only a few commands previously chosed and generated in a dictionary. An audio record is also made simultaneously and saved with the correct date and hour.

## How to launch the program
The script ps2.py calls runMic.py as many times as the number of micros connected. Finally, the program returns all the commands which had been said and from which micro (so in which room).
The record's duration is fixed to 60 seconds. 
To launch it repeatedly, you need to add this program to the crontab of your system.
