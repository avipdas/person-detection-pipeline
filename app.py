'''
    Flask: Web Server
    cv2: Webcam access + drawing
    YOLO: Object Detection Model
'''
from flask import Flask, Response, render_template_string
import cv2
from ultralytics import YOLO

# Intialize App and Model
app = Flask(__name__)
model = YOLO("yolov8n.pt") # Load pre-trained model
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # Open webcam

# HTML template
# Displays a heading and a live image feed (/video_Feed)
HTML = """
<html>
<head><title>Person Detection</title></head>
<body>
    <h1>Live Person Detection</h1>
    <img src="{{ url_for('video_feed') }}">
</body>
</html>
"""

def gen_frames():
    while True:
        success, frame = cap.read() # Grab frame
        if not success:
            break

        results = model(frame) # Run YOLO
        for r in results:
            for box in r.boxes:
                cls = int(box.cls[0])  # Class ID
                if cls == 0:  #  If it's a person
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 2) # Draw Box
                    cv2.putText(frame, "Person", (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,255,0), 2) # Add Label

        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

# Flask Routes
# / -> Homepage
@app.route('/')
def index():
    return render_template_string(HTML)

# /video_feed -> Live video stream
@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Run the app
# visit https://localhost:5000 in browser to see live. 
if __name__ == "__main__":
    app.run(debug=False)
