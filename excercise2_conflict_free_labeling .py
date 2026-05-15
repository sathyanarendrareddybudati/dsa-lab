class Graph:
    def __init__(self):
        self.adj = {}

    def add_user(self, u):
        if u not in self.adj:
            self.adj[u] = []

    def add_edge(self, u, v):
        self.add_user(u)
        self.add_user(v)
        if v not in self.adj[u]:
            self.adj[u].append(v)
        if u not in self.adj[v]:
            self.adj[v].append(u)

    def get_friends(self, u):
        return self.adj.get(u, [])

    @property
    def all_users(self):
        return list(self.adj.keys())


def is_valid_labeling(labeling, graph):
    for user in graph.all_users:
        for neighbor in graph.get_friends(user):
            if labeling.get(user) == labeling.get(neighbor):
                return False
    return True


def assign_labels(k, graph):
    users = graph.all_users
    labeling = {u: -1 for u in users}

    def is_safe(user, color):
        for neighbor in graph.get_friends(user):
            if labeling[neighbor] == color:
                return False
        return True

    def backtrack(index):
        if index == len(users):
            return True

        user = users[index]
        for color in range(k):
            if is_safe(user, color):
                labeling[user] = color
                if backtrack(index + 1):
                    return True
                labeling[user] = -1

        return False

    if backtrack(0):
        return (True, labeling)
    return (False, {})


def find_min_labels(graph):
    n = len(graph.all_users)
    for k in range(1, n + 1):
        success, labeling = assign_labels(k, graph)
        if success:
            return (k, labeling)
    return (n, {})


if __name__ == "__main__":

    print("=" * 55)
    print("GRAPH 1: Triangle  1-2-3-1")
    print("=" * 55)
    g1 = Graph()
    for u, v in [(1, 2), (2, 3), (3, 1)]:
        g1.add_edge(u, v)

    min_k, labeling = find_min_labels(g1)
    print(f"  Minimum labels  : {min_k}")
    print(f"  Labeling        : {labeling}")
    print(f"  Valid           : {is_valid_labeling(labeling, g1)}")

    print()
    print("=" * 55)
    print("GRAPH 2: Bipartite  1-3, 1-4, 2-3, 2-4")
    print("=" * 55)
    g2 = Graph()
    for u, v in [(1, 3), (1, 4), (2, 3), (2, 4)]:
        g2.add_edge(u, v)

    min_k, labeling = find_min_labels(g2)
    print(f"  Minimum labels  : {min_k}")
    print(f"  Labeling        : {labeling}")
    print(f"  Valid           : {is_valid_labeling(labeling, g2)}")

    print()
    print("=" * 55)
    print("GRAPH 3: Complete K4")
    print("=" * 55)
    g3 = Graph()
    for u, v in [(1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4)]:
        g3.add_edge(u, v)

    min_k, labeling = find_min_labels(g3)
    print(f"  Minimum labels  : {min_k}")
    print(f"  Labeling        : {labeling}")
    print(f"  Valid           : {is_valid_labeling(labeling, g3)}")

    print()
    print("=" * 55)
    print("GRAPH 4: Empty (no edges)")
    print("=" * 55)
    g4 = Graph()
    for u in [1, 2, 3, 4]:
        g4.add_user(u)

    min_k, labeling = find_min_labels(g4)
    print(f"  Minimum labels  : {min_k}")
    print(f"  Labeling        : {labeling}")
    print(f"  Valid           : {is_valid_labeling(labeling, g4)}")

    print()
    print("=" * 55)
    print("EDGE CASE: assign_labels(1) on graph with edges")
    print("=" * 55)
    success, _ = assign_labels(1, g1)
    print(f"  assign_labels(1) on triangle : {success}")

    success, _ = assign_labels(2, g1)
    print(f"  assign_labels(2) on triangle : {success}")

    success, _ = assign_labels(3, g1)
    print(f"  assign_labels(3) on triangle : {success}")

    print()
    print("=" * 55)
    print("EDGE CASE: Verify invalid labeling")
    print("=" * 55)
    bad_labeling = {1: 0, 2: 0, 3: 1}
    print(
        f"  Bad labeling {bad_labeling} on triangle : {is_valid_labeling(bad_labeling, g1)}"
    )
