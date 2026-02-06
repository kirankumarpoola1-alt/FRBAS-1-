import cv2
import csv
import pickle
import os
from datetime import datetime

import face_recognition

from timetable import get_current_period
from utils.blink_detection import detect_blink
from utils.head_movement import detect_head_movement

# -------------------- LOAD FACE ENCODINGS --------------------
with open("encodings/face_encodings.pickle", "rb") as f:
    data = pickle.load(f)

known_encodings = data["encodings"]
students = data["students"]

# -------------------- ATTENDANCE FILE SETUP --------------------
os.makedirs("attendance", exist_ok=True)
ATTENDANCE_FILE = "attendance/attendance.csv"

# Create CSV if not exists
if not os.path.exists(ATTENDANCE_FILE):
    with open(ATTENDANCE_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "ID", "Name", "Branch", "Year",
            "Day", "Date", "Time",
            "Period", "Subject"
        ])

# -------------------- LOAD ALREADY MARKED ATTENDANCE --------------------
marked = set()

with open(ATTENDANCE_FILE, "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        # Unique key: one student, one day, one period
        marked.add((row["ID"], row["Day"], row["Period"]))

# -------------------- START CAMERA --------------------
cap = cv2.VideoCapture(0)

print("[INFO] Attendance system started")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Get current valid period
    period, subject, day = get_current_period()

    # If attendance window closed
    if period is None:
        cv2.putText(
            frame,
            "Attendance Closed",
            (30, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            2
        )
        cv2.imshow("Attendance System", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
        continue

    # Face detection
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    boxes = face_recognition.face_locations(rgb)
    encodings = face_recognition.face_encodings(rgb, boxes)

    blink_detected = detect_blink(frame)

    for encoding, box in zip(encodings, boxes):
        matches = face_recognition.compare_faces(known_encodings, encoding)

        if True not in matches:
            continue

        idx = matches.index(True)
        student = students[idx]

        key = (student["id"], day, period)

        # 🚫 BLOCK DUPLICATE ATTENDANCE
        if key in marked:
            continue

        # 🛡️ Liveness verification
        if blink_detected and detect_head_movement(box):
            now = datetime.now()

            with open(ATTENDANCE_FILE, "a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([
                    student["id"],
                    student["name"],
                    student["branch"],
                    student["year"],
                    day,
                    now.strftime("%Y-%m-%d"),
                    now.strftime("%H:%M:%S"),
                    period,
                    subject
                ])

            marked.add(key)
            print(f"[MARKED] {student['name']} | {period} | {subject}")

            cv2.putText(
                frame,
                f"Marked: {student['name']}",
                (30, 80),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9,
                (0, 255, 0),
                2
            )

    cv2.imshow("Attendance System", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# -------------------- CLEANUP --------------------
cap.release()
cv2.destroyAllWindows()
print("[INFO] Attendance system stopped")
