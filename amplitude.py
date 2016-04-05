#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

from scipy.io.wavfile import read

# read audio samples
input_data = read("demo.wav")
audio1 = input_data[1]

fs = 8000 # fréquence d'échantillonnage
t = 10 # durée
nbSamples = t * fs

mean1 = 0
mean1 = float(mean1)
for t in range(nbSamples):
    mean1 = mean1 + abs(audio1[t])
mean1 = float(mean1 / nbSamples)
print(mean1)