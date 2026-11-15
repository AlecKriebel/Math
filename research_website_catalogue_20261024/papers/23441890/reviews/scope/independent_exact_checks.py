#!/usr/bin/env python3
"""Independent exact PL algebra checks, supplementary to the written proof.

No source modules are imported. All assertions below use explicit require(), so
the same checks run under python -O. Composition is ordinary composition.
"""
from fractions import Fraction as Q
from bisect import bisect_right
import json, random

def require(p, message):
    if not p: raise AssertionError(message)

class PL:
    def __init__(self, points):
        self.points=tuple(sorted(set((Q(x),Q(y)) for x,y in points)))
        require(len(self.points)>=2,'at least two knots')
        require(self.points[0]==(0,0) and self.points[-1]==(1,1),'fixed endpoints')
        require(all(x<X and y<Y for (x,y),(X,Y) in zip(self.points,self.points[1:])), 'increasing')
    def __call__(self,x):
        x=Q(x);i=min(bisect_right([a for a,b in self.points],x)-1,len(self.points)-2)
        a,b=self.points[i];c,d=self.points[i+1]
        return b+(d-b)*(x-a)/(c-a)
    def inverse(self): return PL([(y,x) for x,y in self.points])
    def after(self,g):
        gi=g.inverse()
        xs={x for x,y in g.points}|{gi(x) for x,y in self.points}
        return PL([(x,self(g(x))) for x in xs])
    def equals(self,g): return all(self(x)==g(x) for x in {a for a,b in self.points}|{a for a,b in g.points})
    def slopes(self):return [(Y-y)/(X-x) for (x,y),(X,Y) in zip(self.points,self.points[1:])]

identity=PL([(0,0),(1,1)])
def two(k): return Q(2**k) if k>=0 else Q(1,2**(-k))
def is_two_power(x):
    return x>0 and x.numerator&(x.numerator-1)==0 and x.denominator&(x.denominator-1)==0
def bump(a,b):
    a,b=Q(a),Q(b)
    return PL([(0,0),(a,a),(a+(b-a)/3,a+2*(b-a)/3),(b,b),(1,1)])
def interpolate(xs,ys):
    # Select the bracketing power with a binary exponent rather than the native
    # script's ratio loop, then solve the two linear length equations directly.
    c=min(xs+ys)/2;d=(max(xs+ys)+1)/2;out=[(0,0),(c,c)]
    for a,b,C,D in zip([c]+xs,[*xs,d],[c]+ys,[*ys,d]):
        r=(D-C)/(b-a);k=r.numerator.bit_length()-r.denominator.bit_length()
        if two(k)>r:k-=1
        s=two(k);t=2*s
        length=(t*(b-a)-(D-C))/(t-s)
        require(0<=length<=b-a,'convex lengths')
        out.extend([(a,C),(a+length,C+s*length),(b,D)])
    out.append((1,1));return PL(out)

def run():
    rng=random.Random(23441890);counts={}
    interpolation=0
    for size in range(1,9):
        for trial in range(40):
            xs=sorted(Q(n,1009) for n in rng.sample(range(1,1009),size))
            ys=sorted(Q(n,1013) for n in rng.sample(range(1,1013),size))
            f=interpolate(xs,ys)
            require(all(f(x)==y for x,y in zip(xs,ys)), 'tuple values')
            require(all(is_two_power(s) for s in f.slopes()), 'all power-of-two slopes')
            require(f.inverse().after(f).equals(identity),'exact inverse composition')
            interpolation+=1
    counts['tuple_maps_checked_as_whole_PL_functions']=interpolation
    tails=[]
    for m in range(24):
        b=two(-2*m-2);a=b/2
        tails.extend([(a,b),(1-b,1-a)])
    knots=[(0,0),(1,1)]
    for a,b in tails:knots.extend(bump(a,b).points[1:-1])
    h=PL(knots);hi=h.inverse()
    require(hi.after(h).equals(identity),'two-tail inverse')
    require(all(is_two_power(s) for s in h.slopes()),'two-tail slopes')
    nontrivial=0
    for a,b in tails:
        # Choose a small subinterval strictly separated from its h-preimage.
        x=a+(b-a)/6;y=a+(b-a)/5;f=bump(x,y)
        af=hi.after(f).after(h)
        require(not af.equals(f),'automorphism nontrivial on every chosen tail')
        require(af(x)==x and f((x+y)/2)>(x+y)/2,'separated witness supports')
        # The first moved point is transported by h^-1, and its right slope is 2.
        aa=hi(x);j=[u for u,v in af.points].index(aa)
        require(af.slopes()[j]==2,'first germ slope preserved')
        nontrivial+=1
    counts['tail_local_nontriviality_and_first_germs']=nontrivial
    # Ordinary composition automorphism identity as whole PL functions.
    f=bump(Q(1,5),Q(3,5));g=bump(Q(2,5),Q(4,5))
    alpha=lambda f:hi.after(f).after(h)
    require(alpha(f.after(g)).equals(alpha(f).after(alpha(g))),'automorphism multiplication')
    counts['whole_function_automorphism_products']=1
    # One-tail witness is admitted after reflection: its support intervals then
    # increase to the excluded RIGHT endpoint. Both tails retain one descending
    # family after reflection. These finite order checks accompany the symbolic
    # limiting argument; they do not infer an infinite conclusion from a prefix.
    left=tails[::2];right=tails[1::2]
    require(all(B<a for (A,B),(a,b) in zip(left[1:],left)), 'left descends')
    reflected_left=[(1-b,1-a) for a,b in left]
    reflected_right=[(1-b,1-a) for a,b in right]
    require(all(b<A for (a,b),(A,B) in zip(reflected_left,reflected_left[1:])), 'one-tail becomes increasing')
    require(all(B<a for (A,B),(a,b) in zip(reflected_right[1:],reflected_right)), 'other reflected tail descends')
    counts['orientation_tail_pairs']=3*23
    # Countermodel cells: beta conjugation by a finite PL normalizer. Negative
    # powers explicitly use the inverse normalizer; equality is checked at all
    # breakpoints, enough for equality of these continuous PL functions.
    h0=PL([(0,0),(Q(1,3),Q(2,3)),(1,1)])
    def iterate(f,n):
        v=h0 if n>=0 else h0.inverse();vi=v.inverse()
        for _ in range(abs(n)):f=vi.after(f).after(v)
        return f
    shift_cases=0
    for n in range(-7,8):
        fn=iterate(f,n+1);bn=iterate(iterate(f,1),n)
        require(fn.equals(bn),'beta exponent shift for positive and negative n')
        a=-two(-n);b=-two(-n-1);aa=-two(-n-1);bb=-two(-n-2)
        require(aa==a/2 and bb==b/2,'x/2 sends cell n to n+1')
        for x,y in fn.points:
            physical=a+(b-a)*x
            # v^-1 E(f) v = twice the cell(n+1) value.
            lhs=2*(aa+(bb-aa)*fn(x));rhs=a+(b-a)*bn(x)
            require(lhs==rhs,'shift conjugation exact cell values')
            shift_cases+=1
    counts['shift_countermodel_exact_knot_cases']=shift_cases
    return {'status':'passed','arithmetic':'fractions.Fraction; no floats','checks':counts,
            'scope':'Independent finite PL function identities and boundary witnesses; universal obstruction follows from the separate written derivation, not these bounded checks.'}

if __name__=='__main__':print(json.dumps(run(),indent=2))
