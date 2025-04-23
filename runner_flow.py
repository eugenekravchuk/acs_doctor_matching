import os
import sys
from new_algo.algo_flow import generate_schedule_from_csv

os.makedirs("result", exist_ok=True)

generate_schedule_from_csv("./data/new_data/radiology.csv", "./result/flow_output_schedule.txt")
