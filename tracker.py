import cv2
import csv
from ultralytics import YOLO
import numpy as np
from sort import Sort

# Load YOLOv8n model
model = YOLO("yolov8n.pt")
tracker = Sort()

# Open webcam
#cap = cv2.VideoCapture("samples_data_vtest.avi")
cap = cv2.VideoCapture(0)

# Output CSV
csv_file = open("movement_log.csv", mode="w", newline="")
csv_writer = csv.writer(csv_file)
csv_writer.writerow(["frame", "track_id", "x1", "y1", "x2", "y2"])

frame_num = 0

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter("output.mp4", fourcc, 20.0, (int(cap.get(3)), int(cap.get(4))))

while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame_num += 1

    # Run YOLO detection
    results = model(frame)[0]
    detections = []

    for box in results.boxes:
        cls = float(box.conf[0])
        if cls == 0 and conf > 0.5:  # person
            x1, y1, x2, y2 = box.xyxy[0]
            conf = float(box.conf[0])
            detections.append([x1.item(), y1.item(), x2.item(), y2.item(), conf])

    # Track with SORT
    tracks = tracker.update(np.array(detections))

    for track in tracks:
        x1, y1, x2, y2, track_id = map(int, track)
        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
        cv2.putText(frame, f"ID: {track_id}", (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
        csv_writer.writerow([frame_num, track_id, x1, y1, x2, y2])

    out.write(frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Cleanup
out.release()
cap.release()
csv_file.close()
cv2.destroyAllWindows()
