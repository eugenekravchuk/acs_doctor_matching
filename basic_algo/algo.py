from copy import deepcopy

class Rank:

    def __init__(self, R: int, start: float = 0):
        self.rank = [start for _ in range(R)]

    def __add__(self, other):
        if isinstance(other, Rank):
            return Rank.from_list([a + b for a, b in zip(self.rank, other.rank)])
        new_rank = self.rank[:]
        new_rank[other-1] += 1
        return Rank.from_list(new_rank)

    def __sub__(self, other):
        if isinstance(other, Rank):
            return Rank.from_list([a - b for a, b in zip(self.rank, other.rank)])
        new_rank = self.rank[:]
        new_rank[other-1] -= 1
        return Rank.from_list(new_rank)

    def __gt__(self, other):
        return self.rank > other.rank

    def __lt__(self, other):
        return self.rank < other.rank

    def __eq__(self, other):
        return self.rank == other.rank

    def __ne__(self, other):
        return self.rank != other.rank

    def __ge__(self, other):
        return self.rank >= other.rank

    def __le__(self, other):
        return self.rank <= other.rank

    @classmethod
    def from_list(cls, lst: list[float]):
        rank = cls(len(lst))
        rank.rank = lst[:]
        return rank


class SPA:

    def __init__(self, students: set[str], lecturers_projects: dict[str, set[str]],\
                preferences: dict[str, tuple[str]], project_capacities: dict[str, int],
                lecturer_capacities: dict[str, int]):
        self.students = students
        self.lecturers_projects = lecturers_projects
        self.preferences = preferences
        self.project_capacities = project_capacities
        self.lecturer_capacities = lecturer_capacities

        self.R = max(len(preference) for preference in preferences.values())
        self.f = {}

    @property
    def projects(self):
        return set(self.project_capacities.keys())

    @property
    def lecturers(self):
        return set(self.lecturer_capacities.keys())

    @property
    def active_students(self):
        return [student for student in self.students if self.f[('src', student)] > 0]

    def get_rank(self, student, project):
        if project not in self.preferences[student]:
            return self.R + 1
        return self.preferences[student].index(project) + 1

    def get_pair(self, student):
        for project in self.preferences[student]:
            if self.f[(student, project)]:
                return project

        return None

    def get_lecturer(self, project):
        for lecturer, projects in self.lecturers_projects.items():
            if project in projects:
                return lecturer

    def reset(self):
        self.f = {('src', s): 0 for s in self.students}
        self.f.update({(p, l): 0 for l, projects in self.lecturers_projects.items() for p in projects})
        self.f.update({(l, 'dst'): 0 for l in self.lecturer_capacities})
        self.f.update({(s, p): 0 for s in self.students for p in self.preferences[s]})




def get_max_aug(I: 'SPA') -> list[tuple[str, str]]:
    pred = {v: None for v in I.projects | I.lecturers}
    rho = {v: Rank(I.R, float('-inf')) for v in I.projects}

    for p in I.projects:

        for s in I.students:
            if not I.f[('src', s)] and p in I.preferences[s]:

                sigma = Rank(I.R) + I.get_rank(s, p)
                if sigma > rho[p]:
                    rho[p] = sigma
                    pred[p] = s

    for _ in range(len(I.active_students)):

        for student in I.students:

            project = I.get_pair(student)
            cur_rank = I.get_rank(student, project)

            if project is None:
                continue

            for poss in I.preferences[student]:

                if poss == project:
                    continue

                sigma = rho[project] - cur_rank + I.get_rank(student, poss)

                if sigma > rho[poss]:
                    rho[poss] = sigma
                    pred[poss] = student

        for lecturer in I.lecturers:

            sigma = Rank(I.R, float('-inf'))
            best_project = None

            for project in I.lecturers_projects[lecturer]:

                if I.f[(project, lecturer)] < I.project_capacities[project] and\
                 rho[project] > sigma:

                    sigma = rho[project]
                    best_project = project

            if best_project is not None and pred[best_project] != lecturer:

                for project in I.lecturers_projects[lecturer]:

                    if I.f[(project, lecturer)] > 0 and project != best_project:
                        rho[project] = sigma
                        pred[project] = lecturer
                        pred[lecturer] = best_project

    max_profile = Rank(I.R, float('-inf'))
    best_project = None

    for project in I.projects:

        lecturer = I.get_lecturer(project)

        if I.f[(project, lecturer)] < I.project_capacities[project] and \
         I.f[(lecturer, 'dst')] < I.lecturer_capacities[lecturer] and rho[project] > max_profile:

            max_profile = rho[project]
            best_project = project

    if best_project is None:
        return []

    path = []
    current = best_project

    while current in pred and pred[current] is not None:
        path = [current] + path
        current = pred[current]

    path = [current] + path
    return path



def greedy_max_spa(I: 'SPA', flush=True):

    if flush:
        I.reset()

    while True:
        augmenting_path = get_max_aug(I)

        if not augmenting_path:
            break

        I.f['src', augmenting_path[0]] = 1
        finished = False

        for i in range(len(augmenting_path)-1):

            u, v = augmenting_path[i], augmenting_path[i + 1]

            if u in I.lecturers and v in I.projects:
                continue

            if u in I.students and v in I.projects:
                prev_project = I.get_pair(u)

                if prev_project:
                    lecturer = I.get_lecturer(prev_project)
                    I.f[(u, prev_project)] -= 1
                    I.f[(prev_project, lecturer)] -= 1
                    I.f[(lecturer, 'dst')] -= 1


                I.f[(u, v)] = 1

            if u in I.projects and v in I.lecturers:
                bad_project = augmenting_path[i + 2]

                possible_replacements = [student for student in I.students if I.f[student, bad_project] > 0]
                if possible_replacements:
                    student = min(possible_replacements, key=lambda x: I.get_rank(x, bad_project))
                    I.f[(student, bad_project)] -= 1
                    I.f[('src', student)] -= 1

                    I.f[(u, v)] += 1
                    finished = True

        if not finished:
            lecturer = I.get_lecturer(v)
            I.f[(v, lecturer)] += 1
            I.f[(lecturer, 'dst')] += 1


    return [(student, I.get_pair(student)) for student in I.active_students]


def lower_constraints_extension(I: 'SPA', lower_constraints: dict[str, int]):
    I.reset()
    I_aux = deepcopy(I)
    I_aux.lecturer_capacities = lower_constraints

    if len(greedy_max_spa(I_aux)) == sum(lower_constraints.values()):
        I.f = I_aux.f

        return greedy_max_spa(I, False)

    return None
