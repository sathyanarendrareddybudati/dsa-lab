import math
import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection

def draw_sierpinski(ax, x, y, size, depth):

    if depth == 0:
        h = size * math.sqrt(3) / 2
        triangle = Polygon([[x, y], [x + size, y], [x + size / 2, y + h]], closed=True)
        ax.add_patch(triangle)
        return

    half = size / 2
    h = size * math.sqrt(3) / 2

    draw_sierpinski(ax, x, y, half, depth - 1)
    draw_sierpinski(ax, x + half, y, half, depth - 1)
    draw_sierpinski(ax, x + half / 2, y + h / 2, half, depth - 1)


def draw_tree(ax, x, y, length, angle, depth):

    if depth == 0:
        rad = math.radians(angle)
        ex = x + length * math.cos(rad)
        ey = y + length * math.sin(rad)
        ax.plot([x, ex], [y, ey], color="green", linewidth=1)
        return

    rad = math.radians(angle)
    ex = x + length * math.cos(rad)
    ey = y + length * math.sin(rad)

    lw = max(0.5, depth * 0.5)
    color = "brown" if depth > 2 else "green"
    ax.plot([x, ex], [y, ey], color=color, linewidth=lw)

    draw_tree(ax, ex, ey, length * 0.7, angle + 30, depth - 1)
    draw_tree(ax, ex, ey, length * 0.7, angle - 30, depth - 1)


def fractal_dimension(fractal_image, box_sizes):

    counts = []
    for box_size in box_sizes:
        count = 0
        rows, cols = fractal_image.shape
        for i in range(0, rows, box_size):
            for j in range(0, cols, box_size):
                box = fractal_image[i : i + box_size, j : j + box_size]
                if box.max() > 0:
                    count += 1
        counts.append(count)

    log_sizes = [math.log(1.0 / s) for s in box_sizes]
    log_counts = [math.log(c) for c in counts if c > 0]
    log_sizes = log_sizes[: len(log_counts)]

    n = len(log_sizes)
    sum_x = sum(log_sizes)
    sum_y = sum(log_counts)
    sum_xx = sum(x * x for x in log_sizes)
    sum_xy = sum(x * y for x, y in zip(log_sizes, log_counts))

    slope = (n * sum_xy - sum_x * sum_y) / (n * sum_xx - sum_x**2)
    return round(slope, 4)


def render_sierpinski_to_array(size_px=256, depth=4):
    fig, ax = plt.subplots(figsize=(4, 4))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect("equal")
    ax.axis("off")
    draw_sierpinski(ax, 0, 0, 1, depth)
    fig.canvas.draw()
    buf = np.frombuffer(fig.canvas.tostring_argb(), dtype=np.uint8)
    buf = buf.reshape(fig.canvas.get_width_height()[::-1] + (4,))
    plt.close(fig)
    gray = np.mean(buf[:, :, 1:], axis=2)
    binary = (gray < 128).astype(np.uint8)
    return binary


if __name__ == "__main__":

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    fig.suptitle("LAB 7 — Exercise 2: Fractal Drawing", fontsize=14)

    ax1 = axes[0]
    ax1.set_xlim(-0.1, 1.1)
    ax1.set_ylim(-0.1, 1.0)
    ax1.set_aspect("equal")
    ax1.set_title("Sierpinski Triangle (depth=5)")
    ax1.axis("off")
    ax1.set_facecolor("white")

    draw_sierpinski(ax1, 0, 0, 1, depth=5)

    depth = 5
    num_triangles = 3**depth
    print(f"Sierpinski depth {depth} → {num_triangles} small triangles drawn")

    ax2 = axes[1]
    ax2.set_xlim(-150, 150)
    ax2.set_ylim(-10, 250)
    ax2.set_aspect("equal")
    ax2.set_title("Fractal Tree (depth=7)")
    ax2.axis("off")
    ax2.set_facecolor("white")

    draw_tree(ax2, x=0, y=0, length=80, angle=90, depth=7)

    ax3 = axes[2]
    ax3.set_title("Fractal Dimension (Box Counting)")
    ax3.set_xlabel("log(1/box_size)")
    ax3.set_ylabel("log(count)")
    ax3.set_facecolor("white")

    binary = render_sierpinski_to_array(depth=4)

    box_sizes = [2, 4, 8, 16, 32, 64]
    counts = []
    for box_size in box_sizes:
        count = 0
        rows, cols = binary.shape
        for i in range(0, rows, box_size):
            for j in range(0, cols, box_size):
                box = binary[i : i + box_size, j : j + box_size]
                if box.max() > 0:
                    count += 1
        counts.append(count)

    log_sizes = [math.log(1.0 / s) for s in box_sizes]
    log_counts = [math.log(c + 1) for c in counts]

    ax3.plot(log_sizes, log_counts, "bo-", markersize=6, label="Box counts")

    dim = fractal_dimension(binary, box_sizes)
    ax3.set_title(f"Fractal Dimension ≈ {dim}\n(Sierpinski ≈ 1.585 theoretical)")
    ax3.legend()
    ax3.grid(True, alpha=0.3)

    print(f"Estimated fractal dimension: {dim}")
    print(f"Theoretical Sierpinski dimension: ~1.585")
    print()
    print("Complexity answers:")
    print(f"  Sierpinski depth 5 → 3^5 = {3**5} triangles")
    print(f"  Fractal dimension of straight line  = 1.0")
    print(f"  Fractal dimension of filled square  = 2.0")

    plt.tight_layout()
    plt.savefig(
        "exercise2_fractals.png", dpi=120, bbox_inches="tight"
    )
    plt.close()
    print("\nPlot saved to exercise2_fractals.png")
