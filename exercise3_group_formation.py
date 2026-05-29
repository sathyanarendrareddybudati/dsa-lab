import random
import math
def count_cross_edges(groupA, groupB, graph):
    set_B = set(groupB)
    count = 0
    for user in groupA:
        for neighbor in graph.get_friends(user):
            if neighbor in set_B:
                count += 1
    return count
def find_balanced_partition_greedy(graph):
    users = list(graph.all_users)
    n = len(users)
    min_size = math.ceil(0.4 * n)
    random.shuffle(users)
    groupA = users[: n // 2]
    groupB = users[n // 2:]
    improved = True
    while improved:
        improved = False
        for user in users:
            if user in groupA:
                new_A = [u for u in groupA if u != user]
                new_B = groupB + [user]
            else:
                new_A = groupA + [user]
                new_B = [u for u in groupB if u != user]
            if len(new_A) < min_size or len(new_B) < min_size:
                continue
            new_cross = count_cross_edges(new_A, new_B, graph)
            old_cross = count_cross_edges(groupA, groupB, graph)
            if new_cross < old_cross:
                groupA = new_A
                groupB = new_B
                improved = True
                break
    return (
        count_cross_edges(groupA, groupB, graph),
        groupA,
        groupB
    )
def find_balanced_partition_local_search(graph, iterations):
    best_cross = float("inf")
    best_groupA = None
    best_groupB = None
    for i in range(iterations):
        cross, groupA, groupB = find_balanced_partition_greedy(graph)
        if cross < best_cross:
            best_cross = cross
            best_groupA = groupA
            best_groupB = groupB
    return (
        best_cross,
        best_groupA,
        best_groupB
    )
