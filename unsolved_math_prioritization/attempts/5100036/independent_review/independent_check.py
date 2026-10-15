"""Independent k608 review controls, without importing author code.
Use Q(a)[c]/(c²-a²+1), scale y by h=sqrt(2a+1), and intersect
homogeneous lines. Rational controls construct actual outer tangent polygons.
"""
import sympy as s
from fractions import Fraction as F
from math import gcd
from collections import Counter
import json
cnt=Counter()
def check(x,kind):
    assert x,kind
    cnt[kind]+=1
a=s.symbols('a');dc=a*a-1;metric=1/(2*a+1);can=s.cancel
class Q:
    def __init__(self,p=0,q=0):self.p=can(p);self.q=can(q)
    def __add__(self,x):
        x=qf(x);return Q(self.p+x.p,self.q+x.q)
    __radd__=__add__
    def __neg__(self):return Q(-self.p,-self.q)
    def __sub__(self,x):return self+-qf(x)
    def __rsub__(self,x):return qf(x)+-self
    def __mul__(self,x):
        x=qf(x);return Q(self.p*x.p+self.q*x.q*dc,self.p*x.q+self.q*x.p)
    __rmul__=__mul__
    def __truediv__(self,x):
        x=qf(x);nm=can(x.p*x.p-x.q*x.q*dc);assert nm!=0
        return self*Q(x.p/nm,-x.q/nm)
    def zero(self):return self.p==0 and self.q==0
def qf(x):return x if isinstance(x,Q) else Q(x)
def cross(x,y):return tuple(x[(j+1)%3]*y[(j+2)%3]-x[(j+2)%3]*y[(j+1)%3] for j in range(3))
def area(q):return sum(q[i][0]*q[(i+1)%len(q)][1]-q[i][1]*q[(i+1)%len(q)][0] for i in range(len(q)))/2
# Physical vertex (x,y) is represented by (x,h*y), making all input rational in a.
C=a/(a+1);Sscaled=(2*a+1)/(a+1)
P=[(a,0),(a*C,Sscaled),(-a*C,Sscaled),(-a,0),(-a*C,-Sscaled),(a*C,-Sscaled)]
tangent=[(Q(x/a**2),Q(metric*y),Q(-1)) for x,y in P]
outerH=[cross(tangent[i],tangent[(i+1)%6]) for i in range(6)]
outer=[(h[0]/h[2],h[1]/h[2]) for h in outerH]
expected=[(a,1),(0,a+1),(-a,1),(-a,-1),(0,-a-1),(a,-1)]
for t,e in zip(outer,expected):
    for x,y in zip(t,e):check((x-y).zero(),'actual_outer_tangent_vertices')
c=Q(0,1)
L=[(x-c,metric*y,-(x-c)*x-metric*y*y) for x,y in outer]
HH=[cross(L[i],L[(i+1)%6]) for i in range(6)]
V=[(h[0]/h[2],h[1]/h[2]) for h in HH]
for i,v in enumerate(V):
    for line in (L[i],L[(i+1)%6]):check((line[0]*v[0]+line[1]*v[1]+line[2]).zero(),'actual_antipedal_line_incidence')
d=metric;D=(a+1)*(1-d)/2;E=c*((1+d)/2);Z=a*(1+d);Ff=c*d
Y0=(a+1)-(2*a+1)*c*E/(a+1);Y1=(2*a+1)*c*D/(a+1)
expectedV=[(D-E,Y0+Y1),(-D-E,Y0-Y1),(-Z+Ff,Q(0)),(-D-E,-Y0+Y1),(D-E,-Y0-Y1),(Z+Ff,Q(0))]
for v,e in zip(V,expectedV):
    for x,y in zip(v,e):check((x-y).zero(),'all_six_antipedal_vertex_formulas')
Bscaled=area(V)
expectedB=-4*a*(a+1)*(a*a-2*a-2)/(2*a+1)
check(can(Bscaled.p-expectedB)==0,'independent_scaled_area_formula')
check(Bscaled.q==0,'area_radical_coefficient_zero')
g=a*a-2*a-2
for h in HH:
    nm=can(h[2].p**2-h[2].q**2*dc);num,den=s.fraction(nm)
    check(s.gcd(s.Poly(num,a),s.Poly(g,a)).degree()==0,'no_antipedal_denominator_at_root')
    check(s.gcd(s.Poly(den,a),s.Poly(g,a)).degree()==0,'no_hidden_pole_at_root')
