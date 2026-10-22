#!/usr/bin/env python3
"""Additional exact authored checks, independently of the frozen verifier."""
import json
from itertools import product
import sympy as sp
from sympy.matrices.normalforms import smith_normal_form
from independent_cube import check, rank_f2, rank_q


def induced_rank(d, t):
    z = d.nullspace()
    kernel = sp.Matrix.hstack(*z) if z else sp.zeros(d.cols, 0)
    images = t*kernel
    return rank_f2(d.row_join(images).tolist(), d.cols+images.cols)-rank_f2(d.tolist(), d.cols)


def staircase(copies):
    # Each doubled block is (a,c,b,e,a',c',b',e').  Final two
    # generators survive and are paired by nu and X.
    dimension = 8*copies+2
    d, t, nu, x, zigzag = [sp.zeros(dimension) for _ in range(5)]
    for block in range(copies):
        for shift in (0, 4):
            a, c, b, e = [8*block+shift+j for j in range(4)]
            d[b, c] = 1
            t[b, a] = t[e, c] = 1
            zigzag[e, a] = 1
        for j in range(4):
            nu[8*block+4+j, 8*block+j] = 1
            x[8*block+j, 8*block+4+j] = 1
    nu[dimension-1, dimension-2] = 1
    x[dimension-2, dimension-1] = 1
    zero = sp.zeros(dimension)
    for operator in (d, t, nu, x):
        check(operator*operator == zero, 'Operator does not square to zero')
    check(d*t == t*d == zero, 'Double complex relation failed')
    check(d*nu == nu*d and d*x == x*d, 'Pairing is not a chain map')
    check(x*nu+nu*x == sp.eye(dimension), 'Pairing contraction failed')
    diagonal = smith_normal_form(d, domain=sp.ZZ)
    invariant_factors = [abs(int(diagonal[j, j])) for j in range(dimension) if diagonal[j, j]]
    check(all(v == 1 for v in invariant_factors), 'Integral d-homology is not free')
    rank_d = rank_f2(d.tolist(), dimension)
    rank_total = rank_f2((d+t).tolist(), dimension)
    first_rank = induced_rank(d, t)
    second_rank = induced_rank(d, zigzag)
    check(first_rank == 0 and second_rank == 2*copies, 'Incorrect page ranks')
    return {'doubled_blocks': copies, 'chain_dimension': dimension,
            'integral_d_nonzero_smith_factors': invariant_factors,
            'E1_dimension': dimension-2*rank_d,
            'first_differential_rank': first_rank,
            'second_differential_rank': second_rank,
            'total_d_plus_T_dimension': dimension-2*rank_total,
            'nu_X_contraction_and_chain_relations': True}


def compose(outer, inner):
    columns = []
    for v in inner:
        result, j = 0, 0
        while v:
            if v & 1:
                result ^= outer[j]
            v >>= 1
            j += 1
        columns.append(result)
    return tuple(columns)


def nilpotent_columns(parts):
    out, offset = [], 0
    for length in parts:
        out.extend(1 << (offset+j+1) if j+1 < length else 0 for j in range(length))
        offset += length
    return tuple(out)


def module_enumeration():
    partitions = [(), (1,), (2,), (1, 1), (3,), (2, 1), (1, 1, 1)]
    hom_count, composition_pairs, sharp_pairs = 0, 0, 0
    profiles = []
    for left in partitions:
        for right in partitions:
            hm, hn = nilpotent_columns(left), nilpotent_columns(right)
            fs = [f for f in product(range(1 << sum(right)), repeat=sum(left))
                  if compose(hn, f) == compose(f, hm)]
            gs = [g for g in product(range(1 << sum(left)), repeat=sum(right))
                  if compose(hm, g) == compose(g, hn)]
            hom_count += len(fs)+len(gs)
            matches = 0
            for f in fs:
                for g in gs:
                    if compose(g, f) != hm or compose(f, g) != hn:
                        continue
                    matches += 1
                    long_count = sum(length >= 2 for length in left)
                    check(long_count <= len(right), 'Module lemma failed')
                    check(sum(length >= 2 for length in right) <= len(left), 'Reverse module lemma failed')
                    sharp_pairs += int(long_count == len(right))
            if matches:
                profiles.append({'M_bars': left, 'N_bars': right, 'valid_map_pairs': matches})
                composition_pairs += matches
    return {'field': 'F2', 'dimension_limit_each_module': 3,
            'partition_pairs': len(partitions)**2,
            'R_linear_maps_across_both_directions_counted_with_profiles': hom_count,
            'valid_composition_pairs': composition_pairs,
            'sharp_pairs': sharp_pairs, 'verified_profiles': profiles,
            'scope': 'Finite nilpotent examples only; arbitrary fields and free summands are covered by the written proof.'}


def other_checks():
    bockstein = []
    for exponent in range(1, 5):
        value = 2**exponent
        matrix = sp.Matrix([[value]])
        rq, r2 = rank_q(matrix.tolist(), 1), rank_f2(matrix.tolist(), 1)
        beta = (value//2) % 2
        check(beta == int(exponent == 1), 'First Bockstein mismatch')
        bockstein.append({'differential': value, 'Q_homology_dimension': 2-2*rq,
                         'F2_homology_dimension': 2-2*r2, 'first_bockstein_rank': beta,
                         'cokernel_smith_factor': abs(int(smith_normal_form(matrix, domain=sp.ZZ)[0, 0]))})
    cycle_forms = []
    for n in range(3, 9):
        # Edge-relation rows instead of the original script's edge columns.
        matrix = sp.Matrix([[int(j == i or j == (i+1) % n) for j in range(n)] for i in range(n)])
        diagonal = smith_normal_form(matrix, domain=sp.ZZ)
        factors = [abs(int(diagonal[i, i])) for i in range(n)]
        check(factors == [1]*(n-1)+[2 if n % 2 else 0], 'Incidence mismatch')
        cycle_forms.append({'n': n, 'smith': factors})
    inclusion0, inclusion1 = sp.Matrix([[1], [0]]), sp.Matrix([[1]])
    projection0 = sp.Matrix([[0, 1]])
    da, db = sp.Matrix([[2]]), sp.Matrix([[2, 1]])
    check(db*inclusion0 == inclusion1*da, 'Skein inclusion not a chain map')
    check(projection0*inclusion0 == sp.zeros(1), 'Skein sequence not a complex')
    lift = sp.Matrix([[0], [1]])
    check(projection0*lift == sp.eye(1) and db*lift == sp.eye(1), 'Connecting class not generator')
    delta = sp.zeros(3)
    delta[2, 1] = 1
    sign = sp.diag(1, 1, -1)
    total = sp.kronecker_product(delta, sp.eye(3))+sp.kronecker_product(sign, delta)
    check(rank_q(total.tolist(), 9) == 4, 'Tensor connecting rank mismatch')
    return {'bockstein': bockstein, 'cycle_smith': cycle_forms,
            'skein': {'chain_inclusion_and_quotient_verified': True,
                      'A_target_cokernel': 'Z/2', 'B_target_cokernel': '0',
                      'connecting_lift_differential': 1},
            'tensor': {'factor_rank': 1, 'signed_tensor_sum_rank': 4}}


def main():
    result = {'status': 'PASS', 'staircases': [staircase(1), staircase(3)],
              'module_lemma': module_enumeration(), 'other_checks': other_checks()}
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
