import heapq
import math
import random
from helper_fns import all_paths, random_graph

def BaseCase(graph, k, B, S, dist, pred, keys):
    """
    Base case of BMSSP (algorithm 2).

    Arguments:
    graph (dictionary): dictionary with each key as a vertex and the value as a list of vertices connected via an edge
    k (int): integer constant generated based on graph size controlling maximum vertices explored
    B (tuple): tuple representing upper bound on admissible keys
    S (set): set of integers representing source vertices
    dist (dictionary): dictionary of current shortest distances to each vertex
    pred (dictionary): dictionary of current previous vertices on shortest path
    keys (dictionary): dictionary representing lexicographic order for each vertex in the form (distance, path length, (path as tuple))

    Returns: 
    B_prime (tuple): tuple representing the updated boundary key separating explored and not.
    U_prime (set): set of vertices whose keys are smaller than B_prime.
    """
    s = next(iter(S)) # base case only has 1 source
    heap = [(keys[s], s)] # initialize heap with 1 source
    U = set(S)
    processed = set()

    while heap and len(U) < k + 1:
        curr_key, vertex_i = heapq.heappop(heap) # get current smallest vertex

        if curr_key != keys[vertex_i] or vertex_i in processed:
            continue

        processed.add(vertex_i)
        U.add(vertex_i)

        for vertex_j, weight in graph[vertex_i]: # for each vertex connected to current vertex i
            new_dist = dist[vertex_i] + weight

            new_key = (new_dist, keys[vertex_i][1] + 1, (vertex_j,) + keys[vertex_i][2])

            if new_key <= keys[vertex_j] and new_key < B: # new shortest distance to vertex j
                dist[vertex_j] = new_dist
                pred[vertex_j] = vertex_i
                keys[vertex_j] = new_key

                heapq.heappush(heap, (new_key, vertex_j)) # put vertex j in the heap

    if len(U) <= k:
        return B, U

    B_prime = max(keys[v] for v in U)

    U_prime = {v for v in U if keys[v] < B_prime}

    return B_prime, U_prime

def FindPivots(graph, k, B, S, dist, pred, keys):
    """
    Find pivots function of BMSSP (algorithm 1).

    Arguments:
    graph (dictionary): dictionary with each key as a vertex and the value as a list of vertices connected via an edge
    k (int): integer constant generated based on graph size controlling maximum vertices explored
    B (tuple): tuple representing upper bound on admissible keys
    S (set): set of integers representing source vertices
    dist (dictionary): dictionary of current shortest distances to each vertex
    pred (dictionary): dictionary of current previous vertices on shortest path
    keys (dictionary): dictionary representing lexicographic order for each vertex in the form (distance, path length, (path as tuple))

    Returns: 
    P (set): set of pivot vertices.
    W (set): set of vertices reached with keys smaller than B.
    """
    W = set(S)
    W_i_prev = set(S) # current frontier

    for _ in range(1, k+1): # explore k levels from sources
        W_i = set()

        for vertex_i in W_i_prev: # for each vertex i in previous W_i set
            for vertex_j, weight in graph[vertex_i]: # for each vertex j connected to vertex i
                new_dist = dist[vertex_i] + weight
                new_key = (new_dist, keys[vertex_i][1] + 1, (vertex_j,) + keys[vertex_i][2])

                if new_key <= keys[vertex_j]: # new shortest distance to vertex j
                    dist[vertex_j] = new_dist
                    pred[vertex_j] = vertex_i
                    keys[vertex_j] = new_key

                    if new_key < B: # ensure below boundary
                        W_i.add(vertex_j)

        W.update(W_i)
        W_i_prev = W_i

        if len(W) > k * len(S): 
            P = S # all sources become pivots
            return P, W

    F = set() # edges of shortest path forest

    for vertex_i in W:
        for vertex_j, weight in graph[vertex_i]:
            if vertex_j in W:
                new_dist = dist[vertex_i] + weight
                new_key = (new_dist, keys[vertex_i][1] + 1, (vertex_j,) + keys[vertex_i][2])
                if keys[vertex_j] == new_key: # edge is on shortest path
                    F.add(((vertex_i), (vertex_j)))

    P = set() # pivot vertices

    for vertex_i in S:
        found_vertex = True
        tree_vertices = {vertex_i} # vertices in shortest path tree rooted at source

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

        if len(tree_vertices) >= k: # qualifies as pivot
            if is_root == True:
                P.add(vertex_i)

    return P, W

