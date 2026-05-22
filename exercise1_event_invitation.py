from itertools import combinations
class Graph:
    def __init__(self):
        self.adj = {}

    def add_user(self, u):
        if u not in self.adj:
            self.adj[u] = []

    def add_edge(self, u, v):
        self.add_user(u)
        self.add_user(v)
        if v not in self.adj[u]: self.adj[u].append(v)
        if u not in self.adj[v]: self.adj[v].append(u)

    def get_friends(self, u):
        return self.adj.get(u, [])

    @property
    def all_users(self):
        return list(self.adj.keys())

def is_valid_coverage(selected_users, graph):
    covered = set()

    for user in selected_users:
        covered.add(user)
        for neighbor in graph.get_friends(user):
            covered.add(neighbor)

    for user in graph.all_users:
        if user not in covered:
            return False

    return True

def find_minimum_coverage(graph):
    users = graph.all_users
    n     = len(users)

    for size in range(1, n + 1):
        for subset in combinations(users, size):
            if is_valid_coverage(list(subset), graph):
                return (size, list(subset))

    return (n, users)

def find_fast_coverage(graph):
    uncovered = set(graph.all_users)
    selected  = []

    while uncovered:
        best_node  = None
        best_count = -1

        for user in graph.all_users:
            if user in selected:
                continue

            count = 0
            if user in uncovered:
                count += 1
            for neighbor in graph.get_friends(user):
                if neighbor in uncovered:
                    count += 1

            if count > best_count:
                best_count = count
                best_node  = user

        selected.append(best_node)
        uncovered.discard(best_node)
        for neighbor in graph.get_friends(best_node):
            uncovered.discard(neighbor)

    return (len(selected), selected)

if __name__ == "__main__":

    print("=" * 55)
    print("GRAPH 1: Chain  1-2-3-4-5")
    print("=" * 55)
    g1 = Graph()
    for u, v in [(1,2),(2,3),(3,4),(4,5)]:
        g1.add_edge(u, v)

    exact_size,  exact_set  = find_minimum_coverage(g1)
    greedy_size, greedy_set = find_fast_coverage(g1)

    print(f"  Exact   → size={exact_size},  set={exact_set}")
    print(f"  Greedy  → size={greedy_size}, set={greedy_set}")
    print(f"  Verify exact  : {is_valid_coverage(exact_set,  g1)}")
    print(f"  Verify greedy : {is_valid_coverage(greedy_set, g1)}")

    print()
    print("=" * 55)
    print("GRAPH 2: Star  center=1, leaves=2,3,4,5")
    print("=" * 55)
    g2 = Graph()
    for leaf in [2, 3, 4, 5]:
        g2.add_edge(1, leaf)

    exact_size,  exact_set  = find_minimum_coverage(g2)
    greedy_size, greedy_set = find_fast_coverage(g2)

    print(f"  Exact   → size={exact_size},  set={exact_set}")
    print(f"  Greedy  → size={greedy_size}, set={greedy_set}")
    print(f"  Verify exact  : {is_valid_coverage(exact_set,  g2)}")
    print(f"  Verify greedy : {is_valid_coverage(greedy_set, g2)}")
    print()
    print("=" * 55)
    print("GRAPH 3: Triangle  1-2-3-1")
    print("=" * 55)
    g3 = Graph()
    for u, v in [(1,2),(2,3),(3,1)]:
        g3.add_edge(u, v)

    exact_size,  exact_set  = find_minimum_coverage(g3)
    greedy_size, greedy_set = find_fast_coverage(g3)

    print(f"  Exact   → size={exact_size},  set={exact_set}")
    print(f"  Greedy  → size={greedy_size}, set={greedy_set}")
    print(f"  Verify exact  : {is_valid_coverage(exact_set,  g3)}")
    print(f"  Verify greedy : {is_valid_coverage(greedy_set, g3)}")
    print()
    print("=" * 55)
    print("GRAPH 4: Disconnected  {1-2-3}  {4-5}")
    print("=" * 55)
    g4 = Graph()
    for u, v in [(1,2),(2,3),(4,5)]:
        g4.add_edge(u, v)

    exact_size,  exact_set  = find_minimum_coverage(g4)
    greedy_size, greedy_set = find_fast_coverage(g4)

    print(f"  Exact   → size={exact_size},  set={exact_set}")
    print(f"  Greedy  → size={greedy_size}, set={greedy_set}")
    print(f"  Verify exact  : {is_valid_coverage(exact_set,  g4)}")
    print(f"  Verify greedy : {is_valid_coverage(greedy_set, g4)}")

    print()
    print("=" * 55)
    print("EDGE CASES")
    print("=" * 55)
    g_empty = Graph()
    for u in [1, 2, 3, 4]:
        g_empty.add_user(u)
    exact_size, exact_set = find_minimum_coverage(g_empty)
    print(f"  Empty graph (no edges)   → size={exact_size}, set={exact_set}")
    g_complete = Graph()
    for u, v in [(1,2),(1,3),(1,4),(2,3),(2,4),(3,4)]:
        g_complete.add_edge(u, v)
    exact_size, exact_set = find_minimum_coverage(g_complete)
    print(f"  Complete K4              → size={exact_size}, set={exact_set}")

    g_single = Graph()
    g_single.add_user(1)
    exact_size, exact_set = find_minimum_coverage(g_single)
    print(f"  Single node              → size={exact_size}, set={exact_set}")

    print(f"  Verify empty set on g1   → {is_valid_coverage([], g1)}")   # False
    print(f"  Verify all nodes on g1   → {is_valid_coverage(g1.all_users, g1)}")  # True