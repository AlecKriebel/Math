"""Independent exact check of the author's bounded direct-product search.

Uses only (order, number of classes, number of linear characters) as a
necessary prefilter. Every surviving cross-radical comparison uses the full
integer-valued degree multiplicity function. Does not import author code.
"""
from pathlib import Path
from collections import defaultdict
from itertools import combinations_with_replacement
import hashlib
import json
import datetime

HERE = Path(__file__).resolve().parent
INPUT = HERE.parent / "artifacts" / "library_scan.ndjson"
BOUND = 10**12
rows = [json.loads(line) for line in INPUT.read_text().splitlines()]
groups = {((1, 1),): ("explicit identity group", 1, True, ((1, 1),))}
for name, order, degrees, radical_order in rows:
    degrees = tuple(sorted(tuple(pair) for pair in degrees))
    assert all(isinstance(d, int) and isinstance(m, int) and d > 0 and m > 0
               for d, m in degrees)
    assert len({d for d, m in degrees}) == len(degrees)
    assert sum(d*d*m for d, m in degrees) == order
    assert radical_order >= 1 and order % radical_order == 0
    is_radical_free = radical_order == 1
    if degrees in groups:
        assert groups[degrees][1:3] == (order, is_radical_free)
    else:
        groups[degrees] = (name, order, is_radical_free, degrees)

all_groups = list(groups.values())
radical_free = [g for g in all_groups if g[2]]

def invariant(a, b):
    return (a[1] * b[1],
            sum(m for _, m in a[3]) * sum(m for _, m in b[3]),
            dict(a[3]).get(1, 0) * dict(b[3]).get(1, 0))

def exact(a, b):
    result = {}
    for da, ma in a[3]:
        for db, mb in b[3]:
            d = da * db
            result[d] = result.get(d, 0) + ma * mb
    return tuple(sorted(result.items()))

targets = defaultdict(list)
rf_pairs = 0
for a, b in combinations_with_replacement(radical_free, 2):
    if a[1] * b[1] <= BOUND:
        targets[invariant(a, b)].append((a, b))
        rf_pairs += 1

nonrf_pairs = prefilter_survivors = exact_comparisons = 0
collisions = []
for a, b in combinations_with_replacement(all_groups, 2):
    if (a[2] and b[2]) or a[1] * b[1] > BOUND:
        continue
    nonrf_pairs += 1
    candidates = targets.get(invariant(a, b), ())
    if not candidates:
        continue
    prefilter_survivors += 1
    observed = exact(a, b)
    for c, d in candidates:
        exact_comparisons += 1
        if observed == exact(c, d):
            collisions.append({"nonradical_free": [a[0], b[0]],
                               "radical_free": [c[0], d[0]]})

report = {
    "utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "input_sha256": hashlib.sha256(INPUT.read_bytes()).hexdigest(),
    "input_rows": len(rows),
    "distinct_degree_multisets": len(all_groups),
    "radical_free_degree_multisets": len(radical_free),
    "product_order_bound": BOUND,
    "radical_free_pairs": rf_pairs,
    "nonradical_free_pairs": nonrf_pairs,
    "prefilter": ["order", "class count", "linear character count"],
    "nonradical_free_prefilter_survivors": prefilter_survivors,
    "full_exact_comparisons": exact_comparisons,
    "collisions": collisions,
    "scope": "Independent exact recheck on the supplied CTblLib rows and two-factor products only; no classification of finite groups."
}
(HERE / "independent_product_results.json").write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps(report, indent=2))
