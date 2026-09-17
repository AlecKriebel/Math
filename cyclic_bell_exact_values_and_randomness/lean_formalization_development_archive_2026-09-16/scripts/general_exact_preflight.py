#!/usr/bin/env python3
"""Compiler-free EXACT regressions; NEVER Lean proof evidence.

Cyclotomic arithmetic uses Fraction coefficients modulo Phi_N, reconstructed
recursively from x^N-1. Field equality/inverses are checked by rational residuals.
No floating-point comparison or external solver verdict occurs in these checks.
Finite ranges test implementations/conventions, not the general quantifiers.
"""
from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction as F
from functools import lru_cache
from itertools import permutations, product
from datetime import datetime, timezone
from pathlib import Path
import argparse, json


def trim(p):
    p=list(map(F,p))
    while len(p)>1 and not p[-1]: p.pop()
    return p

def padd(p,q):
    r=[F(0)]*max(len(p),len(q))
    for i,a in enumerate(p):r[i]+=a
    for i,a in enumerate(q):r[i]+=a
    return trim(r)

def pmul(p,q):
    r=[F(0)]*(len(p)+len(q)-1)
    for i,a in enumerate(p):
        if a:
            for j,b in enumerate(q):
                if b:r[i+j]+=a*b
    return trim(r)

def pdiv(p,q):
    p,q=trim(p),trim(q)
    if q==[0]:raise ZeroDivisionError
    r=[F(0)]*max(1,len(p)-len(q)+1)
    while p!=[0] and len(p)>=len(q):
        n=len(p)-len(q);c=p[-1]/q[-1];r[n]=c
        for j,a in enumerate(q):p[n+j]-=c*a
        p=trim(p)
    return trim(r),p

@lru_cache(None)
def phi(n):
    if n<1:raise ValueError('positive conductor required')
    p=[F(-1)]+[F(0)]*(n-1)+[F(1)]
    for d in range(1,n):
        if n%d==0:
            p,r=pdiv(p,phi(d))
            if r!=[0]:raise ArithmeticError('cyclotomic polynomial residual')
    return tuple(p)

@dataclass(frozen=True)
class E:
    n:int
    c:tuple[F,...]
    def coerce(self,x):
        if isinstance(x,E):
            if self.n!=x.n:raise ValueError('field mismatch')
            return x
        return elt(self.n,[x])
    def __add__(self,x):return eadd(self,self.coerce(x))
    __radd__=__add__
    def __neg__(self):return elt(self.n,[-x for x in self.c])
    def __sub__(self,x):return self+-self.coerce(x)
    def __rsub__(self,x):return self.coerce(x)+-self
    def __mul__(self,x):return emul(self,self.coerce(x))
    __rmul__=__mul__
    def inv(self):
        if not any(self.c):raise ZeroDivisionError
        r0,r1=list(phi(self.n)),trim(self.c);t0,t1=[F(0)],[F(1)]
        while r1!=[0]:
            q,r=pdiv(r0,r1)
            r0,r1=r1,r;t0,t1=t1,padd(t0,[-a for a in pmul(q,t1)])
        if len(r0)!=1:raise ArithmeticError('non-field inverse')
        inv=elt(self.n,[a/r0[0] for a in t0])
        if self*inv!=elt(self.n,[1]):raise ArithmeticError('inverse residual')
        return inv
    def __truediv__(self,x):
        if isinstance(x,E):return self*x.inv()
        return elt(self.n,[a/F(x) for a in self.c])
    def __rtruediv__(self,x):return self.coerce(x)*self.inv()
    def __pow__(self,k):
        if k<0:return self.inv()**(-k)
        a,r=self,elt(self.n,[1])
        while k:
            if k&1:r=r*a
            a=a*a;k//=2
        return r
    def conj(self):return sum((a*root(self.n,-j) for j,a in enumerate(self.c)),elt(self.n,[0]))
    def real(self):return (self+self.conj())/2
    def normsq(self):return self*self.conj()
    def rat(self):
        if any(self.c[1:]):raise ValueError('not rational')
        return self.c[0]

@lru_cache(maxsize=100000)
def eadd(a,b):
    if not any(a.c):return b
    if not any(b.c):return a
    return elt(a.n,padd(a.c,b.c))

@lru_cache(maxsize=100000)
def emul(a,b):
    if not any(a.c):return a
    if not any(b.c):return b
    if a.c[0]==1 and not any(a.c[1:]):return b
    if b.c[0]==1 and not any(b.c[1:]):return a
    return elt(a.n,pmul(a.c,b.c))

@lru_cache(maxsize=100000)
def elt(n,p):
    p=tuple(p) if isinstance(p,tuple) else p
    _,r=pdiv(p,phi(n));m=len(phi(n))-1
    return E(n,tuple(r+[F(0)]*(m-len(r))))
