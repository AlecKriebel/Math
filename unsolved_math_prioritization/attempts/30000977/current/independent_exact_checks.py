#!/usr/bin/env python3
"""Independent finite interfaces for the credited GPR degree-12 example.

No candidate module is imported. The main computation starts with the six
Kummer equations, derives normalized eigen-differentials and tests all 729
character pairs against all 27 anti-diagonal elements. Geometry is audited
separately in SECOND_AUDIT.md. No assertions and no file writes are used.
"""
import argparse
from copy import deepcopy
from fractions import Fraction
from itertools import product
import json
import os

CHARS = list(product(range(3), repeat=3))
ZERO = (0, 0, 0)
ORDER = [(0, 1, 0), (1, 0, 1), (0, 2, 0), (2, 2, 2)]
# One row for each radical; columns are valuations at 0, 1, 2.
KUMMER_E = [[1, 2, 1], [1, 2, 2], [2, 0, 1]]
KUMMER_F = [[2, 0, 1], [1, 1, 2], [1, 2, 1]]
EXPECTED_E = [(1,1,2), (2,2,0), (1,2,1), (2,1,0)]
EXPECTED_F = [(2,1,1), (0,1,2), (1,2,1), (0,2,2)]
EXPECTED_DIVISORS = [
    [1,0,0,1,1,1,0,0], [2,0,0,0,2,0,0,0],
    [0,1,1,0,0,0,1,1], [0,0,0,2,0,2,0,0],
]
MUTANTS = [
    'rank_two_group', 'dependent_kummer_classes', 'diagonal_quotient',
    'opposite_F_generators', 'duality_sign_error', 'missing_canonical_section',
    'extra_canonical_section', 'wrong_divisor_coefficients',
    'omitted_singular_stratum', 'printed_quadric_relation',
    'smooth_quadric_claim', 'construction_degree_confusion',
]

def demand(value, code, detail):
    if not value:
        raise ValueError(code + ': ' + detail)

def dot(a, b):
    return sum(x*y for x, y in zip(a, b)) % 3

def multiple(k, v):
    return tuple(k*x % 3 for x in v)

def branch_from_equations(rows):
    finite = [tuple(rows[j][i] % 3 for j in range(3)) for i in range(3)]
    infinity = tuple(-sum(row) % 3 for row in rows)
    return finite + [infinity]

def matrix_rank(rows, modulus=3):
    a = deepcopy(rows)
    pivot = 0
    for j in range(len(a[0])):
        choices = [i for i in range(pivot, len(a)) if a[i][j] % modulus]
        if not choices:
            continue
        i = choices[0]
        a[pivot], a[i] = a[i], a[pivot]
        factor = pow(a[pivot][j] % modulus, -1, modulus)
        a[pivot] = [x*factor % modulus for x in a[pivot]]
        for i in range(len(a)):
            if i != pivot:
                factor = a[i][j]
                a[i] = [(x-factor*y) % modulus for x,y in zip(a[i], a[pivot])]
        pivot += 1
        if pivot == len(a):
            break
    return pivot

