import heapq
from helper_fns import all_paths, random_graph

def dijkstra(graph, s=1):
    """
    Dijkstra's shortest path algorithm.

    Arguments:
    graph (dictionary): dictionary with each key as a vertex and the value as a list of vertices connected via an edge
    s (int): number representing the starting vertex

    Returns two lists: dist (shortest distance to each vertex) and pred (list of predecessors on shortest path).
    """

    dist = {x: float('inf') for x in graph}
    pred = {x: None for x in graph}

    dist[s] = 0

    heap = [(0, s)]

    while heap:
        curr_dist, vertex_i = heapq.heappop(heap) # get shortest distance vertex

        if curr_dist > dist[vertex_i]:
            continue

        for vertex_j, weight in graph[vertex_i]: # for each vertex connected to current vertex i
            new_dist = dist[vertex_i] + weight

            if new_dist < dist[vertex_j]: # new shortest distance to vertex j
                dist[vertex_j] = new_dist
                pred[vertex_j] = vertex_i

                heapq.heappush(heap, (new_dist, vertex_j)) # put vertex j in the heap

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

dist, pred = dijkstra(graph, s)

print(f"dist: {dist}")
print(f"pred: {pred}")

for vertex, path in enumerate(all_paths(dist, pred), start=1):
    if path is None:
        print(f"Vertex {vertex} is unreachable")
    else:
        print(f"SP to vertex {vertex}: {path}")