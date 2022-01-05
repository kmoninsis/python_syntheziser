import pyaudio
from math import pi
import numpy as np
from oscillator import *

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paFloat32, channels=1, rate=44100, output=1,)
notes_dict = {}

width = 640

sampleLength = 44100

osc_dict = [SineOscillator(freq=0) for i in range(width)]

soundbar = np.linspace(0,25500, num=width)
print(type(osc_dict[0]))
for val, osc in enumerate(osc_dict):
    freq = soundbar[val]
    osc.freq(freq)
    # print(freq)

print(type(osc_dict[0]))
next(osc)

gen = WaveAdder( [osc for osc in osc_dict])

# print(testarray)
iter(gen)   
wave = np.array([next(gen) for _ in range(sampleLength)])


# print(wave, type(wave), wave.shape)
stream.write(np.float32(wave).tobytes())


stream.stop_stream()
stream.close()