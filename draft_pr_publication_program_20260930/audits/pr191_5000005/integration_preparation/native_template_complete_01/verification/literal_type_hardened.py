# Explicit if/raise hardening of the preserved independent supplementary checker.
# Original source and ordinary baseline remain under reviews/literal_type_source_adversary/.
"""Independent exact adversarial checks; stdlib only, no author checker imported.

All angles in source_branch_labels are normalized by pi/n, not radians.
The rational-pair enumeration tests definition algebra, not realizability of
every pair as a billiard. The model enumeration uses actual polygon chords.
Universal geometric assertions are proved separately in the audit report.
"""
from fractions import Fraction as F
from math import gcd
import hashlib
import json
from pathlib import Path

def source_branch_labels(n, a, b, parity=None, allow_endpoint_representative=True):
    """Transcribe printed four triples; optionally use physical segment parity."""
    N = n - 2
    labels = set()
    representatives = range(N + int(allow_endpoint_representative))
    for k in representatives:
        if n % 2 == 0:
            m = n // 2
            tests = ((k <= m - 1, a <= 2 * (m - k - 1), b - a == 2 * (k + 1), 0), (k <= m - 1, a >= 2 * (m - k - 1), b + a == 2 * (n - k - 1), 1), (k >= m - 1, a >= 2 * (n - k - 2), b - a == 2 * (k + 3 - n), 0), (k >= m - 1, a <= 2 * (n - k - 2), b + a == 2 * (n - k - 1), 1))
        else:
            m = (n - 1) // 2
            tests = ((k <= m + 1, a <= n - 2 * (k + 1), b - a == 2 * (k + 1), 0), (k <= m - 1, a >= n - 2 * (k + 1), b + a == 2 * (n - k - 1), 1), (k >= m, a >= 2 * (n - k - 2), b - a == 2 * (k + 3 - n), 0), (k >= m, a <= 2 * (n - k - 2), b + a == 2 * (n - k - 1), 1))
        if any((x and y and z and (parity is None or p == parity) for x, y, z, p in tests)):
            labels.add(k % N)
    return labels

