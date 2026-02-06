import pickle
import csv
import os
from datetime import datetime
from timetable import PERIODS

ENCODINGS = "encodings/face_encodings.pickle"
ATTENDANCE_FILE = "attendance/attendance.csv"
ABSENT_FILE = "absentee/absentees.csv"

today = datetime.now().strftime("%Y-%m-%d")

# Load all registered students
with open(ENCODINGS, "rb") as f:
    data = pickle.load(f)

students = {}
for s in data["students"]:
    students[s["id"]] = s

os.makedirs("absentee", exist_ok=True)

# Read attendance data
attendance = {}
with open(ATTENDANCE_FILE, "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row["Date"] == today:
            key = row["Period"]
            attendance.setdefault(key, set()).add(row["ID"])

# Generate absentees per period
with open(ABSENT_FILE, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Date", "Period", "ID", "Name", "Branch", "Year"])

    for period in PERIODS.keys():
        present_ids = attendance.get(period, set())

        for sid, s in students.items():
            if sid not in present_ids:
                writer.writerow([
                    today,
                    period,
                    sid,
                    s["name"],
                    s["branch"],
                    s["year"]
                ])

print("[INFO] Absentees list generated successfully")
