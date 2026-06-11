# Crowd Analysis System

## Overview

The Crowd Analysis System is an AI-based monitoring solution developed to analyze crowd occupancy and movement in real time using computer vision.

The system detects people from a live camera feed, calculates occupancy levels, stores analytical data, and generates summary reports for operational insights.

---

## Features

### Crowd Detection

* Real-time person detection using YOLO.
* Live occupancy counting.

### Crowd Analytics

* Average Occupancy
* Peak Occupancy
* Minimum Occupancy
* Crowd Density Analysis

### Data Storage

* MongoDB integration.
* Minute-wise data storage.
* Automated summary generation.

### Reporting

* Excel report export.
* Daily summary reports.
* Historical data analysis.

---

## Technology Stack

* Python
* OpenCV
* YOLOv8
* MongoDB
* Pandas

---

## Project Structure

```text
crowd_analysis/

│
├── main.py
├── export_data.py
├── daily_summary.py
├── reports/
├── yolov8n.pt
└── README.md
```

---

## Database Structure

### Database

```text
crowd_monitoring
```

### Collections

```text
minute_data
summary_data
```

---

## How to Run

### Install Dependencies

```bash
pip install ultralytics
pip install opencv-python
pip install pymongo
pip install pandas
pip install openpyxl
```

### Start MongoDB

```bash
net start MongoDB
```

### Run Crowd Analysis

```bash
python main.py
```

### Export Summary Report

```bash
python export_data.py
```

### Generate Daily Summary

```bash
python daily_summary.py
```

---

## Generated Reports

Reports are automatically saved inside:

```text
reports/
```

Example:

```text
crowd_summary_report_YYYY-MM-DD.xlsx

daily_summary_YYYY-MM-DD.xlsx
```

---

## Current Status

Completed:

* Crowd Detection
* Crowd Analytics
* MongoDB Storage
* Excel Reporting
* Daily Summary Generation

Future Enhancements:

* CCTV Integration
* Advanced Analytics
* Real-Time Dashboard
* Multi-Camera Monitoring