def differential_data(rows, c):
    # eta_c = product(t-i)^floor(w_i/3) dt / product(u_j^c_j).
    # At infinity dt has valuation -4 and a polynomial t^k subtracts 3k.
    w = [sum(c[j]*rows[j][i] for j in range(3)) for i in range(3)]
    floors = [x // 3 for x in w]
    finite_orders = [3*q+2-x for q,x in zip(floors, w)]
    infinity_order = sum(w) - 3*sum(floors) - 4
    allowed_powers = list(range(max(0, infinity_order//3+1)))
    branch = branch_from_equations(rows)
    residues = [dot(c, v) for v in branch]
    d = sum(residues)//3
    demand(sum(residues) % 3 == 0, 'DEGREE', 'Eigenline degree not integral.')
    demand(len(allowed_powers) == max(d-1, 0), 'DIFFERENTIAL', 'Pole-bound/duality disagreement.')
    return {'character': list(c), 'radical_valuations': w,
            'normalizing_polynomial_exponents': floors,
            'finite_zero_orders': finite_orders,
            'infinity_zero_order': infinity_order,
            'allowed_polynomial_powers': allowed_powers,
            'residues': residues, 'eigenline_degree': d,
            'dimension': len(allowed_powers)}

def audit(mutation=None):
    e_rows, f_rows = deepcopy(KUMMER_E), deepcopy(KUMMER_F)
    rank_claim, quotient_sign = 3, -1
    if mutation == 'rank_two_group': rank_claim = 2
    if mutation == 'dependent_kummer_classes': e_rows[2] = e_rows[0][:]
    if mutation == 'diagonal_quotient': quotient_sign = 1
    if mutation == 'opposite_F_generators':
        f_rows = [[(-x) % 3 for x in row] for row in f_rows]
    for name, rows in [('E', e_rows), ('F', f_rows)]:
        demand(matrix_rank(rows) == 3, 'KUMMER_INDEPENDENCE', name + ' valuation classes do not have rank three.')
    demand(rank_claim == 3, 'GROUP_RANK', 'Independent three Kummer classes give degree 27.')
    E, F = branch_from_equations(e_rows), branch_from_equations(f_rows)
    for name, vectors in [('E', E), ('F', F)]:
        demand(all(v != ZERO for v in vectors), 'INERTIA', name + ' has unramified listed point.')
        demand(tuple(sum(v[j] for v in vectors) % 3 for j in range(3)) == ZERO,
               'SPHERICAL', name + ' monodromy sum is not zero.')

    crossings = []
    singular_points = 0
    for i, e in enumerate(E):
        for j, f in enumerate(F):
            inertia_e = {multiple(k, e): k for k in range(3)}
            inertia_f = {multiple(k, f): k for k in range(3)}
            stabilizer = [g for g in CHARS if g in inertia_e and multiple(quotient_sign, g) in inertia_f]
            orbit_size = 27 // len(stabilizer)
            reduced_points = 81 // orbit_size
            rec = {'E': i+1, 'F': j+1, 'stabilizer_order': len(stabilizer),
                   'orbit_size': orbit_size, 'reduced_points_on_X': reduced_points}
            if len(stabilizer) > 1:
                weights = [(inertia_e[g], inertia_f[multiple(quotient_sign, g)])
                           for g in stabilizer if g != ZERO]
                demand(all((a+b) % 3 == 0 for a,b in weights),
                       'NONCANONICAL_LOCAL_ACTION', 'Stabilizer is not in SL(2): ' + str(weights))
                rec['nonidentity_tangent_weights'] = weights
                singular_points += reduced_points
            crossings.append(rec)
    singular_claim = 0 if mutation == 'omitted_singular_stratum' else 9
    demand(singular_points == singular_claim, 'SINGULAR_ORBITS', 'Nine A2 points cannot be omitted.')
    demand(E == EXPECTED_E and F == EXPECTED_F, 'KUMMER_MONODROMY', 'Source branch vectors not realized.')

    # Check the invariant semigroup and the standard module basis at A2.
    monomials_checked = 0
    for a,b in product(range(25), repeat=2):
        invariant = (a-b) % 3 == 0
        normal_forms = [(i,j,k) for k in range(3)
                        if a >= k and b >= k and (a-k) % 3 == (b-k) % 3 == 0
                        for i,j in [((a-k)//3, (b-k)//3)]]
        demand((len(normal_forms) == 1) == invariant,
               'A2_MODULE_BASIS', 'Invariant monomial lacks unique U^i V^j T^k normal form.')
        monomials_checked += 1

    ed = {c:differential_data(e_rows, c) for c in CHARS}
    fd = {c:differential_data(f_rows, c) for c in CHARS}
    demand(sum(x['dimension'] for x in ed.values()) == 10, 'GENUS_E', 'Differentials do not total ten.')
    demand(sum(x['dimension'] for x in fd.values()) == 10, 'GENUS_F', 'Differentials do not total ten.')
    invariant_pairs = []
    character_evaluations = 0
    for c,d in product(CHARS, repeat=2):
        tests = [(-dot(c,g)-quotient_sign*dot(d,g)) % 3 == 0 for g in CHARS]
        character_evaluations += len(tests)
        invariant = all(tests)
        demand(invariant == (c == d), 'ANTIDIAGONAL_CHARACTERS', 'Invariant characters must match.')
        if invariant and ed[c]['dimension'] and fd[d]['dimension']:
            invariant_pairs.append((c,d))
    derived = [c for c,d in invariant_pairs]
    claimed = list(ORDER)
    if mutation == 'duality_sign_error': claimed = [multiple(-1,c) for c in ORDER]
    if mutation == 'missing_canonical_section': claimed.remove((0,2,0))
    if mutation == 'extra_canonical_section': claimed.append((0,0,1))
    demand(set(derived) == set(claimed) and len(derived) == len(claimed),
           'COMPLETE_CANONICAL_BASIS', 'Claimed basis differs from all invariant holomorphic 2-forms.')
    pg = sum(ed[c]['dimension']*fd[d]['dimension'] for c,d in invariant_pairs)
    demand(pg == 4, 'PG', 'Canonical dimension is not four.')

    divisors = []
    for c in ORDER:
        a,b = ed[c],fd[c]
        orders = a['finite_zero_orders']+[a['infinity_zero_order']]+b['finite_zero_orders']+[b['infinity_zero_order']]
        demand(orders == [2-r for r in a['residues']+b['residues']],
               'LOCAL_DIVISOR', 'Explicit differential and residue divisor differ.')
        divisors.append(orders)
    if mutation == 'wrong_divisor_coefficients':
        divisors = [ed[c]['residues']+fd[c]['residues'] for c in ORDER]
    demand(divisors == EXPECTED_DIVISORS, 'CANONICAL_DIVISORS', 'Incorrect zero-order coefficients.')
    strata = []
    for i,j in product(range(-1,4), repeat=2):
        nonzero = [index for index,D in enumerate(divisors)
                   if (i < 0 or D[i] == 0) and (j < 0 or D[j+4] == 0)]
        demand(nonzero, 'BASEPOINT', 'No nonvanishing canonical section on stratum.')
        strata.append({'E': i+1, 'F': j+1, 'nonvanishing_basis_indices': nonzero})
    # The singular crossing is explicitly included, and A, B, D are units there.
    demand([i for i,D in enumerate(divisors) if D[2] == D[6] == 0] == [0,1,3],
           'SINGULAR_BASEPOINT', 'A, B, D must be nonzero at all nine singular points.')
    relation_rhs = (1,2) if mutation == 'printed_quadric_relation' else (1,3)
    demand([2*x for x in divisors[0]] == [x+y for x,y in zip(divisors[relation_rhs[0]], divisors[relation_rhs[1]])],
           'QUADRIC_RELATION', '2A equals B+D, not B+C.')
    # Check the relation as an actual rational differential identity as well:
    # eta_A^2/(eta_B*eta_D) has radical powers divisible by three, and
    # substituting the Kummer equations cancels every finite factor exactly.
    radical_powers = [-2*ORDER[0][j]+ORDER[1][j]+ORDER[3][j] for j in range(3)]
    demand(all(x % 3 == 0 for x in radical_powers), 'RATIONAL_RELATION', 'Ratio is not a base rational function.')
    for data, rows in [(ed,e_rows),(fd,f_rows)]:
        numerators = [data[c]['normalizing_polynomial_exponents'] for c in ORDER]
        net = [2*numerators[0][i]-numerators[1][i]-numerators[3][i]
               +sum((radical_powers[j]//3)*rows[j][i] for j in range(3)) for i in range(3)]
        demand(net == [0,0,0], 'RATIONAL_RELATION', 'Exact Kummer substitution does not give ratio one.')
    # Hessian of x0^2 - x1*x3 over Q; rank is independently computed modulo 5.
    hessian = [[2,0,0,0],[0,0,0,-1],[0,0,0,0],[0,-1,0,0]]
    rank = matrix_rank(hessian,5)
    rank_expected = 4 if mutation == 'smooth_quadric_claim' else 3
    demand(rank == rank_expected, 'SINGULAR_QUADRIC', 'The image equation has rank three.')
    genus = 1 + Fraction(27,2)*(-2+4*Fraction(2,3))
    k2 = Fraction(8*(genus-1)**2,27)
    k2_ramification = 27*2*Fraction(2,3)**2
    demand(genus == 10 and k2 == k2_ramification == 24, 'INTERSECTION', 'Inconsistent intersection invariants.')
    degree_claim = 27 if mutation == 'construction_degree_confusion' else 12
    demand(2*degree_claim == k2, 'CANONICAL_DEGREE', 'Construction cover and canonical morphism have different degrees.')
    return {'status':'PASS_FINITE_INTERFACES_ONLY', 'uid':os.getuid(), 'euid':os.geteuid(),
            'cover_degree':27,'canonical_degree':degree_claim,'genus_E':int(genus),
            'genus_F':int(genus),'K_squared':int(k2),'p_g':pg,'A2_points':singular_points,
            'quadric_rank':rank,'character_pairs_checked':729,
            'explicit_differential_relation':'theta_A^2 = theta_B * theta_D exactly',
            'character_group_evaluations':character_evaluations,
            'local_invariant_monomials_checked':monomials_checked,
            'complete_basis_duality_labels':[list(c) for c in ORDER],
            'divisors':divisors,'crossings':crossings,'branch_strata':strata,
            'character_table':[{'character':list(c),'d_E':ed[c]['eigenline_degree'],
                                'd_F':fd[c]['eigenline_degree'],
                                'canonical_dimension':ed[c]['dimension']*fd[c]['dimension']} for c in CHARS],
            'curve_differentials':{'E':list(ed.values()),'F':list(fd.values())},
            'boundary':'Existence, canonical singularity classification, descent, and finiteness require SECOND_AUDIT.md.'}

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--mutate', choices=MUTANTS)
    args = parser.parse_args()
    try:
        print(json.dumps(audit(args.mutate), sort_keys=True))
    except ValueError as exc:
        print(json.dumps({'status':'REJECTED','mutation':args.mutate,
                          'reason':str(exc),'uid':os.getuid(),'euid':os.geteuid()},sort_keys=True))
        raise SystemExit(2)
