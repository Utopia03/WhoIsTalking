# #!/usr/bin/env python2
# # -*-coding:Latin-1 -*

import subprocess, pyaudio, multiprocessing.pool
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

numberDevices = len(listDevices)

processes = []

pool = multiprocessing.pool.ThreadPool(numberDevices)
for dev in listDevices :
	processes.append(lambda dev=dev: subprocess.check_output((["python", "runMic.py", str(dev)])))

outputs = pool.map(lambda x: x(), processes)

for o in outputs :
	print o

p.terminate()