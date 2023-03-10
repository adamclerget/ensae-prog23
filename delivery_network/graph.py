class Graph:
    """
    A class representing graphs as adjacency lists and implementing various algorithms on the graphs. Graphs in the class are not oriented. 
    Attributes: 
    -----------
    nodes: NodeType
        A list of nodes. Nodes can be of any immutable type, e.g., integer, float, or string.
        We will usually use a list of integers 1, ..., n.
    graph: dict
        A dictionnary that contains the adjacency list of each node in the form
        graph[node] = [(neighbor1, p1, d1), (neighbor1, p1, d1), ...]
        where p1 is the minimal power on the edge (node, neighbor1) and d1 is the distance on the edge
    nb_nodes: int
        The number of nodes.
    nb_edges: int
        The number of edges. 
    """

    def __init__(self, nodes=[]):
        """
        Initializes the graph with a set of nodes, and no edges. 
        Parameters: 
        -----------
        nodes: list, optional
            A list of nodes. Default is empty.
        """
        self.nodes = nodes
        self.graph = dict([(n, []) for n in nodes])
        self.nb_nodes = len(nodes)
        self.nb_edges = 0
    

    def __str__(self):
        """Prints the graph as a list of neighbors for each node (one per line)"""
        if not self.graph:
            output = "The graph is empty"            
        else:
            output = f"The graph has {self.nb_nodes} nodes and {self.nb_edges} edges.\n"
            for source, destination in self.graph.items():
                output += f"{source}-->{destination}\n"
        return output
    
    def add_edge(self, node1, node2, power_min, dist=1):
        """
        Adds an edge to the graph. Graphs are not oriented, hence an edge is added to the adjacency list of both end nodes. 

        Parameters: 
        -----------
        node1: NodeType
            First end (node) of the edge
        node2: NodeType
            Second end (node) of the edge
        power_min: numeric (int or float)
            Minimum power on this edge
        dist: numeric (int or float), optional
            Distance between node1 and node2 on the edge. Default is 1.
        """
        if node1 not in self.graph:
            self.graph[node1] = []
            self.nb_nodes += 1
            self.nodes.append(node1)
        if node2 not in self.graph:
            self.graph[node2] = []
            self.nb_nodes += 1
            self.nodes.append(node2)

        self.graph[node1].append((node2, power_min, dist))
        self.graph[node2].append((node1, power_min, dist))
        self.nb_edges += 1
    
    def get_path_with_power(self, src, dest, power):
        nodes_visited = {node: False for node in self.nodes}

        def dfs(node):
            if node == dest:
                return [node]
            for nei, p, _ in self.graph[node]:
                if not nodes_visited[nei] and p <= power:
                    nodes_visited[nei] = True
                    d = dfs(nei)
                    if d is not None:
                        return [node] + d
            return None
        return dfs(src)
   
    

    def connected_components(self):

        list_comp =[]
        nodes_visited = {node:False for node in self.nodes}

        def dfs(node):
            comp = [node]
            for nei in self.graph[node]:
                nei = nei[0]
                if not nodes_visited[nei]:
                    nodes_visited[nei]=True
                    comp += dfs(nei)
            return comp
        for node in self.nodes :
            if not nodes_visited[node]:
                list_comp.append(dfs(node))
        return list_comp

            




    def connected_components_set(self):
        """
        The result should be a set of frozensets (one per component), 
        For instance, for network01.in: {frozenset({1, 2, 3}), frozenset({4, 5, 6, 7})}
        """

        return set(map(frozenset, self.connected_components()))

    def min_power(self, src, dest):
        liste = []
        for n in self.nodes:
            for i in self.graph[n]:
                liste.append(i[1])
        M = max(liste)
        a = self.get_path_with_power(src, dest, M)
        if a is None:
            return None
        while a is not None:
            M -= 1
            a = self.get_path_with_power(src, dest, M)
        p_min = M+1
        path = self.get_path_with_power(src, dest, p_min)

        return p_min, path


def graph_from_file(filename):
    """
    Reads a text file and returns the graph as an object of the Graph class.

    The file should have the following format: 
        The first line of the file is 'n m'
        The next m lines have 'node1 node2 power_min dist' or 'node1 node2 power_min' (if dist is missing, it will be set to 1 by default)
        The nodes (node1, node2) should be named 1..n
        All values are integers.

    Parameters: 
    -----------
    filename: str
        The name of the file

    Outputs: 
    -----------
    g: Graph
        An object of the class Graph with the graph from file_name.
    """
    with open(filename, "r") as file:
        n, m = map(int, file.readline().split())
        g = Graph(range(1, n+1))
        for _ in range(m):
            edge = list(map(int, file.readline().split()))
            if len(edge) == 3:
                node1, node2, power_min = edge
                g.add_edge(node1, node2, power_min) # will add dist=1 by default
            elif len(edge) == 4:
                node1, node2, power_min, dist = edge
                g.add_edge(node1, node2, power_min, dist)
            else:
                raise Exception("Format incorrect")
    return g




#Question 10
from time import perf_counter
t1_start = perf_counter()
g = graph_from_file("/home/onyxia/ensae-prog23/input/network.1.in")
a = g.min_power(1, 2)
t1_stop = perf_counter()
print(a)
print(t1_stop - t1_start)


"""def kruskal(graph):
    arêtes = []
    for i in graph.graph:
        for n, p, d in graph.graph[i]:
            arêtes.append((i, n, p))
    arêtes_triées = sorted(arêtes, key=lambda a: a[2])"""



class UnionFind:
    """
    A class representing a Union-Find data structure.
    It is used to implement Kruskal's algorithm to find the minimum spanning tree of a graph.
    """
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        xroot, yroot = self.find(x), self.find(y)
        if xroot == yroot:
            return
        if self.rank[xroot] < self.rank[yroot]:
            xroot, yroot = yroot, xroot
        self.parent[yroot] = xroot
        if self.rank[xroot] == self.rank[yroot]:
            self.rank[xroot] += 1


def kruskal(g):
        # Sort edges by weight
        edges = []
        aretes = []

        for i in g.graph:
            for n, p, d in g.graph[i]:
                aretes.append((p, i, n))
        edges = sorted(aretes, key=lambda a: a[0])

        # Initialize UnionFind
        uf = UnionFind(g.nb_nodes)

        # Create minimum spanning tree
        mst = Graph()
        for weight, node1, node2 in edges:
            if uf.find(node1) != uf.find(node2):
                mst.add_edge(node1, node2, weight)
                uf.union(node1, node2)

        return mst


g=Graph([0,1,2,3,4,5,6])
g.add_edge(1, 2, 8)
g.add_edge(2,3,5)
g.add_edge(3,4,3)
g.add_edge(2,4,2)
g.add_edge(5,6,2)

print(g)

print(kruskal(g))

