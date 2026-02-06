import face_recognition
import os
import pickle
import cv2

DATASET = "dataset"
OUT = "encodings/face_encodings.pickle"

encodings = []
students = []

for file in os.listdir(DATASET):
    if not file.lower().endswith(".jpg"):
        continue

    try:
        sid, name, branch, year = file.replace(".jpg", "").split("_")
    except ValueError:
        print(f"[SKIPPED] Invalid filename: {file}")
        continue

    image_path = os.path.join(DATASET, file)
    image = cv2.imread(image_path)

    if image is None:
        continue

    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    boxes = face_recognition.face_locations(rgb)

    if len(boxes) == 0:
        print(f"[NO FACE] {file}")
        continue

    face_encs = face_recognition.face_encodings(rgb, boxes)

    encodings.append(face_encs[0])
    students.append({
        "id": sid,
        "name": name,
        "branch": branch,
        "year": year
    })

os.makedirs("encodings", exist_ok=True)
with open(OUT, "wb") as f:
    pickle.dump({
        "encodings": encodings,
        "students": students
    }, f)

print("[SUCCESS] Face encodings generated from single-image dataset")
