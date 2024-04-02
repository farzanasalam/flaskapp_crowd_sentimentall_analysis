import os
from flask import Flask, redirect, url_for, request, session, render_template, Response
from datetime import timedelta
import cv2
from deepface import DeepFace
from playsound import playsound
import time

app = Flask(__name__)
app.secret_key = "hello"
app.permanent_session_lifetime = timedelta(days=5)


def detect_emotion():
    # Initialize webcam
    cap = cv2.VideoCapture(0)

    xml_file_path = os.path.join(app.root_path, 'data', 'haarcascade_frontalface_default.xml')
    facecascade = cv2.CascadeClassifier(r'FACEEMOTIONRECOGNITION\haarcascade_frontalface_default.xml')

    while True:
        # Capture a frame from the webcam
        ret, frame = cap.read()
        predictions = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)

        # convert input image to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        faces = facecascade.detectMultiScale(gray, 1.1, 4)

        # loop over all faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        for prediction in predictions:
            dominant_emotion = prediction['dominant_emotion']
            region = prediction['region']

            # Add text to the frame
            cv2.putText(frame,
                        dominant_emotion,
                        (region['x'], region['y']),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,  # font scale
                        (255, 255, 255),  # white color
                        2)  # line thickness

        # Encode the frame as JPEG
        _, jpeg = cv2.imencode('.jpg', frame)
        frame_bytes = jpeg.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    # Release the webcam when the loop is finished
    cap.release()


@app.route("/video_feed")
def video_feed():
    # Return the response generated by the detect_emotion function
    return Response(detect_emotion(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


cpt = 0
maxFrames = 200  # Change this value if you want to capture a different number of frames.
count_threshold = 100  # Change this value to set the count threshold for the alarm


@app.route('/stress_analysis')
def stress_analysis():
    global cpt

    try:
        cap = cv2.VideoCapture(0)  # Capture video from the default camera
        while cpt < maxFrames:
            ret, frame = cap.read()
            if not ret:
                break
            frame = cv2.resize(frame, (1080, 500))
            cv2.imwrite(f"static/person_{cpt}.jpg", frame)  # Save the frame as an image file in the 'static' directory.
            cpt += 1
            if cpt > count_threshold:
                alarm_message = 'Alarm: Count exceeded Maximum Value!'
                print(alarm_message)
                return render_template('stress_analysis.html', alarm_message=alarm_message)
                # Print the alarm message for demonstration purposes

        cap.release()
        cv2.destroyAllWindows()

        return render_template('stress_analysis.html', alarm_message='')
    except Exception as e:
        return render_template('stress_analysis.html', alarm_message=f'An error occurred: {str(e)}')


@app.route("/")
def home():
    return render_template("first_page.html")


@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/guest")
def guest():
    return render_template("guest.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        user = request.form["nm"]
        session["user"] = user
        return redirect(url_for("user"))
    else:
        if "user" in session:
            return redirect(url_for("user"))
        return render_template("login.html")


@app.route("/user")
def user():
    if "user" in session:
        user = session["user"]
        return f"<h1>Successfully Logged In {user}!</h1><br><a href='/logout'>Logout</a>"
    else:
        return render_template(url_for("login"))


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)