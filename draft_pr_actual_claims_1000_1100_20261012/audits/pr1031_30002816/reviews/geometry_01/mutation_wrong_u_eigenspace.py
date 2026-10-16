#!/usr/bin/env python3
"""Independent Gaussian-integer polynomial/exterior check. Standard library only.

This script constructs every map coefficient from the 12 real coordinates.
Unlike finite projector sampling, its projector test compares all coefficients
of the universal polynomial in 24 real indeterminates. Its geometric claims
remain justified by INDEPENDENT_DERIVATION.md, not by sampled planes.
Reads pinned submitted inputs; writes only to this script's review directory.
"""
from fractions import Fraction
from itertools import combinations
from pathlib import Path
import hashlib
import json
import sys

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parent.parent
ZERO = (0, 0)
ONE = (1, 0)
I = (0, 1)
PAIRS = list(combinations(range(6), 2))
REAL_FOURS = list(combinations(range(12), 4))


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def gadd(x, y):
    return (x[0] + y[0], x[1] + y[1])


def gmul(x, y):
    return (x[0] * y[0] - x[1] * y[1], x[0] * y[1] + x[1] * y[0])


def gconj(x):
    return (x[0], -x[1])


def add_to(d, key, value, add=gadd, zero=ZERO):
    value = add(d.get(key, zero), value)
    if value == zero:
        d.pop(key, None)
    else:
        d[key] = value


def join_indices(a, b):
    if set(a).intersection(b):
        return None, 0
    inversions = sum(x > y for x in a for y in b)
    return tuple(sorted(a + b)), -1 if inversions % 2 else 1


def wedge_gaussian(a, b):
    result = {}
    for ka, va in a.items():
        for kb, vb in b.items():
            key, sign = join_indices(ka, kb)
            if sign:
                add_to(result, key, gmul((sign, 0), gmul(va, vb)))
    return result


def pvar(j):
    return {(j,): ONE}


def padd(a, b):
    result = dict(a)
    for key, value in b.items():
        add_to(result, key, value)
    return result


def pscale(a, scalar):
    return {key: value for key, old in a.items()
            if (value := gmul(old, scalar)) != ZERO}


def pmul(a, b):
    result = {}
    for ka, va in a.items():
        for kb, vb in b.items():
            add_to(result, tuple(sorted(ka + kb)), gmul(va, vb))
    return result


def pconj(a):
    return {key: gconj(value) for key, value in a.items()}


def wedge_poly(a, b):
    result = {}
    for ka, va in a.items():
        for kb, vb in b.items():
            key, sign = join_indices(ka, kb)
            if sign:
                value = pscale(pmul(va, vb), (sign, 0))
                result[key] = padd(result.get(key, {}), value)
                if not result[key]:
                    result.pop(key)
    return result


def poly_exterior_scale(a, scalar):
    return {k: pscale(v, scalar) for k, v in a.items()}


def wedge_real(a, b):
    """A second, rational scalar exterior path for concrete hostile controls."""
    result = {}
    for ka, va in a.items():
        for kb, vb in b.items():
            key, sign = join_indices(ka, kb)
            if sign:
                result[key] = result.get(key, Fraction(0)) + sign * va * vb
                if result[key] == 0:
                    result.pop(key)
    return result


def real_frame_wedge(vectors):
    result = {(): Fraction(1)}
    for v in vectors:
        result = wedge_real(result, {(j,): Fraction(x) for j, x in v.items()})
    return result


def J_real(v):
    return {j + 1 if j % 2 == 0 else j - 1: x if j % 2 == 0 else -x
            for j, x in v.items()}


def norm2_real(p):
    return sum(x * x for x in p.values())


def phi_real(p):
    return sum(p.get((2 * i, 2 * i + 1, 2 * j, 2 * j + 1), 0)
               for i, j in PAIRS)


def q_real(p):
    return sum(p.get((2 * i, 2 * i + 1, 2 * j, 2 * j + 1), 0)
               for i, j in PAIRS if (j < 3 or i >= 3))


def exact_rank(columns):
    pivots = {}
    for column in columns:
        v = dict(column)
        while v:
            row = min(v)
            if row not in pivots:
                scale = v[row]
                pivots[row] = {r: x / scale for r, x in v.items()}
                break
            scale = v[row]
            for r, x in pivots[row].items():
                v[r] = v.get(r, Fraction(0)) - scale * x
                if v[r] == 0:
                    v.pop(r)
    return len(pivots), sorted(pivots)


