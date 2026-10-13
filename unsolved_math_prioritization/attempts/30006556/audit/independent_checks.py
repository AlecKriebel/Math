#!/usr/bin/env python3
"""Independent exact controls. Standard library; no author code imported.
Finite enumeration is diagnostic, not a proof of the universal conjecture.
"""
from collections import Counter
from fractions import Fraction as F
from itertools import combinations, product
from math import isqrt, comb, gcd
import json

class Box:
    def __init__(self,a,b=None): self.a,self.b=F(a),F(a if b is None else b); assert self.a<=self.b
    def __add__(self,z):
        z=box(z); return Box(self.a+z.a,self.b+z.b)
    __radd__=__add__
    def __neg__(self): return Box(-self.b,-self.a)
    def __sub__(self,z): return self+-box(z)
    def __rsub__(self,z): return box(z)+-self
    def __mul__(self,z):
        z=box(z); v=[a*b for a in [self.a,self.b] for b in [z.a,z.b]]; return Box(min(v),max(v))
    __rmul__=__mul__
    def __truediv__(self,z):
        z=box(z); assert z.a*z.b>0; return self*Box(1/z.b,1/z.a)
    def __pow__(self,n):
        if n==0:return Box(1)
        if n%2==0 and self.a<0<self.b:return Box(0,max(abs(self.a),abs(self.b))**n)
        v=[self.a**n,self.b**n];return Box(min(v),max(v))
    def sqrt(self):
        assert self.a>=0; scale=10**30
        lo=isqrt(self.a.numerator*scale*scale//self.a.denominator)
        hi=isqrt(self.b.numerator*scale*scale//self.b.denominator)+1
        assert F(lo,scale)**2<=self.a and F(hi,scale)**2>=self.b
        return Box(F(lo,scale),F(hi,scale))
    def above(self,z):return self.a>box(z).b
    def compact(self):
        scale=10**12
        return [str(F(self.a.numerator*scale//self.a.denominator,scale)),str(F(-(-self.b.numerator*scale//self.b.denominator),scale))]
def box(z):return z if isinstance(z,Box) else Box(z)

def atan_small(x):
    # Alternating-series enclosure; all 60 terms decrease in magnitude.
    vals=[(-1)**j*x**(2*j+1)/(2*j+1) for j in range(61)]
    s=sum(vals[:60]);return Box(s,s+vals[60])

def cos_small(t):
    assert 0<=t.a<=t.b<1
    # cos decreases on [0,1]; direct exact Taylor bounds at the endpoints.
    def bounds(x):
        term=F(1);s=term
        for j in range(1,25):
            term=-term*x*x/((2*j-1)*(2*j));s+=term
        nextterm=-term*x*x/(49*50)
        return s+nextterm,s
    return Box(bounds(t.b)[0],bounds(t.a)[1])

def construction():
    # pi/4=2 atan(1/3)+atan(1/7): tangent addition gives 1;
    # all summands place the angle in (0,pi/2).
    pi=8*atan_small(F(1,3))+4*atan_small(F(1,7))
    c=cos_small(pi/21)
    D=(2+2*c).sqrt()
    d=(2+2*(4*c**3-3*c)).sqrt()
    r=-c+(c*c+d*d-1).sqrt(); delta=1-r
    sin_a=(1-c*c).sqrt()
    checks={
      'r_positive':r.above(0),'r_below_one':box(1).above(r),
      'delta_positive':delta.above(0),'inner_minimum_above_delta':(2*r*sin_a).above(delta),
      'inner_patch_separated':(r-2*delta).above(delta),
      'outer_patch_separated':(1-2*delta).above(delta),
      'inner_diameter_below_d':d.above(r*D),'d_below_D':D.above(d),
      'patch_diameter_below_d':d.above(4*delta),'patch_ring_below_d':d.above(1+2*delta)}
    assert all(checks.values())
    patch=[(i,j) for i,j in product(range(-2,3),repeat=2) if max(abs(i),abs(j),abs(i+j))<=2]
    assert len(patch)==19
    assert max(i*i+i*j+j*j for i,j in patch)==4
    hist=Counter((i-k)**2+(i-k)*(j-l)+(j-l)**2 for (i,j),(k,l) in combinations(patch,2))
    assert min(hist)==1 and hist[1]==42 and max(hist)==16
    ring=Counter(min((j-i)%21,(i-j)%21) for i,j in combinations(range(21),2))
    cross=Counter(min((j-i)%21,(i-j)%21) for i,j in product(range(21),repeat=2))
    assert ring[10]==ring[9]==21 and cross[10]==42 and cross[0]==21
    return {'points':61,'unordered_pairs':comb(61,2),'patch_quadratic_form_histogram':dict(sorted(hist.items())),
      'ring_chord_index_histogram':dict(sorted(ring.items())), 'cross_chord_index_histogram':dict(sorted(cross.items())),
      'minimum_multiplicity':hist[1]+cross[0],'second_largest_multiplicity':ring[9]+cross[10],
      'diameter_multiplicity':ring[10],'strict_certificates':checks,
      'enclosures':{name:v.compact() for name,v in [('pi',pi),('cos_alpha',c),('r',r),('delta',delta),('D',D),('d',d)]}}

def counts(points):
    return Counter((x-u)**2+(y-v)**2 for (x,y),(u,v) in combinations(points,2))

def check_set(points):
    c=counts(points);assert 0 not in c
    assert sum(c.values())==comb(len(points),2)
    sparse=sum(v<=len(points) for v in c.values())
    assert sparse>=2, (points,c)
    assert c[max(c)]<=len(points)
    return sparse

def circle_controls():
    q=sorted((x,y) for x,y in product(range(-5,6),repeat=2) if x*x+y*y==25)
    extra=list(product(range(-6,7,2),repeat=2))
    assert len(q)==12 and len(extra)==49 and all(x*x+y*y!=25 for x,y in extra)
    by_n=Counter();where=Counter();mins=99
    for m in range(4,13):
      for a in combinations(q,m):
        for p in extra:
            n=m+1;mins=min(mins,check_set(a+(p,)));by_n[n]+=1
            r2=p[0]**2+p[1]**2
            where['center' if r2==0 else 'interior_noncentral' if r2<25 else 'exterior']+=1
    return {'circle':'All 12 integer points x^2+y^2=25','outliers':'49 even-coordinate grid points in [-6,6]^2',
      'cases':sum(by_n.values()),'by_n':dict(sorted(by_n.items())),'outlier_type':dict(where),
      'minimum_sparse_classes':mins,'counterexamples':0}

def hull_vertices(points):
    # Gift wrapping, keeping only extreme endpoints of collinear edges.
    pts=set(points)
    if len(pts)<3:return pts
    start=min(pts);a=start;out=[]
    while True:
        out.append(a);b=next(q for q in pts if q!=a)
        for q in pts:
            cross=(b[0]-a[0])*(q[1]-a[1])-(b[1]-a[1])*(q[0]-a[0])
            dist=lambda p:(p[0]-a[0])**2+(p[1]-a[1])**2
            if cross<0 or (cross==0 and dist(q)>dist(b)):b=q
        a=b
        if a==start:break
        assert len(out)<=len(pts)
    return set(out)

def collinear_number(points):
    best=1
    for x,y in points:
        directions=Counter()
        for u,v in points:
            if (x,y)==(u,v):continue
            dx,dy=u-x,v-y;g=gcd(abs(dx),abs(dy));dx//=g;dy//=g
            if dx<0 or (dx==0 and dy<0):dx,dy=-dx,-dy
            directions[dx,dy]+=1
        best=max(best,1+max(directions.values(),default=0))
    return best

def lattice_controls():
    # A non-square 3 by 5 grid, distinct from the author's 4 by 4 family.
    p=list(product(range(3),range(5)));by_n={};mins=99;line=0
    for n in range(5,16):
      cases=0
      for a in combinations(p,n):
        mins=min(mins,check_set(a));cases+=1
        c=counts(a)
        maxline=collinear_number(a)
        h1=hull_vertices(a);h2=hull_vertices(set(a)-h1)
        bound=min(F(3,2)*(len(h1)+len(h2)),F(4,3)*len(h1)+2*len(h2),2*len(h1)+len(h2))
        assert c[sorted(c)[-2]]<=bound
        if maxline>=n//2+1:
            assert len(c)>=n//2+1;line+=1
      by_n[n]=cases
    return {'grid':'{0,1,2} x {0,1,2,3,4}','cases':sum(by_n.values()),'by_n':by_n,
      'minimum_sparse_classes':mins,'all_direction_line_criterion_cases':line,'hull_layer_controls':sum(by_n.values()),'counterexamples':0}

def reflection_controls():
    total=closed=0
    # Test every subset of cyclic angle grids through order 15. A regular
    # subset must be exactly one congruence class modulo its common gap.
    for N in range(4,16):
      for mask in range(1<<N):
        if mask.bit_count()<4:continue
        A={i for i in range(N) if mask>>i&1};total+=1
        if all((2*a-b)%N in A for a in A for b in A):
            closed+=1;s=sorted(A);gaps=[(s[(i+1)%len(s)]-s[i])%N for i in range(len(s))]
            assert len(set(gaps))==1,(N,A)
    return {'subsets':total,'reflection_closed_subsets':closed,'all_closed_subsets_regular':True}

def center_controls():
    # Exhaust all four-gap orderings from the proof, in units pi/3.
    tested=0;bad=0
    for k in range(1,5):
        theta=1+F(2,k)
        for where in combinations(range(4),k):
            gaps=[theta if i in where else F(1) for i in range(4)]; assert sum(gaps)==6
            angles=[0]
            for g in gaps[:-1]:angles.append(angles[-1]+g)
            lengths={min(abs(a-b),6-abs(a-b)) for a,b in combinations(angles,2)}
            assert not lengths<={F(1),theta};tested+=1
    # For m=5 saturation gives a full +/-pi/3 orbit, containing six points.
    orbit={j%6 for j in range(6)};assert len(orbit)==6
    return {'four_point_gap_orderings_rejected':tested,'five_point_required_orbit_size':len(orbit)}

def algebra_controls():
    checks=0
    for m in range(4,504):
        for x in [F(-1,2),F(0),F(1,3),F(1),F(7,4),F(5),1+F(6,m-1)]:
            y=m*(x-1)
            assert m*(1+4*x+x*x)-(6*m+y*y)==-m*(x-1)*((m-1)*(x-1)-6)
            checks+=1
        z=F(6,m-1);assert z<3 # equivalent to impossible 2 <= sqrt(1+z)
    # Joined unit equilateral triangles, coordinates in Q(sqrt(3)).
    p=[(F(0),F(0)),(F(1),F(0)),(F(1,2),F(1,2)),(F(1,2),F(-1,2))]
    hist=Counter((x-u)**2+3*(y-v)**2 for (x,y),(u,v) in combinations(p,2))
    assert hist=={F(1):5,F(3):1}
    return {'moment_identity_values':checks,'strict_moment_obstructions':500,
      'n4_control_squared_distances':{str(k):v for k,v in sorted(hist.items())}}

def source_graph_control():
    # Refutes the external working draft's graph lemma, not any planar claim.
    cycles=[(0,1,2,3),(0,4,5,6,7)]
    edges={tuple(sorted((c[i],c[(i+1)%len(c)]))) for c in cycles for i in range(len(c))}
    degree=Counter(v for edge in edges for v in edge)
    assert len(degree)==8 and len(edges)==9
    assert sorted(degree.values())==[2,2,2,2,2,2,2,4]
    return {'vertices':8,'edges':9,'degree_sequence':sorted(degree.values()),'vertices_degree_at_least_3':1,
      'claimed_euclidean_realization':False}

if __name__=='__main__':
    out={'problem_id':30006556,'independent_code':True,'author_code_imported':False,'general_problem_solved':False,
      'construction':construction(),'external_source_graph_counterexample':source_graph_control(),'algebra':algebra_controls(),'center':center_controls(),
      'reflection':reflection_controls(),'lattice':lattice_controls(),'circle':circle_controls()}
    print(json.dumps(out,indent=2,sort_keys=True))
