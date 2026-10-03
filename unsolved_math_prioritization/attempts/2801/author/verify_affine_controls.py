#!/usr/bin/env python3
"""Exact finite controls for Ge 2609.27635v1, Example 3.5 and Lemma 3.2.

This is independent verification code, not a hyperbolic-manifold census or a
formal proof of the universal theorem. All arithmetic is rational (SymPy).
Run: python verify_affine_controls.py
"""
from itertools import combinations, product
import json
from sympy import Matrix, Rational

CHECKS = 0


def check(condition, message):
    global CHECKS
    CHECKS += 1
    if not condition:
        raise AssertionError(message)


def point(s):
    return tuple(map(int, s))


def affine_matrix(vertices):
    return Matrix([[1, *point(v)] for v in vertices])


def lower_cells(vertices, heights):
    cells = set()
    for subset in combinations(vertices, 4):
        matrix = affine_matrix(subset)
        if matrix.det() == 0:
            continue
        coefficients = matrix.inv() * Matrix([heights[v] for v in subset])
        gaps = {v: heights[v] - (affine_matrix([v]) * coefficients)[0]
                for v in vertices}
        if all(gap >= 0 for gap in gaps.values()):
            cells.add(tuple(sorted(v for v, gap in gaps.items() if gap == 0)))
    return cells


def face_triangles(tetrahedra, axis, value):
    return {tuple(sorted(v for v in tetra if point(v)[axis] == value))
            for tetra in tetrahedra
            if sum(point(v)[axis] == value for v in tetra) == 3}


def translated(triangles, axis):
    result = set()
    for tri in triangles:
        image = []
        for v in tri:
            p = list(point(v))
            check(p[axis] == 0, "Translation source must be low face")
            p[axis] = 1
            image.append(''.join(map(str, p)))
        result.add(tuple(sorted(image)))
    return result


cube = tuple(''.join(map(str, v)) for v in product(range(2), repeat=3))
heights = dict.fromkeys(cube, 0)
heights['110'] = heights['111'] = -1
prism_a = tuple(sorted(['000', '001', '010', '011', '110', '111']))
prism_b = tuple(sorted(['000', '001', '100', '101', '110', '111']))
first = lower_cells(cube, heights)
check(first == {prism_a, prism_b}, "First lift must give exactly two prisms")

ha = dict(zip(['000', '001', '010', '011', '110', '111'], [0, 0, 0, -1, 0, -2]))
hb = dict(zip(['000', '001', '100', '101', '110', '111'], [0, 0, 0, -1, 0, -2]))
ta, tb = lower_cells(prism_a, ha), lower_cells(prism_b, hb)
expected_a = {tuple(sorted(t)) for t in [
    ['000', '010', '110', '111'],
    ['000', '010', '011', '111'],
    ['000', '001', '011', '111']]}
expected_b = {tuple(sorted(t)) for t in [
    ['000', '100', '110', '111'],
    ['000', '100', '101', '111'],
    ['000', '001', '101', '111']]}
check(ta == expected_a, "Prism A lower tetrahedra")
check(tb == expected_b, "Prism B lower tetrahedra")
tetrahedra = ta | tb
volumes = [abs(affine_matrix(t).det()) / 6 for t in sorted(tetrahedra)]
check(all(v > 0 for v in volumes), "Every tetrahedron has positive Euclidean volume")
check(sum(volumes) == 1, "Total volume equals cube volume")
for axis in range(3):
    low = face_triangles(tetrahedra, axis, 0)
    high = face_triangles(tetrahedra, axis, 1)
    check(len(low) == len(high) == 2, "Each square boundary face has two triangles")
    check(translated(low, axis) == high, "Opposite boundary triangulations match")

rectangle = {'000', '001', '110', '111'}
common_a = {tuple(sorted(set(t) & rectangle)) for t in ta if len(set(t) & rectangle) == 3}
common_b = {tuple(sorted(set(t) & rectangle)) for t in tb if len(set(t) & rectangle) == 3}
check(common_a == common_b, "The two prism triangulations match internally")
check(all({'000', '111'} <= set(t) for t in common_a), "Shared rectangle diagonal")

# Stress eight parity choices for the three opposite-square pairings. Either
# parity is realized by a square affine symmetry; individual dihedral symmetries
# with the same parity yield the same single affine-dependency condition.
# These are algebraic controls only; the quotient need not be hyperbolic or a manifold.
face_dependencies = []
for axis in range(3):
    lows = [v for v in cube if point(v)[axis] == 0]
    highs = [v for v in cube if point(v)[axis] == 1]
    other = [i for i in range(3) if i != axis]
    def dependency(face):
        row = [0] * len(cube)
        for v in face:
            row[cube.index(v)] = (-1) ** sum(point(v)[i] for i in other)
        return Matrix([row])
    face_dependencies.append((dependency(lows), dependency(highs)))

dimensions = []
for parities in product([-1, 1], repeat=3):
    rows = [low - sign * high for (low, high), sign in zip(face_dependencies, parities)]
    B = Matrix.vstack(*rows)
    check(B * affine_matrix(cube) == Matrix.zeros(3, 4), "Affine classes lie in kernel")
    quotient_dimension = len(cube) - B.rank() - 4
    check(quotient_dimension >= Rational(6 - 4, 2), "Lemma 3.2 dimension bound")
    # At least one kernel vector must be non-affine and yield a strict subdivision.
    witness = next((h for h in B.nullspace()
                    if affine_matrix(cube).row_join(h).rank() > 4), None)
    check(witness is not None, "Nonzero compatible quotient height exists")
    cells = lower_cells(cube, dict(zip(cube, witness)))
    check(len(cells) > 1, "Non-affine height genuinely refines")
    # Exact matching of face-height classes was checked by B; applying the
    # restriction lemma then matches the whole geometric face subdivision.
    dimensions.append(quotient_dimension)

independent_foursets = sum(affine_matrix(s).det() != 0 for s in combinations(cube, 4))
check(len(tetrahedra) <= independent_foursets, "Finite termination capacity control")

result = {
    'status': 'PASS',
    'checks': CHECKS,
    'arithmetic': 'exact rational, SymPy',
    'scope': 'finite affine controls only; not a proof of the universal hyperbolic theorem',
    'example_source': 'Huabin Ge, arXiv:2609.27635v1, Example 3.5',
    'first_stage_prisms': [list(p) for p in sorted(first)],
    'final_tetrahedra': [list(t) for t in sorted(tetrahedra)],
    'tetrahedron_volumes': list(map(str, volumes)),
    'square_pairing_parity_cases': len(dimensions),
    'compatible_quotient_dimensions': list(map(int, dimensions)),
    'cube_independent_foursets': independent_foursets,
}
print(json.dumps(result, indent=2))
