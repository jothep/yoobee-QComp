import math
import matplotlib.pyplot as plt
from typing import Iterable

class CNum:
    def __init__(self, a: float, b: float):
        self.a, self.b = a, b

    def to_polar(self, deg: bool = False) -> tuple[float, float]:
        r  = math.hypot(self.a, self.b)
        th = math.atan2(self.b, self.a)
        return (r, math.degrees(th) if deg else th)

    @classmethod
    def from_polar(cls, r: float, theta: float, deg: bool = False) -> "CNum":
        if deg:
            theta = math.radians(theta)
        if r < 0:
            r, theta = -r, theta + math.pi
        return cls(r * math.cos(theta), r * math.sin(theta))

def plot_vectors(vectors: Iterable[CNum],
                 labels: list[str] | None = None,
                 title: str = "Complex vectors",
                 ax=None):

    xs = [z.a for z in vectors]
    ys = [z.b for z in vectors]

    n = len(xs)
    if labels is None:
        labels = [f"z{i+1}" for i in range(n)]
    else:
        labels = list(labels)[:n] + [f"z{i+1}" for i in range(len(labels), n)]

    max_r = max((math.hypot(x, y) for x, y in zip(xs, ys)), default=1.0)
    margin = 0.2 * max_r
    head_w = 0.04 * max_r
    head_l = 0.06 * max_r
    if max_r == 0:
        head_w = head_l = 0.1

    created_ax = False
    if ax is None:
        fig, ax = plt.subplots()
        created_ax = True

    for (x, y), lab in zip(zip(xs, ys), labels):
        ax.arrow(0, 0, x, y, head_width=head_w, head_length=head_l, length_includes_head=True)
        ax.text(x, y, f"  {lab}", ha="left", va="bottom")

    ax.axhline(0, linewidth=1)
    ax.axvline(0, linewidth=1)
    ax.set_aspect("equal", adjustable="box")
    ax.grid(True, linestyle="--", linewidth=0.5)
    ax.set_xlim(-max_r - margin, max_r + margin)
    ax.set_ylim(-max_r - margin, max_r + margin)
    ax.set_xlabel("Real")
    ax.set_ylabel("Imag")
    ax.set_title(title)

    if created_ax:
        plt.show()
    return ax

def draw_polar_guides(ax,
                      r: float,
                      theta: float,
                      show_circle: bool = True,
                      show_angle: bool = True,
                      arc_ratio: float = 0.35,
                      steps: int = 180):

    if r <= 0:
        return ax

    if show_circle:
        ts = [(2 * math.pi) * i / steps for i in range(steps + 1)]
        xs = [r * math.cos(t) for t in ts]
        ys = [r * math.sin(t) for t in ts]
        ax.plot(xs, ys, linestyle=":", linewidth=1)

    if show_angle and theta != 0:
        ts = [theta * i / steps for i in range(steps + 1)]  # 0 -> theta
        rr = arc_ratio * r
        xs = [rr * math.cos(t) for t in ts]
        ys = [rr * math.sin(t) for t in ts]
        ax.plot(xs, ys, linestyle="--", linewidth=1.2)

        mid = len(ts) // 2
        ax.text(xs[mid], ys[mid], f"θ ≈ {math.degrees(theta):.1f}°",
                ha="left", va="bottom")
    return ax

def main():

    z  = CNum(-2, 1)
    r, th = z.to_polar()             
    z2 = CNum.from_polar(r, th)      
    z3 = CNum.from_polar(2, 30, deg=True)

    fig, ax = plt.subplots(figsize=(6, 5))
    plot_vectors([z, z2, z3],
                 labels=["z = -2+1i", "z2 = from_polar(r,θ)", "z3 = (r=2, θ=30°)"],
                 title="Polar ↔ Cartesian",
                 ax=ax)

    draw_polar_guides(ax, r, th)          
    r3, th3 = z3.to_polar()
    draw_polar_guides(ax, r3, th3)        

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