# Lists are not hashable; keep caching on a canonical tuple wrapper.
_elt_cached=elt.__wrapped__
@lru_cache(maxsize=100000)
def _canon(n,p):return _elt_cached(n,p)
def elt(n,p):return _canon(n,tuple(map(F,p)))

@lru_cache(None)
def root(n,k):
    k%=n
    return elt(n,[0]*k+[1])

def prod(xs,one):
    for x in xs:one=one*x
    return one

def mm(a,b):
    z=a[0][0]*0
    return [[sum((a[i][k]*b[k][j] for k in range(len(b))),z)
             for j in range(len(b[0]))] for i in range(len(a))]
def ma(a,b):return [[x+y for x,y in zip(r,s)] for r,s in zip(a,b)]
def ms(c,a):return [[c*x for x in r] for r in a]
def adj(a):return [[a[j][i].conj() for j in range(len(a))] for i in range(len(a[0]))]
def ident(d,n):return [[elt(n,[int(i==j)]) for j in range(d)] for i in range(d)]
def shift(w):
    d=len(w);z=w[0]*0
    return [[w[j] if i==(j+1)%d else z for j in range(d)] for i in range(d)]
def mpow(a,k):
    r=ident(len(a),a[0][0].n)
    while k:
        if k&1:r=mm(r,a)
        a=mm(a,a);k//=2
    return r
def tr(a):return sum((a[i][i] for i in range(len(a))),a[0][0]*0)
def phi_expect(a,b):return sum((a[i][j]*b[i][j] for i in range(len(a)) for j in range(len(a))),a[0][0]*0)/len(a)

def pvm(q,a):
    d=len(q);om=root(q[0].n,4)
    return [[q[i]*q[j].conj()*om**(a*(j-i))/d for j in range(d)] for i in range(d)]
def prefix(w):
    q=[w[0]*0+1]
    for x in w[:-1]:q.append(q[-1]*x)
    return q

class Checks:
    def __init__(self):self.rows=[];self.controls=[]
    def equal(self,label,a,b):
        if a!=b:raise AssertionError(label)
        self.rows.append(label)
    def truth(self,label,a):
        if not a:raise AssertionError(label)
        self.rows.append(label)
    def negative(self,label,a,b):
        if a==b:raise AssertionError('negative control failed: '+label)
        self.controls.append(label)

