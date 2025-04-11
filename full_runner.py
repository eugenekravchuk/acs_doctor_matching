import os
import re
import pandas as pd
from gale_shapley_algo.algo import run_scheduler

# === КОНФІГУРАЦІЯ ===
NUM_WEEKS = 4
NUM_ITERATIONS = 100
DATA_PATHS = (
    "./data/doctors_schedule_160.csv",
    "./data/doctors_160.csv",
    "./data/rooms_80.csv",
)

# === КАТАЛОГИ ===
os.makedirs("weekly_schedules", exist_ok=True)
os.makedirs("result", exist_ok=True)

# === ФУНКЦІЯ ПРОГРЕС-БАРУ ===
def print_progress_bar(iteration, total, prefix='', length=50):
    percent = f"{100 * (iteration / total):.1f}"
    filled_length = int(length * iteration // total)
    bar = '█' * filled_length + '-' * (length - filled_length)
    print(f'\r{prefix} |{bar}| {percent}% Complete', end='\r')
    if iteration == total:
        print()

# === ГЕНЕРАЦІЯ НАЙКРАЩИХ РОЗКЛАДІВ НА КОЖЕН ТИЖДЕНЬ ===
for week in range(1, NUM_WEEKS + 1):
    best_happiness = -1
    best_file = None

    print(f"\n📅 Тиждень {week}:")
    for i in range(NUM_ITERATIONS):
        output_file = f"result/week{week}_output_{i}.txt"
        happiness = run_scheduler(*DATA_PATHS, output_file)
        if happiness > best_happiness:
            best_happiness = happiness
            best_file = output_file
        print_progress_bar(i + 1, NUM_ITERATIONS, prefix='Optimizing')

    for i in range(NUM_ITERATIONS):
        fname = f"result/week{week}_output_{i}.txt"
        if fname != best_file and os.path.exists(fname):
            os.remove(fname)

    final_path = f"weekly_schedules/week_{week}.txt"
    if best_file and os.path.exists(best_file):
        if os.path.exists(final_path):
            os.remove(final_path)
        os.rename(best_file, final_path)

def parse_schedule(filepath, week_number):
    records = []
    cabinet = None
    with open(filepath, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line.startswith("Cabinet:"):
                match = re.search(r"Cabinet: (\d+)", line)
                if match:
                    cabinet = match.group(1)
            elif "Shift" in line:
                match = re.search(r"Shift: (\d\.\d)\s+-> Doctor: (.+)", line)
                if match:
                    shift, doctor = match.groups()
                    day, part = shift.split('.')
                    records.append({
                        "Week": week_number,
                        "Day": int(day),
                        "Shift": int(part),
                        "Cabinet": cabinet,
                        "Doctor": doctor
                    })
    return records

# Збір усіх записів
all_records = []
for week in range(1, 5):
    file_path = f"weekly_schedules/week_{week}.txt"
    if os.path.exists(file_path):
        all_records.extend(parse_schedule(file_path, week))

df = pd.DataFrame(all_records)

# === Створення Excel з 3 аркушами ===
excel_path = "final_schedule.xlsx"
with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
    # 1. FlatTable
    df.to_excel(writer, sheet_name="FlatTable", index=False)

    # 2. WeeklyDoctorsView
    for week in sorted(df["Week"].unique()):
        week_df = df[df["Week"] == week]
        pivot = pd.pivot_table(
            week_df,
            index="Doctor",
            columns=["Day", "Shift"],
            values="Cabinet",
            aggfunc="first",
            fill_value=""
        )
        pivot.columns = [f"{['Пн','Вт','Ср','Чт','Пт','Сб'][day-1]} {day}.{shift}" for day, shift in pivot.columns]
        pivot.to_excel(writer, sheet_name=f"Week_{week}", index=True)

    # 3. CabinetMatrix: таблиця по кабінетах
    pivot_cab = pd.pivot_table(
        df,
        index=["Cabinet"],
        columns=["Week", "Day", "Shift"],
        values="Doctor",
        aggfunc="first",
        fill_value=""
    )
    pivot_cab.columns = [
        f"Тиждень {week} {['Пн','Вт','Ср','Чт','Пт','Сб'][day-1]} {day}.{shift}"
        for week, day, shift in pivot_cab.columns
    ]
    pivot_cab.to_excel(writer, sheet_name="CabinetMatrix", index=True)

excel_path