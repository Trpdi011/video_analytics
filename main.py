import cv2
import time
import tkinter as tk

from datetime import datetime
from pymongo import MongoClient
from ultralytics import YOLO

# =====================================
# MongoDB
# =====================================

client = MongoClient("mongodb://localhost:27018/")

db = client["crowd_monitoring"]

minute_data = db["minute_data"]
summary_data = db["summary_data"]

# =====================================
# YOLO
# =====================================

model = YOLO("yolov8n.pt")

# =====================================
# Screen Size
# =====================================

root = tk.Tk()

SCREEN_W = root.winfo_screenwidth()
SCREEN_H = root.winfo_screenheight()

root.destroy()

# =====================================
# Camera
# =====================================

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Camera not found")
    exit()

# =====================================
# Full Screen
# =====================================

cv2.namedWindow(
    "Crowd Monitoring",
    cv2.WINDOW_NORMAL
)

cv2.setWindowProperty(
    "Crowd Monitoring",
    cv2.WND_PROP_FULLSCREEN,
    cv2.WINDOW_FULLSCREEN
)

# =====================================
# Configuration
# =====================================

SUMMARY_INTERVAL = 30

last_minute_save = time.time()

summary_start = datetime.now()

occupancy_samples = []

minute_records = []

print("System Started")

# =====================================
# Main Loop
# =====================================

while True:

    ret, frame = cap.read()

    if not ret:
        break

    frame = cv2.resize(
        frame,
        (SCREEN_W, SCREEN_H)
    )

    current_time = datetime.now()

    # =====================================
    # Detection
    # =====================================

    results = model(frame, verbose=False)

    current_occupancy = 0

    for result in results:

        for box in result.boxes:

            cls = int(box.cls[0])

            if cls == 0:

                current_occupancy += 1

                x1, y1, x2, y2 = map(
                    int,
                    box.xyxy[0]
                )

                cv2.rectangle(
                    frame,
                    (x1, y1),
                    (x2, y2),
                    (0, 255, 0),
                    2
                )

    occupancy_samples.append(
        current_occupancy
    )

    # =====================================
    # Save Every Minute
    # =====================================

    if time.time() - last_minute_save >= 60:

        if len(occupancy_samples) > 0:

            avg_occ = round(
                sum(occupancy_samples)
                / len(occupancy_samples),
                2
            )

            peak_occ = max(
                occupancy_samples
            )

            min_occ = min(
                occupancy_samples
            )

            minute_data.insert_one({

                "timestamp":
                datetime.now(),

                "avg_occupancy":
                avg_occ,

                "peak_occupancy":
                peak_occ,

                "min_occupancy":
                min_occ

            })

            minute_records.append({

                "avg_occupancy":
                avg_occ,

                "peak_occupancy":
                peak_occ,

                "min_occupancy":
                min_occ

            })

            print(
                f"Minute Saved | "
                f"Avg={avg_occ} "
                f"Peak={peak_occ} "
                f"Min={min_occ}"
            )

        occupancy_samples.clear()

        last_minute_save = time.time()

    # =====================================
    # 30 Minute Summary
    # =====================================

    elapsed = (
        datetime.now() -
        summary_start
    ).total_seconds()

    if elapsed >= SUMMARY_INTERVAL:

        if len(minute_records) > 0:

            avg_occ = round(

                sum(
                    x["avg_occupancy"]
                    for x in minute_records
                )
                /
                len(minute_records),

                2

            )

            peak_occ = max(

                x["peak_occupancy"]
                for x in minute_records

            )

            min_occ = min(

                x["min_occupancy"]
                for x in minute_records

            )

            summary_data.insert_one({

                "date":
                summary_start.strftime(
                    "%Y-%m-%d"
                ),

                "start_time":
                summary_start.strftime(
                    "%H:%M:%S"
                ),

                "end_time":
                datetime.now().strftime(
                    "%H:%M:%S"
                ),

                "average_occupancy":
                avg_occ,

                "peak_occupancy":
                peak_occ,

                "minimum_occupancy":
                min_occ

            })

            print(
                "30 Minute Summary Saved"
            )

        minute_records.clear()

        summary_start = datetime.now()

    # =====================================
    # Display Occupancy
    # =====================================

    cv2.putText(

        frame,

        f"Current Occupancy: {current_occupancy}",

        (20, 40),

        cv2.FONT_HERSHEY_SIMPLEX,

        0.8,

        (0, 255, 255),

        2

    )

    # =====================================
    # Timestamp
    # =====================================

    timestamp_text = current_time.strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    text_size = cv2.getTextSize(
        timestamp_text,
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        2
    )[0]

    cv2.putText(

        frame,

        timestamp_text,

        (
            SCREEN_W -
            text_size[0] -
            20,

            40
        ),

        cv2.FONT_HERSHEY_SIMPLEX,

        0.8,

        (0, 255, 0),

        2

    )

    cv2.imshow(
        "Crowd Monitoring",
        frame
    )

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# =====================================
# Cleanup
# =====================================

cap.release()

cv2.destroyAllWindows()