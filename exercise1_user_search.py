class UserNode:
    def __init__(self, user_id, name, friends_list):
        self.user_id  = user_id
        self.name     = name
        self.friends  = friends_list
        self.left     = None
        self.right    = None

    def __repr__(self):
        return f"User({self.user_id}, {self.name}, friends={self.friends})"

class UserBST:
    def __init__(self):
        self.root = None

    def insert(self, user_id, name, friends_list):
        self.root = self._insert(self.root, user_id, name, friends_list)

    def _insert(self, node, user_id, name, friends_list):
        if node is None:
            return UserNode(user_id, name, friends_list)
        if user_id < node.user_id:
            node.left  = self._insert(node.left,  user_id, name, friends_list)
        elif user_id > node.user_id:
            node.right = self._insert(node.right, user_id, name, friends_list)
        return node

    def find(self, user_id):
        return self._find(self.root, user_id)

    def _find(self, node, user_id):
        if node is None:
            return None
        if user_id == node.user_id:
            return node
        elif user_id < node.user_id:
            return self._find(node.left,  user_id)
        else:
            return self._find(node.right, user_id)

    def inorder_traversal(self):
        result = []
        self._inorder(self.root, result)
        return result

    def _inorder(self, node, result):
        if node is None:
            return
        self._inorder(node.left, result)
        result.append(node.user_id)
        self._inorder(node.right, result)

    def delete(self, user_id):
        self.root = self._delete(self.root, user_id)

    def _delete(self, node, user_id):
        if node is None:
            return None

        if user_id < node.user_id:
            node.left  = self._delete(node.left,  user_id)
        elif user_id > node.user_id:
            node.right = self._delete(node.right, user_id)
        else:
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left

            successor        = self._min_node(node.right)
            node.user_id     = successor.user_id
            node.name        = successor.name
            node.friends     = successor.friends
            node.right       = self._delete(node.right, successor.user_id)

        return node

    def _min_node(self, node):
        while node.left is not None:
            node = node.left
        return node

    def suggest_friends(self, user_id, max_suggestions=5):
        user = self.find(user_id)
        if user is None:
            return []

        direct_friends = set(user.friends)
        fof_count      = {}

        for friend_id in direct_friends:
            friend = self.find(friend_id)
            if friend is None:
                continue
            for fof_id in friend.friends:
                if fof_id == user_id:
                    continue
                if fof_id in direct_friends:
                    continue
                fof_count[fof_id] = fof_count.get(fof_id, 0) + 1

        sorted_fof = sorted(fof_count.items(), key=lambda x: x[1], reverse=True)
        return sorted_fof[:max_suggestions]

    def get_height(self):
        return self._height(self.root)

    def _height(self, node):
        if node is None:
            return -1
        return 1 + max(self._height(node.left), self._height(node.right))

    def is_balanced(self):
        return self._check_balanced(self.root) != -2

    def _check_balanced(self, node):
        if node is None:
            return 0
        left_h  = self._check_balanced(node.left)
        right_h = self._check_balanced(node.right)

        if left_h == -2 or right_h == -2:
            return -2
        if abs(left_h - right_h) > 1:
            return -2

        return 1 + max(left_h, right_h)

    def get_leaf_count(self):
        return self._count_leaves(self.root)

    def _count_leaves(self, node):
        if node is None:
            return 0
        if node.left is None and node.right is None:
            return 1
        return self._count_leaves(node.left) + self._count_leaves(node.right)

if __name__ == "__main__":

    bst = UserBST()
    bst.insert(5, "Eve",     [2, 7, 8])
    bst.insert(3, "Charlie", [1, 7])
    bst.insert(7, "Grace",   [3, 5])
    bst.insert(1, "Alice",   [2, 3, 4])
    bst.insert(4, "Diana",   [1, 6])
    bst.insert(6, "Frank",   [2, 4])
    bst.insert(2, "Bob",     [1, 5, 6])
    bst.insert(8, "Henry",   [5])

    print("=" * 55)
    print("IN-ORDER TRAVERSAL (sorted user IDs)")
    print("=" * 55)
    print(f"  {bst.inorder_traversal()}")

    print()
    print("=" * 55)
    print("FIND")
    print("=" * 55)
    print(f"  find(3)  → {bst.find(3)}")
    print(f"  find(99) → {bst.find(99)}")

    print()
    print("=" * 55)
    print("BST ANALYTICS")
    print("=" * 55)
    print(f"  get_height()    : {bst.get_height()}")
    print(f"  is_balanced()   : {bst.is_balanced()}")
    print(f"  get_leaf_count(): {bst.get_leaf_count()}")

    print()
    print("=" * 55)
    print("FRIEND-OF-FRIEND SUGGESTIONS")
    print("=" * 55)

    suggestions = bst.suggest_friends(1, max_suggestions=5)
    print(f"  Suggestions for Alice(1):")
    for user_id, mutual_count in suggestions:
        user = bst.find(user_id)
        name = user.name if user else "Unknown"
        print(f"    User {user_id} ({name}) — {mutual_count} mutual friend(s)")

    print()
    suggestions2 = bst.suggest_friends(5, max_suggestions=5)
    print(f"  Suggestions for Eve(5):")
    for user_id, mutual_count in suggestions2:
        user = bst.find(user_id)
        name = user.name if user else "Unknown"
        print(f"    User {user_id} ({name}) — {mutual_count} mutual friend(s)")

    print()
    print("=" * 55)
    print("DELETE")
    print("=" * 55)
    print(f"  Before delete: {bst.inorder_traversal()}")
    bst.delete(5)
    print(f"  After delete(5): {bst.inorder_traversal()}")
    print(f"  find(5) after delete: {bst.find(5)}")
    print(f"  is_balanced() after delete: {bst.is_balanced()}")

    print()
    print("=" * 55)
    print("EDGE CASES")
    print("=" * 55)
    print(f"  delete non-existent user(99): ", end="")
    bst.delete(99)
    print("no crash ✓")

    print(f"  suggest_friends for non-existent user(99): {bst.suggest_friends(99)}")

    print(f"  insert duplicate user(1): ", end="")
    bst.insert(1, "Alice_duplicate", [])
    print(f"  find(1) still → {bst.find(1).name} (original kept) ✓")