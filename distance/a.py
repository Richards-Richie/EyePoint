print("Hello World")
import os
import cv2 # type: ignore

# Base directory setup
base_dir = os.path.dirname(os.path.abspath(__file__))

# Set paths to your files using absolute paths
cascade_path = os.path.join(base_dir, 'haarcascade_frontalface_default.xml')
ref_image_path = os.path.join(base_dir, 'Ref_image.png')

# Load the Haar Cascade
face_detector = cv2.CascadeClassifier(cascade_path)
if face_detector.empty():
    raise IOError(f"Cannot load cascade file: {cascade_path}")

# Load the reference image
ref_image = cv2.imread(ref_image_path)
if ref_image is None:
    raise IOError(f"Cannot load image file: {ref_image_path}")

# Variables
Known_distance = 30  # Inches
Known_width = 5.7  # Inches

# Colors
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
ORANGE = (0, 69, 255)
YELLOW = (0, 255, 255)

fonts = cv2.FONT_HERSHEY_COMPLEX

# Camera Object
cap = cv2.VideoCapture(0)
Distance_level = 0

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*"XVID")
out = cv2.VideoWriter("output21.mp4", fourcc, 30.0, (640, 480))

def FocalLength(measured_distance, real_width, width_in_rf_image):
    focal_length = (width_in_rf_image * measured_distance) / real_width
    return focal_length

def Distance_finder(Focal_Length, real_face_width, face_width_in_frame):
    distance = (real_face_width * Focal_Length) / face_width_in_frame
    return distance

def face_data(image, CallOut, Distance_level):
    face_width = 0
    face_center_x = 0
    face_center_y = 0
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(gray_image, 1.3, 5)
    for (x, y, w, h) in faces:
        line_thickness = 2
        LLV = int(h * 0.12)
        cv2.line(image, (x, y + LLV), (x + w, y + LLV), GREEN, line_thickness)
        cv2.line(image, (x, y + h), (x + w, y + h), GREEN, line_thickness)
        cv2.line(image, (x, y + LLV), (x, y + LLV + LLV), GREEN, line_thickness)
        cv2.line(image, (x + w, y + LLV), (x + w, y + LLV + LLV), GREEN, line_thickness)
        cv2.line(image, (x, y + h), (x, y + h - LLV), GREEN, line_thickness)
        cv2.line(image, (x + w, y + h), (x + w, y + h - LLV), GREEN, line_thickness)
        face_width = w
        face_center_x = int(w / 2) + x
        face_center_y = int(h / 2) + y
        if Distance_level < 10:
            Distance_level = 10
        if CallOut:
            cv2.line(image, (x, y - 11), (x + 180, y - 11), ORANGE, 28)
            cv2.line(image, (x, y - 11), (x + 180, y - 11), YELLOW, 20)
            cv2.line(image, (x, y - 11), (x + Distance_level, y - 11), GREEN, 18)
    return face_width, faces, face_center_x, face_center_y

ref_image_face_width, _, _, _ = face_data(ref_image, False, Distance_level)
Focal_length_found = FocalLength(Known_distance, Known_width, ref_image_face_width)
print(Focal_length_found)

cv2.imshow("ref_image", ref_image)

while True:
    _, frame = cap.read()
    face_width_in_frame, Faces, FC_X, FC_Y = face_data(frame, True, Distance_level)
    for (face_x, face_y, face_w, face_h) in Faces:
        if face_width_in_frame != 0:
            Distance = Distance_finder(Focal_length_found, Known_width, face_width_in_frame)
            Distance = round(Distance, 2)
            Distance_level = int(Distance)
            cv2.putText(frame, f"Distance {Distance} Inches", (face_x - 6, face_y - 6), fonts, 0.5, BLACK, 2)
    cv2.imshow("frame", frame)
    out.write(frame)
    if cv2.waitKey(1) == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
