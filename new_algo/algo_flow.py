import pandas as pd
import networkx as nx
import itertools
import sys
import os
import json 

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from maximum_flow_impl import min_cost_max_flow

def generate_preference_schedule_from_csv(input_csv_path: str, loc_cabs_path: str, output_path: str, doctor_penalty: dict, week) -> str:
    df = pd.read_csv(input_csv_path)
    days, shifts = range(1, 8), range(1, 3)
    all_shift_ids = [f"{d}.{s}" for d, s in itertools.product(days, shifts)]
    if doctor_penalty is None:
        doctors = df['Doctor'].unique()
        doctor_penalty = {doctor: 0 for doctor in doctors}


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
    costs = {}
    cabinet_penalty = {}
    necessary_shifts = {}

    for _, row in df.iterrows():

        doctor = row['Doctor']
        costs[doctor] = {}
        specs = split_data(row['Specialization'])
        locs = split_data(row['Cabinets'])
        doctor_node = f"D|{doctor}"
        max_shifts = int(row['MaxShifts']) // 4 if pd.notna(row['MaxShifts']) else len(all_shift_ids) // 4
        min_shifts = int(row['MinShifts']) //4 if pd.notna(row['MinShifts']) else 0
        forbidden = set(split_data(row['ForbiddenShifts'])) if pd.notna(row['ForbiddenShifts']) else set()
        forbidden = set('.'.join(data.split('.')[1:]) for data in forbidden if data[0] == str(week))
        obligatory = split_data(row['RequiredShifts']) if pd.notna(row['RequiredShifts']) else set()
        obligatory = [data.split('|') for data in obligatory if data.split('|')[2][0] == str(week)]
        obligatory = set('|'.join([data[0], data[1], data[2][2:]]) for data in obligatory)
        necessary_shifts[doctor] = obligatory

        G.add_edge(source, doctor_node, capacity=max_shifts)

        for i, loc in enumerate(locs):

            costs[doctor][loc] = 5*i + 1
            if loc not in costs:
                costs[loc] = {}
            costs[loc][doctor] = -costs[doctor][loc]

            for spec in specs:
                if loc in loc_cabs_dict and spec in loc_cabs_dict[loc]:
                    for cab in loc_cabs_dict[loc][spec]:
                        cabinet_penalty[f'{loc}|{cab}'] = 0
                        for shift in all_shift_ids:
                            if shift in forbidden:
                                continue
                            d_shift_node = f"{doctor}|{shift}"
                            G.add_edge(doctor_node, d_shift_node, capacity=1)
                            node = f"{loc}|{cab}|{shift}"
                            G.add_edge(d_shift_node, node, capacity=1)
                            G.add_edge(node, sink, capacity=1)

    _, total_cost, flow_dict = min_cost_max_flow(G, costs, doctor_penalty, cabinet_penalty, necessary_shifts, source, sink)

    schedule = {}
    for doctor in df['Doctor']:
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
    
    return flow_dict

def generate_monthly_schedule_from_csv(input_csv_path: str, loc_cabs_path: str, output_path: str) -> str:
    df = pd.read_csv(input_csv_path)
    doctors = df['Doctor'].unique()
    doctor_penalty = {doctor: 0 for doctor in doctors}
    for week in range(1, 5):
        out_res = output_path + f"week_{week}.txt"
        flow_dict = generate_preference_schedule_from_csv(input_csv_path, loc_cabs_path, out_res, doctor_penalty, week)
        for doctor in doctors:
            doctor_node = f"D|{doctor}"
            assigned_shifts = sum(flow_dict.get(doctor_node, {}).values())
            doctor_penalty[doctor] = assigned_shifts // 2
    
    print('Generated monthly schedule')

# print(generate_monthly_schedule_from_csv(
#     "C:\\Users\\Admin\\Desktop\\AKS\\Project\\acs_doctor_matching\\data\\new_data\\loc_data_with_specializations.csv",
#     "C:\\Users\\Admin\\Desktop\\AKS\\Project\\acs_doctor_matching\\data\\new_data\\rooms_locations_updated.json",
#     "C:\\Users\\Admin\\Desktop\\AKS\\Project\\acs_doctor_matching\\result\\"
# ))
        