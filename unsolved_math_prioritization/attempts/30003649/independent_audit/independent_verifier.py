#!/usr/bin/env python3
"""Independent audit. Reads separately obtained, hash-pinned public witness data.

No source-package or authored-freeze checker is imported. Field elements use a
single positive denominator. Facets use recursively shared Laplace minors,
not elimination/nullspace code. The program emits verification metadata only.
"""
import argparse
import csv
from fractions import Fraction
import gzip
import hashlib
from itertools import combinations
import json
from math import gcd, lcm
from pathlib import Path
import sys
import time


def check(ok, message):
    if not ok:
        raise ValueError(message)


class Field:
    __slots__ = ('a', 'd')
    def __init__(self, value=0, denominator=1):
        if isinstance(value, Field):
            self.a, self.d = value.a, value.d
            return
        if isinstance(value, (tuple, list)):
            check(len(value) == 3, 'field shape')
            q = [Fraction(v) for v in value]
        else:
            q = [Fraction(value), Fraction(0), Fraction(0)]
        den = lcm(*(v.denominator for v in q)) * denominator
        nums = [int(v * (den // denominator)) for v in q]
        check(den != 0, 'zero denominator')
        if den < 0:
            den = -den; nums = [-v for v in nums]
        g = gcd(den, *nums)
        self.a = tuple(v // g for v in nums)
        self.d = den // g
    def __add__(self, other):
        other = Field(other)
        return Field([x * other.d + y * self.d for x, y in zip(self.a, other.a)], self.d * other.d)
    __radd__ = __add__
    def __neg__(self):
        return Field([-x for x in self.a], self.d)
    def __sub__(self, other):
        return self + (-Field(other))
    def __rsub__(self, other):
        return Field(other) - self
    def __mul__(self, other):
        other = Field(other)
        a,b,c = self.a; x,y,z = other.a
        return Field([a*x + 2*b*z + 2*c*y, a*y + b*x + 2*c*z, a*z + b*y + c*x], self.d * other.d)
    __rmul__ = __mul__
    def __eq__(self, other):
        other = Field(other)
        return self.a == other.a and self.d == other.d
    def interval(self, low, high):
        # Horner evaluation; full interval products, even across zero.
        lo = hi = Fraction(self.a[2], self.d)
        for c in [self.a[1], self.a[0]]:
            four = [lo*low, lo*high, hi*low, hi*high]
            lo, hi = min(four) + Fraction(c,self.d), max(four) + Fraction(c,self.d)
        return lo, hi
    def mod(self, prime):
        # p = 2 mod 3 gives a unique cube root. A nonzero image witnesses
        # nonzero characteristic-zero determinant; no converse is inferred.
        check(prime % 3 == 2 and self.d % prime, 'invalid modular specialization')
        root = pow(2, pow(3,-1,prime-1), prime)
        check(pow(root,3,prime)==2, 'modular root relation')
        return (self.a[0] + root*self.a[1] + root*root*self.a[2]) * pow(self.d,-1,prime) % prime


def tr(a):
    return [list(c) for c in zip(*a)]


def matrix(a, rows, cols, convert=Field):
    check(len(a) == rows and all(len(r) == cols for r in a), 'matrix dimensions')
    return [[convert(v) for v in r] for r in a]


def mul(a,b):
    check(a and b and len(a[0]) == len(b), 'matrix product dimensions')
    return [[sum(x*y for x,y in zip(r,c)) for c in tr(b)] for r in a]


def dot(a,b):
    check(len(a) == len(b), 'dot product dimensions')
    return sum(x*y for x,y in zip(a,b))


def full_rank(a, expected):
    p = 1000000007
    rows = [[Field(x).mod(p) for x in r] for r in a]
    pivots = 0
    for col in range(len(rows[0])):
        candidates = [i for i in range(pivots,len(rows)) if rows[i][col]]
        if not candidates: continue
        j = candidates[0]; rows[pivots],rows[j] = rows[j],rows[pivots]
        scale = pow(rows[pivots][col],-1,p)
        rows[pivots] = [x*scale % p for x in rows[pivots]]
        for i in range(pivots+1,len(rows)):
            scale = rows[i][col]
            rows[i] = [(x-scale*y)%p for x,y in zip(rows[i],rows[pivots])]
        pivots += 1
        if pivots == expected: return True
    return False


def primitive(v):
    q = [Fraction(x) for x in v]
    den = lcm(*(x.denominator for x in q))
    nums = tuple(int(x*den) for x in q)
    g = gcd(*nums)
    check(g > 0, 'zero primitive vector')
    return tuple(x//g for x in nums)


def seed_checks(seed, cone):
    alpha = Field([0,1,0]); v = [[Field(1)],[alpha],[alpha*alpha]]
    # Derive our own root interval by 192 steps of rational bisection.
    low, high = Fraction(1), Fraction(2)
    for _ in range(192):
        middle = (low+high)/2
        if middle**3 < 2: low = middle
        else: high = middle
    check(low**3 < 2 < high**3, 'root isolation')
    positive = lambda x: Field(x).interval(low,high)[0] > 0
    O = matrix(seed['orthogonal_matrix'],7,7)
    Q = matrix(seed['Q'],7,7); Qp = matrix(seed['Qprime'],7,7)
    I = [[int(i==j) for j in range(7)] for i in range(7)]
    check(mul(O,tr(O)) == I and mul(tr(O),O) == I,'orthogonality')
    check(Q == tr(Q) and Qp == tr(Qp),'symmetry')
    check(sum(Q[i][i] for i in range(7)) == 0,'trace zero')
    check(all(Qp[i][i] == 0 for i in range(7)),'conjugate diagonal')
    check(Q == mul(mul(O,Qp),tr(O)),'conjugation')
    B = [[[Fraction(O[i][j].a[k],O[i][j].d) for j in range(7)] for i in range(7)] for k in range(3)]
    supplied_B = [matrix(x,7,7) for x in seed['coefficient_matrices']]
    check(B == supplied_B,'coefficient expansion')
    S = matrix(seed['S'],7,7,int); T = matrix(seed['T'],7,7,int)
    check(all(S[i][j] == -S[j][i] and T[i][j] == -T[j][i] for i in range(7) for j in range(7)),'skew symmetry')
    omega = [[alpha*S[i][j]+alpha*alpha*T[i][j] for j in range(7)] for i in range(7)]
    check(mul([[I[i][j]+omega[i][j] for j in range(7)] for i in range(7)],O) == [[I[i][j]-omega[i][j] for j in range(7)] for i in range(7)],'Cayley identity')
    Cs = [[[B[k][i][j] for k in range(3)] for i in range(7)] for j in range(7)]
    for j,C in enumerate(Cs):
        check(full_rank(C,3),'irrational ray coefficient rank')
        H = mul(mul(tr(C),Q),C)
        check(H == matrix(seed['restricted_gram'][j],3,3),'restricted form consistency')
        check(mul(H,v) == [[0],[0],[0]],'local kernel')
        check(positive(H[0][0]),'local first minor')
        check(positive(H[0][0]*H[1][1]-H[1][0]*H[0][1]),'local second minor')
    # Additional source-definition checks not needed by the obstruction lemma.
    pairs = list(combinations(range(7),2))
    rows = []
    for k in range(2):
        M = mul(tr(O),B[k])
        check(all(sum(Qp[i][j]*M[j][i] for j in range(7)) == 0 for i in range(7)), 'defining seed linear equations')
        for i in range(7):
            rows.append([M[t][i] if s==i else M[s][i] if t==i else 0 for s,t in pairs[:14]])
    check(full_rank(rows,14),'seed unique determined entries')
    check(all(positive(Qp[i][j]) for i,j in pairs),'conjugate off diagonal signs')
    W = matrix(cone['coefficient_triangle'],3,3,Fraction)
    check(W[0] == [1,1,1] and full_rank(W,3),'triangle rank/first row')
    lam = [[Field(x)] for x in cone['barycentric_coefficients']]
    check(len(lam) == 3 and all(positive(x[0]) for x in lam),'barycentric positivity')
    check(mul(W,lam) == v,'basis ray in rational cone')
    blocks = [mul(C,W) for C in Cs]
    V = [[x for block in blocks for x in block[i]] for i in range(7)]
    check(V == matrix(cone['generators'],7,21,Fraction),'generator identity')
    columns = tr(V)
    h = [Fraction(x) for x in cone['positive_slice_functional']]
    check(len(h)==7 and all(dot(h,x)>0 for x in columns),'pointedness')
    QV = mul(Q,V); count=0
    for i,j in combinations(range(21),2):
        if i//3 != j//3:
            check(positive(dot(columns[i],[QV[k][j] for k in range(7)])),'strict cross pairing')
            count += 1
    check(count == 189,'cross count')
    return [primitive(x) for x in columns], O, (low,high)


def all_cofactors(P):
    """All 6-row null vectors from Laplace expansion of shared minors.

    At level k, cache determinants for every k-subset of the input rows and
    every k-subset of the seven coordinate columns. No rank oracle, floating
    point tolerance, Bareiss division, or supplied facet flag is used.
    """
    prev = {(): (1,)}; oldcols = [()]
    for k in range(1,7):
        cols = list(combinations(range(7),k)); loc = {c:i for i,c in enumerate(oldcols)}
        expansions = [[(loc[c[:j]+c[j+1:]],c[j],(-1)**(k-1+j)) for j in range(k)] for c in cols]
        nxt={}
        for rows in combinations(range(len(P)),k):
            prefix=prev[rows[:-1]]; last=P[rows[-1]]
            nxt[rows]=tuple(sum(sign*prefix[index]*last[col] for index,col,sign in terms) for terms in expansions)
        prev,oldcols=nxt,cols
    for rows, minors in prev.items():
        lookup={c:x for c,x in zip(oldcols,minors)}
        cofactor=tuple((-1)**j*lookup[tuple(k for k in range(7) if k!=j)] for j in range(7))
        yield rows,cofactor


def facet_checks(P, supplied, R):
    check(P == [tuple(x) for x in supplied['integer_generators']],'integer generator rays')
    found={}; candidates=deficient=nonsupporting=0
    for rows,normal in all_cofactors(P):
        candidates += 1
        if not any(normal): deficient += 1; continue
        check(all(dot(normal,P[i])==0 for i in rows),'cofactor orthogonality')
        normal=primitive(normal); values=[dot(normal,x) for x in P]
        if min(values)<0 and max(values)>0: nonsupporting += 1; continue
        check(any(values),'cone full dimension')
        if min(values)<0:
            normal=tuple(-x for x in normal); values=[-x for x in values]
        found[normal]=tuple(i for i,x in enumerate(values) if not x)
    ordered=sorted(found,key=lambda x:(found[x],x))
    check(candidates==54264 and deficient==0 and len(ordered)==444,'complete facet counts')
    check(all(len(x)==6 for x in found.values()),'simplicial facets')
    check(ordered==[tuple(x) for x in supplied['facet_normals']],'complete facet normals')
    check([found[x] for x in ordered]==[tuple(x) for x in supplied['facets']],'facet incidences')
    check(ordered==R and full_rank(R,7),'facet matrix and rational rank')
    return {'candidate_supports':candidates,'deficient_supports':deficient,'nonsupporting_supports':nonsupporting,'facets':len(found),'rank':7}


def factor_checks(R,O,interval):
    factor=mul(R,O); counts=[0,0]
    for row in factor:
        for x in row:
            if x==0: counts[1]+=1
            else:
                check(x.interval(*interval)[0]>0,'factor sign')
                counts[0]+=1
    check(counts==[2966,142],'factor sign counts')
    return counts


def gram_checks(data,R):
    seen=set();largest=0
    with gzip.open(data/'A_integer.mtx.gz','rt') as f:
        check(next(f).strip()=='%%MatrixMarket matrix coordinate integer symmetric','matrix format')
        lines=(x for x in f if x.strip() and not x.startswith('%'))
        check(list(map(int,next(lines).split()))==[444,444,98790],'Gram dimensions')
        for line in lines:
            i,j,value=map(int,line.split());i-=1;j-=1
            check(0<=j<=i<444 and (i,j) not in seen,'Gram unique index')
            seen.add((i,j));check(value==dot(R[i],R[j]) and value>0,'Gram equality and positivity')
            largest=max(largest,len(str(value)))
    check(len(seen)==98790,'Gram completeness')
    return {'stored_entries':len(seen),'maximum_decimal_digits':largest}


def load(data):
    pins=json.loads(Path(__file__).with_name('input_pins.json').read_text())
    for item in pins['files']:
        blob=(data/item['name']).read_bytes()
        check(len(blob)==item['bytes'] and hashlib.sha256(blob).hexdigest()==item['sha256'],'pinned input mismatch: '+item['name'])
    seed=json.loads((data/'exact_algebraic_certificate.json').read_text())
    cone=json.loads((data/'rational_cone_certificate.json').read_text())
    facets=json.loads((data/'facets.json').read_text())
    with (data/'R_integer.csv').open() as f:R=[tuple(map(int,x)) for x in csv.reader(f)]
    return seed,cone,facets,R


def run(data):
    started=time.monotonic();seed,cone,facets,R=load(data)
    P,O,interval=seed_checks(seed,cone)
    print('Independent field, local PSD, ray, and cross-pair predicates PASS',file=sys.stderr,flush=True)
    result=facet_checks(P,facets,R)
    print('Independent Laplace-minor exhaustive facets PASS',file=sys.stderr,flush=True)
    signs=factor_checks(R,O,interval);gram=gram_checks(data,R)
    return {'status':'PASS','method':'common-denominator cubic arithmetic, independent bisection, shared Laplace cofactors, modular nonzero-rank witnesses','field_and_cone':{'local_forms':7,'cross_pairings':189,'defining_equation_rank':14,'root_bisection_steps':192},'facets':result,'factor_positive_entries':signs[0],'factor_zero_entries':signs[1],'integer_Gram':gram,'elapsed_seconds':round(time.monotonic()-started,3)}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('data',type=Path)
    args=parser.parse_args();print(json.dumps(run(args.data),sort_keys=True,indent=2))
