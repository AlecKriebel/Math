#!/usr/bin/env python3
"""Independent, standard-library checker for Holden's public PF-03 data.

No source code is imported or executed from the inspected publication. The
data directory is an explicit command-line input, deliberately not bundled.
All mathematical decisions use integers and fractions. Output contains only
verification metadata, never downloaded datasets or source text.
"""
import argparse
import csv
from fractions import Fraction as F
from functools import reduce
from itertools import combinations
import gzip
import hashlib
import json
from math import gcd, lcm
from pathlib import Path
import sys
import time


def require(condition, message):
    if not condition:
        raise ValueError(message)


class Cubic:
    """Q[t]/(t^3-2), represented in the basis 1,t,t^2."""
    def __init__(self, x=0):
        if isinstance(x, Cubic):
            self.c = x.c
        elif isinstance(x, (list, tuple)):
            require(len(x) == 3, 'field element must have three coefficients')
            self.c = tuple(map(F, x))
        else:
            self.c = (F(x), F(0), F(0))

    def __add__(self, other):
        b = Cubic(other)
        return Cubic([x+y for x,y in zip(self.c,b.c)])
    __radd__ = __add__

    def __neg__(self):
        return Cubic([-x for x in self.c])

    def __sub__(self, other):
        return self + (-Cubic(other))

    def __rsub__(self, other):
        return Cubic(other) + (-self)

    def __mul__(self, other):
        b = Cubic(other)
        p = [F(0)]*5
        for i in range(3):
            for j in range(3):
                p[i+j] += self.c[i]*b.c[j]
        for k in (4,3):
            p[k-3] += 2*p[k]
        return Cubic(p[:3])
    __rmul__ = __mul__

    def __eq__(self, other):
        return self.c == Cubic(other).c

    def bounds(self, lo, hi):
        result = [self.c[0], self.c[0]]
        for coefficient, left, right in zip(self.c[1:], (lo,lo*lo), (hi,hi*hi)):
            terms = (coefficient*left, coefficient*right)
            result[0] += min(terms)
            result[1] += max(terms)
        return tuple(result)


def transpose(a):
    return list(map(list,zip(*a)))


def mm(a,b):
    bt=transpose(b)
    return [[sum(x*y for x,y in zip(row,col)) for col in bt] for row in a]


def ident(n):
    return [[int(i==j) for j in range(n)] for i in range(n)]


def mat(a):
    return [[Cubic(x) for x in row] for row in a]


def rank(a):
    b=[list(map(F,row)) for row in a]
    i=0
    for j in range(len(b[0])):
        p=next((k for k in range(i,len(b)) if b[k][j]),None)
        if p is None:
            continue
        b[i],b[p]=b[p],b[i]
        pivot=b[i][j]
        b[i]=[x/pivot for x in b[i]]
        for k in range(i+1,len(b)):
            c=b[k][j]
            if c:
                b[k]=[x-c*y for x,y in zip(b[k],b[i])]
        i+=1
        if i==len(b):
            break
    return i


