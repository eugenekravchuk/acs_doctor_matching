students = {
    "Alice", "Bob", "Charlie", "David", "Emma", "Frank", "Grace", "Hannah", "Isaac", "Jack",
    "Katherine", "Liam", "Mia", "Nathan", "Olivia", "Peter", "Quinn", "Rachel", "Samuel", "Tina",
    "Umar", "Victor", "Wendy", "Xander", "Yasmine", "Zack", "Adam", "Bella", "Chris", "Diana",
    "Ethan", "Fiona", "George", "Helen", "Ian", "Julia", "Kevin", "Laura", "Mike", "Nancy",
    "Oscar", "Paul", "Rita", "Steve", "Tracy", "Ursula", "Vincent", "Walter", "Xenia", "Yvonne"
}

projects = {f"Proj_{i}" for i in range(1, 11)}

lecturers_projects = {
    "Prof_A": {"Proj_1", "Proj_2", "Proj_3"},
    "Prof_B": {"Proj_4", "Proj_5", "Proj_6"},
    "Prof_C": {"Proj_7", "Proj_8", "Proj_9"},
    "Prof_D": {"Proj_10"},
    "Prof_K": {"Proj_1", "Proj_4", "Proj_7"},
    "Prof_L": {"Proj_10"},
    "Prof_N": {"Proj_2", "Proj_5"},
    "Prof_O": {"Proj_8"}
}

