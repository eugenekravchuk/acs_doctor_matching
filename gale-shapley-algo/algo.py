import csv
from collections import defaultdict

# === Data Loading ===

# Load doctor preferences.
# File format: doctor,number_of_shifts,1,2,...,12 (where the numbers are shift codes, e.g., "5.2")
doctors = []
doctor_prefs = {}
doctor_needed = {}
with open("../data/doctor_prefs.csv", encoding="utf-8") as f:
    reader = csv.reader(f)
    header = next(reader)  # e.g., ["doctor", "number_of_shifts", "1", "2", ..., "12"]
    for row in reader:
        doctor = row[0].strip()
        doctors.append(doctor)
        doctor_needed[doctor] = int(row[1])
        # Each doctor's preferences is a list of shift codes (e.g., "5.2")
        doctor_prefs[doctor] = [s.strip() for s in row[2:]]

# Load doctor specialties.
# File format: doctor,specialty   (with specialty given as a list, e.g., "['Терапія']")
doctor_specialties = {}
with open("../data/doctor_specialities.csv", encoding="utf-8") as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        doctor = row[0].strip()
        specialties = eval(row[1])
        doctor_specialties[doctor] = specialties

# Load cabinet (room) specialties.
# File format: room,specialty   (we enumerate the rows to assign a cabinet id)
cabinet_info = {}
with open("../data/rooms_specialities.csv", encoding="utf-8") as f:
    reader = csv.reader(f)
    next(reader)
    for i, row in enumerate(reader, start=1):
        cabinet_id = str(i)
        cabinet_info[cabinet_id] = {
            "room": row[0].strip(),
            "specialty": eval(row[1])
        }

# === Build Available Shift Slots ===

# Each cabinet gets 12 shifts: days 1..6 with two shifts per day (coded as "day.shift")
available_shifts = {}  # key: (cabinet_id, shift_code) with value None (unassigned) or a doctor name.
for cabinet_id in cabinet_info:
    for day in range(1, 7):
        for sh in range(1, 3):
            shift_code = f"{day}.{sh}"
            available_shifts[(cabinet_id, shift_code)] = None

# === Gale–Shapley–Style Matching ===

# For each doctor, keep track of which preference they have proposed to so far.
doctor_current_index = {doctor: 0 for doctor in doctors}
doctor_assigned_counts = defaultdict(int)
assignments = {}  # mapping from (cabinet_id, shift_code) to doctor

# --- Phase 1: Preference-Based Assignment ---
progress = True
while progress:
    progress = False
    for doctor in doctors:
        # Skip if doctor has reached their allowed number of shifts.
        if doctor_assigned_counts[doctor] >= doctor_needed[doctor]:
            continue
        # If the doctor has exhausted their preference list, skip for now.
        if doctor_current_index[doctor] >= len(doctor_prefs[doctor]):
            continue
        # Get the next preferred shift code (e.g., "5.2")
        pref = doctor_prefs[doctor][doctor_current_index[doctor]]
        doctor_current_index[doctor] += 1

        # Try to assign the doctor to any cabinet that has this shift slot available
        # and where the cabinet's required specialty is among the doctor's specialties.
        for cabinet_id in sorted(cabinet_info.keys(), key=int):
            slot = (cabinet_id, pref)
            # Check that the slot exists and is unassigned.
            if slot not in available_shifts or available_shifts[slot] is not None:
                continue
            # Check qualification: does the doctor have any specialty that matches the cabinet's requirement?
            doc_specs = doctor_specialties.get(doctor, [])
            cab_specs = cabinet_info[cabinet_id]["specialty"]
            if not any(spec in doc_specs for spec in cab_specs):
                continue
            # Assign doctor to this shift slot.
            available_shifts[slot] = doctor
            assignments[slot] = doctor
            doctor_assigned_counts[doctor] += 1
            progress = True
            break  # Stop searching cabinets for this proposal

# --- Phase 2: Fallback Assignment for Unfilled Slots ---
# For any remaining available slot, try to fill it with any qualified doctor with capacity.
for slot, assigned in list(available_shifts.items()):
    if assigned is None:
        cabinet_id, shift_code = slot
        cab_specs = cabinet_info[cabinet_id]["specialty"]
        for doctor in doctors:
            if doctor_assigned_counts[doctor] >= doctor_needed[doctor]:
                continue
            doc_specs = doctor_specialties.get(doctor, [])
            if not any(spec in doc_specs for spec in cab_specs):
                continue
            # Assign this doctor as a fallback.
            available_shifts[slot] = doctor
            assignments[slot] = doctor
            doctor_assigned_counts[doctor] += 1
            break

# Optionally, warn if any slot remains unfilled.
unfilled = [slot for slot, doc in available_shifts.items() if doc is None]
if unfilled:
    print("Warning: Some slots remain unfilled:", unfilled)

# === Output the Schedule ===

# Organize assignments by cabinet (room).
cabinet_schedule = defaultdict(list)
for (cabinet_id, shift_code), doctor in assignments.items():
    room_name = cabinet_info[cabinet_id]["room"]
    cabinet_schedule[room_name].append((shift_code, doctor))

# Write the schedule to a file.
with open("schedule_output.txt", "w", encoding="utf-8") as out:
    for room in sorted(cabinet_schedule.keys()):
        out.write(f"Cabinet: {room}\n")
        # Sort the shifts in order (by day and shift number)
        schedule = sorted(cabinet_schedule[room], key=lambda x: tuple(map(int, x[0].split("."))))
        for shift_code, doctor in schedule:
            out.write(f"  Shift: {shift_code:4} -> Doctor: {doctor}\n")
        out.write("\n")

print("Schedule written to schedule_output.txt")
