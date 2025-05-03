import pandas as pd
import networkx as nx
import itertools
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from maximum_flow_impl import custom_maximum_flow

def generate_schedule_from_csv(input_csv_path: str, output_path: str = "./rozklad_optimized.txt") -> str:
    df = pd.read_csv(input_csv_path)
    weeks, days, shifts = range(1, 5), range(1, 8), range(1, 3)
    all_shift_ids = [f"{w}.{d}.{s}" for w, d, s in itertools.product(weeks, days, shifts)]

    def split_cabinets(cab_str):
        parts = []
        for c in str(cab_str).split(','):
            parts.append(c.strip())
        return parts

    G = nx.DiGraph()
    source, sink = 'S', 'T'
    G.add_node(source)
    G.add_node(sink)

    cabinet_shift_nodes = []
    cabinet_set = set()
    for row in df['Cabinets']:
        cabinet_set.update(split_cabinets(row))
    cabinet_list = sorted(cabinet_set)

    for cab in cabinet_list:
        for shift in all_shift_ids:
            node = f"{cab}|{shift}"
            G.add_edge(node, sink, capacity=1)
            cabinet_shift_nodes.append((cab, shift, node))  

    for _, row in df.iterrows():
        doctor = row['Doctor']
        doctor_node = f"D|{doctor}"
        max_shifts = int(row['MaxShifts']) if pd.notna(row['MaxShifts']) else len(all_shift_ids)
        G.add_edge(source, doctor_node, capacity=max_shifts)

        possible_cabs = split_cabinets(row['Cabinets'])
        forbidden = set(map(str.strip, str(row['ForbiddenShifts']).split(','))) if pd.notna(row['ForbiddenShifts']) else set()

        for shift in all_shift_ids:
            d_shift_node = f"{doctor}|{shift}"
            G.add_edge(doctor_node, d_shift_node, capacity=1)

            for cab, shift_id, node in cabinet_shift_nodes:
                if shift_id == shift and cab in possible_cabs and shift not in forbidden:
                    G.add_edge(d_shift_node, node, capacity=1)

    flow_value, flow_dict = custom_maximum_flow(G, source, sink)

    for _, row in df.iterrows():
        doctor = row['Doctor']
        min_required = int(row['MinShifts']) if pd.notna(row.get('MinShifts')) else 0
        doctor_node = f"D|{doctor}"
        assigned_shifts = sum(flow_dict.get(doctor_node, {}).values())
        if assigned_shifts < min_required:
            print(f"Лікар {doctor} має лише {assigned_shifts} змін (мінімум: {min_required})")

    schedule = {cab: {} for cab in cabinet_list}
    for doctor in df['Doctor']:
        for shift in all_shift_ids:
            d_shift_node = f"{doctor}|{shift}"
            doctor_node = f"D|{doctor}"
            if doctor_node in flow_dict and d_shift_node in flow_dict[doctor_node]:
                for target, f in flow_dict[d_shift_node].items():
                    if f > 0 and '|' in target:
                        cab, shift_id = target.split('|')
                        schedule[cab][shift_id] = doctor


    with open(output_path, "w", encoding="utf-8") as f:
        for cab in cabinet_list:
            f.write(f"{cab}:\n")
            for shift in sorted(all_shift_ids, key=lambda x: list(map(int, x.split('.')))):
                assigned = schedule[cab].get(shift, "Немає лікаря")
                f.write(f"{shift} - {assigned}\n")
            f.write("\n")
