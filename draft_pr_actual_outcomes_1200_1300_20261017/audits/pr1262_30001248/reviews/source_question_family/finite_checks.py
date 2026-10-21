#!/usr/bin/env python3
"""Fresh finite checks. Standard-library only; asymptotic claims are proved in report.md."""
from collections import Counter, defaultdict
from datetime import datetime, timezone
from fractions import Fraction
from itertools import combinations
from math import comb, cos, exp, fsum, pi, sin, sqrt, ceil
from pathlib import Path
import hashlib
import json


def falling(x, k):
    out = 1
    for j in range(k):
        out *= x - j
    return out


def exact_graph_checks():
    rows = []
    tested = 0
    max_fourier_error = 0.0
    for n in range(3, 7):
        edges = list(combinations(range(n), 2))
        edge_index = {e: i for i, e in enumerate(edges)}
        edge_masks = [1 << i for i in range(len(edges))]
        triangles = [sum(1 << edge_index[e] for e in combinations(v, 2))
                     for v in combinations(range(n), 3)]
        incidents = [sum(1 << i for i, e in enumerate(edges) if v in e)
                     for v in range(n)]
        matching_masks = [(1 << i) | (1 << j)
                          for i, e in enumerate(edges)
                          for j, f in enumerate(edges) if i < j and not set(e) & set(f)]
        hist = Counter()
        whist = Counter()
        mhist = Counter()
        N, C = len(edges), comb(n, 3)
        for graph in range(1 << N):
            m = graph.bit_count()
            t = sum(graph & z == z for z in triangles)
            w = sum(comb((graph & z).bit_count(), 2) for z in incidents)
            x = sum(graph & z == z for z in matching_masks)
            assert x == comb(m, 2) - w
            hist[t, m] += 1
            whist[w, m] += 1
            mhist[x, m] += 1
        assert sum(hist.values()) == 1 << N
        assert any(t == 1 for t, m in hist)
        tested += 1 << N
        for a, b in [(1, 3), (1, 2), (2, 3)]:
            p = Fraction(a, b)
            den = b ** N
            weights = [a ** m * (b - a) ** (N - m) for m in range(N + 1)]
            dist = Counter()
            matchdist = Counter()
            for (t, m), count in hist.items():
                dist[t] += count * weights[m]
            for (x, m), count in mhist.items():
                matchdist[x] += count * weights[m]
            assert sum(dist.values()) == den
            mu = Fraction(sum(t * w for t, w in dist.items()), den)
            var = Fraction(sum(t * t * w for t, w in dist.items()), den) - mu * mu
            formula = C * p ** 3 * (1 - p ** 3) + 12 * comb(n, 4) * p ** 5 * (1 - p)
            projection = N * (n - 2) ** 2 * p ** 5 * (1 - p)
            remainder = 3 * C * p ** 4 * (1 - p) ** 2 + C * p ** 3 * (1 - p) ** 3
            assert mu == C * p ** 3
            assert var == formula == projection + remainder
            sample_moduli = []
            for q in range(1, C + 4):
                residues = [0] * q
                for t, w in dist.items():
                    residues[t % q] += w
                D = max(Fraction(abs(q * w - den), den) for w in residues)
                if q >= 2:
                    cf = complex(fsum(w / den * cos(2 * pi * t / q) for t, w in dist.items()),
                                 fsum(w / den * sin(2 * pi * t / q) for t, w in dist.items()))
                    assert abs(cf) <= float(D) + 1e-12
                # Independent finite Fourier inversion of every residue.
                for residue, w in enumerate(residues):
                    inv = 0j
                    for k in range(q):
                        cf = sum((weight / den) * complex(cos(2 * pi * k * t / q),
                                                         sin(2 * pi * k * t / q))
                                 for t, weight in dist.items())
                        angle = -2 * pi * k * residue / q
                        inv += cf * complex(cos(angle), sin(angle)) / q
                    error = abs(inv - w / den)
                    max_fourier_error = max(max_fourier_error, error)
                    assert error < 1e-12
                if q in {1, 2, 3, C + 3}:
                    sample_moduli.append({'q': q, 'D_exact': str(D), 'D_decimal': float(D)})
            cmu = Fraction(sum(x * w for x, w in matchdist.items()), den)
            cvar = Fraction(sum(x * x * w for x, w in matchdist.items()), den) - cmu * cmu
            Ddisjoint = comb(n - 2, 2)
            assert cmu == 3 * comb(n, 4) * p * p
            assert cvar == N * Ddisjoint ** 2 * p ** 3 * (1 - p) + 3 * comb(n, 4) * p ** 2 * (1 - p) ** 2
            conditional = None
            if n >= 4:
                m0 = (a * N) // b
                total = comb(N, m0)
                ew = Fraction(sum(w * count for (w, m), count in whist.items() if m == m0), total)
                ew2 = Fraction(sum(w * w * count for (w, m), count in whist.items() if m == m0), total)
                s, d = 3 * C, 2 * (n - 2)
                A = N * comb(d, 2)
                B = comb(s, 2) - A
                r = {j: Fraction(falling(m0, j), falling(N, j)) for j in [2, 3, 4]}
                varw = ew2 - ew * ew
                assert ew == s * r[2]
                assert varw == s * r[2] + 2 * A * r[3] + 2 * B * r[4] - s ** 2 * r[2] ** 2
                assert 2 * A - Fraction(4 * s ** 2, N) == -2 * s
                conditional = {'m': m0, 'mean_W_exact': str(ew), 'variance_W_exact': str(varw)}
            rows.append({'n': n, 'p': str(p), 'graphs': 1 << N, 'mean_T_exact': str(mu),
                         'variance_T_exact': str(var), 'projection_variance_exact': str(projection),
                         'remainder_variance_exact': str(remainder), 'matching_variance_exact': str(cvar),
                         'moduli_checked': list(range(1, C + 4)), 'sample_discrepancies': sample_moduli,
                         'conditional_wedge_check': conditional})
    return {'graphs_enumerated_once_per_n': tested, 'parameter_cases': len(rows),
            'maximum_DFT_inversion_absolute_error': max_fourier_error, 'cases': rows}


