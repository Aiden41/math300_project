import random
import time
from bmssp import bmssp
from dijkstra import dijkstra
from helper_fns import all_paths, random_graph

bmssp_time = 0
dijkstra_time = 0
sizes = [100, 250, 500, 750, 1000]
for size in sizes:
    print(f"Size: {size}")
    for i in range(1, 101):
        # vertices = random.randint(2, 1000)
        vertices = size
        edges = random.randint(1, vertices * (vertices - 1))
        graph = random_graph(vertices, edges)

        # graph = {
        #         1: [(2, 10), (3, 1)],
        #         2: [],
        #         3: [(2, 1)]
        #     }

        # graph = {
        #         1: [(2, 0), (3, 1)],
        #         2: [(3, 0)],
        #         3: []
        #     }

        # graph = {
        #         1: [(2, 2), (3, 2)],
        #         2: [(4, 2)],
        #         3: [(4, 2)],
        #         4: []
        #     }

        # graph = {
        #         1: [(2, 10), (3, 1)],
        #         2: [],
        #         3: [(4, 2)],
        #         4: [(2, 1)]
        #     }

        # graph = {
        #     1: [(2, 2), (3, 8)],
        #     2: [(3, 5), (4, 3)],
        #     3: [(2, 6), (5, 0)],
        #     4: [(3, 1), (5, 7), (6, 6)],
        #     5: [(4, 4)],
        #     6: [(5, 2)]
        # }

        # print(graph)

        s = 1

        REPEATS = 10

        start = time.perf_counter()
        for _ in range(REPEATS):
            bmssp_dist, bmssp_pred = bmssp(graph, s)
        bmssp_time += (time.perf_counter() - start) / REPEATS

        start = time.perf_counter()
        for _ in range(REPEATS):
            dijkstra_dist, dijkstra_pred = dijkstra(graph, s)
        dijkstra_time += (time.perf_counter() - start) / REPEATS
        
        if not bmssp_dist==dijkstra_dist:
            print(f"dist didn't match for: {graph}")
            print(f"bmssp dist: {bmssp_dist}")
            print(f"dijkstra dist: {dijkstra_dist}")
            break

        print(f"{i}: Each algorithm has the same SP distance")

        # for vertex, path in enumerate(all_paths(bmssp_dist, bmssp_pred), start=1):
        #     if path is None:
        #         print(f"Vertex {vertex} is unreachable")
        #     else:
        #         print(f"SP to vertex {vertex}: {path}")

        # for vertex, path in enumerate(all_paths(dijkstra_dist, dijkstra_pred), start=1):
        #     if path is None:
        #         print(f"Vertex {vertex} is unreachable")
        #     else:
        #         print(f"SP to vertex {vertex}: {path}")

    print(f"BMSSP Time: {bmssp_time}")
    print(f"Dijkstra Time: {dijkstra_time}")