preferences = {
    "Alice": ("Proj_1", "Proj_2", "Proj_3", "Proj_4", "Proj_5", "Proj_6", "Proj_7", "Proj_8", "Proj_9", "Proj_10"),
    "Bob": ("Proj_2", "Proj_1", "Proj_3", "Proj_4", "Proj_5", "Proj_6", "Proj_7", "Proj_8", "Proj_9", "Proj_10"),
    "Charlie": ("Proj_3", "Proj_1", "Proj_2", "Proj_4", "Proj_5", "Proj_6", "Proj_7", "Proj_8", "Proj_9", "Proj_10"),
    "David": ("Proj_4", "Proj_1", "Proj_2", "Proj_3", "Proj_5", "Proj_6", "Proj_7", "Proj_8", "Proj_9", "Proj_10"),
    "Emma": ("Proj_5", "Proj_1", "Proj_2", "Proj_3", "Proj_4", "Proj_6", "Proj_7", "Proj_8", "Proj_9", "Proj_10"),
    "Frank": ("Proj_6", "Proj_1", "Proj_2", "Proj_3", "Proj_4", "Proj_5", "Proj_7", "Proj_8", "Proj_9", "Proj_10"),
    "Grace": ("Proj_7", "Proj_1", "Proj_2", "Proj_3", "Proj_4", "Proj_5", "Proj_6", "Proj_8", "Proj_9", "Proj_10"),
    "Hannah": ("Proj_8", "Proj_1", "Proj_2", "Proj_3", "Proj_4", "Proj_5", "Proj_6", "Proj_7", "Proj_9", "Proj_10"),
    "Isaac": ("Proj_9", "Proj_1", "Proj_2", "Proj_3", "Proj_4", "Proj_5", "Proj_6", "Proj_7", "Proj_8", "Proj_10"),
    "Jack": ("Proj_10", "Proj_1", "Proj_2", "Proj_3", "Proj_4", "Proj_5", "Proj_6", "Proj_7", "Proj_8", "Proj_9"),
    "Katherine": ("Proj_1", "Proj_3", "Proj_2", "Proj_4", "Proj_5", "Proj_6", "Proj_7", "Proj_8", "Proj_9", "Proj_10"),
    "Liam": ("Proj_2", "Proj_1", "Proj_3", "Proj_4", "Proj_5", "Proj_6", "Proj_7", "Proj_8", "Proj_9", "Proj_10"),
    "Mia": ("Proj_3", "Proj_1", "Proj_2", "Proj_4", "Proj_5", "Proj_6", "Proj_7", "Proj_8", "Proj_9", "Proj_10"),
    "Nathan": ("Proj_4", "Proj_1", "Proj_2", "Proj_3", "Proj_5", "Proj_6", "Proj_7", "Proj_8", "Proj_9", "Proj_10"),
    "Olivia": ("Proj_5", "Proj_1", "Proj_2", "Proj_3", "Proj_4", "Proj_6", "Proj_7", "Proj_8", "Proj_9", "Proj_10"),
    "Peter": ("Proj_6", "Proj_1", "Proj_2", "Proj_3", "Proj_4", "Proj_5", "Proj_7", "Proj_8", "Proj_9", "Proj_10"),
    "Quinn": ("Proj_7", "Proj_1", "Proj_2", "Proj_3", "Proj_4", "Proj_5", "Proj_6", "Proj_8", "Proj_9", "Proj_10"),
    "Rachel": ("Proj_8", "Proj_1", "Proj_2", "Proj_3", "Proj_4", "Proj_5", "Proj_6", "Proj_7", "Proj_9", "Proj_10"),
    "Samuel": ("Proj_9", "Proj_1", "Proj_2", "Proj_3", "Proj_4", "Proj_5", "Proj_6", "Proj_7", "Proj_8", "Proj_10"),
    "Tina": ("Proj_10", "Proj_1", "Proj_2", "Proj_3", "Proj_4", "Proj_5", "Proj_6", "Proj_7", "Proj_8", "Proj_9"),
    "Umar": ("Proj_1", "Proj_2", "Proj_3", "Proj_4", "Proj_5", "Proj_6", "Proj_7", "Proj_8", "Proj_9", "Proj_10"),
    "Victor": ("Proj_2", "Proj_1", "Proj_3", "Proj_4", "Proj_5", "Proj_6", "Proj_7", "Proj_8", "Proj_9", "Proj_10"),
    "Wendy": ("Proj_3", "Proj_1", "Proj_2", "Proj_4", "Proj_5", "Proj_6", "Proj_7", "Proj_8", "Proj_9", "Proj_10"),
    "Xander": ("Proj_4", "Proj_1", "Proj_2", "Proj_3", "Proj_5", "Proj_6", "Proj_7", "Proj_8", "Proj_9", "Proj_10"),
    "Yasmine": ("Proj_5", "Proj_1", "Proj_2", "Proj_3", "Proj_4", "Proj_6", "Proj_7", "Proj_8", "Proj_9", "Proj_10"),
    "Zack": ("Proj_6", "Proj_1", "Proj_2", "Proj_3", "Proj_4", "Proj_5", "Proj_7", "Proj_8", "Proj_9", "Proj_10"),
    "Adam": ("Proj_7", "Proj_1", "Proj_2", "Proj_3", "Proj_4", "Proj_5", "Proj_6", "Proj_8", "Proj_9", "Proj_10"),
    "Bella": ("Proj_8", "Proj_1", "Proj_2", "Proj_3", "Proj_4", "Proj_5", "Proj_6", "Proj_7", "Proj_9", "Proj_10"),
    "Chris": ("Proj_9", "Proj_1", "Proj_2", "Proj_3", "Proj_4", "Proj_5", "Proj_6", "Proj_7", "Proj_8", "Proj_10"),
    "Diana": ("Proj_10", "Proj_1", "Proj_2", "Proj_3", "Proj_4", "Proj_5", "Proj_6", "Proj_7", "Proj_8", "Proj_9"),
    "Ethan": ("Proj_1", "Proj_2", "Proj_3", "Proj_4", "Proj_5", "Proj_6", "Proj_7", "Proj_8", "Proj_9", "Proj_10"),
    "Fiona": ("Proj_2", "Proj_1", "Proj_3", "Proj_4", "Proj_5", "Proj_6", "Proj_7", "Proj_8", "Proj_9", "Proj_10"),
    "George": ("Proj_3", "Proj_1", "Proj_2", "Proj_4", "Proj_5", "Proj_6", "Proj_7", "Proj_8", "Proj_9", "Proj_10"),
    "Helen": ("Proj_4", "Proj_1", "Proj_2", "Proj_3", "Proj_5", "Proj_6", "Proj_7", "Proj_8", "Proj_9", "Proj_10"),
    "Ian": ("Proj_5", "Proj_1", "Proj_2", "Proj_3", "Proj_4", "Proj_6", "Proj_7", "Proj_8", "Proj_9", "Proj_10"),
    "Julia": ("Proj_6", "Proj_1", "Proj_2", "Proj_3", "Proj_4", "Proj_5", "Proj_7", "Proj_8", "Proj_9", "Proj_10"),
    "Kevin": ("Proj_7", "Proj_1", "Proj_2", "Proj_3", "Proj_4", "Proj_5", "Proj_6", "Proj_8", "Proj_9", "Proj_10"),
    "Laura": ("Proj_8", "Proj_1", "Proj_2", "Proj_3", "Proj_4", "Proj_5", "Proj_6", "Proj_7", "Proj_9", "Proj_10"),
    "Mike": ("Proj_9", "Proj_1", "Proj_2", "Proj_3", "Proj_4", "Proj_5", "Proj_6", "Proj_7", "Proj_8", "Proj_10"),
    "Nancy": ("Proj_10", "Proj_1", "Proj_2", "Proj_3", "Proj_4", "Proj_5", "Proj_6", "Proj_7", "Proj_8", "Proj_9"),
    "Oscar": ("Proj_1", "Proj_2", "Proj_3", "Proj_4", "Proj_5", "Proj_6", "Proj_7", "Proj_8", "Proj_9", "Proj_10"),
    "Paul": ("Proj_2", "Proj_1", "Proj_3", "Proj_4", "Proj_5", "Proj_6", "Proj_7", "Proj_8", "Proj_9", "Proj_10"),
    "Rita": ("Proj_3", "Proj_1", "Proj_2", "Proj_4", "Proj_5", "Proj_6", "Proj_7", "Proj_8", "Proj_9", "Proj_10"),
    "Steve": ("Proj_4", "Proj_1", "Proj_2", "Proj_3", "Proj_5", "Proj_6", "Proj_7", "Proj_8", "Proj_9", "Proj_10"),
    "Tracy": ("Proj_5", "Proj_1", "Proj_2", "Proj_3", "Proj_4", "Proj_6", "Proj_7", "Proj_8", "Proj_9", "Proj_10"),
    "Ursula": ("Proj_6", "Proj_1", "Proj_2", "Proj_3", "Proj_4", "Proj_5", "Proj_7", "Proj_8", "Proj_9", "Proj_10"),
    "Vincent": ("Proj_7", "Proj_1", "Proj_2", "Proj_3", "Proj_4", "Proj_5", "Proj_6", "Proj_8", "Proj_9", "Proj_10"),
    "Walter": ("Proj_8", "Proj_1", "Proj_2", "Proj_3", "Proj_4", "Proj_5", "Proj_6", "Proj_7", "Proj_9", "Proj_10"),
    "Xenia": ("Proj_9", "Proj_1", "Proj_2", "Proj_3", "Proj_4", "Proj_5", "Proj_6", "Proj_7", "Proj_8", "Proj_10"),
    "Yvonne": ("Proj_10", "Proj_1", "Proj_2", "Proj_3", "Proj_4", "Proj_5", "Proj_6", "Proj_7", "Proj_8", "Proj_9")
}

project_capacities = {f"Proj_{i}": 6 for i in range(1, 11)}

lecturer_capacities = {
    "Prof_A": 21, "Prof_B": 21, "Prof_C": 21, "Prof_D": 7,
    "Prof_K": 21, "Prof_L": 6, "Prof_N": 14, "Prof_O": 10
}

if __name__ == "__main__":
    import sys
    import os

    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    from algo import SPA, greedy_max_spa

    spa_instance = SPA(students, lecturers_projects, preferences, project_capacities, lecturer_capacities)
    result = greedy_max_spa(spa_instance)
    
    print("Matching Result:", result)
