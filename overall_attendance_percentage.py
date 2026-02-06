import csv
from collections import defaultdict

ATTENDANCE_FILE = "attendance/attendance.csv"
OUTPUT_FILE = "reports/overall_attendance_percentage.csv"

total_classes = set()
student_attendance = defaultdict(set)

with open(ATTENDANCE_FILE, "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        class_key = (row["Date"], row["Period"], row["Subject"])
        total_classes.add(class_key)

        student_attendance[row["ID"]].add(class_key)

# Write report
with open(OUTPUT_FILE, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow([
        "ID", "Name", "Branch", "Year",
        "Overall Attendance %"
    ])

    for sid, attended_classes in student_attendance.items():
        percentage = (len(attended_classes) / len(total_classes)) * 100 if total_classes else 0

        sample_row = next(
            r for r in csv.DictReader(open(ATTENDANCE_FILE))
            if r["ID"] == sid
        )

        writer.writerow([
            sid,
            sample_row["Name"],
            sample_row["Branch"],
            sample_row["Year"],
            f"{percentage:.2f}"
        ])

print("[SUCCESS] Overall attendance percentage generated")
