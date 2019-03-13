import face_recognition
import cv2
#NEEDED FOR VLC STREAM import sys 

cap = cv2.VideoCapture(0)

sam_image = face_recognition.load_image_file("images/sam.jpg")
sam_face_encoding = face_recognition.face_encodings(sam_image)[0]

samo_image = face_recognition.load_image_file("images/Sam O.jpg")
samo_face_encoding = face_recognition.face_encodings(samo_image)[0]



known_face_encoding = [
	sam_face_encoding,
	samo_face_encoding

]

known_face_names = [
	"Sam", 
	"Sam O Heron"
]

face_locations = []
face_encodings = []
face_names = []
process_this_frame = 0

while True:
	ret, frame = cap.read()
	small_frame = cv2.resize(frame, (0,0), fx = 0.25, fy = 0.25)

	#converts brg file format to RGB for face recog library
	rgb_small_frame = small_frame[:,:,::-1]

	if (process_this_frame == 5):
		face_locations = face_recognition.face_locations(rgb_small_frame)
		print(face_locations)
		face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

		face_names = []

		for face_encoding in face_encodings:
			matches = face_recognition.compare_faces(known_face_encoding, face_encoding)
			name = "Unknown"
			if True in matches:
				first_match_index = matches.index(True)
				name = known_face_names[first_match_index]
			face_names.append(name)
		process_this_frame = 0
	process_this_frame += 1

	for (top, right, bottom, left), name in zip(face_locations, face_names):
		top*=4
		right*=4
		bottom*=4
		left*=4

		cv2.rectangle(frame, (left, top), (right, bottom), (57, 255, 20), 1)
		cv2.rectangle(frame, (left, bottom-35), (right, bottom), (57, 255, 20), cv2.FILLED)
		font = cv2.FONT_HERSHEY_SIMPLEX
		cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255,255,255), 1)
	cv2.imshow('Video', frame)
	#TEST FOR RTP STREAM TO VLC
	#sys.stdout.write(frame.tostring())

	if cv2.waitKey(1) & 0xff == ord('q'):
		break
cap.release()
cap.destroyAllWindows()
