#!/usr/bin/env python3
"""Exact finite algebra and optional input-identity checks; not a topology prover."""
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import sys

N = 6
ZERO = (0,) * N

def require(condition, message):
    if not condition:
        raise ValueError(message)

def clean(p):
    return {k: v for k, v in p.items() if v != 0}

def add(a, b):
    out = dict(a)
    for k, v in b.items():
        out[k] = out.get(k, 0) + v
    return clean(out)

def scale(a, c):
    return clean({k: c * v for k, v in a.items()})

def mul(a, b):
    out = {}
    for i, x in a.items():
        for j, y in b.items():
            k = tuple(u + v for u, v in zip(i, j))
            out[k] = out.get(k, 0) + x * y
    return clean(out)

def diff(a, i):
    out = {}
    for k, v in a.items():
        if k[i]:
            l = list(k)
            l[i] -= 1
            out[tuple(l)] = v * k[i]
    return out

def evaluate(a, point):
    return sum(v * product(point[i] ** k[i] for i in range(N)) for k, v in a.items())

def product(xs):
    out = 1
    for x in xs:
        out *= x
    return out

def form_add(a, b):
    out = {k: dict(v) for k, v in a.items()}
    for k, v in b.items():
        out[k] = add(out.get(k, {}), v)
    return {k: v for k, v in out.items() if v}

def form_scale(a, p):
    return {k: v for k, v in ((k, mul(v, p)) for k, v in a.items()) if v}

def wedge(a, b):
    out = {}
    for i, x in a.items():
        for j, y in b.items():
            if set(i).intersection(j):
                continue
            sign = (-1) ** sum(u > v for u in i for v in j)
            key = tuple(sorted(i + j))
            term = scale(mul(x, y), sign)
            out[key] = add(out.get(key, {}), term)
    return {k: v for k, v in out.items() if v}

def exterior(a):
    out = {}
    for indices, coefficient in a.items():
        for i in range(N):
            out = form_add(out, wedge({(i,): diff(coefficient, i)}, {indices: ONE}))
    return out

def contract(a, vector):
    out = {}
    for indices, coefficient in a.items():
        for pos, i in enumerate(indices):
            key = indices[:pos] + indices[pos + 1:]
            term = scale(mul(coefficient, vector[i]), (-1) ** pos)
            out[key] = add(out.get(key, {}), term)
    return {k: v for k, v in out.items() if v}

def form_value(a, point, vectors):
    f = a
    for vector in vectors:
        f = contract(f, [{ZERO: c} if c else {} for c in vector])
    require(not set(f).difference({()}), 'Evaluation did not yield a scalar')
    return evaluate(f.get((), {}), point)

ONE = {ZERO: 1}
X = []
for i in range(N):
    k = list(ZERO)
    k[i] = 1
    X.append({tuple(k): 1})


def check_math():
    x, y, z, w, u, v = X
    q = add(add(mul(x, x), mul(y, y)), add(mul(z, z), mul(w, w)))
    r = add(mul(u, u), mul(v, v))
    R = [scale(y, -1), x, scale(w, -1), z, {}, {}]
    T = [{}, {}, {}, {}, scale(v, -1), u]
    alpha = {(0,): scale(y, -1), (1,): x, (2,): scale(w, -1), (3,): z}
    eta = {(4,): scale(v, -1), (5,): u}
    omega = wedge(alpha, eta)
    dq = exterior({(): q})
    dr = exterior({(): r})
    da = exterior(alpha)
    dw = exterior(omega)
    require(contract(dq, R) == {}, 'R must be tangent to the q-level sphere')
    require(contract(dr, T) == {}, 'T must be tangent to the r-level circle')
    require(contract(alpha, R) == {(): q}, 'alpha(R)=q failed')
    require(contract(eta, T) == {(): r}, 'eta(T)=r failed')
    require(contract(alpha, T) == {}, 'Cross-factor alpha(T) failed')
    require(contract(eta, R) == {}, 'Cross-factor eta(R) failed')
    require(contract(da, R) == form_scale(dq, {ZERO: -1}), 'i_R d(alpha)=-dq failed')
    require(contract(contract(omega, R), T) == {(): mul(q, r)}, 'omega(R,T)=qr failed')
    # In ambient R^6, i_T i_R d(omega)=r*dq+q*dr. On q=r=1 both differentials vanish.
    expected = form_add(form_scale(dq, r), form_scale(dr, q))
    actual = contract(contract(dw, R), T)
    require(actual == expected, 'Weak condition modulo sphere constraints failed')
    require(exterior(dw) == {}, 'd^2(omega)=0 failed')
    require(wedge(omega, omega) == {}, 'Decomposability identity failed')
    bracket = []
    for j in range(N):
        coefficient = {}
        for i in range(N):
            coefficient = add(coefficient, mul(R[i], diff(T[j], i)))
            coefficient = add(coefficient, scale(mul(T[i], diff(R[j], i)), -1))
        bracket.append(coefficient)
    require(all(not x for x in bracket), 'Commuting generators failed')
    p = (1, 0, 0, 0, 1, 0)
    U = (0, 0, 1, 0, 0, 0)
    V = (0, 0, 0, 1, 0, 0)
    Tp = (0, 0, 0, 0, 0, 1)
    require(evaluate(q, p) == 1 and evaluate(r, p) == 1, 'Test point is not on M')
    for vector in (U, V, Tp):
        require(form_value(dq, p, [vector]) == 0 and form_value(dr, p, [vector]) == 0,
                'Test vector not tangent to M')
    require(form_value(dw, p, [U, V, Tp]) == 2, 'Nonclosedness witness failed')
    # Integral homology is torsion-free for each factor; this only checks the Kunneth ranks.
    ranks = [sum(a * b for i, a in enumerate([1, 0, 0, 1])
                 for j, b in enumerate([1, 1]) if i + j == k) for k in range(5)]
    require(ranks == [1, 1, 0, 1, 1], 'Sphere-product homology rank check failed')
    require(0 < 1, 'Sphere genus must be smaller than torus genus')
    return {'exact_polynomial_form_identities': 'PASS',
            'nonclosedness_witness': 2,
            'integral_kunneth_ranks_given_torsion_free_factors': ranks,
            'topological_proof': 'manual: see PROOF.md',
            'original_closed_form_problem_solved': False}

