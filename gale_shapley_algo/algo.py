import csv
from collections import defaultdict
from typing import Dict, List, Tuple
import random


def read_doctor_preferences(filepath: str) -> Tuple[List[str], Dict[str, int], Dict[str, List[str]]]:
    doctors = []
    doctor_needed = {}
    doctor_prefs = {}
    with open(filepath, encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            doctor = row[0].strip()
            doctors.append(doctor)
            doctor_needed[doctor] = int(row[1])
            doctor_prefs[doctor] = [s.strip() for s in row[2:]]
    return doctors, doctor_needed, doctor_prefs


def read_doctor_specialties(filepath: str) -> Dict[str, List[str]]:
    doctor_specialties = {}
    with open(filepath, encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            doctor = row[0].strip()
            specialties = eval(row[1])  # Replace with safer parsing if possible
            doctor_specialties[doctor] = specialties
    return doctor_specialties


def read_cabinet_info(filepath: str) -> Dict[str, Dict]:
    cabinet_info = {}
    with open(filepath, encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)
        for i, row in enumerate(reader, start=1):
            cabinet_id = str(i)
            cabinet_info[cabinet_id] = {
                "room": row[0].strip(),
                "specialty": eval(row[1])  # Replace with safer parsing if possible
            }
    return cabinet_info


def generate_schedule(doctors, doctor_needed, doctor_prefs, doctor_specialties, cabinet_info):
    available_shifts = {}
    for cabinet_id in cabinet_info:
        for day in range(1, 4):
            for sh in range(1, 3):
                shift_code = f"{day}.{sh}"
                available_shifts[(cabinet_id, shift_code)] = None

    doctor_current_index = {doctor: 0 for doctor in doctors}
    doctor_assigned_counts = defaultdict(int)
    assignments = {}

    progress = True
    while progress:
        progress = False
        for doctor in doctors:
            if doctor_assigned_counts[doctor] >= doctor_needed[doctor]:
                continue
            if doctor_current_index[doctor] >= len(doctor_prefs[doctor]):
                continue
            pref = doctor_prefs[doctor][doctor_current_index[doctor]]
            doctor_current_index[doctor] += 1
            for cabinet_id in sorted(cabinet_info.keys(), key=int):
                slot = (cabinet_id, pref)
                if slot not in available_shifts or available_shifts[slot] is not None:
                    continue
                doc_specs = doctor_specialties.get(doctor, [])
                cab_specs = cabinet_info[cabinet_id]["specialty"]
                if not any(spec in doc_specs for spec in cab_specs):
                    continue
                available_shifts[slot] = doctor
                assignments[slot] = doctor
                doctor_assigned_counts[doctor] += 1
                progress = True
                break

    # Second pass: fill remaining
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
                available_shifts[slot] = doctor
                assignments[slot] = doctor
                doctor_assigned_counts[doctor] += 1
                break

    return available_shifts, assignments, doctor_assigned_counts


# def compute_doctor_happiness(doctors, assignments, doctor_prefs, doctor_assigned_counts) -> Dict[str, float]:
#     doctor_happiness = {}
#     for doctor in doctors:
#         total_shifts = doctor_assigned_counts[doctor]
#         if total_shifts == 0:
#             doctor_happiness[doctor] = 0
#             continue
#         assigned_prefs = [pref for (cabinet, pref), doc in assignments.items() if doc == doctor]
#         happiness_score = sum(12 if pref in doctor_prefs[doctor][-2:] else 1 for pref in assigned_prefs)
#         doctor_happiness[doctor] = happiness_score / total_shifts
#     return doctor_happiness

def compute_doctor_happiness(doctors, assignments, doctor_prefs, doctor_assigned_counts) -> Dict[str, float]:
    doctor_happiness = {}
    for doctor in doctors:
        total_shifts = doctor_assigned_counts[doctor]
        if total_shifts == 0:
            doctor_happiness[doctor] = 0
            continue

        assigned_prefs = [pref for (cabinet, pref), doc in assignments.items() if doc == doctor]
        happiness_score = 0
        for pref in assigned_prefs:
            try:
                pref_index = doctor_prefs[doctor].index(pref)
                score = max(1, 12 - pref_index)
            except ValueError:
                score = 0
            happiness_score += score

        doctor_happiness[doctor] = happiness_score / total_shifts

    return sum(doctor_happiness.values()) / len(doctor_happiness.values())

def write_schedule(assignments, cabinet_info, output_file="schedule_output.txt"):
    cabinet_schedule = defaultdict(list)
    for (cabinet_id, shift_code), doctor in assignments.items():
        room_name = cabinet_info[cabinet_id]["room"]
        cabinet_schedule[room_name].append((shift_code, doctor))

    with open(output_file, "w", encoding="utf-8") as out:
        for room in sorted(cabinet_schedule.keys()):
            out.write(f"Cabinet: {room}\n")
            schedule = sorted(cabinet_schedule[room], key=lambda x: tuple(map(int, x[0].split("."))))
            for shift_code, doctor in schedule:
                out.write(f"  Shift: {shift_code:4} -> Doctor: {doctor}\n")
            out.write("\n")

def run_scheduler(prefs_path, specialties_path, cabinets_path, output_path="schedule_output.txt"):
    doctors, doctor_needed, doctor_prefs = read_doctor_preferences(prefs_path)
    random.shuffle(doctors)
    doctor_specialties = read_doctor_specialties(specialties_path)
    cabinet_info = read_cabinet_info(cabinets_path)
    available_shifts, assignments, doctor_assigned_counts = generate_schedule(
        doctors, doctor_needed, doctor_prefs, doctor_specialties, cabinet_info
    )

    unfilled = [slot for slot, doc in available_shifts.items() if doc is None]
    if unfilled:
        print("Warning: Some slots remain unfilled:", unfilled)

    happiness = compute_doctor_happiness(doctors, assignments, doctor_prefs, doctor_assigned_counts)
    write_schedule(assignments, cabinet_info, output_path)
    return happiness


if __name__ == "__main__":

    run_scheduler(
        "../data/doctor_prefs.csv",
        "../data/doctor_specialities.csv",
        "../data/rooms_specialities.csv"
    )
