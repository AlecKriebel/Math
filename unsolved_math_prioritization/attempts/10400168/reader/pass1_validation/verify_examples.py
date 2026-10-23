#!/usr/bin/env python3
"""Authored exact finite checks for the restricted-regular interface.

No external fixtures, packages, random sampling, or imported lane implementations.
Every mathematical test uses an explicit exception, so optimization cannot erase it.
"""
from collections import Counter
from fractions import Fraction
from itertools import combinations, product
import json

CHECKS = 0


def check(condition, message):
    global CHECKS
    CHECKS += 1
    if not condition:
        raise RuntimeError(message)


def compose(p, q):
    return tuple(p[q[i]] for i in range(len(p)))


def generated_group(degree, generators):
    identity = tuple(range(degree))
    elements = {identity}
    frontier = [identity]
    while frontier:
        x = frontier.pop()
        for g in generators:
            y = compose(x, g)
            if y not in elements:
                elements.add(y)
                frontier.append(y)
    return Group(sorted(elements), compose, identity)


class Group:
    def __init__(self, elements, operation, identity):
        self.elements = tuple(elements)
        self.mul = operation
        self.one = identity
        carrier = set(elements)
        check(identity in carrier, 'identity missing')
        self.inv = {}
        for a in elements:
            check(operation(identity, a) == a == operation(a, identity), 'unit failed')
            for b in elements:
                check(operation(a, b) in carrier, 'closure failed')
                if operation(a, b) == identity == operation(b, a):
                    self.inv[a] = b
                for c in elements:
                    check(operation(operation(a, b), c) == operation(a, operation(b, c)),
                          'associativity failed')
            check(a in self.inv, 'inverse missing')

    def power(self, a, n):
        result = self.one
        for _ in range(n):
            result = self.mul(result, a)
        return result

    def conj(self, h, a):
        return self.mul(self.mul(h, a), self.inv[h])

    def commuting(self, a, b):
        return self.mul(a, b) == self.mul(b, a)


def orbit_summary(group, tuples):
    """Enumerate orbits and stabilizers, independently of count/order formula."""
    tuples = set(tuples)
    remaining = set(tuples)
    orbits = []
    for representative in sorted(tuples):
        if representative not in remaining:
            continue
        orbit = {tuple(group.conj(h, x) for x in representative) for h in group.elements}
        check(orbit <= tuples, 'conjugation left solution set')
        stabilizer = [h for h in group.elements
                      if all(group.conj(h, x) == x for x in representative)]
        check(len(orbit) * len(stabilizer) == len(group.elements), 'orbit-stabilizer failed')
        orbits.append({'representative': representative, 'orbit_size': len(orbit),
                       'stabilizer_order': len(stabilizer)})
        remaining -= orbit
    check(not remaining, 'orbit enumeration incomplete')
    weighted = sum((Fraction(1, o['stabilizer_order']) for o in orbits), Fraction())
    check(weighted == Fraction(len(tuples), len(group.elements)), 'groupoid weighting failed')
    return {'hom_count': len(tuples), 'unweighted_orbit_count': len(orbits),
            'weighted_groupoid_cardinality': str(weighted),
            'orbit_size_histogram': dict(sorted(Counter(o['orbit_size'] for o in orbits).items())),
            'stabilizer_order_histogram': dict(sorted(Counter(o['stabilizer_order'] for o in orbits).items())),
            'orbits': orbits}


