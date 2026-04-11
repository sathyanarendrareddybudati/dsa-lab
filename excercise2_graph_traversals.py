class SocialGraph:

    def __init__(self):
        self.adjacency_list = {}

    def add_user(self, user):
        if user not in self.adjacency_list:
            self.adjacency_list[user] = []

    def add_friendship(self, u, v):
        self.add_user(u)
        self.add_user(v)
        if v not in self.adjacency_list[u]:
            self.adjacency_list[u].append(v)
        if u not in self.adjacency_list[v]:
            self.adjacency_list[v].append(u)

    def get_friends(self, user):
        return self.adjacency_list.get(user, [])

    def get_degree(self, user):
        return len(self.get_friends(user))

    @property
    def all_users(self):
        return list(self.adjacency_list.keys())


def dfs_recursive(graph, start_user):
    visited = set()
    result = []

    def helper(user):
        visited.add(user)
        result.append(user)
        for friend in graph.get_friends(user):
            if friend not in visited:
                helper(friend)

    helper(start_user)
    return result


def dfs_iterative(graph, start_user):
    visited = set()
    stack = [start_user]
    result = []

    while stack:
        user = stack.pop()
        if user not in visited:
            visited.add(user)
            result.append(user)
            for friend in graph.get_friends(user):
                if friend not in visited:
                    stack.append(friend)

    return result


def find_connected_components(graph):
    visited = set()
    components = []

    def helper(user, component):
        visited.add(user)
        component.append(user)
        for friend in graph.get_friends(user):
            if friend not in visited:
                helper(friend, component)

    for user in graph.all_users:
        if user not in visited:
            component = []
            helper(user, component)
            components.append(component)

    return components


def is_connected(graph):
    components = find_connected_components(graph)
    return len(components) == 1


def has_path(graph, start_user, target_user):
    visited = set()

    def helper(user):
        visited.add(user)
        if user == target_user:
            return True
        for friend in graph.get_friends(user):
            if friend not in visited:
                if helper(friend):
                    return True
        return False

    return helper(start_user)


def find_path(graph, start_user, target_user):
    visited = set()
    path = []

    def helper(user):
        visited.add(user)
        path.append(user)

        if user == target_user:
            return True

        for friend in graph.get_friends(user):
            if friend not in visited:
                if helper(friend):
                    return True

        path.pop()
        return False

    helper(start_user)
    return path


def get_connected_components_sizes(graph):
    components = find_connected_components(graph)
    return [len(c) for c in components]


def find_largest_component(graph):
    components = find_connected_components(graph)
    return max(components, key=len)


def find_isolated_users(graph):
    return [user for user in graph.all_users if graph.get_degree(user) == 0]


if __name__ == "__main__":

    g = SocialGraph()

    g.add_friendship("Alice", "Bob")
    g.add_friendship("Bob", "Charlie")
    g.add_friendship("Charlie", "Diana")
    g.add_friendship("Charlie", "Eve")
    g.add_friendship("Frank", "Grace")
    g.add_user("Henry")

    print("=" * 55)
    print("PART A — Recursive DFS from Alice")
    print("=" * 55)
    print(" ", dfs_recursive(g, "Alice"))

    print()
    print("=" * 55)
    print("PART B — Iterative DFS from Alice")
    print("=" * 55)
    print(" ", dfs_iterative(g, "Alice"))

    print()
    print("=" * 55)
    print("PART C — Connected Components")
    print("=" * 55)
    components = find_connected_components(g)
    for i, comp in enumerate(components):
        print(f"  Component {i + 1}: {comp}")

    print()
    print("=" * 55)
    print("PART D — Is Graph Connected?")
    print("=" * 55)
    print(f"  Is connected: {is_connected(g)}")

    print()
    print("=" * 55)
    print("PART E — Has Path?")
    print("=" * 55)
    print(f"  Alice  → Diana : {has_path(g, 'Alice', 'Diana')}")
    print(f"  Alice  → Frank : {has_path(g, 'Alice', 'Frank')}")
    print(f"  Frank  → Grace : {has_path(g, 'Frank', 'Grace')}")
    print(f"  Alice  → Henry : {has_path(g, 'Alice', 'Henry')}")

    print()
    print("=" * 55)
    print("PART F — Find Actual Path")
    print("=" * 55)
    print(f"  Alice  → Diana : {find_path(g, 'Alice', 'Diana')}")
    print(f"  Alice  → Eve   : {find_path(g, 'Alice', 'Eve')}")
    print(f"  Alice  → Frank : {find_path(g, 'Alice', 'Frank')}")

    print()
    print("=" * 55)
    print("ANALYTICS")
    print("=" * 55)
    print(f"  Component sizes   : {get_connected_components_sizes(g)}")

    print(f"  Largest component : {find_largest_component(g)}")

    print(f"  Isolated users    : {find_isolated_users(g)}")
