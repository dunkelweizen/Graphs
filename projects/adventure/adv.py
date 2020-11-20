from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
#map_file = "maps/test_line.txt"
#map_file = "maps/test_cross.txt"
#map_file = "maps/test_loop.txt"
map_file = "maps/test_loop_fork.txt"
#map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []


traversal_graph = {}
room_init = {'n': '?', 's': '?', 'w': '?', 'e': '?'}
opposite_dir_dict = {'n':'s', 's':'n', 'e':'w', 'w':'e'}

def walk_graph(traversal_graph):
    dead_end = False

    while not dead_end:
        room = player.current_room.id
        print(room)
        if room not in traversal_graph:
            traversal_graph[room] = room_init.copy()
        try:
            next_direction = random.choice([x for x in traversal_graph[room].keys() if traversal_graph[room][x] == '?'])
            player.travel(next_direction)
            new_room = player.current_room.id
            if room != new_room:
                traversal_graph[room][next_direction] = new_room
                traversal_path.append(next_direction)
            else:
                traversal_graph[room][next_direction] = 'X'
        except IndexError:
            dead_end = True
    return traversal_graph

while len(traversal_graph) < world.grid_size:
    walk_graph(traversal_graph)
    i = -1
    while '?' not in traversal_graph[player.current_room.id].values() and i > 0:
        reverse = opposite_dir_dict[traversal_path[i]]
        traversal_path.append(reverse)
        player.travel(reverse)
        i -= 1



print(traversal_path)
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
