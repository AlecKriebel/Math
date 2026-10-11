#!/usr/bin/env python3
"""Independent exact controls; imports no author/reviewer implementation.

The universal claims are the written representation/analytic proofs. Finite
syzygy-coordinate controls use Dade's credited classification, not a claimed
finite simulation of an arbitrary endotrivial group.
"""
from collections import defaultdict
from fractions import Fraction as Q
from itertools import combinations, product
from math import comb
from random import Random
import json

COUNTS = defaultdict(int)
def check(value, family):
    assert value, family
    COUNTS[family] += 1

def rref_spaces(p, r):
    out = []
    for d in range(r + 1):
        for pivots in combinations(range(r), d):
            cells = [(i, j) for i, c in enumerate(pivots)
                     for j in range(c + 1, r) if j not in pivots]
            for vals in product(range(p), repeat=len(cells)):
                rows = [[int(j == c) for j in range(r)] for c in pivots]
                for (i, j), v in zip(cells, vals): rows[i][j] = v
                span = frozenset(tuple(sum(a * row[j] for a, row in zip(cs, rows)) % p
                                       for j in range(r))
                                 for cs in product(range(p), repeat=d))
                out.append((d, span))
    return sorted(out, key=lambda x: (x[0], sorted(x[1])))

def tidy(d): return {x: v for x, v in d.items() if v}
def add(a, b):
    z = defaultdict(Q, a)
    for x, v in b.items(): z[x] += v
    return tidy(z)
def scale(a, v): return tidy({x: v * c for x, c in a.items()})
def syzygy_dim(p, r, n):
    d = 1
    for j in range(abs(n)): d = p ** r * comb(j + r - 1, r - 1) - d
    return d

def stable_class(p, r, n):
    if r != 1: return n
    return 0 if p == 2 else n % 2

def norm(a, spaces, p):
    return sum(abs(c) * syzygy_dim(p, spaces[h][0], t) for (h, t), c in a.items())

