import time
import cv2
import dlib
import pyttsx3
from scipy.spatial import distance
import serial

#ser = serial.Serial('COM7', 9600)  # Change the port and baud rate as necessary

#pyttsx3 is used for audio generation
audiogen = pyttsx3.init()

# SETTING UP OF CAMERA TO 0
cap = cv2.VideoCapture(0)

start_time = None

# FACE DETECTION OR MAPPING THE FACE TO
# GET THE Eye AND EYES DETECTED
face_detector = dlib.get_frontal_face_detector()


# PREDECTING THE LANDMARKS ON FACE )
dlib_facelandmark = dlib.shape_predictor(
	"shape_predictor_68_face_landmarks.dat")

# FUNCTION CALCULATING THE ASPECT RATIO FOR
# THE Eye BY USING EUCLIDEAN DISTANCE FUNCTION
def Detect_Eye(eye):
	poi_A = distance.euclidean(eye[1], eye[5])
	poi_B = distance.euclidean(eye[2], eye[4])
	poi_C = distance.euclidean(eye[0], eye[3])
	aspect_ratio_Eye = (poi_A+poi_B)/(2*poi_C)
	return aspect_ratio_Eye
def detect_mouth(mouth):
	poi_A = distance.euclidean(mouth[2], mouth[10])
	poi_B = distance.euclidean(mouth[4], mouth[8])
	poi_C = distance.euclidean(mouth[0], mouth[6])
	aspect_ratio_mouth = (poi_A + poi_B) / (2 * poi_C)
	return aspect_ratio_mouth


# MAIN LOOP IT WILL RUN ALL THE UNLESS AND
# UNTIL THE PROGRAM IS BEING KILLED BY THE USER
while True:
	null, frame = cap.read()
	gray_scale = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

	faces = face_detector(gray_scale)

	for face in faces:
		face_landmarks = dlib_facelandmark(gray_scale, face)
		leftEye = []
		rightEye = []
		mouth =[]

		# THESE ARE THE POINTS ALLOCATION FOR THE
		# LEFT EYES IN .DAT FILE THAT ARE FROM 42 TO 47
		for n in range(42, 48):
			x = face_landmarks.part(n).x
			y = face_landmarks.part(n).y
			rightEye.append((x, y))
			next_point = n+1
			if n == 47:
				next_point = 42
			x2 = face_landmarks.part(next_point).x
			y2 = face_landmarks.part(next_point).y
			cv2.line(frame, (x, y), (x2, y2), (0, 255, 0), 1)

		# THESE ARE THE POINTS ALLOCATION FOR THE
		# RIGHT EYES IN .DAT FILE THAT ARE FROM 36 TO 41
		for n in range(36, 42):
			x = face_landmarks.part(n).x
			y = face_landmarks.part(n).y
			leftEye.append((x, y))
			next_point = n+1
			if n == 41:
				next_point = 36
			x2 = face_landmarks.part(next_point).x
			y2 = face_landmarks.part(next_point).y
			cv2.line(frame, (x, y), (x2, y2), (255, 255, 0), 1)

		for n in range(48, 68):
			x = face_landmarks.part(n).x
			y = face_landmarks.part(n).y
			mouth.append((x, y))
			next_point = n + 1
			if n == 67:
				next_point = 48
			x2 = face_landmarks.part(next_point).x
			y2 = face_landmarks.part(next_point).y
			cv2.line(frame, (x, y), (x2, y2), (0, 0, 255), 1)

		# CALCULATING THE ASPECT RATIO FOR LEFT
		# AND RIGHT EYE
		right_Eye = Detect_Eye(rightEye)
		left_Eye = Detect_Eye(leftEye)
		Eye_Rat = (left_Eye+right_Eye)/2
		Eye_Rat = round(Eye_Rat, 2)
		mouth_aspect_ratio = detect_mouth(mouth)

		 #check if average is less than 0,20
		if Eye_Rat < 0.25:
			if start_time is None:
				start_time = time.time()
			elif time.time() - start_time >= 1.25:
				cv2.putText(frame, "DROWSINESS DETECTED", (50, 100),
						cv2.FONT_HERSHEY_PLAIN, 2, (21, 56, 210), 3)
				# audio output
				audiogen.say("please... wakeup")
				audiogen.runAndWait()
				if time.time() - start_time >= 8:
					 #Send data to the Arduino
					data = 'off'
					data = data.strip()
					#ser.write(data.encode())

					#Close the serial connection
					#ser.close()


		elif mouth_aspect_ratio > 0.5:
			if start_time is None:
				start_time = time.time()
			elif time.time() - start_time >= 1.25:
				cv2.putText(frame, "YAWNING DETECTED", (50, 100), cv2.FONT_HERSHEY_PLAIN, 2, (21, 56, 210), 3)
				# audio output
				audiogen.say("Please stop yawning")
				audiogen.runAndWait()


		else:
			start_time = None

	cv2.imshow("Drowsiness Detector", frame)
	key = cv2.waitKey(9)
	if key == 20:
		break
cap.release()
cv2.destroyAllWindows()