def dimension_checks(d,C):
    n=4*d;one=elt(n,[1]);zero=elt(n,[0]);om=root(n,4);eta=root(n,2);ii=root(n,d)
    delta=int(d%2==0)
    z=[root(n,2*(2*k+delta)) for k in range(d)]
    s0=[root(n,2*k+delta)*(1 if 2*k+delta<d else -1) for k in range(d)]
    sy=[[s0[(y+k)%d] for k in range(d)] for y in range(d)]
    C.equal(f'd{d}:root product',prod(z,one),one)
    for k in range(d):
        C.equal(f'd{d}:root order {k}',z[k]**d,one*((-1)**(d-1)))
        C.equal(f'd{d}:polar squared {k}',s0[k]**2,z[k])
    for y in range(d):
        C.equal(f'd{d}:polar product {y}',prod(sy[y],one),one)
        cut=sum(2*k+delta<d for k in range(d));special=(cut-1-y)%d
        for k in range(d):
            C.equal(f'd{d}:adjacent-wrap {y},{k}',sy[(y+1)%d][k],eta*sy[y][k]*(-1 if k==special else 1))
    lam=[];r=[]
    for l in range(d):
        ss=(root(n,2*l-1)-root(n,-(2*l-1)))/(2*ii)
        ll=((-1)**(l+1))*eta**(l*(l-1))/(d*ss)
        rr=eta**(-l*(l-1+delta));lam.append(ll);r.append(rr)
        S=sum((om**(l*t)*s0[t].conj() for t in range(d)),zero)
        C.equal(f'd{d}:lambda compression {l}',S,d*ll*rr)
    C.equal(f'd{d}:lambda normalization',sum((x.normsq() for x in lam),zero),one)
    M=2/((root(n,1)-root(n,-1))/(2*ii))
    orders=[list(range(d))]
    if d>=4:orders.append(list(range(d-2))+[d-1,d-2])
    else:orders=list(permutations(range(d)))
    saved=None
    for order in orders:
        w=[z[k] for k in order];q=prefix(w)
        Fq=[sum((q[j]*om**(m*j) for j in range(d)),zero) for m in range(d)]
        power=[x.normsq() for x in Fq]
        C.equal(f'd{d}:Parseval {order}',sum(power,zero),one*d*d)
        R=[sum((q[(j+t)%d]*q[j].conj() for j in range(d)),zero) for t in range(d)]
        for m in range(d):C.equal(f'd{d}:WK {order} {m}',power[m],sum((R[t]*om**(m*t) for t in range(d)),zero))
        if tuple(order)==tuple(range(d)):
            C.equal(f'd{d}:canonical flat',power,[one*d]*d)
            expected=[root(n,2*j*(j-1+delta)) for j in range(d)]
            C.equal(f'd{d}:chirp phases',q,expected)
        elif d<4:C.equal(f'd{d}:low-dimensional orbit flat {order}',power,[one*d]*d)
        else:
            C.equal(f'd{d}:swapped R2',R[2],(z[-1]-z[-2])*(z[-3]-z[0]))
            C.negative(f'd{d}:swap not flat',power,[one*d]*d)
            if d==4:C.equal('d4:parity powers',power,[one*k for k in [2,6,2,6]])
        h0=[];h1=[]
        for y in range(d):
            h0.append(sum((sy[y][k].conj() for k in order),zero)/d)
            h1.append(sum((z[k]*sy[y][k].conj() for k in order),zero)/d)
        if saved is None:saved=(h0,h1)
        else:C.equal(f'd{d}:permutation blindness {order}',(h0,h1),saved)
        C.equal(f'd{d}:first score {order}',sum(((h0[y]+om**y*h1[y]).real() for y in range(d)),zero)+one,M+one)
        # Actual matrix encoding of target eigenprojectors, independent of Fourier power.
        if d<=8:
            ps=[pvm(q,a) for a in range(d)];us=[pvm([one]*d,b) for b in range(d)]
            encoded=[[sum((om**a*ps[a][i][j] for a in range(d)),zero) for j in range(d)] for i in range(d)]
            C.equal(f'd{d}:target observable encoding {order}',encoded,shift(w))
            for b in range(d):
                # rho_{(i,i),(j,j)}=1/d, zero off that support. Exact full Born trace.
                born=sum((ps[0][j][i]*us[b][j][i]/d for i in range(d) for j in range(d)),zero)
                C.equal(f'd{d}:projector Born {order} 0,{b}',born,power[(-b)%d]/(d**3))
            if d<=5:
                for a in range(d):
                    C.equal(f'd{d}:target idempotent {order} {a}',mm(ps[a],ps[a]),ps[a])
                    C.equal(f'd{d}:target Hermitian {order} {a}',adj(ps[a]),ps[a])
        # Fourier compression gives the actual second-score first harmonics.
        second=zero
        for l in range(d):
            aa=[r[l].conj()*om**(l*k) for k in order]
            C.equal(f'd{d}:second A order {order} {l}',prod(aa,one),one)
            if l==1:C.equal(f'd{d}:same target A1 {order}',aa,w)
            hh=[sum((aa[j]*sy[y][order[j]].conj() for j in range(d)),zero)/d for y in range(d)]
            for y in range(d):C.equal(f'd{d}:second harmonics {order} {l},{y}',hh[y],lam[l]*om**(-l*y))
            second+=(lam[l].conj()*sum((om**(l*y)*hh[y] for y in range(d)),zero)).real()
        C.equal(f'd{d}:second augmented score {order}',second+one,one*(d+1))
    C.negative(f'd{d}:wrong coefficient phase detected',sum((x.normsq() for x in lam),zero)*2,one)
    # Reflection-rank hypothesis on a genuine cycle, and a wrong-power control.
    V=shift([one]*d);wr=[one]*d;wr[0]=-one;W=shift(wr)
    C.equal(f'd{d}:reflection V power',mpow(V,d),ident(d,n))
    C.equal(f'd{d}:reflection W power',mpow(W,d),ms(-one,ident(d,n)))
    C.negative(f'd{d}:altered reflection power',mpow(V,d),ms(-one,ident(d,n)))
    if d%2==0:
        C.equal(f'd{d}:unused ambient polar kernel',one+om**(d//2)*one,zero)
        C.negative(f'd{d}:global phase outside support invalid',one**d,one*((-1)**(d-1)))

def one_input_checks(C):
    pa=[F(1,3),F(2,3),F(0)]
    r=[[[F(1,4),F(3,4)],[F(2,5),F(3,5)],[F(1),F(0)]],
       [[F(1,2),F(1,3),F(1,6)],[F(1,5),F(1,5),F(3,5)],[F(1),F(0),F(0)]]]
    weights={(a,b,c):pa[a]*r[0][a][b]*r[1][a][c] for a in range(3) for b in range(2) for c in range(3)}
    C.equal('one-input:hidden normalization',sum(weights.values()),F(1))
    for y,nb in enumerate([2,3]):
        for a in range(3):
            for b in range(nb):C.equal(f'one-input:behavior y{y} a{a} b{b}',
                sum(w for L,w in weights.items() if L[0]==a and L[y+1]==b),pa[a]*r[y][a][b])
        success=F(0)
        for a in range(3):
            for b in range(nb):
                # conditional Eve density is diagonal; guess projector selects the same labels.
                success+=sum(w for L,w in weights.items() if L[0]==a and L[y+1]==b)
        C.equal(f'one-input:physical diagonal-Eve success y{y}',success,F(1))
    C.equal('one-input:zero marginal joint',sum(w for L,w in weights.items() if L[0]==2),F(0))

# Free products C2*C2 in each party, direct product across the two parties.
def word_mul(x,y):
    ans=[]
    for a,b in zip(x,y):
        out=list(a)
        for c in b:
            if out and out[-1]==c:out.pop()
            else:out.append(c)
        ans.append(tuple(out))
    return tuple(ans)
def poly_add(x,y):
    r=dict(x)
    for w,c in y.items():
        r[w]=r.get(w,c*0)+c
        if not any(r[w].c):del r[w]
    return r
def poly_scale(c,p):return {w:c*a for w,a in p.items() if any((c*a).c)}
def poly_mul(x,y):
    r={}
    for u,a in x.items():
        for v,b in y.items():r=poly_add(r,{word_mul(u,v):a*b})
    return r

def binary_checks(C):
    n=12;o=elt(n,[1]);s=root(n,1)+root(n,-1)
    I={((),()):o};A0={((0,),()):o};A1={((1,),()):o};B0={((),(0,)):o};B1={((),(1,)):o}
    add=poly_add;sc=poly_scale;mu=poly_mul
    W=add(add(mu(A0,B0),sc(-2,mu(A0,B1))),add(sc(2,mu(A1,B0)),sc(2,mu(A1,B1))))
    R0=add(add(sc(s,A0),sc(-1,B0)),sc(2,B1));R1=add(add(sc(s,A1),sc(-1,B0)),sc(-1,B1))
    C.equal('binary:sqrt3 exact',s*s,3*o)
    C.equal('binary:free two-square SOS',add(sc(3*s,I),sc(-1,W)),
        add(sc(1/(2*s),mu(R0,R0)),sc(1/s,mu(R1,R1))))
    C.negative('binary:wrong SOS factor',add(sc(3*s,I),sc(-1,W)),
        add(sc(1/s,mu(R0,R0)),sc(1/s,mu(R1,R1))))
    X=[[0*o,o],[o,0*o]];Z=[[o,0*o],[0*o,-o]]
    a0=Z;a1=ma(ms(F(-1,2),Z),ms(s/2,X));b0=X;b1=ma(ms(-s/2,Z),ms(F(1,2),X))
    for label,a in [('a0',a0),('a1',a1),('b0',b0),('b1',b1)]:
        C.equal('binary:witness involution '+label,mm(a,a),ident(2,n))
    val=phi_expect(a0,b0)-2*phi_expect(a0,b1)+2*phi_expect(a1,b0)+2*phi_expect(a1,b1)
    C.equal('binary:actual attained value',val,3*s)
    for a,b in product(range(2),repeat=2):
        P=ms(F(1,2),ma(ident(2,n),ms((-1)**a,a0)));Q=ms(F(1,2),ma(ident(2,n),ms((-1)**b,b0)))
        C.equal(f'binary:actual target Born {a},{b}',phi_expect(P,Q),o/4)


def run(ds):
    C=Checks();start=datetime.now(timezone.utc)
    for d in ds:dimension_checks(d,C)
    one_input_checks(C);binary_checks(C)
    return {'status':'PASS_compiler_free_exact_regressions_only','kernel_checked':False,
        'started_utc':start.isoformat(),'finished_utc':datetime.now(timezone.utc).isoformat(),
        'dimensions':list(ds),'arithmetic':'Fraction in Q[x]/Phi_(4d), exact rational residuals',
        'checks':len(C.rows),'negative_controls':len(C.controls),'check_names':C.rows,
        'negative_control_names':C.controls,
        'limitations':['Finite test ranges do not prove universal quantifiers.',
          'No Lean/compiler invocation and no actual axiom output.',
          'One author; not an independent-agent or external review.',
          'No certificate is imported by any Lean source.']}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--min-d',type=int,default=2);p.add_argument('--max-d',type=int,default=12);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args()
    if not 2<=a.min_d<=a.max_d<=20 or a.max_d<4:
        raise SystemExit('Use 2<=min-d<=max-d<=20 and max-d>=4 for this bounded regression suite.')
    report=run(range(a.min_d,a.max_d+1))
    a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ('status','dimensions','checks','negative_controls','kernel_checked')},indent=2))
