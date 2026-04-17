import random

class Region:
    def __init__(self, x, y, width, height):
        self.x      = x
        self.y      = y
        self.width  = width
        self.height = height

    def contains(self, px, py):
        return (self.x <= px < self.x + self.width and
                self.y <= py < self.y + self.height)

    def __repr__(self):
        return f"Region(x={self.x}, y={self.y}, w={self.width}, h={self.height})"

def split_region(x, y, width, height, min_size, level=0):
    region = Region(x, y, width, height)

    if width < min_size or height < min_size:
        print("  " * level + f"LEAF → {region}")
        return [region]

    print("  " * level + f"SPLIT → {region}")

    half_w = width  // 2
    half_h = height // 2

    top_left     = split_region(x,          y,          half_w, half_h, min_size, level + 1)
    top_right    = split_region(x + half_w, y,          half_w, half_h, min_size, level + 1)
    bottom_left  = split_region(x,          y + half_h, half_w, half_h, min_size, level + 1)
    bottom_right = split_region(x + half_w, y + half_h, half_w, half_h, min_size, level + 1)

    return top_left + top_right + bottom_left + bottom_right

def count_points_in_region(points, region):
    count = 0
    for (px, py) in points:
        if region.contains(px, py):
            count += 1
    return count

def find_dense_regions(points, x, y, width, height, min_size, density_threshold):
    region  = Region(x, y, width, height)
    area    = width * height
    count   = count_points_in_region(points, region)
    density = count / area if area > 0 else 0

    if width < min_size or height < min_size:
        if density > density_threshold:
            return [(region, count, round(density, 4))]
        return []

    half_w = width  // 2
    half_h = height // 2

    results = []
    results += find_dense_regions(points, x,          y,          half_w, half_h, min_size, density_threshold)
    results += find_dense_regions(points, x + half_w, y,          half_w, half_h, min_size, density_threshold)
    results += find_dense_regions(points, x,          y + half_h, half_w, half_h, min_size, density_threshold)
    results += find_dense_regions(points, x + half_w, y + half_h, half_w, half_h, min_size, density_threshold)

    return results

if __name__ == "__main__":

    print("=" * 55)
    print("SPLIT REGION (100x100, min_size=25)")
    print("=" * 55)
    leaves = split_region(0, 0, 100, 100, min_size=25)
    print(f"\n  Total leaf regions: {len(leaves)}")

    print()
    print("=" * 55)
    print("COUNT POINTS IN REGION")
    print("=" * 55)
    random.seed(42)
    points = [(random.randint(0, 99), random.randint(0, 99)) for _ in range(100)]

    full_region = Region(0, 0, 100, 100)
    q1          = Region(0,  0,  50, 50)
    q2          = Region(50, 0,  50, 50)
    q3          = Region(0,  50, 50, 50)
    q4          = Region(50, 50, 50, 50)

    print(f"  Points in full region (100x100) : {count_points_in_region(points, full_region)}")
    print(f"  Points in Q1 (0,0  → 50x50)    : {count_points_in_region(points, q1)}")
    print(f"  Points in Q2 (50,0 → 50x50)    : {count_points_in_region(points, q2)}")
    print(f"  Points in Q3 (0,50 → 50x50)    : {count_points_in_region(points, q3)}")
    print(f"  Points in Q4 (50,50→ 50x50)    : {count_points_in_region(points, q4)}")
    print(f"  Q1+Q2+Q3+Q4 total              : {sum(count_points_in_region(points, q) for q in [q1,q2,q3,q4])}")

    print()
    print("=" * 55)
    print("FIND DENSE REGIONS (threshold = 0.04)")
    print("=" * 55)

    clustered_points = (
        [(random.randint(0, 24), random.randint(0, 24)) for _ in range(70)] +
        [(random.randint(25, 99), random.randint(25, 99)) for _ in range(30)]
    )

    dense = find_dense_regions(
        clustered_points,
        x=0, y=0, width=100, height=100,
        min_size=10,
        density_threshold=0.04
    )

    print(f"  Dense regions found: {len(dense)}")
    for region, count, density in dense:
        print(f"    {region}  →  {count} points, density={density}")