def recursive_bmssp(graph, k, t, level, B, S, dist, pred, keys):
    """
    Recursive portion of BMSSP (algorithm 3).

    Arguments:
    graph (dictionary): dictionary with each key as a vertex and the value as a list of vertices connected via an edge
    k (int): integer constant generated based on graph size controlling maximum vertices explored
    t (int): integer constant generated based on graph size controlling batch sizes
    level (int): integer parameter generated based on graph size representing the maximum recursion depth
    B (tuple): tuple representing upper bound on admissible keys
    S (set): set of integers representing source vertices
    dist (dictionary): dictionary of current shortest distances to each vertex
    pred (dictionary): dictionary of current previous vertices on shortest path
    keys (dictionary): dictionary representing lexicographic order for each vertex in the form (distance, path length, (path as tuple))

    Returns two lists: 
    B_prime (tuple): tuple representing updated boundary key produced by recursive search.
    U (set): set of vertices settled whose keys are less than B_prime.
    """
    if level == 0: # last level of recursion, return BaseCase
        return BaseCase(graph, k, B, S, dist, pred, keys)

    P, W = FindPivots(graph, k, B, S, dist, pred, keys) # find pivots and reachable vertices

    heap = []

    for p in P:
        heapq.heappush(heap, (keys[p], p))

    U = set() # settled vertices
    B_i_prime = min((keys[p] for p in P), default=B) # current smallest pivot key, if no pivots use B

    while len(U) < (k * (2 ** (level * t))) and heap: # go until limit or heap is empty
        M = 2 ** ((level - 1) * t) # batch size from algorithm

        batch = []

        while heap and len(batch) < M:
            curr_key, vertex_i = heapq.heappop(heap)

            if curr_key != keys[vertex_i]: # skip outdated heap entry
                continue

            batch.append((curr_key, vertex_i))

        if not batch:
            break

        S_i = {v for _, v in batch} # sources for recursive call

        while heap and heap[0][0] != keys[heap[0][1]]: # remove stale entries
            heapq.heappop(heap)

        if heap: # get next boundary key
            B_i = heap[0][0]
        else:
            B_i = B
                
        B_i_prime, U_i = recursive_bmssp(graph, k, t, level - 1, B_i, S_i, dist, pred, keys) # make recursive call, drop level down by 1

        U.update(U_i)
        
        K = set() # temp vertices below boundary

        for u in U_i:
            for w, weight in graph[u]:
                new_dist = dist[u] + weight
                new_key = (new_dist, keys[u][1] + 1, (w,) + keys[u][2])

                if new_key <= keys[w]: # new shortest path to w
                    dist[w] = new_dist
                    pred[w] = u
                    keys[w] = new_key

                    if B_i <= new_key < B: # candidate for heap
                        heapq.heappush(heap, (new_key, w))

                    elif B_i_prime <= new_key < B_i: # candidate for K, delay insert
                        K.add((new_key, w))

        for item in K: # insert delayed candidates
            heapq.heappush(heap, item)

        for v in S_i: # reinsert sources whose keys moved below B_i
            if B_i_prime <= keys[v] < B_i:
                heapq.heappush(heap, (keys[v], v))

    B_prime = min(B_i_prime, B) # get final boundary for this recursive call

    U.update(vertex for vertex in W if keys[vertex] < B_prime) # add reachable vertices below B_prime

    return B_prime, U

def bmssp(graph, s=1):
    """
    Bounded multi-source shortest path algorithm.

    Arguments:
    graph (dictionary): dictionary with each key as a vertex and the value as a list of vertices connected via an edge
    s (int): number representing the starting vertex

    Returns two lists: dist (shortest distance to each vertex) and pred (list of predecessors on shortest path).
    """
        
    dist = {x: float('inf') for x in graph}
    pred = {x: None for x in graph}
    keys = {x: (float('inf'), float('inf'), ()) for x in graph} # used for tie-breaker heap sorting

    dist[s] = 0
    keys[s] = (0, 1, (s,))

    n = len(graph)

    k = int(math.ceil(math.log2(n) ** (1/3))) # from lemma 3.12
    t = int(math.ceil(math.log2(n) ** (2/3)))
    l = int(math.ceil(math.log2(n)/t))

    B = (float('inf'), float('inf'), ())

    recursive_bmssp(graph, k, t, l, B, {s}, dist, pred, keys) # start running bmssp

    return (list(dist.values()), list(pred.values()))

if __name__ == "__main__":
    # graph = {
    #     1: [(2, 2), (3, 8)],
    #     2: [(3, 5), (4, 3)],
    #     3: [(2, 6), (5, 0)],
    #     4: [(3, 1), (5, 7), (6, 6)],
    #     5: [(4, 4)],
    #     6: [(5, 2)]
    # }

    vertices = random.randint(2, 100)
    edges = random.randint(1, vertices * (vertices - 1))
    graph = random_graph(vertices, edges)

    s = 1

    dist, pred = bmssp(graph, s)

    print(f"dist: {dist}")
    print(f"pred: {pred}")

    for vertex, path in enumerate(all_paths(dist, pred), start=1):
        if path is None:
            print(f"Vertex {vertex} is unreachable")
        else:
            print(f"SP to vertex {vertex}: {path}")