#!/usr/bin/env python3
"""Independent exact audit. No author verifier imports, floating point, or packages.

Numbers are pairs a+b*sqrt(2). Order is proved by isolating sqrt(2) in
rational intervals, distinct from the author's direct sign-by-squaring code.
Chords are found by edge/line intersections, not half-space segment clipping.
"""
from fractions import Fraction as F
from functools import total_ordering
from pathlib import Path
import json


def need(value, label):
    if not value:
        raise RuntimeError(label)


@total_ordering
class R:
    __slots__ = ('a', 'b')
    def __init__(self, a=0, b=0):
        if isinstance(a,R): self.a,self.b=a.a,a.b
        else: self.a,self.b=F(a),F(b)
    def __add__(self,z):
        z=R(z); return R(self.a+z.a,self.b+z.b)
    __radd__=__add__
    def __neg__(self):return R(-self.a,-self.b)
    def __sub__(self,z):return self+-R(z)
    def __rsub__(self,z):return R(z)+-self
    def __mul__(self,z):
        z=R(z);return R(self.a*z.a+2*self.b*z.b,self.a*z.b+self.b*z.a)
    __rmul__=__mul__
    def __truediv__(self,z):
        z=R(z);den=z.a*z.a-2*z.b*z.b
        if den==0:raise ZeroDivisionError
        return self*R(z.a/den,-z.b/den)
    def __eq__(self,z):
        z=R(z);return self.a==z.a and self.b==z.b
    def __hash__(self):return hash((self.a,self.b))
    def __lt__(self,z):
        d=self-R(z)
        if d.b==0:return d.a<0
        lo,hi=F(1),F(2)
        while True:
            x,y=d.a+d.b*lo,d.a+d.b*hi
            if max(x,y)<0:return True
            if min(x,y)>0:return False
            mid=(lo+hi)/2
            if mid*mid<2:lo=mid
            else:hi=mid
    def data(self):return [str(self.a),str(self.b)]


def vec(p,q):return (q[0]-p[0],q[1]-p[1])
def dot(p,q):return p[0]*q[0]+p[1]*q[1]
def cross(p,q):return p[0]*q[1]-p[1]*q[0]

def line_chord(vertices,axis,value,side):
    """Intersect polygon EDGES with an axis line; sort and clip endpoints."""
    hits=[]
    for i,p in enumerate(vertices):
        q=vertices[(i+1)%len(vertices)]
        if p[axis]==q[axis]:
            if p[axis]==value:hits.extend([p[1-axis],q[1-axis]])
        else:
            t=(value-p[axis])/(q[axis]-p[axis])
            if 0<=t<=1:hits.append(p[1-axis]+t*(q[1-axis]-p[1-axis]))
    if not hits:return None
    lo,hi=max(R(0),min(hits)),min(side,max(hits))
    return None if hi<lo else (lo,hi)


def configuration(h=F(101,100),delta=F(1,100),cx=None):
    h,delta=R(h),R(delta); side=4*h
    cx=2*h if cx is None else R(cx)
    r=R(0,F(1,2));cy=r-delta
    vertices=[(cx-r,cy),(cx,cy-r),(cx+r,cy),(cx,cy+r)]
    edges=[vec(p,vertices[(i+1)%4]) for i,p in enumerate(vertices)]
    need(all(dot(e,e)==1 for e in edges),'Unit side length')
    need(all(dot(e,edges[(i+1)%4])==0 for i,e in enumerate(edges)),'Right angles')
    area=sum((cross(p,vertices[(i+1)%4]) for i,p in enumerate(vertices)),R())/2
    need(area==1,'Unit area')
    records=[]; boundary=[];positive=[];total=R()
    for axis in (0,1):
        for k in range(5):
            interval=line_chord(vertices,axis,k*h,side)
            length=R() if interval is None else interval[1]-interval[0]
            rec={'fixed_coordinate':'x' if axis==0 else 'y','index':k,'interval':None if interval is None else [v.data() for v in interval],'length':length.data()}
            records.append(rec)
            if interval is not None and k in (0,4):boundary.append((axis,k))
            if length>0:positive.append((axis,k))
            total+=length
    return dict(h=h,delta=delta,side=side,cx=cx,cy=cy,r=r,vertices=vertices,records=records,boundary=boundary,positive=positive,total=total)


def valid_counterexample(q):
    return q['h']>1 and q['boundary']==[(1,0)] and q['records'][5]['interval'] is not None and R(*q['records'][5]['length'])>0 and q['total']>R(0,F(3,2))


