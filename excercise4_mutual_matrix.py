#!/usr/bin/env python3

class FollowerMatrix:
    def __init__(self, N):
        self.size = N
        self.user_count = N
        self.matrix = [[False for _ in range(N)] for _ in range(N)]

    def Follow(self, follower, followee):
        self.matrix[follower][followee] = True

    def Unfollow(self, follower, followee):
        self.matrix[follower][followee] = False

    def Is_following(self, follower, followee):
        return self.matrix[follower][followee]

    def Get_followers(self, user):
        followers = []
        for i in range(self.size):
            if self.matrix[i][user]:
                followers.append(i)
        return followers

    def Get_following(self, user):
        following = []
        for j in range(self.size):
            if self.matrix[user][j]:
                following.append(j)
        return following

    def Find_mutual_followers(self):
        mutual = [[False for _ in range(self.size)] for _ in range(self.size)]
        for i in range(self.size):
            for j in range(self.size):
                if self.matrix[i][j] and self.matrix[j][i]:
                    mutual[i][j] = True
        return mutual

    def Get_influence_score(self, user):
        followers_count = len(self.Get_followers(user))
        following_count = len(self.Get_following(user))
        return (followers_count + following_count) / self.user_count


fm = FollowerMatrix(3)

fm.Follow(0, 1)
fm.Follow(1, 0)
fm.Follow(1, 2)

print("Followers of User 1:", fm.Get_followers(1))
print("Following of User 1:", fm.Get_following(1))

print("Mutual Followers Matrix:")
for row in fm.Find_mutual_followers():
    print(row)

print("Influence Score of User 1:", fm.Get_influence_score(1))