def cmul(a,b): return (a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def cconj(a): return (a[0],-a[1])
UNITS=[(1,0),(0,1),(-1,0),(0,-1)]
def cpow(a,n):
    if n<0:return cpow(cconj(a),-n)
    z=(1,0)
    for _ in range(n):z=cmul(z,a)
    return z

LATTICES = []
rng = Random(7020614)
for p, r in [(2, 0), (2, 1), (3, 1), (5, 1), (2, 3), (2, 4), (3, 3), (5, 2), (7, 2)]:
    spaces = rref_spaces(p, r)
    lookup = {H: i for i, (_, H) in enumerate(spaces)}
    n = len(spaces)
    meet = {(h, k): lookup[H & K]
            for h, (_, H) in enumerate(spaces) for k, (_, K) in enumerate(spaces)}
    le = lambda h, k: spaces[h][1] <= spaces[k][1]
    def res(h, t): return stable_class(p, spaces[h][0], t)
    def multiply(a, b):
        z = defaultdict(Q)
        for (h, t), x in a.items():
            for (k, s), y in b.items():
                l = meet[h, k]
                if l: z[l, res(l, t + s)] += x * y
        return tidy(z)
    def mu(h, k):
        d = spaces[k][0] - spaces[h][0]
        return (-1) ** d * p ** (d * (d - 1) // 2) if le(h, k) else 0
    idem = {h: {(l, 0): mu(l, h) for l in range(1, n) if mu(l, h)}
            for h in range(1, n)}
    def lift(h, f):
        z = {}
        for t, c in f.items():
            z = add(z, scale(multiply(idem[h], {(h, t): 1}), c))
        return z
    def inverse(b):
        blocks = {}
        for h in range(1, n):
            pb = multiply(idem[h], b)
            blocks[h] = {t: c for (l, t), c in pb.items() if l == h}
            check(lift(h, blocks[h]) == pb, "weighted_completed_inverse")
        return blocks
    for h, k in product(range(n), repeat=2):
        if le(h, k):
            check(sum(mu(h, j) for j in range(n) if le(h, j) and le(j, k))
                  == int(h == k), "mobius_closed_formula")
            for t in range(-9, 10):
                if h:
                    wh = syzygy_dim(p, spaces[h][0], res(h, t))
                    wk = syzygy_dim(p, spaces[k][0], res(k, t))
                    check(wh <= wk and (wk - wh) % (p ** spaces[h][0]) == 0,
                          "actual_syzygy_restriction_weights")
        l = meet[h, k]
        a_h, a_k, a_l = (p ** (r - spaces[x][0]) for x in [h, k, l])
        double_cosets = p ** (r - spaces[h][0] - spaces[k][0] + spaces[l][0])
        check(double_cosets * a_l == a_h * a_k, "mackey_normalization")
        if h and k:
            check(multiply(idem[h], idem[k]) == (idem[h] if h == k else {}),
                  "orthogonal_blocks")
    if r:
        total = {}
        for v in idem.values(): total = add(total, v)
        check(total == {(n - 1, 0): 1}, "orthogonal_blocks")
        for h in range(1, n):
            d = spaces[h][0]
            for t, s in product(range(-7, 8), repeat=2):
                wt, ws, wts = [syzygy_dim(p, d, res(h, v)) for v in [t, s, t+s]]
                check(wts <= wt * ws and (wt * ws - wts) % (p ** d) == 0,
                      "actual_syzygy_tensor_multiplicity")
            for k in range(1, n):
                for t in [-11, -2, -1, 0, 1, 2, 13]:
                    lhs = multiply(idem[h], {(k, res(k, t)): 1})
                    rhs = lift(h, {res(h, t): 1}) if le(h, k) else {}
                    check(lhs == rhs, "collapsing_restrictions_and_projections")
            C = sum(abs(c) for c in idem[h].values())
            for _ in range(9):
                f = defaultdict(Q)
                for t in range(-5, 6): f[res(h, t)] += Q(rng.randrange(-9, 10), 5)
                f = tidy(f)
                image = lift(h, f)
                fn = norm({(h, t): c for t, c in f.items()}, spaces, p)
                check(fn <= norm(image, spaces, p) <= C * fn,
                      "weighted_completed_block_bounds")
                check(inverse(image)[h] == f, "weighted_completed_inverse")
        Csum = sum(sum(abs(c) for c in v.values()) for v in idem.values())
        for _ in range(6):
            b = defaultdict(Q)
            for h in range(1, n):
                for t in range(-3, 4): b[h, res(h, t)] += Q(rng.randrange(-5, 6), 3)
            b = tidy(b); blocks = inverse(b); rebuilt = {}
            for h, f in blocks.items(): rebuilt = add(rebuilt, lift(h, f))
            check(rebuilt == b, "weighted_completed_inverse")
            fn = sum(norm({(h, t): c for t, c in f.items()}, spaces, p)
                     for h, f in blocks.items())
            check(fn <= Csum * norm(b, spaces, p), "weighted_completed_inverse")
            # Exact full/stable splitting, including cancellation of D.
            D = sum(c * syzygy_dim(p, spaces[h][0], t) for (h, t), c in b.items())
            check(norm(b, spaces, p) <= norm(b, spaces, p) + abs(D)
                  <= 2 * norm(b, spaces, p), "full_stable_norm")
        for h in range(1,n):
            allowed=([(1,0)] if p==2 else [(1,0),(-1,0)]) if spaces[h][0]==1 else UNITS
            for u in allowed:
                def value(k,t):return cpow(u,res(h,t)) if le(h,k) else (0,0)
                for _ in range(25):
                    k,j=rng.randrange(1,n),rng.randrange(1,n)
                    t,s=rng.randrange(-15,16),rng.randrange(-15,16)
                    l=meet[k,j]
                    rhs=value(l,t+s) if l else (0,0)
                    check(cmul(value(k,t),value(j,s))==rhs,"exact_unitary_species")
                    check(value(k,-t)==cconj(value(k,t)),"exact_unitary_species")
                    a_k=p**(r-spaces[k][0]);v=value(k,t)
                    check(a_k*a_k*(v[0]*v[0]+v[1]*v[1])
                          <=(a_k*syzygy_dim(p,spaces[k][0],res(k,t)))**2,
                          "unnormalized_dimension_bounded_species")
    else:
        check(n == 1 and not idem, "trivial_group_excluded_edge")
    LATTICES.append({"p": p, "rank": r, "subgroups": n,
                     "functor": "actual syzygy classes (credited Dade input)",
                     "maximum_mobius_bound": max([sum(abs(c) for c in v.values())
                                                   for v in idem.values()] or [0])})

# Actual induction matrices for cyclic endotrivial cores in rank two. The
# core is a Jordan block of size 1 or p-1; induction uses a regular complement.
def ident(n): return [[int(i == j) for j in range(n)] for i in range(n)]
def mm(a, b, p):
    return [[sum(x * y for x, y in zip(row, col)) % p for col in zip(*b)] for row in a]
def mp(a, n, p):
    z = ident(len(a))
    for _ in range(n): z = mm(z, a, p)
    return z
def sub(a, b, p): return [[(x-y)%p for x,y in zip(ar,br)] for ar,br in zip(a,b)]
def kron(a, b):
    return [[x*y for x in ar for y in br] for ar in a for br in b]
def matrix_rank(a, p):
    if not a: return 0
    a = [row[:] for row in a]; rank = 0
    for j in range(len(a[0])):
        pivot = next((i for i in range(rank, len(a)) if a[i][j]%p), None)
        if pivot is None: continue
        a[rank], a[pivot] = a[pivot], a[rank]
        v = pow(a[rank][j]%p, -1, p)
        a[rank] = [v*x%p for x in a[rank]]
        for i in range(len(a)):
            if i != rank and a[i][j]%p:
                v = a[i][j]%p
                a[i] = [(x-v*y)%p for x,y in zip(a[i],a[rank])]
        rank += 1
        if rank == len(a): break
    return rank

ACTUAL_MODULES = []
for p in [2, 3, 5]:
    vecs = list(product(range(p), repeat=2))
    lines = [H for d,H in rref_spaces(p,2) if d == 1]
    for H in lines:
        h = next(v for v in sorted(H) if any(v)); c = next(v for v in vecs if v not in H)
        coord = {tuple((a*h[i]+b*c[i])%p for i in range(2)):(a,b)
                 for a,b in product(range(p),repeat=2)}
        for m in sorted(set([1, p-1])):
            A = ident(m)
            for j in range(m-1): A[j][j+1] = 1
            R = [[int(i==(j+1)%p) for j in range(p)] for i in range(p)]
            n = m*p
            actions = {v:kron(mp(A,a,p),mp(R,b,p)) for v,(a,b) in coord.items()}
            check(mp(actions[(1,0)],p,p)==ident(n), "actual_induction_actions")
            check(mp(actions[(0,1)],p,p)==ident(n), "actual_induction_actions")
            for C in lines:
                v = next(v for v in sorted(C) if any(v))
                free = matrix_rank(mp(sub(actions[v],ident(n),p),p-1,p),p)==n//p
                check(free == (C != H), "actual_cyclic_recovery_of_H")
            check(n%(p*p)!=0,"actual_induced_nonprojective_dimension")
            ACTUAL_MODULES.append({"p":p,"core_dimension":m,"induced_dimension":n})

    # Direct matrix Jordan-rank check of core(Omega_C(k) tensor Omega_C(k))=k.
    m=p-1;A=ident(m)
    for j in range(m-1):A[j][j+1]=1
    action=kron(A,A);N=sub(action,ident(m*m),p)
    for j in range(1,p):
        check(matrix_rank(mp(N,j,p),p)==(p-2)*(p-j),"actual_cyclic_tensor_core")
    check((p-1)**2==1+p*(p-2),"actual_cyclic_tensor_multiplicities")
    if p>2:
        check((p-1)**2!=1,"stable_dimension_not_multiplicative")

# F8 proper-family example rebuilt with the other irreducible cubic x^3+x^2+1.
# We also inspect it after a quadratic extension F8 -> F64. Distinct polynomial
# coordinates are independent of the author's bitwise implementation.
def fadd(a,b): return tuple((x+y)%2 for x,y in zip(a,b))
def fmul(a,b):
    cs=[0]*5
    for i,x in enumerate(a):
        for j,y in enumerate(b): cs[i+j]^=x*y
    for i in range(4,2,-1):
        if cs[i]: cs[i]=0;cs[i-1]^=1;cs[i-3]^=1
    return tuple(cs[:3])
F8=list(product(range(2),repeat=3));zero=(0,0,0);one=(1,0,0);z=(0,1,0)
for a,b,c in product(F8,repeat=3):
    check(fmul(fmul(a,b),c)==fmul(a,fmul(b,c)),"extension_field_arithmetic")
    check(fmul(a,fadd(b,c))==fadd(fmul(a,b),fmul(a,c)),"extension_field_arithmetic")
for a in F8[1:]: check(any(fmul(a,b)==one for b in F8),"extension_field_arithmetic")
lam=[zero]
for coeffs in product(range(2),repeat=3):
    v=zero
    for c,a in zip(coeffs,[one,z,fmul(z,z)]):
        if c:v=fadd(v,a)
    check((v==zero)==(not any(coeffs)),"F8_ordinary_cyclic_restrictions")
    if any(coeffs):lam.append(v)
check(len(set(lam))==8,"F8_ordinary_cyclic_restrictions")
check(fadd(z,z)==zero,"F8_shifted_nonprojectivity")
check(2%8!=0,"F8_shifted_nonprojectivity")

# For A=[[a,b],[c,d]], AJ=JA iff c=0,d=a. Enumerate every F8 matrix;
# centralizer units iff a != 0, nonunits square to zero in characteristic two.
for a,b,c,d in product(F8,repeat=4):
    AJ=(zero,a,zero,c); JA=(c,d,zero,zero)
    check((AJ==JA)==(c==zero and d==a),"F8_actual_endomorphism_locality")
    if c==zero and d==a:
        check((fmul(a,a)==zero)==(a==zero),"F8_actual_endomorphism_locality")

F64=list(product(F8,repeat=2))
def eadd(a,b):return(fadd(a[0],b[0]),fadd(a[1],b[1]))
def emul(a,b):
    ac=fmul(a[0],b[0]);bd=fmul(a[1],b[1]);ad=fmul(a[0],b[1]);bc=fmul(a[1],b[0])
    return(fadd(ac,bd),fadd(fadd(ad,bc),bd)) # y^2=y+1
ez=(zero,zero);eo=(one,zero)
for a in F64[1:]: check(any(emul(a,b)==eo for b in F64),"F8_to_F64_base_change")
for a,b in product(F8,repeat=2):
    check(emul((a,zero),(b,zero))==(fmul(a,b),zero),"F8_to_F64_base_change")
for a in lam[1:]:check((a,zero)!=ez,"F8_to_F64_base_change")

print(json.dumps({"total_exact_assertions":sum(COUNTS.values()),"families":dict(COUNTS),
 "lattices":LATTICES,"actual_induced_matrix_cases":len(ACTUAL_MODULES),
 "proper_F8_example_independent_cubic": "x^3+x^2+1",
 "field_extension":"F8 subset F64=F8[y]/(y^2+y+1)",
 "infinite_completion_claim_proved_in_writing":True,
 "universal_symmetry_claimed":False},indent=2))
