# Dial's Algorithm

The canonical way to compute single-source shortest paths in an undirected, weighted graph 
*G = (V, E)* is via Dijkstra's algorithm. Using a binary min-heap, Dijkstra's algorithm should 
run in *O((V + E) log V)* time.

However, in some cases, we can do better. For instance, in a directed acylcic graph,
we can determine the shortest paths for vertices in topological order, for a total runtime
of O(V + E). 

In this assignment, you will be implementing a similar shortest path algorithm that is
more efficient than Dijkstra's in certain cases. If the edges of an undirected graph are bounded integers, 
you can use Dial's algorithm to find shortest paths more efficiently.


## Assignment

Consider an undirected graph *G* with small positive integer edge weights, 
upper bounded by a maximum edge weight *W*. In this special case, we can solve the single-source shortest paths problem with a better runtime than Dijkstra's algorithm.

Dial's Algorithm is essentially a modification of Dijkstra's algorithm to use a 
different data structure to store vertices instead of the typical min-heap.
When the edge weights are small positive integers,
a [bucket queue](https://en.wikipedia.org/wiki/Bucket_queue) is an appropriate choice.

Dial's algorithm works as follows: store vertices in buckets numbered from 1 (highest priority) 
to *W* (lowest priority). At each iteration, take out a vertex from the nonempty 
bucket with the highest priority.

Implement Dial's algorithm in `dial.py`. There are several ways to implement a bucket queue in Python - you should decide what works best. To keep things simple, we will compute only the shortest path distances, although the algorithm can easily be extended to find the shortest path tree as well. The NetworkX `Graph` class is used to provide a standardized input format, but you should not use any NetworkX algorithms. 

Basic tests are provided in `test_dial.py`, but passing them is not a guarantee of full credit. Inefficient code may also not receive full credit.

Leave a comment analyzing the following in terms of *V*, *E*, and *W*:
- Runtime of your implementation of Dial's algorithm
- Amount of **additional** space used in memory (excluding the space used to hold the input graph)
