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
		command.mic = int(string[5 * i + 1])
		command.text = string[5 * i + 2]
		command.time = float(string[5 * i + 3])
		command.amplitude = float(string[5 * i + 4])
		commands.append(command)

# class which save the text of a command and the time when it is finished
class Command:
	def __init__(self):
		self.mic = 0
		self.text = ""
		self.time = 0
		self.amplitude = 0.00
		self.treated = False

# create the connection with MongoLab
connection = pymongo.MongoClient('ds059185.mlab.com', 59185)

# get the database
db = connection['audiomanager_db']
db.authenticate('thibault', 'ISEN')

# detect the indices of the connected micros
max_devs = p.get_device_count()

for i in range(max_devs):
	devinfo = p.get_device_info_by_index(i)

	# récupère les indices des micros Samson connectés
	for k in list(devinfo.items()):
		name, value = k
		if name == 'name' and 'Samson' in value :
			listDevices.append(i)

numberDevices = len(listDevices)

index1 = 0
index2 = 0

if (numberDevices > 0) :
	index1 = listDevices(0)
if (numberDevices > 1) :
	index2 = listDevices(1)

result = db.micros.update_one(
    {"_id": "Micro 1"},
    {
        "$set": {
            "index": index1
        }
    }
)

result = db.micros.update_one(
    {"_id": "Micro 2"},
    {
        "$set": {
            "index": index2
        }
    }
)

processes = []
lastCommands = []
commands = []
pool = multiprocessing.pool.ThreadPool(numberDevices)
for dev in listDevices :
	processes.append(lambda dev=dev: subprocess.check_output((["python", "runMic.py", str(dev)])))

print("processes : " + str(len(processes)))
outputs = pool.map(lambda x: x(), processes)

for o in outputs :
	print(o)
	output_to_command(o)

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

# create a history document
micros = db.micros.find()

for command in lastCommands:
	print(command.text + " has been said at " + str(command.time) + " seconds" + " in micro " + str(command.mic))
	for micro in micros:
	   if micro['index'] == command.mic :
		result = db.history.insert_one(
	           {
		      "username": "Agathe",
		      "location" : micro['location'],
		      "request" : command.text
	           }
		)

# close the connection to MongoDB
connection.close()