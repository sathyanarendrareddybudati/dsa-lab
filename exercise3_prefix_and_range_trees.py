class TrieNode:
    def __init__(self):
        self.children = {}   
        self.is_end = False
        self.user_id = None
class AutocompleteTrie:
    def __init__(self):
        self.root = TrieNode()
        self.total_words = 0
    def insert(self, username, user_id):
        node = self.root
        for ch in username:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        if not node.is_end:
            self.total_words += 1
        node.is_end = True
        node.user_id = user_id
    def search(self, username):
        node = self.root
        for ch in username:
            if ch not in node.children:
                return None
            node = node.children[ch]
        if node.is_end:
            return node.user_id
        return None
    def starts_with(self, prefix):
        node = self.root
        for ch in prefix:
            if ch not in node.children:
                return False
            node = node.children[ch]
        return True
    def _dfs(self, node, prefix, results, max_results):
        if len(results) >= max_results:
            return
        if node.is_end:
            results.append((prefix, node.user_id))
        for ch in node.children:
            self._dfs(node.children[ch], prefix + ch, results, max_results)
    def autocomplete(self, prefix, max_results=10):
        node = self.root
        for ch in prefix:
            if ch not in node.children:
                return []
            node = node.children[ch]
        results = []
        self._dfs(node, prefix, results, max_results)
        return results
    def count_words(self):
        return self.total_words
    def _get_height(self, node):
        if not node.children:
            return 0
        return 1 + max(self._get_height(child) for child in node.children.values())
    def get_height(self):
        return self._get_height(self.root)
    def _count_nodes(self, node):
        count = 1
        for child in node.children.values():
            count += self._count_nodes(child)
        return count
    def get_total_nodes(self):
        return self._count_nodes(self.root)
    def delete(self, username):
        def _delete(node, word, depth):
            if depth == len(word):
                if not node.is_end:
                    return False
                node.is_end = False
                node.user_id = None
                self.total_words -= 1
                return len(node.children) == 0
            ch = word[depth]
            if ch not in node.children:
                return False  
            should_delete = _delete(node.children[ch], word, depth + 1)
            if should_delete:
                del node.children[ch]
                return not node.is_end and len(node.children) == 0
            return False
        _delete(self.root, username, 0)
trie = AutocompleteTrie()
users = ["alice", "bob", "alice123", "alex", "albert"]
for i, u in enumerate(users):
    trie.insert(u, i)
print(trie.autocomplete("al"))
print(trie.search("bob"))
print(trie.count_words())
import random
class ActivitySegmentTree:
    def __init__(self, activity):
        self.n = len(activity)
        self.tree = [0] * (4 * self.n)
        self.data = activity[:]
        self.build(0, 0, self.n - 1)
    def build(self, idx, left, right):
        if left == right:
            self.tree[idx] = self.data[left]
            return
        mid = (left + right) // 2
        self.build(2 * idx + 1, left, mid)
        self.build(2 * idx + 2, mid + 1, right)  
        self.tree[idx] = self.tree[2 * idx + 1] + self.tree[2 * idx + 2]
    def query(self, l, r):
        return self._query(0, 0, self.n - 1, l, r)
    def _query(self, idx, left, right, l, r):
        if r < left or l > right:
            return 0
        if l <= left and right <= r:
            return self.tree[idx]
        mid = (left + right) // 2
        return (self._query(2 * idx + 1, left, mid, l, r) +
                self._query(2 * idx + 2, mid + 1, right, l, r))
    def get_range_max(self, l, r):
        return max(self.data[l:r+1])
    def get_range_min(self, l, r):
        return min(self.data[l:r+1])
    def get_tree_size(self):
        return len(self.tree)
    def get_height(self):
        import math
        return math.ceil(math.log2(self.n)) if self.n > 0 else 0
    def get_leaf_values(self):
        return self.data
activity = [random.randint(0, 1000) for _ in range(30)]
seg = ActivitySegmentTree(activity)
print("Last 7 days total:", seg.query(23, 29))
for i in range(24):
    print(f"Days {i}-{i+6}:", seg.query(i, i+6))
