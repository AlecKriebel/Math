"""Probe the phase-averaged positive-completion inequality for rank-two C."""

from itertools import combinations

import numpy as np


def partial_trace(c: np.ndarray, dims: tuple[int, ...], traced: tuple[int, ...]):
    n = len(dims)
    a = c.reshape(dims + dims)
    live = list(range(n))
    for site in sorted(traced, reverse=True):
        pos = live.index(site)
        a = np.trace(a, axis1=pos, axis2=pos + len(live))
        live.pop(pos)
    d = int(np.prod([dims[i] for i in live], dtype=int))
    return a.reshape(d, d)


def bil(c: np.ndarray, d: np.ndarray, dims=(3, 3, 3)):
    out = 0j
    for r in range(4):
        for s in combinations(range(3), r):
            cs = partial_trace(c, dims, s)
            ds = partial_trace(d, dims, s)
            out += (-0.5) ** r * np.vdot(cs, ds)
    return out


def q(c):
    return float(bil(c, c).real)


def scalar_s(c):
    return (2 * np.vdot(c, c).real - abs(np.trace(c)) ** 2) / 8


def main():
    rng = np.random.default_rng(84319)
    worst = (1e9, None)
    for _ in range(2000):
        x = rng.normal(size=(27, 4)) + 1j * rng.normal(size=(27, 4))
        uv, _ = np.linalg.qr(x)
        u, v = uv[:, :2], uv[:, 2:]
        ss = np.exp(rng.uniform(-2, 2, size=2))
        d = np.diag(ss)
        a = u @ d @ u.conj().T
        b = v @ d @ v.conj().T
        c = u @ d @ v.conj().T
        fa = q(a) - scalar_s(a)
        fb = q(b) - scalar_s(b)
        cross = bil(a, b).real - (
            2 * np.trace(a @ b).real - np.trace(a).real * np.trace(b).real
        ) / 8
        target = scalar_s(c) - (ss[0] - ss[1]) ** 2 / 8
        gap = target - cross - np.sqrt(max(0, fa * fb))
        # Desired completion implication would require gap <= 0.
        if -gap < worst[0]:
            worst = (-gap, (ss, fa, fb, cross, target, q(c)))
    print("minimum implication slack:", worst)


if __name__ == "__main__":
    main()
