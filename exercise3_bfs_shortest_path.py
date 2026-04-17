from collections import deque
class SocialNetwork:
    def __init__(self):
        self.graph = {}
    def add_user(self, user):
        if user not in self.graph:
            self.graph[user] = []
    def add_friendship(self, user1, user2):
        self.add_user(user1)
        self.add_user(user2)
        if user2 not in self.graph[user1]:
            self.graph[user1].append(user2)
        if user1 not in self.graph[user2]:
            self.graph[user2].append(user1)
    def bfs(self, start_user):
        if start_user not in self.graph:
            return []
        visited = set()
        queue = deque([start_user])
        visited.add(start_user)
        order = []
        while queue:
            current = queue.popleft()
            order.append(current)
            for neighbor in self.graph[current]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        return order
    def bfs_with_distances(self, start_user):
        if start_user not in self.graph:
            return {}
        distances = {start_user: 0}
        queue = deque([start_user])
        while queue:
            current = queue.popleft()
            for neighbor in self.graph[current]:
                if neighbor not in distances:
                    distances[neighbor] = distances[current] + 1
                    queue.append(neighbor)
        return distances
    def shortest_path(self, start_user, target_user):
        if start_user not in self.graph or target_user not in self.graph:
            return []
        if start_user == target_user:
            return [start_user]
        came_from = {start_user: None}
        queue = deque([start_user])
        while queue:
            current = queue.popleft()
            if current == target_user:
                path = []
                node = target_user
                while node is not None:
                    path.append(node)
                    node = came_from[node]
                path.reverse()
                return path
            for neighbor in self.graph[current]:
                if neighbor not in came_from:
                    came_from[neighbor] = current
                    queue.append(neighbor)
        return []  
    def degrees_of_separation(self, start_user, target_user):
        path = self.shortest_path(start_user, target_user)
        if not path:
            return -1  
        return len(path) - 1
    def friends_within_k_hops(self, start_user, k):
        if start_user not in self.graph:
            return set()
        visited = {start_user: 0}
        queue = deque([start_user])
        result = set()
        while queue:
            current = queue.popleft()
            current_dist = visited[current]
            if current_dist == k:
                continue  
            for neighbor in self.graph[current]:
                if neighbor not in visited:
                    visited[neighbor] = current_dist + 1
                    queue.append(neighbor)
                    result.add(neighbor)
        return result
    def compute_average_degrees_of_separation(self):
        users = list(self.graph.keys())
        total = 0
        count = 0
        for i in range(len(users)):
            distances = self.bfs_with_distances(users[i])
            for j in range(i + 1, len(users)):
                if users[j] in distances:
                    total += distances[users[j]]
                    count += 1
        if count == 0:
            return 0.0
        return round(total / count, 4)
    def get_distance_distribution(self, start_user):
        distances = self.bfs_with_distances(start_user)
        distribution = {}
        for user, dist in distances.items():
            if user == start_user:
                continue 
            if dist not in distribution:
                distribution[dist] = 0
            distribution[dist] += 1
        return distribution
    def recommend_friends(self, start_user, max_recommendations=5):
        if start_user not in self.graph:
            return []
        direct_friends = set(self.graph[start_user])
        direct_friends.add(start_user)
        candidate_scores = {}
        for friend in self.graph[start_user]:
            for fof in self.graph[friend]: 
                if fof not in direct_friends:
                    if fof not in candidate_scores:
                        candidate_scores[fof] = 0
                    candidate_scores[fof] += 1 
        ranked = sorted(candidate_scores.items(), key=lambda x: x[1], reverse=True)
        return [user for user, score in ranked[:max_recommendations]]
if __name__ == "__main__":
    net = SocialNetwork()
    friendships = [
        ("Alice", "Bob"), ("Alice", "Carol"), ("Bob", "Dave"),
        ("Carol", "Dave"), ("Dave", "Eve"), ("Eve", "Frank"),
        ("Frank", "Grace"), ("Bob", "Heidi")
    ]
    for u1, u2 in friendships:
        net.add_friendship(u1, u2)
    print("BFS order from Alice:")
    print(" ", net.bfs("Alice"))
    print("\nDistances from Alice:")
    print(" ", net.bfs_with_distances("Alice"))
    print("\nShortest path Alice -> Frank:")
    print(" ", net.shortest_path("Alice", "Frank"))
    print("\nDegrees of separation Alice -> Frank:")
    print(" ", net.degrees_of_separation("Alice", "Frank"))
    print("\nFriends within 2 hops of Alice:")
    print(" ", net.friends_within_k_hops("Alice", 2))
    print("\nAverage degrees of separation:")
    print(" ", net.compute_average_degrees_of_separation())
    print("\nDistance distribution from Alice:")
    print(" ", net.get_distance_distribution("Alice"))
    print("\nFriend recommendations for Alice:")
    print(" ", net.recommend_friends("Alice"))
