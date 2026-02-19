def mutual_friends_system(friends_of_user1, friends_of_user2, network):

    A = set(friends_of_user1)
    B = set(friends_of_user2)

    common = A.intersection(B)

    unique_A = A.difference(B)
    unique_B = B.difference(A)

    all_friends = A.union(B)

    if len(all_friends) > 0:
        jaccard = len(common) / len(all_friends)
    else:
        jaccard = 0

    recommendations = set()

    for friend in A:
        if friend in network:
            recommendations.update(network[friend])

    recommendations = recommendations - A
    recommendations.discard("user1")

    return common, unique_A, unique_B, jaccard, recommendations


network = {
    "A": {"B", "C", "D"},
    "B": {"A", "E"},
    "C": {"A", "F"},
    "D": {"A"},
    "E": {"B"},
    "F": {"C"}
}

user1_friends = {"B", "C", "D"}
user2_friends = {"C", "E"}

result = mutual_friends_system(user1_friends, user2_friends, network)

print("Common:", result[0])
print("Unique A:", result[1])
print("Unique B:", result[2])
print("Jaccard:", result[3])
print("Recommendations:", result[4])
