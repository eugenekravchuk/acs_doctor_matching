import os
import sys
from new_algo.algo_flow import generate_preference_schedule_from_csv

os.makedirs("result", exist_ok=True)


generate_preference_schedule_from_csv("./data/new_data/loc_data_with_specializations.csv", "./data/new_data/rooms_locations_updated.json", "./result/flow_output_schedule.txt", None, 1)
