
import cv2
import numpy as np


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

while cap.isOpened():
	ret, frame = cap.read()

	#Copy left half of videoframe to the blank frame
	history[historyIndex] = frame[:half]
	
	for i in range(histLen, 0, -1):

		y = i * incr
		# print(y)
		currentIndex = (i + offset) % histLen
		# hist = history[i].reshape(half, width, 3)
		frame[y-incr:y] = history[currentIndex, y-incr:y]

	#take n pixel vertival slice/slit
	# slit = frame[half:half+incr]
	
	# #copy slit to split array
	# # scans[-1-incr:-1] = slit
	# scans = np.concatenate([scans, slit])[incr:half+incr]
	# for i in range(half):
	# 	frame[i] = scans[i]	
	
	cv2.imshow("webcam", frame)			

	historyIndex = (historyIndex + 1) % histLen 
	offset += 1		
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

cap.release()
