from room import Room
from player import Player
from world import World

import random
from ast import literal_eval


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


# Load world
world = World()

# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

room_init = {'n': '?', 's': '?', 'w': '?', 'e': '?'}
traversal_graph = {0: room_init.copy()}
try_order = ['e','s', 'w', 'n']

def walk_graph(traversal_graph):
    dead_end = False
    while not dead_end:
        room = player.current_room.id
        if room not in traversal_graph:
            traversal_graph[room] = room_init.copy()
            moved = False
            i = 0
            while not moved and i < 4:
                player.travel(try_order[i])
                new_room = player.current_room.id
                if room != new_room:
                    traversal_graph[room][try_order[i]] = new_room
                    traversal_path.append(try_order[i])
                    moved = True
                else:
                    traversal_graph[room][try_order[i]] = room
                i += 1
        else:
            try:
                next_direction = random.choice(
                    [x for x in traversal_graph[room].keys() if traversal_graph[room][x] == '?'])
                player.travel(next_direction)
                new_room = player.current_room.id
                if room != new_room:
                    traversal_graph[room][next_direction] = new_room
                    traversal_path.append(next_direction)
                else:
                    traversal_graph[room][next_direction] = room
            except IndexError:
                dead_end = True
    return traversal_graph


def bfs(current_room, graph):
    visited = set()
    queue = Queue()
    queue.enqueue([current_room])
    while queue.size() > 0:
        current_path = queue.dequeue()
        current_room = current_path[-1]
        possible_exits = graph[current_room].values()
        if '?' in possible_exits:
            return current_path
        if current_room not in visited:
            visited.add(current_room)
            exits = traversal_graph[current_room].values()
            for pos_exit in exits:
                path_copy = current_path + [pos_exit]
                queue.enqueue(path_copy)


while bfs(player.current_room.id, traversal_graph) is not None:
    # graph does not yet contain all rooms
    # player is standing in a room with no univisited exits
    # need to search from here to next room with unvisited exit, then travel there
    travel_rooms = bfs(player.current_room.id, traversal_graph)
    for room in travel_rooms[1:]:
        switched = [(value, key) for (key, value) in traversal_graph[player.current_room.id].items()]
        for pair in switched:
            if pair[0] == room:
                player.travel(pair[1])
                traversal_path.append(pair[1])
                break
    walk_graph(traversal_graph)

# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")

#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
