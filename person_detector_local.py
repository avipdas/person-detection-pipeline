'''
    1. Opens webcam
    2. YOLO detects people
    3. Draws boxes
    4. Displays live results
    5. Press 'q' to stop
'''
import cv2                   # For video capture and drawing
from ultralytics import YOLO # Loads YOLO8n model

# Load YOLOv8n (tiny) pre-trained model
model = YOLO("yolov8n.pt")

# Captures from my your laptop's webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read() # Gets a single frame from the webcam
    if not ret:
        break

    # Run detection on the frame
    results = model(frame)

    # Draw bounding boxes
    for r in results:
        for box in r.boxes:
            cls = int(box.cls[0]) # Get the class (0 = person)
            if cls == 0:  # Person class
                x1, y1, x2, y2 = map(int, box.xyxy[0]) # Coordinates
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2) # Draw box
                cv2.putText(frame, "Person", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2) # Label it "Person"

    cv2.imshow("Person Detection", frame) # Live display 

    if cv2.waitKey(1) == ord('q'): # Quit when you press 'q'
        break

cap.release()
cv2.destroyAllWindows()
