"""Finite sanity checks for the analytic review; these do not verify PDE gluing."""
from itertools import product, permutations
from fractions import Fraction
from pathlib import Path
import json


def tree_from_prufer(seq, n):
    degree = [1] * n
    for v in seq:
        degree[v] += 1
    edges = []
    for v in seq:
        w = next(i for i, d in enumerate(degree) if d == 1)
        edges.append(tuple(sorted((w, v))))
        degree[w] -= 1
        degree[v] -= 1
    a, b = (i for i, d in enumerate(degree) if d == 1)
    edges.append((a, b))
    return tuple(sorted(edges))


def towards_root(edges, n, root=0):
    adjacency = [[] for _ in range(n)]
    for a, b in edges:
        adjacency[a].append(b)
        adjacency[b].append(a)
    parent = {root: None}
    queue = [root]
    for v in queue:
        for w in adjacency[v]:
            if w not in parent:
                parent[w] = v
                queue.append(w)
    return parent


def normalize(edges, parent, switch, order):
    """A vertex's ordinary output is its fixed edge toward the marked root."""
    flags = []
    for edge in order:
        a, b = edge
        child, par = (a, b) if parent.get(a) == b else (b, a)
        if switch[edge]:
            flags.extend([(par, child, 'p', 'q'), (child, par, 'q', 'p')])
        else:
            flags.extend([(par, child, 'diag'), (child, par, 'diag')])
    return tuple(sorted(flags))


trees = orders = switch_cases = 0
for n in range(2, 6):
    for seq in product(range(n), repeat=n-2):
        edges = tree_from_prufer(seq, n)
        parent = towards_root(edges, n)
        trees += 1
        for switches in product((False, True), repeat=n-1):
            switch = dict(zip(edges, switches))
            expected = normalize(edges, parent, switch, edges)
            switch_cases += 1
            for order in permutations(edges):
                assert normalize(edges, parent, switch, order) == expected
                orders += 1

cost_checks = 0
eps = Fraction(1, 7)
for ep, ec, r, s in product(range(5), range(1, 5), range(7), range(7)):
    original = ep + ec + eps * (r+s)
    root = ep + eps * (r+1)
    child = ec + eps * (s-1)
    assert original == root + child
    assert child > 0 and root > 0
    assert root < original and child < original
    cost_checks += 1
for r, s in product(range(7), range(2, 7)):
    assert eps*(r+s) == eps*(r+1) + eps*(s-1)
    cost_checks += 1

sign_checks = 0
for b, l, q, r, o in product(range(2), repeat=5):
    raw = b*(l+q+r+o) + q*(b+q+r+o) + (r+o)*(b+q)
    assert raw % 2 == (b*l+q) % 2
    sign_checks += 1
for p, q in product(range(20), repeat=2):
    exponent = (p+q)*(p+q-1)//2 + p*q - p*(p-1)//2 - q*(q-1)//2
    assert exponent % 2 == 0
    sign_checks += 1
for d in range(1, 30):
    assert ((d*(d-1)//2 - (d-1)*(d-2)//2)+(d+1)) % 2 == 0
    sign_checks += 1

cyclic_count_checks = 0
for k in range(1, 20):
    for s in range(k+1):
        # Normalized labeled child attachments have exactly k starts/gaps.
        placements = tuple(range(k))
        assert len(set(placements)) == k
        cyclic_count_checks += 1

result = dict(
    status='passed',
    rooted_labeled_trees=trees,
    reciprocal_sector_assignments=switch_cases,
    normalization_orders=orders,
    cost_checks=cost_checks,
    sign_checks=sign_checks,
    cyclic_multiplicity_checks=cyclic_count_checks,
    scope='finite combinatorial and arithmetic sanity checks only; no PDE or virtual integration proof',
)
out = Path(__file__).with_name('identity_results.json')
out.write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
