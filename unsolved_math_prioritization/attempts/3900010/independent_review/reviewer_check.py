"""Independent exact reconstruction for the scoped 3900010 partials.

No author module is imported. A six-entry row-vector DFS replaces the author's
single-integer BFS. The low-pivot elimination differs from the author's rank
algorithm. Author certificates are input data, not accepted conclusions.
Run: python reviewer_check.py /path/to/author/attempt
"""
from pathlib import Path
from collections import Counter
from itertools import product
import hashlib
import json
import sys
import sympy as S

root = Path(sys.argv[1])
checks = Counter()


def verify(condition, label):
    assert condition, label
    checks[label] += 1


cells = tuple((x, y) for y, width in [(0, 4), (1, 4), (2, 6)] for x in range(width))
# Explicit eight geometric maps, in the certificate's documented indexing.
transforms = [lambda x, y: (x, y), lambda x, y: (2-y, x),
              lambda x, y: (5-x, 2-y), lambda x, y: (y, 5-x),
              lambda x, y: (5-x, y), lambda x, y: (2-y, 5-x),
              lambda x, y: (x, 2-y), lambda x, y: (y, x)]
shapes = [tuple(sorted(f(x, y) for x, y in cells)) for f in transforms]
verify(len(set(shapes)) == 8, 'eight_distinct_orientations')
verify(set(cells) == {tuple(z) for z in json.loads((root/'tile.json').read_text())['unit_cells']},
       'independent_source_shape_matches_model')

# Positive coordinate witness, checked as ordinary integer occupancy counts.
witness = json.loads((root/'known_even_witness.json').read_text())
W, H = witness['width'], witness['height']
occupancy = [[0]*W for _ in range(H)]
for tile in witness['tiles']:
    for a, b in shapes[tile['orientation']]:
        x, y = a+tile['x'], b+tile['y']
        verify(0 <= x < W and 0 <= y < H, 'even_witness_cell_bounds')
        occupancy[y][x] += 1
for row in occupancy:
    for count in row:
        verify(count == 1, 'even_witness_exact_single_coverage')
verify((W, H, len(witness['tiles'])) == (84, 66, 396), 'credited_even_dimensions_count')

# Independent exact polynomial ideal calculation over Q. This is a check on
# the written reflection argument, not a numerical search for common roots.
x, y = S.symbols('x y')
polynomials = [sum(x**a*y**b for a, b in shape) for shape in shapes]
G = S.groebner(polynomials, x, y, domain=S.QQ)
expected = [sum(x**i for i in range(6)), (x+1)*(y+1), sum(y**i for i in range(6))]
verify([p.as_expr() for p in G.polys] == [S.expand(p) for p in expected],
       'independent_groebner_basis_exactly_character_locus')
for shape in shapes:
    verify(sorted([abs(sum((-1)**a for a, b in shape)),
                   abs(sum((-1)**b for a, b in shape))]) == [0, 6],
           'orientation_stripe_sums')
