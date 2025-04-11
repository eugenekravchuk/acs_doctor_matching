
import pandas as pd
import re
import matplotlib.pyplot as plt
from collections import defaultdict

prefs_df = pd.read_csv("../data/doctors_schedule_160.csv")

doctor_preferences = {}
shift_counts = {}
for _, row in prefs_df.iterrows():
    name = row["doctor"]
    prefs = row.iloc[2:].tolist()
    doctor_preferences[name] = {str(shift).strip(): i + 1 for i, shift in enumerate(prefs)}
    shift_counts[name] = int(row["number_of_shifts"])

with open("../result/final_schedule.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()

doctor_assignments = defaultdict(list)
for line in lines:
    match = re.match(r"\s*Shift:\s*(\S+)\s*->\s*Doctor:\s*(.+)", line)
    if match:
        shift, doctor = match.groups()
        doctor_assignments[doctor.strip()].append(shift.strip())

satisfaction_data = []
for doctor, assigned_shifts in doctor_assignments.items():
    prefs = doctor_preferences.get(doctor, {})
    weighted_score = 0
    for shift in assigned_shifts:
        rank = prefs.get(shift, 0)
        if 8 <= rank <= 12:
            rank *= 2  # подвійне покарання
        weighted_score += rank
    count = len(assigned_shifts)
    norm_score = weighted_score / count if count else 0
    satisfaction_data.append({
        "doctor": doctor,
        "assigned_shifts": count,
        "weighted_score": weighted_score,
        "normalized_score": norm_score
    })

satisfaction_df = pd.DataFrame(satisfaction_data)
satisfaction_df = satisfaction_df.sort_values(by="normalized_score")
satisfaction_df.to_csv("metrics.csv", index=False)


filtered_df = satisfaction_df[satisfaction_df["normalized_score"] > 0]

plt.figure(figsize=(10, 6))
plt.hist(filtered_df["normalized_score"], bins=20, edgecolor='black')
plt.title("Розподіл нормалізованої задоволеності лікарів (з покаранням за пріоритети 8–12)")
plt.xlabel("Середній зважений ранг призначених змін")
plt.ylabel("Кількість лікарів")
plt.grid(True)
plt.tight_layout()
plt.savefig("satisfaction_histogram.png")


print("ТОП 10 лікарів з найгіршим розкладом (з урахуванням подвійного штрафу за пріоритети 8-12):")
print(satisfaction_df.tail(10).to_string(index=False))
print("\nМетрики збережено в 'metrics.csv'")
print("Графік збережено в 'satisfaction_histogram.png'")
