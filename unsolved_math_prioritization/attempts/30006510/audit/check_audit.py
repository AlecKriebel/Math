#!/usr/bin/env python3
"""Portable audit controls. Read the frozen release; never rewrite it.

Python standard library only. Optional positional argument: release directory.
The checks support, but do not prove, the analytic/geometric arguments.
"""
from fractions import Fraction as F
from pathlib import Path
from hashlib import sha256
from math import comb
import json
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
RELEASE = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else HERE.parent / 'release'
EXPECTED = 'bbe672f14e9a541bc1700d76454c809654478ff159038c0982f17b75f3191648'
checks = []
def check(name, condition):
    if not condition:
        raise AssertionError(name)
    checks.append(name)
def digest(p):
    return sha256(p.read_bytes()).hexdigest()

manifest_path = RELEASE / 'AUTHOR_MANIFEST.json'
check('frozen manifest SHA-256', digest(manifest_path) == EXPECTED)
manifest = json.loads(manifest_path.read_text())
check('manifest contains seven author files', len(manifest['files']) == 7)
before = {}
for entry in manifest['files']:
    rel = Path(entry['path'])
    check('safe relative manifest path: ' + str(rel), not rel.is_absolute() and '..' not in rel.parts)
    p = RELEASE / rel
    before[str(rel)] = digest(p)
    check('file length: ' + str(rel), p.stat().st_size == entry['bytes'])
    check('file SHA-256: ' + str(rel), before[str(rel)] == entry['sha256'])

# Reproduce author output on a disposable copy, because its script writes a receipt.
with tempfile.TemporaryDirectory(prefix='hyperbolic-audit-') as tmp:
    p = Path(tmp) / 'check.py'
    p.write_bytes((RELEASE / 'checks/check.py').read_bytes())
    run = subprocess.run([sys.executable, str(p)], text=True, capture_output=True, check=True)
    receipt = json.loads((Path(tmp) / 'result.json').read_text())
    frozen_receipt = json.loads((RELEASE / 'checks/result.json').read_text())
    check('author controls reproduce all 40 outcomes', receipt == frozen_receipt and receipt['passed'] == 40)
    check('author control stdout agrees', json.loads(run.stdout) == {'all_passed': True, 'passed': 40})

# Laurent-polynomial verification of strict-convexity algebra.
# Monomial key is (A power, B power, exp(t) power).
def add(p, q):
    r = dict(p)
    for k, v in q.items():
        r[k] = r.get(k, F(0)) + v
    return {k: v for k, v in r.items() if v}
def scale(p, c):
    return {k: c*v for k, v in p.items() if c*v}
def mul(p, q):
    r = {}
    for a, x in p.items():
        for b, y in q.items():
            k = tuple(i+j for i, j in zip(a, b))
            r[k] = r.get(k, F(0)) + x*y
    return {k: v for k, v in r.items() if v}
def derivative(p):
    return {k: k[2]*v for k, v in p.items() if k[2]*v}
u = {(1,0,1):F(1,2), (0,1,1):F(1,2), (1,0,-1):F(1,2), (0,1,-1):F(-1,2)}
v = derivative(u)
check('hyperbolic distance auxiliary function has u second derivative = u', derivative(v) == u)
check('symbolic u squared minus u-prime squared = A squared minus B squared',
      add(mul(u,u), scale(mul(v,v), -1)) == {(2,0,0):F(1), (0,2,0):F(-1)})
# h=arcosh(u): numerator of h'' is u''(u^2-1)-u(u')^2.
one = {(0,0,0): F(1)}
lhs = add(mul(derivative(v), add(mul(u,u), scale(one,-1))), scale(mul(u,mul(v,v)),-1))
rhs = mul(u,{(2,0,0):F(1),(0,2,0):F(-1),(0,0,0):F(-1)})
check('symbolic strict convexity numerator', lhs == rhs)

# Moment-free probability control: divergent first moment does not invalidate
# an integral with pointwise difference bounded by distance between test points.
for N in (1, 2, 10, 100):
    p = [F(1,n*(n+1)) for n in range(1,N+1)]
    check(f'heavy-tail probability mass telescopes N={N}', sum(p) == 1-F(1,N+1))
    check(f'heavy-tail first-moment partial sum N={N}',
          sum(n*p[n-1] for n in range(1,N+1)) == sum(F(1,k) for k in range(2,N+2)))
# This is a general probability test, not a proposed convex-cell volume law.

# Independent truncated reciprocal-volume transport test. A missing probability
# mass represents the infinite-volume sector, whose outgoing transport here is zero.
p = [F(1,10),F(1,5),F(3,10)]
vol = [F(1,100), F(2,3), F(17)]
f = [F(2),F(3),F(5)]
for n in (1,2,50,100,1000):
    outgoing = sum(a*b/c for a,b,c in zip(p,f,vol) if c >= F(1,n))
    check(f'finite source-density bound at truncation n={n}', outgoing <= n*max(f)*sum(p))
gamma = sum(a/c for a,c in zip(p,vol))
q = [a/c/gamma for a,c in zip(p,vol)]
check('independent mixed-sector Palm law normalizes', sum(q) == 1)
check('independent mixed-sector volume identity is p_f, not one',
      gamma*sum(a*c for a,c in zip(q,vol)) == F(3,5))
check('independent invariant-mark inversion',
      gamma*sum(a*b for a,b in zip(q,f)) == sum(a*b/c for a,b,c in zip(p,f,vol)))

# Exact leading-term controls for sinh(r)^(d-1) = 2^(-p) sum_j (-1)^j binom(p,j)e^((p-2j)r).
# Integration has leading coefficient 1/(p 2^p), with all other exponential
# terms of strictly smaller exponent and, when p is even, one linear term.
for d in range(2,13):
    pwr = d-1
    terms = {pwr-2*j: F((-1)**j*comb(pwr,j),2**pwr) for j in range(pwr+1)}
    check(f'ball asymptotic leading exponent d={d}', max(terms) == d-1)
    check(f'ball asymptotic leading coefficient d={d}', terms[pwr]/pwr == F(1,pwr*2**pwr))

# Deterministic finite-measure cover bound: disjoint incidence volumes at least
# 1/k cannot occur more than k times the window volume. Reconstruction divides
# each positive cell weight by itself, regardless of ordinary cell volume.
for k in (1,3,7):
    weights = [F(1,k),F(2,k),F(3,k)]
    window_volume = sum(weights)
    check(f'incidence-cover count bound k={k}', len(weights) <= k*window_volume)
    check(f'weighted reconstruction normalization k={k}', sum(w/w for w in weights) == len(weights))

for rel, value in before.items():
    check('release unchanged after controls: ' + rel, digest(RELEASE / rel) == value)
check('manifest unchanged after controls', digest(manifest_path) == EXPECTED)
result = {
    'all_passed': True,
    'audit_controls_passed': len(checks),
    'author_controls_reproduced': 40,
    'frozen_manifest_sha256': EXPECTED,
    'release_unchanged': True,
    'checks': checks,
    'scope': 'Integrity, exact symbolic algebra, and finite normalization controls. Analytic proof review and source inspection are in AUDIT_REPORT.md. These controls are not formal verification or a proof of the original open problem.'
}
(HERE / 'audit_controls_result.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k: v for k,v in result.items() if k != 'checks'},indent=2))