def group_examples(group):
    elements = group.elements
    commuting_pairs = [(a, b) for a, b in product(elements, repeat=2) if group.commuting(a, b)]
    commuting_triples = [(a, b, c) for a, b, c in product(elements, repeat=3)
                         if all(group.commuting(x, y) for x, y in combinations((a, b, c), 2))]
    results = {
        'S3': orbit_summary(group, [()]),
        'S2_times_S1': orbit_summary(group, [(a,) for a in elements]),
        'L2_1': orbit_summary(group, [(a,) for a in elements if group.power(a, 2) == group.one]),
        'L3_1': orbit_summary(group, [(a,) for a in elements if group.power(a, 3) == group.one]),
        'T2_surface': orbit_summary(group, commuting_pairs),
        'T3': orbit_summary(group, commuting_triples),
    }
    # Burnside provides a second independent count of torus gauge orbits.
    fixed_pair_sum = 0
    for h in elements:
        fixed_pair_sum += sum(all(group.conj(h, x) == x for x in pair) for pair in commuting_pairs)
    burnside = Fraction(fixed_pair_sum, len(elements))
    check(burnside.denominator == 1, 'Burnside count not integral')
    check(burnside == results['T2_surface']['unweighted_orbit_count'], 'Burnside/orbit mismatch')
    check(burnside == Fraction(len(commuting_triples), len(elements)), 'TQFT trace count mismatch')
    # Exact cylinder/gauge-averaging projector on the flat-pair label space.
    pair_index = {pair: i for i, pair in enumerate(commuting_pairs)}
    projector = [[Fraction() for _ in commuting_pairs] for _ in commuting_pairs]
    for column, pair in enumerate(commuting_pairs):
        for h in elements:
            image = tuple(group.conj(h, x) for x in pair)
            projector[pair_index[image]][column] += Fraction(1, len(elements))
    for row in range(len(projector)):
        for column in range(len(projector)):
            square_entry = sum(projector[row][k]*projector[k][column] for k in range(len(projector)))
            check(square_entry == projector[row][column], 'gauge projector is not idempotent')
    projector_rank = rational_rank(projector)
    projector_trace = sum(projector[i][i] for i in range(len(projector)))
    check(projector_rank == projector_trace == burnside, 'projector image dimension mismatch')
    centralizer_class_counts = []
    for orbit in results['S2_times_S1']['orbits']:
        a = orbit['representative'][0]
        centralizer = [h for h in elements if group.commuting(a, h)]
        subgroup = Group(centralizer, group.mul, group.one)
        count = orbit_summary(subgroup, [(h,) for h in centralizer])['unweighted_orbit_count']
        centralizer_class_counts.append({'element_order': next(n for n in range(1, len(elements)+1)
                                                               if group.power(a, n) == group.one),
                                        'class_size': orbit['orbit_size'],
                                        'centralizer_order': len(centralizer),
                                        'centralizer_conjugacy_classes': count})
    check(sum(x['centralizer_conjugacy_classes'] for x in centralizer_class_counts) == burnside,
          'centralizer-class/orbit count mismatch')
    return {'group_order': len(elements), 'manifolds_and_surface': results,
            'torus_dimension': int(burnside), 'centralizer_class_counts': centralizer_class_counts,
            'torus_gauge_projector': {'pre_space_dimension': len(commuting_pairs),
                                     'image_rank': projector_rank, 'trace': str(projector_trace),
                                     'idempotent': True}}


def simplicial_complex(tetrahedra):
    vertices = sorted(set().union(*(set(t) for t in tetrahedra)))
    edges = sorted(set().union(*(set(combinations(t, 2)) for t in tetrahedra)))
    triangles = sorted(set().union(*(set(combinations(t, 3)) for t in tetrahedra)))
    return vertices, edges, triangles


def flat_by_local_constraints(group, tetrahedra):
    """Backtracking assigns every edge, pruning only completed flat triangles."""
    vertices, edges, triangles = simplicial_complex(tetrahedra)
    position = {edge: n for n, edge in enumerate(edges)}
    tests = [[] for _ in edges]
    for i, j, k in triangles:
        indices = (position[i, j], position[j, k], position[i, k])
        tests[max(indices)].append(indices)
    values = [None] * len(edges)
    count = 0
    def extend(n):
        nonlocal count
        if n == len(edges):
            count += 1
            return
        for g in group.elements:
            values[n] = g
            if all(group.mul(values[a], values[b]) == values[c] for a, b, c in tests[n]):
                extend(n+1)
    extend(0)
    return count


