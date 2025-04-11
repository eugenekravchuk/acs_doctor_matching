students = {
    "Alice", "Bob", "Charlie", "David", "Eve", "Frank", "Grace", "Hannah", "Ivy", "Jack", 
    "Kathy", "Liam", "Mason", "Nina", "Olivia", "Paul", "Quinn", "Rita", "Sam", "Tom",
    "Ursula", "Vera", "Wendy", "Xander", "Yara", "Zoe"
}
lecturers_projects = {
    "ProfA": {"Proj1", "Proj2", "Proj3", "Proj4"},
    "ProfB": {"Proj5", "Proj6", "Proj7"},
    "ProfC": {"Proj8", "Proj9", "Proj10"},
    "ProfD": {"Proj11", "Proj12"},
    "ProfE": {"Proj13"}
}
preferences = {
    "Alice": ("Proj1", "Proj2", "Proj3", "Proj4", "Proj5", "Proj6", "Proj7", "Proj8", "Proj9", "Proj10", "Proj11", "Proj12", "Proj13"),
    "Bob": ("Proj2", "Proj3", "Proj4", "Proj5", "Proj6", "Proj7", "Proj8", "Proj9", "Proj10", "Proj11", "Proj12", "Proj13", "Proj1"),
    "Charlie": ("Proj3", "Proj4", "Proj5", "Proj6", "Proj7", "Proj8", "Proj9", "Proj10", "Proj11", "Proj12", "Proj13", "Proj1", "Proj2"),
    "David": ("Proj4", "Proj5", "Proj6", "Proj7", "Proj8", "Proj9", "Proj10", "Proj11", "Proj12", "Proj13", "Proj1", "Proj2", "Proj3"),
    "Eve": ("Proj5", "Proj6", "Proj7", "Proj8", "Proj9", "Proj10", "Proj11", "Proj12", "Proj13", "Proj1", "Proj2", "Proj3", "Proj4"),
    "Frank": ("Proj6", "Proj7", "Proj8", "Proj9", "Proj10", "Proj11", "Proj12", "Proj13", "Proj1", "Proj2", "Proj3", "Proj4", "Proj5"),
    "Grace": ("Proj7", "Proj8", "Proj9", "Proj10", "Proj11", "Proj12", "Proj13", "Proj1", "Proj2", "Proj3", "Proj4", "Proj5", "Proj6"),
    "Hannah": ("Proj8", "Proj9", "Proj10", "Proj11", "Proj12", "Proj13", "Proj1", "Proj2", "Proj3", "Proj4", "Proj5", "Proj6", "Proj7"),
    "Ivy": ("Proj9", "Proj10", "Proj11", "Proj12", "Proj13", "Proj1", "Proj2", "Proj3", "Proj4", "Proj5", "Proj6", "Proj7", "Proj8"),
    "Jack": ("Proj10", "Proj11", "Proj12", "Proj13", "Proj1", "Proj2", "Proj3", "Proj4", "Proj5", "Proj6", "Proj7", "Proj8", "Proj9"),
    "Kathy": ("Proj11", "Proj12", "Proj13", "Proj1", "Proj2", "Proj3", "Proj4", "Proj5", "Proj6", "Proj7", "Proj8", "Proj9", "Proj10"),
    "Liam": ("Proj12", "Proj13", "Proj1", "Proj2", "Proj3", "Proj4", "Proj5", "Proj6", "Proj7", "Proj8", "Proj9", "Proj10", "Proj11"),
    "Mason": ("Proj13", "Proj1", "Proj2", "Proj3", "Proj4", "Proj5", "Proj6", "Proj7", "Proj8", "Proj9", "Proj10", "Proj11", "Proj12"),
    "Nina": ("Proj1", "Proj2", "Proj3", "Proj4", "Proj5", "Proj6", "Proj7", "Proj8", "Proj9", "Proj10", "Proj11", "Proj12", "Proj13"),
    "Olivia": ("Proj2", "Proj3", "Proj4", "Proj5", "Proj6", "Proj7", "Proj8", "Proj9", "Proj10", "Proj11", "Proj12", "Proj13", "Proj1"),
    "Paul": ("Proj3", "Proj4", "Proj5", "Proj6", "Proj7", "Proj8", "Proj9", "Proj10", "Proj11", "Proj12", "Proj13", "Proj1", "Proj2"),
    "Quinn": ("Proj4", "Proj5", "Proj6", "Proj7", "Proj8", "Proj9", "Proj10", "Proj11", "Proj12", "Proj13", "Proj1", "Proj2", "Proj3"),
    "Rita": ("Proj5", "Proj6", "Proj7", "Proj8", "Proj9", "Proj10", "Proj11", "Proj12", "Proj13", "Proj1", "Proj2", "Proj3", "Proj4"),
    "Sam": ("Proj6", "Proj7", "Proj8", "Proj9", "Proj10", "Proj11", "Proj12", "Proj13", "Proj1", "Proj2", "Proj3", "Proj4", "Proj5"),
    "Tom": ("Proj7", "Proj8", "Proj9", "Proj10", "Proj11", "Proj12", "Proj13", "Proj1", "Proj2", "Proj3", "Proj4", "Proj5", "Proj6"),
    "Ursula": ("Proj8", "Proj9", "Proj10", "Proj11", "Proj12", "Proj13", "Proj1", "Proj2", "Proj3", "Proj4", "Proj5", "Proj6", "Proj7"),
    "Vera": ("Proj9", "Proj10", "Proj11", "Proj12", "Proj13", "Proj1", "Proj2", "Proj3", "Proj4", "Proj5", "Proj6", "Proj7", "Proj8"),
    "Wendy": ("Proj10", "Proj11", "Proj12", "Proj13", "Proj1", "Proj2", "Proj3", "Proj4", "Proj5", "Proj6", "Proj7", "Proj8", "Proj9"),
    "Xander": ("Proj11", "Proj12", "Proj13", "Proj1", "Proj2", "Proj3", "Proj4", "Proj5", "Proj6", "Proj7", "Proj8", "Proj9", "Proj10"),
    "Yara": ("Proj12", "Proj13", "Proj1", "Proj2", "Proj3", "Proj4", "Proj5", "Proj6", "Proj7", "Proj8", "Proj9", "Proj10", "Proj11"),
    "Zoe": ("Proj13", "Proj1", "Proj2", "Proj3", "Proj4", "Proj5", "Proj6", "Proj7", "Proj8", "Proj9", "Proj10", "Proj11", "Proj12")
}
project_capacities = {
    "Proj1": 10, "Proj2": 10, "Proj3": 10, "Proj4": 10, "Proj5": 10, "Proj6": 8, "Proj7": 8, "Proj8": 7, "Proj9": 6,
    "Proj10": 6, "Proj11": 5, "Proj12": 4, "Proj13": 2
}
lecturer_capacities = {
    "ProfA": 6, "ProfB": 5, "ProfC": 4, "ProfD": 3, "ProfE": 2
}

if __name__ == "__main__":
    import sys
    import os

    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    from algo import SPA, greedy_max_spa

    spa_instance = SPA(students, lecturers_projects, preferences, project_capacities, lecturer_capacities)
    result = greedy_max_spa(spa_instance)
    
    print("Matching Result:", result)
