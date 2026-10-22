"""Exact finite sanity checks; not a substitute for the universal proof."""
from fractions import Fraction as F
from math import isqrt

for n in range(2, 17):
    m = (4*n*n).bit_length()
    den = 2**m
    num = isqrt(den*den//2)+1
    t = F(num, den)
    assert F(1,2) < t*t < (1+F(1,n*n))**2/2
    B = []
    for i in range(n):
        row = [F(0) for _ in range(n)] if not B else [x/2 for x in B[-1]]
        row[i] = t**i
        B.append(row)
    dot = lambda x,y: sum(a*b for a,b in zip(x,y))
    star, mu = [], []
    for i, row in enumerate(B):
        coeff = [dot(row,s)/dot(s,s) for s in star]
        s = [row[k]-sum(coeff[j]*star[j][k] for j in range(i)) for k in range(n)]
        assert s == [t**i if k==i else 0 for k in range(n)]
        assert all(abs(x)<=F(1,2) for x in coeff)
        if i:
            assert dot(s,s)+coeff[-1]**2*dot(star[-1],star[-1]) > F(3,4)*dot(star[-1],star[-1])
        star.append(s); mu.append(coeff)
    v = [2*x-y for x,y in zip(B[-1],B[-2])]
    assert v == [2*t**(n-1) if k==n-1 else 0 for k in range(n)]
    D = (2*den)**(n-1)
    assert all((D*x).denominator==1 for row in B for x in row)
    # X(D b1) has coefficient D on e1, hence requires 1/t copies of D b2.
    assert (1/t).denominator != 1
    print(f'n={n}: exact reducedness, integral scaling, short vector, and ideal failure PASS')
