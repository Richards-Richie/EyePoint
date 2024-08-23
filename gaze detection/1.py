import cv2
import dlib
import os
import json
import sys

# Function to collect user information
def get_user_info():
    iris_color = "brown"
    return iris_color

# Pre-load detector and predictor
detector = dlib.get_frontal_face_detector()
try:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    target_file = os.path.join(current_dir, 'shape_predictor_68_face_landmarks.dat')
    predictor = dlib.shape_predictor(target_file)
except RuntimeError:
    print("Shape predictor file not found. Please download it from http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2")
    exit()

# Constants for eye landmarks
LEFT_EYE_START, LEFT_EYE_END = 36, 41
RIGHT_EYE_START, RIGHT_EYE_END = 42, 47

# Function to process webcam frame and get gaze
def get_gaze(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)

    if len(faces) == 1:
        face = faces[0]
        landmarks = predictor(gray, face)

        left_eye_left = landmarks.part(LEFT_EYE_START)
        left_eye_right = landmarks.part(LEFT_EYE_END)
        right_eye_left = landmarks.part(RIGHT_EYE_START)
        right_eye_right = landmarks.part(RIGHT_EYE_END)

        left_eye_center_x = (left_eye_left.x + left_eye_right.x) // 2
        left_eye_center_y = (left_eye_left.y + left_eye_right.y) // 2
        right_eye_center_x = (right_eye_left.x + right_eye_right.x) // 2
        right_eye_center_y = (right_eye_left.y + right_eye_right.y) // 2

        gaze_x = (left_eye_center_x + right_eye_center_x) // 2
        gaze_y = (left_eye_center_y + right_eye_center_y) // 2

        return gaze_x, gaze_y, face, landmarks
    else:
        return None, None, None, None

# Main program flow
user_iris_color = get_user_info()
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    gaze_x, gaze_y, face, landmarks = get_gaze(frame)

    if gaze_x is not None and gaze_y is not None:
        # Print gaze coordinates in JSON format
        gaze_data = json.dumps({'gaze_x': gaze_x, 'gaze_y': gaze_y})
        print(gaze_data)
        sys.stdout.flush()  # Ensure the output is immediately available for subprocess

        # Draw gaze point
        cv2.circle(frame, (gaze_x, gaze_y), 5, (0, 0, 255), -1)
        cv2.putText(frame, f"Gaze: ({gaze_x}, {gaze_y})", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # Draw face bounding box
        x1, y1, x2, y2 = face.left(), face.top(), face.right(), face.bottom()
        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)

        # Draw eye landmarks
        for i in range(LEFT_EYE_START, LEFT_EYE_END + 1):
            x, y = landmarks.part(i).x, landmarks.part(i).y
            cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)
        for i in range(RIGHT_EYE_START, RIGHT_EYE_END + 1):
            x, y = landmarks.part(i).x, landmarks.part(i).y
            cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)

    cv2.imshow('Gaze Detection (Estimate)', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

print(f"User Iris Color: {user_iris_color}")
