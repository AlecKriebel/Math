"""Finite adversarial sanity checks for AUDIT.md; universal proofs are separate."""
import itertools
import random
from math import isqrt
import sympy as s
rng = random.Random(1822)
cases = 0
for n in range(1, 8):
    for d in range(1, n+1):
        for trial in range(20):
            C = s.Matrix([[rng.randrange(-2,3) for j in range(n)] for i in range(d)])
            indices = list(itertools.combinations(range(n), d))
            nonzero = [I for I in indices if C[:, I].det() != 0]
            if not nonzero:
                continue
            I = max(nonzero)
            M = s.eye(n)
            for i in range(n):
                for j in range(i):
                    M[i,j] = s.Rational(rng.randrange(-3,4), rng.randrange(1,5))
            assert (C*M)[:,I].det() == C[:,I].det()
            for J in indices:
                if M[J,I].det() != 0:
                    assert all(j>=i for j,i in zip(J,I))
            cases += 1
print('Maximal-minor invariance PASS:', cases, 'exact rational cases')
for n in range(2,6):
    m = isqrt(2*n)+1
    short = []
    for v in itertools.product(range(-m,m+1), repeat=n):
        if any((x-v[0]) % m for x in v):
            continue
        norm2 = sum(x*x for x in v)
        if 0 < norm2 <= n:
            short.append(v)
    assert set(short) == {(-1,)*n, (1,)*n}
    B = s.Matrix([(1,)*n]+[tuple(m if j==i else 0 for j in range(n)) for i in range(1,n)])
    assert abs(B.det()) == m**(n-1)
    print('Cyclic example PASS: n=',n,'m=',m)