def build_kernels():
    w = [{(2 * j,): ONE, (2 * j + 1,): (0, 1)} for j in range(6)]
    wb = [{key: gconj(value) for key, value in v.items()} for v in w]
    w2 = [wedge_gaussian(w[i], w[j]) for i, j in PAIRS]
    wb2 = [wedge_gaussian(wb[i], wb[j]) for i, j in PAIRS]
    return [[wedge_gaussian(w2[i], wb2[j]) for j in range(15)] for i in range(15)]


def embed_numerator(kernels, matrix):
    result = {}
    for (i, j), scalar in matrix.items():
        for key, value in kernels[i][j].items():
            add_to(result, key, gmul(scalar, value))
    return result


def embed_poly_numerator(kernels, z, transpose=False):
    result = {}
    for i in range(15):
        for j in range(15):
            h = pmul(pconj(z[i]), z[j]) if transpose else pmul(z[i], pconj(z[j]))
            for key, value in kernels[i][j].items():
                result[key] = padd(result.get(key, {}), pscale(h, value))
                if not result[key]:
                    result.pop(key)
    return result


def verify_inputs():
    pinfile = AUDIT / 'SUBMITTED_PINS.json'
    pins = json.loads(pinfile.read_text())
    checks = []
    for item in pins['files']:
        data = (AUDIT / 'submitted' / item['relative']).read_bytes()
        checks.append({'relative': item['relative'],
                       'sha256': hashlib.sha256(data).hexdigest(),
                       'bytes': len(data),
                       'pass': hashlib.sha256(data).hexdigest() == item['sha256']
                               and len(data) == item['bytes']})
    require(len(checks) == 29 and all(x['pass'] for x in checks), 'input pins fail')
    return {'head_commit': pins['head_commit'],
            'pinfile_sha256': hashlib.sha256(pinfile.read_bytes()).hexdigest(),
            'all_29_match': True,
            'proof_sha256': hashlib.sha256((AUDIT / 'submitted/current/PROOF.md').read_bytes()).hexdigest()}


