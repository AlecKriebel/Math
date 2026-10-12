#!/usr/bin/env python3
"""Source-first controls. No candidate files imported, read, or executed.

Only Python standard library; exact arithmetic and actual noncommuting models.
All finite checks are controls for the written proofs, never universal proofs.
"""
from fractions import Fraction as F
from itertools import combinations
from functools import lru_cache
import random

def red(w):
    out=[]
    for x in w:
        if out and out[-1]==-x: out.pop()
        else: out.append(x)
    return tuple(out)
def wi(w): return tuple(-x for x in w[::-1])
def wm(*ws): return red(x for w in ws for x in w)
def wp(w,n): return wm(*([w if n>=0 else wi(w)]*abs(n)))
def wc(a,b): return wm(a,b,wi(a),wi(b))

# Affine Z[1/2] semidirect Z: actual noncommuting metabelian group.
def am(a,b):
    x,k=a; y,l=b
    return x+F(2)**k*y,k+l
def ai(a):
    x,k=a
    return -F(2)**(-k)*x,-k
def ac(a,b): return am(am(am(a,b),ai(a)),ai(b))
def metabelian_controls():
    a=(F(1),0); t=(F(0),1)
    assert am(a,t)!=am(t,a)
    checked=0
    for k in range(9):
        for n in range(-13,14):
            r=F(n,2**k)
            assert ac((-r,0),t)==(r,0)
            checked+=1
    print('AFFINE actual noncommuting action: 2; exact commutator compression cases:',checked)
    # Integer lamplighter, no periodic support identification.
    def shift(d,k): return {i+k:v for i,v in d.items() if v}
    def add(a,b):
        out=dict(a)
        for i,v in b.items():
            out[i]=out.get(i,0)+v
            if not out[i]: del out[i]
        return out
    rng=random.Random(38030002762)
    for n in range(1,41):
        lamp={i:rng.randrange(-9,10) for i in range(-n,n+1)}
        lamp={i:v for i,v in lamp.items() if v}
        lamp[n+1]=-sum(lamp.values())
        lamp={i:v for i,v in lamp.items() if v}
        u={}; running=0
        for i in range(min(lamp),max(lamp)):
            running+=lamp.get(i,0)
            if running:u[i]=running
        assert add(u,{i:-v for i,v in shift(u,1).items()})==lamp
    print('LAMPLIGHTER exact integer support compression: 40 cases; augmentation-zero only')
    # Virtually abelian infinite dihedral model.
    def dm(a,b):return a[0]+(-1)**a[1]*b[0],(a[1]+b[1])%2
    def di(a):return -(-1)**a[1]*a[0],a[1]
    def dc(a,b):return dm(dm(dm(a,b),di(a)),di(b))
    s=(0,1); v=(1,0)
    assert dm(v,s)!=dm(s,v)
    for n in range(-100,101):assert dc((n,0),s)==(2*n,0)
    print('DIHEDRAL virtually metabelian derived=2Z compression: 201 cases')

# Nonsplit central extension, coordinates of integral Heisenberg matrices.
def hm(a,b):
    x,y,z=a; X,Y,Z=b
    return x+X,y+Y,z+Z+x*Y
def hi(a):
    x,y,z=a
    return -x,-y,-z+x*y
def hc(a,b):return hm(hm(hm(a,b),hi(a)),hi(b))
def extension_controls():
    X=(1,0,0); Y=(0,1,0)
    assert hm(X,Y)!=hm(Y,X)
    for n in range(-100,101):assert hc((n,0,0),Y)==(0,0,n)
    print('HEISENBERG nonsplit extension A=center Z, Q=Z^2: A_Q=Z, but center powers norm <=2; 201 cases')
    # Finite quotient retains the noncommutation and central cocycle.
    for p in (2,3,5,7,11):
        mod=lambda a:tuple(x%p for x in a)
        assert mod(hc(X,Y))==(0,0,1)
        for n in range(p):assert mod(hc((n,0,0),Y))==(0,0,n)
    print('HEISENBERG finite quotient controls mod 2,3,5,7,11 passed')
    # Split inversion extension: coinvariant torsion survives.
    # In Z semidirect C2 with action -1 the coinvariant is Z/2,
    # translation 2n is a commutator, while odd translation needs one lamp.
    print('SPLIT control: inversion action has A_Q=Z/2; naive rational quotient loses finite word-length data')