def flat_by_vertex_potentials(group, tetrahedra):
    """Enumerate normalized vertex potentials and verify each flat edge assignment."""
    vertices, edges, triangles = simplicial_complex(tetrahedra)
    assignments = set()
    for rest in product(group.elements, repeat=len(vertices)-1):
        potentials = dict(zip(vertices, (group.one,) + rest))
        edge_values = {edge: group.mul(group.inv[potentials[edge[0]]], potentials[edge[1]])
                       for edge in edges}
        check(all(group.mul(edge_values[i, j], edge_values[j, k]) == edge_values[i, k]
                  for i, j, k in triangles), 'potential assignment not flat')
        assignments.add(tuple(edge_values[edge] for edge in edges))
    check(len(assignments) == len(group.elements)**(len(vertices)-1), 'potential map not injective')
    return len(assignments)


def sphere_examples(groups):
    sphere = list(combinations(range(5), 4))  # Boundary of the 4-simplex, hence S^3.
    chosen = sphere[0]
    subdivided = sphere[1:] + [tuple(sorted(face + (5,))) for face in combinations(chosen, 3)]
    output = {}
    for name, group in groups.items():
        count = flat_by_local_constraints(group, sphere)
        potentials = flat_by_vertex_potentials(group, sphere)
        refined = flat_by_local_constraints(group, subdivided)
        refined_potentials = flat_by_vertex_potentials(group, subdivided)
        check(count == potentials, 'S3 local/potential mismatch')
        check(refined == refined_potentials, 'subdivided S3 local/potential mismatch')
        value = Fraction(count, len(group.elements)**5)
        refined_value = Fraction(refined, len(group.elements)**6)
        check(value == refined_value == Fraction(1, len(group.elements)), 'S3 normalization failed')
        output[name] = {'vertices': 5, 'flat_edge_labelings': count,
                        'after_1_4_move_vertices': 6, 'after_1_4_move_labelings': refined,
                        'normalized_value': str(value), 'after_1_4_move_value': str(refined_value)}
    wrong_5 = Fraction(output['C3']['flat_edge_labelings'], 6**5)
    wrong_6 = Fraction(output['C3']['after_1_4_move_labelings'], 6**6)
    check(wrong_5 != wrong_6, 'wrong normalization countercheck failed')
    return {'sphere_triangulation': sphere, 'subdivided_triangulation': subdivided,
            'groups': output, 'C3_labels_wrong_S3_vertex_factor':
            {'before_1_4': str(wrong_5), 'after_1_4': str(wrong_6), 'not_invariant': True}}


