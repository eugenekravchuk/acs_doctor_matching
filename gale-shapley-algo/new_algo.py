import csv
from collections import defaultdict

# === Step 1: Parse data ===

doctors = []
doctor_prefs = {}
doctor_needed = {}

with open("../data/rating_table.csv", encoding="utf-8") as f:
    reader = csv.reader(f)
    headers = next(reader)
    for row in reader:
        name = row[0].strip()
        needed = int(row[1])
        prefs = [s.strip() for s in row[2:]]
        doctors.append(name)
        doctor_needed[name] = needed
        doctor_prefs[name] = prefs

# === Step 2: Parse shift-room-specialty mapping ===

shift_info = {}

with open("../data/rooms_specialities.csv", encoding="utf-8") as f:
    reader = csv.reader(f)
    next(reader)  # skip header
    for i, row in enumerate(reader, start=1):
        shift = str(i)  # shifts are numbered from 1 to 12
        shift_info[shift] = {
            "room": row[0].strip(),
            "specialty": eval(row[1])
        }

# === Step 3: Gale-Shapley Matching Algorithm ===

# available_shifts maps shift_id like '3.2' to whether it's free
available_shifts = set()
for i in range(1, 7):
    for j in range(1, 3):
        available_shifts.add(f"{i}.{j}")

# result: shift_id -> doctor
assignments = {}

doctor_current_index = {doc: 0 for doc in doctors}  # where each doctor is in their pref list
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

            if shift in available_shifts:
                assignments[shift] = doctor
                assigned_counts[doctor] += 1
                available_shifts.remove(shift)
                progress = True
                break  # move to next doctor

    if not progress:
        break  # no further assignments possible

# === Step 4: Output results ===

for shift, doctor in sorted(assignments.items()):
    room = shift_info.get(shift.split(".")[0], {}).get("room", "?")
    specialty = shift_info.get(shift.split(".")[0], {}).get("specialty", ["?"])[0]
    print(f"Doctor: {doctor:25} -> Shift: {shift:4} Room: {room:30} Specialty: {specialty}")
