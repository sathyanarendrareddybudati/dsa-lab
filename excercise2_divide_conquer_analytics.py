
class Post:
    def __init__(self, post_id, user_id, content_preview, likes, comments, shares):
        self.post_id         = post_id
        self.user_id         = user_id
        self.content_preview = content_preview
        self.likes           = likes
        self.comments        = comments
        self.shares          = shares
        self.engagement_score = (likes * 1) + (comments * 2) + (shares * 3)

    def __repr__(self):
        return f"Post{self.post_id}(score={self.engagement_score})"


def max_engagement(posts, left, right):

    if left == right:
        return posts[left].engagement_score

    mid = (left + right) // 2

    left_max  = max_engagement(posts, left, mid)
    right_max = max_engagement(posts, mid + 1, right)

    if left_max >= right_max:
        return left_max
    else:
        return right_max


def sum_engagement(posts, left, right):
    if left == right:
        return posts[left].engagement_score

    mid = (left + right) // 2

    return sum_engagement(posts, left, mid) + sum_engagement(posts, mid + 1, right)


def average_engagement(posts, left, right):
    total = sum_engagement(posts, left, right)
    count = right - left + 1
    return total / count


def count_above_threshold(posts, left, right, threshold):

    if left == right:
        return 1 if posts[left].engagement_score > threshold else 0

    mid = (left + right) // 2

    return (count_above_threshold(posts, left, mid, threshold) +
            count_above_threshold(posts, mid + 1, right, threshold))


def merge_sort_by_engagement(posts, left, right):

    if left >= right:
        return

    mid = (left + right) // 2

    merge_sort_by_engagement(posts, left, mid)
    merge_sort_by_engagement(posts, mid + 1, right)
    merge(posts, left, mid, right)


def merge(posts, left, mid, right):
    left_part  = posts[left : mid + 1]
    right_part = posts[mid + 1 : right + 1]

    i = 0
    j = 0
    k = left

    while i < len(left_part) and j < len(right_part):
        if left_part[i].engagement_score <= right_part[j].engagement_score:
            posts[k] = left_part[i]
            i += 1
        else:
            posts[k] = right_part[j]
            j += 1
        k += 1

    while i < len(left_part):
        posts[k] = left_part[i]
        i += 1
        k += 1

    while j < len(right_part):
        posts[k] = right_part[j]
        j += 1
        k += 1



def find_peak_hour(likes, left, right):

    if left == right:
        return left

    mid = (left + right) // 2

    if likes[mid] < likes[mid + 1]:
        return find_peak_hour(likes, mid + 1, right)
    else:
        return find_peak_hour(likes, left, mid)



if __name__ == "__main__":

    posts = [
        Post(1, "alice", "Post 1 content", likes=50,  comments=30, shares=10),
        Post(2, "bob",   "Post 2 content", likes=100, comments=60, shares=20),
        Post(3, "carol", "Post 3 content", likes=30,  comments=20, shares=5),
        Post(4, "dave",  "Post 4 content", likes=80,  comments=50, shares=20),
    ]

    posts[0].engagement_score = 150
    posts[1].engagement_score = 320
    posts[2].engagement_score = 95
    posts[3].engagement_score = 280

    print("=" * 50)
    print("POSTS")
    print("=" * 50)
    for p in posts:
        print(f"  {p}")

    print()
    print("=" * 50)
    print("PART A — Max Engagement")
    print("=" * 50)
    result = max_engagement(posts, 0, 3)
    print(f"  max_engagement(posts, 0, 3) → {result}")

    print()
    print("=" * 50)
    print("PART B — Sum and Average")
    print("=" * 50)
    total = sum_engagement(posts, 0, 3)
    avg   = average_engagement(posts, 0, 3)
    print(f"  sum_engagement(posts, 0, 3)     → {total}")
    print(f"  average_engagement(posts, 0, 3) → {avg}")

    print()
    print("=" * 50)
    print("PART C — Count Above Threshold (200)")
    print("=" * 50)
    count = count_above_threshold(posts, 0, 3, 200)
    print(f"  count_above_threshold(posts, 0, 3, 200) → {count}")

    print()
    print("=" * 50)
    print("PART D — Merge Sort by Engagement")
    print("=" * 50)
    print(f"  Before sort: {posts}")
    merge_sort_by_engagement(posts, 0, 3)
    print(f"  After sort:  {posts}")

    print()
    print("=" * 50)
    print("PART D — Peak Hour")
    print("=" * 50)
    hourly_likes = [5, 8, 12, 25, 30, 28, 15, 10, 6, 4, 3, 2, 1, 2, 3, 5, 7, 6, 4, 3, 2, 1, 1, 1]
    peak = find_peak_hour(hourly_likes, 0, 23)
    print(f"  find_peak_hour(likes, 0, 23) → hour {peak} ({hourly_likes[peak]} likes)")