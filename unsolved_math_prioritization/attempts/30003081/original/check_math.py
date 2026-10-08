#!/usr/bin/env python3
"""Exact finite diagnostics. Written proofs, not these finite checks, carry universal claims."""
from fractions import Fraction as F
from math import comb, factorial
import json

class CheckFailure(Exception):
    pass

def require(condition, message):
    if not condition:
        raise CheckFailure(message)

def monomials(n, d):
    if n == 1:
        return [(d,)]
    return [(k,) + tail for k in range(d + 1) for tail in monomials(n - 1, d - k)]

def rref(rows, width=None):
    a = [[F(x) for x in row] for row in rows]
    n = len(a[0]) if a else (width or 0)
    require(all(len(row) == n for row in a), 'ragged matrix')
    pivots = []
    r = 0
    for c in range(n):
        pivot = next((i for i in range(r, len(a)) if a[i][c]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        q = a[r][c]
        a[r] = [v / q for v in a[r]]
        for i in range(len(a)):
            if i != r and a[i][c]:
                q = a[i][c]
                a[i] = [v - q * w for v, w in zip(a[i], a[r])]
        pivots.append(c)
        r += 1
        if r == len(a):
            break
    return a, pivots

def kernel(rows, width):
    a, piv = rref(rows, width)
    answer = []
    for j in range(width):
        if j not in piv:
            v = [F(0)] * width
            v[j] = F(1)
            for i, p in enumerate(piv):
                v[p] = -a[i][j]
            answer.append(v)
    return answer

def substitute_monomial(e, linear):
    """Remainder modulo a linear equation, represented in the two free variables."""
    pivot = next((i for i, c in enumerate(linear) if c), None)
    require(pivot is not None, 'zero linear equation')
    free = [i for i in range(3) if i != pivot]
    a, b = (-F(linear[j], linear[pivot]) for j in free)
    ans = {}
    for k in range(e[pivot] + 1):
        coeff = comb(e[pivot], k) * a ** k * b ** (e[pivot] - k)
        exp = (e[free[0]] + k, e[free[1]] + e[pivot] - k)
        ans[exp] = ans.get(exp, F(0)) + coeff
    return ans

def log_kernel(lines, degree):
    mons = monomials(3, degree)
    rows = []
    for linear in lines:
        remainders = [substitute_monomial(e, linear) for e in mons]
        for q in monomials(2, degree):
            rows.append([F(linear[j]) * rem.get(q, F(0)) for j in range(3) for rem in remainders])
    return mons, rows, kernel(rows, 3 * len(mons))

def restriction_profile(lines, degree):
    mons, rows, basis = log_kernel(lines, degree)
    for v in basis:
        require(all(sum(x*y for x,y in zip(row,v)) == 0 for row in rows), 'nullspace residual')
    selected = [j*len(mons)+k for j in (0,1) for k,e in enumerate(mons) if e[2] == 0]
    images = [[v[k] for k in selected] for v in basis]
    rank = len(rref(images, len(selected))[1])
    return {'degree':degree,'ambient_dimension':len(basis),'restriction_rank':rank}

SEVEN = [(1,0,0),(0,1,0),(0,0,1),(1,0,-1),(0,1,-1),(1,-1,1),(1,-1,-1)]
FOUR = [(1,0,0),(0,1,0),(0,0,1),(1,-1,0)]

def main():
    profiles = []
    for d in range(1, 6):
        p = restriction_profile(SEVEN, d)
        p['target_dimension'] = d + max(0,d-1)
        p['defect_dimension'] = p['target_dimension']-p['restriction_rank']
        require(p['defect_dimension'] == ({2:1,3:1}.get(d,0)), 'seven-plane defect profile')
        profiles.append(p)
        q = restriction_profile(FOUR,d)
        require(q['restriction_rank'] == d+max(0,d-1), 'product restriction must be onto')
    # Independently encoded degree-two tangency equations for the chosen eta.
    # Variables a,b,c,d,e. Conditions for x-z and y-z, followed by x-y+z.
    equations = [
        [1,0,-1,0,-1,-1],   # 1+a-c-e=0
        [0,0,0,-1,0,1],     # -1-d=0
        [0,0,-1,0,0,0],     # c=0
        [0,1,0,-1,-1,0],    # b-d-e=0
    ]
    # Above row convention: coefficients followed by right-hand side.
    coef=[r[:5] for r in equations]; rhs=[r[5] for r in equations]
    _, piv=rref([a+[b] for a,b in zip(coef,rhs)])
    require(5 not in piv, 'first four tangencies should be consistent')
    # Residual at a=0 and a=7, evaluated at y=3,z=1,x=y-z; -2z(y-z)=-4.
    for a in (0,7,-11):
        x,y,z=2,3,1
        u=x*(x-y+a*z);v=a*y*z;t=z*(-y+(a+1)*z)
        require(u-v+t == -4, 'explicit nonzero tangency residual')
    # Exact normal-monomial counts, contrasting codimension two with a fat point.
    counts=[]
    for n in range(2,7):
        for d in range(1,8):
            count=sum(1 for e in monomials(n+1,d) if e[0]+e[1]>=d-1)
            require(count == n*d+1, 'codimension-two monomial count')
            conditions=comb(n+d,n)-count
            counts.append({'n':n,'degree':d,'space':count,'conditions':conditions})
    require(comb(6,3)-10 == 10, 'P3 double-line conditions')
    require(comb(4,3) == 4, 'P3 double-point conditions')
    # Chern-character class of a point from its Koszul resolution: (1-exp(-u))^3.
    def mul(a,b):
        return [sum(a[i]*b[k-i] for i in range(k+1)) for k in range(4)]
    q=[F(0),F(1),F(-1,2),F(1,6)]
    require(mul(mul(q,q),q) == [0,0,0,1], 'point Chern character')
    out={'status':'PASS_FINITE_DIAGNOSTICS','seven_plane_profiles':profiles,
         'product_profiles_checked':5,'codimension_two_counts':counts,
         'point_ch':[0,0,0,1],
         'scope':'Finite rational diagnostics supplement, and do not prove, the written universal geometric statements.'}
    print(json.dumps(out,sort_keys=True,indent=2))

if __name__ == '__main__':
    main()
