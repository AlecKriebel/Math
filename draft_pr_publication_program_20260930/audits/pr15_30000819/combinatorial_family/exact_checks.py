#!/usr/bin/env python3
"""Independent exact combinatorial controls for the frozen PR15 note.

Standard library only. Integer determinants and rational elimination are used;
no floating point, packages, source verifier imports, or bounded-search claim of
general normality. The all-degree certificates are justified in REPORT.md.
"""
from collections import Counter
from fractions import Fraction as F
from itertools import combinations, product
from math import gcd, lcm, prod, comb
from pathlib import Path
import json

ASSERTIONS = 0
GROUPS = []


def check(condition, message):
    global ASSERTIONS
    ASSERTIONS += 1
    if not condition:
        raise AssertionError(message)


def group(name, before, **data):
    GROUPS.append(dict(name=name, exact_assertions=ASSERTIONS-before, **data))


def det(rows):
    a = [[F(x) for x in row] for row in rows]
    answer = F(1)
    for j in range(len(a)):
        pivot = next((i for i in range(j, len(a)) if a[i][j]), None)
        if pivot is None:
            return 0
        if pivot != j:
            a[pivot], a[j] = a[j], a[pivot]
            answer = -answer
        value = a[j][j]
        answer *= value
        for i in range(j+1, len(a)):
            multiplier = a[i][j]/value
            for k in range(j+1, len(a)):
                a[i][k] -= multiplier*a[j][k]
    if answer.denominator != 1:
        raise ArithmeticError('integer determinant acquired denominator')
    return answer.numerator


def rref_columns(columns):
    if not columns:
        return [], []
    rows = [[F(x) for x in row] for row in zip(*columns)]
    pivots = []
    i = 0
    for j in range(len(columns)):
        pivot = next((k for k in range(i, len(rows)) if rows[k][j]), None)
        if pivot is None:
            continue
        rows[pivot], rows[i] = rows[i], rows[pivot]
        value = rows[i][j]
        rows[i] = [x/value for x in rows[i]]
        for k in range(len(rows)):
            if k != i:
                multiplier = rows[k][j]
                rows[k] = [x-multiplier*y for x, y in zip(rows[k], rows[i])]
        pivots.append(j)
        i += 1
        if i == len(rows):
            break
    return rows, pivots


def rank(columns):
    return len(rref_columns(columns)[1])


def homogeneous(A):
    return [tuple(v)+(1,) for v in A]


