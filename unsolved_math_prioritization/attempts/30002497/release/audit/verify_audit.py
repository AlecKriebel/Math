#!/usr/bin/env python3
"""Verify binding, exact interval relationships, and the export correction.

Usage: python verify_audit.py --author ../author --output verification_results.json
No source downloads or remote operations are performed. With --rerun, the
standard-library independent controls are rerun and compared byte-for-byte.
"""
import argparse
import hashlib
import importlib.util
import json
from fractions import Fraction as Q
from pathlib import Path
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent


def interval(s):
    return tuple(Q(x.strip()) for x in s.strip('[]').split(','))


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def exact_mpf(raw):
    s, m, e, bc = raw
    assert bc >= 0
    return Q((-1)**s*m)*Q(2)**e


def verify(author=None, rerun=False):
    out = {'problem_id': 30002497, 'input_hashes_verified': None}
    if author:
        binding = json.loads((HERE/'AUDITED_INPUTS.json').read_text())
        for f in binding['files']:
            data = (author/f['path']).read_bytes()
            assert hashlib.sha256(data).hexdigest() == f['sha256'], f['path']
        out['input_hashes_verified'] = len(binding['files'])
    low = json.loads((HERE/'corrected_controls_2048_40.json').read_text())
    high = json.loads((HERE/'corrected_controls_4096_60.json').read_text())
    independent = json.loads((HERE/'independent_results.json').read_text())
    relationships = []
    for a, b, c in zip(low['metallic_reciprocals'], high['metallic_reciprocals'],
                       independent['metallic_reciprocals']):
        assert a['m'] == b['m'] == c['m']
        m = a['m']
        lo, hi = interval(a['derivative_interval'])
        hl, hh = interval(b['derivative_interval'])
        il, ih = map(Q, [c['derivative']['lower'], c['derivative']['upper']])
        assert il <= lo <= hl <= hh <= hi <= ih
        assert (lo > 0 if m <= 9 else hi < 0)
        assert (il > 0 if m <= 9 else ih < 0)
        assert a['sign'] == b['sign'] == c['sign']
        relationships.append({'m': m, 'high_nested_in_low': True,
                              'low_nested_in_independent': True,
                              'sign': a['sign']})
    assert len(relationships) == 11
    out['interval_relationships'] = relationships
    from mpmath import iv
    import mpmath
    assert mpmath.__version__ == '1.3.0'
    fixed = load_module('outward_controls', HERE/'verify_controls_outward.py')
    test_count = 0
    for dps in (20, 40, 60):
        iv.dps = dps
        for z in [iv.mpf(0), iv.mpf(1), iv.mpf(-1), iv.mpf(1)/3,
                  -iv.mpf(1)/3, iv.sqrt(2), iv.ln(11), iv.mpf([-3, 2])]:
            lo, hi = interval(fixed.bracket(z))
            exact_lo, exact_hi = map(exact_mpf, z._mpi_)
            assert lo <= exact_lo <= exact_hi <= hi
            test_count += 1
    out['outward_serializer_exact_tests'] = test_count
    iv.dps = 40
    y = (2+iv.sqrt(8))/2
    text_lo, text_hi = interval(str(y))
    exact_lo, exact_hi = map(exact_mpf, y._mpi_)
    # A reproducible counterexample to the original outward-safe comment.
    assert text_lo > exact_lo
    out['original_serialization_counterexample'] = {
        'argument': 'y_2 = 1 + sqrt(2)', 'iv_dps': 40,
        'nearest_display': str(y), 'corrected_outward_display': fixed.bracket(y),
        'exact_binary_lower_as_fraction': str(exact_lo),
        'displayed_lower_minus_binary_lower': str(text_lo-exact_lo),
        'displayed_lower_is_inward': True,
        'effect': 'display/export guarantee; in-memory sign tests unaffected'}
    if rerun:
        engine = load_module('independent_controls', HERE/'independent_controls.py')
        repeated = engine.run(independent['cutoff'])
        assert repeated == independent
        out['independent_rerun_exact_match'] = True
    out['all_checks_passed'] = True
    return out


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--author', type=Path)
    p.add_argument('--rerun', action='store_true')
    p.add_argument('--output', type=Path)
    a = p.parse_args()
    data = json.dumps(verify(a.author, a.rerun), indent=2)+'\n'
    if a.output:
        a.output.write_text(data)
    else:
        print(data, end='')
