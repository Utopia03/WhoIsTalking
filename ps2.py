# #!/usr/bin/env python2
# # -*-coding:Latin-1 -*

import commands, time, subprocess, signal, os, pyaudio, sys, wave, multiprocessing.pool
from subprocess import Popen

listDevices = list()
p = pyaudio.PyAudio()

# recover the ouput string from runMic.py and save all commands in "Command" classes
def output_to_command(string):
	numberEntries = string.count("new")
	string = string.split("-")

	for i in xrange(numberEntries):
		command = Command()
		command.mic = string[5 * i + 1]
		command.text = string[5 * i + 2]
		command.time = string[5 * i + 3]
		command.amplitude = string[5 * i + 4]
		commands.append(command)

	for command in commands :
		print(command.mic)
		print(command.text)
		print(command.time)
		print(command.amplitude)

# class which save the text of a command and the time when it is finished
class Command:
	def __init__(self):
		self.mic = 0
		self.text = ""
		self.time = 0
		self.amplitude = 0.00

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
lastCommands = []
commands = []
pool = multiprocessing.pool.ThreadPool(numberDevices)
for dev in listDevices :
	processes.append(lambda dev=dev: subprocess.check_output((["python", "runMic.py", str(dev)])))

outputs = pool.map(lambda x: x(), processes)

for o in outputs :
	output_to_command(o)

	commands.sort(key=lambda x: x.time)

	# permits to determine where the command has been said the higher
	for mainCommand in commands:
		mainCommand.treated = True
		for command in commands:
			if command.treated == False:
				if command.time >= mainCommand.time - 0.5 and command.time <= mainCommand.time + 0.5:
					if mainCommand.amplitude > command.amplitude:
						lastCommands.append(mainCommand)
						command.treated = True
				else:
					lastCommands.append(command)
					command.treated = True

	for command in lastCommands:
		print command.time

p.terminate()