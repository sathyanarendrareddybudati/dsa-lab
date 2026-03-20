from datetime import datetime


class CommentNode:
    def __init__(self, comment_id, user_id, content, likes=0, timestamp=None):
        self.comment_id = comment_id
        self.user_id = user_id
        self.content = content[:100]
        self.likes = likes
        self.timestamp = timestamp or datetime.now()
        self.replies = []

    def __repr__(self):
        return f"Comment({self.comment_id}, {self.user_id}: '{self.content}')"


def display_thread(comment, level=0):
    indent = "  " * level
    print(f"{indent}[ID {comment.comment_id}] {comment.user_id}: {comment.content}  ❤ {comment.likes}")
    for reply in comment.replies:
        display_thread(reply, level + 1)


def count_total_comments(comment):
    total = 1
    for reply in comment.replies:
        total += count_total_comments(reply)
    return total


def total_likes(comment):
    total = comment.likes
    for reply in comment.replies:
        total += total_likes(reply)
    return total


def find_deepest_reply(comment):
    if not comment.replies:
        return 0
    max_depth = 0
    for reply in comment.replies:
        depth = find_deepest_reply(reply)
        if depth > max_depth:
            max_depth = depth
    return max_depth + 1


def search_by_user(user_id, comment):
    result = []
    if comment.user_id == user_id:
        result.append(comment)
    for reply in comment.replies:
        result += search_by_user(user_id, reply)
    return result


def contains_keyword(keyword, comment):
    if keyword.lower() in comment.content.lower():
        return True
    for reply in comment.replies:
        if contains_keyword(keyword, reply):
            return True
    return False


def delete_comment(comment_id, thread):
    if thread.comment_id == comment_id:
        return None

    new_replies = []
    for reply in thread.replies:
        result = delete_comment(comment_id, reply)
        if result is not None:
            new_replies.append(result)

    thread.replies = new_replies
    return thread


if __name__ == "__main__":
    c101 = CommentNode(101, "Alice", "This recipe looks amazing!", likes=10)
    c201 = CommentNode(201, "Bob", "I tried it last night!", likes=5)
    c301 = CommentNode(301, "Alice", "What did you think?", likes=3)
    c401 = CommentNode(401, "Bob", "It was delicious!", likes=8)
    c202 = CommentNode(202, "Charlie", "Can I use olive oil instead?", likes=2)
    c302 = CommentNode(302, "Alice", "Yes, that works too!", likes=4)

    c301.replies = [c401]
    c201.replies = [c301]
    c202.replies = [c302]
    c101.replies = [c201, c202]

    print("=" * 55)
    print("DISPLAY THREAD")
    print("=" * 55)
    display_thread(c101)

    print()
    print("=" * 55)
    print("COUNT TOTAL COMMENTS")
    print("=" * 55)
    count = count_total_comments(c101)
    print(f"  Total comments in thread: {count}")

    print()
    print("=" * 55)
    print("TOTAL LIKES")
    print("=" * 55)
    likes = total_likes(c101)
    print(f"  Total likes in thread: {likes}")

    print()
    print("=" * 55)
    print("FIND DEEPEST REPLY")
    print("=" * 55)
    depth = find_deepest_reply(c101)
    print(f"  Maximum nesting depth: {depth}")

    print()
    print("=" * 55)
    print("SEARCH BY USER — Alice")
    print("=" * 55)
    alice_comments = search_by_user("Alice", c101)
    for c in alice_comments:
        print(f"  {c}")

    print()
    print("=" * 55)
    print("CONTAINS KEYWORD")
    print("=" * 55)
    print(f"  'delicious' found: {contains_keyword('delicious', c101)}")
    print(f"  'pizza'     found: {contains_keyword('pizza', c101)}")
    print(f"  'olive'     found: {contains_keyword('olive', c101)}")

    print()
    print("=" * 55)
    print("DELETE COMMENT 201 (cascades 301 and 401 too)")
    print("=" * 55)
    print("  Thread BEFORE delete:")
    display_thread(c101)

    delete_comment(201, c101)

    print()
    print("  Thread AFTER delete:")
    display_thread(c101)