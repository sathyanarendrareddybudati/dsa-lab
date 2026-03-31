from datetime import datetime


class CategoryNode:
    def __init__(self, category_id, name, post_count):
        self.category_id = category_id
        self.name = name
        self.post_count = post_count
        self.left = None
        self.right = None
        self.parent = None

    def __repr__(self):
        return f"{self.name}({self.post_count})"


def in_order_collect(node):
    if node is None:
        return []
    return in_order_collect(node.left) + [node.name] + in_order_collect(node.right)


def in_order_accumulate_posts(node):
    if node is None:
        return 0
    total = in_order_accumulate_posts(node.left)
    total += node.post_count
    total += in_order_accumulate_posts(node.right)
    return total


def in_order_find_kth(node, k, counter=None):
    if counter is None:
        counter = [0]
    if node is None:
        return None

    result = in_order_find_kth(node.left, k, counter)
    if result:
        return result

    counter[0] += 1
    if counter[0] == k:
        return node

    return in_order_find_kth(node.right, k, counter)


def pre_order_export(node, level=0):
    if node is None:
        return
    indent = "  " * level
    print(f"{indent}{node.name}({node.post_count})")
    pre_order_export(node.left, level + 1)
    pre_order_export(node.right, level + 1)


def pre_order_copy(node):
    if node is None:
        return None
    new_node = CategoryNode(node.category_id, node.name, node.post_count)
    new_node.left = pre_order_copy(node.left)
    new_node.right = pre_order_copy(node.right)
    return new_node


def pre_order_serialize(node):
    if node is None:
        return ""
    parts = [f"{node.name}({node.post_count})"]
    left_part = pre_order_serialize(node.left)
    right_part = pre_order_serialize(node.right)
    if left_part:
        parts.append(left_part)
    if right_part:
        parts.append(right_part)
    return "|".join(parts)


def post_order_total_posts(node):
    if node is None:
        return 0
    left_total = post_order_total_posts(node.left)
    right_total = post_order_total_posts(node.right)
    return left_total + right_total + node.post_count


def post_order_collect_leaves(node):
    if node is None:
        return []
    if node.left is None and node.right is None:
        return [node]
    return post_order_collect_leaves(node.left) + post_order_collect_leaves(node.right)


def post_order_average_depth(node, current_depth=0):
    if node is None:
        return (0, 0)
    if node.left is None and node.right is None:
        return (current_depth, 1)
    left_depth, left_count = post_order_average_depth(node.left, current_depth + 1)
    right_depth, right_count = post_order_average_depth(node.right, current_depth + 1)
    return (left_depth + right_depth, left_count + right_count)


def find_most_popular_category(node):
    if node is None:
        return None
    best = node
    left_best = find_most_popular_category(node.left)
    right_best = find_most_popular_category(node.right)
    if left_best and left_best.post_count > best.post_count:
        best = left_best
    if right_best and right_best.post_count > best.post_count:
        best = right_best
    return best


def category_with_most_subcategories(node):
    if node is None:
        return (None, -1)

    direct = sum(1 for child in [node.left, node.right] if child is not None)
    best = (node, direct)

    left_best = category_with_most_subcategories(node.left)
    right_best = category_with_most_subcategories(node.right)

    if left_best[0] and left_best[1] > best[1]:
        best = left_best
    if right_best[0] and right_best[1] > best[1]:
        best = right_best

    return best


def distribution_by_depth(node, depth=0, dist=None):
    if dist is None:
        dist = {}
    if node is None:
        return dist
    dist[depth] = dist.get(depth, 0) + 1
    distribution_by_depth(node.left, depth + 1, dist)
    distribution_by_depth(node.right, depth + 1, dist)
    return dist


if __name__ == "__main__":

    tech = CategoryNode(1, "Technology", 150)
    prog = CategoryNode(2, "Programming", 85)
    design = CategoryNode(3, "Design", 65)
    python = CategoryNode(4, "Python", 42)
    java = CategoryNode(5, "Java", 30)
    uiux = CategoryNode(6, "UI/UX", 38)
    gfx = CategoryNode(7, "Graphics", 22)
    django = CategoryNode(8, "Django", 18)
    flask = CategoryNode(9, "Flask", 12)

    tech.left = prog
    tech.right = design
    prog.left = python
    prog.right = java
    design.left = uiux
    design.right = gfx
    python.left = django
    python.right = flask

    print("=" * 55)
    print("IN-ORDER TRAVERSAL")
    print("=" * 55)
    result = in_order_collect(tech)
    print("  " + " → ".join(result))

    print(f"\n  Accumulated posts (in-order): {in_order_accumulate_posts(tech)}")

    kth = in_order_find_kth(tech, 3)
    print(f"  3rd category in-order: {kth}")

    print()
    print("=" * 55)
    print("PRE-ORDER EXPORT")
    print("=" * 55)
    pre_order_export(tech)

    print()
    print("  Serialized:")
    print(" ", pre_order_serialize(tech))

    print()
    print("  Deep copy root name:", pre_order_copy(tech).name)

    print()
    print("=" * 55)
    print("POST-ORDER TOTAL POSTS")
    print("=" * 55)
    print(f"  Python subtree total  : {post_order_total_posts(python)}")
    print(f"  Programming subtree   : {post_order_total_posts(prog)}")
    print(f"  Design subtree        : {post_order_total_posts(design)}")
    print(f"  Full tree total       : {post_order_total_posts(tech)}")

    print()
    print("  Leaf categories:")
    for leaf in post_order_collect_leaves(tech):
        print(f"    {leaf}")

    total_depth, leaf_count = post_order_average_depth(tech)
    print(f"\n  Average leaf depth: {total_depth / leaf_count:.2f}")

    print()
    print("=" * 55)
    print("ANALYTICS")
    print("=" * 55)
    popular = find_most_popular_category(tech)
    print(f"  Most popular category        : {popular}")

    most_sub, count = category_with_most_subcategories(tech)
    print(f"  Category with most subcats   : {most_sub} ({count} children)")

    dist = distribution_by_depth(tech)
    print(f"  Distribution by depth        : {dist}")