for i in range(6):
    dx=V[i][0]-V[(i+1)%6][0];dy=V[i][1]-V[(i+1)%6][1]
    sq=dx*dx+metric*dy*dy;nm=can(sq.p**2-sq.q**2*dc);num,den=s.fraction(nm)
    check(s.gcd(s.Poly(num,a),s.Poly(g,a)).degree()==0,'nonzero_antipedal_edges_at_root')
# Genuine six-orbit: equation, all tangencies, and unsquared reflection ingredients.
lam=C*C
for i,(x,y) in enumerate(P):
    check(can(x*x/a**2+metric*y*y-1)==0,'six_original_vertices_on_ellipse')
    xx,yy=P[(i+1)%6];nx,ny=yy-y,x-xx;h=nx*x+ny*y
    check(can(h*h-(a*a-lam)*nx*nx-(1-lam)*(2*a+1)*ny*ny)==0,'all_six_strict_caustic_tangencies')
check(can(C*C+metric*Sscaled*Sscaled-1)==0,'diagonal_unit_length')
check(can(1-C-C/a)==0,'positive_specular_normal')
check(can(1-lam-(2*a+1)/(a+1)**2)==0,'strict_caustic_minor_axis')
check(s.simplify(g.subs(a,1+s.sqrt(3)))==0,'exact_positive_root')
check(s.simplify((dc-(2*a+1)).subs(a,1+s.sqrt(3)))==0,'focus_h_identity_at_root')
# Normal-backtracking exclusion, independently formed from its chord covector.
A,B,z=s.symbols('A B z',positive=True)
# z=sin²(theta); squared numerator and denominator of line-normal covector.
line_n2=z/B+(1-z)/A
support2=(A-B)**2*z*(1-z)/(A*B)
normal_lambda=can((A*z/B+B*(1-z)/A-support2)/line_n2)
check(can(normal_lambda-(A*z+B*(1-z)))==0,'normal_chord_parameter')
# Direct hand shoelace step (not used to obtain independent Bscaled).
D,E,Z,Ff,Y0,Y1=s.symbols('D E Z F Y0 Y1')
hand=[(D-E,Y0+Y1),(-D-E,Y0-Y1),(-Z+Ff,0),(-D-E,-Y0+Y1),(D-E,-Y0-Y1),(Z+Ff,0)]
check(s.expand(area(hand)-2*Y0*(D+Z)-2*Y1*(E+Ff))==0,'hand_shoelace_pairing')
# Rational exact controls using actual outer tangents, then antipedals.
def meet(l,m):
    p=cross(l,m);check(p[2]!=0,'rational_finite_intersection');return (p[0]/p[2],p[1]/p[2])
def anti(points,focus):
    L=[(x-focus,y,-(x-focus)*x-y*y) for x,y in points]
    return [meet(L[i],L[(i+1)%len(L)]) for i in range(len(L))]
cases=0
for m in range(2,16):
    for aa,bb,ff in [(F(5,4),F(3,4),F(1)),(F(13,12),F(5,12),F(1)),(F(5),F(4),F(3))]:
        half=[]
        for j in range(m):
            u=F(j,m-j);half.append((aa*(1-u*u)/(1+u*u),bb*2*u/(1+u*u)))
        boundary=half+[(-x,-y) for x,y in half]
        for tau in range(1,m):
            if gcd(tau,2*m)!=1:continue
            ordered=[boundary[i*tau%(2*m)] for i in range(2*m)]
            L=[(x/aa**2,y/bb**2,F(-1)) for x,y in ordered]
            T=[meet(L[i],L[(i+1)%(2*m)]) for i in range(2*m)]
            plus=anti(T,ff);minus=anti(T,-ff)
            for i in range(2*m):
                check(T[(i+m)%(2*m)]==tuple(-x for x in T[i]),'outer_central_pair')
                check(minus[(i+m)%(2*m)]==tuple(-x for x in plus[i]),'antipedal_central_pair')
                # Actual adjacent outer vertices lie on the shared original tangent.
                for j in [i,(i+1)%(2*m)]:
                    x,y=T[j];ell=L[(i+1)%(2*m)]
                    check(ell[0]*x+ell[1]*y+ell[2]==0,'shared_supporting_tangent')
            check(area(plus)==area(minus),'rational_signed_area_equality')
            cases+=1
print(json.dumps({'status':'PASS','exact_assertions':sum(cnt.values()),'families':dict(sorted(cnt.items())),'actual_outer_rational_controls':cases,'symbolic_scaled_area':str(s.factor(Bscaled.p)),'radical_coefficient':str(Bscaled.q),'scope':'Independent field arithmetic, direct outer and antipedal intersections, exact six-orbit and root controls. Rational central original polygons test derived geometry, not billiard dynamics.'},indent=2,sort_keys=True))
