import csv
from collections import defaultdict

summary = defaultdict(int)

with open("attendance/attendance.csv") as f:
    reader = csv.DictReader(f)
    for r in reader:
        month = r["Date"][:7]
        summary[(month, r["Subject"])] += 1

with open("reports/monthly_summary.csv","w",newline="") as f:
    w = csv.writer(f)
    w.writerow(["Month","Subject","Total Attendance"])
    for k,v in summary.items():
        w.writerow([k[0],k[1],v])
