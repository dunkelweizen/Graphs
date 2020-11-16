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
            graph[t[1]] = set(t[0])
    return graph

def earliest_ancestor(ancestors, starting_node):
    neighbor_graph = make_neighbors(ancestors)
    # need to return ancestor node farthest from starting node
    # must move from starting_node -> parent node -> parent node, no child nodes, else it's not an ancestor
    if starting_node not in neighbor_graph:
        #if node isn't in graph dict, it has no parents
        return -1
    parents = neighbor_graph[starting_node]
    # need to travel graph dict for each parent, stopping when run out of ancestors
    # then check which path is longer and return last ancestor of that path




