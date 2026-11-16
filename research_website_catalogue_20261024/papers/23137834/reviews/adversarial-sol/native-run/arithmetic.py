#!/usr/bin/env python3
# Public export: optimization must not disable scientific assertions.
import sys
if sys.flags.optimize:
    raise SystemExit("Verification refuses Python optimization (-O/-OO).")
"""Portable exact controls; standard library only, no source/package writes.

These controls supplement the source-based proof. Finite-field observations
alone do not prove a number-field division-field equality.
"""
import argparse
from fractions import Fraction as F
import json
import sys

parser = argparse.ArgumentParser()
parser.add_argument('--mutant', choices=['drop_twist','wrong_radical','wrong_cyclotomic','wrong_norm_degree'])
args = parser.parse_args()
checks = 0

def ck(test, label):
    global checks
    checks += 1
    if not test:
        print(json.dumps({'status':'FAIL','check':label,'checks_before_failure':checks,
                          'mutant':args.mutant}, sort_keys=True))
        sys.exit(1)

class K:
    """Exact Q[r]/(r^2-5)."""
    def __init__(self,a=0,b=0): self.a,self.b=F(a),F(b)
    def __add__(self,o):
        o=lift(o); return K(self.a+o.a,self.b+o.b)
    __radd__=__add__
    def __neg__(self): return K(-self.a,-self.b)
    def __sub__(self,o): return self+-lift(o)
    def __rsub__(self,o): return lift(o)+-self
    def __mul__(self,o):
        o=lift(o); return K(self.a*o.a+5*self.b*o.b,self.a*o.b+self.b*o.a)
    __rmul__=__mul__
    def norm(self): return self.a*self.a-5*self.b*self.b
    def __truediv__(self,o):
        o=lift(o); n=o.norm(); return self*K(o.a/n,-o.b/n)
    def __rtruediv__(self,o): return lift(o)/self
    def __pow__(self,n):
        if n<0:return (1/self)**(-n)
        out=K(1)
        for _ in range(n):out=out*self
        return out
    def __eq__(self,o):
        o=lift(o); return self.a==o.a and self.b==o.b
    def __repr__(self): return f'({self.a})+({self.b})r'

def lift(x):return x if isinstance(x,K) else K(x)
def padd(a,b):
    return [(a[i] if i<len(a) else K())+(b[i] if i<len(b) else K()) for i in range(max(len(a),len(b)))]
def pscale(a,s):return [v*s for v in a]
def pmul(a,b):
    out=[K() for _ in range(len(a)+len(b)-1)]
    for i,x in enumerate(a):
        for j,y in enumerate(b):out[i+j]=out[i+j]+x*y
    return out
def ppow(a,n):
    out=[K(1)]
    for _ in range(n):out=pmul(out,a)
    return out
def peq(a,b,label):
    n=max(len(a),len(b))
    for i in range(n):ck((a[i] if i<len(a) else K())==(b[i] if i<len(b) else K()),f'{label}: coefficient {i}')

r=K(0,1); phi=(1+r)/2; c=phi**5; d=5+2*r
ck(c==K(F(11,2),F(5,2)),'golden ratio fifth power')
ck(c-1/c==11 and c+1/c==5*r,'two cusp and parameter identities')
ck(d.norm()==5,'twist class norm obstruction to squareness')
ck((phi**2+1)!=0 and (c*c+1)!=0,'Mobius transformations invertible')
# Homogeneous equality in the free beta coefficient, not interpolation.
N=ppow([K(1),phi],5); D=ppow([-phi,K(1)],5)
A=padd(N,pscale(D,-c)); B=pscale(padd(pscale(N,c),D),-1)
f=list(map(K,[1,2,4,3,1])); g=list(map(K,[1,-3,4,-2,1]))
s=-(c*c+1)
peq(A,pscale(g,-s),'cover coefficient of beta')
peq(B,pscale([K()]+f,s),'cover constant coefficient')
# Thus (beta-c)N-(beta*c+1)D = s*(t*f-beta*g).
for u in [K(-3),K(-2),K(1),K(2),r]:
    a=u**5; lam=a-c
    ck(lam!=0 and lam!=-5*r and lam!=-c,'split specialization smooth')
    beta=(11-5*r)*lam/(2*(lam+5*r))
    ck((c*beta+1)/(beta-c)==-1/a,'specialized radical identity')
    # Degree-four norm descent works even for a base-field element.
    nn=u**(2 if args.mutant=='wrong_norm_degree' else 4)
    ck((a/nn)**5==a,'degree-four norm descent')
ck(K(2).norm()==4 and r.norm()==-5,'nonsplit examples have non-fifth-power rational norms')

# F5 representation, its full generated group and exact fixed subspaces.
I=(1,0,0,1); U=(1,1,0,1); V=(1,0,0,4); S=(4,0,0,4)
def mm(a,b):
    return ((a[0]*b[0]+a[1]*b[2])%5,(a[0]*b[1]+a[1]*b[3])%5,
            (a[2]*b[0]+a[3]*b[2])%5,(a[2]*b[1]+a[3]*b[3])%5)
def mp(a,n):
    out=I
    for _ in range(n):out=mm(out,a)
    return out