def main():
    inputs = verify_inputs()
    kernels = build_kernels()
    bases = []
    for i in range(15):
        bases.append((f'diagonal({i})', {(i, i): ONE}, 1, int(PAIRS[i][1] < 3 or PAIRS[i][0] >= 3)))
    for i in range(15):
        for j in range(i + 1, 15):
            bases.append((f'real({i},{j})', {(i, j): ONE, (j, i): ONE}, 0, 0))
            bases.append((f'imaginary({i},{j})', {(i, j): I, (j, i): (0, -1)}, 0, 0))
    columns = []
    column_data = []
    coefficient_denominators = set()
    for name, h, trace, dtrace in bases:
        raw = embed_numerator(kernels, h)
        require(all(c[1] == 0 for c in raw.values()), ('nonreal Hermitian output', name))
        col = {key: Fraction(value[0], 4) for key, value in raw.items() if value[0]}
        require(phi_real(col) == trace, ('wrong Phi', name))
        require(q_real(col) == dtrace, ('wrong Q', name))
        coefficient_denominators.update(x.denominator for x in col.values())
        columns.append(col)
        column_data.append({'hermitian_basis': name,
                            'coordinates': [{'real_indices': list(k), 'coefficient': str(v)}
                                            for k, v in sorted(col.items())]})
    rank, pivot_indices = exact_rank(columns)
    require(rank == 225 and len(bases) == 225, 'rank mismatch')
    # The adjoint formula gives an explicit linear inverse on the full ambient.
    gram_diagonal = [1] * 15 + [2] * 210
    gram_checks = 0
    for i, col in enumerate(columns):
        for j in range(i, 225):
            inner = sum(x * columns[j].get(key, Fraction(0)) for key, x in col.items())
            require(inner == (gram_diagonal[i] if i == j else 0), ('Gram mismatch', i, j))
            gram_checks += 1

    # Universal a,b with independent real and imaginary parts: 24 variables.
    a = [padd(pvar(2 * j), pscale(pvar(2 * j + 1), I)) for j in range(6)]
    b = [padd(pvar(12 + 2 * j), pscale(pvar(13 + 2 * j), I)) for j in range(6)]
    z = [padd(pmul(a[i], b[j]), pscale(pmul(a[j], b[i]), (-1, 0))) for i, j in PAIRS]
    ar = {(j,): pvar(j) for j in range(12)}
    br = {(j,): pvar(j + 12) for j in range(12)}
    Jar = {(j + 1 if j % 2 == 0 else j - 1,): pscale(pvar(j), (1 if j % 2 == 0 else -1, 0))
           for j in range(12)}
    Jbr = {(j + 1 if j % 2 == 0 else j - 1,): pscale(pvar(j + 12), (1 if j % 2 == 0 else -1, 0))
           for j in range(12)}
    rhs = wedge_poly(wedge_poly(wedge_poly(ar, Jar), br), Jbr)
    lhs_raw = embed_poly_numerator(kernels, z)
    require(lhs_raw == poly_exterior_scale(rhs, (4, 0)), 'universal projector mismatch')
    require(all(c[1] == 0 for p in lhs_raw.values() for c in p.values()), 'nonreal universal projector')
    universal_coefficients = sum(len(v) for v in lhs_raw.values())

    # Universal mixed Pluecker/minor identity in nine commuting indeterminates.
    mixed = {(i, r + 3): pvar(3 * i + r) for i in range(3) for r in range(3)}
    mixed_square = wedge_poly(mixed, mixed)
    expected = {}
    for i, j in combinations(range(3), 2):
        for r, s in combinations(range(3), 2):
            minor = padd(pmul(pvar(3 * i + r), pvar(3 * j + s)),
                         pscale(pmul(pvar(3 * i + s), pvar(3 * j + r)), (-1, 0)))
            expected[(i, j, r + 3, s + 3)] = pscale(minor, (-2, 0))
    require(mixed_square == expected and len(expected) == 9, 'mixed minor identity mismatch')

    controls = {}
    controls['wrong_global_sign_rejected'] = lhs_raw != poly_exterior_scale(rhs, (-4, 0))
    controls['omitted_one_quarter_rejected'] = lhs_raw != rhs
    controls['transposed_projector_rejected'] = embed_poly_numerator(kernels, z, transpose=True) != lhs_raw
    controls['nonhermitian_input_not_silently_real'] = any(c[1] for c in kernels[0][1].values())

    pure = real_frame_wedge([{0: 1}, {1: 1}, {2: 1}, {3: 1}])
    reversed_pure = {key: -value for key, value in pure.items()}
    controls['positive_complex_orientation'] = (phi_real(pure), q_real(pure), norm2_real(pure)) == (1, 1, 1)
    controls['reverse_orientation_excluded'] = phi_real(reversed_pure) == -1
    controls['Q_not_globally_nonnegative'] = q_real(reversed_pure) == -1
    totally_real = real_frame_wedge([{0: 1}, {2: 1}, {4: 1}, {6: 1}])
    controls['totally_real_plane_not_face'] = phi_real(totally_real) == 0 and norm2_real(totally_real) == 1
    partly_complex = real_frame_wedge([{0: 1}, {1: 1}, {2: 1}, {4: 1}])
    controls['one_complex_line_not_face'] = phi_real(partly_complex) == 0 and norm2_real(partly_complex) == 1

    near_cases = []
    for t in [Fraction(1, 2), Fraction(1, 1000)]:
        c = (1 - t*t)/(1 + t*t)
        s = 2*t/(1 + t*t)
        p = real_frame_wedge([{0: 1}, {1: 1}, {2: c, 6: s}, {3: 1}])
        require(norm2_real(p) == 1 and phi_real(p) == c and abs(c) < 1, 'near-face control mismatch')
        near_cases.append({'t': str(t), 'Phi': str(c), 'norm_squared': str(norm2_real(p))})
    controls['near_equality_does_not_count_as_equality'] = len(near_cases) == 2

    av = {0: Fraction(3, 5), 6: Fraction(4, 5)}
    bv = {2: Fraction(3, 5), 8: Fraction(4, 5)}
    p = real_frame_wedge([av, J_real(av), bv, J_real(bv)])
    require(phi_real(p) == 1 and norm2_real(p) == 1 and q_real(p) == Fraction(337, 625), 'positive D-projection control mismatch')
    controls['face_generator_with_positive_D_projection'] = True

    xv = {0: Fraction(3, 5), 3: Fraction(4, 5)}
    yv = {6: Fraction(5, 13), 11: Fraction(12, 13)}
    p = real_frame_wedge([xv, J_real(xv), yv, J_real(yv)])
    controls['nonreal_product_generator_in_section'] = norm2_real(p) == 1 and phi_real(p) == 1 and q_real(p) == 0
    dep = real_frame_wedge([av, J_real(av), av, J_real(av)])
    zero = real_frame_wedge([{}, {}, bv, J_real(bv)])
    controls['dependent_and_zero_factors_give_zero'] = not dep and not zero
    nonorth = real_frame_wedge([{0: 1}, {1: 1}, {0: 1, 2: 1}, {1: 1, 3: 1}])
    controls['nonorthogonal_factors_normalized_by_bivector'] = nonorth == pure

    rank_two = {(0, 3): Fraction(1), (1, 4): Fraction(1)}
    rank_two_square = wedge_real(rank_two, rank_two)
    controls['rank_two_mixed_tensor_rejected'] = rank_two_square == {(0, 1, 3, 4): Fraction(-2)}
    zidx = [PAIRS.index((0, 3)), PAIRS.index((1, 4))]
    entangled_h = {(i, j): (Fraction(1, 2), 0) for i in zidx for j in zidx}
    entangled_raw = embed_numerator(kernels, entangled_h)
    entangled_a = {key: value[0] / 4 for key, value in entangled_raw.items()}
    controls['ambient_two_hyperplanes_alone_allow_entangled_projector'] = phi_real(entangled_a) == 1 and q_real(entangled_a) == 0
    require(all(controls.values()), [k for k, v in controls.items() if not v])

    certificate = {'real_basis_order': ['e1','f1','e2','f2','e3','f3','e4','f4','e5','f5','e6','f6'],
                   'complex_pair_basis': [list(x) for x in PAIRS],
                   'map': 'A(H)=1/4 sum H_IJ (ei-if_i) wedge (ej-if_j) wedge (er+if_r) wedge (es+if_s)',
                   'columns': column_data,
                   'rank': rank,
                   'gram_diagonal': gram_diagonal,
                   'gram_off_diagonal': 0,
                   'inverse_extended_to_real_ambient': 'G^(-1) A^T, expressed in the real Hermitian basis and the ordered real exterior basis',
                   'pivot_exterior_indices': [list(x) for x in pivot_indices]}
    cert_path = HERE / 'COORDINATE_CERTIFICATE.json'
    cert_path.write_text(json.dumps(certificate, indent=2) + '\n')
    verdict = {'verdict': 'PASS_GEOMETRIC_BRIDGE',
               'scope': 'Exact coordinate identities plus independent universal geometric derivation; external obstruction and moment/SOS implication not adjudicated here.',
               'inputs': inputs,
               'hermitian_dimension': 225,
               'ambient_real_dimension': 495,
               'exact_map_rank': rank,
               'python_optimization': sys.flags.optimize,
               'assertions_used_for_checks': False,
               'gram_entry_checks': gram_checks,
               'explicit_ambient_inverse': 'G^(-1) A^T, where G has 15 ones and 210 twos on its diagonal',
               'real_rational_map_denominators': sorted(coefficient_denominators),
               'Phi_and_Q_basis_checks': 225,
               'universal_projector_polynomial': {'real_indeterminates': 24, 'degree': 4,
                                                'ambient_coordinates': 495,
                                                'nonzero_coordinates': len(lhs_raw),
                                                'nonzero_exact_monomial_coefficients': universal_coefficients,
                                                'all_equal': True},
               'universal_mixed_minor_polynomial': {'complex_indeterminates': 9,
                                                  'minors': 9, 'coefficient_multiplier': -2,
                                                  'all_equal': True},
               'adversarial_and_boundary_controls': controls,
               'near_face_exact_values': near_cases,
               'coordinate_certificate_sha256': hashlib.sha256(cert_path.read_bytes()).hexdigest(),
               'remaining_geometry_gap': None,
               'finite_sample_limit': 'Concrete controls support implementation only; universal face and convex hull equalities are proved separately.'}
    (HERE / 'MACHINE_VERDICT.json').write_text(json.dumps(verdict, indent=2) + '\n')
    print(json.dumps(verdict, indent=2))


if __name__ == '__main__':
    main()
