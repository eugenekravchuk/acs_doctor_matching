import csv
from collections import defaultdict

doctors = []
doctor_prefs = {}
doctor_needed = {}
doctor_specialties = {}

with open("../data/dorctors_prefs.csv", encoding="utf-8") as f:
    reader = csv.reader(f)
    headers = next(reader)
    for row in reader:
        name = row[0].strip()
        needed = int(row[1])
        prefs = [s.strip() for s in row[2:]]
        doctors.append(name)
        doctor_needed[name] = needed
        doctor_prefs[name] = prefs


with open("../data/doctors_specialities.csv", encoding="utf-8") as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        name = row[0].strip()
        specialties = eval(row[1])
        doctor_specialties[name] = specialties

shift_info = {}

with open("../data/rooms_specialities.csv", encoding="utf-8") as f:
    reader = csv.reader(f)
    next(reader) 
    for i, row in enumerate(reader, start=1):
        shift = str(i)
        shift_info[shift] = {
            "room": row[0].strip(),
            "specialty": eval(row[1])
        }

# === Step 4: Gale-Shapley Matching Algorithm (with specialty filtering) ===

available_shifts = set()
for i in range(1, 7):
    for j in range(1, 3):
        available_shifts.add(f"{i}.{j}")

assignments = {}
doctor_current_index = {doc: 0 for doc in doctors}
assigned_counts = defaultdict(int)

while True:
    progress = False
    for doctor in doctors:
        if assigned_counts[doctor] >= doctor_needed[doctor]:
            continue

        prefs = doctor_prefs[doctor]
        idx = doctor_current_index[doctor]

        while idx < len(prefs):
            shift = prefs[idx]
            doctor_current_index[doctor] += 1
            idx += 1

            if shift not in available_shifts:
                continue

            shift_room = shift_info.get(shift.split(".")[0], {})
            shift_specialty = shift_room.get("specialty", [])
            doctor_specs = doctor_specialties.get(doctor, [])

            if not any(spec in doctor_specs for spec in shift_specialty):
                continue  # skip if doctor is not qualified

            assignments[shift] = doctor
            assigned_counts[doctor] += 1
            available_shifts.remove(shift)
            progress = True
            break

    if not progress:
        break

# === Step 5: Output results ===

for shift, doctor in sorted(assignments.items()):
    room = shift_info.get(shift.split(".")[0], {}).get("room", "?")
    specialty = shift_info.get(shift.split(".")[0], {}).get("specialty", ["?"])[0]
    print(f"Doctor: {doctor:25} -> Shift: {shift:4} Room: {room:30} Specialty: {specialty}")