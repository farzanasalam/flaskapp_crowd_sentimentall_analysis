
import cv2
from deepface import DeepFace
cap = cv2.VideoCapture(0)
facecascade=cv2.CascadeClassifier(r"C:\Users\LENOVO\Downloads\FACEEMOTIONRECOGNITION-20240402T092443Z-001\FACEEMOTIONRECOGNITION\haarcascade_frontalface_default.xml")

while True:
    # Capture a frame from the webcam
    ret, frame = cap.read()
    predictions = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)

   # convert input image to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = facecascade.detectMultiScale(gray,1.1,4)

# loop over all plates
    for (x,y,w,h) in faces:
        cv2.rectangle(frame, (x,y), (x+w, y+h), (255,0,0), 2)


# Add text to the image
    # Assuming emotions[0] contains the emotion as a string
    emotion_text = str(predictions[0])



# Modify the cv2.putText function to use emotion_text
    cv2.putText(frame, emotion_text, position, font, font_scale, font_color, font_thickness, cv2.LINE_AA)

    cv2.imshow("org",frame)

# Exit the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
