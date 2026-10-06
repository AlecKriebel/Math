#!/usr/bin/env python3
"""Fail-closed package and exact-polynomial diagnostics. No mathematical assert statements.

The geometric and topological arguments remain written proofs in REPORT.md.
This program neither certifies those proofs nor declares KP-4.110 solved.
"""
from fractions import Fraction as Q
from pathlib import Path
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parent
CHECKS = 0


def require(condition, message):
    global CHECKS
    if not condition:
        raise ValueError(message)
    CHECKS += 1


def clean(p):
    return {k: v for k, v in p.items() if v}


def add(*polys):
    r = {}
    for p in polys:
        for m, c in p.items():
            r[m] = r.get(m, Q(0)) + c
    return clean(r)


def scale(p, c):
    return clean({m: c * x for m, x in p.items()})


def mul(p, q):
    r = {}
    for a, c in p.items():
        for b, d in q.items():
            m = tuple(x + y for x, y in zip(a, b))
            r[m] = r.get(m, Q(0)) + c * d
    return clean(r)


def diff(p, i):
    r = {}
    for m, c in p.items():
        if m[i]:
            n = list(m)
            n[i] -= 1
            r[tuple(n)] = c * m[i]
    return clean(r)


def variable(i):
    return {tuple(int(j == i) for j in range(4)): Q(1)}


def parse_polynomial(terms):
    require(isinstance(terms, list) and len(terms) == 4, 'Expected four polynomial terms')
    r = {}
    for term in terms:
        require(set(term) == {'powers', 'coefficient'}, 'Unexpected polynomial term schema')
        m = tuple(term['powers'])
        require(len(m) == 4 and all(type(e) is int and 0 <= e <= 2 for e in m), 'Invalid exponents')
        require(m not in r, 'Duplicate monomial')
        require(isinstance(term['coefficient'], str), 'Coefficient must be an exact rational string')
        r[m] = Q(term['coefficient'])
    return clean(r)


def polynomial_checks(model):
    q1, q2, p1, p2 = [variable(i) for i in range(4)]
    f = parse_polynomial(model['f_terms'])
    expected_f = add(scale(mul(p1, q2), -1), scale(mul(p2, q1), 1),
                     scale(mul(p1, q1), Q(-1, 2)), scale(mul(p2, q2), Q(-1, 2)))
    require(f == expected_f, 'Polynomial does not match Proposition 1')
    lam0 = [scale(p1, Q(-1, 2)), scale(p2, Q(-1, 2)), scale(q1, Q(1, 2)), scale(q2, Q(1, 2))]
    lam1 = [add(lam0[i], diff(f, i)) for i in range(4)]
    lam_expected = [add(scale(p1, -1), p2), add(scale(p1, -1), scale(p2, -1)), scale(q2, -1), q1]
    for i in range(4):
        require(lam1[i] == lam_expected[i], 'Incorrect differentiated primitive component')
    for i in range(4):
        for j in range(i + 1, 4):
            actual = add(diff(lam1[j], i), scale(diff(lam1[i], j), -1))
            expected = {(0, 0, 0, 0): Q(1)} if (i, j) in [(0, 2), (1, 3)] else {}
            require(actual == expected, 'Exterior derivative is not the standard symplectic form')
            require(diff(diff(f, i), j) == diff(diff(f, j), i), 'Mixed partials do not commute')
    vector = [lam1[2], lam1[3], scale(lam1[0], -1), scale(lam1[1], -1)]
    expected_vector = [scale(q2, -1), q1, add(p1, scale(p2, -1)), add(p1, p2)]
    for i in range(4):
        require(vector[i] == expected_vector[i], 'Wrong Liouville vector component')
    for i in (2, 3):
        require(not {m: c for m, c in vector[i].items() if m[2] == m[3] == 0}, 'The plane p=0 is not invariant')
    norm_q = add(mul(q1, q1), mul(q2, q2))
    deriv_norm = add(*(mul(diff(norm_q, i), vector[i]) for i in range(4)))
    require(not deriv_norm, 'Rotation does not preserve q norm')
    radius = Q(model['orbit_radius'])
    inner, outer = map(Q, model['cutoff_squared_radii'])
    require(radius == Q(1, 2), 'Unexpected orbit radius')
    require((inner, outer) == (Q(1, 2), Q(3, 4)), 'Unexpected cutoff constants')
    require(0 < radius * radius < inner < outer < 1, 'Orbit/cutoff/boundary separation fails')
    require(radius * radius > 0, 'The proposed orbit is stationary')
    norm_all = add(*(mul(x, x) for x in (q1, q2, p1, p2)))
    radial = [scale(x, Q(1, 2)) for x in (q1, q2, p1, p2)]
    require(add(*(mul(diff(norm_all, i), radial[i]) for i in range(4))) == norm_all,
            'The standard Lyapunov identity fails')
    return True