def poisson_checks():
    rows = []
    for h in [0.125, 0.5, 1.0, 2.0, 4.0, 10.0, 50.0]:
        for theta in [0.0, 0.1, 0.49]:
            radius = ceil(14 / h) + 3
            direct = h * fsum(exp(-0.5 * (h * (j + theta)) ** 2) / sqrt(2 * pi)
                              for j in range(-radius, radius + 1))
            mradius = ceil(14 * h / (2 * pi)) + 5
            dual = 1 + 2 * fsum(exp(-2 * pi * pi * m * m / (h * h)) * cos(2 * pi * m * theta)
                                for m in range(1, mradius + 1))
            error = abs(direct - dual)
            assert error < 1e-12
            rows.append({'h': h, 'theta': theta, 'direct_folded_gaussian': direct,
                         'poisson_dual': dual, 'absolute_error': error})
    return {'truncation': 'Direct: |j| <= ceil(14/h)+3; dual: m <= ceil(14h/(2pi))+5; numerical evidence only.',
            'cases': rows}


def main():
    result = {'run_started_utc': datetime.now(timezone.utc).isoformat(),
              'status': 'all assertions passed', 'scope': 'Finite exact arithmetic plus floating-point identities; not a proof of an asymptotic LLT.',
              'exact_enumeration': exact_graph_checks(), 'poisson_identity': poisson_checks()}
    result['run_completed_utc'] = datetime.now(timezone.utc).isoformat()
    result['script_sha256'] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    destination = Path(__file__).with_name('finite_checks.json')
    destination.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    print(json.dumps({'status': result['status'], 'graphs': result['exact_enumeration']['graphs_enumerated_once_per_n'],
                      'parameter_cases': result['exact_enumeration']['parameter_cases'],
                      'max_DFT_error': result['exact_enumeration']['maximum_DFT_inversion_absolute_error'],
                      'output': str(destination)}, indent=2))


if __name__ == '__main__':
    main()
