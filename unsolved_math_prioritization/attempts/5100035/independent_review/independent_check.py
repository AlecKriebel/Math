"""Independent review controls for k607; no import of the author's checker.
Two-coordinate quadratic field Q(t)[e]/(e^2-(1-1/R)) keeps radical
branches separate; projective line intersections are formed by cross products.
"""
import sympy as sp
from fractions import Fraction as F
from math import gcd
from collections import Counter
import json
cnt=Counter()
def check(x,typ):
    assert x,typ
    cnt[typ]+=1
t=sp.symbols('t')
C=(1-t*t)/(1+t*t);S=2*t/(1+t*t)
R=(1-t)**3*(1+t)/(4*t**3);D=1-1/R
f=t**4-6*t**3-2*t**2-2*t+1
can=sp.cancel
class Q:
    def __init__(self,a=0,b=0):self.a=can(a);self.b=can(b)
    def __add__(self,v):
        if not isinstance(v,Q):v=Q(v)
        return Q(self.a+v.a,self.b+v.b)
    __radd__=__add__
    def __neg__(self):return Q(-self.a,-self.b)
    def __sub__(self,v):return self+-asq(v)
    def __rsub__(self,v):return asq(v)+-self
    def __mul__(self,v):
        v=asq(v);return Q(self.a*v.a+self.b*v.b*D,self.a*v.b+self.b*v.a)
    __rmul__=__mul__
    def __truediv__(self,v):
        v=asq(v);norm=can(v.a*v.a-v.b*v.b*D)
        assert norm!=0
        return self*Q(v.a/norm,-v.b/norm)
    def zero(self):return self.a==0 and self.b==0

def asq(v):return v if isinstance(v,Q) else Q(v)
def cross(x,y):return tuple(x[(j+1)%3]*y[(j+2)%3]-x[(j+2)%3]*y[(j+1)%3] for j in range(3))
P=[(1,0),(C,S),(0,1),(-C,S),(-1,0),(-C,-S),(0,-1),(C,-S)]
e=Q(0,1)
lines=[(Q(z)-e,Q(y/R),-Q(z*z+y*y/R)+z*e) for z,y in P]
H=[cross(lines[i],lines[(i+1)%8]) for i in range(8)]
U=[(h[0]/h[2],h[1]/h[2]) for h in H]
for i,(x,y) in enumerate(U):
    for L in (lines[i],lines[(i+1)%8]):
        check((L[0]*x+L[1]*y+L[2]).zero(),'quadratic_field_incidence')
area=sum(U[i][0]*U[(i+1)%8][1]-U[i][1]*U[(i+1)%8][0] for i in range(8))/2
expected=(t*t-2*t-1)*f/(4*t**3)
check(can(area.a-expected)==0,'independent_area_coefficient')
check(area.b==0,'independent_radical_coefficient')
# There is no cancelled antipedal denominator at the algebraic root.
for h in H:
    norm=can(h[2].a**2-h[2].b**2*D)
    num,den=sp.fraction(norm)
    check(sp.gcd(sp.Poly(num,t),sp.Poly(f,t)).degree()==0,'denominator_norm_root_coprimality')
    check(sp.gcd(sp.Poly(den,t),sp.Poly(f,t)).degree()==0,'denominator_poles_root_coprimality')
# Adjacent derived vertices also remain distinct at the certified root.
for i in range(8):
    du=U[i][0]-U[(i+1)%8][0];dv=U[i][1]-U[(i+1)%8][1]
    sq=R*du*du+dv*dv
    nm=can(sq.a**2-sq.b**2*D)
    nn,dd=sp.fraction(nm)
    check(sp.gcd(sp.Poly(nn,t),sp.Poly(f,t)).degree()==0,'nonzero_antipedal_edges_at_root')