for width, height in product(range(1, 151), repeat=2):
    passed = all((width % 2 == 0 or height % order == 0) and
                 (height % 2 == 0 or width % order == 0) for order in [2, 3, 6])
    formula = (width % 2 == height % 2 == 0) or (width % 2 and height % 6 == 0) or (
        height % 2 and width % 6 == 0)
    verify(passed == bool(formula), 'rectangle_character_conditions')
    if width*height % 14 == 0 and width*height//14 % 2 and passed:
        even = width if width % 2 == 0 else height
        verify(even % 12 == 6 and width*height//14 % 6 == 3, 'odd_area_restrictions')


def row_shapes(width):
    """Every contained bottom-anchored translation, then indexed by its cells."""
    covering = [[] for _ in range(width)]
    for shape in shapes:
        for shift in range(width-max(a for a, b in shape)):
            rows = [0]*6
            for a, b in shape:
                rows[b] |= 1 << (a+shift)
            rows = tuple(rows)
            for column in range(width):
                if rows[0] & (1 << column):
                    covering[column].append(rows)
    return covering


def close_rows(width):
    choices = row_shapes(width)
    full = (1 << width)-1
    empty = (0,)*6
    initial = (empty, 0)
    visited = {initial}
    stack = [initial]
    transitions = 0
    returns = [0, 0]
    while stack:
        rows, parity = stack.pop()
        # Use a direct column scan rather than the author's low-bit selection.
        first = next(c for c in range(width) if not rows[0] & (1 << c))
        for addition in choices[first]:
            if any(a & b for a, b in zip(rows, addition)):
                continue
            combined = tuple(a | b for a, b in zip(rows, addition))
            removed = 0
            while removed < 6 and combined[removed] == full:
                removed += 1
            following = combined[removed:] + (0,)*removed
            verify(sum(r.bit_count() for r in following) ==
                   sum(r.bit_count() for r in rows)+14-width*removed,
                   'independent_frontier_area_identity')
            transitions += 1
            new_parity = 1-parity
            if following == empty:
                returns[new_parity] += 1
            state = following, new_parity
            if state not in visited:
                visited.add(state)
                stack.append(state)
    # Same mathematical encoding permits exact set-hash comparison despite
    # different data structures, transition code, and DFS discovery order.
    encoded = sorted((sum(row << (j*width) for j, row in enumerate(rows)), parity)
                     for rows, parity in visited)
    digest = hashlib.sha256(''.join(f'{mask},{parity};' for mask, parity in encoded).encode()).hexdigest()
    return {'width': width, 'states': len(visited), 'edges': transitions,
            'return_edges_even_odd': returns, 'state_sha256': digest}


author_graphs = json.loads((root/'turn_3_checks.json').read_text())['complete_fixed_width_certificates']
independent_graphs = []
for width in range(1, 31):
    actual = close_rows(width)
    wanted = author_graphs[width-1]
    verify(all(actual[key] == wanted[key] for key in actual), 'full_frontier_state_set_and_counts_match')
    verify(actual['return_edges_even_odd'] == [0, 0], 'all_height_no_return_at_this_width')
    independent_graphs.append(actual)
verify(sum(r['states'] for r in independent_graphs) == 463612, 'total_exhaustive_states')

# Periodic construction is independently reconstructed from the residue rule.
verify(sorted((a+4*b) % 14 for a, b in cells) == list(range(14)), 'complete_lattice_residue_system')
torus_checks = []
for width, height in [(14, 7), (42, 7), (14, 21), (42, 21)]:
    mult = Counter()
    seam = 0
    count = 0
    for b in range(height):
        for a in range(width):
            if (a+4*b) % 14:
                continue
            points = [(a+u, b+v) for u, v in cells]
            seam += any(u >= width or v >= height for u, v in points)
            reduced = {(u % width, v % height) for u, v in points}
            verify(len(reduced) == 14, 'individual_torus_tile_injectivity')
            mult.update(reduced)
            count += 1
    verify(len(mult) == width*height and set(mult.values()) == {1}, 'torus_exact_partition')
    verify(count % 2 == 1 and seam > 0, 'odd_torus_with_actual_seam_wrap')
    torus_checks.append({'width': width, 'height': height, 'tiles': count, 'wrapped_tiles': seam})

# Binary overlap witness: use a cell multiplicity table and a separate
# low-pivot rank elimination, including the final count coordinate.
binary = json.loads((root/'parity_42x31.json').read_text())
width, height = binary['width'], binary['height']
area = width*height
mult = Counter()
distinct = set()
for placement in binary['selected_placements']:
    key = placement['orientation'], placement['x'], placement['y']
    verify(key not in distinct, 'binary_selected_placements_distinct')
    distinct.add(key)
    for a, b in shapes[key[0]]:
        u, v = a+key[1], b+key[2]
        verify(0 <= u < width and 0 <= v < height, 'binary_placement_contained')
        mult[u, v] += 1
verify(len(distinct) == 403 and len(mult) == area and all(n % 2 for n in mult.values()),
       'explicit_binary_target_and_odd_count')
verify({str(k): v for k, v in sorted(Counter(mult.values()).items())} == binary['coverage_histogram'],
       'independent_overlap_histogram')
verify(max(mult.values()) == 19 and len(distinct) != area//14, 'binary_witness_is_not_exact_cover')
low_basis = {}
placements = 0
for shape in shapes:
    for a in range(width-max(u for u, v in shape)):
        for b in range(height-max(v for u, v in shape)):
            column = (1 << area) | sum(1 << (a+u+width*(b+v)) for u, v in shape)
            placements += 1
            while column:
                pivot = (column & -column).bit_length()-1
                if pivot not in low_basis:
                    low_basis[pivot] = column
                    break
                column ^= low_basis[pivot]
verify(placements == 8452 and len(low_basis) == 1293, 'independent_low_pivot_rank')
target = (1 << (area+1))-1
while target:
    pivot = (target & -target).bit_length()-1
    verify(pivot in low_basis, 'binary_target_in_low_pivot_span')
    target ^= low_basis[pivot]

print(json.dumps({'status': 'PASS', 'exact_assertions': sum(checks.values()),
                  'families': dict(sorted(checks.items())),
                  'independent_full_graphs': independent_graphs,
                  'torus_checks': torus_checks,
                  'binary_rank': len(low_basis),
                  'scope': 'Independent exact source-cell, even-witness, polynomial, full width-1-to-30 frontier closure, torus, and binary-overlap controls. No positive odd rectangle or global obstruction is inferred.'},
                 indent=2, sort_keys=True))
