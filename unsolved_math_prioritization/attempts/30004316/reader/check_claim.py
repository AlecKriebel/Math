#!/usr/bin/env python3
"""Independent finite checks; no imported source archive or network access.

The mathematical arguments in REPORT.md are all-degree proofs. This program
checks finite instances and exact rational linear algebra, not those quantifiers.
Only the standard library and SymPy are used. See PORTABILITY.md for edits.
"""
from collections import defaultdict
from fractions import Fraction as F
from itertools import product, permutations
import argparse
import json
from pathlib import Path
import sympy as sp


def require(condition, detail):
    """Keep each finite check active under normal Python, -O, and -OO."""
    if not condition:
        raise AssertionError(detail)


def r(w, j):
    w = list(w)
    w[j], w[j + 1] = w[j + 1], (w[j] + 1) % 4
    return tuple(w)


def reduced_lift(p):
    """Bubble-sort labels then reverse: reduced adjacent swaps from identity."""
    a, swaps = list(p), []
    for last in range(len(a) - 1, 0, -1):
        for j in range(last):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                swaps.append(j)
    require(a == list(range(len(p))), 'check failed at original line 30')
    return list(reversed(swaps))


def qs(n):
    words = list(product(range(4), repeat=n))
    index = {w: i for i, w in enumerate(words)}
    q = sp.zeros(len(words))
    lifts = [reduced_lift(p) for p in permutations(range(n))]
    for w in words:
        for lift in lifts:
            z = w
            for j in lift:
                z = r(z, j)
            q[index[z], index[w]] += (-1) ** len(lift)
    return words, q


def classes(n):
    words = list(product(range(4), repeat=n))
    parent = {w: w for w in words}
    def find(w):
        if parent[w] != w:
            parent[w] = find(parent[w])
        return parent[w]
    for w in words:
        for j in range(n - 1):
            parent[find(r(w, j))] = find(w)
    roots = sorted(set(find(w) for w in words))
    return {w: roots.index(find(w)) for w in words}, len(roots)


# Exact Q(i), represented without symbolic simplification or floating point.
class G:
    __slots__ = ('a', 'b')
    def __init__(self, a=0, b=0):
        self.a, self.b = F(a), F(b)
    def __add__(self, y):
        if not isinstance(y, G): y = G(y)
        return G(self.a + y.a, self.b + y.b)
    __radd__ = __add__
    def __neg__(self): return G(-self.a, -self.b)
    def __sub__(self, y): return self + (-y if isinstance(y,G) else G(-y))
    def __mul__(self, y):
        if not isinstance(y, G): y = G(y)
        return G(self.a*y.a-self.b*y.b, self.a*y.b+self.b*y.a)
    __rmul__ = __mul__
    def inv(self):
        d = self.a*self.a+self.b*self.b
        return G(self.a/d,-self.b/d)
    def __truediv__(self, y):
        if not isinstance(y, G): y = G(y)
        return self*y.inv()
    def __eq__(self, y):
        if not isinstance(y, G): y=G(y)
        return (self.a,self.b)==(y.a,y.b)
    def __bool__(self): return self.a != 0 or self.b != 0
    def __repr__(self): return f'({self.a},{self.b})'


LAM = [G(1),G(0,1),G(-1),G(0,-1)]


def clean(z): return {w:a for w,a in z.items() if a}


def add(*zs):
    z=defaultdict(G)
    for t in zs:
        for w,a in t.items(): z[w] += a
    return clean(z)


def apply(f,z):
    ans=defaultdict(G)
    for w,a in z.items():
        for v,b in f(w).items(): ans[v] += a*b
    return clean(ans)


def differential(w):
    """Lebed d=sum (-1)^(i-1)(left-face minus right-face), epsilon(x)=1."""
    z=defaultdict(G)
    prefix=G(1)
    for j,a in enumerate(w):
        if a == 0:
            z[w[:j]+w[j+1:]] += 4*((-1)**j)*(prefix-1)
        prefix = prefix*LAM[a]
    return clean(z)


def homotopy(w):
    """Contraction off the pure u0-tensor block."""
    pos = next((j for j,a in enumerate(w) if a != 0), None)
    if pos is None: return {}
    end=pos+1
    while end<len(w) and w[end]==0: end+=1
    gap=end-pos-1
    if gap % 2: return {}
    c=4*(LAM[w[pos]]-1)
    return {w[:pos+1]+(0,)+w[pos+1:]: G((-1)**(pos+1))/c}


def eig_qs(w):
    z=defaultdict(G)
    for p in permutations(range(len(w))):
        v=list(w); a=G(1)
        for j in reduced_lift(p):
            a = a*(-LAM[v[j]])
            v[j],v[j+1]=v[j+1],v[j]
        z[tuple(v)] += a
    return clean(z)


