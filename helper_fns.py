import random

def reconstruct_path(dist, pred, t):
    if dist[t - 1] == float('inf'):
        return None
    
    path = []

    while t != 0:
        path.append(t)
        t = pred[t - 1]

    path.reverse()
    return path

def all_paths(dist, pred):
    paths = []

    for vertex in range(1, len(pred) + 1):
        paths.append(reconstruct_path(dist, pred, vertex))

    return paths

def random_graph(vertices, edges):
    if edges > vertices * (vertices - 1):
        edges = vertices * (vertices - 1)
        print(f"WARNING: requested too many edges, limiting to {edges} edges (vertices * (vertices - 1)).")     

    graph = {vertex: [] for vertex in range(1, vertices + 1)}

    exists = set()

    while len(exists) < edges:
        i = random.randint(1, vertices)
        j = random.randint(1, vertices)

        if i != j and (i, j) not in exists:
            weight = random.randint(0, 100)
            graph[i].append((j, weight))
            exists.add((i, j))

    return graph