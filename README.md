Python program with voice recognition and audio source geolocalisation.
Spots the microphones connected to PC (or Raspberry), make voice recognition on a few known commands and determine where the source is the higher.

Microphones
-
All the tests had been made with Samson UB1 micros. They are omnidirectional surface microphones, perfects for a domotic use.

Voice recognition
-
System based on CMU Sphinx. Recognize only a few commands chosen before to generate a dictionary. An audio record is also made simultaneously and saved with the corrects date and hour.


How to launch the program
-
The script ps2.py calls runMic.py as many times as the number of micros connected. Finally, the program returns all the commands which had been said and from what micro (so in what room).
The time of record is fixed at 60 seconds. It is necessary to add this program to crontab of your system in order to work every time.
