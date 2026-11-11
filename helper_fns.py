import random

def reconstruct_path(dist, pred, t):
    """
    Reconstructs the shortest path to a target vertex.
    
    Arguments:
    dist (list): list of shortest distances 
    pred (list): list of predecessors in shortest path
    t (int): number specifying the target index

    Returns a list representing the shortest path to the vertex t. 
    """

    if dist[t - 1] == float('inf'): # the distance was inf, no path to this vertex
        return None
    path = []

    while t is not None: 
        path.append(t) # add vertex to list
        t = pred[t - 1] # move back an index

    path.reverse() # path is backwards since we started at t
    return path

def all_paths(dist, pred):
    """
    Reconstructs all shortest paths.

    Arguments:
    dist (list): list of shortest distances 
    pred (list): list of predecessors in shortest path

    Returns a list of lists containing the shortest path to each vertex.
    """

    paths = []

    for vertex in range(1, len(pred) + 1): # loop through each vertex
        paths.append(reconstruct_path(dist, pred, vertex)) # get the shortest path to that vertex

    return paths

def random_graph(vertices, edges):
    """
    Generates a random graph.

    Arguments:
    vertices (int): number of vertices
    edges (int): number of edges

    Returns a dictionary representing a random graph matching the specified arguments.
    """

    if edges > vertices * (vertices - 1):
        edges = vertices * (vertices - 1)
        print(f"WARNING: requested too many edges, limiting to {edges} edges (vertices * (vertices - 1)).")     

    graph = {vertex: [] for vertex in range(1, vertices + 1)} # empty graph with correct number of vertices

    exists = set() # set so we don't have duplicate edges (O(1) search)

    while len(exists) < edges: # need correct number of edges
        i = random.randint(1, vertices)
        j = random.randint(1, vertices)

        if i != j and (i, j) not in exists:
            weight = random.randint(0, 100)
            graph[i].append((j, weight))
            exists.add((i, j))

    return graph