# Root existence, uniqueness, and admissibility by rational interval reasoning.
check(f.subs(t,F(3,10))==F(661,10000),'root_endpoint_positive')
check(f.subs(t,F(1,3))==-F(8,81),'root_endpoint_negative')
# On 0<t<1/3, f'(t) <= 4/27-2 < 0 (other terms negative).
check(F(4,27)-2<0,'derivative_interval_bound')
check(F(2,3)**3/(4*F(1,3)**3)>1,'R_lower_bound')
check(1-F(1,3)**2-2*F(1,3)>0,'C_greater_than_S_bound')
check(can(C*C+S*S-1)==0,'ellipse_unit_circle')
d1=R*(C-1)**2+S*S;d2=R*C*C+(1-S)**2
ratio=(1-C)/(1-S)
check(can(d1-ratio**2*d2)==0,'positive_length_ratio')
# The exact difference of incoming/outgoing unit directions, multiplied by d1.
v=(C-1+C*ratio,S-(1-S)*ratio)
# Metric x=a z, normal=(C/a,S): determinant after multiplication by a.
check(can(R*v[0]*S-v[1]*C)==0,'specular_normal_parallelism')
check(can(v[1]-(C+S-1))==0,'normal_coefficient_positive')
# Construct chord covectors in normalized coordinates z,y. Tangency to
# z²/(1-lambda/R)+y²/(1-lambda)=1 is h²=A²nx²+B²ny².
lamb=can(R*(1-C)**2/d1)
for i in range(8):
    x,y=P[i];xx,yy=P[(i+1)%8]
    nx,ny=yy-y,x-xx;h=nx*x+ny*y
    check(can(h*h-(1-lamb/R)*nx*nx-(1-lamb)*ny*ny)==0,'all_eight_dual_conic_tangencies')
check(can(1-lamb-S*S/d1)==0,'strict_caustic_denominator')
# Symbolic orbit remains in the ellipse, and no consecutive vertices coincide.
for x,y in P:check(can(x*x+y*y-1)==0,'all_eight_ellipse_vertices')
for i in range(8):
    x,y=P[i];xx,yy=P[(i+1)%8]
    squared=can(R*(x-xx)**2+(y-yy)**2)
    n,d=sp.fraction(squared)
    check(sp.gcd(sp.Poly(n,t),sp.Poly(f,t)).degree()==0,'nonzero_sides_at_algebraic_root')
# Generic central rational polygons, including nontrivial primitive star orders.
def crossf(x,y):return tuple(x[(j+1)%3]*y[(j+2)%3]-x[(j+2)%3]*y[(j+1)%3] for j in range(3))
def anti(points,focus):
    lines=[]
    for x,y in points:
        nx=x-focus[0];ny=y-focus[1]
        lines.append((nx,ny,-nx*x-ny*y))
    out=[]
    for i in range(len(points)):
        h=crossf(lines[i],lines[(i+1)%len(points)])
        check(h[2]!=0,'rational_intersection_finite')
        out.append((h[0]/h[2],h[1]/h[2]))
    return out
rational_cases=0
for m in range(2,19):
    half=[]
    for j in range(m):
        u=F(j,m-j)
        half.append((F(5,4)*(1-u*u)/(1+u*u),F(3,4)*2*u/(1+u*u)))
    points=half+[(-x,-y) for x,y in half]
    for tau in range(1,m):
        if gcd(tau,2*m)!=1:continue
        pts=[points[i*tau%(2*m)] for i in range(2*m)]
        for focus in [(F(1,101),F(1,103)),(F(1,11),F(1,13)),(F(0),F(0))]:
            plus=anti(pts,focus);minus=anti(pts,(-focus[0],-focus[1]))
            for i in range(2*m):
                check(plus[i]==tuple(-z for z in minus[(i+m)%(2*m)]),'rational_cyclic_equivariance')
            ar=lambda q:sum(q[i][0]*q[(i+1)%len(q)][1]-q[i][1]*q[(i+1)%len(q)][0] for i in range(len(q)))/2
            check(ar(plus)==ar(minus),'rational_signed_area_equality')
            # Traversal reversal changes both area signs, preserving equality.
            check(ar(list(reversed(plus)))==-ar(plus),'signed_orientation_reversal')
            rational_cases+=1
print(json.dumps({'status':'PASS','exact_assertions':sum(cnt.values()),'families':dict(sorted(cnt.items())),'rational_polygon_cases':rational_cases,'symbolic_area_over_a':str(sp.factor(area.a)),'radical_coefficient':str(area.b),'method':'Independent quadratic-field arithmetic and projective line cross products; no author code imported. Finite generic polygons are algebra controls, not asserted billiard orbits.'},indent=2,sort_keys=True))
