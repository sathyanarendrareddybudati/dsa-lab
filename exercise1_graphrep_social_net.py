class SocialGraphMatrix:
    def __init__(self, users):
        self.users     = users
        self.index     = {u: i for i, u in enumerate(users)}
        n              = len(users)
        self.matrix    = [[0] * n for _ in range(n)]

    def add_friendship(self, u, v):
        i, j = self.index[u], self.index[v]
        self.matrix[i][j] = 1
        self.matrix[j][i] = 1

    def remove_friendship(self, u, v):
        i, j = self.index[u], self.index[v]
        self.matrix[i][j] = 0
        self.matrix[j][i] = 0

    def are_friends(self, u, v):
        i, j = self.index[u], self.index[v]
        return self.matrix[i][j] == 1

    def get_friends(self, u):
        i = self.index[u]
        return [self.users[j] for j in range(len(self.users)) if self.matrix[i][j] == 1]

    def get_degree(self, u):
        i = self.index[u]
        return sum(self.matrix[i])

    def get_num_users(self):
        return len(self.users)

    def get_num_edges(self):
        total = 0
        for i in range(len(self.users)):
            for j in range(i + 1, len(self.users)):
                if self.matrix[i][j] == 1:
                    total += 1
        return total

    def is_complete_graph(self):
        n = len(self.users)
        for i in range(n):
            for j in range(n):
                if i != j and self.matrix[i][j] == 0:
                    return False
        return True

    def graph_density(self):
        v = len(self.users)
        e = self.get_num_edges()
        if v <= 1:
            return 0
        return (2 * e) / (v * (v - 1))

    def degree_distribution(self):
        dist = {}
        for u in self.users:
            d = self.get_degree(u)
            dist[d] = dist.get(d, 0) + 1
        return dist

    def matrix_to_list(self):
        g = SocialGraphList()
        for u in self.users:
            g.add_user(u)
        for u in self.users:
            for v in self.get_friends(u):
                if not g.are_friends(u, v):
                    g.add_friendship(u, v)
        return g

    def display(self):
        header = "       " + "  ".join(f"{u[:4]:>4}" for u in self.users)
        print(header)
        for i, u in enumerate(self.users):
            row = "  ".join(str(self.matrix[i][j]) for j in range(len(self.users)))
            print(f"  {u[:4]:>4}   {row}")


class SocialGraphList:
    def __init__(self):
        self.adj = {}

    def add_user(self, u):
        if u not in self.adj:
            self.adj[u] = []

    def add_friendship(self, u, v):
        self.add_user(u)
        self.add_user(v)
        if v not in self.adj[u]:
            self.adj[u].append(v)
        if u not in self.adj[v]:
            self.adj[v].append(u)

    def remove_friendship(self, u, v):
        if u in self.adj and v in self.adj[u]:
            self.adj[u].remove(v)
        if v in self.adj and u in self.adj[v]:
            self.adj[v].remove(u)

    def are_friends(self, u, v):
        return u in self.adj and v in self.adj[u]

    def get_friends(self, u):
        return self.adj.get(u, [])

    def get_degree(self, u):
        return len(self.get_friends(u))

    def get_num_users(self):
        return len(self.adj)

    def get_num_edges(self):
        total = sum(len(friends) for friends in self.adj.values())
        return total // 2

    def is_complete_graph(self):
        n = self.get_num_users()
        for u in self.adj:
            if self.get_degree(u) != n - 1:
                return False
        return True

    def graph_density(self):
        v = self.get_num_users()
        e = self.get_num_edges()
        if v <= 1:
            return 0
        return (2 * e) / (v * (v - 1))

    def degree_distribution(self):
        dist = {}
        for u in self.adj:
            d = self.get_degree(u)
            dist[d] = dist.get(d, 0) + 1
        return dist

    def list_to_matrix(self):
        users = list(self.adj.keys())
        g     = SocialGraphMatrix(users)
        for u in self.adj:
            for v in self.adj[u]:
                g.add_friendship(u, v)
        return g

    def display(self):
        for u, friends in self.adj.items():
            print(f"  {u:10} → {friends}")


if __name__ == "__main__":

    users = ["Alice", "Bob", "Charlie", "Diana", "Eve", "Frank", "Grace", "Henry"]

    print("=" * 55)
    print("ADJACENCY MATRIX")
    print("=" * 55)
    gm = SocialGraphMatrix(users)
    gm.add_friendship("Alice",   "Bob")
    gm.add_friendship("Bob",     "Charlie")
    gm.add_friendship("Charlie", "Diana")
    gm.add_friendship("Charlie", "Eve")
    gm.add_friendship("Alice",   "Eve")
    gm.add_friendship("Frank",   "Grace")
    gm.display()

    print(f"\n  are_friends(Alice, Bob)     : {gm.are_friends('Alice', 'Bob')}")
    print(f"  are_friends(Alice, Diana)   : {gm.are_friends('Alice', 'Diana')}")
    print(f"  get_friends(Charlie)        : {gm.get_friends('Charlie')}")
    print(f"  get_degree(Charlie)         : {gm.get_degree('Charlie')}")
    print(f"  get_num_users()             : {gm.get_num_users()}")
    print(f"  get_num_edges()             : {gm.get_num_edges()}")
    print(f"  is_complete_graph()         : {gm.is_complete_graph()}")
    print(f"  graph_density()             : {gm.graph_density():.4f}")
    print(f"  degree_distribution()       : {gm.degree_distribution()}")

    print()
    print("  After removing Alice-Bob friendship:")
    gm.remove_friendship("Alice", "Bob")
    print(f"  are_friends(Alice, Bob)     : {gm.are_friends('Alice', 'Bob')}")
    gm.add_friendship("Alice", "Bob")

    print()
    print("=" * 55)
    print("ADJACENCY LIST")
    print("=" * 55)
    gl = SocialGraphList()
    gl.add_friendship("Alice",   "Bob")
    gl.add_friendship("Bob",     "Charlie")
    gl.add_friendship("Charlie", "Diana")
    gl.add_friendship("Charlie", "Eve")
    gl.add_friendship("Alice",   "Eve")
    gl.add_friendship("Frank",   "Grace")
    gl.add_user("Henry")
    gl.display()

    print(f"\n  are_friends(Alice, Bob)     : {gl.are_friends('Alice', 'Bob')}")
    print(f"  are_friends(Alice, Diana)   : {gl.are_friends('Alice', 'Diana')}")
    print(f"  get_friends(Charlie)        : {gl.get_friends('Charlie')}")
    print(f"  get_degree(Charlie)         : {gl.get_degree('Charlie')}")
    print(f"  get_num_users()             : {gl.get_num_users()}")
    print(f"  get_num_edges()             : {gl.get_num_edges()}")
    print(f"  is_complete_graph()         : {gl.is_complete_graph()}")
    print(f"  graph_density()             : {gl.graph_density():.4f}")
    print(f"  degree_distribution()       : {gl.degree_distribution()}")

    print()
    print("  After removing Alice-Bob friendship:")
    gl.remove_friendship("Alice", "Bob")
    print(f"  are_friends(Alice, Bob)     : {gl.are_friends('Alice', 'Bob')}")
    gl.add_friendship("Alice", "Bob")

    print()
    print("=" * 55)
    print("CONVERSION: Matrix → List")
    print("=" * 55)
    converted_list = gm.matrix_to_list()
    converted_list.display()

    print()
    print("=" * 55)
    print("CONVERSION: List → Matrix")
    print("=" * 55)
    converted_matrix = gl.list_to_matrix()
    converted_matrix.display()