#!/usr/bin/env python3
"""Read-only exact LP/support/packing controls; no universal theorem by census."""
from fractions import Fraction as F
from itertools import combinations, product
import json

counts = {}
def check(family, condition):
    if not condition:
        raise AssertionError(family)
    counts[family] = counts.get(family, 0) + 1
def mv(M, w):
    return [sum(F(a) * b for a, b in zip(row, w)) for row in M]
def transpose(M):
    return list(map(list, zip(*M)))
def solve(A, b):
    aug = [[F(x) for x in row] + [F(y)] for row, y in zip(A, b)]
    n = len(A)
    for col in range(n):
        pivot = next((i for i in range(col, n) if aug[i][col]), None)
        if pivot is None:
            return None
        aug[col], aug[pivot] = aug[pivot], aug[col]
        factor = aug[col][col]
        aug[col] = [x / factor for x in aug[col]]
        for i in range(n):
            if i != col:
                factor = aug[i][col]
                aug[i] = [x - factor * y for x, y in zip(aug[i], aug[col])]
    return [row[-1] for row in aug]
def packing_vertices(M, theta):
    """Max t: p_i>=t>=0, Mp<=theta, sum(p)<=1; active-set exact LP."""
    n = len(M[0])
    H = [list(map(F, row)) + [F(0)] for row in M]
    rhs = [theta] * len(M)
    for i in range(n):
        row = [F(0)] * (n + 1)
        row[i], row[-1] = F(-1), F(1)
        H.append(row); rhs.append(F(0))
    H.extend([[F(1)] * n + [F(0)], [F(0)] * n + [F(-1)]])
    rhs.extend([F(1), F(0)])
    values = []
    for inds in combinations(range(len(H)), n + 1):
        v = solve([H[i] for i in inds], [rhs[i] for i in inds])
        if v is not None and all(a <= b for a, b in zip(mv(H, v), rhs)):
            values.append(v[-1])
    return max(values)

# Source 2.2 complementary slackness certifies only positive primal support.
M = [[1, 1], [1, 0]]
primal, dual = [F(1), F(0)], [F(0), F(1)]
check('duality_support', min(mv(M, primal)) >= 1)
check('duality_support', max(mv(transpose(M), dual)) <= 1)
check('duality_support', sum(primal) == sum(dual) == 1)
check('duality_support', mv(transpose(M), dual) == [1, 0])
check('duality_support', sum(primal[j] * (1 - v) for j, v in enumerate(mv(transpose(M), dual))) == 0)
check('duality_support', not all(v >= 1 for v in mv(transpose(M), dual)))

# Independent all-positive coupled-middle-polytope obstruction.
P, Q = [[1, 0], [0, 1]], [[1, 1], [1, 0]]
x, y = F(2, 5), F(3, 5)
a, b, c = [F(1, 2)] * 2, [y, x], [y, x]
for w in (a, b, c):
    check('coupled_middle', min(w) > 0 and sum(w) == 1)
for L, w, threshold in ((P,b,x),(transpose(P),a,x),(Q,c,y),(transpose(Q),b,y)):
    check('coupled_middle', min(mv(L,w)) >= threshold)
b_opt = [F(1, 2)] * 2
check('coupled_middle', min(mv(P,b_opt)) > x)
check('coupled_middle', min(mv(transpose(Q),b_opt)) < y)

# Nonattainment and rounding are independently adversarial generic controls.
# This is not asserted to be an actual sequence of psi examples.
for n in range(1, 101):
    z = F(1, 2) + F(1, 2*n)
    check('generic_nonattainment', z > F(1, 2))
    check('generic_nonattainment', F(1,2) + F(1,2*(n+1)) < z)
exact, rounded = [F(1,2),F(1,2)], [F(499,1000),F(501,1000)]
check('boundary_rounding', sum(exact) == sum(rounded) == 1)
check('boundary_rounding', min(mv(P,exact)) == F(1,2))
check('boundary_rounding', min(mv(P,rounded)) < F(1,2))
check('normalization', sum(a) == sum(b) == sum(c) == 1)
check('normalization', min(mv(P,[v/3 for v in b])) < x)