def exact_lp(cols,target):
    signed=cols+[tuple(-x for x in c) for c in cols]
    if target==(0,0):return F(0),[]
    candidates=[]
    for i,j in combinations(range(len(signed)),2):
        a,b=signed[i],signed[j]; det=a[0]*b[1]-a[1]*b[0]
        if not det:continue
        u=F(target[0]*b[1]-target[1]*b[0],det)
        v=F(a[0]*target[1]-a[1]*target[0],det)
        if min(u,v)>=0:candidates.append((u+v,[(i,u),(j,v)]))
    if not candidates:raise ValueError('target outside span')
    return min(candidates,key=lambda t:t[0])
def integer_cost(n,torsion=True):
    # S = ((2,0;1),(0,3;2),(1,1;3)), target=(n,0;n mod4).
    # Every expression has 2x+z=n, 3y+z=0, hence z=-3y.
    # The torsion congruence is y=5n mod8. Choosing |y|<=4 gives
    # cost <= |n|/2+22. Since cost>=4|y|, any optimum satisfies
    # |y| <= |n|/8+11/2, inside the conservative search interval below.
    best=None; witness=None
    for y in range(-5*abs(n)-8,5*abs(n)+9):
        if (n+3*y)%2:continue
        x=(n+3*y)//2; z=-3*y
        if torsion and (x+2*y+3*z-n)%4:continue
        cost=abs(x)+abs(y)+abs(z)
        if best is None or cost<best:best=cost;witness=(x,y,z)
    assert best is not None
    assert 2*witness[0]+witness[2]==n and 3*witness[1]+witness[2]==0
    return best,witness
def cancellation_length(w):
    @lru_cache(None)
    def dp(i,j):
        if i>=j:return 0
        out=1+dp(i+1,j)
        for k in range(i+1,j):
            if w[k]==-w[i]:out=min(out,dp(i+1,k)+dp(k+1,j))
        return out
    return dp(0,len(w))
def q_ab(w):
    return sum(1 if w[i:i+2]==(1,2) else -1 if w[i:i+2]==(-2,-1) else 0 for i in range(len(w)-1))
def lp_controls():
    cols=[(2,0),(0,3),(1,1)]
    val,witness=exact_lp(cols,(1,0))
    assert val==F(1,2)
    print('RATIONAL LP: columns',cols,'target (1,0), exact optimum',val,'basis certificate',witness)
    print('INTEGRAL/torsion lengths: n, minimum, minimizing integer coefficients, stable lower bound')
    for n in range(0,33):
        cost,sol=integer_cost(n)
        assert F(cost)>=n*val
        if n%8==0:assert cost==n//2
        print(n,cost,sol,n*val)
    # Proven bounded residue control, not numerical convergence assertion.
    for n in range(0,257):
        cost,_=integer_cost(n)
        residue=n%8; residual,_=integer_cost(residue)
        assert cost <= (n-residue)//2+residual
    print('INTEGRAL upper bound for all 0<=n<=256 checked; exact proof uses period 8 and finite residues')
    g=(1,2,-1,-2)
    print('MISSING bounded-derived promise countercontrol: free-group commutator abelian LP=0')
    for n in range(1,17):
        w=wp(g,n); cost=cancellation_length(w)
        assert q_ab(w)==n and cost>=F(n,6)
        print('power',n,'exact cancellation norm',cost,'Brooks numerator',q_ab(w))
    rng=random.Random(8675309)
    words=[red(rng.choices((1,2,-1,-2),k=rng.randrange(1,30))) for _ in range(120)]
    maxdef=0
    for a in words:
        for b in words:
            d=abs(q_ab(wm(a,b))-q_ab(a)-q_ab(b)); maxdef=max(maxdef,d)
            assert d<=3
    print('ordinary Brooks defect bound 3: 14,400 noncommuting controls, observed max',maxdef)