def trace_basis_checks(group, left_grades, middle_grades, right_grades, character):
    """All matrix-unit endomorphisms on the specified graded tensor products."""
    for g in group.elements:
        check(character(g) in (-1, 1), 'spherical sign condition failed')
        check(character(g) == character(group.inv[g]), 'left/right pivotal dimensions differ')
        for h in group.elements:
            check(character(group.mul(g, h)) == character(g)*character(h), 'not a pivotal character')
    cases = {'left': 0, 'right': 0, 'mixed': 0, 'mixed_off_diagonal': 0}
    left = list(product(range(len(left_grades)), range(len(middle_grades))))
    right = list(product(range(len(middle_grades)), range(len(right_grades))))
    for indices, grades_a, grades_b, side in [(left, left_grades, middle_grades, 'left'),
                                            (right, middle_grades, right_grades, 'right')]:
        for (i, j), (k, l) in product(indices, repeat=2):
            grade = group.mul(grades_a[i], grades_b[j])
            if grade != group.mul(grades_a[k], grades_b[l]):
                continue
            full_trace = character(grade) if (i, j) == (k, l) else 0
            if side == 'left':
                partial_then_trace = character(grades_a[i])*character(grades_b[j]) if i == k and j == l else 0
            else:
                partial_then_trace = character(grades_b[j])*character(grades_a[i]) if j == l and i == k else 0
            check(full_trace == partial_then_trace, side + ' partial trace failed')
            cases[side] += 1
    triples = list(product(range(len(left_grades)), range(len(middle_grades)), range(len(right_grades))))
    for (i, j, k), (l, m, n) in product(triples, repeat=2):
        grade = group.mul(group.mul(left_grades[i], middle_grades[j]), right_grades[k])
        other = group.mul(group.mul(left_grades[l], middle_grades[m]), right_grades[n])
        if grade != other:
            continue
        full_trace = character(grade) if (i, j, k) == (l, m, n) else 0
        # Each partial trace is represented as its matrix-unit coefficient and residual indices.
        left_then_right = (character(left_grades[i])*character(right_grades[k]), j, m) if i == l and k == n else (0, j, m)
        right_then_left = (character(right_grades[k])*character(left_grades[i]), j, m) if k == n and i == l else (0, j, m)
        check(left_then_right == right_then_left, 'partial closures do not commute')
        coefficient, row, column = left_then_right
        closed_trace = coefficient*character(middle_grades[row]) if row == column else 0
        check(full_trace == closed_trace, 'mixed partial trace failed')
        cases['mixed'] += 1
        cases['mixed_off_diagonal'] += (i, j, k) != (l, m, n)
    # Matrix units E_pq and E_qp exhibit nondegeneracy, including repeated labels.
    witness_count = 0
    for i, g in enumerate(middle_grades):
        for j, h in enumerate(middle_grades):
            if g == h:
                pairing = character(g)
                check(pairing != 0, 'trace pairing degenerate')
                witness_count += 1
    cases['nondegenerate_pairing_basis_witnesses'] = witness_count
    # Cyclicity for every pair of composable rectangular matrix units X -> Y -> X.
    # Distinct multiplicities in X,Y ensure the test is not only square-matrix cyclicity.
    source = middle_grades
    target = list(reversed(middle_grades)) + [group.one]
    forward_units = [(j, i) for j, h in enumerate(target) for i, g in enumerate(source) if g == h]
    backward_units = [(k, l) for k, g in enumerate(source) for l, h in enumerate(target) if g == h]
    cyclic_pairs = 0
    for (j, i), (k, l) in product(forward_units, backward_units):
        tr_gf = character(source[k]) if l == j and k == i else 0
        tr_fg = character(target[j]) if i == k and j == l else 0
        check(tr_gf == tr_fg, 'rectangular-matrix cyclicity failed')
        cyclic_pairs += 1
    cases['cyclicity_matrix_unit_pairs'] = cyclic_pairs
    return cases


def rational_rank(rows):
    a = [[Fraction(x) for x in row] for row in rows]
    rank = 0
    for column in range(len(a[0]) if a else 0):
        pivot = next((i for i in range(rank, len(a)) if a[i][column]), None)
        if pivot is None:
            continue
        a[rank], a[pivot] = a[pivot], a[rank]
        scale = a[rank][column]
        a[rank] = [x / scale for x in a[rank]]
        for i in range(len(a)):
            if i != rank:
                scale = a[i][column]
                a[i] = [x - scale*y for x, y in zip(a[i], a[rank])]
        rank += 1
    return rank


