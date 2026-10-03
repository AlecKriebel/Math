"""Exact, finite diagnostics for PARTIAL.md; no asymptotic or novelty claim."""
from fractions import Fraction
from itertools import combinations
from pathlib import Path
import hashlib
import json
import random

checks = 0


def require(condition):
    global checks
    checks += 1
    assert condition


def squared_distance(p, q):
    return (p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2


def counts(points):
    assert len(set(points)) == len(points)
    return [len({squared_distance(p, q) for q in points if q != p})
            for p in points]


def deficits(points):
    return {len(points) - 1 - r for r in counts(points)}


def admissible(blocks):
    flat = [p for block in blocks for p in block]
    if len(set(flat)) != len(flat):
        return False
    for i, block in enumerate(blocks):
        outside = [p for j, other in enumerate(blocks) if j != i for p in other]
        for p in block:
            internal = {squared_distance(p, q) for q in block if p != q}
            external = [squared_distance(p, q) for q in outside]
            if len(set(external)) != len(external) or internal.intersection(external):
                return False
    return True


rng = random.Random(653)


def place(seeds):
    for _ in range(1000):
        blocks = []
        for seed in seeds:
            a, b = rng.randrange(-100000, 100001), rng.randrange(-100000, 100001)
            blocks.append([(x + a, y + b) for x, y in seed])
        if admissible(blocks):
            return blocks
    raise AssertionError("No admissible finite witness found within diagnostic limit")


def check_union(seeds):
    blocks = place(seeds)
    flat = [p for block in blocks for p in block]
    expected_counts = [len(flat) - len(seed) + r for seed in seeds for r in counts(seed)]
    require(counts(flat) == expected_counts)
    require(deficits(flat) == set().union(*(deficits(seed) for seed in seeds)))
    largest = max(map(len, seeds))
    require(len(deficits(flat)) <= max(1, largest - 1))
    return flat


def classical_bound(points):
    rs = counts(points)
    n = len(points)
    for a, b in combinations(rs, 2):
        require(n - 2 <= 2 * a * b)
    h = n - len(set(rs))
    require(n - 2 <= 2 * h * (h + 1))


seeds = [
    [(0, 0)],
    [(0, 0), (1, 0)],
    [(0, 0), (1, 0), (0, 1)],
    [(0, 0), (1, 0), (0, 1), (1, 1)],
    [(j, 0) for j in range(7)],
    [(i, j) for i in range(3) for j in range(2)],
    [(0, 0), (1, 0), (3, 2), (-2, 5)],
]
for _ in range(120):
    selected = [rng.choice(seeds) for _ in range(rng.randrange(2, 5))]
    classical_bound(check_union(selected))
for seed in seeds:
    repeated = check_union([seed] * 6)
    require(deficits(repeated) == deficits(seed))
    padded = check_union([seed] + [[(0, 0)]] * 9)
    require(deficits(padded) == deficits(seed) | {0})

# Hierarchical gluing: translate completed lower-level blocks without changing them.
lower = [check_union([seeds[2], seeds[3]]), check_union([seeds[4], seeds[0]])]
upper = check_union(lower)
require(deficits(upper) == set().union(*(deficits(seeds[j]) for j in [2, 3, 4, 0])))

# A nongeneric control must fail admissibility and the claimed generic identity.
square_blocks = [[(0, 0), (1, 0)], [(0, 1), (1, 1)]]
require(not admissible(square_blocks))
require(deficits(sum(square_blocks, [])) == {1})
require(set().union(*(deficits(b) for b in square_blocks)) == {0})

line_examples = 0
for size in range(2, 9):
    for subset in combinations(range(8), size):
        points = [(i, 0) for i in subset]
        require(len(set(counts(points))) <= (size + 1) // 2)
        classical_bound(points)
        line_examples += 1
for n in range(2, 65):
    points = [(i, 0) for i in range(n)]
    require(counts(points) == [max(i, n - 1 - i) for i in range(n)])
    require(len(set(counts(points))) == (n + 1) // 2)

# Exact rational parametrization of a positive-radius circle.
circle = [(Fraction(1 - t*t, 1 + t*t), Fraction(2*t, 1 + t*t))
          for t in range(-3, 4)]
require(all(x*x + y*y == 1 for x, y in circle))
circle_examples = 0
for size in range(2, 8):
    for subset in combinations(circle, size):
        require(len(set(counts(subset))) <= (size + 1) // 2)
        classical_bound(subset)
        circle_examples += 1

# Restricted supports with arbitrary off-support additions.
exception_examples = 0
for supported in [circle, [(i, 0) for i in range(7)]]:
    for t in range(5):
        for trial in range(12):
            extra = [(Fraction(31 + j), Fraction(13 + trial + j*j)) for j in range(t)]
            points = supported + extra
            n, m = len(points), len(supported)
            bound = min(n - 1, n + t - ((m - 1 + 1) // 2))
            require(len(set(counts(points))) <= bound)
            exception_examples += 1

# All nontrivial subsets of a small planar grid: no floating comparisons.
grid = [(i, j) for i in range(3) for j in range(3)]
grid_examples = 0
for size in range(2, 10):
    for points in combinations(grid, size):
        classical_bound(points)
        grid_examples += 1

root = Path(__file__).resolve().parent
result = {
    "all_passed": True,
    "assertions": checks,
    "generic_random_seed_tuples": 120,
    "repeated_and_padded_seed_types": len(seeds),
    "hierarchical_gluing_checked": True,
    "nongeneric_square_control_checked": True,
    "line_subsets_checked": line_examples,
    "arithmetic_progression_sizes": [2, 64],
    "rational_circle_subsets_checked": circle_examples,
    "support_with_exception_examples": exception_examples,
    "grid_subsets_checked": grid_examples,
    "arithmetic": "exact integers and fractions; squared distances preserve equality",
    "partial_sha256": hashlib.sha256((root / "PARTIAL.md").read_bytes()).hexdigest(),
    "scope": "Finite diagnostics only; the original asymptotic conjecture remains unresolved.",
}
(root / "check_results.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
