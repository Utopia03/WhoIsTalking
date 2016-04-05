import pyaudio, wave, struct, math
import matplotlib.pyplot as plt
import numpy as np

SHORT_NORMALIZE = (1.0 / 32768.0)

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

    return math.sqrt( sum_squares / count )

CHUNK = 4096
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 22050
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK,
                input_device_index = 3)

print("* recording")

frames = []

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    amplitude = get_rms(data)
    frames.append(amplitude) # 2 bytes(16 bits) per channel

print("* done recording")

stream.stop_stream()
stream.close()
p.terminate()

for amplitude in frames:
    print(amplitude)

t = np.linspace(0,len(frames),len(frames))
plt.plot(t,frames)  # on utilise la fonction sinus de Numpy
plt.ylabel('t')
plt.xlabel('amplitude')
plt.show()
