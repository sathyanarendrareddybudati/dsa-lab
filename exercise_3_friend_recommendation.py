#!/usr/bin/env python3
import math
class FriendRecommender:
    def __init__(self, matrix, friendships):
        self.matrix = matrix
        self.users = len(matrix)
        self.interests = len(matrix[0])
        self.friendships = friendships
    def cosine_similarity(self, a, b):
        dot = sum(a[i] * b[i] for i in range(self.interests))
        norm_a = math.sqrt(sum(a[i] * a[i] for i in range(self.interests)))
        norm_b = math.sqrt(sum(b[i] * b[i] for i in range(self.interests)))
        if norm_a == 0 or norm_b == 0:
            return 0
        return dot / (norm_a * norm_b)
    def compute_similarity_matrix(self):
        sim = [[0]*self.users for _ in range(self.users)]
        for i in range(self.users):
            for j in range(self.users):
                sim[i][j] = self.cosine_similarity(self.matrix[i], self.matrix[j])
        return sim
    def recommend_friends(self, user, k):
        scores = []
        for other in range(self.users):
            if other != user and other not in self.friendships[user]:
                s = self.cosine_similarity(self.matrix[user], self.matrix[other])
                scores.append((other, s))
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:k]
    def recommend_interests(self, user):
        sim_scores = []
        for other in range(self.users):
            if other != user:
                s = self.cosine_similarity(self.matrix[user], self.matrix[other])
                sim_scores.append((other, s))
        sim_scores.sort(key=lambda x: x[1], reverse=True)
        recommendations = [0]*self.interests
        for other, score in sim_scores:
            for i in range(self.interests):
                if self.matrix[user][i] == 0:
                    recommendations[i] += self.matrix[other][i] * score
        return recommendations
matrix = [
    [10, 0, 8, 2, 5, 7],
    [9, 1, 7, 3, 6, 8],
    [2, 9, 1, 8, 3, 0]
]
friendships = {
    0: [1],
    1: [0],
    2: []
}
fr = FriendRecommender(matrix, friendships)
print("Similarity Matrix:")
for row in fr.compute_similarity_matrix():
    print(row)
print("Top Friend Recommendations for User 0:", fr.recommend_friends(0, 2))
print("Interest Recommendations for User 0:", fr.recommend_interests(0))

