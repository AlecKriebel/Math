"""Exact integer audit; standard library only; no source-file imports."""
import hashlib
import itertools
import json
from pathlib import Path
OUT = Path(__file__).resolve().parent
W = 'ababa'
N = len(W)

def ranks(order):
    return {v: rank for rank, v in enumerate(order)}

def overlaps(h, i, j):
    lo_i, hi_i = sorted((h[i], h[(i + 1) % N]))
    lo_j, hi_j = sorted((h[j], h[(j + 1) % N]))
    return max(lo_i, lo_j) < min(hi_i, hi_j)
pairs = [(i, j) for i in range(N) for j in range(i + 1, N) if W[i] == W[j]]
rows = []
full_orders_checked = 0
full_orders_accepted = 0
for central_order in itertools.permutations(range(N)):
    h = ranks(central_order)
    violations = [[i, j] for i, j in pairs if overlaps(h, i, j)]
    leaf_orders_accepted = 0
    for a_order in itertools.permutations([0, 2, 4]):
        for b_order in itertools.permutations([1, 3]):
            full_orders_checked += 1
            leaf = dict(ranks(a_order), **{})
            leaf.update(ranks(b_order))
            no_inversion = True
            for label in 'ab':
                strands = [(h[c], leaf[i]) for i in range(N) if W[i] == label for c in (i, (i + 1) % N)]
                for (x1, y1), (x2, y2) in itertools.combinations(strands, 2):
                    if (x1 - x2) * (y1 - y2) < 0:
                        no_inversion = False
            leaf_orders_accepted += int(no_inversion)
            full_orders_accepted += int(no_inversion)
    if not bool(leaf_orders_accepted) == (not violations):
        raise AssertionError()
    rows.append({'central_order_low_to_high': central_order, 'overlapping_same_leaf_excursion_pairs': violations, 'accepted_leaf_orders': leaf_orders_accepted})
directed = tuple(((label, direction) for label in W for direction in (1, -1)))
variants = []
for inverse in (False, True):
    word = tuple(((label, -direction) for label, direction in reversed(directed))) if inverse else directed
    for shift in range(len(word)):
        rotated = word[shift:] + word[:shift]
        proper_periods = [p for p in range(1, len(word)) if len(word) % p == 0 and rotated == rotated[:p] * (len(word) // p)]
        if not not proper_periods:
            raise AssertionError()
        variants.append({'inverse': inverse, 'cyclic_shift': shift, 'proper_periods': proper_periods})
if not len(rows) == 120:
    raise AssertionError()
if not full_orders_checked == 1440:
    raise AssertionError()
if not full_orders_accepted == 0:
    raise AssertionError()
if not all((row['overlapping_same_leaf_excursion_pairs'] for row in rows)):
    raise AssertionError()
report = {'word': W, 'directed_edge_length': len(directed), 'central_orders_checked': len(rows), 'accepted_central_orders': 0, 'complete_vertex_orders_checked': full_orders_checked, 'accepted_complete_vertex_orders': full_orders_accepted, 'rotation_and_inverse_variants_checked': len(variants), 'nonpower_checks': variants, 'all_central_order_results': rows}
report_path = OUT / 'verification_receipt.json'
report_path.write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps({k: v for k, v in report.items() if k not in ('nonpower_checks', 'all_central_order_results')}, indent=2))
print('receipt_sha256', hashlib.sha256(report_path.read_bytes()).hexdigest())
print('script_sha256', hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
