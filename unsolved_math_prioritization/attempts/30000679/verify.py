#!/usr/bin/env python3
"""Finite algebra controls and hash-bound source-locator checks; no theorem prover."""
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent

def mul(p, q):
    return tuple(p[q[i]] for i in range(len(p)))

def inv(p):
    q = [0] * len(p)
    for i, x in enumerate(p):
        q[x] = i
    return tuple(q)

def conjugate(x, g):
    return mul(mul(inv(g), x), g)

def closure(generators, identity):
    gens = set(generators)
    gens |= {inv(g) for g in gens}
    found, todo = {identity}, [identity]
    while todo:
        x = todo.pop()
        for g in gens:
            y = mul(x, g)
            if y not in found:
                found.add(y)
                todo.append(y)
    return found

def derived(group, identity):
    return closure((mul(mul(mul(inv(x), inv(y)), x), y)
                    for x in group for y in group), identity)

def algebra_controls():
    e4 = tuple(range(4))
    s4 = set(itertools.permutations(range(4)))
    h = {p for p in s4 if p[0] == 0}
    dh = derived(h, e4)
    assert len(h) == 6 and len(dh) == 3 and derived(dh, e4) == {e4}
    conjugates = {frozenset(conjugate(x, g) for x in h) for g in s4}
    core = set.intersection(*(set(c) for c in conjugates))
    assert len(conjugates) == 4 and core == {e4}
    assert core <= h and all(conjugate(x, g) in core for x in core for g in s4)
    # Negative control: finite-by-trivial considerations do not imply solvability.
    e5 = tuple(range(5))
    a5 = {p for p in itertools.permutations(range(5))
          if sum(p[i] > p[j] for i in range(5) for j in range(i+1, 5)) % 2 == 0}
    assert len(a5) == 60 and derived(a5, e5) == a5
    assert len(a5) // len({e5}) == 60
    # Check the finite-normalizer identity used to clarify Claim 14.
    normalizer_cases = 0
    for group, identity in [(s4, e4), (a5, e5)]:
        for c in group - {identity}:
            f = {g for g in group if mul(c, g) == mul(g, c)}
            ordered_f = sorted(f)
            nf = {g for g in group if {conjugate(x, g) for x in f} == f}
            cf = {g for g in group if all(mul(g, x) == mul(x, g) for x in f)}
            images = {tuple(conjugate(x, g) for x in ordered_f) for g in nf}
            assert cf <= f
            assert len(nf) == len(cf) * len(images)
            normalizer_cases += 1
    # Exact square-root-map identities in three odd dihedral examples.
    root_cases = 0
    for n in [3, 5, 7]:
        identity = tuple(range(n))
        r = tuple((x + 1) % n for x in range(n))
        i = tuple((-x) % n for x in range(n))
        rotations = closure([r], identity)
        group = closure([r, i], identity)
        centralizer = {g for g in group if mul(g, i) == mul(i, g)}
        assert len(group) == 2*n and len(centralizer) == 2
        def f(g):
            product = mul(i, conjugate(i, g))
            roots = [x for x in rotations if mul(x, x) == product]
            assert len(roots) == 1
            return mul(roots[0], inv(g))
        for g in group - centralizer:
            fg = f(g)
            assert fg in centralizer
            for b in centralizer:
                assert f(mul(b, g)) == mul(fg, inv(b))
                root_cases += 1
    return {
        'status': 'PASS_FINITE_ALGEBRA_ONLY',
        'S4_order': 24, 'solvable_H_order': 6,
        'H_derived_series_orders': [6, 3, 1],
        'distinct_H_conjugates': 4, 'normal_core_order': 1,
        'A5_order': 60, 'A5_derived_subgroup_order': 60,
        'negative_control_solvable_by_finite_need_not_be_solvable': True,
        'normalizer_identity_cases': normalizer_cases,
        'dihedral_square_root_identity_cases': root_cases,
        'proves_model_theoretic_theorem': False,
    }

def source_controls(directory):
    bindings = json.loads((HERE / 'SOURCE_BINDINGS.json').read_text())
    results = []
    for source in bindings['sources']:
        path = directory / source['basename']
        if not path.is_file():
            return {'status': 'NOT_RUN_MISSING_SOURCES', 'missing': source['basename']}, 2
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != source['sha256']:
            return {'status': 'FAIL_SOURCE_HASH', 'source': source['id']}, 1
        checks = []
        for check in source['checks']:
            raw = subprocess.check_output([
                'pdftotext', '-layout', '-f', str(check['pdf_page']),
                '-l', str(check['pdf_page']), str(path), '-'], text=True)
            normalized = ' '.join(raw.replace('\x1c', 'fi').split())
            passed = all(fragment in normalized for fragment in check['fragments'])
            checks.append({'label': check['label'], 'pass': passed})
        results.append({'id': source['id'], 'sha256_match': True, 'checks': checks})
    passed = all(c['pass'] for result in results for c in result['checks'])
    return {'status': 'PASS_SOURCE_IDENTITY_AND_LOCATORS' if passed else 'FAIL_LOCATOR',
            'sources': results, 'proves_model_theoretic_theorem': False}, 0 if passed else 1

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--sources', type=Path)
    args = parser.parse_args()
    result = {'algebra': algebra_controls()}
    if args.sources is None:
        result['source_gate'] = {'status': 'NOT_RUN_MISSING_SOURCES'}
        code = 2
    else:
        result['source_gate'], code = source_controls(args.sources)
    result['overall'] = 'PASS_CONTROLS_ONLY' if code == 0 else 'INCOMPLETE_OR_FAILED'
    print(json.dumps(result, indent=2, sort_keys=True))
    return code

if __name__ == '__main__':
    try:
        sys.exit(main())
    except (AssertionError, OSError, subprocess.CalledProcessError) as error:
        print(json.dumps({'overall': 'FAIL_CONTROLS', 'error': str(error)}, sort_keys=True))
        sys.exit(1)
