"""Illustrations only: no validated-computation or theorem certificate claim."""
import math


def g(x):
    return (x + 1) * math.log1p(x) - x * math.log(x) if x else 0.0


def inverse_g(s):
    lo, hi = 0.0, 1.0
    while g(hi) < s:
        hi *= 2
    for _ in range(200):
        middle = (lo + hi) / 2
        if g(middle) < s:
            lo = middle
        else:
            hi = middle
    return (lo + hi) / 2


def depalma2019_vacuum_bound(tau, s):
    reference = g(tau / (1 - tau))
    return g(tau * inverse_g(s + reference) + tau) - reference


if __name__ == "__main__":
    for tau in (0.25, 0.5, 0.75):
        s = g(1)
        sharp = g(tau)
        exponential = math.log(tau * math.exp(s) + 1 - tau)
        improved = depalma2019_vacuum_bound(tau, s)
        print(f"tau={tau}: thermal={sharp:.15g}, qEPI={exponential:.15g}, "
              f"DePalma2019={improved:.15g}, gap={sharp - improved:.15g}")
