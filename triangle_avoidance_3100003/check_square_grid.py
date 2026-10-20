"""Exact integer checks of the dyadic lattice coloring; not a plane proof."""
from itertools import combinations

def color(x, y, n):
    v = (n & -n).bit_length() - 1
    k = v // 2
    q = 1 << k
    return ((x // q + y // q) if v % 2 == 0 else x // q) % 2

points = [(x, y) for x in range(-8, 9) for y in range(-8, 9)]
checks = {}
for (x,y), (u,v) in combinations(points, 2):
    n = (x-u)**2 + (y-v)**2
    assert color(x,y,n) != color(u,v,n), (x,y,u,v,n)
    checks[n] = checks.get(n, 0) + 1
print(f'PASS: {sum(checks.values())} pairs; {len(checks)} distinct squared distances; 289 points.')