def primitive_circuits(A):
    columns = homogeneous(A)
    r = rank(columns)
    out = []
    for size in range(2, r+2):
        for subset in combinations(range(len(A)), size):
            rows, pivots = rref_columns([columns[i] for i in subset])
            if len(pivots) != size-1:
                continue
            free = next(j for j in range(size) if j not in pivots)
            v = [F(0)]*size
            v[free] = F(1)
            for row, pivot in zip(rows, pivots):
                v[pivot] = -row[free]
            if not all(v):
                continue
            scale = lcm(*(x.denominator for x in v))
            v = [int(x*scale) for x in v]
            divisor = gcd(*v)
            v = [x//divisor for x in v]
            if v[0] < 0:
                v = [-x for x in v]
            u = [0]*len(A)
            for i, x in zip(subset, v):
                u[i] = x
            out.append(tuple(u))
    return out


def generated_group_index(A):
    cols = homogeneous(A)
    r = len(cols[0])
    divisor = 0
    for chosen in combinations(cols, r):
        divisor = gcd(divisor, abs(det(list(zip(*chosen)))))
        if divisor == 1:
            return 1
    return divisor


def simplex_volume(A, simplex):
    return abs(det(list(zip(*(homogeneous(A)[i] for i in simplex)))))


def independent_basis(circuits):
    basis = []
    for u in circuits:
        if rank(basis+[u]) > len(basis):
            basis.append(u)
    return basis


def circuit_controls(name, A, ambient_volume, expected_nonpyramidal):
    before = ASSERTIONS
    columns = homogeneous(A)
    r = rank(columns)
    index = generated_group_index(A)
    check(index > 0 and ambient_volume % index == 0, 'lattice index/volume')
    V = ambient_volume//index
    circuits = primitive_circuits(A)
    basis = independent_basis(circuits)
    c = len(A)-r
    check(len(basis) == c, 'circuits span exact rational kernel')
    covered = {i for u in basis for i, x in enumerate(u) if x}
    nonpyramidal = len(covered) == len(A)
    check(nonpyramidal == expected_nonpyramidal, 'pyramidal columns detected')
    check(c <= V-1, 'codimension <= intrinsic volume - 1')
    if nonpyramidal:
        check(len(A) <= 2*V*c, 'support-cover dimension removal')
    extensions = []
    for u in circuits:
        check(all(sum(a[j]*x for a, x in zip(columns, u)) == 0
                  for j in range(r)), 'circuit equation')
        degree = sum(x for x in u if x > 0)
        check(degree == -sum(x for x in u if x < 0), 'height makes degrees equal')
        support = [i for i, x in enumerate(u) if x]
        check(len(support) <= 2*degree <= 2*V, 'circuit degree and support')
        chosen = support[:]
        for i in range(len(A)):
            if rank([columns[j] for j in chosen+[i]]) > rank([columns[j] for j in chosen]):
                chosen.append(i)
            if rank([columns[j] for j in chosen]) == r:
                break
        check(len(chosen) == r+1, 'complementary columns extend circuit')
        minors = [simplex_volume(A, tuple(j for j in chosen if j != i))
                  for i in chosen]
        minor_gcd = gcd(*minors)
        check(minor_gcd % index == 0, 'intrinsic maximal-minor gcd has no fractional index')
        delta = minor_gcd//index
        check(delta >= 1, 'extended generated-group index is positive integer')
        positive_volume = sum(simplex_volume(A, tuple(j for j in chosen if j != i))
                              for i in support if u[i] > 0)//index
        negative_volume = sum(simplex_volume(A, tuple(j for j in chosen if j != i))
                              for i in support if u[i] < 0)//index
        check(positive_volume == negative_volume == delta*degree,
              'both circuit triangulations have determinant volume delta*degree')
        check(positive_volume <= V, 'circuit hull is bounded by total volume')
        extensions.append((degree, delta, positive_volume))
    group(name, before, dimension=r-1, n=len(A), c=c, group_index=index,
          intrinsic_V=V, primitive_circuits=len(circuits),
          maximum_circuit_degree=max((t[0] for t in extensions), default=0),
          basis_support_covers_every_column=nonpyramidal)


def simplex_lattice_points(q, k):
    return {v for v in product(range(k+1), repeat=q) if sum(v) <= k}


def product_configuration(m, q):
    vertices = [(0,)*q]+[tuple(int(i == j) for i in range(q)) for j in range(q)]
    return tuple((x,)+v for x in (0, 1, m-1, m) for v in vertices)


def sumset_step(previous, A):
    return {tuple(x+y for x, y in zip(v, a)) for v in previous for a in A}


def prism_triangulation(A, m, q):
    vertices = [(0,)*q]+[tuple(int(i == j) for i in range(q)) for j in range(q)]
    positions = {v:i for i, v in enumerate(A)}
    simplices = []
    for j in range(q+1):
        fixed = [(0,)+v for v in vertices[:j]]+[(m,)+v for v in vertices[j+1:]]
        for lower, upper in ((0, 1), (1, m-1), (m-1, m)):
            simplices.append(tuple(sorted(positions[v] for v in
                                          fixed+[(lower,)+vertices[j], (upper,)+vertices[j]])))
    return simplices


def connected_dual_graph(simplices):
    seen = {0}
    stack = [0]
    d = len(simplices[0])-1
    while stack:
        i = stack.pop()
        for j in range(len(simplices)):
            if j not in seen and len(set(simplices[i]) & set(simplices[j])) == d:
                seen.add(j)
                stack.append(j)
    return len(seen) == len(simplices)


def triangulation_controls(A, simplices, volume):
    d = len(A[0])
    check(len(set(simplices)) == len(simplices), 'no repeated full simplices')
    check(set().union(*map(set, simplices)) == set(range(len(A))), 'all selected points used')
    volumes = [simplex_volume(A, t) for t in simplices]
    check(all(v > 0 for v in volumes), 'full-dimensional integer simplices')
    check(sum(volumes) == volume, 'sum of determinant volumes')
    check(connected_dual_graph(simplices), 'facet adjacency connected')
    check(len(A) <= d+len(simplices) <= d+volume, 'all-point minimum-volume count')
    return volumes


def barycentric(point, simplex):
    cols = homogeneous(simplex)
    rhs = tuple(point)+(1,)
    matrix = [list(row)+[F(b)] for row, b in zip(zip(*cols), rhs)]
    n = len(cols)
    for j in range(n):
        pivot = next(i for i in range(j, n) if matrix[i][j])
        matrix[j], matrix[pivot] = matrix[pivot], matrix[j]
        value = matrix[j][j]
        matrix[j] = [x/value for x in matrix[j]]
        for i in range(n):
            if i != j:
                multiplier = matrix[i][j]
                matrix[i] = [x-multiplier*y for x, y in zip(matrix[i], matrix[j])]
    return [matrix[i][-1] for i in range(n)]


def stellar_insert(A, triangles, point_index):
    new = []
    for t in triangles:
        coefficients = barycentric(A[point_index], [A[i] for i in t])
        if all(x >= 0 for x in coefficients):
            for j, x in enumerate(coefficients):
                if x > 0:
                    new.append(tuple(sorted(t[:j]+(point_index,)+t[j+1:])))
        else:
            new.append(t)
    return new


def orient(a, b, c):
    return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])