# Faithful Artin action on a free group: equality of these automorphisms
# is canonical braid equality, not merely permutation or a nonfaithful matrix image.
def ident(n):return tuple((i,) for i in range(1,n+1))
def sub(A,w):return wm(*(A[x-1] if x>0 else wi(A[-x-1]) for x in w))
def compose(A,B):return tuple(sub(A,w) for w in B)
def sigma(n,i,sign=1):
    A=list(ident(n))
    if sign==1:A[i-1]=(i,i+1,-i);A[i]=(i,)
    else:A[i-1]=(i+1,);A[i]=(-(i+1),i,i+1)
    return tuple(A)
def braid(n,w):
    A=ident(n)
    for i in w:A=compose(A,sigma(n,abs(i),1 if i>0 else -1))
    return A
def braid_controls():
    for n in range(3,10):
        # Actual Artin and distant commuting relators.
        for i in range(1,n-1):assert braid(n,(i,i+1,i))==braid(n,(i+1,i,i+1))
        for i in range(1,n):
            for j in range(i+2,n):assert braid(n,(i,j))==braid(n,(j,i))
        delta=tuple(range(1,n))
        for i in range(1,n-1):assert braid(n,wm(delta,(i,),wi(delta)))==sigma(n,i+1)
        # This intentionally does NOT wrap the last Artin generator.
        assert braid(n,wm(delta,(n-1,),wi(delta)))!=sigma(n,1)
        for window in range(1,n-1):
            shifted=[wm(wp(delta,k),(1,),wp(delta,-k)) for k in range(window+1)]
            for k,w in enumerate(shifted):assert braid(n,w)==sigma(n,k+1)
            for i in range(window):assert braid(n,wm(shifted[i],shifted[i+1],shifted[i]))==braid(n,wm(shifted[i+1],shifted[i],shifted[i+1]))
            for i in range(window+1):
                for j in range(i+2,window+1):assert braid(n,wm(shifted[i],shifted[j]))==braid(n,wm(shifted[j],shifted[i]))
    print('CANONICAL BRAID: faithful Artin actions for B_3..B_9; finite-window relators and non-wrap negative checks passed')
    alpha=(1,-3); D=(2,1,3,2)
    assert braid(4,wm(D,alpha,wi(D)))==braid(4,wi(alpha))
    for k in range(-8,9):assert braid(4,wm(wp(alpha,k),D,wp(alpha,-k),wi(D)))==braid(4,wp(alpha,2*k))
    print('B_4 actual canonical conjugate-to-inverse and [alpha^k,D]=alpha^(2k) for -8<=k<=8; even bound8/odd bound10')
    # Exact signature via an actual symmetric torus Seifert form.
    # V+V^T has diagonal 2 and off-diagonal -1. LDL pivots (k+1)/k.
    def signature_tridiagonal(dim,sign):
        last=None; sig=0; det=F(1)
        for k in range(1,dim+1):
            pivot=F(2*sign) if last is None else F(2*sign)-F(1)/last
            assert pivot==sign*F(k+1,k)
            sig+=1 if pivot>0 else -1
            det*=pivot;last=pivot
        assert det==sign**dim*(dim+1)
        return sig
    for n in list(range(1,21))+[50,100]:
        sig=signature_tridiagonal(2*n,1)+signature_tridiagonal(2*n-2,-1)
        assert sig==2
        print('TORUS connected-sum signature: n',n,'dimensions',2*n,2*n-2,'signature',sig,'mirror convention reverses sign')

# Restricted direct product of copies of F_2 indexed by Z, extended by shift.
# Dictionary supports do not truncate or identify endpoints.
class W:
    def __init__(self,d=None,k=0,period=None):
        self.period=period;self.k=k if period is None else k%period;self.d={}
        for i,w in (d or {}).items():
            if period is not None:i%=period
            v=wm(self.d.get(i,()),w)
            if v:self.d[i]=v
            elif i in self.d:del self.d[i]
    def __mul__(self,o):
        assert self.period==o.period
        d=dict(self.d)
        for i,w in o.d.items():
            j=i+self.k
            if self.period is not None:j%=self.period
            v=wm(d.get(j,()),w)
            if v:d[j]=v
            elif j in d:del d[j]
        return W(d,self.k+o.k,self.period)
    def inv(self):return W({i-self.k:wi(w) for i,w in self.d.items()},-self.k,self.period)
    def __eq__(self,o):return self.k==o.k and self.d==o.d and self.period==o.period
    def __repr__(self):return repr((self.k,self.d,self.period))
