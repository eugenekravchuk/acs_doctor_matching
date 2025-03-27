import pandas as pd
from collections import defaultdict

# Завантаження даних
doctors_df = pd.read_csv('doctors.csv')
shifts_df = pd.read_csv('shifts.csv')

# Обробка лікарів
class Doctor:
    def __init__(self, id, specializations, preferences):
        self.id = id
        self.specializations = set(specializations.split(';'))
        self.preferences = eval(preferences)  # Очікується dict: {(location, shift): score}
        self.assigned_shifts = []
    
    def is_available(self, new_shift):
        return all(s['time'] != new_shift['time'] for s in self.assigned_shifts)

# Побудова словників
doctors = {}
for _, row in doctors_df.iterrows():
    doctors[row['id']] = Doctor(row['id'], row['specializations'], row['preferences'])

# Підготовка варіантів
available_shifts = []
for _, row in shifts_df.iterrows():
    available_shifts.append({
        'id': row['id'],
        'location': row['location'],
        'time': row['time'],
        'specialization': row['specialization'],
        'assigned_to': None
    })

# Індексація змін за спеціалізацією
shifts_by_spec = defaultdict(list)
for shift in available_shifts:
    shifts_by_spec[shift['specialization']].append(shift)

# Основний алгоритм
active_specializations = set(shifts_by_spec.keys())
while active_specializations:
    for spec in list(active_specializations):
        spec_doctors = [d for d in doctors.values() if spec in d.specializations]
        spec_shifts = [s for s in shifts_by_spec[spec] if s['assigned_to'] is None]
        
        if not spec_shifts:
            active_specializations.remove(spec)
            continue

        for doc in spec_doctors:
            # Знайти пріоритетні shift-и
            sorted_options = sorted(
                spec_shifts,
                key=lambda s: doc.preferences.get((s['location'], s['time']), float('inf'))
            )
            for option in sorted_options:
                if doc.is_available(option):
                    option['assigned_to'] = doc.id
                    doc.assigned_shifts.append(option)
                    break

        # Якщо кількість лікарів = кількість змін — "закриваємо" підзадачу
        if len([s for s in spec_shifts if s['assigned_to'] is not None]) >= len(spec_shifts):
            active_specializations.remove(spec)

# Вивід результату
for doc in doctors.values():
    print(f"Doctor {doc.id} assigned to shifts:")
    for s in doc.assigned_shifts:
        print(f"  - {s['location']} @ {s['time']} for {s['specialization']} (Shift ID: {s['id']})")
