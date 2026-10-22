#!/usr/bin/env python3
"""Independent exact boundary controls and retained-witness checks; stdlib only.

No authored proof code, historical certificates, or acceptance metadata is imported.
All checks use explicit guards, so python -O cannot remove them.
"""
from itertools import product
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parent
PIN = '68c040d5bfe5d536e6f33f0f319a2d721bac5c562ec60f802fc516f293205b75'
INPUT = ROOT.parent.parent / 'inputs' / 'PROOF.md'

def need(ok, message):
    if not ok:
        raise RuntimeError(message)

need(hashlib.sha256(INPUT.read_bytes()).hexdigest() == PIN, 'wrong proof bytes')

def ab_elements(mods):
    return list(product(*(range(m) for m in mods)))

def plus(x, y, mods):
    return tuple((a+b) % m for a,b,m in zip(x,y,mods))

def minus(x, y, mods):
    return tuple((a-b) % m for a,b,m in zip(x,y,mods))

class Candidate:
    def __init__(self, tm, sm, b, alpha):
        self.tm, self.sm, self.b, self.alpha = tm, sm, b, alpha
        self.T, self.S = ab_elements(tm), ab_elements(sm)
        self.zero = (tuple(0 for _ in tm), tuple(0 for _ in sm))
        self.elements = list(product(self.T,self.S))
    def add(self, a, c):
        t,s = a; u,v = c
        return (plus(t,u,self.tm), plus(plus(s,v,self.sm), self.b(t,u), self.sm))
    def sub(self, a, c):
        t,s = a; u,v = c
        diff = minus(t,u,self.tm)
        return diff, minus(minus(s,v,self.sm),self.b(diff,u),self.sm)
    def mul(self, a, c):
        t,s = a; u,v = c
        return plus(t,self.alpha(s,u),self.tm), plus(s,v,self.sm)
    def lam(self, a, c):
        return self.sub(self.mul(a,c),a)
    def star(self, a, c):
        return self.sub(self.lam(a,c),c)
    def order(self, a):
        acc=self.zero
        for n in range(1,len(self.elements)+1):
            acc=self.add(acc,a)
            if acc==self.zero: return n
        raise RuntimeError('order failed')
    def all_brace_laws(self):
        E=self.elements; z=self.zero
        for a in E:
            need(self.add(a,z)==a and self.mul(a,z)==a and self.mul(z,a)==a,'identity')
            need(any(self.add(a,c)==z for c in E),'additive inverse')
            need(any(self.mul(a,c)==z and self.mul(c,a)==z for c in E),'multiplicative inverse')
            for c in E:
                need(self.add(a,c)==self.add(c,a),'additive commutativity')
                for d in E:
                    need(self.add(self.add(a,c),d)==self.add(a,self.add(c,d)),'additive associativity')
                    need(self.mul(self.mul(a,c),d)==self.mul(a,self.mul(c,d)),'multiplicative associativity')
                    need(self.lam(a,self.add(c,d))==self.add(self.lam(a,c),self.lam(a,d)),'brace compatibility')
        return len(E)**3
    def triple_counts(self, subset=None):
        E=self.elements if subset is None else subset
        nonzero=[]
        for a,c,d in product(E,repeat=3):
            value=self.star(self.star(a,c),d)
            if value!=self.zero: nonzero.append([a,c,d,value])
        return {'tested':len(E)**3,'nonzero':len(nonzero),'first_nonzero':nonzero[0] if nonzero else None}

