import random
import math
def midpoint_displacement(x1, y1, x2, y2, roughness, depth):
    if depth == 0:
        return []
    mid_x = (x1 + x2) / 2
    mid_y = (y1 + y2) / 2
    offset = roughness * random.uniform(-1, 1)
    mid_y += offset
    points = [(mid_x, mid_y)]
    left_points = midpoint_displacement(x1, y1, mid_x, mid_y, roughness * 0.5, depth - 1)
    right_points = midpoint_displacement(mid_x, mid_y, x2, y2, roughness * 0.5, depth - 1)
    return left_points + points + right_points
def generate_terrain(width, height, roughness, depth):
    grid = [[0.0 for _ in range(width)] for _ in range(height)]
    grid[0][0] = 0
    grid[0][width - 1] = 0
    grid[height - 1][0] = 0
    grid[height - 1][width - 1] = 0
    def diamond_square(x1, y1, x2, y2, rough, d):
        if d == 0:
            return
        mid_x = (x1 + x2) // 2
        mid_y = (y1 + y2) // 2
        center_val = (grid[y1][x1] + grid[y1][x2] + grid[y2][x1] + grid[y2][x2]) / 4
        center_val += rough * random.uniform(-1, 1)
        grid[mid_y][mid_x] = center_val
        def avg(*vals):
            return sum(vals) / len(vals)
        grid[y1][mid_x] = avg(grid[y1][x1], grid[y1][x2], center_val) + rough * random.uniform(-1, 1)
        grid[y2][mid_x] = avg(grid[y2][x1], grid[y2][x2], center_val) + rough * random.uniform(-1, 1)
        grid[mid_y][x1] = avg(grid[y1][x1], grid[y2][x1], center_val) + rough * random.uniform(-1, 1)
        grid[mid_y][x2] = avg(grid[y1][x2], grid[y2][x2], center_val) + rough * random.uniform(-1, 1)
        next_rough = rough * 0.5
        diamond_square(x1, y1, mid_x, mid_y, next_rough, d - 1)
        diamond_square(mid_x, y1, x2, mid_y, next_rough, d - 1)
        diamond_square(x1, mid_y, mid_x, y2, next_rough, d - 1)
        diamond_square(mid_x, mid_y, x2, y2, next_rough, d - 1)
    diamond_square(0, 0, width - 1, height - 1, roughness, depth)
    return grid
def detect_artifacts(terrain_grid, threshold):
    suspicious = []
    rows = len(terrain_grid)
    cols = len(terrain_grid[0])
    for r in range(rows):
        for c in range(cols):
            current = terrain_grid[r][c]
            neighbors = []
            if r > 0:
                neighbors.append(terrain_grid[r - 1][c])
            if r < rows - 1:
                neighbors.append(terrain_grid[r + 1][c])
            if c > 0:
                neighbors.append(terrain_grid[r][c - 1])
            if c < cols - 1:
                neighbors.append(terrain_grid[r][c + 1])
            for n in neighbors:
                if abs(current - n) > threshold:
                    suspicious.append((r, c))
                    break  
    return suspicious
if __name__ == "__main__":
    print("testing midpoint displacement...")
    pts = midpoint_displacement(0, 0, 100, 0, 20, 4)
    print(f"  got {len(pts)} midpoints back")
    print("\ngenerating terrain (17x17)...")
    terrain = generate_terrain(17, 17, 1.0, 4)
    print(f"  grid size: {len(terrain)} x {len(terrain[0])}")
    print(f"  sample values: {[round(terrain[i][i], 2) for i in range(5)]}")
    print("\ndetecting artifacts with threshold=1.5...")
    artifacts = detect_artifacts(terrain, 1.5)
    print(f"  found {len(artifacts)} suspicious cells")
    if artifacts:
        print(f"  first few: {artifacts[:5]}")