def group(generators):
    out={I}; todo=[I]
    while todo:
        a=todo.pop()
        for g0 in generators:
            z=mm(a,g0)
            if z not in out:out.add(z);todo.append(z)
    return out
def fixed(generators):
    return [(x,y) for x in range(5) for y in range(5)
            if all(((a*x+b*y)%5,(cc*x+dd*y)%5)==(x,y) for a,b,cc,dd in generators)]
ck(mp(U,5)==I and mp(U,1)!=I,'nontrivial transvection of exact order five')
ck(mm(mm(V,U),V)==mp(U,4),'complex conjugation inverts the transvection')
ck(mm(S,U)==mm(U,S) and mm(S,V)==mm(V,S),'twist factor central')
ck(len(group([U,V,S]))==20 and len(group([V,S]))==4,'faithful nonsplit/split image orders')
ck(fixed([U,V,S])==[(0,0)] and fixed([V,S])==[(0,0)],'no K-rational nonzero torsion')
ck(len(fixed([U,V]))==5 and len(fixed([V]))==5,'M-rational torsion exactly one line in both cases')
ck((V[0]*V[3]-V[1]*V[2])%5==4,'cyclotomic determinant')

# Independent finite-field group law on the d-twist of the completed-square
# Tate cubic; includes nonsquare d and primes with no primitive fifth root.
fibers=points=cover_checks=0
categories={}; witnesses={}
for p in [19,29,31,59,71,79,109,131,181]:
    inv=lambda x:pow(x%p,-1,p)
    squares={}
    for y in range(p):squares.setdefault(y*y%p,[]).append(y)
    for rr in [v for v in range(p) if v*v%p==5]:
        dd=(5+2*rr)%p; dsquare=dd in squares
        cc=pow((1+rr)*inv(2)%p,5,p)
        for ll in range(p):
            if ll in [0,(-5*rr)%p,(-cc)%p]:continue
            beta=(11-5*rr)*ll*inv(2*(ll+5*rr))%p
            aa=(beta*beta-6*beta+1)*inv(4)%p
            ab=(beta*beta-beta)*inv(2)%p; ac=beta*beta*inv(4)%p
            def torsion_count(twist):
                nonlocal_dummy=None
                global points
                a2=twist*aa%p;a4=twist*twist*ab%p;a6=twist**3*ac%p
                def add(P,Q):
                    if P is None:return Q
                    if Q is None:return P
                    x,y=P;z,w=Q
                    if x==z and (y+w)%p==0:return None
                    slope=((3*x*x+2*a2*x+a4)*inv(2*y) if P==Q else (w-y)*inv(z-x))%p
                    xx=(slope*slope-a2-x-z)%p
                    return xx,(-y+slope*(x-xx))%p
                out=1
                for x in range(p):
                    for y in squares.get((x**3+a2*x*x+a4*x+a6)%p,[]):
                        P=(x,y);PP=add(P,P)
                        if add(add(PP,PP),P) is None:out+=1
                        points+=1
                return out
            nd=torsion_count(1); ne=torsion_count(dd)
            a=(ll+cc)%p
            fifth=(pow(a,(p-1)//5,p)==1) if p%5==1 else True
            cover=0
            for t in range(p):
                fv=(t**4+3*t**3+4*t*t+2*t+1)%p
                gv=(t**4-2*t**3+4*t*t-3*t+1)%p
                if (t*fv-beta*gv)%p==0:
                    cover+=1
                    der=(5*t**4+12*t**3+12*t*t+4*t+1-beta*(4*t**3-6*t*t+8*t-3))%p
                    ck(der!=0,'smooth cover has no repeated specialized root')
            ck(cover==((5 if fifth else 0) if p%5==1 else 1),'finite cover fiber count with cyclotomic condition')
            cover_checks+=1
            ck(nd==((25 if fifth else 5) if p%5==1 else 5),'untwisted Tate count')
            expected=((25 if fifth else 5) if dsquare else 1) if p%5==1 else 5
            if args.mutant=='drop_twist':expected=nd
            if args.mutant=='wrong_radical' and p%5==1 and dsquare:
                expected=25 if pow(ll,(p-1)//5,p)==1 else 5
            if args.mutant=='wrong_cyclotomic' and p%5!=1:expected=25 if cover else 5
            ck(ne==expected,f'full twist torsion count p={p},r={rr},lambda={ll},delta_square={dsquare}')
            category=f'chi={1 if p%5==1 else -1};psi={1 if dsquare else -1};radical_split={fifth}'
            categories[category]=categories.get(category,0)+1
            witnesses.setdefault(category,{'p':p,'r':rr,'lambda':ll,'Tate_5_points':nd,'twist_5_points':ne,'cover_points':cover})
            fibers+=1
ck(len(categories)==6,'all six distinct character/splitting categories exercised')
print(json.dumps({'status':'PASS','exact_checks':checks,'finite_field_fibers':fibers,
                  'enumerated_affine_points':points,'cover_fibers':cover_checks,
                  'categories':categories,'witnesses':witnesses,
                  'scope':'Exact Q(sqrt(5)) identities, specialization/norm/matrix controls and finite-field falsification tests supplement the source-based proof; no external dependency.'},indent=2,sort_keys=True))