def status_checks(status):
    require(status['problem_id'] == 2986 and status['problem_number'] == 'KP-4.110', 'Wrong problem')
    require(status['status'] == 'partial', 'The outcome must remain partial')
    require(status['full_solution'] is False and status['target_example_constructed'] is False,
            'Unsupported solved/example declaration')
    require(status['turns_used'] == 4 and status['turn_limit'] == 5, 'Unexpected approach count')
    require(status['stopping_reason'] == 'stalled_partial', 'Unexpected stopping reason')
    require(status['novelty_established'] is False, 'Unsupported novelty declaration')


def expect_rejection(call, message):
    try:
        call()
    except (ValueError, KeyError, TypeError, ZeroDivisionError):
        return
    raise ValueError('Negative control was incorrectly accepted: ' + message)


def main():
    require(len(sys.argv) == 1, 'This checker accepts no flags or unchecked alternate input')
    manifest = json.loads((ROOT / 'MANIFEST.json').read_text())
    require(manifest['schema'] == 'sha256-member-manifest-v1', 'Unknown manifest schema')
    entries = manifest['files']
    require(isinstance(entries, list) and len(entries) == 8, 'Unexpected member count')
    names = [e['path'] for e in entries]
    require(len(names) == len(set(names)), 'Duplicate manifest names')
    expected_names = {'REPORT.md', 'README.md', 'ATTEMPT_LOG.md', 'STATUS.json',
                      'SOURCE_AUDIT.json', 'model.json', 'verify.py', 'CHECK_RESULTS.json'}
    require(set(names) == expected_names, 'Manifest has missing or unexpected members')
    actual = {p.name for p in ROOT.iterdir() if p.is_file()}
    require(actual == expected_names | {'MANIFEST.json'}, 'Package has unlisted or missing files')
    require(not any(p.is_dir() or p.is_symlink() for p in ROOT.iterdir()), 'Nested directories or symlinks are forbidden')
    for e in entries:
        require(set(e) == {'path', 'bytes', 'sha256'}, 'Unexpected manifest entry schema')
        b = (ROOT / e['path']).read_bytes()
        require(type(e['bytes']) is int and len(b) == e['bytes'], 'Byte count mismatch: ' + e['path'])
        require(hashlib.sha256(b).hexdigest() == e['sha256'], 'Hash mismatch: ' + e['path'])
    model = json.loads((ROOT / 'model.json').read_text())
    require(set(model) == {'coordinates', 'f_terms', 'orbit_radius', 'cutoff_squared_radii'}, 'Unexpected model schema')
    require(model['coordinates'] == ['q1', 'q2', 'p1', 'p2'], 'Unexpected coordinate order')
    status = json.loads((ROOT / 'STATUS.json').read_text())
    status_checks(status)
    polynomial_checks(model)
    positive_checks = CHECKS
    bad = json.loads(json.dumps(model))
    bad['f_terms'][0]['coefficient'] = '1'
    expect_rejection(lambda: polynomial_checks(bad), 'flipped rotational coefficient')
    bad2 = json.loads(json.dumps(model))
    bad2['orbit_radius'] = '1'
    expect_rejection(lambda: polynomial_checks(bad2), 'orbit moved to boundary')
    bad3 = dict(status)
    bad3['full_solution'] = True
    expect_rejection(lambda: status_checks(bad3), 'false full-solution claim')
    result = {'result': 'PASS', 'positive_checks': positive_checks, 'negative_controls_rejected': 3,
              'arithmetic': 'exact rational sparse polynomials', 'target_solved': False,
              'limitations': 'Written geometric and topological proofs are not machine-certified.'}
    require(result == json.loads((ROOT / 'CHECK_RESULTS.json').read_text()), 'Stored results differ from replay')
    print(json.dumps(result, sort_keys=True, indent=2))


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print('FAIL: ' + str(exc), file=sys.stderr)
        sys.exit(1)
