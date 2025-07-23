import cv2
import numpy as np
import json
import time
from ultralytics import YOLO
from sort import Sort
from collections import defaultdict

model = YOLO("yolov8n.pt")
tracker = Sort()
cap = cv2.VideoCapture(0)

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter("anomaly_output.mp4", fourcc, 20.0, (int(cap.get(3)), int(cap.get(4))))
anomaly_log = open("anomaly_log.jsonl", "w")

LOITER_THRESHOLD = 30  
REGION = (100, 100, 400, 400)  
OVERCOUNT_THRESHOLD = 3

track_history = defaultdict(list) 

def in_region(x, y, region):
    x1, y1, x2, y2 = region
    return x1 <= x <= x2 and y1 <= y <= y2

def direction(positions):
    if len(positions) < 2:
        return "unknown"
    dx = positions[-1][0] - positions[0][0]
    return "right" if dx > 0 else "left"

while True:
    ret, frame = cap.read()
    if not ret:
        break
    timestamp = time.time()

    results = model(frame)[0]
    detections = []

    for box in results.boxes:
        cls = int(box.cls[0])
        if cls == 0:
            x1, y1, x2, y2 = box.xyxy[0]
            conf = float(box.conf[0])
            detections.append([x1.item(), y1.item(), x2.item(), y2.item(), conf])

    tracks = tracker.update(np.array(detections))

    count_in_region = 0

    for track in tracks:
        x1, y1, x2, y2, track_id = map(int, track)
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        track_history[track_id].append((cx, cy, timestamp))
        track_history[track_id] = [p for p in track_history[track_id] if timestamp - p[2] <= 60]

        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame, f"ID {track_id}", (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        dwell_time = timestamp - track_history[track_id][0][2]
        if dwell_time > LOITER_THRESHOLD:
            cv2.putText(frame, "LOITER", (x1, y2 + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
            anomaly_log.write(json.dumps({
                "type": "loitering",
                "id": int(track_id),
                "duration": round(dwell_time, 2),
                "timestamp": timestamp
            }) + "\n")

        if len(track_history[track_id]) > 10:
            dir_label = direction([pos[:2] for pos in track_history[track_id]])
            if dir_label == "left":
                cv2.putText(frame, "WRONG DIR", (x1, y2 + 40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
                anomaly_log.write(json.dumps({
                    "type": "wrong_direction",
                    "id": int(track_id),
                    "direction": dir_label,
                    "timestamp": timestamp
                }) + "\n")

        if in_region(cx, cy, REGION):
            count_in_region += 1

    cv2.rectangle(frame, REGION[:2], REGION[2:], (255, 0, 0), 2)
    if count_in_region > OVERCOUNT_THRESHOLD:
        cv2.putText(frame, "OVERCROWDING", (REGION[0], REGION[1] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        anomaly_log.write(json.dumps({
            "type": "overcrowding",
            "count": count_in_region,
            "timestamp": timestamp
        }) + "\n")

    out.write(frame)
    cv2.imshow("Anomaly Detection", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
out.release()
anomaly_log.close()
cv2.destroyAllWindows()
