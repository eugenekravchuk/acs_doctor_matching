import pandas as pd
import itertools
from collections import defaultdict
import random
from io import StringIO

# Вхідні дані як CSV-строка
data = """
Лікар,Кабінети,Мінімальна клк змін,Максимальна клк змін,Неможливі зміни,Обов'язкові зміни
Іващик О. М.,"110, 131",0,,"4.1.1, 4.1.2, 4.2.1, 4.2.2","1.1.1, 1.2.1"
Бур'янова К. І.,"101, 141, 212",0,,"1.1.1, 1.1.2",
Варшавська Л. В.,"105, 105А, 110A, 110, 131",0,,,
Вдовенко О. В.,"110, 131",0,,,"1.1.1, 1.2.1"
Горбкова О. І.,"105, 105А, 107, 108",0,,,
Древич І.Р,"143",0,,,
Древич І.Р.,"110, 143",0,,,
Коваль А. М.,"101, 141, 110, 131",0,,,
Козак Р.П.,"106, 143",0,,"1.1.1, 1.3.1,1.5.1",
Козак Я. Р.,"110, 131",0,,"2.1.1, 2.1.2, 3.1.1, 3.1.2",
Кутянський В.С.,"101, 141",0,,,
Мацько (Опришко) А. Ю.,"105, 105А, 107, 108",0,,,
Олексяк К. І.,"143, 110",0,,,
Паламарчук Ю. О.,"110, 131",0,,,
Петруха Г. Ю.,"105, 105А, 107, 108",0,,,"1.1.1, 1.3.1,1.5.1"
Петруха Х. Ю.,"106, 143",0,,,
Предземірська О. В.,"131, 143A, 143, 131",0,,,
Ступницька Н. Д.,"106, 143A, 143",0,,,
Шелемех А. Я.,"101, 141",0,,,
"""

df = pd.read_csv(StringIO(data))

# Формуємо список усіх змін
weeks = range(1, 5)
days = range(1, 8)
shifts = range(1, 3)
all_shifts = [f"{w}.{d}.{s}" for w, d, s in itertools.product(weeks, days, shifts)]

# Розклад: {кабінет: {зміна: лікар}}
schedule = defaultdict(dict)
doctor_assignments = defaultdict(list)

# Створимо список усіх унікальних кабінетів
cabinet_set = set()
for cabs in df['Кабінети']:
    for c in str(cabs).split(','):
        cabinet_set.add(c.strip())

cabinet_list = sorted(cabinet_set)

# Допоміжна функція для розкладу
def can_assign(doctor_row, shift_code):
    if pd.notna(doctor_row['Неможливі зміни']):
        if shift_code in map(str.strip, str(doctor_row['Неможливі зміни']).split(',')):
            return False
    return True

# Призначаємо обов'язкові зміни
for _, row in df.iterrows():
    name = row['Лікар']
    if pd.notna(row["Обов'язкові зміни"]):
        for shift_code in map(str.strip, row["Обов'язкові зміни"].split(',')):
            for cab in str(row["Кабінети"]).split(','):
                cab = cab.strip()
                if shift_code not in schedule[cab]:
                    schedule[cab][shift_code] = name
                    doctor_assignments[name].append(shift_code)
                    break

def doctor_is_free(name, shift_code):
    return shift_code not in doctor_assignments[name]

# Призначення решти змін випадково
for cab in cabinet_list:
    for shift in all_shifts:
        if shift in schedule[cab]:
            continue
        rows = list(df.iterrows())
        candidates = []
        for _, row in df.iterrows():
            name = row['Лікар']
            if cab in str(row["Кабінети"]) and can_assign(row, shift) and doctor_is_free(name, shift):
                max_shifts = row['Максимальна клк змін']
                if pd.isna(max_shifts) or len(doctor_assignments[name]) < int(max_shifts):
                    candidates.append(name)
        if candidates:
            chosen = random.choice(candidates)  # або candidates[0] для deterministic
            schedule[cab][shift] = chosen
            doctor_assignments[chosen].append(shift)
        else:
            schedule[cab][shift] = "Немає лікаря"


# Формуємо текстовий результат
output_lines = []
for cab in cabinet_list:
    output_lines.append(f"{cab}:")
    for shift in sorted(schedule[cab].keys(), key=lambda x: list(map(int, x.split('.')))):
        output_lines.append(f"{shift} - {schedule[cab][shift]}")
    output_lines.append("")

# Запис у файл
output_path = "./rozklad_likariv.txt"
with open(output_path, "w", encoding="utf-8") as f:
    f.write("\n".join(output_lines))

count_empty = sum(
    1 for cab in schedule for shift, doc in schedule[cab].items() if doc == "Немає лікаря"
)
print("Кількість змін без лікаря:", count_empty)
