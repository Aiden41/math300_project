import heapq
import math
from helper_fns import all_paths, random_graph

def BaseCase(graph, k, B, S, dist, pred, keys):
    s = next(iter(S))
    heap = [(keys[s], s)]
    U = set(S)
    processed = set()

    while heap and len(U) < k + 1:
        curr_key, vertex_i = heapq.heappop(heap)

        if curr_key != keys[vertex_i] or vertex_i in processed:
            continue

        processed.add(vertex_i)
        U.add(vertex_i)

        for vertex_j, weight in graph[vertex_i]:
            new_dist = dist[vertex_i] + weight

            new_key = (new_dist, keys[vertex_i][1] + 1, (vertex_j,) + keys[vertex_i][2])

            if new_key <= keys[vertex_j] and new_key < B:
                dist[vertex_j] = new_dist
                pred[vertex_j] = vertex_i
                keys[vertex_j] = new_key

                heapq.heappush(heap, (new_key, vertex_j))

    if len(U) <= k:
        return B, U

    B_prime = max(keys[v] for v in U)

    U_prime = {v for v in U if keys[v] < B_prime}

    return B_prime, U_prime

def FindPivots(graph, k, B, S, dist, pred, keys):
    W = set(S)
    W_i_prev = set(S)

    for _ in range(1, k+1):
        W_i = set()

        for vertex_i in W_i_prev:
            for vertex_j, weight in graph[vertex_i]:
                new_dist = dist[vertex_i] + weight
                new_key = (new_dist, keys[vertex_i][1] + 1, (vertex_j,) + keys[vertex_i][2])

                if new_key <= keys[vertex_j]:
                    dist[vertex_j] = new_dist
                    pred[vertex_j] = vertex_i
                    keys[vertex_j] = new_key

                    if new_key < B:
                        W_i.add(vertex_j)

        W.update(W_i)
        W_i_prev = W_i

        if len(W) > k * len(S):
            P = S
            return P, W

    F = set()

    for vertex_i in W:
        for vertex_j, weight in graph[vertex_i]:
            if vertex_j in W:
                new_dist = dist[vertex_i] + weight
                new_key = (new_dist, keys[vertex_i][1] + 1, (vertex_j,) + keys[vertex_i][2])
                if keys[vertex_j] == new_key:
                    F.add(((vertex_i), (vertex_j)))

    P = set()

    for vertex_i in S:
        found_vertex = True
        tree_vertices = {vertex_i}

        while found_vertex:
            found_vertex = False
            for u, v in F:
                if u in tree_vertices and v not in tree_vertices:
                    tree_vertices.add(v)
                    found_vertex = True

        is_root = True
        for u, v in F:
            if v == vertex_i:
                is_root = False

        if len(tree_vertices) >= k:
            if is_root == True:
                P.add(vertex_i)

    return P, W

def recursive_bmssp(graph, k, t, level, B, S, dist, pred, keys):
    if level == 0:
        return BaseCase(graph, k, B, S, dist, pred, keys)

    P, W = FindPivots(graph, k, B, S, dist, pred, keys)

    heap = []

    for p in P:
        heapq.heappush(heap, (keys[p], p))

    U = set()
    B_i_prime = min((keys[p] for p in P), default=B)

    while len(U) < (k * (2 ** (level * t))) and heap:

        M = 2 ** ((level - 1) * t)

        batch = []

        while heap and len(batch) < M:
            curr_key, vertex_i = heapq.heappop(heap)

            if curr_key != keys[vertex_i]:
                continue

            batch.append((curr_key, vertex_i))

        if not batch:
            break

        S_i = {v for _, v in batch}

        while heap and heap[0][0] != keys[heap[0][1]]:
            heapq.heappop(heap)

        if heap:
            B_i = heap[0][0]
        else:
            B_i = B
                
        B_i_prime, U_i = recursive_bmssp(graph, k, t, level - 1, B_i, S_i, dist, pred, keys)

        U.update(U_i)
        
        K = set()

        for u in U_i:
            for w, weight in graph[u]:
                new_dist = dist[u] + weight
                new_key = (new_dist, keys[u][1] + 1, (w,) + keys[u][2])

                if new_key <= keys[w]:
                    dist[w] = new_dist
                    pred[w] = u
                    keys[w] = new_key

                    if B_i <= new_key < B:
                        heapq.heappush(heap, (new_key, w))

                    elif B_i_prime <= new_key < B_i:
                        K.add((new_key, w))

        for item in K:
            heapq.heappush(heap, item)

        for v in S_i:
            if B_i_prime <= keys[v] < B_i:
                heapq.heappush(heap, (keys[v], v))

    B_prime = min(B_i_prime, B)

    U.update(vertex for vertex in W if keys[vertex] < B_prime)

    return B_prime, U

def bmssp(graph, s=1):
    dist = {x: float('inf') for x in graph}
    pred = {x: None for x in graph}
    keys = {x: (float('inf'), float('inf'), ()) for x in graph}

    dist[s] = 0
    keys[s] = (0, 1, (s,))

    n = len(graph)

    k = int(math.floor(math.log(n) ** (1/3)))
    t = int(math.floor(math.log(n) ** (2/3)))
    l = int(math.ceil(math.log(n)/t))

    B = (float('inf'), float('inf'), ())

    recursive_bmssp(graph, k, t, l, B, {s}, dist, pred, keys)

    return (list(dist.values()), list(pred.values()))

graph = {
    1: [(2, 2), (3, 8)],
    2: [(3, 5), (4, 3)],
    3: [(2, 6), (5, 0)],
    4: [(3, 1), (5, 7), (6, 6)],
    5: [(4, 4)],
    6: [(5, 2)]
}

# vertices = 6
# edges = 11
# graph = random_graph(vertices, edges)

s = 1

dist, pred = bmssp(graph, s)

print(f"dist: {dist}")
print(f"pred: {pred}")

for vertex, path in enumerate(all_paths(dist, pred), start=1):
    if path is None:
        print(f"Vertex {vertex} is unreachable")
    else:
        print(f"SP to vertex {vertex}: {path}")
