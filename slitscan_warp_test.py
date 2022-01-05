
import cv2
import numpy as np
import Nsound as ns

cap = cv2.VideoCapture(0)

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(cap.get(cv2.CAP_PROP_FPS))

cap.set(cv2.CAP_PROP_FPS, 30)

incr = 3
half = int(height/2)
histLen = int(half/incr)
index = half
scans = np.zeros([half,width,3])
history = np.zeros([histLen, half, width, 3])
historyIndex = 0
offset = 0

ns.use("portaudio")
audioBuffer = ns.AudioStream(44100.0, 2)

audioBuffer >> ns.AudioPlayback(44100.0, 2, 16)

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

	soundbar = cv2.cvtColor(frame[half-1:half], cv2.COLOR_BGR2GRAY)[0]
	
	audioBuffer << soundbar

	

	cv2.imshow("webcam", frame)			

	historyIndex = (historyIndex + 1) % histLen 
	offset += 2		
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

cap.release()
