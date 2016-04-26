# #!/usr/bin/env python2
# # -*-coding:Latin-1 -*

import commands, subprocess, pyaudio, multiprocessing.pool, pymongo
from pymongo import MongoClient

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
		self.treated = False

# detect the indices of connected mics
max_devs = p.get_device_count()

for i in range(max_devs):
	devinfo = p.get_device_info_by_index(i)

	# recover the indices of Samson connected mics
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

for command in commands:
	print(command.text + " has been said at " + str(command.time) + " seconds" + " in micro " + str(command.mic))

commands.sort(key=lambda x: x.time)

# permits to determine where the command has been said the higher
for i in range(0, len(commands)):
	for j in range(i + 1, len(commands)):
		if commands[j].time >= commands[i].time - 0.5 and commands[j].time <= commands[i].time + 0.5:
			if commands[i].amplitude > commands[j].amplitude:
				lastCommands.append(commands[i])
			if commands[j].amplitude >= commands[i].amplitude:
				lastCommands.append(commands[j])
			commands[i].treated = True
			commands[j].treated = True
		if commands[i].treated == False:
			lastCommands.append(commands[i])
			commands[i].treated = True

for command in lastCommands:
	print(command.text + " has been said at " + str(command.time) + " seconds" + " in micro " + str(command.mic))

p.terminate()

# create the connection with MongoLab
connection = pymongo.MongoClient('ds059185.mlab.com', 59185)

# get the database
db = connection['audiomanager_db']
db.authenticate('admin', 'admin')

# create a history document
for command in lastCommands:
	print(command.text + " has been said at " + str(command.time) + " seconds" + " in micro " + str(command.mic))
	result = db.history.insert_one(
	   {
		"username": "Agathe",
		"micro" : command.mic,
		"text" : command.text
	   }
	)

# close the connection to MongoDB
connection.close()