def main():
    q=configuration();rt=R(0,1)
    need(valid_counterexample(q),'Central certificate')
    need(q['positive']==[(0,2),(1,0),(1,1)],'Exactly three positive chords')
    need(q['total']==R(F(-203,100),3),'Total grid length')
    need(q['total']-R(0,F(3,2))==R(F(-203,100),F(3,2)),'Exact excess')
    need(F(9,2)>F(41209,10000),'Independent squared comparison')
    # The lower outside cap is a triangle with height delta and base 2*delta.
    outside_vertices=[q['vertices'][1],(q['cx']+q['delta'],R()),(q['cx']-q['delta'],R())]
    outside_area=sum((cross(p,outside_vertices[(i+1)%3]) for i,p in enumerate(outside_vertices)),R())/2
    need(outside_area==R(F(1,10000)),'Exact spill triangle')
    need(all(0<p[0]<q['side'] and p[1]<q['side'] for p in q['vertices']),'No other target sides')
    need(q['vertices'][1][1]<0,'Positive crossing rather than tangency')
    # Exact boundary-centred control attains the published constant.
    central=configuration(delta=F(0))
    need(not valid_counterexample(central),'Tangency rejected for positive-contact certificate')
    # Separate shape centred on y=0 uses delta=r, an algebraic parameter.
    centred=configuration(delta=R(0,F(1,2)))
    need(centred['total']==R(0,F(3,2)),'Boundary-centred equality control')
    controls=[configuration(h=F(6,5)),configuration(delta=F(1,2)),configuration(cx=0)]
    need(all(not valid_counterexample(x) for x in controls),'Reject nonviolating or wrong-boundary controls')
    nearby=[F(1000000001,1000000000),F(100001,100000),F(21,20),F(211,200)]
    need(all(valid_counterexample(configuration(h=x)) for x in nearby),'Nearby rational examples')
    # Exact arithmetic stress controls, including almost cancelling radicals.
    need(rt*rt==2 and (1+rt)/(1+rt)==1,'Field identities')
    need(R(-1414213562373095,1000000000000000)>0,'Small positive sign')
    need(R(1414213562373095,-1000000000000000)<0,'Small negative sign')
    # Source-definition covering context: integer 5 by 5 tiling covers [0,5]^2.
    need(0<q['side']<5,'Finite-cover containment witness')
    # Stronger context witness: Q can be ESSENTIAL, not merely appended redundantly.
    # Six bottom-row tiles cover outside a narrow slit up to height 1.
    # Twenty-five tiles with bottom heights eta+j cover everything above eta.
    eta=R(F(1,200)); left=q['cx']-eta; right=q['cx']+eta
    bottom_starts=[R(0),R(1),left-1,right,right+1,right+2]
    need(bottom_starts[0]==0 and bottom_starts[1]<=bottom_starts[0]+1
         and bottom_starts[2]<=bottom_starts[1]+1,'Left bottom interval union')
    need(bottom_starts[2]+1==left and bottom_starts[-1]+1>q['side'],
         'Slit is sole bottom-row gap')
    need(eta+5>q['side'] and eta<1,'Upper grid covers remainder')
    slit_vertices=[(x,y) for x in (left,right) for y in (R(0),eta)]
    absr=lambda x: -x if x<0 else x
    need(all(absr(x-q['cx'])+absr(y-q['cy'])<=q['r'] for x,y in slit_vertices),
         'Convex slit rectangle lies in Q')
    need(all(not (x<=q['cx']<=x+1) for x in bottom_starts),'Bottom tiles miss witness')
    need(eta>0,'Upper tiles miss witness (cx,0)')
    # Supplemental scalar observations checked exactly; general arguments in audit.
    for n in range(2,301):
        s=F(n)+F(1,4*n);N=n*n+1
        need(0<N-s*s<1,'Area relaxation')
        need((n+1)**2==N+2*n,'Incidence relaxation')
        need(R(2*(n+1)*s)<2*rt*N,'Length relaxation')
        k=n-2
        need(8*n**3-20*n**2+23*n-5==8*k**3+28*k**2+39*k+25,'Polynomial identity')
    # Rational Pythagorean angles test supplementary n=1 and two-line formulas.
    pythagorean_tests=0
    for j in range(1,41):
        u=F(j,100);c=(1-u*u)/(1+u*u);t=2*u/(1+u*u)
        need(c>=t>0 and c*c+t*t==1,'Pythagorean orientation')
        s=(1+1/c)/2
        a=(1-s*c)/t;b=(1-s*t)/c
        need(a+b==(c+t-s)/(c*t)<2/(c+t+1)<1,'n=1 edge-sum identity')
        h=(1+c+t)/2
        need((c+t-h)/(c*t)<2/(c+t+1)<1,'Two-parallel-line bound')
        pythagorean_tests+=1
    result={'status':'PASS','scope':'Independent exact local-lemma certificate; original covering conjecture unresolved','arithmetic':'Q(sqrt(2)) pairs; signs by rational root isolation','geometry':'Independent polygon-edge/axis-line intersection','coefficient_encoding':'[rational, coefficient of sqrt(2)]','n':4,'h':q['h'].data(),'side':q['side'].data(),'vertices':[[v.data() for v in p] for p in q['vertices']],'grid_chords':q['records'],'boundary_sides':['bottom'],'positive_boundary_length':['1/50','0'],'total':q['total'].data(),'claimed_bound':['0','3/2'],'excess':(q['total']-R(0,F(3,2))).data(),'outside_area':outside_area.data(),'full_cover_context':{'axis_aligned_unit_squares':25,'plus_certificate_tile':1,'contains_target':True,'is_17_tile_cover':False,'essential_tile_alternative':{'total_tiles':32,'certificate_tile_unique_at':['101/50','0'],'slit_half_width':'1/200','upper_grid_bottom':'1/200','verified_whole_target_containment_by_rectangular_decomposition':True}},'checks':{'negative_controls':4,'equality_control':True,'nearby_rational_examples':len(nearby),'relaxation_n_range':[2,300],'rational_angle_controls':pythagorean_tests},'author_code_imported':False}
    text=json.dumps(result,indent=2,sort_keys=True)+'\n'
    expected=Path(__file__).with_name('independent_results.json')
    if expected.exists():need(expected.read_text()==text,'Recorded independent result mismatch')
    print(text,end='')

if __name__=='__main__':main()