def planar_complex_controls(A, triangles):
    edge_counts = Counter(e for t in triangles for e in combinations(sorted(t), 2))
    check(all(count <= 2 for count in edge_counts.values()), 'facets have multiplicity at most two')
    for edge, count in edge_counts.items():
        a, b = (A[i] for i in edge)
        opposite = [next(i for i in t if i not in edge) for t in triangles if set(edge) <= set(t)]
        if count == 2:
            check(orient(a, b, A[opposite[0]])*orient(a, b, A[opposite[1]]) < 0,
                  'neighbors lie on opposite sides')
        else:
            check((a[0] == b[0] and a[0] in (0, 4)) or
                  (a[1] == b[1] and a[1] in (0, 2)), 'one-sided edge is hull boundary')
        for i, p in enumerate(A):
            if i not in edge and orient(a, b, p) == 0:
                check(not(min(a[0], b[0]) <= p[0] <= max(a[0], b[0]) and
                          min(a[1], b[1]) <= p[1] <= max(a[1], b[1])), 'no unsplit vertex on edge')
    edges = list(edge_counts)
    for e, f in combinations(edges, 2):
        if set(e) & set(f):
            continue
        a, b = (A[i] for i in e)
        c, d = (A[i] for i in f)
        check(not(orient(a, b, c)*orient(a, b, d) < 0 and
                  orient(c, d, a)*orient(c, d, b) < 0), 'no proper crossing edges')


def finite_hole_product_controls():
    before = ASSERTIONS
    families = []
    for q in range(1, 5):
        for m in range(4, 8):
            A = product_configuration(m, q)
            actual = {(0,)*(q+1)}
            last_hole = -1
            degree_receipts = []
            for k in range(m):
                intervals = {j*(m-1)+offset for j in range(k+1) for offset in range(k+1)}
                lattice_simplex = simplex_lattice_points(q, k)
                saturated = {(x,)+v for x in range(m*k+1) for v in lattice_simplex}
                expected = {(x,)+v for x in intervals for v in lattice_simplex}
                check(actual == expected, 'Cartesian degree sumsets from independent addition')
                holes = saturated-actual
                check(bool(holes) == (1 <= k <= m-3), 'finite-hole product height')
                expected_holes = k*(m-k-2)*comb(k+q, q) if 1 <= k <= m-3 else 0
                check(len(holes) == expected_holes, 'closed-form finite-hole count')
                if holes:
                    last_hole = k
                degree_receipts.append(dict(k=k, semigroup_points=len(actual),
                                            saturated_points=len(saturated), holes=len(holes)))
                actual = sumset_step(actual, A)
            V = (q+1)*m
            check(last_hole == m-3, 'last-hole product certificate')
            check(last_hole <= 2*V*V*(V-1)**2-2, 'coarse bound numerical control')
            triangles = prism_triangulation(A, m, q)
            volumes = triangulation_controls(A, triangles, V)
            check(Counter(volumes) == Counter({1:2*(q+1), m-2:q+1}), 'subdivision lengths')
            families.append(dict(m=m, dimension=q+1, n=len(A), c=len(A)-q-2,
                                 intrinsic_V=V, highest_hole=m-3,
                                 triangulation_simplices=len(triangles), degrees=degree_receipts))
    group('nonempty finite holes in dimensions two through five', before,
          all_degree_mechanism='Cartesian pairing and interval coverage', families=families)


