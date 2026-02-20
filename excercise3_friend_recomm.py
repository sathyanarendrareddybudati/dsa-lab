import math


def cosine_similarity(userA, userB):

    dot_product = 0
    normA = 0
    normB = 0

    for i in range(len(userA)):
        dot_product += userA[i] * userB[i]
        normA += userA[i] * userA[i]
        normB += userB[i] * userB[i]

    normA = math.sqrt(normA)
    normB = math.sqrt(normB)

    if normA == 0 or normB == 0:
        return 0

    return dot_product / (normA * normB)


def top_k_similar_users(matrix, targetUser, K, friendships):

    similarities = []
    number_of_users = len(matrix)

    for u in range(number_of_users):

        if u == targetUser:
            continue

        if targetUser in friendships and u in friendships[targetUser]:
            continue

        sim = cosine_similarity(matrix[targetUser], matrix[u])

        similarities.append((u, sim))

    similarities.sort(key=lambda x: x[1], reverse=True)

    return similarities[:K]


def recommend_interests(matrix, targetUser, K, friendships):

    similarUsers = top_k_similar_users(matrix, targetUser, K, friendships)

    recommendations = []
    number_of_interests = len(matrix[0])

    for i in range(number_of_interests):

        if matrix[targetUser][i] != 0:
            continue

        weighted_sum = 0
        similarity_sum = 0

        for userIndex, similarity in similarUsers:
            weighted_sum += similarity * matrix[userIndex][i]
            similarity_sum += similarity

        if similarity_sum > 0:
            predicted_score = weighted_sum / similarity_sum
            recommendations.append((i, predicted_score))

    recommendations.sort(key=lambda x: x[1], reverse=True)

    return recommendations


def reduce_dimensions(matrix, groups):

    reduced_matrix = []

    for user in matrix:

        reduced_user = []

        for group in groups:

            total = 0

            for interest_index in group:
                total += user[interest_index]

            average = total / len(group)
            reduced_user.append(average)

        reduced_matrix.append(reduced_user)

    return reduced_matrix