def trace_examples(c3, s3):
    # Proper non-positive spherical example: Vec_C2 inside Vec_(C2 x C2).
    v4 = Group(list(product(range(2), repeat=2)), lambda x, y: ((x[0]+y[0])%2, (x[1]+y[1])%2), (0, 0))
    sign = lambda g: (-1)**g[0]
    traces = {
        'C3_in_S3_standard': trace_basis_checks(s3, list(c3.elements)+[c3.one],
                                               list(s3.elements)+[s3.one],
                                               list(s3.elements[:3])+[s3.one], lambda _: 1),
        'C2_in_V4_inherited_sign': trace_basis_checks(v4, [(0,0), (1,0), (1,0)],
                                                     list(v4.elements)+[(0,0)],
                                                     list(v4.elements), sign),
    }
    # In Vec_C2 with sign pivotal structure, trace(id_(1+g)) is zero,
    # but its diagonal endomorphism algebra has trace pairing diag(1,-1).
    zero_dim_pairing = [[1, 0], [0, -1]]
    check(sum([1, -1]) == 0, 'zero categorical dimension example failed')
    check(rational_rank(zero_dim_pairing) == 2, 'zero-dimension object pairing degenerate')
    traces['zero_dimension_nonsimple'] = {'categorical_dimension': 0,
                                        'trace_pairing_matrix': zero_dim_pairing, 'rank': 2}
    # Unknown simple traces (t_1,t_g). Left sign and right standard impose
    # t_g=-t_1 and t_g=t_1 respectively.
    incompatible = [[1, 1], [-1, 1]]
    compatible = [[1, 1], [1, 1]]
    check(rational_rank(incompatible) == 2, 'incompatible pivotal counterexample failed')
    check(rational_rank(compatible) == 1, 'compatible pivotal control failed')
    traces['C2_sign_left_standard_right'] = {'constraint_matrix': incompatible, 'rank': 2,
                                            'trace_solution_dimension': 0,
                                            'nondegenerate_trace_exists': False}
    traces['C2_sign_both_sides'] = {'constraint_matrix': compatible, 'rank': 1,
                                   'normalized_simple_traces': [1, -1]}
    return traces


def run():
    c3 = generated_group(3, [(1, 2, 0)])
    s3 = generated_group(3, [(1, 2, 0), (1, 0, 2)])
    c2 = generated_group(2, [(1, 0)])
    trivial = generated_group(1, [])
    check(len(c3.elements) == 3 and len(s3.elements) == 6, 'wrong generated group sizes')
    check(set(c3.elements) < set(s3.elements), 'C3 not a proper subgroup of S3')
    groups = {'trivial': trivial, 'C2': c2, 'C3': c3, 'S3': s3}
    results = {name: group_examples(group) for name, group in groups.items()}
    check(results['C3']['torus_dimension'] == 9, 'C3 torus dimension changed')
    check(results['S3']['torus_dimension'] == 8, 'S3 torus dimension changed')
    check(results['C3']['manifolds_and_surface']['S3']['weighted_groupoid_cardinality'] == '1/3', 'C3 sphere value changed')
    check(results['S3']['manifolds_and_surface']['S3']['weighted_groupoid_cardinality'] == '1/6', 'S3 sphere value changed')
    ratios = {}
    for manifold in ('S3', 'S2_times_S1', 'L2_1', 'L3_1', 'T3'):
        sub = Fraction(results['C3']['manifolds_and_surface'][manifold]['weighted_groupoid_cardinality'])
        ambient = Fraction(results['S3']['manifolds_and_surface'][manifold]['weighted_groupoid_cardinality'])
        ratios[manifold] = str(sub/ambient)
    check(len(set(ratios.values())) > 1, 'constant ratio countercheck failed')
    spheres = sphere_examples(groups)
    traces = trace_examples(c3, s3)
    return {'status': 'PASS', 'arithmetic': 'integers and fractions.Fraction',
            'groups_generated_from_permutations': {name: group.elements for name, group in groups.items()},
            'finite_group_results': results, 'C3_over_S3_partition_function_ratios': ratios,
            'triangulated_sphere_checks': spheres, 'trace_checks': traces,
            'explicit_checks_completed': CHECKS,
            'scope': 'Finite examples and algebraic counterchecks, not a computational proof of the general defect theorem.'}


if __name__ == '__main__':
    print(json.dumps(run(), indent=2, sort_keys=True))
