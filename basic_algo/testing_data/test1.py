students = {
    "Alice", "Bob", "Charlie", "David", "Eve", "Frank", "Grace", "Hannah", "Ivy", "Jack",
    "Kathy", "Liam", "Mason", "Nina", "Olivia", "Paul", "Quinn", "Rita", "Sam", "Tom"
}
lecturers_projects = {
    "ProfA": {"Proj1", "Proj2", "Proj3", "Proj4", "Proj5"},
    "ProfB": {"Proj6", "Proj7", "Proj8", "Proj9"},
    "ProfC": {"Proj10", "Proj11", "Proj12"},
    "ProfD": {"Proj13", "Proj14", "Proj15"}
}
preferences = {
    "Alice": ("Proj1", "Proj2", "Proj3", "Proj4", "Proj5", "Proj6", "Proj7", "Proj8", "Proj9", "Proj10", "Proj11", "Proj12", "Proj13", "Proj14", "Proj15"),
    "Bob": ("Proj1", "Proj2", "Proj3", "Proj4", "Proj5", "Proj6", "Proj7", "Proj8", "Proj9", "Proj10", "Proj11", "Proj12", "Proj13", "Proj14", "Proj15"),
    "Charlie": ("Proj2", "Proj3", "Proj4", "Proj5", "Proj6", "Proj7", "Proj8", "Proj9", "Proj10", "Proj11", "Proj12", "Proj13", "Proj14", "Proj15", "Proj1"),
    "David": ("Proj3", "Proj4", "Proj5", "Proj6", "Proj7", "Proj8", "Proj9", "Proj10", "Proj11", "Proj12", "Proj13", "Proj14", "Proj15", "Proj1", "Proj2"),
    "Eve": ("Proj4", "Proj5", "Proj6", "Proj7", "Proj8", "Proj9", "Proj10", "Proj11", "Proj12", "Proj13", "Proj14", "Proj15", "Proj1", "Proj2", "Proj3"),
    "Frank": ("Proj5", "Proj6", "Proj7", "Proj8", "Proj9", "Proj10", "Proj11", "Proj12", "Proj13", "Proj14", "Proj15", "Proj1", "Proj2", "Proj3", "Proj4"),
    "Grace": ("Proj6", "Proj7", "Proj8", "Proj9", "Proj10", "Proj11", "Proj12", "Proj13", "Proj14", "Proj15", "Proj1", "Proj2", "Proj3", "Proj4", "Proj5"),
    "Hannah": ("Proj7", "Proj8", "Proj9", "Proj10", "Proj11", "Proj12", "Proj13", "Proj14", "Proj15", "Proj1", "Proj2", "Proj3", "Proj4", "Proj5", "Proj6"),
    "Ivy": ("Proj8", "Proj9", "Proj10", "Proj11", "Proj12", "Proj13", "Proj14", "Proj15", "Proj1", "Proj2", "Proj3", "Proj4", "Proj5", "Proj6", "Proj7"),
    "Jack": ("Proj9", "Proj10", "Proj11", "Proj12", "Proj13", "Proj14", "Proj15", "Proj1", "Proj2", "Proj3", "Proj4", "Proj5", "Proj6", "Proj7", "Proj8"),
    "Kathy": ("Proj10", "Proj11", "Proj12", "Proj13", "Proj14", "Proj15", "Proj1", "Proj2", "Proj3", "Proj4", "Proj5", "Proj6", "Proj7", "Proj8", "Proj9"),
    "Liam": ("Proj11", "Proj12", "Proj13", "Proj14", "Proj15", "Proj1", "Proj2", "Proj3", "Proj4", "Proj5", "Proj6", "Proj7", "Proj8", "Proj9", "Proj10"),
    "Mason": ("Proj12", "Proj13", "Proj14", "Proj15", "Proj1", "Proj2", "Proj3", "Proj4", "Proj5", "Proj6", "Proj7", "Proj8", "Proj9", "Proj10", "Proj11"),
    "Nina": ("Proj13", "Proj14", "Proj15", "Proj1", "Proj2", "Proj3", "Proj4", "Proj5", "Proj6", "Proj7", "Proj8", "Proj9", "Proj10", "Proj11", "Proj12"),
    "Olivia": ("Proj14", "Proj15", "Proj1", "Proj2", "Proj3", "Proj4", "Proj5", "Proj6", "Proj7", "Proj8", "Proj9", "Proj10", "Proj11", "Proj12", "Proj13"),
    "Paul": ("Proj15", "Proj1", "Proj2", "Proj3", "Proj4", "Proj5", "Proj6", "Proj7", "Proj8", "Proj9", "Proj10", "Proj11", "Proj12", "Proj13", "Proj14"),
    "Quinn": ("Proj1", "Proj2", "Proj3", "Proj4", "Proj5", "Proj6", "Proj7", "Proj8", "Proj9", "Proj10", "Proj11", "Proj12", "Proj13", "Proj14", "Proj15"),
    "Rita": ("Proj2", "Proj3", "Proj4", "Proj5", "Proj6", "Proj7", "Proj8", "Proj9", "Proj10", "Proj11", "Proj12", "Proj13", "Proj14", "Proj15", "Proj1"),
    "Sam": ("Proj3", "Proj4", "Proj5", "Proj6", "Proj7", "Proj8", "Proj9", "Proj10", "Proj11", "Proj12", "Proj13", "Proj14", "Proj15", "Proj1", "Proj2"),
    "Tom": ("Proj4", "Proj5", "Proj6", "Proj7", "Proj8", "Proj9", "Proj10", "Proj11", "Proj12", "Proj13", "Proj14", "Proj15", "Proj1", "Proj2", "Proj3")
}
project_capacities = {
    "Proj1": 5, "Proj2": 4, "Proj3": 4, "Proj4": 4, "Proj5": 3, "Proj6": 3, "Proj7": 2, "Proj8": 2, "Proj9": 2, 
    "Proj10": 2, "Proj11": 2, "Proj12": 2, "Proj13": 2, "Proj14": 1, "Proj15": 1
}
lecturer_capacities = {
    "ProfA": 6, "ProfB": 5, "ProfC": 4, "ProfD": 3
}

if __name__ == "__main__":
    import sys
    import os

    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    from algo import SPA, greedy_max_spa

    spa_instance = SPA(students, lecturers_projects, preferences, project_capacities, lecturer_capacities)
    result = greedy_max_spa(spa_instance)
    
    print("Matching Result:", result)
