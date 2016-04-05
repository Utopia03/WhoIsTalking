#!/usr/bin/env python2
# -*-coding:Latin-1 -*

from pocketsphinx import *
from threading import Thread
import pyaudio, sys, wave, time, commands, os

hmm = '/usr/local/share/pocketsphinx/model/en-us/en-us'
dic = '/usr/local/share/pocketsphinx/model/en-us/6892.dic'
lm = '/usr/local/share/pocketsphinx/model/en-us/6892.lm'

config = Decoder.default_config()
config.set_string('-hmm', hmm)
config.set_string('-lm', lm)
config.set_string('-dict', dic)
config.set_string('-logfn', '/dev/null')

# mots clés de début et de fin
start = "OPEN"
end = "LIGHT"

list = [] # liste d'objets de type "Command"

index = 0
delay = 0

# classe qui stocke le texte d'une commande et le temps où elle a fini d'être dite
class Command:
	def __init__(self):
		self.text = ""
		self.time = 0

# classe qui permet d'exécuter un second Thread qui va enregistrer en même temps
class Record(Thread):
	def __init__(self, device):
		super(Record, self).__init__()
		self.device = device
	def run(self):
		# permet d'enregistrer en spécifiant le / les bons micros, et enregistre un fichier à la bonne date et heure, en spécifiant le numéro du micro
		u = commands.getoutput('arecord -D plughw:' + str(self.device) + ',0 -f cd -t wav -d 10 --use-strftime %Y/%m/%d/mic' + str(self.device) + '-listen-%H-%M-%v.wav')

class ActionsPerMic(Thread):
	def __init__(self, device):
		super(ActionsPerMic, self).__init__()
		self.device = device

	def run(self):
		global delay
		global index
		decoder = Decoder(config)
		p = pyaudio.PyAudio()
		stream = p.open(format=pyaudio.paInt16, channels=1, rate=22050, input=True, frames_per_buffer=4096, input_device_index = int(self.device))
		stream.start_stream()
		decoder.start_utt()

		# rec = Record(self.device)
		# rec.start()

		# on fait l'action que pendant 60 secondes soit une minute
		print "temps " + str(time.time())
		while delay < 15 :
			buf = stream.read(4096)
			if buf:
				decoder.process_raw(buf, False, False)
				try:
					if decoder.hyp().hypstr != '':
						print "Hearing : ", decoder.hyp().hypstr
						remaining = decoder.hyp().hypstr[index:]
						delay = time.time() - t0
						# print "index : ", index
						# print "remaining : ", remaining
						if start in remaining:
							if end in remaining:
								command = Command()
								command.name = remaining.split(start)[1].split(end)[0]
								command.time = time.time() - t0
								print "Between " + start + " and : " + end, command.name
								list.append(command)
								index = len(decoder.hyp().hypstr)
				except AttributeError:
					pass
			else:
				break

		decoder.end_utt()

		print 'Time out'
		for command in list :
			print command.name, " at ", command.time, " seconds"

		# rec.join()

# on démarre le timer
t0 = time.time()

# pour un micro branché au Raspberry Pi
mic = ActionsPerMic(sys.argv[1])
mic.start()
mic.join()