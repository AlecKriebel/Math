"""Fresh exact controls written for geometry_rigidity_01; standard library only.
No inherited checker, historical activity counts or executable is replayed.
Polynomial identities over Q[u] are supporting evidence, not the general proof.
"""
from fractions import Fraction as Q
from itertools import product
import json

class P:
    def __init__(self, x=0):
        if isinstance(x,P): self.c=x.c
        elif isinstance(x,tuple): self.c=tuple(Q(v) for v in x)
        else: self.c=(Q(x),)
        while len(self.c)>1 and not self.c[-1]: self.c=self.c[:-1]
    def __add__(self,x):
        x=P(x); n=max(len(self.c),len(x.c))
        return P(tuple((self.c[i] if i<len(self.c) else 0)+(x.c[i] if i<len(x.c) else 0) for i in range(n)))
    __radd__=__add__
    def __neg__(self):return P(tuple(-v for v in self.c))
    def __sub__(self,x):return self+-P(x)
    def __rsub__(self,x):return P(x)+-self
    def __mul__(self,x):
        x=P(x);c=[Q(0)]*(len(self.c)+len(x.c)-1)
        for i,a in enumerate(self.c):
            for j,b in enumerate(x.c):c[i+j]+=a*b
        return P(tuple(c))
    __rmul__=__mul__
    def d(self):return P(tuple(i*v for i,v in enumerate(self.c) if i) or (0,))
    def at(self,u):return sum(v*Q(u)**i for i,v in enumerate(self.c))
    def __eq__(self,x):return self.c==P(x).c
    def __repr__(self):return str([str(v) for v in self.c])

u=P((0,1));zero=P(0)
def mat(r,c):return [[P(0) for j in range(c)] for i in range(r)]
def clone(M):return [[P(x) for x in row] for row in M]
def diff(M):return [[P(x).d() for x in row] for row in M]
def mul(A,B):return [[sum((A[i][k]*B[k][j] for k in range(len(B))),P(0)) for j in range(len(B[0]) if B else 0)] for i in range(len(A))]
def mv(A,v):return [sum((a*b for a,b in zip(row,v)),P(0)) for row in A]
def vsub(a,b):return [x-y for x,y in zip(a,b)]
def bracket(a,b):return [a[-1]*x.d()-b[-1]*y.d() for x,y in zip(b,a)]
def torsion(L):
    n=len(L);E=[[P(i==j) for i in range(n)] for j in range(n)];LE=[[L[i][j] for i in range(n)] for j in range(n)]
    return {(i,j):vsub(vsub(bracket(LE[i],LE[j]),mv(L,bracket(LE[i],E[j]))),mv(L,bracket(E[i],LE[j]))) for i in range(n) for j in range(i+1,n)}
def big(A,b,lam):
    n=len(A)+1;L=mat(n,n)
    for i,row in enumerate(A):L[i][:-1]=row;L[i][-1]=b[i]
    L[-1][-1]=lam
    return L
def residual(A,lam):
    B=clone(A)
    for i in range(len(A)):B[i][i]-=lam
    return mul(B,diff(A))
def iszero(M):return all(x==0 for row in M for x in row)
def value(L,t):return [[x.at(t) for x in row] for row in L]
def comps(n):
    if n==0:yield ()
    for k in range(1,n+1):
        for tail in comps(n-k):yield (k,)+tail

def stages(sizes, mus):
    n=sum(sizes);J=mat(n,n);off=0
    for size,mu in zip(sizes,mus):
        for i in range(size):J[off+i][off+i]=P(mu)
        for i in range(size-1):J[off+i][off+i+1]=P(1)
        off+=size
    A=[row[:-1] for row in J[:-1]];b=[row[-1] for row in J[:-1]];lam=J[-1][-1]
    prev=value(J,0)
    def emit(AA,bb,ll):
        nonlocal A,b,lam,prev
        L=big(AA,bb,ll)
        assert value(L,0)==prev
        assert iszero(residual(AA,ll))
        prev=value(L,1); A=[[P(x.at(1)) for x in row] for row in AA];b=[P(x.at(1)) for x in bb];lam=P(ll.at(1))
        return L
    yield emit(A,[x*(1-u) for x in b],lam)
    angular_sizes=list(sizes); angular_sizes[-1]-=1
    off=0
    for size,mu in zip(angular_sizes,mus):
        if not size:continue
        yield emit(A,b,lam+(P(mu)-lam)*u)
        for j in range(size-1):
            AA=clone(A);AA[off+j][off+j+1]=1-u
            yield emit(AA,b,lam)
        AA=clone(A)
        for i in range(size):AA[off+i][off+i]=P(mu)*(1-u)
        yield emit(AA,b,P(mu)*(1-u))
        off+=size
    if not A:yield emit(A,b,lam*(1-u))
    assert all(x==0 for row in prev for x in row)

counts={'compositions':0,'stages':0,'direct_bracket_stages':0,'arbitrary_polynomial_identity_cases':0}
for n in range(1,8):
    for sizes in comps(n):
        mus=[(Q(-3,2),Q(0),Q(5,7))[i%3] for i in range(len(sizes))]
        for L in stages(sizes,mus):
            counts['stages']+=1
            if n<=4:
                assert all(all(x==0 for x in v) for v in torsion(L).values())
                counts['direct_bracket_stages']+=1
        counts['compositions']+=1
for sizes,mus in [((5,3,1,1),(Q(0),Q(0),Q(-3,2),Q(-3,2))),((1,1,1,1,1,1,1,1),(Q(0),)*8),((8,), (Q(5,7),))]:
    for L in stages(sizes,mus):counts['stages']+=1
    counts['compositions']+=1

# Arbitrary polynomial coefficients, including independently nonzero b', lambda'.
for m in range(1,6):
    A=[[P((Q((i+1)*(j+2)),Q(i-j),Q(i+j+1))) for j in range(m)] for i in range(m)]
    b=[P((Q(i+1),Q(-2*i-3),Q(7-i),Q(i+2))) for i in range(m)]
    lam=P((Q(-7),Q(3),Q(-2)))
    L=big(A,b,lam);N=torsion(L);R=residual(A,lam)
    for i in range(m):assert N[(i,m)]==[R[k][i] for k in range(m)]+[P(0)]
    for i in range(m):
        for j in range(i+1,m):assert all(x==0 for x in N[(i,j)])
    counts['arbitrary_polynomial_identity_cases']+=1

neg={}
A=mat(3,3);A[0][1]=1;A[1][2]=1-u
neg['reversed_arrow_deletion']=not iszero(residual(A,P(0)))
A=mat(2,2);A[0][0]=u
neg['raw_cutoff_distinct_real_eigenvalues']=not iszero(residual(A,2*u))
A=mat(3,3);A[0][1]=u;A[1][2]=u
neg['raw_cutoff_nilpotent_length_three']=not iszero(residual(A,P(0)))
A=mat(1,1);A[0][0]=1-u
neg['unmatched_scalar_drift']=not iszero(residual(A,P(2)))
assert all(neg.values())
print(json.dumps({'result':'PASS','arithmetic':'Exact Fraction-coefficient polynomials Q[u]','counts':counts,'negative_controls_detected':neg,'scope':'New supporting finite checks only; no historical checker or output used'},indent=2))