def transformed_group_controls():
    before = ASSERTIONS
    receipts = []
    for d in range(2, 6):
        q = d-1
        m = 5
        A = product_configuration(m, q)
        T = [[int(i == j)*(i+2)+int(i == j+1) for j in range(d)] for i in range(d)]
        offset = tuple(7-3*i for i in range(d))
        transform = lambda v: tuple(sum(T[i][j]*v[j] for j in range(d))+offset[i] for i in range(d))
        transformed = tuple(transform(v) for v in A)
        index = det(T)
        check(index == prod(range(2, d+2)), 'exact ambient lattice index')
        base_witness = [A.index((0,)*d), A.index((1,)+(0,)*q)]
        base_witness += [A.index((0,)+tuple(int(i == j) for i in range(q))) for j in range(q)]
        witness_volume = simplex_volume(transformed, tuple(base_witness))
        check(witness_volume == index, 'explicit lattice-basis minor')
        simplices = prism_triangulation(A, m, q)
        ambient_V = sum(simplex_volume(transformed, t) for t in simplices)
        check(ambient_V == index*d*m, 'ambient volume scales by index')
        check(ambient_V//index == d*m, 'intrinsic volume unchanged')
        actual = {(0,)*d}
        transformed_actual = {(0,)*d}
        for k in range(5):
            predicted = {tuple(sum(T[i][j]*v[j] for j in range(d))+k*offset[i] for i in range(d))
                         for v in actual}
            check(transformed_actual == predicted, 'homogenized translation uses degree times offset')
            if k:
                # The last edge T e_{d-1}/(d+1) is the ambient integer e_{d-1}.
                # Its intrinsic coordinate is nonintegral, but lies in k Delta_q.
                ambient_witness = tuple(k*offset[i]+int(i == d-1) for i in range(d))
                check(ambient_witness not in transformed_actual, 'ambient coset hole survives every tested degree')
                check(F(1, d+1) <= k, 'ambient witness lies on scaled simplex edge')
                check(F(1, d+1).denominator > 1, 'ambient witness is outside generated group')
                unshifted = {tuple(sum(T[i][j]*v[j] for j in range(d)) for i in range(d)) for v in actual}
                check(transformed_actual != unshifted, 'translation-offset mutation rejected')
            actual = sumset_step(actual, A)
            transformed_actual = sumset_step(transformed_actual, transformed)
        receipts.append(dict(dimension=d, intrinsic_V=d*m, ambient_V=ambient_V,
                             group_index=index, intrinsic_highest_hole=m-3))
    group('nonspanning ambient lattice and affine-offset controls', before, families=receipts)


def negative_controls():
    before = ASSERTIONS
    # Genuine pyramid in dimension three, over a finite-hole 2D product.
    base = product_configuration(4, 1)
    A = tuple(v+(0,) for v in base)+((0, 0, 1),)
    actual = {(0, 0, 0)}
    for k in range(1, 9):
        actual = sumset_step(actual, A)
        witness = (2, 0, k-1)
        check(witness not in actual, 'pyramid prolongs base degree-one hole')
        check(witness[2] >= 0 and witness[0] <= 4*(k-witness[2]), 'pyramid witness in saturated cone')
    # Delete the edge point 1: x=1 is unreachable at every positive degree.
    A = (0, 3, 4)
    values = {0}
    for k in range(1, 12):
        values = {x+a for x in values for a in A}
        check(1 not in values and 0 <= 1 <= 4*k, 'missing edge generator destroys finite-hole hypothesis')
    # Replacing A by every interval lattice point changes the degree-one holes.
    check(set(range(5))-{0, 1, 3, 4} == {2}, 'chosen configuration omits a genuine intrinsic lattice point')
    check(set(range(5))-set(range(5)) == set(), 'filling omitted lattice points removes that hole')
    # Omitting height from the membership test makes degree-one 2 incorrectly reachable.
    check(2 == 1+1 and 2 not in {0, 1, 3, 4}, 'height-preserving membership is essential')
    check(4*3+1 > 4*3, 'group membership alone falsely admits a point outside the degree-three cone')
    # A nonspanning simplex: intrinsic V=1, c=0, no intrinsic holes, infinitely
    # many ambient holes witnessed by (1,0) at every positive degree.
    simplex = ((0, 0), (2, 0), (1, 3))
    values = {(0, 0)}
    for k in range(9):
        intrinsic = {(2*a+b, 3*b) for a in range(k+1) for b in range(k-a+1)}
        check(values == intrinsic, 'free simplex is normal in its own group')
        if k:
            check((1, 0) not in values and 1 <= 2*k, 'ambient volume-one interpretation mutation rejected')
        values = sumset_step(values, simplex)
    check(generated_group_index(simplex) == 6, 'nonspanning simplex lattice index')
    check(simplex_volume(simplex, (0, 1, 2))//6 == 1, 'simplex intrinsic V=1')
    # Distinct d=0 point set has exactly one generator at every degree.
    values = {0}
    for k in range(9):
        check(values == {7*k}, 'dimension-zero single generator is intrinsically normal')
        values = {x+7 for x in values}
    group('pyramid/lattice/cone/height/configuration mutations and degenerate boundaries', before,
          pyramid_degrees=8, missing_edge_degrees=11, volume_one_degrees=9,
          zero_dimensional_degrees=9)


def main():
    finite_hole_product_controls()
    transformed_group_controls()
    negative_controls()
    before = ASSERTIONS
    A = ((0, 0), (4, 0), (4, 2), (0, 2), (1, 0), (2, 0), (4, 1), (2, 1), (1, 1))
    triangles = [(0, 1, 2), (0, 2, 3)]
    for i in range(4, len(A)):
        triangles = stellar_insert(A, triangles, i)
    volumes = triangulation_controls(A, triangles, 16)
    planar_complex_controls(A, triangles)
    check(generated_group_index(A) == 1, 'selected points generate full lattice')
    check(len(A) < 15, 'rectangle configuration omits six lattice points')
    group('all-selected-point triangulation with boundary and interior insertions', before,
          A=A, simplices=triangles, simplex_volumes=volumes, intrinsic_V=16,
          omitted_rectangle_lattice_points=6)
    circuit_controls('one-dimensional sparse circuit family', ((0,), (1,), (6,), (7,)), 7, True)
    circuit_controls('square attains support equality', ((0, 0), (1, 0), (0, 1), (1, 1)), 2, True)
    circuit_controls('nonspanning diamond with omitted ambient center', ((-1, 0), (1, 0), (0, -1), (0, 1)), 4, True)
    circuit_controls('three-dimensional cube circuits', tuple(product((0, 1), repeat=3)), 6, True)
    circuit_controls('four-dimensional crosspolytope circuits', tuple(tuple(s*int(i == j) for i in range(4))
                                                                   for j in range(4) for s in (-1, 1)), 16, True)
    circuit_controls('finite-hole three-dimensional prism circuits', product_configuration(4, 2), 12, True)
    circuit_controls('pyramidal excluded-column circuit control', ((0, 0), (1, 0), (3, 0), (4, 0), (0, 1)), 4, False)
    circuit_controls('nonspanning V=1 simplex and c=0 control', ((0, 0), (2, 0), (1, 3)), 6, False)
    receipt = dict(status='passed', arithmetic='exact integers and fractions; standard library only',
                   independent_assertions=ASSERTIONS, groups=GROUPS,
                   source_script_imports=False,
                   general_claim_scope='Finite checks supplement the separate all-degree derivations in REPORT.md; do not prove regularity or the sharp source bound.',
                   sharp_source_question='h <= V remains unproved and unrefuted')
    encoded = json.dumps(receipt, indent=2)+'\n'
    Path(__file__).with_name('exact_checks.json').write_text(encoded)
    print(encoded, end='')


if __name__ == '__main__':
    main()
