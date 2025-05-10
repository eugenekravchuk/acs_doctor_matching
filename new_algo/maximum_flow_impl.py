from collections import deque, defaultdict
import networkx as nx
import heapq
import random
EPSILON = 1e-5
PENALTY_MULTIPLIER = 1.5

def bellman_ford(graph, costs, doctor_penalty, cabinet_penalty, necessary_shifts, source, sink):
    dist = {node: float('inf') for node in graph}
    dist[source] = 0
    parent = {node: None for node in graph}

    for _ in range(len(graph) - 1):
        for u in graph:
            for v in graph[u]:
                if not graph[u][v]:
                    continue
                first = u.split('|')[0]
                second = v.split('|')[0] 
                cost = costs[first][second] if (not (u in necessary_shifts and v in necessary_shifts[u])) and (first in costs and second in costs[first]) else 0
                if cost:
                    cab = second + '|' + v.split('|')[1]
                    penalize_doctor = doctor_penalty[first] if first in doctor_penalty else doctor_penalty[second]
                    penalize_cabinet = cabinet_penalty[cab] if cab in cabinet_penalty else cabinet_penalty[first + '|' + u.split('|')[1]]
                    cost += (penalize_doctor + penalize_cabinet) * PENALTY_MULTIPLIER
                cost += random.uniform(0, EPSILON)
                if dist[u] + cost < dist[v]:
                    dist[v] = dist[u] + cost
                    parent[v] = u
    if dist[sink] == float('inf'):
        return None, None

    path = []
    current_node = sink
    while current_node is not None:
        path.append(current_node)
        current_node = parent[current_node]

    path.reverse()
    return dist[sink], path


def min_cost_max_flow(G: nx.DiGraph, costs, doctor_penalty, cabinet_penalty, necessary_shifts, source: str, sink: str):
    residual = defaultdict(lambda: defaultdict(int))

    for u, v, data in G.edges(data=True):
        residual[u][v] = data.get('capacity', 1)
        residual[v][u] = 0

    max_flow = 0
    min_cost = 0
    flow_dict = defaultdict(dict)

    while True:
        _, path = bellman_ford(residual, costs, doctor_penalty, cabinet_penalty, necessary_shifts, source, sink)

        if path is None:
            break

        path_flow = float('inf')
        for i in range(len(path) - 1):
            u, v = path[i], path[i + 1]
            path_flow = min(path_flow, residual[u][v])

        for i in range(len(path) - 1):
            u, v = path[i], path[i + 1]
            residual[u][v] -= path_flow
            residual[v][u] += path_flow

            first = u.split('|')[0]
            second = v.split('|')[0]

            if second[0] != 'D' and first in doctor_penalty:
                doctor_penalty[first] += 1
                cab = second + '|' + v.split('|')[1]
                try:
                    cabinet_penalty[cab] += 1
                except KeyError:
                    raise KeyError(f"Key {cab} not found in cabinet_penalty, {first}, {second}")


            cost = costs[first][second] if first in costs and second in costs[first] else 0

            min_cost += cost * path_flow

        max_flow += path_flow
        for i in range(len(path) - 1):
            u, v = path[i], path[i + 1]
            if v in G[u]:
                flow_sent = G[u][v].get('capacity', 0) - residual[u][v]
                if flow_sent > 0:
                    flow_dict[u][v] = path_flow
            else:
                flow_sent = G[v][u].get('capacity', 0) - residual[v][u]
                if flow_sent > 0:
                    flow_dict[v][u] = path_flow


    return max_flow, min_cost, dict(flow_dict)


    

