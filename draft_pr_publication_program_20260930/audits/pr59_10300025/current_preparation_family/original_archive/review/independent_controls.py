"""Independent exact finite controls for the countable exhaustion argument.

No author verifier is imported. Finite controls do not prove the infinite theorem.
"""
from fractions import Fraction as F
from bisect import bisect_right
from collections import Counter
from pathlib import Path
import json, random, hashlib

counts=Counter()
def check(label, condition):
    assert condition, label
    counts[label]+=1

class Map:
    def __init__(self, x, y):
        self.x=tuple(map(F,x)); self.y=tuple(map(F,y))
        self.sign=1 if self.y[-1]>self.y[0] else -1
        assert all(a<b for a,b in zip(self.x,self.x[1:]))
        assert all(self.sign*(b-a)>0 for a,b in zip(self.y,self.y[1:]))
    def at(self,x):
        x=F(x)
        i=max(0,min(len(self.x)-2,bisect_right(self.x,x)-1))
        return self.y[i]+(x-self.x[i])*(self.y[i+1]-self.y[i])/(self.x[i+1]-self.x[i])
    def inv(self):
        if self.sign==1:return Map(self.y,self.x)
        return Map(self.y[::-1],self.x[::-1])

rng=random.Random(10300025)
maps=[]
# Unequal rational slopes, large shifts, alternating orientation, common fixed
# point cases, and finite identity/reflection cases.
for k in range(12):
    xs=[F(-9),F(-3),F(0),F(2),F(11)]
    ys=[F(rng.randint(-30,30))]
    for _ in range(4):ys.append(ys[-1]+F(rng.randint(1,19),rng.randint(1,7)))
    if k%2:ys=[-y for y in ys]
    maps.append(Map(xs,ys))
maps.extend([Map([-1,1],[-1,1]),Map([-1,1],[1,-1]),Map([-1,1],[-F(1,100),F(1,100)])])
invs=[f.inv() for f in maps]
for f,g in zip(maps,invs):
    for q in range(-20,21):
        x=F(q,7)
        check('inverse_identity',g.at(f.at(x))==x and f.at(g.at(x))==x)

R=[F(0),F(1)]
for n in range(1,23):
    candidates=[R[n]+1]
    for j in range(min(n,len(maps))):
        candidates.extend(abs(g.at(s*R[n])) for g in (maps[j],invs[j]) for s in (-1,1))
    R.append(max(candidates)+F(3,2))
H=Map([-r for r in R[:0:-1]]+R,list(range(-len(R)+1,len(R))))
for n in range(len(R)-1):
    check('radii_escape',R[n+1]>R[n]+1 if n else R[1]==1)
    check('integer_coordinate_knots',H.at(R[n])==n and H.at(-R[n])==-n)

for j,(f,inv) in enumerate(zip(maps,invs),1):
    for n in range(j,len(R)-1):
        for g in (f,inv):
            for sign in (-1,1):
                check('both_image_inclusions',abs(g.at(sign*R[n]))<R[n+1])
    samples=[]
    for n in range(j+1,len(R)-2):
        for sign in (-1,1):
            for k in range(9):
                x=sign*(R[n]+F(k,8)*(R[n+1]-R[n]))
                fx=f.at(x); samples.append(x)
                check('annular_lower',abs(fx)>=R[n-1])
                check('annular_upper',abs(fx)<R[n+2])
                check('orientation_tail',f.sign*x*fx>0)
                check('tail_error',abs(H.at(fx)-f.sign*H.at(x))<=2)
    # Complete finite PL certificate on the core: the error is affine between
    # knots of H, knots of f and inverse images of knots of H.
    radius=R[j+1]
    knots={-radius,radius}
    knots.update(x for x in H.x+f.x if -radius<x<radius)
    knots.update(inv.at(y) for y in H.x if -radius<inv.at(y)<radius)
    for x in sorted(knots):
        check('exact_core_bound',abs(H.at(f.at(x))-f.sign*H.at(x))<=2*j+3)
    samples+=sorted(knots)
    for i,x in enumerate(samples):
        y=samples[(i*37+11)%len(samples)]
        e1=H.at(f.at(x))-f.sign*H.at(x)
        e2=H.at(f.at(y))-f.sign*H.at(y)
        defect=abs(abs(H.at(f.at(x))-H.at(f.at(y)))-abs(H.at(x)-H.at(y)))
        check('two_point_reduction',defect<=abs(e1)+abs(e2)<=4*j+6)

# Exact negative control: image inclusions alone with radii 2n do not stop
# contraction from producing an unbounded conjugated displacement.
for n in (10,100,1000):
    x=F(2*n); fx=x/100
    check('forward_only_not_sufficient',abs(fx)<2*(n+1) and abs(fx/2-x/2)==F(99*n,100))
    check('reflection_needs_signed_reference',abs(-x-x)==2*x and abs(-x-(-1)*x)==0)

result={'assertions_passed':sum(counts.values()),'by_category':dict(counts),
        'maps':len(maps),'radii':len(R),'seed':10300025,'arithmetic':'exact rational',
        'limitations':'Finite diagnostics plus exact core certificates; infinite/countable conclusion rests on the proof.'}
Path(__file__).with_name('independent_controls.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
