"""Exact symbolic and rational checks for k607. No floating-point roots.

SymPy is a pre-existing dependency. This is an authored verification script,
not downloaded source code. The mathematical proof is in PROOF.md.
"""
import sympy as s
from fractions import Fraction as F
from collections import Counter
import json

counts=Counter()
def ck(value, family):
    assert value, family
    counts[family]+=1
def zero(expr, family):
    ck(s.cancel(expr)==0, family)

a,C,S,c=s.symbols('a C S c')
P=[(a,0),(a*C,S),(0,1),(-a*C,S),(-a,0),(-a*C,-S),(0,-1),(a*C,-S)]
def intersections(points,f):
    result=[]
    for i,(x,y) in enumerate(points):
        X,Y=points[(i+1)%len(points)]
        n,N=x-f,X-f; h,H=n*x+y*y,N*X+Y*Y
        delta=n*Y-y*N
        result.append(((h*Y-y*H)/delta,(n*H-h*N)/delta))
    return result
def area(Q):
    return sum(Q[i][0]*Q[(i+1)%len(Q)][1]-Q[i][1]*Q[(i+1)%len(Q)][0] for i in range(len(Q)))/2
Q=intersections(P,c); Qminus=intersections(P,-c)
for i,(qx,qy) in enumerate(Q):
    for x,y in (P[i],P[(i+1)%8]):
        zero((x-c)*(qx-x)+y*(qy-y),'symbolic_line_incidence')
    for d in (0,1):
        zero(Qminus[(i+4)%8][d]+Q[i][d],'symbolic_central_equivariance')

t=s.symbols('t',positive=True)
Ct=(1-t*t)/(1+t*t); St=2*t/(1+t*t)
R=(1-t)**3*(1+t)/(4*t**3)
f=t**4-6*t**3-2*t**2-2*t+1
zero(Ct**2+St**2-1,'unit_circle')
zero(R-Ct*(1-St)/(St*(1-Ct)),'closure_parameter')
d1=R*(1-Ct)**2+St**2
d2=R*Ct**2+(1-St)**2
zero(d1*(1-St)**2-d2*(1-Ct)**2,'positive_chord_ratio_squared')
lam=R*(1-Ct)**2/d1
zero(lam-R*(1-St)**2/d2,'common_caustic')
zero(R*(1-Ct)/(1-St)-Ct/St,'reflection_normal_ratio')

# Exact polynomial reduction in c^2=a^2-1, followed by a^2=R(t).
expr=s.factor(area(Q)/a)
num,den=s.fraction(expr)
def reduce_c(poly):
    return s.Poly(poly,c).rem(s.Poly(c*c-a*a+1,c)).as_expr()
num=reduce_c(num); den=reduce_c(den)
expr=s.factor((num/den).subs({C:Ct,S:St}))
num,den=s.fraction(expr)
def reduce_a(poly):
    return s.Poly(poly,a).rem(s.Poly(a*a-R,a)).as_expr()
num=reduce_a(num); den=reduce_a(den)
target=(t*t-2*t-1)*f/(4*t**3)
zero(num-target*den,'zero_area_polynomial_identity')
ck(s.factor(den)!=0,'symbolic_denominator_not_identically_zero')
zero(f.subs(t,s.Rational(3,10))-s.Rational(661,10000),'root_left_sign_exact')
zero(f.subs(t,s.Rational(1,3))+s.Rational(8,81),'root_right_sign_exact')
ck(s.Rational(1,3)**2+2*s.Rational(1,3)-1<0,'root_interval_below_sqrt2_minus1')

# Rational central polygons independently test the equivariance and shoelace
# argument. These generic polygons are not claimed to be billiard orbits.
def qa(P,f):
    out=[]
    for i,(x,y) in enumerate(P):
        X,Y=P[(i+1)%len(P)]; n,N=x-f,X-f
        delta=n*Y-y*N
        ck(delta!=0,'rational_unique_intersections')
        h,H=n*x+y*y,N*X+Y*Y
        out.append(((h*Y-y*H)/delta,(n*H-h*N)/delta))
    return out
for half in range(2,9):
    for seed in range(1,16):
        params=[F(j+seed,half+seed) for j in range(1,half+1)]
        upper=[(F(2)*(1-v*v)/(1+v*v),2*v/(1+v*v)) for v in params]
        pts=upper+[(-x,-y) for x,y in upper]
        focus=F(seed,1000)
        plus=qa(pts,focus); minus=qa(pts,-focus)
        for i in range(2*half):
            ck(minus[(i+half)%(2*half)]==tuple(-x for x in plus[i]),'rational_equivariance')
        ck(area(plus)==area(minus),'rational_signed_area_equality')

print(json.dumps({'status':'PASS','exact_assertions':sum(counts.values()),'families':dict(sorted(counts.items())),'sympy_version':s.__version__,'scope':'Exact finite algebraic controls and symbolic zero certificate; the universal source-symmetry argument is in PROOF.md.'},indent=2,sort_keys=True))
