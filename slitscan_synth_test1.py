
import cv2
import numpy as np
import pyaudio
from math import pi

def make_sinewave(frequency, length, sample_rate=44100):
    length = int(length * sample_rate)
    factor = float(frequency) * (pi * 2) / sample_rate
    waveform = np.sin(np.arange(length) * factor)
    return waveform


cap = cv2.VideoCapture(0)
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paFloat32, channels=1, rate=44100, output=1,)

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(cap.get(cv2.CAP_PROP_FPS))
length = 1/fps

cap.set(cv2.CAP_PROP_FPS, 30)

incr = 3
half = int(height/2)
histLen = int(half/incr)
index = half
scans = np.zeros([half,width,3])
history = np.zeros([histLen, half, width, 3])
historyIndex = 0
offset = 0

print(length)

while cap.isOpened():
	ret, frame = cap.read()

	#Copy left half of videoframe to the blank frame
	history[historyIndex] = frame[:half]
	
	for i in range(histLen, 0, -1): #count backwards from end of history-array

		y = i * incr
		# print(y)
		currentIndex = (i + offset) % histLen
		# print(currentIndex)
		frame[y-incr:y] = history[currentIndex, half-incr:half]	

	# soundbar = cv2.cvtColor(frame[half-1:half], cv2.COLOR_BGR2GRAY)[0]
	soundbar = cv2.cvtColor(frame[half-1:half], cv2.COLOR_BGR2GRAY).sum()
	soundbar = soundbar/10
	# for i in soundbar:
	wave = make_sinewave(soundbar, length)
	stream.write(wave.astype(np.float32).tostring())


	cv2.imshow("webcam", frame)			

	historyIndex = (historyIndex + 1) % histLen 
	offset += 1	
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

cap.release()
stream.stop_stream()
stream.close()