def check_type_algebra():
    count = 0
    raw_ambiguous = 0
    endpoint_rep_needed = []
    for n in range(3, 41):
        N = n - 2
        for parity in (0, 1):
            smin, smax = (-(n // 2), n // 2 + 1) if parity == 0 else (1, n - 1)
            for s in range(smin, smax + 1):
                for numerator in range(4 * N + 1):
                    a = F(numerator, 4)
                    b = 2 * s + a if parity == 0 else 2 * s - a
                    if not 2 <= b <= n:
                        continue
                    k = (s - 1 if parity == 0 else n - 1 - s) % N
                    if not source_branch_labels(n, a, b, parity) == {k}:
                        raise AssertionError((n, a, b, parity, k))
                    raw = source_branch_labels(n, a, b)
                    raw_ambiguous += len(raw) > 1
                    if not source_branch_labels(n, a, b, parity, False):
                        endpoint_rep_needed.append((n, str(a), str(b), parity, k))
                    count += 1
    if not endpoint_rep_needed == [(n, '0', '2', 1, 0) for n in range(3, 41)]:
        raise AssertionError()
    if not source_branch_labels(4, F(1), F(3)) == {0, 1}:
        raise AssertionError()
    if not source_branch_labels(5, F(2), F(4)) == {0, 1}:
        raise AssertionError()
    if not source_branch_labels(5, F(2), F(4), 1) == {1}:
        raise AssertionError()
    if not 2 not in source_branch_labels(5, F(2), F(4)):
        raise AssertionError()
    return {'rational_angle_pairs': count, 'raw_ambiguous_pair_rows': raw_ambiguous, 'only_missing_representative_case': 'all n: alpha=0, beta=2pi/n, odd segment parity, requires k=n-2 identified with 0', 'n_range': [3, 40], 'alpha_mesh_in_pi_over_n': '1/4'}

def check_model_chords():
    count = 0
    for n in range(3, 61):
        N = n - 2
        for polygon in (0, 1):
            for j in range(n):
                t = j if n % 2 == 0 or j % 2 == polygon else j + n
                for q in range(1, n):
                    jp = (j + q) % n
                    tp = jp if n % 2 == 0 or jp % 2 == polygon else jp + n
                    h = polygon * n - 2 * j + n - 1 - q
                    u = t * N + n - 1 - q
                    v = tp * N + q - 1
                    if not ((u - h) % n == 0 and (v - h) % n == 0):
                        raise AssertionError()
                    a, b = ((u - h) // n, (v - h) // n)
                    if not (a + b + h) % N == 0:
                        raise AssertionError((n, polygon, j, q, a, b, h))
                    if not (b - a - (q - 1)) % N == 0:
                        raise AssertionError()
                    count += 1
    return {'actual_oriented_polygon_chords': count, 'n_range': [3, 60], 'identities': ['a+b=-h modulo n-2', 'b-a=q-1 modulo n-2'], 'side_germs_included': True}

def check_literal_diagonal_rule():
    count = 0
    self_stabilizers = 0
    for n in range(3, 201):
        N = n - 2
        for a in range(N + 1):
            k = -a % N
            for ap in range(N + 1):
                kp = -ap % N
                for eps in (-1, 1):
                    ell = ap - eps * a
                    if n % 2 == 0 and ell % 2:
                        continue
                    if not (eps * k - ell) % N == kp:
                        raise AssertionError()
                    count += 1
                    self_stabilizers += a == ap and eps == -1
    return {'admissible_literal_angle_transformations': count, 'n_range': [3, 200], 'reflection_self_stabilizers': self_stabilizers, 'angle_reduction_used': False}

def refute_unqualified_A0_target():
    for n in range(5, 201):
        N = n - 2
        raw = source_branch_labels(n, F(1), F(3))
        if not raw == {0, N - 1}:
            raise AssertionError((n, raw))
        ell, eps = (2, -1)
        if not ell + eps * 1 == 1:
            raise AssertionError()
        demanded = (eps * 0 - ell) % N
        if not (demanded != 0 and demanded not in raw):
            raise AssertionError()
        intended = N - 1
        if not (eps * intended - ell) % N == intended:
            raise AssertionError()
        shift = 1 if n % 2 else 2
        ap = 1 + shift
        bp = 3 + shift
        if not (0 < ap < N and 2 < bp < n):
            raise AssertionError()
        target_raw = source_branch_labels(n, F(ap), F(bp))
        if not target_raw == {0, N - 1 - shift}:
            raise AssertionError()
        if not -shift % N not in target_raw:
            raise AssertionError()
    return {'literal_upstream_target': 'REFUTED', 'analytic_family': 'every n>=5: direct chord X0 X_(n-2), alpha=pi/n, beta=3pi/n, ell=2, epsilon=-1', 'finite_specializations_checked': [5, 200], 'bare_shorthand_label': 0, 'demanded_label': '-2 mod (n-2)', 'raw_definition_labels': '0 and n-3', 'parity_selected_label': 'n-3', 'distinct_interior_chord_variant': 'epsilon=+1, ell=1 for odd n, ell=2 for even n; target alpha=(1+ell)pi/n, beta=(3+ell)pi/n', 'side_or_intermediate_vertex_hit_degeneracy': False, 'exceptional_symmetry_ray': True, 'preceding_open_fundamental_sector': 'outside for odd n; endpoint for even n; does not refute that restricted conjecture'}

def hex_type(p, q):
    s = (p + q) % 3
    if s == 1:
        return 0
    if s == 2:
        return 2
    if not (p % 3, q % 3) in ((1, 2), (2, 1)):
        raise AssertionError()
    return 1 if p % 3 == 1 else 3

def check_elementary():
    count = 0
    for p in range(-80, 81):
        for q in range(-80, 81):
            if gcd(p, q) != 1:
                continue
            k = hex_type(p, q)
            if not hex_type(p - q, p) == (k - 2) % 4:
                raise AssertionError()
            if not hex_type(q, p) == -k % 4:
                raise AssertionError()
            first = next((r for r in range(1, 4) if (r * p + r * q) % 3 != 2))
            if not first == (2 if (p + q) % 3 == 2 else 1):
                raise AssertionError()
            count += 1
    return {'primitive_hexagon_directions': count, 'coordinate_box': [-80, 80], 'identities': ['rotation K(p-q,p)=K(p,q)-2 mod 4', 'bisector K(q,p)=-K(p,q) mod 4', 'first honeycomb vertex multiplier is 1 or 2']}
if __name__ == '__main__':
    result = {'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(), 'type_algebra': check_type_algebra(), 'model_chords': check_model_chords(), 'literal_direct_diagonals': check_literal_diagonal_rule(), 'literal_target_obstruction': refute_unqualified_A0_target(), 'elementary_hexagon': check_elementary(), 'result': 'All audit assertions passed; unqualified upstream target REFUTED; parity-selected formulas passed these finite checks', 'limitations': 'Finite exact checks supplement the analytic proof audit; they do not verify Veech reduction or prove the all-n all-trajectory theorem.'}
    print(json.dumps(result, indent=2, sort_keys=True))
