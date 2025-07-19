# Real-Time Person Detection Web App

This project is a real-time person detection system using [YOLOv8n](https://github.com/ultralytics/ultralytics) and OpenCV, streamed through a Flask web server. It uses your webcam to detect people in the video feed and displays it with bounding boxes in your browser.

---

## ✅ Week 1: Setup & Real-Time Detection

### Goals:
- Install Python, OpenCV, Flask, and YOLOv8n
- Capture webcam feed using OpenCV
- Run real-time person detection (using `yolov8n.pt`)
- Draw bounding boxes and labels
- Stream the processed video feed via Flask

---

## 📷 Live Demo Screenshot

![Screenshot of live detection](images/Screenshot (280).png)


---

## 🗂 Files

| File              | Description                                 |
|-------------------|---------------------------------------------|
| `app.py`          | Main Flask app for streaming detection      |
| `person_detector.py` | Local test script (optional/archived)     |
| `yolov8n.pt`      | YOLOv8n model weights (ignored in Git)      |
| `.gitignore`      | Ignores venv, model weights, cache, etc.    |

---

## 🚀 How to Run

```bash
# (1) Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate   # On Windows

# (2) Install dependencies
pip install ultralytics opencv-python flask

# (3) Run the app
python app.py

# (4) Open in browser
http://localhost:5000

## ⚙️ Tech Stack

- **Python** – general-purpose programming language  
- **OpenCV** – real-time computer vision library  
- **Flask** – lightweight Python web framework  
- **YOLOv8 (Ultralytics)** – object detection model for identifying people in video frames  
