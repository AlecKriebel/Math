"""Exact sufficient certificates for prescribed deadlines; not game solving."""
from fractions import Fraction as F
from dataclasses import dataclass
import json


@dataclass(frozen=True)
class Kernel:
    # K(x,y)=coeff[x]*coeff[y]/denominator, centered support.
    coeff: tuple
    denominator: F

    def average_bound(self, q):
        c = self.coeff
        if q >= len(c):
            largest = sum(c)
        else:
            total = sum(c[:q])
            largest = total
            for i in range(q, len(c)):
                total += c[i] - c[i-q]
                largest = max(largest, total)
        return F(largest * largest, q*q) / self.denominator

    def smear(self, side, divisor):
        out = [0] * (len(self.coeff)+side-1)
        for i, v in enumerate(self.coeff):
            for j in range(side):
                out[i+j] += v
        return Kernel(tuple(out), self.denominator * divisor)


DELTA = Kernel((1,), F(1))


def geometry(r):
    assert r >= 1
    side = 3
    while side * 3 <= 2*r+1:
        side *= 3
    wait = r - (side-1)//2
    scales = []
    q = 3
    while q < side:
        scales.append(q)
        q *= 3
    return side, wait, scales


def concentration(kernels, q):
    return max(k.average_bound(q) for k in kernels)


def terminal_bound(kernels, horizon):
    side, wait, scales = geometry(horizon)
    return wait * concentration(kernels, side) + sum(
        (q * concentration(kernels, q) for q in scales), F(0))


def backward_step(kernels, gap):
    side, wait, scales = geometry(gap)
    average = terminal_bound(kernels, gap)
    divisor = side*side * (1-average-concentration(kernels, side))
    if divisor <= 0:
        return None, divisor
    return [DELTA]+[k.smear(side, divisor) for k in kernels], divisor


def certify(deadlines):
    assert deadlines and deadlines[0] >= 1
    assert all(a < b for a, b in zip(deadlines, deadlines[1:]))
    kernels = [DELTA]
    records = []
    for earlier, later in reversed(list(zip(deadlines, deadlines[1:]))):
        kernels, divisor = backward_step(kernels, later-earlier)
        records.append({"earlier": earlier, "later": later,
                        "divisor": str(divisor)})
        if kernels is None:
            return {"certified": False, "reason": "nonpositive divisor",
                    "steps": records}
    bound = terminal_bound(kernels, deadlines[0])
    return {"certified": bound < 1, "terminal_bound": str(bound),
            "steps": records}


if __name__ == '__main__':
    results = {"three_times": certify([13,17,21])}
    kernels = [DELTA]
    for depth in range(1, 150):
        kernels, divisor = backward_step(kernels, 1)
        if kernels is None:
            results["consecutive_gap_recursion_failure"] = {
                "smoothing_step": depth, "divisor_sign": "nonpositive",
                "meaning": "Failure of this sufficient certificate only"}
            break
    print(json.dumps(results, indent=2))
