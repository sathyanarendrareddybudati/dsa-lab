from collections import deque
class BinaryNode:
    def __init__(self, category_id, name, post_count=0):
        self.category_id = category_id
        self.name = name
        self.post_count = post_count
        self.left = None
        self.right = None
   def __repr__(self):
        return f"BinaryNode({self.name})"
class GeneralizedCategoryNode:
    def __init__(self, category_id, name, post_count=0):
        self.category_id = category_id
        self.name = name
        self.post_count = post_count
        self.children = []
        self.parent = None
    def add_child(self, child_node):
        child_node.parent = self
        self.children.append(child_node)
    def __repr__(self):
        return f"GeneralizedNode({self.name}, children={[c.name for c in self.children]})"

def binary_to_generalized(binary_root, parent_gen=None):
        if binary_root is None:
        return None
    gen_node = GeneralizedCategoryNode(
        binary_root.category_id,
        binary_root.name,
        binary_root.post_count
    )
    child_bin = binary_root.left
    while child_bin is not None:
        child_gen = binary_to_generalized(child_bin, gen_node)
        gen_node.add_child(child_gen)
        child_bin = child_bin.right  
    return gen_node
def generalized_to_binary(gen_root):
       if gen_root is None:
        return None

    bin_node = BinaryNode(gen_root.category_id, gen_root.name, gen_root.post_count)

    if gen_root.children:
        bin_node.left = generalized_to_binary(gen_root.children[0])
        current = bin_node.left
        for sibling in gen_root.children[1:]:
            current.right = generalized_to_binary(sibling)
            current = current.right
    return bin_node
def pre_order_generalized(node):
    if node is None:
        return []
    result = [node.name]
    for child in node.children:
        result.extend(pre_order_generalized(child))
    return result
def post_order_generalized(node):
    if node is None:
        return []
    result = []
    for child in node.children:
        result.extend(post_order_generalized(child))
    result.append(node.name)
    return result
def level_order_generalized(node):
    if node is None:
        return []
        result = []
    queue = deque([node])
       while queue:
        current = queue.popleft()
        result.append(current.name)
        for child in current.children:
            queue.append(child)
        return result


def calculate_fan_out(node):
        if node is None:
        return 0
    max_children = len(node.children)
    for child in node.children:
        max_children = max(max_children, calculate_fan_out(child))
    return max_children
def calculate_height_generalized(node):
       if node is None:
        return -1
    if not node.children:
        return 0
    return 1 + max(calculate_height_generalized(child) for child in node.children)
def count_nodes_generalized(node):
    if node is None:
        return 0
    return 1 + sum(count_nodes_generalized(child) for child in node.children)
def count_leaves_generalized(node):
    if node is None:
        return 0
    if not node.children:
        return 1
    return sum(count_leaves_generalized(child) for child in node.children)
def calculate_branching_factor(node):
    total_children = 0
    non_leaf_count = 0
    def _walk(n):
        nonlocal total_children, non_leaf_count
        if n is None:
            return
        if n.children:
            non_leaf_count += 1
            total_children += len(n.children)
        for child in n.children:
            _walk(child)

    _walk(node)

    if non_leaf_count == 0:
        return 0.0
    return round(total_children / non_leaf_count, 2)
def build_example_tree():
    root = GeneralizedCategoryNode(1, "Technology", 0)

    programming = GeneralizedCategoryNode(2, "Programming", 120)
    python = GeneralizedCategoryNode(3, "Python", 80)
    django = GeneralizedCategoryNode(4, "Django", 40)
    flask = GeneralizedCategoryNode(5, "Flask", 30)
    java = GeneralizedCategoryNode(6, "Java", 50)

    design = GeneralizedCategoryNode(7, "Design", 90)
    uiux = GeneralizedCategoryNode(8, "UI/UX", 60)
    graphics = GeneralizedCategoryNode(9, "Graphics", 45)

    business = GeneralizedCategoryNode(10, "Business", 75)
    finance = GeneralizedCategoryNode(11, "Finance", 55)
    marketing = GeneralizedCategoryNode(12, "Marketing", 65)
    hr = GeneralizedCategoryNode(13, "HR", 30)

    python.add_child(django)
    python.add_child(flask)
    programming.add_child(python)
    programming.add_child(java)

    design.add_child(uiux)
    design.add_child(graphics)

    business.add_child(finance)
    business.add_child(marketing)
    business.add_child(hr)

    root.add_child(programming)
    root.add_child(design)
    root.add_child(business)

    return root
