import random
from bmssp import bmssp
from dijkstra import dijkstra
from helper_fns import all_paths, random_graph

for i in range(1, 1001):
    vertices = random.randint(2, 100)
    edges = random.randint(1, vertices * (vertices - 1))
    graph = random_graph(vertices, edges)

    # print(graph)

    s = 1

    bmssp_dist, bmssp_pred = bmssp(graph, s)
    dijkstra_dist, dijkstra_pred = dijkstra(graph, s)
    
    if not bmssp_dist==dijkstra_dist:
        print(f"dist didn't match for: {graph}")
        print(f"bmssp dist: {bmssp_dist}")
        print(f"dijkstra dist: {dijkstra_dist}")
        break

    print(f"{i}: Each algorithm has the same SP distance")

    # print(f"{i}: bmssp dist: {bmssp_dist}")
    # print(f"{i}: bmssp pred: {bmssp_pred}")

    # print(f"{i}: dijkstra dist: {dijkstra_dist}")
    # print(f"{i}: dijkstra pred: {dijkstra_pred}")
