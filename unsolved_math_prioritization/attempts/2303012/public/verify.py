#!/usr/bin/env python3
"""Exact consistency checks; not a formal proof of the analytic theorem."""
from fractions import Fraction as F
from pathlib import Path
import argparse
import hashlib
import json

ROOT = Path(__file__).resolve().parent


def mul(a, b):
    """Multiply q*pi^(e/2), represented exactly by (q,e)."""
    return a[0] * b[0], a[1] + b[1]


def inv(a):
    return 1 / a[0], -a[1]


def gamma_half(k):
    """Gamma(k/2) for positive integer k, in q*pi^(e/2) form."""
    assert k >= 1
    if k == 1:
        return F(1), 1
    if k == 2:
        return F(1), 0
    return mul((F(k - 2, 2), 0), gamma_half(k - 2))


def sin_integral(k):
    """Integral_0^(pi/2) sin(theta)^k dtheta via its exact recurrence."""
    assert k >= 0
    if k == 0:
        return F(1, 2), 2
    if k == 1:
        return F(1), 0
    return mul((F(k - 1, k), 0), sin_integral(k - 2))


def run(source_dir=None):
    status = json.loads((ROOT / 'STATUS.json').read_text())
    sources = json.loads((ROOT / 'SOURCE_MANIFEST.json').read_text())['sources']
    assert status['problem_id'] == 2303012
    assert status['problem_number'] == 'AMR-022-3012'
    assert status['rank'] == 569
    assert status['status'] == 'already_solved'
    assert status['turns_used'] == 1 and status['turns_budget'] == 5
    assert status['novelty_claim'] is False
    assert status['remaining_mathematical_gap'] is None
    assert status['source_locator'] == 'Corollary 3, printed p. 67 / PDF p. 15'
    b = next(s for s in sources if s['id'] == 'benedicks_1980')
    assert b['url'] == 'https://doi.org/10.1007/BF02384681'
    assert b['bytes'] == 682635
    assert b['sha256'] == 'a24b38583e76fbb3e14178608099e73dc2b0883e9f070a66032456320ee26811'
    assert 53 + 15 - 1 == 67
    assert 64 + 1 == 65  # arXiv collection's cover-page offset

    # Radial integration followed by r=y*tan(theta) reduces the Poisson
    # kernel mass to kappa_n * area(S^(n-1)) * integral sin^(n-1).
    # The recurrence identities are mathematical inputs, not proved by code.
    dims = list(range(1, 51))
    for n in dims:
        kappa = mul(gamma_half(n + 1), (F(1), -(n + 1)))
        area = mul((F(2), n), inv(gamma_half(n)))
        mass = mul(mul(kappa, area), sin_integral(n - 1))
        assert mass == (F(1), 0), (n, mass)

    # Check the elementary finite-radius cancellation against exact
    # rational fixtures. This does not establish Lemma 8's estimate.
    cases = 0
    for a in map(F, [0, 1, 3, 100]):
        for h in [F(1, 5), F(1), F(9, 2)]:
            for eta in [F(1, 16), F(1, 3), F(1)]:
                for A in [F(1, 7), F(1), F(17)]:
                    C = F(11, 3)
                    L = 1 + a + h
                    outer = A * (1 + a + L)
                    escape_bound = C * h / (eta**3 * L)
                    assert outer * escape_bound <= 2 * A * C * h / eta**3
                    assert 0 < eta <= 1 and L > h
                    cases += 1

    # Bounded-remainder uniqueness: for nonzero d, y=(B+1)/|d|
    # contradicts |d|y<=B. These are fixtures, not the quantified proof.
    uniqueness = 0
    for d in [F(-7), F(-1, 3), F(1, 19), F(9)]:
        for B in [F(0), F(1, 5), F(100)]:
            y = (B + 1) / abs(d)
            assert abs(d) * y > B
            uniqueness += 1

    hashes = []
    if source_dir is not None:
        for s in sources:
            if 'sha256' not in s:
                continue
            raw = (source_dir / s['local_input_filename']).read_bytes()
            assert len(raw) == s['bytes']
            assert hashlib.sha256(raw).hexdigest() == s['sha256']
            hashes.append(s['id'])
    return {
        'passed': True,
        'problem_id': 2303012,
        'status_consistency': True,
        'poisson_normalization_dimensions': [1, 50],
        'poisson_normalization_exact_checks': len(dims),
        'finite_radius_rational_fixtures': cases,
        'coefficient_uniqueness_rational_fixtures': uniqueness,
        'source_hashes_checked': hashes,
        'limitations': [
            'No formal verification of Benedicks Corollary 3 or Lemmas 2, 3, 8.',
            'No machine proof of Green-function regularity or harmonic measure.',
            'Finite fixtures are consistency tests and are not universal proofs.',
            'Source hashing authenticates inspected bytes, not theorem correctness.',
            'The unbounded-dimensional assertion rests on the published theorem, not this finite dimension sweep.'
        ]
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--source-dir', type=Path)
    args = parser.parse_args()
    print(json.dumps(run(args.source_dir), indent=2))
