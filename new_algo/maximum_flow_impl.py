from collections import deque, defaultdict
import networkx as nx
import heapq

def bfs(residual_graph, source, sink, parent):
    visited = set()
    queue = deque([source])
    visited.add(source)

    while queue:
        u = queue.popleft()
        for v in residual_graph[u]:
            if v not in visited and residual_graph[u][v] > 0:
                visited.add(v)
                parent[v] = u
                if v == sink:
                    return True
                queue.append(v)
    return False

def custom_maximum_flow(G: nx.DiGraph, source: str, sink: str):
    residual = defaultdict(lambda: defaultdict(int))
    for u, v, data in G.edges(data=True):
        residual[u][v] = data.get('capacity', 1)
        if v not in residual or u not in residual[v]:
            residual[v][u] = 0

    max_flow = 0
    parent = {}

    while bfs(residual, source, sink, parent):
        path_flow = float('inf')
        s = sink
        while s != source:
            path_flow = min(path_flow, residual[parent[s]][s])
            s = parent[s]

        v = sink
        while v != source:
            u = parent[v]
            residual[u][v] -= path_flow
            residual[v][u] += path_flow
            v = parent[v]

        max_flow += path_flow
        parent = {}

    flow_dict = defaultdict(dict)
    for u in G.nodes():
        for v in G[u]:
            flow_sent = G[u][v].get('capacity', 0) - residual[u][v]
            if flow_sent > 0:
                flow_dict[u][v] = flow_sent

    return max_flow, dict(flow_dict)


def dijkstra(graph, costs, source, sink):
    dist = {node: float('inf') for node in graph}
    dist[source] = 0
    parent = {node: None for node in graph}
    visited = set()
    pr_queue = [(0, source)]

    while pr_queue:
        current_dist, current_node = heapq.heappop(pr_queue)
        if current_node == sink:
            break
        if current_node in visited:
            continue
        visited.add(current_node)

        for neighbor in graph[current_node]:
            if neighbor in visited:
                continue
            new_dist = current_dist + costs[current_node][neighbor]
            if new_dist < dist[neighbor]:
                dist[neighbor] = new_dist
                parent[neighbor] = current_node
                heapq.heappush(pr_queue, (new_dist, neighbor))
    
    if dist[sink] == float('inf'):
        return None, None
    
    path = []
    current_node = sink
    while current_node is not None:
        path.append(current_node)
        current_node = parent[current_node]
    
    path.reverse()
    return dist[sink], path


def bellman_ford(graph, costs, source, sink):
    dist = {node: float('inf') for node in graph}
    dist[source] = 0
    parent = {node: None for node in graph}

    for _ in range(len(graph) - 1):
        for u in graph:
            for v in graph[u]:
                if not graph[u][v]:
                    continue 
                if dist[u] + costs[u][v] < dist[v]:
                    dist[v] = dist[u] + costs[u][v]
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


def min_cost_max_flow(G: nx.DiGraph, source: str, sink: str):
    residual = defaultdict(lambda: defaultdict(int))
    costs = defaultdict(lambda: defaultdict(int))

    for u, v, data in G.edges(data=True):
        residual[u][v] = data.get('capacity', 1)
        costs[u][v] = data.get('cost', 0)
        residual[v][u] = 0
        costs[v][u] = -costs[u][v]

    max_flow = 0
    min_cost = 0
    flow_dict = defaultdict(dict)

    while True:
        cost, path = bellman_ford(residual, costs, source, sink)

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
            min_cost += costs[u][v] * path_flow

        max_flow += path_flow
        for i in range(len(path) - 1):
            u, v = path[i], path[i + 1]
            flow_sent = G[u][v].get('capacity', 0) - residual[u][v]
            if flow_sent > 0:
                flow_dict[u][v] = flow_dict[u].get(v, 0) + path_flow

    return max_flow, min_cost, dict(flow_dict)

    