results={'proof_sha256':PIN,'controls':{}}
# A nonzero square in a valid two-trivial-factor, abelian-Sylow example.
C25=Candidate((5,),(5,),lambda t,u:((t[0]*u[0])%5,),lambda s,u:u)
trials=C25.all_brace_laws()
triples=C25.triple_counts()
need(triples['nonzero']==0,'order25 triple obstruction fails')
square=C25.star(((1,),(0,)),((1,),(0,)))
need(square!=C25.zero,'order25 square should be nonzero')
results['controls']['order25_nonzero_square_zero_triples']={'brace_triples':trials,'star_square':square,'triple_products':triples}
# Even-primary addition can be C4 although T x S has four two-torsion coordinates.
C4=Candidate((2,),(2,),lambda t,u:((t[0]*u[0])%2,),lambda s,u:u)
trials=C4.all_brace_laws(); twisted_order=C4.order(((1,),(0,)))
need(twisted_order==4,'additive Sylow twist not exercised')
triples=C4.triple_counts(); need(triples['nonzero']==0,'twisted primary triple')
results['controls']['order4_additive_twist']={'brace_triples':trials,'additive_order_of_coordinate_generator':twisted_order,'triple_products':triples}
# A mixed-prime case tests setwise Sylow identification without direct-product addition.
C36=Candidate((2,3),(2,3),lambda t,u:((t[0]*u[0])%2,(t[1]*u[1])%3),lambda s,u:u)
trials=C36.all_brace_laws(); primary={}
for p,index in [(2,0),(3,1)]:
    expected=[a for a in C36.elements if all(a[j][1-index]==0 for j in (0,1))]
    actual=[]
    for a in C36.elements:
        order=C36.order(a); remaining=order
        while remaining%p==0: remaining//=p
        if remaining==1: actual.append(a)
    need(set(expected)==set(actual),'primary set mismatch')
    ts=C36.triple_counts(expected); need(ts['nonzero']==0,'mixed primary triple')
    primary[str(p)]={'size':len(actual),'maximum_additive_order':max(map(C36.order,actual)),'triple_products':ts}
results['controls']['order36_mixed_primes']={'brace_triples':trials,'primary':primary}
# Symmetric normalized nonlinear coboundary: cocycle yes, admissible brace no.
f=lambda t:t**3 % 5
b=lambda t,u:((f(t[0])+f(u[0])-f((t[0]+u[0])%5))%5,)
N=Candidate((5,),(5,),b,lambda s,u:u)
for t,u,w in product(N.T,repeat=3):
    need(b(t,u)==b(u,t),'nonlinear symmetry')
    need(plus(b(plus(t,u,N.tm),w),b(t,u),N.sm)==plus(b(t,plus(u,w,N.tm)),b(u,w),N.sm),'nonlinear cocycle')
need(b((0,),(0,))==(0,),'nonlinear normalization')
a=((1,),(0,)); c=((1,),(0,)); target=((1,),(0,))
lhs=N.lam(a,N.lam(c,target)); rhs=N.lam(N.mul(a,c),target)
need(lhs!=rhs,'nonlinear cocycle unexpectedly admissible')
results['controls']['nonlinear_symmetric_cocycle_rejected']={'cocycle_triples':125,'lambda_composition_witness':{'a':a,'b':c,'target':target,'left':lhs,'right':rhs}}
# Removing abelian-Sylow hypothesis permits a nonzero triple, even with both factors trivial.
D8=Candidate((2,2),(2,),lambda t,u:((t[0]*u[0]+t[1]*u[1])%2,),lambda s,u:u if s[0]==0 else (u[1],u[0]))
trials=D8.all_brace_laws(); triples=D8.triple_counts()
need(triples['nonzero']>0,'nonabelian-primary negative control did not fail')
commuting=all(D8.mul(a,c)==D8.mul(c,a) for a,c in product(D8.elements,repeat=2))
need(not commuting,'negative control Sylow should be nonabelian')
results['controls']['order8_nonabelian_primary']={'brace_triples':trials,'multiplication_abelian':commuting,'triple_products':triples}

# Direct implementation of the proposed brace, used only for retained invariant witnesses.
Z=(0,0,0,0)
def radd(a,c): return tuple((a[i]+c[i])%5 for i in range(4))
def rneg(a): return tuple(-x%5 for x in a)
def rscale(k,a): return tuple(k*x%5 for x in a)
def rmul(a,c):
    out=[0]*4
    for i,x in enumerate(a):
        for j,y in enumerate(c):
            if i+j+1<4: out[i+j+1]=(out[i+j+1]+x*y)%5
    return tuple(out)
def poly(a,coefficients):
    power=a; out=Z
    for c in coefficients:
        out=radd(out,rscale(c,power)); power=rmul(power,a)
    return out
