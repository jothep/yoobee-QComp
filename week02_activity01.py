import math
import matplotlib.pyplot as plt
from typing import Iterable

class CNum:
    def __init__(self, a: float, b: float):
        self.a = a
        self.b = b

    def _cAdd(self, o):
        return CNum(self.a + o.a, self.b + o.b)
    
    def _cSub(self, o):
        return CNum(self.a - o.a, self.b - o.b)
    
    def _cMul(self, o):
        return CNum(self.a*o.a - self.b*o.b, self.a*o.b + self.b*o.a)
    
    def _cDiv(self, o):
        # （a+bi）/(c+di) = [(ac+bd) + (bc-ad)i] / (c^2 + d^2)
        denom = o.a*o.a + o.b*o.b
        if denom == 0:
            raise ComplexDivisionByZero("complex division by 0")
        real = (self.a*o.a + self.b*o.b) / denom
        imag = (self.b*o.a - self.a*o.b) / denom
        return CNum(real, imag)    
class ComplexDivisionByZero(ArithmeticError): pass

def plot_vectors(vectors: Iterable["CNum"],
                 labels: list[str] | None = None,
                 title: str = "Complex vectors", ax=None):
    xs = []
    ys = []
    for z in vectors:
        xs.append(z.a)
        ys.append(z.b)

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
        ax.arrow(0, 0, x, y,
                 head_width=head_w, head_length=head_l,
                 length_includes_head=True)
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

def maintask():
    c1 = CNum(1, -2)
    c2 = CNum(2, -1)

    sum = c1._cAdd(c2)
    dif = c1._cSub(c2)
    pro = c1._cMul(c2)
    quo = c1._cDiv(c2)

    plot_vectors(
    [c1, c2, sum, dif, pro, quo],
    labels=["c1", "c2", "c1 + c2", "c1 - c2", "c1 * c2", "c1 / c2"],
    title="Originals and Results")

if __name__ == "__main__":
    maintask()