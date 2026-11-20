Math 300 Final Project

This project compares Dijkstra's and the bounded multi-source shortest path algorithms.

There are two main files: dijkstra.py and bmssp.py

To run, type `python dijkstra.py` or `python bmssp.py`.

These commands will run each algorithm on the graph and source defined at the bottom of each file starting at lines 42 and 259 respectively. By default, they generate random graphs and run on those. Each algorithm outputs the dist and pred vectors, and also the shortest path to each vertex.

There are two more files, helper_fns.py and compare.py. 

helper_fns.py contains three functions used to generate random graphs and reconstruct the actual shortest paths from dist and pred. In the random graph generator, the weights are some integer between 0 and 100. This can be changed on line 68. 

compare.py simply runs each algorithm on the same graph and ensures they output the same dist vectors. They don't compare pred, as each algorithm might find a different path. To run, type `python compare.py`.

The only packages necessary are heapq, math, and random.

AI Disclosure:
Bridgette Lopez:  ChatGPT was used to help understand the BMSSP algorithm and its pseudocode, clarify Python concepts, and provide guidance during the coding and debugging process.
