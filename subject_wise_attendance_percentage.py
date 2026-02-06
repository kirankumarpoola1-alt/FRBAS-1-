import csv
from collections import defaultdict

ATTENDANCE_FILE = "attendance/attendance.csv"
OUTPUT_FILE = "reports/subject_wise_attendance_percentage.csv"

# subject → total classes conducted
total_classes = defaultdict(set)

# (student_id, subject) → classes attended
student_attendance = defaultdict(set)

with open(ATTENDANCE_FILE, "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        key = (row["Date"], row["Period"], row["Subject"])
        total_classes[row["Subject"]].add(key)

        student_key = (row["ID"], row["Subject"])
        student_attendance[student_key].add(key)

# Write report
with open(OUTPUT_FILE, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow([
        "ID", "Name", "Branch", "Year",
        "Subject", "Attendance %"
    ])

    for (sid, subject), attended_classes in student_attendance.items():
        total = len(total_classes[subject])
        percentage = (len(attended_classes) / total) * 100 if total > 0 else 0

        # Get student details
        sample_row = next(
            r for r in csv.DictReader(open(ATTENDANCE_FILE))
            if r["ID"] == sid and r["Subject"] == subject
        )

        writer.writerow([
            sid,
            sample_row["Name"],
            sample_row["Branch"],
            sample_row["Year"],
            subject,
            f"{percentage:.2f}"
        ])

print("[SUCCESS] Subject-wise attendance percentage generated")
