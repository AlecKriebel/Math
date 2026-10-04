#!/usr/bin/env python3
"""Finite algebra/parameter controls, not an analytic proof checker."""
import argparse
from fractions import Fraction as F
import hashlib
import json
import math
from pathlib import Path


def run(source_dir=None):
    counts = {}
    def record(name, n=1):
        counts[name] = counts.get(name, 0) + n
    def require(condition, name):
        if not condition:
            raise AssertionError(name)
        record(name)

    # Exact rational grid: all n=2,...,12; a=1,...,10 in steps of 1/20.
    for n in range(2, 13):
        old = None
        for ai in range(20, 201):
            a = F(ai, 20)
            pc = F(n, 1) / (n + a - 2)
            ph = F(1, 1) / (a - 1) if a > 1 else None
            bound = pc if ph is None else min(pc, ph)
            require(bound > 0, 'positive_threshold')
            expected = pc if a <= 2 else ph
            require(bound == expected, 'branch_identity')
            if old is not None:
                require(bound <= old, 'finite_grid_monotonicity')
            old = bound
            if a > 2:
                require(ph < pc, 'single_cone_does_not_certify_narrow_sharpness')
            for numerator in range(1, 20):
                p = bound * F(numerator, 20)
                if a < 2 and p >= 1:
                    eps = 2 - a - n * (1 - 1/p)
                    require(eps > 0, 'whitney_epsilon_positive')
                    require(a - 2 + eps == -n * (1 - 1/p), 'whitney_weight_identity')
                    if n > 2:
                        require(p < F(n, n-2), 'local_integrability_range')
                elif a < 2:
                    require(p < 1 and bound > 1, 'low_p_from_l1')
                else:
                    eps = (1/p - (a-1))/2
                    b = a - 2 + eps
                    require(eps > 0 and b > 0, 'holder_epsilon_positive')
                    q = b*p/(1-p)
                    require(q < 1 and q >= 0, 'holder_boundary_exponent')
                    require((q < 1) == ((a-1+eps)*p < 1), 'holder_equivalence')
            # Characteristic radial roots are checked exactly.
            b = -(a+n-2)
            require(b*(b+n-2) == a*(a+n-2), 'negative_radial_root')
            radial_endpoint = F(n-1) - pc*(a+n-2)
            require(radial_endpoint == -1, 'cone_endpoint_log_divergence')
            for scale in (F(1,2), F(3,4), F(5,4), F(2)):
                p = scale*pc
                radial_power = n-1-p*(a+n-2)
                require((radial_power > -1) == (p < pc), 'cone_integral_criterion')

    # Non-grid identities encoded with integer coefficients.
    for n in range(2, 101):
        laplacian_q = 2*(n-1) - sum(2 for _ in range(n-1))
        require(laplacian_q == 0, 'quadratic_harmonicity')
        a = F(2)
        require(F(n)/(n+a-2) == 1 and 1/(a-1) == 1, 'quadratic_l1_transition')
        require(-(a+n-2) == -n, 'quadratic_kelvin_degree')
        # Smooth limiting exponent a=1.
        require(F(n)/(n+1-2) == F(n,n-1), 'smooth_limit')

    # Negative controls: reject tempting erroneous claims explicitly.
    a = F(3)
    require(1/(1-a) < 0 < 1/(a-1), 'reject_sign_typo')
    require(F(1,2) < F(2,3), 'reject_narrow_cone_sharpness_inference')
    for a in (F(2),F(3),F(10)):
        p = 1/(a-1)
        for eps in (F(1,1000),F(1,10),F(1)):
            require((a-1+eps)*p > 1, 'reject_holder_endpoint_extension')
    theta = math.pi/4
    require(1/(theta-1) < 0, 'reject_literal_angle_substitution')
    require(math.isclose(math.pi/(2*theta), 2.0), 'planar_angle_control')
    require(math.isclose(math.pi/(math.pi/3)-1, 2.0), 'four_dimensional_angle_control')
    # The two preceding floating checks are illustrative angle conversions;
    # all theorem parameter inequalities above use Fraction, never floats.

    source_checks = None
    if source_dir is not None:
        source_checks = []
        manifest = json.loads((Path(__file__).parent/'SOURCE_MANIFEST.json').read_text())
        for source in manifest['sources']:
            if 'download_name' not in source:
                continue
            path = Path(source_dir)/source['download_name']
            got = hashlib.sha256(path.read_bytes()).hexdigest()
            require(got == source['sha256'], 'source_sha256')
            source_checks.append({'name':path.name, 'sha256':got, 'passed':True})
    return {'result':'passed', 'checks':counts, 'total_assertions':sum(counts.values()),
            'source_checks':source_checks,
            'limits':['Finite parameter grid is a transcription/algebra control, not a universal proof.',
                      'No numerical eigenvalue calculation is used to certify the theorem.',
                      'Analytic lemmas and a>2 sharpness are not certified by this script.',
                      'Two angle examples use floating arithmetic only as illustrative controls.']}

if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--source-dir')
    args=parser.parse_args()
    print(json.dumps(run(args.source_dir),indent=2,sort_keys=True))
