
class CategoryNode:
    def __init__(self, category_id, name, post_count):
        self.category_id = category_id
        self.name        = name
        self.post_count  = post_count
        self.left        = None
        self.right       = None
        self.parent      = None

    def __repr__(self):
        return f"{self.name}({self.post_count})"



def calculate_height(node):
    if node is None:
        return -1
    left_height  = calculate_height(node.left)
    right_height = calculate_height(node.right)
    return 1 + max(left_height, right_height)


def calculate_node_depth(node, target_id, depth=0):
    if node is None:
        return -1
    if node.category_id == target_id:
        return depth
    left_result = calculate_node_depth(node.left,  target_id, depth + 1)
    if left_result != -1:
        return left_result
    return calculate_node_depth(node.right, target_id, depth + 1)


def calculate_node_height(node, target_id):
    target_node = find_category(node, target_id)
    if target_node is None:
        return -1
    return calculate_height(target_node)


def count_nodes(node):
    if node is None:
        return 0
    return 1 + count_nodes(node.left) + count_nodes(node.right)


def count_leaves(node):
    if node is None:
        return 0
    if node.left is None and node.right is None:
        return 1
    return count_leaves(node.left) + count_leaves(node.right)


def is_balanced(node):
    def check(node):
        if node is None:
            return 0, True
        left_h,  left_ok  = check(node.left)
        right_h, right_ok = check(node.right)
        balanced = left_ok and right_ok and abs(left_h - right_h) <= 1
        return 1 + max(left_h, right_h), balanced

    _, result = check(node)
    return result



def is_full_binary_tree(node):
    if node is None:
        return True
    if node.left is None and node.right is None:
        return True
    if node.left is not None and node.right is not None:
        return is_full_binary_tree(node.left) and is_full_binary_tree(node.right)
    return False


def is_perfect_binary_tree(node):
    height = calculate_height(node)
    total  = count_nodes(node)
    return total == (2 ** (height + 1)) - 1


def is_complete_binary_tree(node):
    if node is None:
        return True

    queue = [node]
    found_null = False

    while queue:
        current = queue.pop(0)

        if current.left is not None:
            if found_null:
                return False
            queue.append(current.left)
        else:
            found_null = True

        if current.right is not None:
            if found_null:
                return False
            queue.append(current.right)
        else:
            found_null = True

    return True



def find_category(node, target):
    if node is None:
        return None
    if isinstance(target, int):
        matched = (node.category_id == target)
    else:
        matched = (node.name == target)
    if matched:
        return node
    left_result = find_category(node.left, target)
    if left_result:
        return left_result
    return find_category(node.right, target)


def find_path_to_root(node, target, path=None):
    if path is None:
        path = []
    if node is None:
        return None

    path.append(node.name)

    if isinstance(target, int):
        matched = (node.category_id == target)
    else:
        matched = (node.name == target)

    if matched:
        return list(reversed(path))

    left_result = find_path_to_root(node.left,  target, path)
    if left_result:
        return left_result

    right_result = find_path_to_root(node.right, target, path)
    if right_result:
        return right_result

    path.pop()
    return None


def lowest_common_ancestor(node, value1, value2):
    if node is None:
        return None

    if isinstance(value1, int):
        match1 = (node.category_id == value1)
    else:
        match1 = (node.name == value1)

    if isinstance(value2, int):
        match2 = (node.category_id == value2)
    else:
        match2 = (node.name == value2)

    if match1 or match2:
        return node

    left_lca  = lowest_common_ancestor(node.left,  value1, value2)
    right_lca = lowest_common_ancestor(node.right, value1, value2)

    if left_lca and right_lca:
        return node

    return left_lca if left_lca else right_lca



if __name__ == "__main__":


    tech   = CategoryNode(1, "Technology",   150)
    prog   = CategoryNode(2, "Programming",   85)
    design = CategoryNode(3, "Design",         65)
    python = CategoryNode(4, "Python",         42)
    java   = CategoryNode(5, "Java",           30)
    uiux   = CategoryNode(6, "UI/UX",          38)
    gfx    = CategoryNode(7, "Graphics",       22)
    django = CategoryNode(8, "Django",         18)
    flask  = CategoryNode(9, "Flask",          12)

    tech.left    = prog
    tech.right   = design
    prog.left    = python
    prog.right   = java
    design.left  = uiux
    design.right = gfx
    python.left  = django
    python.right = flask

    prog.parent   = tech
    design.parent = tech
    python.parent = prog
    java.parent   = prog
    uiux.parent   = design
    gfx.parent    = design
    django.parent = python
    flask.parent  = python

    print("=" * 55)
    print("TREE METRICS")
    print("=" * 55)
    print(f"  Tree height              : {calculate_height(tech)}")

    print(f"  Depth of Java            : {calculate_node_depth(tech, java.category_id)}")

    print(f"  Total nodes              : {count_nodes(tech)}")

    print(f"  Leaf nodes               : {count_leaves(tech)}")

    print(f"  Is balanced?             : {is_balanced(tech)}")

    print()
    print("=" * 55)
    print("TREE PROPERTY VERIFICATION")
    print("=" * 55)
    print(f"  Is full binary tree?     : {is_full_binary_tree(tech)}")
    print(f"  Is perfect binary tree?  : {is_perfect_binary_tree(tech)}")
    print(f"  Is complete binary tree? : {is_complete_binary_tree(tech)}")

    print()
    print("=" * 55)
    print("SEARCH AND NAVIGATION")
    print("=" * 55)

    found = find_category(tech, "Python")
    print(f"  find_category('Python')              : {found}")

    path = find_path_to_root(tech, "Django")
    print(f"  find_path_to_root('Django')          : {path}")

    lca = lowest_common_ancestor(tech, "Django", "Java")
    print(f"  lowest_common_ancestor(Django, Java) : {lca}")

    lca2 = lowest_common_ancestor(tech, "Python", "Design")
    print(f"  lowest_common_ancestor(Python,Design): {lca2}")
