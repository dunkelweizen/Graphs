class Queue():
    def __init__(self):
        self.queue = []
    def enqueue(self, value):
        self.queue.append(value)
    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None
    def size(self):
        return len(self.queue)

def make_neighbors(l):
    #creates a dictionary of sets where dict[child] calls the set of parents
    graph = {}
    for t in l:
        if t[1] in graph:
            graph[t[1]].add(t[0])
        else:
            graph[t[1]] = set()
            graph[t[1]].add(t[0])
    return graph

path = []
visited = set()

def earliest_ancestor(ancestors, starting_node, path = [], visited = set()):
    neighbor_graph = make_neighbors(ancestors)
    # need to return ancestor node farthest from starting node
    # must move from starting_node -> parent node -> parent node, no child nodes, else it's not an ancestor
    if path == [] or visited == set():
        path = []
        visited = set()
    if starting_node not in neighbor_graph and len(path) == 0:
        return -1
    if starting_node not in visited:
        visited.add(starting_node)
    path.append(starting_node)
    try:
        parents = neighbor_graph[starting_node]
        for parent in parents:
            if parent not in visited:
                new_path = earliest_ancestor(ancestors, parent, path, visited)
                if new_path is not None:
                    return new_path
    except KeyError:
        return starting_node