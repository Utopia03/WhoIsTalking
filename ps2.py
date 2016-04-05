# #!/usr/bin/env python2
# # -*-coding:Latin-1 -*

import commands, time, subprocess, signal, os, pyaudio, sys, wave
from subprocess import Popen

listDevices = list()
p = pyaudio.PyAudio()

# détecte les index des micros connectés
max_apis = p.get_host_api_count()
max_devs = p.get_device_count()

for i in range(max_devs):
	devinfo = p.get_device_info_by_index(i)

	# récupère les indices des micros Samson connectés
	for k in list(devinfo.items()):
		name, value = k
		if name == 'name' and 'Samson' in value :
			listDevices.append(i)

# pour chacun des micros
numberDevices = len(listDevices)
print(numberDevices)

for i in listDevices:
	print(i)

dic = {}
pDic = {}
var = 1
if (numberDevices > 1) :
	for dev in listDevices :
		if var == 1 :
	 		dic["string{0}".format(dev)] = ["python", "runMic.py", str(dev)]
			pDic["string{0}".format(dev)] = subprocess.Popen(dic["string{0}".format(dev)])
			var = 2
		else :
			dic["string{0}".format(dev)] = ["python", "runMic1.py", str(dev)]
			pDic["string{0}".format(dev)] = subprocess.Popen(dic["string{0}".format(dev)])
elif (numberDevices == 1) :
 	dev0 = ["python", "runMic.py", str(listDevices[0])]
 	pDev0 = subprocess.Popen(dev0)

# dev0 = ["python", "runMic.py", "3"]
# dev1 = ["python", "runMic1.py", "4"]
# pDev0 = subprocess.Popen(dev0)
# pDev1 = subprocess.Popen(dev1)

p.terminate()