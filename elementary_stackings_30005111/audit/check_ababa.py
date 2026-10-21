"""Exact finite certificate: the ababa walk has no permissible central-height order.

Five distinct real heights have exactly one of the 5! orders below. A necessary
condition for a stacking is that the height intervals of excursions to the
same leaf have pairwise disjoint interiors. Every rejected order records an
explicit pair violating that condition. No floating-point arithmetic is used.
"""
from itertools import combinations, permutations
import json
from pathlib import Path
EXCURSIONS = {'a': [(0, 1), (2, 3), (4, 0)], 'b': [(1, 2), (3, 4)]}

def rejection(order):
    heights = [0] * 5
    for height, visit in enumerate(order):
        heights[visit] = height
    for leaf, pairs in EXCURSIONS.items():
        for pair1, pair2 in combinations(pairs, 2):
            lo1, hi1 = sorted((heights[v] for v in pair1))
            lo2, hi2 = sorted((heights[v] for v in pair2))
            lo, hi = (max(lo1, lo2), min(hi1, hi2))
            if lo < hi:
                return {'central_visits_in_increasing_height': order, 'height_by_central_visit': heights, 'leaf': leaf, 'conflicting_excursion_endpoint_pairs': [pair1, pair2], 'overlap_open_interval': [lo, hi]}
    return None

def main():
    rejections, accepted = ([], [])
    for order in permutations(range(5)):
        certificate = rejection(order)
        (rejections if certificate else accepted).append(certificate or order)
    result = {'walk': ['O', 'A', 'O', 'B', 'O', 'A', 'O', 'B', 'O', 'A', 'O'], 'excursion_word': 'ababa', 'excursion_endpoint_pairs': EXCURSIONS, 'tested_order_count': len(rejections) + len(accepted), 'rejected_order_count': len(rejections), 'accepted_order_count': len(accepted), 'accepted_orders': accepted, 'rejections': rejections}
    if not result['tested_order_count'] == 120:
        raise AssertionError()
    if not result['rejected_order_count'] == 120:
        raise AssertionError()
    if not result['accepted_order_count'] == 0:
        raise AssertionError()
    output = Path(__file__).with_name('ababa_permutation_certificate.json')
    output.write_text(json.dumps(result, indent=2) + '\n')
    print('Tested 120 central-height orders; rejected 120; accepted 0.')
    print('Each rejected order has an explicit same-leaf open-interval overlap.')
    print(f'Certificate: {output.name}')
if __name__ == '__main__':
    main()
