import random, time, math, copy


class TrendingHeap:
    def __init__(self):
        self.heap = []
        self.pos_map = {}

    def _swap(self, i, j):
        self.pos_map[self.heap[i][1]] = j
        self.pos_map[self.heap[j][1]] = i
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

    def _bubble_up(self, i):
        while i > 0:
            parent = (i - 1) // 2
            if self.heap[i][0] > self.heap[parent][0]:
                self._swap(i, parent)
                i = parent
            else:
                break

    def _bubble_down(self, i):
        n = len(self.heap)
        while True:
            largest = i
            left = 2 * i + 1
            right = 2 * i + 2

            if left < n and self.heap[left][0] > self.heap[largest][0]:
                largest = left
            if right < n and self.heap[right][0] > self.heap[largest][0]:
                largest = right

            if largest != i:
                self._swap(i, largest)
                i = largest
            else:
                break

    def push(self, post_id, likes, timestamp):
        entry = [likes, post_id, timestamp]
        self.heap.append(entry)
        self.pos_map[post_id] = len(self.heap) - 1
        self._bubble_up(len(self.heap) - 1)

    def pop_max(self):
        if not self.heap:
            return None

        max_entry = self.heap[0][:]

        last = self.heap.pop()
        del self.pos_map[max_entry[1]]

        if self.heap:
            self.heap[0] = last
            self.pos_map[last[1]] = 0
            self._bubble_down(0)

        return max_entry

    def peek_max(self):
        if not self.heap:
            return None
        return self.heap[0]

    def get_top_k(self, k):
        temp = TrendingHeap()
        temp.heap = copy.deepcopy(self.heap)
        temp.pos_map = copy.deepcopy(self.pos_map)

        result = []
        for _ in range(min(k, len(temp.heap))):
            result.append(temp.pop_max())
        return result

    def update_likes(self, post_id, new_likes, timestamp):
        if post_id not in self.pos_map:
            return False

        i = self.pos_map[post_id]
        old_likes = self.heap[i][0]

        self.heap[i][0] = new_likes
        self.heap[i][2] = timestamp

        if new_likes > old_likes:
            self._bubble_up(i)
        else:
            self._bubble_down(i)

        return True

    def size(self):
        return len(self.heap)

    def is_valid_heap(self):
        for i in range(1, len(self.heap)):
            parent = (i - 1) // 2
            if self.heap[i][0] > self.heap[parent][0]:
                return False
        return True

    def get_height(self):
        if not self.heap:
            return -1
        return math.floor(math.log2(len(self.heap)))

    def get_level_order(self):
        if not self.heap:
            return []

        result = []
        level = 0
        start = 0

        while start < len(self.heap):
            end = min(start + (2**level), len(self.heap))
            level_list = self.heap[start:end]
            result.append(level_list)
            start = end
            level += 1

        return result

    def display_heap(self):
        levels = self.get_level_order()
        print("  Heap level order:")
        for i, level in enumerate(levels):
            entries = [f"Post{e[1]}({e[0]}likes)" for e in level]
            print(f"    Level {i}: {' | '.join(entries)}")


def simulate_trending_feed():
    print("=" * 55)
    print("TRENDING FEED SIMULATION")
    print("=" * 55)

    heap = TrendingHeap()
    post_ids = list(range(1, 101))
    likes_map = {}

    print("\n  Initializing 100 posts...")
    for post_id in post_ids:
        likes = random.randint(0, 1000)
        likes_map[post_id] = likes
        heap.push(post_id, likes, time.time())

    print(f"  Heap size      : {heap.size()}")
    print(f"  Heap valid     : {heap.is_valid_heap()}")
    print(f"  Heap height    : {heap.get_height()}")

    print("\n  Initial top 5 posts:")
    for entry in heap.get_top_k(5):
        print(f"    Post{entry[1]:>3} → {entry[0]} likes")

    print()
    start_time = time.time()

    for update in range(1, 10001):
        post_id = random.choice(post_ids)
        increment = random.randint(1, 50)
        likes_map[post_id] += increment
        heap.update_likes(post_id, likes_map[post_id], time.time())

        if update % 1000 == 0:
            elapsed = time.time() - start_time
            top5 = heap.get_top_k(5)
            print(f"  After {update:>5} updates (elapsed {elapsed:.3f}s) → Top 5:")
            for entry in top5:
                print(f"    Post{entry[1]:>3} → {entry[0]} likes")
            print()

    total_time = time.time() - start_time
    print(f"  Total time for 10,000 updates : {total_time:.4f}s")
    print(f"  Average time per update       : {(total_time/10000)*1000:.4f}ms")
    print(f"  Heap still valid after sim    : {heap.is_valid_heap()}")


if __name__ == "__main__":

    print("=" * 55)
    print("CORE HEAP OPERATIONS")
    print("=" * 55)

    h = TrendingHeap()
    h.push(1, 500, time.time())
    h.push(2, 320, time.time())
    h.push(3, 780, time.time())
    h.push(4, 150, time.time())
    h.push(5, 640, time.time())
    h.push(6, 910, time.time())
    h.push(7, 430, time.time())

    print(f"\n  size()         : {h.size()}")
    print(f"  peek_max()     : Post{h.peek_max()[1]} ({h.peek_max()[0]} likes)")
    print(f"  is_valid_heap(): {h.is_valid_heap()}")
    print(f"  get_height()   : {h.get_height()}")

    print("\n  get_top_k(3):")
    for entry in h.get_top_k(3):
        print(f"    Post{entry[1]} → {entry[0]} likes")

    print(f"\n  Heap still intact after get_top_k: {h.size()} posts")

    print("\n  update_likes(Post2, 950):")
    h.update_likes(2, 950, time.time())
    print(f"  peek_max() now : Post{h.peek_max()[1]} ({h.peek_max()[0]} likes)")
    print(f"  is_valid_heap(): {h.is_valid_heap()}")

    print("\n  pop_max():")
    popped = h.pop_max()
    print(f"  Popped         : Post{popped[1]} ({popped[0]} likes)")
    print(f"  size() after   : {h.size()}")
    print(f"  peek_max() now : Post{h.peek_max()[1]} ({h.peek_max()[0]} likes)")
    print(f"  is_valid_heap(): {h.is_valid_heap()}")

    print()
    h.display_heap()

    print()
    print("=" * 55)
    print("EDGE CASES")
    print("=" * 55)

    empty = TrendingHeap()
    print(f"\n  pop_max on empty heap  : {empty.pop_max()}")
    print(f"  peek_max on empty heap : {empty.peek_max()}")
    print(f"  get_top_k(1000) with 3 posts:")

    small = TrendingHeap()
    small.push(1, 100, time.time())
    small.push(2, 200, time.time())
    small.push(3, 300, time.time())
    result = small.get_top_k(1000)
    print(f"    Returns {len(result)} posts (capped at heap size)")

    print(f"\n  update non-existent post: {small.update_likes(999, 500, time.time())}")

    print()
    random.seed(42)
    simulate_trending_feed()
