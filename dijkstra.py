import heapq

def dijkstra(graph, s=1):
    dist = {x: float('inf') for x in graph}
    pred = {x: 0 for x in graph}

    dist[s] = 0

    heap = [(0, s)]

    while heap:
        curr_dist, vertex_i = heapq.heappop(heap)

        if curr_dist > dist[vertex_i]:
            continue

        for vertex_j, weight in graph[vertex_i]:

            new_dist = dist[vertex_i] + weight

            if new_dist < dist[vertex_j]:
                dist[vertex_j] = new_dist
                pred[vertex_j] = vertex_i

                heapq.heappush(heap, (new_dist, vertex_j))

    return (list(dist.values()), list(pred.values()))

graph = {
    1: [(2, 2), (3, 8)],
    2: [(3, 5), (4, 3)],
    3: [(2, 6), (5, 0)],
    4: [(3, 1), (5, 7), (6, 6)],
    5: [(4, 4)],
    6: [(5, 2)]
}

s = 1

dist, pred = dijkstra(graph, s)

print(f"dist: {dist}")
print(f"pred: {pred}")