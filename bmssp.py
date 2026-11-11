import heapq
import math
from helper_fns import all_paths, random_graph

def BaseCase(graph, k, B, S, dist, pred):
    s = next(iter(S))
    heap = [(dist[s], s)]
    U = set(S)
    processed = set()

    while heap and len(U) < k + 1:
        curr_dist, vertex_i = heapq.heappop(heap)

        if curr_dist > dist[vertex_i] or vertex_i in processed:
            continue

        processed.add(vertex_i)
        U.add(vertex_i)

        for vertex_j, weight in graph[vertex_i]:
            new_dist = dist[vertex_i] + weight

            if new_dist <= dist[vertex_j] and new_dist < B:
                dist[vertex_j] = new_dist
                pred[vertex_j] = vertex_i

                heapq.heappush(heap, (new_dist, vertex_j))

    if len(U) <= k:
        return B, U

    B_prime = max(dist[v] for v in U)

    U_prime = {v for v in U if dist[v] < B_prime}

    return B_prime, U_prime

def FindPivots(graph, k, B, S, dist, pred):
    # TODO
    return P, W

def recursive_bmssp(graph, k, t, level, B, S, dist, pred):
    if level == 0:
        return BaseCase(graph, k, B, S, dist, pred)

    P, W = FindPivots(graph, k, B, S, dist, pred)

    heap = []

    for p in P:
        heapq.heappush(heap, (dist[p], p))

    U = set()
    B_i_prime = min((dist[p] for p in P), default=B)

    while len(U) < (k * (2 ** (level * t))) and heap:

        M = 2 ** ((level - 1) * t)

        batch = []

        while heap and len(batch) < M:
            curr_dist, vertex_i = heapq.heappop(heap)

            if curr_dist > dist[vertex_i]:
                continue

            batch.append((curr_dist, vertex_i))

        if not batch:
            break

        S_i = {v for _, v in batch}

        if heap:
            B_i = heap[0][0]
        else:
            B_i = B
                
        B_i_prime, U_i = recursive_bmssp(graph, k, t, level - 1, B_i, S_i, dist, pred)

        U.update(U_i)
        
        K = set()

        for u in U_i:
            for w, weight in graph[u]:
                new_dist = dist[u] + weight

                if new_dist <= dist[w]:
                    dist[w] = new_dist
                    pred[w] = u

                    if B_i <= new_dist < B:
                        heapq.heappush(heap, (new_dist, w))
                    elif B_i_prime <= new_dist < B_i:
                        K.add((new_dist, w))

        for item in K:
            heapq.heappush(heap, item)

        for v in S_i:
            if B_i_prime <= dist[v] < B_i:
                heapq.heappush(heap, (dist[v], v))

    B_prime = min(B_i_prime, B)

    U.update(vertex for vertex in W if dist[vertex] < B_prime)

    return B_prime, U

def bmssp(graph, s=1):
    dist = {x: float('inf') for x in graph}
    pred = {x: None for x in graph}

    dist[s] = 0

    n = len(graph)

    k = int(math.floor(math.log(n) ** (1/3)))
    t = int(math.floor(math.log(n) ** (2/3)))
    l = int(math.ceil(math.log(n)/t))

    recursive_bmssp(graph, k, t, l, float('inf'), {s}, dist, pred)

    return (list(dist.values()), list(pred.values()))

graph = {
    1: [(2, 2), (3, 8)],
    2: [(3, 5), (4, 3)],
    3: [(2, 6), (5, 0)],
    4: [(3, 1), (5, 7), (6, 6)],
    5: [(4, 4)],
    6: [(5, 2)]
}

# dist: [0, 2, 6, 5, 6, 11]
# pred: [None, 1, 4, 2, 3, 4]
# SP to vertex 1: [1]
# SP to vertex 2: [1, 2]
# SP to vertex 3: [1, 2, 4, 3]
# SP to vertex 4: [1, 2, 4]
# SP to vertex 5: [1, 2, 4, 3, 5]
# SP to vertex 6: [1, 2, 4, 6]

# vertices = 6
# edges = 11
# graph = random_graph(vertices, edges)

s = 1

dist, pred = bmssp(graph, s)

for vertex, path in enumerate(all_paths(dist, pred), start=1):
    if path is None:
        print(f"Vertex {vertex} is unreachable")
    else:
        print(f"SP to vertex {vertex}: {path}")
