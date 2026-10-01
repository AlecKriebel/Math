"""Independent verification of already-claimed fixed-interior obstructions.

No search is performed on the author's five inconclusive models. The nine
claimed complete negative cases are rechecked with a different exact-cover
branch rule: choose a cell with the fewest currently available placements.
"""
from pathlib import Path
from collections import Counter
import json
import sys

root = Path(sys.argv[1])
P = [(x, y) for y, n in [(0, 4), (1, 4), (2, 6)] for x in range(n)]
maps = [lambda x, y: (x, y), lambda x, y: (2-y, x),
        lambda x, y: (5-x, 2-y), lambda x, y: (y, 5-x),
        lambda x, y: (5-x, y), lambda x, y: (2-y, 5-x),
        lambda x, y: (x, 2-y), lambda x, y: (y, x)]
shapes = [tuple(f(*z) for z in P) for f in maps]
counts = Counter()


def ck(b, name):
    assert b, name
    counts[name] += 1


W, H = 42, 133
board = (1 << (W*H))-1
all_placements = []
for shape in shapes:
    for a in range(W-max(x for x, y in shape)):
        for b in range(H-max(y for x, y in shape)):
            all_placements.append(sum(1 << (a+x+W*(b+y)) for x, y in shape))


def components(mask):
    cells = {(i % W, i // W) for i in range(W*H) if (mask >> i) & 1}
    sizes = []
    while cells:
        first = cells.pop()
        component = {first}
        front = {first}
        while front:
            adjacent = {(a+dx, b+dy) for a, b in front for dx, dy in
                        [(1, 0), (-1, 0), (0, 1), (0, -1)]}
            front = adjacent & cells
            component |= front
            cells -= front
        sizes.append(len(component))
    return sorted(sizes)


def exhausted_exact_cover(mask, placements):
    cover = {}
    for placement in placements:
        bits = placement
        while bits:
            bit = bits & -bits
            bits -= bit
            cover.setdefault(bit, []).append(placement)
    dead = set()
    nodes = 0

    def visit(remaining):
        nonlocal nodes
        if not remaining:
            return True
        if remaining in dead:
            return False
        nodes += 1
        options = None
        to_inspect = remaining
        while to_inspect:
            bit = to_inspect & -to_inspect
            to_inspect -= bit
            available = [p for p in cover.get(bit, []) if p & remaining == p]
            if not available:
                dead.add(remaining)
                return False
            if options is None or len(available) < len(options):
                options = available
                if len(options) == 1:
                    break
        for placement in options:
            if visit(remaining ^ placement):
                return True
        dead.add(remaining)
        return False

    return visit(mask), nodes


results = []
models = json.loads((root/'boundary_repair_receipt.json').read_text())['models']
for model in models:
    margin, phase = model['margin'], model['phase']
    fixed = 0
    blocked = 0
    for a in range(margin, W-5-margin):
        for b in range(margin, H-2-margin):
            if (a+4*b) % 14 != phase:
                continue
            placement = sum(1 << (a+x+W*(b+y)) for x, y in P)
            ck(blocked & placement == 0, 'prescribed_interior_tiles_disjoint')
            blocked |= placement
            fixed += 1
    holes = board ^ blocked
    sizes = components(holes)
    legal = [p for p in all_placements if p & blocked == 0]
    ck(fixed == model['fixed_tiles'] and holes.bit_count() == model['hole_cells'],
       'independent_prescribed_interior_reconstruction')
    ck(sizes == model['hole_component_sizes'], 'independent_repair_component_sizes')
    ck(len(legal) == model['legal_repair_placements'], 'independent_full_repair_placement_count')
    result = {'margin': margin, 'phase': phase}
    if any(size % 14 for size in sizes):
        ck(model['component_divisibility_obstruction'], 'component_obstruction_reconfirmed')
        result['verdict'] = 'component_area_obstruction'
    elif model['capped']:
        ck(not model['exhausted_for_this_fixed_interior'], 'inconclusive_models_kept_inconclusive')
        result['verdict'] = 'not_searched_by_reviewer_author_model_inconclusive'
    else:
        found, nodes = exhausted_exact_cover(holes, legal)
        ck(not found, 'independent_uncapped_MRV_exhaustion_no_repair')
        result.update(verdict='independent_exhaustive_no_repair', reviewer_MRV_nodes=nodes)
    results.append(result)

print(json.dumps({'status': 'PASS', 'exact_assertions': sum(counts.values()),
                  'families': dict(sorted(counts.items())), 'models': results,
                  'scope': 'The already-claimed 14 component obstructions and nine fixed-interior negative searches are independently verified. The other five models remain inconclusive and were not extended.'},
                 indent=2, sort_keys=True))
