#!/usr/bin/env python3
"""Exact rational certificate: at least five alpha=16 cube-move centers.

Only Python integers, Fraction, and isqrt enter any pass/fail decision.
Printed decimal estimates are explanatory only.
"""
from fractions import Fraction as Q
from math import isqrt
from pathlib import Path
import json

class I:
    def __init__(self,a,b=None):
        self.a=Q(a);self.b=self.a if b is None else Q(b)
        assert self.a<=self.b
    def __add__(self,o):
        o=coerce(o);return I(self.a+o.a,self.b+o.b)
    __radd__=__add__
    def __neg__(self):return I(-self.b,-self.a)
    def __sub__(self,o):return self+-coerce(o)
    def __rsub__(self,o):return coerce(o)+-self
    def __mul__(self,o):
        o=coerce(o);v=[self.a*o.a,self.a*o.b,self.b*o.a,self.b*o.b];return I(min(v),max(v))
    __rmul__=__mul__
    def __truediv__(self,o):
        o=coerce(o);assert o.a*o.b>0
        return self*I(1/o.b,1/o.a)
    def square(self):
        return I(0 if self.a<=0<=self.b else min(self.a*self.a,self.b*self.b),max(self.a*self.a,self.b*self.b))
    def pow(self,n):
        assert n>=0
        if n==0:return I(1)
        if n%2==0:return self.square().pow(n//2)
        return self*self.pow(n-1)
    def sign(self):return 1 if self.a>0 else -1 if self.b<0 else 0
    def data(self):return {'lower':str(self.a),'upper':str(self.b),'decimal_bounds':[float(self.a),float(self.b)]}

def coerce(x):return x if isinstance(x,I) else I(x)

checks=0
def verify(condition):
    global checks
    assert condition
    checks+=1

def eighth(q,bits=200):
    q=Q(q);verify(q>=0)
    if q==0:return I(0)
    scale=1<<bits
    z=(q.numerator<<(8*bits))//q.denominator
    k=isqrt(isqrt(isqrt(z)))
    lo,hi=Q(k,scale),Q(k+1,scale)
    verify(lo**8<=q<hi**8)
    return I(lo,hi)

def eighth_interval(v):
    v=coerce(v)
    return I(eighth(v.a).a,eighth(v.b).b)

B=Q(2073,10000)
cx=Q(4719,10000)
cy=Q(64,10000)
lam=Q(27,1250)
mu=Q(1)

def outgoing_box(s):
    s=coerce(s)
    u,v,w=eighth_interval(s),eighth_interval(s+lam),eighth_interval(s+mu)
    x=(B*B+u-v)/(2*B)
    y=(cx*cx+cy*cy+u-w-2*cx*x)/(2*cy)
    return (x,y),x.square()+y.square()-u

def scalar_residual(s):return outgoing_box(s)[1]

def monotone_level_root(dx,dy,height,level,steps=160):
    """Point t*(dx,dy)+height*J(dx,dy); focused difference target."""
    norm2=dx*dx+dy*dy
    def f(t):
        return norm2**8*(((t-1)**2+height*height)**8-(t*t+height*height)**8)-level
    lo,hi=Q(-1),Q(1)
    while f(lo)<=0:lo*=2
    while f(hi)>=0:hi*=2
    for _ in range(steps):
        mid=(lo+hi)/2
        if f(mid)>0:lo=mid
        else:hi=mid
    verify(f(lo)>0>f(hi))
    return I(lo,hi),{'t_interval':[str(lo),str(hi)],'polynomial_signs':[1,-1],
                      'dx':str(dx),'dy':str(dy),'height':str(height),'level':str(level)}

def point(base,dx,dy,h,t):
    return (I(base[0])+t*dx-h*dy,I(base[1])+t*dy+h*dx)

def sub(p,q):return (p[0]-q[0],p[1]-q[1])
def det(u,v):return u[0]*v[1]-u[1]*v[0]
def norm16(p):return (p[0].square()+p[1].square()).pow(8)

cutpoints=[Q(9,10000),Q(11,10000),Q(13,10000),Q(1,2),Q(1),Q(10**17)]
expected=[1,-1,1,-1,1,-1]
root_checks=[]
for s,sgn in zip(cutpoints,expected):
    g=scalar_residual(s)
    verify(g.sign()==sgn)
    root_checks.append({'s':str(s),'sign':sgn,'G_interval':g.data()})

# A1 has focus difference C-A=mu, A3 B-A=lambda,
# A5 C-B=mu-lambda. The offsets keep the odd points well separated.
t1,r1=monotone_level_root(cx,cy,Q(10),mu)
t3,r3=monotone_level_root(B,Q(0),Q(1),lam)
dx,dy=cx-B,cy
t5,r5=monotone_level_root(dx,dy,Q(-10),mu-lam)
A1=point((0,0),cx,cy,Q(10),t1)
A2=(I(0),I(0))
A3=point((0,0),B,Q(0),Q(1),t3)
A4=(I(B),I(0))
A5=point((B,0),dx,dy,Q(-10),t5)
A6=(I(cx),I(cy))
points=[A1,A2,A3,A4,A5,A6]
for i,P in enumerate(points):
    for R in points[:i]:
        verify(any(P[k].b<R[k].a or R[k].b<P[k].a for k in range(2)))
even_area=det(sub(A4,A2),sub(A6,A2))
odd_area=det(sub(A3,A1),sub(A5,A1))
verify(even_area.sign()!=0)
verify(odd_area.sign()!=0)

# All common-focus centers lie in x<B/2 because lambda>0.
verify(A1[0].a>B/2)
verify(A5[0].a>B/2)
# The remaining odd point satisfies the B level, but not the C level.
third_residual=norm16(sub(A3,A6))-norm16(A3)-mu
verify(third_residual.sign()!=0)
# No even focus is a center: lambda,mu>0 exclude B,C; A fails B level.
verify(lam>0 and mu>0 and B**16!=lam)

# Stronger than the required alternating-triple condition: no boundary triple
# is collinear. This also rules out overlapping consecutive boundary edges.
for i in range(6):
    for j in range(i):
        for k in range(j):
            verify(det(sub(points[i],points[k]),sub(points[j],points[k])).sign()!=0)

# Refine five IVT intervals without presuming monotonicity or unique roots.
# Each retained interval still has opposite strict signs, hence contains a root.
centers=[]
for lo,hi,leftsign in zip(cutpoints[:-1],cutpoints[1:],expected[:-1]):
    for _ in range(100):
        mid=(lo+hi)/2
        sg=scalar_residual(mid).sign()
        verify(sg!=0)
        if sg==leftsign:lo=mid
        else:hi=mid
    verify(scalar_residual(lo).sign()==leftsign)
    verify(scalar_residual(hi).sign()==-leftsign)
    box,_=outgoing_box(I(lo,hi))
    for P in points:
        verify(any(box[k].b<P[k].a or P[k].b<box[k].a for k in range(2)))
    for old in centers:
        P=old['box']
        verify(any(box[k].b<P[k].a or P[k].b<box[k].a for k in range(2)))
    # No center is on the line through any boundary pair.
    for i,P in enumerate(points):
        for R in points[:i]:verify(det(sub(box,P),sub(R,P)).sign()!=0)
    centers.append({'s_interval':[str(lo),str(hi)],'box':box})

# Certify an incoming center independently of the published flip theorem.
# Common focus A3; other foci A5 and A1. Boundary data give its levels.
L=norm16(sub(A4,A5))-norm16(sub(A4,A3))
M=norm16(sub(A2,A1))-norm16(sub(A2,A3))
verify(L.a>0 and M.a>0)
b,c=sub(A5,A3),sub(A1,A3)
D=det(b,c)
verify(D.sign()!=0)
def incoming_box(s):
    s=coerce(s)
    u=eighth_interval(s)
    v=eighth_interval(s+L)
    w=eighth_interval(s+M)
    R1=b[0].square()+b[1].square()+u-v
    R2=c[0].square()+c[1].square()+u-w
    x=(R1*c[1]-R2*b[1])/(2*D)
    y=(b[0]*R2-c[0]*R1)/(2*D)
    return (A3[0]+x,A3[1]+y),x.square()+y.square()-u
inlo,inhi=Q(1,100),Q(11,1000)
_,ginlo=incoming_box(inlo)
_,ginhi=incoming_box(inhi)
verify(ginlo.sign()*ginhi.sign()==-1)
inbox,_=incoming_box(I(inlo,inhi))
for P in points:
    verify(any(inbox[k].b<P[k].a or P[k].b<inbox[k].a for k in range(2)))
for i,P in enumerate(points):
    for R in points[:i]:verify(det(sub(inbox,P),sub(R,P)).sign()!=0)

result={'status':'PASS_EXACT_FIVE_CENTER_COUNTEREXAMPLE','alpha':16,
        'foci':[['0','0'],[str(B),'0'],[str(cx),str(cy)]],
        'levels':[str(lam),str(mu)],'checks':checks,
        'root_isolation':'Five disjoint intervals between the six listed cutpoints; exact IVT sign certificate',
        'scalar_sign_certificates':root_checks,
        'boundary_definitions':{'A1':r1,'A3':r3,'A5':r5},
        'boundary_boxes':[[x.data(),y.data()] for x,y in points],
        'even_determinant':even_area.data(),'odd_determinant':odd_area.data(),
        'A3_not_center_residual':third_residual.data(),
        'outgoing_center_boxes':[{'s_interval':d['s_interval'],'box':[v.data() for v in d['box']]} for d in centers],
        'incoming_certificate':{'common_focus':'A3','other_foci':['A5','A1'],
                                'levels':[L.data(),M.data()],
                                's_interval':[str(inlo),str(inhi)],
                                'G_at_left':ginlo.data(),'G_at_right':ginhi.data(),
                                'coordinate_box':[v.data() for v in inbox],
                                'source_quad_reason':'The first two old quads follow from these levels; the third follows by the exact outer balance identity'},
        'arithmetic':'Exact Fraction intervals; eighth-root brackets certified by integer eighth powers',
        'dependencies':['Intermediate value theorem','Strict convexity of (t^2+h^2)^8 for uniqueness of boundary parameters'],
        'claim_limit':'At least five centers, not an upper bound or claim that exactly five is maximal'}
Path(__file__).with_name('turn2_exact_certificate.json').write_text(json.dumps(result,indent=2)+'\n')
print('STATUS',result['status'],'checks',checks)
print('SCALAR SIGNS',[(r['s'],r['sign'],r['G_interval']['decimal_bounds']) for r in root_checks])
print('BOUNDARY BOXES',[[[float(v.a),float(v.b)] for v in P] for P in points])
print('AREAS',even_area.data()['decimal_bounds'],odd_area.data()['decimal_bounds'])
print('A3 EXCLUSION',third_residual.data()['decimal_bounds'])
print('CENTERS',[[v.data()['decimal_bounds'] for v in d['box']] for d in centers])
print('INCOMING',ginlo.data()['decimal_bounds'],ginhi.data()['decimal_bounds'],[v.data()['decimal_bounds'] for v in inbox])