# A zero-weight middle vertex remains topologically relevant until deleted.
P0, Q0 = [[1, 0]], [[1], [0]]
check('zero_middle_path', any(P0[0][j]*Q0[j][0] for j in range(2)))
check('zero_middle_path', not (P0[0][1]*Q0[1][0]))

# Exact read-only LP checks on cyclic templates, including zero residual.
for r in range(2, 6):
    for p in range(1, r):
        N = [[int((i-j)%r < p) for j in range(r)] for i in range(r)]
        theta, delta = F(p,r), p
        check('packing_lp', packing_vertices(N,theta) == theta/delta)
        check('packing_lp', 1-r*theta/delta == 0)

# Independently traced seed row sets from the primary figure, one-based.
sets = [{1,3,4,5},{2,3,4,5},{3,6,7},{4,6,7},{5,6,7},{1,2,6},{1,2,7}]
bseed = [F(v,27) for v in [5,5,3,3,3,4,4]]
qseed = [F(v,27) for v in [4,4,3,3,3,5,5]]
for complement, numerator in ((False,13),(True,14)):
    N = [[int((j in row) != complement) for j in range(1,8)] for row in sets]
    theta = F(numerator,27); Delta = max(map(sum,N))
    check('seed_packing', mv(N,qseed) == [theta]*7)
    check('seed_packing', mv(transpose(N),bseed) == [theta]*7)
    check('seed_packing', Delta == 4)
    check('seed_packing', len(set(map(tuple,transpose(N)))) == 7)
    t = theta/Delta; ps = [t]*7; residual = 1-sum(ps)
    check('seed_packing', residual > 0)
    check('seed_packing', max(mv(N,ps)) == theta)
    check('seed_packing', sum(v*d for v,d in zip(bseed,map(sum,N))) == 7*theta)
    for i,j in product(range(7),repeat=2):
        if i != j:
            check('seed_packing', any(N[k][i] and not N[k][j] for k in range(7)))

# Candidate turn2 duals: directions, support, normalization, optimality.
P2 = [[1,1,1,0],[0,0,0,1]]
Q2 = [[1,1,0],[1,0,0],[0,1,0],[0,0,1]]
R2 = [[1,1,0],[0,0,1]]
uf, vf = [F(1),F(0),F(0)], [F(0),F(1),F(0),F(0)]
ur, vr = [F(1),F(0)], [F(0),F(1),F(1),F(0)]
for u,v in ((uf,vf),(ur,vr)):
    check('template_dual', sum(u)==1 and min(u)>=0 and min(v)>=0)
check('template_dual', mv(R2,uf)==mv(P2,vf))
check('template_dual', mv(transpose(R2),ur)==mv(transpose(Q2),vr))
for yy in (F(251,1000), F(3,10), F(1,3)):
    q = [yy,yy,1-2*yy]; pp=[F(1,2)]*2
    check('template_dual', max(mv(transpose(R2),pp)) == F(1,2)*sum(vf))
    check('template_dual', max(mv(R2,q)) == yy*sum(vr))
    check('template_dual', max(mv(R2,q))>max(mv(transpose(R2),pp)))

# A rotation moves asterisks with their coordinates; no phi-to-psi inference.
triple = [('x',True),('y',True),('z',False)]
rotation = triple[-1:]+triple[:-1]
check('rotation', rotation == [('z',False),('x',True),('y',True)])
check('rotation', rotation != [('z',True),('x',True),('y',False)])
gaps = [abs(F(13,27*d)-F(14,27*e)) for d,e in product(range(1,5),repeat=2)]
check('integer_gap', min(gaps)==F(1,108))
check('integer_gap', all(g>0 for g in gaps))
print(json.dumps({'status':'PASS','assertions':sum(counts.values()),'categories':counts,
    'scope':'Exact finite LP, support and boundary controls. Generic nonattainment and rounding controls do not assert psi examples. No invariant minima, exact psi values, ordering or priority computed.'},sort_keys=True,indent=2))