EXPECTED = {
    'catalog': (21735099, '891938878f1e395de77f6829d5d5d13cb5d5393f85efaa7941fb14bd3e3d7566'),
    'problems': (68931837, '04128381e42a5e312326d74adb0947ee02062ade70229e02d3060ac4ef9942cf'),
    'reports': (80334822, '8da848d31c20eb4eecaa07702eced4724aa4a89f877c2a0774d9f3138389aa6b'),
}

def check_inputs(paths):
    data, receipt = {}, {}
    for name, path in paths.items():
        b = Path(path).read_bytes()
        digest = hashlib.sha256(b).hexdigest()
        size, expected_digest = EXPECTED[name]
        require(len(b) == size and digest == expected_digest, name + ' integrity mismatch')
        data[name] = json.loads(b)
        receipt[name] = {'bytes': len(b), 'sha256': digest, 'match': True}
    require(isinstance(data['catalog'], list) and isinstance(data['problems'], list)
            and isinstance(data['reports'], dict), 'Unexpected dataset top-level schema')
    cat = [x for x in data['catalog'] if str(x.get('id')) == '2999']
    records = [x for x in data['problems'] if str(x.get('id')) == '2999']
    require(len(cat) == len(records) == 1, 'Exact-ID uniqueness failed')
    c, record = cat[0], records[0]
    require(c['problem_number'] == record['problem_number'] == 'KP-4.123', 'Problem-number mismatch')
    report = data['reports'].get(record['problem_number'], {})
    require(report == {}, 'Inherited report is unexpectedly nonempty')
    statement = hashlib.sha256(record['statement'].encode()).hexdigest()
    pair = hashlib.sha256(json.dumps([record, report], sort_keys=True).encode()).hexdigest()
    require(statement == c['statement_hash'] == '6a8125110b6505c896473e9e044f3e63229c5908b78f8941b94b2de882cb10c0', 'Statement hash mismatch')
    require(pair == c['review_hash'] == 'ac85358559b11d7537ed33955622bd4fd0db74b4c56795be28cf85f517376670', 'Complete record/report hash mismatch')
    receipt.update({'exact_id': 2999, 'problem_number': 'KP-4.123',
                    'statement_sha256': statement, 'record_report_pair_sha256': pair,
                    'inherited_report_empty': True,
                    'prose_gate_classification': 'manual review required; never inferred solely from an empty report'})
    return receipt

def check_status():
    path = Path(__file__).resolve().with_name('STATUS.json')
    s = json.loads(path.read_text())
    require(s.get('id') == 2999 and s.get('problem_number') == 'KP-4.123', 'Wrong status identity')
    require(s.get('turns_used') == 2 and s.get('turn_limit') == 5, 'Wrong approach accounting')
    require(s.get('literal_weak_formulation') == 'refuted_by_explicit_counterexample', 'Wrong weak status')
    require(s.get('original_closed_formulation') == 'unresolved_by_this_work', 'Overstated original status')
    require(s.get('novelty_claim') is False, 'Novelty must not be claimed')
    return {'scope_labels': 'PASS'}

def self_test():
    failures = 0
    for label, a, b in [('unequal polynomial', ONE, {}),
                        ('wrong derivative', diff(X[0], 0), {}),
                        ('false equality under optimization', 1, 0)]:
        try:
            require(a == b, label)
        except ValueError:
            failures += 1
    require(failures == 3, 'A deliberately false identity was accepted')
    return {'deliberately_false_checks_rejected': failures}

def main():
    p = argparse.ArgumentParser(description=__doc__)
    for name in EXPECTED:
        p.add_argument('--' + name)
    p.add_argument('--self-test', action='store_true')
    args = p.parse_args()
    paths = {name: getattr(args, name) for name in EXPECTED}
    supplied = sum(value is not None for value in paths.values())
    require(supplied in (0, 3), 'Supply all three dataset paths, or none')
    result = {'math': check_math(), 'status': check_status(),
              'python_optimization_level': sys.flags.optimize}
    if supplied:
        result['inputs'] = check_inputs(paths)
    if args.self_test:
        result['self_test'] = self_test()
    print(json.dumps(result, indent=2, sort_keys=True))

if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, KeyError, TypeError, json.JSONDecodeError) as exc:
        print('CHECK FAILED: ' + str(exc), file=sys.stderr)
        sys.exit(1)
