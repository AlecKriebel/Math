#!/usr/bin/env python3
"""Independent exact rational stress tests of the proposed Koszul rank formula.
Standard library only. No network, randomness, or author's checking code used.
"""
from fractions import Fraction as F
from itertools import product, combinations
import json
from pathlib import Path


def rank(a):
    if not a or not a[0]:
        return 0
    a = [[F(x) for x in row] for row in a]
    r = 0
    for c in range(len(a[0])):
        pivot = next((i for i in range(r, len(a)) if a[i][c]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        den = a[r][c]
        a[r] = [x / den for x in a[r]]
        for i in range(len(a)):
            if i != r and a[i][c]:
                q = a[i][c]
                a[i] = [x - q*y for x,y in zip(a[i], a[r])]
        r += 1
        if r == len(a):
            break
    return r


def monomial_algebra(staircase):
    B = sorted(staircase)
    assert B and all(all(t >= 0 for t in e) for e in B)
    d, n = len(B[0]), len(B)
    idx = {e:i for i,e in enumerate(B)}
    mats = [[[0]*n for _ in range(n)] for _ in range(d)]
    border = set()
    for j,e in enumerate(B):
        for k in range(d):
            nxt = tuple(t+(k==i) for i,t in enumerate(e))
            if nxt in idx:
                mats[k][idx[nxt]][j] = 1
            else:
                border.add(nxt)
            if e[k]:
                pred = tuple(t-(k==i) for i,t in enumerate(e))
                assert pred in idx, 'basis must be divisor closed'
    minimal = [e for e in border if not any(f != e and all(x<=y for x,y in zip(f,e)) for f in border)]
    return mats, len(minimal)


def koszul_ranks(mats, lam):
    d, n = len(mats), len(mats[0])
    t = [[[mats[k][i][j] - (lam[k] if i == j else 0) for j in range(n)] for i in range(n)] for k in range(d)]
    pairs = list(combinations(range(d),2))
    d1 = [sum((t[k][i] for k in range(d)),[]) for i in range(n)]
    d2 = [[0]*(len(pairs)*n) for _ in range(d*n)]
    for c,(i,j) in enumerate(pairs):
        for row in range(n):
            for col in range(n):
                d2[i*n+row][c*n+col] = -t[j][row][col]
                d2[j*n+row][c*n+col] = t[i][row][col]
    # Direct multiplication checks signs and dimensions.
    for i in range(n):
        for j in range(len(pairs)*n):
            assert sum(d1[i][k]*d2[k][j] for k in range(d*n)) == 0
    return rank(d1),rank(d2)


def direct_sum(components):
    d = len(components[0][0])
    n = sum(len(m[0]) for m,_ in components)
    out = [[[0]*n for _ in range(n)] for _ in range(d)]
    off = 0
    for mats,shift in components:
        size = len(mats[0])
        for k in range(d):
            for i in range(size):
                for j in range(size):
                    out[k][off+i][off+j] = mats[k][i][j] + (shift[k] if i == j else 0)
        off += size
    return out

results = []

def check(name,mats,support):
    d,n = len(mats),len(mats[0])
    local=[]
    for lam,expected in support:
        r1,r2 = koszul_ranks(mats,lam)
        got = (d-1)*n+1-r2
        assert r1 == n-1, (name,lam,r1,n)
        assert got == expected, (name,lam,got,expected)
        assert (r2 == (d-1)*(n-1)) == (expected == d)
        local.append({'point':lam,'rank_d1':r1,'rank_d2':r2,'local_generators':got})
    outside = tuple(100+k for k in range(d))
    r1,r2 = koszul_ranks(mats,outside)
    assert r1 == n and r2 == (d-1)*n
    results.append({'name':name,'d':d,'length':n,'local_results':local,'expected_global_generators':max(mu for _,mu in support)})

for n in [1,2,5]:
    m,mu = monomial_algebra({(i,) for i in range(n)})
    check(f'univariate_length_{n}',m,[((0,),mu)])

# Distinct staircase shapes; minimal monomial generator counts are known independently.
for rows in [(1,), (3,3), (3,2,1), (4,2), (3,3,1), (2,2,2,2), (5,4,2,1)]:
    m,mu = monomial_algebra({(i,j) for j,width in enumerate(rows) for i in range(width)})
    check('plane_staircase_'+str(rows),m,[((0,0),mu)])

for d in [2,3,4]:
    m,mu = monomial_algebra(set(product(range(2),repeat=d)))
    check(f'box_CI_d{d}',m,[(tuple([0]*d),mu)])
    m,mu = monomial_algebra({tuple([0]*d)} | {tuple(int(i==j) for i in range(d)) for j in range(d)})
    check(f'square_zero_maximal_ideal_d{d}',m,[(tuple([0]*d),mu)])

# Nonmonomial Gorenstein example: 1,x,y,z,s with x^2=y^2=z^2=s,
# distinct degree-one products zero, and s times x,y,z zero.
g = [[[0]*5 for _ in range(5)] for _ in range(3)]
for k in range(3):
    g[k][1+k][0] = 1
    g[k][4][1+k] = 1
check('Gorenstein_length5_not_CI',g,[((0,0,0),5)])

m2,mu2 = monomial_algebra(set(product(range(2),repeat=3)))
simple,mu_simple = monomial_algebra({(0,0,0)})
mixed = direct_sum([(g,(0,0,0)),(m2,(2,-1,3)),(simple,(-2,5,1))])
check('three_supports_nonCI_CI_simple',mixed,[((0,0,0),5),((2,-1,3),3),((-2,5,1),3)])

# A deliberately inadmissible noncyclic tuple must fail the claimed support rank.
bad = [[[0,0],[0,0]],[[0,0],[0,0]]]
assert koszul_ranks(bad,(0,0))[0] == 0 != 1

# Follow-up checks of the author's added diagnostic examples.
g2 = [[[0]*5 for _ in range(5)] for _ in range(3)]
for k in range(3): g2[k][1+k][0] = 1
g2[0][4][2] = 1
g2[1][4][1] = 1
g2[2][4][3] = 1
check('added_Gorenstein_xy_equals_z_squared',g2,[((0,0,0),5)])
t = [[int(i==j+1) for j in range(4)] for i in range(4)]
def mul(a,b):
    return [[sum(a[i][k]*b[k][j] for k in range(len(a))) for j in range(len(a))] for i in range(len(a))]
t2 = mul(t,t)
t3 = mul(t2,t)
check('added_nonstrict_CI_t_t2_t3', [t,t2,t3], [((0,0,0),3)])

payload={'tests':results,'test_count':len(results),'inadmissible_tuple_guard_passed':True,'arithmetic':'exact Fraction Gaussian elimination','scope':'Finite stress tests, not a proof of the global generation theorem.'}
Path(__file__).with_name('independent_results.json').write_text(json.dumps(payload,indent=2)+'\n')
print(f'PASS {len(results)} independent exact examples, including nonmonomial Gorenstein and three-support cases')
print('PASS chain conditions, expected local counts, CI thresholds, outside-support acyclicity ranks')
print('PASS noncyclic tuple guard')
