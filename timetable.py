from datetime import datetime, time, timedelta

# Attendance allowed only in first 10 minutes
ATTENDANCE_WINDOW_MINUTES = 10

# Weekly timetable (Mon–Sat)
TIMETABLE = {
    "Monday": {
        "Period 1": {"start": time(9, 0), "subject": "Data Structures"},
        "Period 2": {"start": time(10, 0), "subject": "Operating Systems"},
        "Period 3": {"start": time(11, 0), "subject": "DBMS"},
        "Period 4": {"start": time(12, 0), "subject": "Computer Networks"},
    },
    "Tuesday": {
        "Period 1": {"start": time(9, 0), "subject": "Operating Systems"},
        "Period 2": {"start": time(10, 0), "subject": "DBMS"},
        "Period 3": {"start": time(11, 0), "subject": "Data Structures"},
        "Period 4": {"start": time(12, 0), "subject": "Software Engineering"},
    },
    "Wednesday": {
        "Period 1": {"start": time(9, 0), "subject": "DBMS"},
        "Period 2": {"start": time(10, 0), "subject": "Computer Networks"},
        "Period 3": {"start": time(11, 0), "subject": "Operating Systems"},
        "Period 4": {"start": time(20, 49), "subject": "Data Structures"},
    },
    "Thursday": {
        "Period 1": {"start": time(9, 0), "subject": "Software Engineering"},
        "Period 2": {"start": time(10, 0), "subject": "Data Structures"},
        "Period 3": {"start": time(11, 0), "subject": "DBMS"},
        "Period 4": {"start": time(12, 0), "subject": "Computer Networks"},
    },
    "Friday": {
        "Period 1": {"start": time(9, 0), "subject": "Computer Networks"},
        "Period 2": {"start": time(10, 0), "subject": "Operating Systems"},
        "Period 3": {"start": time(11, 0), "subject": "Software Engineering"},
        "Period 4": {"start": time(12, 0), "subject": "DBMS"},
    },
    "Saturday": {
        "Period 1": {"start": time(9, 0), "subject": "Data Structures Lab"},
        "Period 2": {"start": time(10, 0), "subject": "DBMS Lab"},
        "Period 3": {"start": time(11, 0), "subject": "Mini Project"},
        "Period 4": {"start": time(12, 0), "subject": "Seminar"},
    }
}

def get_current_period():
    now = datetime.now()
    today = now.strftime("%A")  # Monday, Tuesday, etc.

    if today not in TIMETABLE:
        return None, None, None

    for period, info in TIMETABLE[today].items():
        start_dt = datetime.combine(now.date(), info["start"])
        end_dt = start_dt + timedelta(minutes=ATTENDANCE_WINDOW_MINUTES)

        if start_dt <= now <= end_dt:
            return period, info["subject"], today

    return None, None, today