def primitive(v):
    d=lcm(*(x.denominator for x in v))
    ints=[int(x*d) for x in v]
    g=reduce(gcd,map(abs,ints),0)
    require(g>0,'zero generator or normal')
    return tuple(x//g for x in ints)


def null6(rows):
    """Fraction-free Gaussian elimination, then rational back substitution.

    Returns None at deficient rank, otherwise a primitive integer null vector.
    Column permutations are tracked. Every Bareiss division is verified.
    """
    a=[list(row) for row in rows]
    perm=list(range(7)); previous=1
    for k in range(6):
        hit=next(((i,j) for i in range(k,6) for j in range(k,7) if a[i][j]),None)
        if hit is None:
            return None
        i,j=hit
        a[k],a[i]=a[i],a[k]
        if j!=k:
            for row in a:
                row[k],row[j]=row[j],row[k]
            perm[k],perm[j]=perm[j],perm[k]
        pivot=a[k][k]
        for i in range(k+1,6):
            entry=a[i][k]
            for j in range(k+1,7):
                numerator=pivot*a[i][j]-entry*a[k][j]
                quotient,remainder=divmod(numerator,previous)
                require(remainder==0,'non-exact Bareiss division')
                a[i][j]=quotient
            a[i][k]=0
        previous=pivot
    x=[F(0)]*7; x[6]=F(1)
    for i in range(5,-1,-1):
        x[i]=-sum(a[i][j]*x[j] for j in range(i+1,7))/a[i][i]
    y=[F(0)]*7
    for i in range(7):
        y[perm[i]]=x[i]
    z=primitive(y)
    require(all(sum(x*y for x,y in zip(row,z))==0 for row in rows),'null vector incorrect')
    return z


def verify(data, progress=False):
    def stage(s):
        if progress:
            print(s,file=sys.stderr,flush=True)
    begin=time.monotonic()
    source_files=['exact_algebraic_certificate.json','rational_cone_certificate.json','facets.json','R_integer.csv','A_integer.mtx.gz']
    hashes={p:{'sha256':hashlib.sha256((data/p).read_bytes()).hexdigest(),'bytes':(data/p).stat().st_size} for p in source_files}
    seed=json.loads((data/source_files[0]).read_text())
    cone=json.loads((data/source_files[1]).read_text())
    facets=json.loads((data/source_files[2]).read_text())
    lo,hi=map(F,cone['isolation_interval'])
    require(0<lo<hi and lo**3<2<hi**3,'invalid real-root isolation')
    alpha=Cubic([0,1,0]); alpha2=alpha*alpha
    require(alpha2*alpha==2,'field multiplication failed')
    O=mat(seed['orthogonal_matrix']); Q=mat(seed['Q']); Qp=mat(seed['Qprime'])
    require(len(O)==7 and all(len(row)==7 for row in O),'wrong orthogonal matrix shape')
    I=ident(7)
    require(mm(O,transpose(O))==I and mm(transpose(O),O)==I,'orthogonality failed')
    require(Q==transpose(Q) and Qp==transpose(Qp),'symmetry failed')
    require(sum(Q[i][i] for i in range(7))==0,'trace is not zero')
    require(all(Qp[i][i]==0 for i in range(7)),'Qprime diagonal is not zero')
    require(Q==mm(mm(O,Qp),transpose(O)),'Q conjugation failed')
    S=seed['S'];T=seed['T']
    require(all(S[i][j]==-S[j][i] and T[i][j]==-T[j][i] for i in range(7) for j in range(7)),'seed skew symmetry')
    omega=[[alpha*S[i][j]+alpha2*T[i][j] for j in range(7)] for i in range(7)]
    plus=[[omega[i][j]+I[i][j] for j in range(7)] for i in range(7)]
    minus=[[-omega[i][j]+I[i][j] for j in range(7)] for i in range(7)]
    require(mm(plus,O)==minus,'Cayley definition failed')
    B=[]
    for k in range(3):
        B.append([[O[i][j].c[k] for j in range(7)] for i in range(7)])
    require([mat(b) for b in B]==[mat(b) for b in seed['coefficient_matrices']],'coefficient matrices disagree')
    Cs=[[[B[k][i][j] for k in range(3)] for i in range(7)] for j in range(7)]
    v=[[Cubic(1)],[alpha],[alpha2]]
    minor_bounds=[]
    for i,C in enumerate(Cs):
        require(rank(C)==3,'coefficient rank does not exclude rational rays')
        H=mm(mm(transpose(C),Q),C)
        require(H==mat(seed['restricted_gram'][i]),'restricted form mismatch')
        require(mm(H,v)==[[0],[0],[0]],'local kernel failed')
        d=H[0][0]*H[1][1]-H[0][1]*H[1][0]
        low1=H[0][0].bounds(lo,hi)[0];low2=d.bounds(lo,hi)[0]
        require(low1>0 and low2>0,'local positive definiteness failed')
        minor_bounds.append([str(low1),str(low2)])
    W=[[F(x) for x in row] for row in cone['coefficient_triangle']]
    require(rank(W)==3 and W[0]==[1,1,1],'triangle invalid')
    lam=[[Cubic(x)] for x in cone['barycentric_coefficients']]
    require(mm(W,lam)==v,'barycentric inclusion identity failed')
    require(all(x[0].bounds(lo,hi)[0]>0 for x in lam),'barycentric inclusion sign failed')
    blocks=[mm(C,W) for C in Cs]
    V=[[x for block in blocks for x in block[i]] for i in range(7)]
    require(V==[[F(x) for x in row] for row in cone['generators']],'rational generators mismatch')
    h=list(map(F,cone['positive_slice_functional']))
    require(all(sum(x*y for x,y in zip(h,p))>0 for p in transpose(V)),'pointedness functional failed')
    pairing=mm(mm(transpose(V),Q),V)
    lows=[]
    for i,j in combinations(range(21),2):
        if i//3!=j//3:
            low=pairing[i][j].bounds(lo,hi)[0]
            require(low>0,'cross-block pairing not positive')
            lows.append(low)
    require(len(lows)==189,'cross-pair count')
    stage('PASS: exact cubic-field identities, irrational rays, local PSD and cross positivity')
    P=[primitive(p) for p in transpose(V)]
    require(P==[tuple(p) for p in facets['integer_generators']],'primitive generators mismatch')
    found={};deficient=0;rejected=0;total=0
    for subset in combinations(range(21),6):
        total+=1
        r=null6([P[j] for j in subset])
        if r is None:
            deficient+=1;continue
        dots=[sum(a*b for a,b in zip(r,p)) for p in P]
        if all(x<=0 for x in dots):
            r=tuple(-x for x in r);dots=[-x for x in dots]
        if not all(x>=0 for x in dots):
            rejected+=1;continue
        found[r]=tuple(i for i,d in enumerate(dots) if d==0)
    R=sorted(found,key=lambda r:(found[r],r))
    require(len(R)==444 and total==54264 and deficient==0,'facet enumeration counts differ')
    require(all(len(v)==6 for v in found.values()),'facet incidence count differs')
    require(R==[tuple(row) for row in facets['facet_normals']],'full facet set or order differs')
    require([found[r] for r in R]==[tuple(v) for v in facets['facets']],'facet incidence file differs')
    csvrows=[tuple(map(int,row)) for row in csv.reader((data/'R_integer.csv').open())]
    require(R==csvrows and rank(R)==7,'matrix R mismatch or deficient rank')
    stage('PASS: all 54,264 candidate supports, 444 exact facets and rational rank seven')
    nonnegative=mm(R,O);positive=0;zeros=0
    for row in nonnegative:
        for value in row:
            if value==0:
                zeros+=1
            else:
                require(value.bounds(lo,hi)[0]>0,'real factor nonnegativity failed')
                positive+=1
    entries=0;maxdigits=0;seen=set()
    with gzip.open(data/'A_integer.mtx.gz','rt') as f:
        require(next(f).strip()=='%%MatrixMarket matrix coordinate integer symmetric','matrix format')
        lines=(line for line in f if line.strip() and not line.startswith('%'))
        require(list(map(int,next(lines).split()))==[444,444,98790],'matrix dimensions')
        for line in lines:
            i,j,value=map(int,line.split()); i-=1;j-=1
            require(0<=j<=i<444 and (i,j) not in seen,'matrix indexing')
            seen.add((i,j))
            require(value==sum(x*y for x,y in zip(R[i],R[j])) and value>0,'expanded Gram entry incorrect')
            entries+=1;maxdigits=max(maxdigits,len(str(value)))
    require(entries==98790,'matrix entry count')
    stage('PASS: real factor, all 98,790 integer Gram entries and strict entry positivity')
    return {'status':'PASS','checker':'independently authored; no third-party code execution',
            'field':'Q[t]/(t^3-2), positive real root','order':444,'rank':7,'real_cp_rank':7,
            'local_psd_forms':7,'cross_block_sign_checks':189,'candidate_facet_supports':total,
            'rank_deficient_supports':deficient,'non_supporting_supports':rejected,'facets':len(R),
            'real_factor_positive_entries':positive,'real_factor_zero_entries':zeros,
            'matrix_entries_checked':entries,'largest_entry_decimal_digits':maxdigits,
            'all_local_principal_minor_lower_bounds_positive':True,
            'all_cross_pairing_lower_bounds_exceed_17_over_1000':min(lows)>F(17,1000),
            'input_metadata':hashes,'elapsed_seconds':round(time.monotonic()-begin,3)}


def selftest():
    a=Cubic([0,1,0]);require(a*a*a==2,'cubic relation')
    require((a+1)*(a*a-a+1)==3,'cubic unit identity')
    base=[[int(i==j) for j in range(7)] for i in range(6)]
    require(null6(base)==(0,0,0,0,0,0,1),'nullspace base')
    base[0]=[0,0,0,0,0,0,1]
    require(null6(base)==(1,0,0,0,0,0,0),'nullspace column pivot')
    base[1]=base[0]
    require(null6(base) is None,'nullspace deficient control')
    try:
        require(False,'deliberate rejection')
    except ValueError:
        pass
    else:
        raise RuntimeError('negative control failed')
    return {'status':'PASS','arithmetic_and_rejection_controls':6}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('data',type=Path,nargs='?')
    p.add_argument('--selftest',action='store_true')
    args=p.parse_args()
    if args.selftest:
        print(json.dumps(selftest(),indent=2))
    else:
        require(args.data is not None,'supply the separately retrieved public data directory')
        print(json.dumps(verify(args.data,progress=True),indent=2,sort_keys=True))
