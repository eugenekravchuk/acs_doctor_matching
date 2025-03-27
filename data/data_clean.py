import pandas as pd
input_file = "Лікарі_київ.xlsx"
df = pd.read_excel(input_file, sheet_name=0)
df.columns = ["address", "specialty", "room", "doctor"]


df = df.dropna(subset=["doctor", "specialty", "room"])
doctor_specialties = df.groupby("doctor")["specialty"].unique().reset_index()
doctor_specialties["specialty"] = doctor_specialties["specialty"].apply(list)
room_specialties = df.groupby("room")["specialty"].unique().reset_index()
room_specialties["specialty"] = room_specialties["specialty"].apply(list)

doctor_specialties.to_csv("doctors_specialties.csv", index=False)
room_specialties.to_csv("rooms_specialties.csv", index=False)

