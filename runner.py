import os
import sys
from gale_shapley_algo.algo import run_scheduler

NUM_ITERATIONS = 100
best_happiness = -1
best_file = None

os.makedirs("result", exist_ok=True)

def print_progress_bar(iteration, total, prefix='', length=50):
    percent = f"{100 * (iteration / total):.1f}"
    filled_length = int(length * iteration // total)
    bar = '█' * filled_length + '-' * (length - filled_length)
    print(f'\r{prefix} |{bar}| {percent}% Complete', end='\r')
    if iteration == total:
        print()

for i in range(NUM_ITERATIONS):
    output_file = f"result/output_{i}.txt"
    happiness = run_scheduler(
        "./data/doctors_schedule_160.csv",
        "./data/doctors_160.csv",
        "./data/rooms_80.csv",
        output_file
    )

    if happiness > best_happiness:
        best_happiness = happiness
        best_file = output_file

    print_progress_bar(i + 1, NUM_ITERATIONS, prefix='Optimizing schedules')

for i in range(NUM_ITERATIONS):
    fname = f"result/output_{i}.txt"
    if fname != best_file and os.path.exists(fname):
        os.remove(fname)

final_name = "result/final_schedule.txt"
if os.path.exists(best_file):
    os.rename(best_file, final_name)

print(f"\nBest schedule: {final_name} with happiness = {best_happiness:.4f}")
