import pandas as pd
import networkx as nx
import itertools
import sys
import os
import json 

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from maximum_flow_impl import custom_maximum_flow, min_cost_max_flow

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


def generate_preference_schedule_from_csv(input_csv_path: str, loc_cabs_path: str, output_path: str = "./rozklad_optimized.txt") -> str:
    df = pd.read_csv(input_csv_path)
    weeks, days, shifts = range(1, 5), range(1, 8), range(1, 3)
    all_shift_ids = [f"{d}.{s}" for d, s in itertools.product(days, shifts)]

    def split_data(data_str):
        parts = []
        for c in str(data_str).split(','):
            parts.append(c.strip())
        return parts

    with open(loc_cabs_path, 'r', encoding='utf-8') as f:
        loc_cabs_data = json.load(f)
        loc_cabs_dict = {}

        for elem in loc_cabs_data:
            loc = elem['location']
            cabinets = elem['room']
            spec = elem['specialization']
            if not loc in loc_cabs_dict:
                loc_cabs_dict[loc] = {}

            loc_cabs_dict[loc][spec] = split_data(cabinets)

    G = nx.DiGraph()
    source, sink = 'S', 'T'
    G.add_node(source)
    G.add_node(sink)

    for _, row in df.iterrows():

        doctor = row['Лікар']
        specs = split_data(row['Спеціалізація'])
        locs = split_data(row['Кабінети'])
        doctor_node = f"D|{doctor}"
        max_shifts = int(row['Максимальна клк змін']) if pd.notna(row['Максимальна клк змін']) else len(all_shift_ids)
        forbidden = set(split_data(row['Неможливі зміни'])) if pd.notna(row['Неможливі зміни']) else set()
        #TODO: necessary shifts
        #TODO: min shifts

        G.add_edge(source, doctor_node, capacity=max_shifts)

        for loc in locs:
            for spec in specs:
                if loc in loc_cabs_dict and spec in loc_cabs_dict[loc]:
                    for cab in loc_cabs_dict[loc][spec]:
                        for shift in all_shift_ids:
                            if shift in forbidden:
                                continue
                            d_shift_node = f"{doctor}|{shift}"
                            G.add_edge(doctor_node, d_shift_node, capacity=1)
                            node = f"{loc}|{cab}|{shift}"
                            G.add_edge(d_shift_node, node, capacity=1, cost=3*locs.index(loc) + 1)
                            G.add_edge(node, sink, capacity=1)

    _, total_cost, flow_dict = min_cost_max_flow(G, source, sink)

    for _, row in df.iterrows():
        doctor = row['Лікар']
        min_required = int(row['Мінімальна клк змін']) if pd.notna(row.get('Мінімальна клк змін')) else 0
        doctor_node = f"D|{doctor}"
        assigned_shifts = sum(flow_dict.get(doctor_node, {}).values())
        if assigned_shifts < min_required:
            print(f"Лікар {doctor} має лише {assigned_shifts} змін (мінімум: {min_required})")

    schedule = {}
    for doctor in df['Лікар']:
        doctor_node = f"D|{doctor}"
        if doctor_node not in flow_dict:
            continue
        
        for target, flow in flow_dict[doctor_node].items():
            if flow > 0 and '|' in target:
                d_shift_node = target
                for loc_cab_node, flow_value in flow_dict.get(d_shift_node, {}).items():
                    if flow_value > 0 and '|' in loc_cab_node:
                        loc, cab, shift = loc_cab_node.split('|')
                        
                        if loc not in schedule:
                            schedule[loc] = {}
                        if cab not in schedule[loc]:
                            schedule[loc][cab] = {}
                        
                        schedule[loc][cab][shift] = doctor

    with open(output_path, "w", encoding="utf-8") as f:
        for loc in sorted(schedule.keys()):
            f.write(f"Локація: {loc}\n")
            f.write("="*40 + "\n")
            
            for cab in sorted(schedule[loc].keys()):
                f.write(f"Кабінет: {cab}\n")
                f.write("-"*30 + "\n")
                
                for shift in sorted(all_shift_ids, key=lambda x: list(map(int, x.split('.')))):
                    assigned = schedule[loc][cab].get(shift, "Немає лікаря")
                    f.write(f"{shift} - {assigned}\n")
                
                f.write("\n")
            
            f.write("\n")
        
        f.write(f"Загальна вартість розкладу: {total_cost}\n")
    
    return output_path

print(generate_preference_schedule_from_csv(
    "C:\\Users\\Admin\\Desktop\\AKS\\Project\\acs_doctor_matching\\data\\new_data\\loc_data_with_specializations.csv",
    "C:\\Users\\Admin\\Desktop\\AKS\\Project\\acs_doctor_matching\\data\\new_data\\rooms_locations_updated.json",
    "C:\\Users\\Admin\\Desktop\\AKS\\Project\\acs_doctor_matching\\result\\output.txt"
))