# 1/2=3, 1/3=2, 1/4=4, 1/6=1, 1/24=4 modulo 5.
def log(a): return poly(a,[1,2,2,1])
def exp(a): return poly(a,[1,3,1,4])
def sigma(a): return ((-a[0])%5,a[1],(-a[2])%5,a[3])
def eta(a): return log(a)[3]
def beta(v,w): return (v&w).bit_count()%2
def q(v): return (v.bit_count()//2)%2
def rotate(v): return ((v<<1)&31)|(v>>4)
def mpow(s,v):
    for _ in range(s%5): v=rotate(v)
    return v
zero=(Z,0,0)
def add(a,c): return radd(a[0],c[0]), a[1]^c[1], a[2]^c[2]
def neg(a): return rneg(a[0]),a[1],a[2]
def mul(a,c):
    r,v,z=a; u,w,zz=c
    h=sigma(u) if z^q(v) else u
    mw=mpow(eta(r),w)
    return radd(radd(r,h),rmul(r,h)),v^mw,z^zz^beta(v,mw)
def lam(a,c): return add(mul(a,c),neg(a))
def star(a,c): return add(lam(a,c),neg(c))
def inverse(a):
    r,v,z=a; lr=log(r); e=z^q(v)
    invlr=sigma(rneg(lr)) if e else rneg(lr)
    w=mpow(-lr[3],v)
    return exp(invlr),w,e^q(w)
R=list(product(range(5),repeat=4)); V=[v for v in range(32) if v.bit_count()%2==0]
E=[(r,v,z) for r,v,z in product(R,V,range(2))]
ringbasis=[tuple(int(j==i) for j in range(4)) for i in range(4)]
vbasis=[(1<<i)|16 for i in range(4)]
generators=[(r,0,0) for r in ringbasis]+[(Z,v,0) for v in vbasis]+[(Z,0,1)]
fixed=[a for a in E if all([lam(g,a)==a for g in generators])]
expected_fixed=[((0,0,0,c),0,z) for c,z in product(range(5),range(2))]
need(set(fixed)==set(expected_fixed),'fixed set disagreement')
center=[a for a in E if all([mul(g,a)==mul(a,g) for g in generators])]
expected_center=[(exp((0,c,0,0)),0,0) for c in range(5)]
need(set(center)==set(expected_center),'center disagreement')
central=(exp((0,1,0,0)),0,0)
need(all(mul(a,central)==mul(central,a) for a in E),'central witness fails full universe')
k=(Z,0,1); h=(exp((2,0,0,0)),0,0)
d=mul(mul(mul(k,h),inverse(k)),inverse(h))
need(d==(exp((1,0,0,0)),0,0),'commutator witness mismatch')
x=((1,0,0,0),0,0)
dx=star(d,x); xdx=star(x,dx)
need(dx==((0,1,3,1),0,0),'d*x coefficient mismatch')
need(xdx==((0,0,1,3),0,0),'x*(d*x) coefficient mismatch')
triple=star(star(x,x),x)
need(triple==((0,0,1,0),0,0),'decisive triple witness mismatch')
# The nine displayed generators generate the whole multiplicative group: closure by right generators.
closure={zero}; frontier=[zero]
while frontier:
    a=frontier.pop()
    for g in generators:
        c=mul(a,g)
        if c not in closure: closure.add(c); frontier.append(c)
need(len(closure)==20000,'witness testing generators do not generate G')
for a in E:
    need(mul(a,inverse(a))==zero and mul(inverse(a),a)==zero,'inverse error')
results['retained_witnesses']={'element_count':len(E),'multiplicative_generator_closure':len(closure),'fixed_target_generator_tests':len(E)*len(generators),'fixed_set_order':len(fixed),'center_target_generator_tests':len(E)*len(generators),'center_order':len(center),'central_witness_all_element_tests':len(E),'central_witness':central,'commutator':d,'d_star_x':dx,'x_star_d_star_x':xdx,'sylow5_triple_star':triple,'all_element_two_sided_inverse_tests':2*len(E)}
print(json.dumps(results,indent=2,sort_keys=True))