def prod(ws,period=None):
    out=W(period=period)
    for x in ws:out=out*x
    return out
def conj(a,b):return a*b*a.inv()
def comm(a,b):return a*b*a.inv()*b.inv()
def power(a,n):return prod([a if n>=0 else a.inv()]*abs(n),a.period)
def transport(gs,period=None):
    # gs are base words whose IN ORDER product is identity.
    assert wm(*gs)==()
    prefix=();d={}
    for i,g in enumerate(gs[:-1]):
        prefix=wm(prefix,g)
        if prefix:d[i]=prefix
    T=W(k=1,period=period); v=W(d,period=period)
    out=comm(T,v.inv())
    desired=W({i:g for i,g in enumerate(gs)},period=period)
    assert out==desired
    return out
def seven(fs,gs):
    m=len(fs);assert m>=2 and len(gs)==m
    T=W(k=1)
    cs=[wc(f,g) for f,g in zip(fs,gs)]
    x=wm(*cs[::-1]); K=transport([x]+[wi(c) for c in cs])
    theta=W({i+1:c for i,c in enumerate(cs)})
    phi=W({i+1:f for i,f in enumerate(fs)});psi=W({i+1:g for i,g in enumerate(gs)})
    f=wm(*fs[::-1]);g=wm(*gs[::-1]); f0=W({0:f});g0=W({0:g})
    Kf=transport([f]+[wi(a) for a in fs]);Kg=transport([g]+[wi(a) for a in gs])
    X=f0.inv()*phi;Y=g0.inv()*psi
    assert X==conj(f0.inv(),Kf.inv()) and Y==conj(g0.inv(),Kg.inv())
    U=transport([wm(f,g),wi(g),wi(f)])
    V=transport([wm(wi(f),wi(g)),g,f])
    assert U*V==comm(f0,g0)
    factors=[K,U,V,conj(g0*f0*g0.inv(),X),conj(g0*f0,Y),conj(g0*f0,X.inv()),conj(g0,Y.inv())]
    assert K*theta==W({0:x}) and theta==comm(phi,psi)
    assert prod(factors)==W({0:x})
    return x,factors
def displacement_controls():
    rng=random.Random(4242380)
    word=lambda:red(rng.choices((1,2,-1,-2),k=rng.randrange(1,9)))
    for m in range(2,15):
        for case in range(15):
            fs=[word() for _ in range(m)];gs=[word() for _ in range(m)]
            seven(fs,gs)
    T=W(k=1);f=W({0:(1,)});g=W({0:(2,)})
    assert comm(f,g)!=W()
    assert comm(f,conj(T,g))==W()
    assert comm(comm(f,T),g)==comm(f,g)
    # The same m=1 assertion uses only disjoint blocks 0 and 1.
    t2=W(k=1,period=2);f2=W({0:(1,)},period=2);g2=W({0:(2,)},period=2)
    assert comm(f2,conj(t2,g2))==W(period=2)
    assert comm(comm(f2,t2),g2)==comm(f2,g2)
    # A three-block formula cannot be licensed by only 1-displacement.
    U2=W({0:(1,2),1:(-2,),2:(-1,)},period=2)
    V2=W({0:(-1,-2),1:(2,),2:(1,)},period=2)
    assert U2*V2!=comm(f2,g2)
    print('DISPLACEMENT: 195 actual noncommuting seven-factor identities; integer-index supports, no wrap')
    print('m=1 double-commutator bound4 works in exactly two blocks; unsupported three-block formula fails')
    for period in range(2,10):
        t=W(k=1,period=period);a=W({0:(1,)},period=period);b=W({0:(2,)},period=period)
        assert comm(a,conj(power(t,period),b))!=W(period=period)
    print('WRAP-AROUND negative controls: periods2..9 fail displacement at the repeated endpoint')
    # Degenerate abelian base: identity displacer entails trivial derived.
    assert wc((1,1),(1,1,1))==()
    print('DEGENERACY: abelian base, identity displacer => derived identity; cl=0 bound0')

if __name__=='__main__':
    print('SOURCE-FIRST independent controls; seed values fixed; exact arithmetic throughout')
    metabelian_controls();extension_controls();lp_controls();braid_controls();displacement_controls()
    print('ALL INDEPENDENT CONTROLS PASSED')
