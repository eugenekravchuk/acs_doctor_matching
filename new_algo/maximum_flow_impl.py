from collections import deque, defaultdict
import networkx as nx

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
