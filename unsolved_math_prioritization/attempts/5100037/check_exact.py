"""Exact k609 controls, including the admissible star denominator certificate.

Authored code; uses Python fractions and pre-existing SymPy. No floating roots.
"""
import sympy as s
from fractions import Fraction as F
from collections import Counter
import json
counts=Counter()
def ck(x,label):
    assert x,label
    counts[label]+=1
def zero(x,label): ck(s.cancel(x)==0,label)
def det(x,y):return x[0]*y[1]-x[1]*y[0]
def dot(x,y):return x[0]*y[0]+x[1]*y[1]
def sub(x,y):return (x[0]-y[0],x[1]-y[1])
def feet(P,M):
    out=[]
    for i,x in enumerate(P):
        d=sub(P[(i+1)%len(P)],x);u=dot(sub(M,x),d)/dot(d,d)
        out.append((x[0]+u*d[0],x[1]+u*d[1]))
    return out
def area(P):return sum(det(x,P[(i+1)%len(P)]) for i,x in enumerate(P))/2

X,Y,U,V,c,a,t=s.symbols('X Y U V c a t')
P=[(X,Y),(-U,-V),(U,-V),(-X,Y),(-X,-Y),(U,V),(-U,V),(X,-Y)]
Q=feet(P,(c,0));Qminus=feet(P,(-c,0))
for i,q in enumerate(Q):
    d=sub(P[(i+1)%8],P[i]);n=(-d[1],d[0])
    zero(dot(sub(q,P[i]),n),'symbolic_foot_on_line')
    zero(dot(sub(q,(c,0)),d),'symbolic_foot_orthogonal')
    for k in (0,1):zero(Qminus[(i+4)%8][k]+q[k],'symbolic_equivariance')
C=(1-t*t)/(1+t*t);S=2*t/(1+t*t)
R=(1-t)*(1+t)**3/(4*t)
lam=R*(1+C)**2/(S*S+R*(1+C)**2)
zero(C*C+S*S-1,'circle_parameter')
zero(R-C*(1+S)/(S*(1+C)),'closure_parameter')
d1=R*(1+C)**2+S*S;d2=R*C*C+(1+S)**2
zero(d1*(1+S)**2-d2*(1+C)**2,'squared_positive_chord_ratio')
zero(lam-R*(1+S)**2/d2,'equal_caustic')
zero(R*(1+C)/(1+S)-C/S,'reflection_normal')
xx=(R-lam)/a;yy=(1-lam)*(1+C)/S
uu=(R-lam)*(1+S)/(a*C);vv=1-lam
def reduce_a(x):
    num,den=s.fraction(s.factor(x))
    num=s.Poly(num,a).rem(s.Poly(a*a-R,a)).as_expr()
    den=s.Poly(den,a).rem(s.Poly(a*a-R,a)).as_expr()
    return s.factor(num/den)
zero(reduce_a(xx*xx/(R-lam)+yy*yy/(1-lam)-1),'contact_on_caustic')
zero(reduce_a(S*xx+a*(1+C)*yy-a*S),'contact_on_first_line')
zero(reduce_a((1+S)*(-uu)+a*C*(-vv)+a*C),'contact_on_second_line')
f=t**7-4*t**6+3*t**5+6*t**4-t**3+5*t-2
G=t**6-2*t**5-3*t**4-8*t**3+3*t*t+2*t-1
ar=s.factor(area(Q))
expected=-8*t**3*(1-t)**2*(1+t)**2*f/((1+t*t)**2*(t*t-2*t-1)**2*G)
evaluated=reduce_a(ar.subs({X:xx,Y:yy,U:uu,V:vv,c*c:R-1})/a)
zero(evaluated-expected,'star_area_polynomial')
zero(reduce_a((xx+uu)**2+(yy+vv)**2)+(1+t)**2*G/(t*(1+t*t)*(t*t-2*t-1)**2),'physical_denominator_identity')
zero(f.subs(t,s.Rational(3,8))+s.Rational(98389,2097152),'left_root_sign')
zero(f.subs(t,s.Rational(2,5))-s.Rational(8248,78125),'right_root_sign')
ck(s.Rational(2,5)**2+2*s.Rational(2,5)-1<0,'interval_below_sqrt2_minus1')
# The normal chord's dual tangency numerator equals D^2, so lambda=D>=b^2.
A,B,u=s.symbols('A B u')
D=A*u+B*(1-u)
zero(A*A*u+B*B*(1-u)-(A-B)**2*u*(1-u)-D*D,'normal_chord_parameter')

for half in range(2,10):
    for seed in range(1,16):
        params=[F(j+seed,half+seed) for j in range(1,half+1)]
        upper=[(2*(1-v*v)/(1+v*v),2*v/(1+v*v)) for v in params]
        poly=upper+[(-x,-y) for x,y in upper]
        normals=[]
        for i,p in enumerate(poly):
            d=sub(poly[(i+1)%len(poly)],p)
            normals.append((d[1],-d[0]))
        coeff=sum(F(det(n,normals[(i+1)%len(poly)])*dot(n,normals[(i+1)%len(poly)]),4*dot(n,n)*dot(normals[(i+1)%len(poly)],normals[(i+1)%len(poly)])) for i,n in enumerate(normals))
        b0=area(feet(poly,(F(0),F(0))))
        ck(b0>0,'convex_origin_positive')
        ck(coeff==0 if half==2 else coeff>0,'convex_quadratic_sign')
        for M in [(F(0),F(0)),(F(1),F(2)),(F(-7,3),F(11,2)),(F(100),F(-31))]:
            plus=feet(poly,M);minus=feet(poly,(-M[0],-M[1]));bp=area(plus)
            ck(bp==b0+coeff*dot(M,M),'rational_radial_identity')
            ck(bp>0,'convex_arbitrary_point_positive')
            ck(bp==area(minus),'rational_focal_area_equality')
            for i,q in enumerate(plus):
                ck(minus[(i+half)%len(poly)]==(-q[0],-q[1]),'rational_foot_equivariance')

print(json.dumps({'status':'PASS','exact_assertions':sum(counts.values()),'families':dict(sorted(counts.items())),'sympy_version':s.__version__,'scope':'Exact finite and symbolic controls, not a substitute for the universal proof or published symmetry input.'},indent=2,sort_keys=True))