def end_boundary(w):
    z=defaultdict(G)
    if w and w[0]==0: z[w[1:]] += 4
    if w and w[-1]==0: z[w[:-1]] += 4*((-1)**len(w))
    return clean(z)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, help='optional JSON output path; default: stdout only')
    args = parser.parse_args()
    out={}
    for w in product(range(4),repeat=3):
        require(r(r(r(w,0),1),0)==r(r(r(w,1),0),1), 'check failed at original line 154')
    require(len({r(w,0) for w in product(range(4),repeat=2)})==16, 'check failed at original line 155')
    for x in range(4):
        require({r((x,y),0)[0] for y in range(4)}==set(range(4)), 'check failed at original line 157')
    for y in range(4):
        require({r((x,y),0)[1] for x in range(4)}==set(range(4)), 'check failed at original line 159')
    out['YBE_and_nondegeneracy']={'triples':64,'passed':True}
    words2,q2=qs(2); words3,q3=qs(3)
    ca2,na2=classes(2); ca3,na3=classes(3)
    require((na2,na3)==(2,1), 'check failed at original line 163')
    p=sp.zeros(na2*4+4*na2,64)
    for j,(a,b,c) in enumerate(words3):
        p[4*ca2[(a,b)]+c,j]=1
        p[4*na2+a*na2+ca2[(b,c)],j]=1
    require(p*q3==sp.zeros(p.rows,q3.cols), 'check failed at original line 168')
    e=sp.ones(4,1); a=sp.Matrix([1,0,-1,0]); b=sp.Matrix([0,1,0,-1])
    tr=sp.kronecker_product(e,sp.kronecker_product(a,a)-sp.kronecker_product(b,b))
    ti=-sp.kronecker_product(e,sp.kronecker_product(a,b)+sp.kronecker_product(b,a))
    require(p*tr==sp.zeros(p.rows,1) and p*ti==sp.zeros(p.rows,1), 'check failed at original line 172')
    rq2=q2.rank(); rq3=q3.rank(); rk3=64-p.rank(); rext=q3.row_join(tr).row_join(ti).rank()
    require((rq2,rq3,rk3,rext)==(14,47,49,49), 'check failed at original line 174')
    out['rational_degree3']={'dim_A2':na2,'dim_A3':na3,'rank_QS2':rq2,'rank_QS3':rq3,'dim_K3':rk3,'rank_QS3_plus_two_witnesses':rext}
    # Degree-2 differential in weight 3: ambient domain is two copies of V^3,
    # target A2*V + V*V*V + V*A2, and C2 has B2 in the appropriate pair.
    d2=sp.zeros(8+64+8,128)
    for j,(a,b,c) in enumerate(words3):
        # theta word: a | bc | 1
        d2[4*ca2[(a,b)]+c,j]+=1
        d2[8+j,j]+=1
        # rho word: 1 | ab | c
        d2[8+j,64+j]+=1
        d2[8+64+a*2+ca2[(b,c)],64+j]+=1
    b2=q2.columnspace(); rb2=sp.Matrix.hstack(*b2)
    c2=sp.diag(sp.kronecker_product(sp.eye(4),rb2),sp.kronecker_product(rb2,sp.eye(4)))
    rankd2=(d2*c2).rank()
    for t in (tr,ti): require(d2*sp.Matrix.vstack(t,-t)==sp.zeros(80,1), 'check failed at original line 189')
    require(d2*sp.Matrix.vstack(q3,-q3)==sp.zeros(80,64), 'check failed at original line 190')
    require(rankd2==63 and 112-rankd2-rq3==2, 'check failed at original line 191')
    out['weight3_C_homology']={'dim_C2':112,'rank_d2':rankd2,'rank_d3':rq3,'dim_H2':2}
    # Exact Fourier 3-by-3 block; generated by braid lifts, not hard-coded.
    W=[(1,1,0),(1,0,1),(0,1,1)]
    mat=[[eig_qs(w).get(v,G()) for w in W] for v in W]
    ell=[G(0,1),G(1,1),G(1)]
    require(all(sum((ell[j]*mat[j][k] for j in range(3)),G())==0 for k in range(3)), 'check failed at original line 197')
    require(ell[2]==1, 'check failed at original line 198')
    out['Fourier_block']={'matrix_Qi_pairs':[[repr(v) for v in row] for row in mat],'annihilator_verified':True}
    count=0
    for n in range(7):
        for w in product(range(4),repeat=n):
            require(not apply(differential,differential(w)), 'check failed at original line 203')
            dhhd=add(apply(differential,homotopy(w)),apply(homotopy,differential(w)))
            expected={} if all(a==0 for a in w) else {w:G(1)}
            require(dhhd==expected, ('contraction',w,dhhd,expected))
            count+=1
    for n in range(2,7): require(not eig_qs((0,)*n), 'check failed at original line 208')
    chain_count=0
    for n in range(1,5):
        for w in product(range(4),repeat=n):
            require(apply(end_boundary,eig_qs(w))==apply(eig_qs,differential(w)), w)
            chain_count+=1
    out['constant_character_checks']={'contraction_words_degree0_through6':count,'chain_map_words_degree1_through4':chain_count,'pure_u0_QS_zero_degrees':[2,3,4,5,6]}
    out['limits']='Finite checks over Q and Q(i); no proof of arbitrary-degree or all-characteristic assertions by computation alone. See REPORT.md.'
    payload = json.dumps(out, indent=2) + '\n'
    if args.output is not None:
        args.output.write_text(payload, encoding='utf-8')
    print(payload, end='')


if __name__=='__main__': main()
