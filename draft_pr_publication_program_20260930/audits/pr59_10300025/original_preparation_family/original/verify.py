#!/usr/bin/env python3
"""Exact finite diagnostics for two common-conjugacy constructions, stdlib only."""
from fractions import Fraction as Q
from pathlib import Path
from bisect import bisect_right
from itertools import product
import hashlib,json

counts={}
def check(name, condition):
    assert condition,name
    counts[name]=counts.get(name,0)+1

class PL:
    def __init__(self,x,y):
        self.x=list(map(Q,x)); self.y=list(map(Q,y))
        assert len(x)==len(y)>=2 and all(a<b for a,b in zip(self.x,self.x[1:]))
        self.eps=1 if self.y[1]>self.y[0] else -1
        assert all(self.eps*(b-a)>0 for a,b in zip(self.y,self.y[1:]))
    def __call__(self,t):
        t=Q(t);i=max(0,min(len(self.x)-2,bisect_right(self.x,t)-1))
        return self.y[i]+(t-self.x[i])*(self.y[i+1]-self.y[i])/(self.x[i+1]-self.x[i])
    def inverse(self):
        return PL(self.y if self.eps==1 else self.y[::-1],self.x if self.eps==1 else self.x[::-1])

family=[PL([0,1],[3,4]), PL([0,1],[0,4]),
        PL([-3,0,2],[-8,1,2]), PL([0,1],[5,3]),
        PL([-2,0,3],[8,2,-7]), PL([-2,0,1],[-4,-1,5])]
inverses=[f.inverse() for f in family]
for f,fi in zip(family,inverses):
    for t in [Q(i,3) for i in range(-30,31)]:
        check('exact_inverse',fi(f(t))==t and f(fi(t))==t)

# Proposition 1: exact arithmetic, genuine nonlinear generators and inverses.
S=[family[i] for i in (0,1,2,5)]+[inverses[i] for i in (0,1,2,5)]
Sinv=[s.inverse() for s in S]
def F(x): return max([x+1]+[s(x) for s in S])
def Finv(x): return min([x-1]+[si(x) for si in Sinv])
a=F(Q(0))
def H(x):
    x=Q(x);n=0
    while x<0: x=F(x);n-=1
    while x>a: x=Finv(x);n+=1
    return n+x/a
for x in [Q(i,5) for i in range(-100,101)]:
    check('envelope_inverse',F(Finv(x))==x and Finv(F(x))==x)
    check('conjugated_envelope_translation',H(F(x))==H(x)+1)
    for s in S:
        check('generator_sandwich',Finv(x)<=s(x)<=F(x))
        check('generator_displacement',abs(H(s(x))-H(x))<=1)
for word in product(range(4),repeat=3):
    for x,y in [(Q(-11),Q(7)),(Q(0),Q(1,3)),(Q(19),Q(35))]:
        xx,yy=x,y
        for k in word: xx,yy=S[k](xx),S[k](yy)
        check('word_displacement',abs(H(xx)-H(x))<=len(word))
        check('word_two_point_distortion',abs(abs(H(xx)-H(yy))-abs(H(x)-H(y)))<=2*len(word))

# Proposition 2: finite prefix of the recursively chosen exhaustion.
r=[Q(0),Q(1)]
for n in range(1,14):
    targets=[r[n]+1]
    for f,fi in zip(family[:n],inverses[:n]):
        targets.extend(abs(g(t)) for g in (f,fi) for t in (-r[n],r[n]))
    r.append(max(targets)+1)
h=PL([-v for v in r[:0:-1]]+r,[-i for i in range(len(r)-1,0,-1)]+list(range(len(r))))
for n in range(1,len(r)-1):
    for j,(f,fi) in enumerate(zip(family[:n],inverses[:n]),1):
        for t in (-r[n],r[n]):
            check('compact_image_inverse_inclusion',abs(f(t))<r[n+1] and abs(fi(t))<r[n+1])
for j,(f,fi) in enumerate(zip(family,inverses),1):
    samples=[]
    for n in range(j+1,len(r)-2):
        for t in (Q(0),Q(1,4),Q(1,2),Q(3,4),Q(1)):
            for sign in (-1,1):
                x=sign*(r[n]+t*(r[n+1]-r[n]));samples.append(x)
                check('annular_image_bracket',r[n-1]<=abs(f(x))<=r[n+2])
                check('tail_orientation',f.eps*x*f(x)>0)
                check('tail_displacement',abs(h(f(x))-f.eps*h(x))<=2)
    # The signed displacement is piecewise affine; check every breakpoint
    # inside the compact core to obtain an exact finite interval certificate.
    R=r[j+1];knots={-R,R}
    knots.update(x for x in h.x+f.x if -R<=x<=R)
    knots.update(fi(t) for t in h.x if -R<=fi(t)<=R)
    core_max=max(abs(h(f(x))-f.eps*h(x)) for x in knots)
    check('exact_compact_core_maximum',core_max<=2*j+3)
    samples.extend(sorted(knots))
    for x,y in zip(samples,samples[::-1]):
        du=h(f(x))-f.eps*h(x);dv=h(f(y))-f.eps*h(y)
        defect=abs(abs(h(f(x))-h(f(y)))-abs(h(x)-h(y)))
        check('signed_displacement_to_distance',defect<=abs(du)+abs(dv)<=2*(2*j+3))

# Negative controls: original dilations need unbounded additive error;
# orientation reversal requires comparison to -u, not to +u.
for n in (1,2,5,20,100):
    check('raw_dilation_distortion',abs(abs(4*Q(n)-0)-abs(Q(n)-0))==3*n)
    check('reflection_signed_control',abs((-Q(n))-(-1)*Q(n))==0 and abs(-Q(n)-Q(n))==2*n)

root=Path(__file__).resolve().parent
receipt={'artifact_sha256':hashlib.sha256((root/'KNOWN_RESULT.md').read_bytes()).hexdigest(),
         'arithmetic':'fractions.Fraction only; no floating-point tolerances',
         'assertions_passed':sum(counts.values()),'by_category':counts,
         'maps':len(family),'exhaustion_intervals':len(r)-1,
         'limits':'Finite diagnostic controls support, and do not replace, the general proofs; no novelty claim.'}
(root/'verification.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
