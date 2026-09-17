#!/usr/bin/env python3
"""Floating-point sign/boundary diagnostic from manuscript matrix formulas.
This is not Lean proof evidence. Uses only Python's standard library.
"""
import cmath
import itertools
import json
import math
from pathlib import Path

maxerr = {name: 0.0 for name in (
    'complex_correlators', 'extra_column', 'local_moments',
    'literal_residual', 'aligned_residual', 'transported_score')}
wrong = []
cases = 0
for d in range(2, 7):
    delta = 1 if d % 2 == 0 else 0
    def e(x):
        return cmath.exp(1j*x)
    z = [e(math.pi*(2*j+delta)/d) for j in range(d)]
    p = [[(1+e(2*math.pi*y/d)*z[j])/abs(1+e(2*math.pi*y/d)*z[j])
          for j in range(d)] for y in range(d)]
    lam = [(-1.0)**(l-1)*e(math.pi*l*(l-1)/d)/
           (d*math.sin(math.pi*(l-.5)/d)) for l in range(d)]
    perms = (itertools.permutations(range(d)) if d <= 4 else
             [tuple(range(d)), tuple(reversed(range(d))), tuple(range(d-2))+(d-1,d-2)])
    def cyc(w):
        return [[w[j] if i == (j+1) % d else 0j for j in range(d)] for i in range(d)]
    def adj(a):
        return [[a[j][i].conjugate() for j in range(d)] for i in range(d)]
    def corr(a, b):
        # Direct Phi expectation of A tensor B.
        return sum(a[i][j]*b[i][j] for i in range(d) for j in range(d))/d
    def residual(a, b, c):
        # Maximum coordinate of (c I - A tensor B) Phi.
        return max(abs((c if i == k else 0)-sum(a[i][j]*b[k][j] for j in range(d)))/
                   math.sqrt(d) for i in range(d) for k in range(d))
    X = cyc([1]*d)
    for perm in perms:
        cases += 1
        A = [cyc([(e(-math.pi*l*(l-1+delta)/d)*e(-2*math.pi*l*t/d)).conjugate()
                  for t in perm]) for l in range(d)]
        B = [cyc([p[y][t].conjugate() for t in perm]) for y in range(d)]
        for l in range(d):
            for y in range(d):
                maxerr['complex_correlators'] = max(maxerr['complex_correlators'],
                    abs(corr(A[l], B[y])-lam[l]*e(-2*math.pi*l*y/d)))
            maxerr['extra_column'] = max(maxerr['extra_column'],
                abs(corr(A[l], X)-(1 if l == 0 else 0)))
            bhat = [[sum(e(2*math.pi*l*y/d)*B[y][i][j] for y in range(d))
                     for j in range(d)] for i in range(d)]
            maxerr['literal_residual'] = max(maxerr['literal_residual'],
                residual(A[l], bhat, d*lam[l]))
        maxerr['local_moments'] = max(maxerr['local_moments'],
            max(abs(sum(m[i][i] for i in range(d))/d) for m in A+B+[X]))
        maxerr['aligned_residual'] = max(maxerr['aligned_residual'], residual(A[0], X, 1))
        Bprime = [adj(b) for b in B]
        Xprime = adj(X)
        score = sum(lam[l].conjugate()*sum(e(2*math.pi*l*y/d)*corr(A[l], adj(Bprime[y]))
                    for y in range(d)) for l in range(d))+corr(A[0], adj(Xprime))
        maxerr['transported_score'] = max(maxerr['transported_score'], abs(score.real-d-1))
        unchanged = sum(lam[l].conjugate()*sum(e(2*math.pi*l*y/d)*corr(A[l], Bprime[y])
                        for y in range(d)) for l in range(d))+corr(A[0], Xprime)
        if abs(unchanged.real-d-1) > .1 and len(wrong) < 3:
            wrong.append({'d': d, 'permutation': perm,
                          'untransported_score': unchanged.real, 'correct_score': d+1})
assert max(maxerr.values()) < 1e-12
report = {'status': 'floating_point_diagnostic_passed_NOT_PROOF', 'cases': cases,
          'dimensions': 'every permutation d=2,3,4; identity/reversal/final-swap d=5,6',
          'max_absolute_errors': maxerr, 'deliberate_wrong_fixed_functional': wrong}
text = json.dumps(report, indent=2)+'\n'
Path(__file__).with_suffix('.json').write_text(text)
print(text)
