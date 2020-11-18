import random

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

class User:
    def __init__(self, name):
        self.name = name


class SocialGraph:
    def __init__(self):
        self.last_id = 0
        self.users = {}
        self.friendships = {}

    def add_friendship(self, user_id, friend_id):
        """
        Creates a bi-directional friendship
        """
        if user_id == friend_id:
            print("WARNING: You cannot be friends with yourself")
        elif friend_id in self.friendships[user_id] or user_id in self.friendships[friend_id]:
            print("WARNING: Friendship already exists")
        else:
            self.friendships[user_id].add(friend_id)
            self.friendships[friend_id].add(user_id)

    def add_user(self, name):
        """
        Create a new user with a sequential integer ID
        """
        self.last_id += 1  # automatically increment the ID to assign the new user
        self.users[self.last_id] = User(name)
        self.friendships[self.last_id] = set()

    def populate_graph(self, num_users, avg_friendships):
        """
        Takes a number of users and an average number of friendships
        as arguments

        Creates that number of users and a randomly distributed friendships
        between those users.

        The number of users must be greater than the average number of friendships.
        """
        # Reset graph
        self.last_id = 0
        self.users = {}
        self.friendships = {}

        for user in range(num_users):
            self.add_user(user)

        total_friendships = avg_friendships * num_users
        friendship_combos = []
        for user_id in range(1,num_users+1):
            for friend_id in range(user_id +1, num_users+1):
                friendship_combos.append((user_id,friend_id))

        random.shuffle(friendship_combos)

        make_friendships = friendship_combos[:(total_friendships // 2)]

        for friendship in make_friendships:
            self.add_friendship(friendship[0], friendship[1])

    def get_friendships(self, user_id):
        return self.friendships[user_id]

    def get_all_social_paths(self, user_id):
        """
        Takes a user's user_id as an argument

        Returns a dictionary containing every user in that user's
        extended network with the shortest friendship path between them.

        The key is the friend's ID and the value is the path.
        """
        if self.get_friendships(user_id) == set():
            #any user with no friends has an extended network which is empty
            return {}
        visited = {}  # Note that this is a dictionary, not a set
        for friend in self.users:
            if friend not in visited:
                path = self.bfs(user_id, friend)
                if path is not None:
                    visited[friend] = path

        return visited

    def bfs(self, starting_vertex, destination_vertex):
        """
        Return a list containing the shortest path from
        starting_vertex to destination_vertex in
        breath-first order.
        """
        queue = Queue()

        visited = set()
        queue.enqueue([starting_vertex])

        while queue.size() > 0:
            current_path = queue.dequeue()
            current_node = current_path[-1]

            if current_node == destination_vertex:
                return current_path
            if current_node not in visited:
                visited.add(current_node)
                neighbors = self.get_friendships(current_node)
                for neighbor in neighbors:
                    path_copy = current_path + [neighbor]
                    queue.enqueue(path_copy)

if __name__ == '__main__':
    sg = SocialGraph()
    sg.populate_graph(10, 2)
    print(sg.friendships)
    connections = sg.get_all_social_paths(1)
    print(connections)