def calculate_total_posts(node):
        if node is None:
        return 0
    total = node.post_count
    for child in node.children:
        total += calculate_total_posts(child)
    return total
def find_most_subcategories(node):
        if node is None:
        return None

    best = node
    for child in node.children:
        candidate = find_most_subcategories(child)
        if candidate and len(candidate.children) > len(best.children):
            best = candidate

    return best


def find_all_leaves(node):
    
    if node is None:
        return []
    if not node.children:
        return [node]
    leaves = []
    for child in node.children:
        leaves.extend(find_all_leaves(child))
    return leaves


def export_tree_structure(node, indent=0):
    if node is None:
        return ""

    prefix = "    " * indent + ("└── " if indent > 0 else "")
    lines = [f"{prefix}{node.name} (posts: {node.post_count})"]

    for child in node.children:
        lines.append(export_tree_structure(child, indent + 1))

    return "\n".join(lines)


def check_deep_branches(node, max_depth=10, current_depth=0):
        problematic = []
    queue = deque([(node, 0)])

    while queue:
        current, depth = queue.popleft()
        if depth > max_depth:
            problematic.append((current.name, depth))
        for child in current.children:
            queue.append((child, depth + 1))

    return problematic


def categories_by_depth(node):
        if node is None:
        return {}

    depth_map = {}
    queue = deque([(node, 0)])

    while queue:
        current, depth = queue.popleft()
        depth_map.setdefault(depth, []).append(current.name)
        for child in current.children:
            queue.append((child, depth + 1))

    return depth_map
if __name__ == "__main__":
    print("=" * 60)
    print("  Exercise 3: Generalized Trees Demo")
    print("=" * 60)
    gen_root = build_example_tree()

    print("\n[Traversals]")
    print("Pre-order  :", pre_order_generalized(gen_root))
    print("Post-order :", post_order_generalized(gen_root))
    print("Level-order:", level_order_generalized(gen_root))

    print("\n[Tree Metrics]")
    print("Height          :", calculate_height_generalized(gen_root))
    print("Total nodes     :", count_nodes_generalized(gen_root))
    print("Leaf nodes      :", count_leaves_generalized(gen_root))
    print("Fan-out (max)   :", calculate_fan_out(gen_root))
    print("Branching factor:", calculate_branching_factor(gen_root))

    print("\n[Conversion: Generalized → Binary → Back to Generalized]")
    bin_root = generalized_to_binary(gen_root)
    print("Binary root     :", bin_root)
    print("Binary left     :", bin_root.left)     # first child (Programming)
    print("Binary left.right:", bin_root.left.right)  # sibling (Design)

    restored = binary_to_generalized(bin_root)
    print("Restored root   :", restored)
    print("Restored children:", [c.name for c in restored.children])

    print("\n[Analytics Dashboard]")

    tech_node = gen_root.children[0]  # Programming subtree for demo
    print("Total posts in Technology branch:", calculate_total_posts(gen_root))

    busiest = find_most_subcategories(gen_root)
    print("Most subcategories:", busiest.name, f"({len(busiest.children)} children)")

    leaves = find_all_leaves(gen_root)
    print("All leaf categories:", [l.name for l in leaves])

    print("\n[Tree Export]")
    print(export_tree_structure(gen_root))

    print("\n[Depth Distribution]")
    depth_map = categories_by_depth(gen_root)
    for depth, names in sorted(depth_map.items()):
        print(f"  Level {depth}: {names}")

    print("\n[Deep Branch Check (max_depth=2)]")
    deep = check_deep_branches(gen_root, max_depth=2)
    if deep:
        for name, depth in deep:
            print(f"  WARNING: '{name}' at depth {depth}")
    else:
        print("  No branches exceed depth 2")
