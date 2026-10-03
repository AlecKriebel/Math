#!/usr/bin/env python3
"""Exact diagnostics and falsifiers; never a Brownian-law proof certificate."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import argparse
import json
import math
import re


def pw(nodes, t):
    for (a, x), (b, y) in zip(nodes, nodes[1:]):
        if a <= t <= b:
            return x + (t-a)*(y-x)/(b-a)
    if t == nodes[-1][0]:
        return nodes[-1][1]
    raise ValueError(t)


def finite_diagnostics():
    cases = points = cut_checks = 0
    patterns = [(F(0), F(1, 10), F(1, 3), F(0), F(2, 5)),
                (F(1, 4), F(0), F(3, 4)), (F(0), F(0), F(1))]
    shapes = [(F(0), F(-2), F(3), F(1)),
              (F(0), F(3), F(-2), F(-1)),
              (F(0), F(0), F(0), F(0))]
    for durations in patterns:
        positive = sum(T > 0 for T in durations)
        for choice in product(shapes, repeat=positive):
            nodes = [(F(0), F(0))]
            chunks = []
            a = z = F(0)
            j = 0
            for T in durations:
                if T == 0:
                    chunks.append((a, T, z, (F(0),)*4))
                    continue
                values = choice[j]
                j += 1
                chunks.append((a, T, z, values))
                for k in range(1, 4):
                    nodes.append((a+T*F(k, 3), z+values[k]))
                a += T
                z += values[-1]
            times = sorted({a+T*F(k, 6) for a, T, z, v in chunks for k in range(7)})
            def direct(t):
                for a, T, z, v in chunks:
                    if T > 0 and a <= t <= a+T:
                        # Direct internal reversal, independent of W formula.
                        local = [(T*F(k, 3), v[k]) for k in range(4)]
                        return z+v[-1]-pw(local, T-(t-a))
                if t == 0:
                    return F(0)
                raise ValueError(t)
            for a, T, z, v in chunks:
                for k in range(7):
                    u = T*F(k, 6)
                    assert direct(a+u) == pw(nodes, a)+pw(nodes, a+T)-pw(nodes, a+T-u)
                    points += 1
            for H in times:
                observed = [t for t in times if t <= H]
                comparison = [t for t in times if t <= min(nodes[-1][0], H+1)]
                omega = max(abs(pw(nodes, t)-pw(nodes, u))
                            for t in comparison for u in comparison if abs(t-u) <= 1)
                error = max(abs(direct(t)-pw(nodes, t)) for t in observed)
                assert error <= 2*omega
                cut_checks += 1
            cases += 1
    return {'finite_continuous_path_configurations': cases,
            'rational_rotation_equalities': points, 'cut_horizon_checks': cut_checks}


def boundary_witness():
    # Single deterministic-duration stopped Brownian path can be close to this
    # continuous shape. The exact curve alone is an algebraic falsifier.
    T = F(1)
    H = F(1, 4)
    nodes = [(F(0), F(0)), (H, F(0)), (F(3, 4), F(8)), (T, F(0))]
    delta = pw(nodes, T)-pw(nodes, T-H)-(pw(nodes, H)-pw(nodes, F(0)))
    omega_past = F(0)
    assert abs(delta) > 2*omega_past
    return {'T': str(T), 'H': str(H), 'error_at_H': str(abs(delta)),
            'past_only_modulus': str(omega_past), 'c': '2',
            'nodes': [[str(t), str(x)] for t, x in nodes]}


def limiting_witnesses():
    # After 2N alternating zero / 1/(2N) pieces only time 1/2 has passed.
    # Subsequent durations 1/2 ensure divergence. Stopping times deterministic.
    N = 100000
    assert N*F(1, 2*N) == F(1, 2)
    piece_count = 2*N+1
    deterministic_cover_count = 4
    assert piece_count > deterministic_cover_count
    # Repeating the same unit BM path makes W(2)=2B(1), variance 4 != 2.
    dependent_variance, correct_variance = F(4), F(2)
    assert dependent_variance != correct_variance
    # Durations 2^{-j} have finite total; exact geometric limit is 1.
    summable_total = F(1, 2)/(1-F(1, 2))
    assert summable_total == 1
    # Durations T_j=2^j, u=T_j/4: disjoint increments give Var(D_j)=T_j/2.
    # Error events |D_j|>=sqrt(T_j/2) are independent with a fixed positive
    # Gaussian probability, hence infinitely frequent by second Borel-Cantelli.
    unbounded = []
    for j in (4, 8, 16, 32):
        T = 2**j
        a = T-2
        u = F(T, 4)
        R = a+u
        variance = 2*u
        assert variance == F(T, 2)
        unbounded.append({'j': j, 'T': str(T), 'R': str(R), 'error_variance': str(variance)})
    # Brownian scaling: covariance of B(r)/sqrt(r), B(2r)/sqrt(2r) is 1/sqrt(2).
    # Algebraic nonzero positive variance 2-sqrt(2) certified by 1<sqrt(2)<2.
    assert 1**2 < 2 < 2**2
    return {'tiny_zero_piece_count': piece_count,
            'physical_time_after_2N_pieces': '1/2', 'deterministic_windows': deterministic_cover_count,
            'dependent_reuse_variance': str(dependent_variance), 'Brownian_variance_at_2': str(correct_variance),
            'nondivergent_duration_sum': str(summable_total),
            'unbounded_duration_Gaussian_witnesses': unbounded,
            'scaled_Brownian_non_Cauchy_difference_variance': '2-sqrt(2)>0',
            'translated_uniform_bound_witness': 'T=1/2, u=T/4; iid D_j~N(0,1/4) have unbounded absolute maximum almost surely'}


def check_prose(path):
    """Guard only explicitly recognized proof clauses; not general prose parsing."""
    doc = path.read_text()
    # These guards tie specific mutations to exact falsifying mathematics.
    if 'common deterministic finite bound' not in doc:
        limiting_witnesses()
        raise AssertionError('MISSING_UNIFORM_BOUND: T_j=2^j defeats the logarithmic error rate')
    if 'are independent but need not be identically distributed' not in doc:
        limiting_witnesses()
        raise AssertionError('MISSING_INDEPENDENCE: reused unit path has variance 4 at time 2')
    if 'sums of durations diverge in both directions' not in doc:
        limiting_witnesses()
        raise AssertionError('MISSING_DIVERGENCE: durations 2^{-j} do not cover the half-line')
    if '2\\,\\omega_W(c;R_0+c)' not in doc:
        boundary_witness()
        raise AssertionError('MISSING_BOUNDARY_ENLARGEMENT: error 8 but past-only modulus 0')
    if '[W(a+T)-W(a+T-u)]-[W(a+u)-W(a)]' not in doc:
        # Concrete distinct endpoint values certify a wrong plus sign.
        a, b, d, e = map(F, (1, 3, 7, 2))
        rotation = a+d-e-b
        wrong = (d-e)+(b-a)
        assert rotation != wrong
        raise AssertionError('WRONG_ROTATION_SIGN: endpoint values (1,3,7,2) falsify the plus variant')
    match = re.search(r'Take \\(r=(\d+)\\sqrt\{cm\}\\\)', doc)
    assert match, 'UNRECOGNIZED_TAIL_THRESHOLD_CLAUSE'
    multiplier = int(match.group(1))
    rate = F(multiplier*multiplier, 16)
    if rate <= F(1, 2):
        # e^x <= 1/(1-x) for 0<=x<1; at x=1/16 this is 16/15<2.
        # Therefore the 2^m exp(-m/16) union majorant grows instead of summing.
        assert F(1)/(1-rate) < 2
        raise AssertionError('NONSUMMABLE_TAIL_MAJORANT: threshold too small for displayed union bound')
    assert multiplier == 8 and '-r^2/(16c)' in doc, 'UNRECOGNIZED_TAIL_CONSTANTS'
    lower = sum(F(4)**j/math.factorial(j) for j in range(4))
    assert lower == F(71, 3) > 16
    assert 8*F(1, 8)/(1-F(1, 8)) == F(8, 7)
    if '\\Longrightarrow' not in doc or 'almost-sure Brownian scaling limit' in doc:
        limiting_witnesses()
        raise AssertionError('INVALID_AS_SCALING_UPGRADE: Gaussian difference variance 2-sqrt(2)>0')
    if 'uniformly over every translated observation window' in doc:
        limiting_witnesses()
        raise AssertionError('INVALID_ALL_ORIGINS_UPGRADE: iid nondegenerate interior errors are unbounded')
    return {'recognized_clauses': 'exact assumptions, boundary term, rotation sign, tail multiplier, weak scaling',
            'tail_rate': str(rate), 'exp4_lower_bound': str(lower), 'geometric_sum_majorant': '8/7',
            'scope': 'Specific clause guards plus exact witnesses; does not certify arbitrary prose or probability arguments'}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--candidate', type=Path)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    result = {'finite_diagnostics': finite_diagnostics(),
              'boundary_witness': boundary_witness(), 'limiting_controls': limiting_witnesses()}
    if args.candidate:
        result['prose_checks'] = check_prose(args.candidate)
    result['scope'] = 'Exact finite diagnostics and mathematical falsifiers, not simulation, Brownian proof, or exact random-shift solution'
    raw = json.dumps(result, indent=2)+'\n'
    args.out.write_text(raw)
    print(raw, end='')


if __name__ == '__main__':
    main()
