#!/usr/bin/env python2
# -*-coding:Latin-1 -*

from pocketsphinx import *
from threading import Thread
import pyaudio, sys, wave, time, commands, os, struct, math
import matplotlib.pyplot as plt
import numpy as np

hmm = '/usr/local/share/pocketsphinx/model/en-us/en-us'
dic = '/usr/local/share/pocketsphinx/model/en-us/6892.dic'
lm = '/usr/local/share/pocketsphinx/model/en-us/6892.lm'

config = Decoder.default_config()
config.set_string('-hmm', hmm)
config.set_string('-lm', lm)
config.set_string('-dict', dic)
config.set_string('-logfn', '/dev/null')

# key words for start and end
start = "OPEN"
end = "LIGHT"

SHORT_NORMALIZE = (1.0 / 32768.0)

list = [] # list of objects of type "Command"
frames = []
framesConverted = []

index = 0
delay = 0

CHUNK = 2048
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 11025
RECORD_SECONDS = 15
WAVE_OUTPUT_FILENAME = time.strftime('%Y-%m-%d-mic -listen-%H-%M-%S.wav')

def get_rms(block):
    count = len(block) / 2
    format = "%dh" % (count)
    shorts = struct.unpack(format, block)

    # iterate over the block.
    sum_squares = 0.0
    for sample in shorts:
        # sample is a signed short in +/- 32768.
        # normalize it to 1.0
        n = sample * SHORT_NORMALIZE
        sum_squares += n * n

    return math.sqrt(sum_squares / count)

# class which save the text of a command and the time when it is finished
class Command:
	def __init__(self):
		self.text = ""
		self.time = 0
		self.amplitude = 0.00

class ActionsPerMic(Thread):
	def __init__(self, device):
		super(ActionsPerMic, self).__init__()
		self.device = device

	def run(self):
		global delay
		global index
		decoder = Decoder(config)
		p = pyaudio.PyAudio()

		stream = p.open(format = FORMAT,
		                channels = CHANNELS,
		                rate = RATE,
		                input = True,
		                frames_per_buffer = CHUNK,
		                input_device_index = int(self.device))

		stream.start_stream()
		decoder.start_utt()

		# we launch the program only for 60 seconds i.e. one minute
		while delay < RECORD_SECONDS :
			# calculation of amplitude
			data = stream.read(CHUNK)
			frames.append(data)
			amplitude = get_rms(data)
			framesConverted.append(amplitude)
			print(amplitude)
			if data:
				decoder.process_raw(data, False, False)
				try:
					if decoder.hyp().hypstr != '':
						# print "Hearing : ", decoder.hyp().hypstr
						remaining = decoder.hyp().hypstr[index:]
						delay = time.time() - t0
						if start in remaining:
							if end in remaining:
								command = Command()
								command.name = remaining.split(start)[1].split(end)[0]
								command.time = time.time() - t0
								# print "Between " + start + " and " + end + " : ", command.name
								list.append(command)
								index = len(decoder.hyp().hypstr)
				except AttributeError:
					pass
			else:
				break

		decoder.end_utt()

		for command in list :
			print command.name, " at ", command.time, " seconds"

		#  record a .wav file
		wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
		wf.setnchannels(CHANNELS)
		wf.setsampwidth(p.get_sample_size(FORMAT))
		wf.setframerate(RATE)
		wf.writeframes(b''.join(frames))
		wf.close()

		p.terminate()

		# plot a figure with amplitude over time
		t = np.linspace(0, len(framesConverted), len(framesConverted))
		plt.plot(t, framesConverted)
		plt.ylabel('amplitude')
		plt.xlabel('time')
		plt.show()

# we start the timer
t0 = time.time()

# for each mic connected
mic = ActionsPerMic(sys.argv[1])
mic.start()
mic.join()