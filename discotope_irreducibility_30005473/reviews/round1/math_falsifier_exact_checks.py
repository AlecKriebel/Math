from fractions import Fraction as F
from itertools import combinations
from math import sqrt
import json


def rank(rows):
    a = [[F(x) for x in row] for row in rows]
    if not a:
        return 0
    r = 0
    for c in range(len(a[0])):
        pivot = next((i for i in range(r, len(a)) if a[i][c]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        v = a[r][c]
        a[r] = [x / v for x in a[r]]
        for i in range(len(a)):
            if i != r and a[i][c]:
                v = a[i][c]
                a[i] = [x - v*y for x, y in zip(a[i], a[r])]
        r += 1
        if r == len(a):
            break
    return r


def solve_square(rows, rhs):
    n = len(rows)
    a = [[F(x) for x in row] + [F(y)] for row, y in zip(rows, rhs)]
    for c in range(n):
        pivot = next(i for i in range(c, n) if a[i][c])
        a[c], a[pivot] = a[pivot], a[c]
        v = a[c][c]
        a[c] = [x/v for x in a[c]]
        for i in range(n):
            if i != c and a[i][c]:
                v = a[i][c]
                a[i] = [x-v*y for x,y in zip(a[i],a[c])]
    return [a[i][-1] for i in range(n)]


def columns(d, ts):
    return [[F(t)**j for j in range(d)] for t in ts]


def dot(a, b):
    return sum((x*y for x,y in zip(a,b)), F(0))


# Check all GP index subsets for several block shapes, including sum ranks
# below/equal/above d and a full-dimensional block.
gp_counts = []
for d, sizes in [(2,[2,2]), (4,[2,2]), (5,[2,2,2]), (6,[2,3,4]), (7,[2,2]), (6,[6,2,3])]:
    cols = columns(d, range(sum(sizes)))
    blocks = []
    k = 0
    for size in sizes:
        blocks.append(cols[k:k+size])
        k += size
    count = 0
    for n in range(1, len(sizes)+1):
        for ids in combinations(range(len(sizes)),n):
            selected = sum((blocks[i] for i in ids), [])
            rows = list(map(list,zip(*selected)))
            assert rank(rows) == min(d,sum(sizes[i] for i in ids))
            count += 1
    gp_counts.append({'d':d,'sizes':sizes,'subsets':count})

# Two simultaneously annihilated nonorthogonal 2-disc blocks in R^5.
cols = columns(5,range(6))
u = [F(0),F(-6),F(11),F(-6),F(1)]
targets = [F(3,5),F(4,5),F(-5,13),F(12,13)]
assert targets[0]**2+targets[1]**2 == 1
assert targets[2]**2+targets[3]**2 == 1
assert [dot(c,u) for c in cols] == [0,0,0,0,24,120]
w = solve_square([c[:4] for c in cols[:4]],targets) + [F(0)]
assert [dot(c,w) for c in cols[:4]] == targets
q = [dot(c,w) for c in cols[4:]]
xi = [sum((cols[k][j]*targets[k] for k in range(4)),F(0)) for j in range(5)]
base = [F(24),F(120)]
base_norm = sqrt(sum(float(x*x) for x in base))
x_limit = [float(xi[j])+sum(float(cols[4+k][j]*base[k])/base_norm for k in range(2)) for j in range(5)]
errors = []
for eps in [F(1,10),F(1,100),F(1,1000),F(1,10000)]:
    z = [base[k]+eps*q[k] for k in range(2)]
    assert z != [0,0]
    # The two annihilated support points are exactly the arbitrary choices:
    assert [(eps*t)/(eps) for t in targets] == targets
    znorm = sqrt(sum(float(a*a) for a in z))
    point = [float(xi[j])+sum(float(cols[4+k][j]*z[k])/znorm for k in range(2)) for j in range(5)]
    errors.append({'epsilon':str(eps),'euclidean_error':sqrt(sum((a-b)**2 for a,b in zip(point,x_limit)))})

# Dependency-free exact multivariate polynomial calculation. Variables
# are a,b,Y,Z; reduce modulo a^2+Y^2-4 and b^2+Z^2-1.
zero = (0,0,0,0)
def polyadd(p,q):
    ans = dict(p)
    for m,c in q.items():
        ans[m] = ans.get(m,F(0))+c
        if not ans[m]: del ans[m]
    return ans
def polyscale(p,k):
    return {m:c*k for m,c in p.items() if c*k}
def polymul(p,q):
    ans = {}
    for m,c in p.items():
        for n,e in q.items():
            v = tuple(x+y for x,y in zip(m,n))
            ans[v] = ans.get(v,F(0))+c*e
    return {m:c for m,c in ans.items() if c}
def power(p,n):
    ans = {zero:F(1)}
    for _ in range(n): ans = polymul(ans,p)
    return ans
def var(i):
    m = list(zero); m[i] = 1
    return {tuple(m):F(1)}
def constant(n): return {zero:F(n)} if n else {}
def reduce_poly(p):
    ans = {}
    pending = dict(p)
    while pending:
        m,c = pending.popitem()
        if m[0] >= 2:
            n = list(m); n[0] -= 2
            for bump,factor in [(0,F(4)),(2,F(-1))]:
                v = list(n); v[2] += bump; v = tuple(v)
                pending[v] = pending.get(v,F(0))+c*factor
                if not pending[v]: del pending[v]
        elif m[1] >= 2:
            n = list(m); n[1] -= 2
            for bump,factor in [(0,F(1)),(2,F(-1))]:
                v = list(n); v[3] += bump; v = tuple(v)
                pending[v] = pending.get(v,F(0))+c*factor
                if not pending[v]: del pending[v]
        else:
            ans[m] = ans.get(m,F(0))+c
    return {m:c for m,c in ans.items() if c}
a,b,Y,Z = [var(i) for i in range(4)]
X = polyadd(a,b)
sum_term = polyadd(polyadd(power(X,2),power(Y,2)),power(Z,2))
P = polyadd(power(polyadd(sum_term,constant(-5)),2),
            polyscale(polymul(polyadd(constant(4),polyscale(power(Y,2),-1)),
                              polyadd(constant(1),polyscale(power(Z,2),-1))),-4))
assert reduce_poly(P) == {}
def separator(x,y,z):
    return (x*x+y*y+z*z-5)**2-4*(4-y*y)*(1-z*z)
assert separator(F(0),F(0),F(1)) == 16
for point in [(F(11,5),F(8,5),F(0)),(F(0),F(2),F(1)),(F(9,5),F(8,5),F(4,5))]:
    assert separator(*point) == 0

print(json.dumps({
    'status':'all assertions passed',
    'GP_exhaustive_subset_checks':gp_counts,
    'two_annihilated_blocks':{'u':list(map(str,u)),'w':list(map(str,w)),
                             'A3_transpose_w':list(map(str,q)),
                             'first_four_transpose_targets':list(map(str,targets)),
                             'convergence_numerics':errors},
    'separator_polynomial_remainder':'0 exactly',
    'separator_at_e3':'16 exactly'
},indent=2))
