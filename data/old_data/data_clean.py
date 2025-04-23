import os
import pandas as pd

input_file = "Лікарі_київ.xlsx"

# === КРОК 1: Зчитування Аркуш1 (перший аркуш) ===
try:
    df_main = pd.read_excel(input_file, sheet_name=0)
    df_main.columns = ["address", "specialty", "room", "doctor"]

    # Очистка
    df_main = df_main.dropna(subset=["doctor", "specialty", "room"])

    # Групування
    doctor_specialties = df_main.groupby("doctor")["specialty"].unique().reset_index()
    doctor_specialties["specialty"] = doctor_specialties["specialty"].apply(list)

    room_specialties = df_main.groupby("room")["specialty"].unique().reset_index()
    room_specialties["specialty"] = room_specialties["specialty"].apply(list)

    # Збереження у CSV
    doctor_specialties.to_csv("doctors_specialties.csv", index=False)
    room_specialties.to_csv("rooms_specialties.csv", index=False)

    print("Збережено doctors_specialties.csv та rooms_specialties.csv")

except Exception as e:
    print(f"Помилка при обробці першого аркуша: {e}")
    exit()


# === КРОК 2: Зчитування рейтингу з аркуша 'r1' ===
try:
    df_rating = pd.read_excel(input_file, sheet_name="r1")

    # Створення папки для експорту
    output_folder = "csv_export"
    os.makedirs(output_folder, exist_ok=True)

    # Збереження
    df_rating.to_csv(os.path.join(output_folder, "rating_table.csv"), index=False)
    print("Збережено csv_export/rating_table.csv")

except Exception as e:
    print(f"Помилка при зчитуванні аркуша r1: {e}")
