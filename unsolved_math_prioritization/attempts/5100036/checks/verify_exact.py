"""Exact algebra and geometry controls for k608; no downloaded code is executed."""
from fractions import Fraction as F
from collections import Counter
import json,math
import sympy as s
counts=Counter()
def ck(value,label):
    assert value,label
    counts[label]+=1
def zero(value,label):ck(s.cancel(value)==0,label)
def det(x,y):return x[0]*y[1]-x[1]*y[0]
def area(P):return sum(det(p,q) for p,q in zip(P,P[1:]+P[:1]))/2
def solve(L,M):
    a,b,h=L;d,e,k=M;D=a*e-b*d
    return ((h*e-b*k)/D,(a*k-h*d)/D)
def anti(T,M):
    lines=[(x-M[0],y-M[1],(x-M[0])*x+(y-M[1])*y) for x,y in T]
    return [solve(x,y) for x,y in zip(lines,lines[1:]+lines[:1])]
t,c=s.symbols('t c');C=(1-t*t)/(1+t*t);S=2*t/(1+t*t);a=(1-t*t)/(2*t*t);h=1/t
P=[(a,0),(a*C,S),(-a*C,S),(-a,0),(-a*C,-S),(a*C,-S)]
lam=C*C
zero(C*C+S*S-1,'circle_parameter')
zero(a-C/(1-C),'six_orbit_parameter')
for p,q in zip(P,P[1:]+P[:1]):
    zero(p[0]**2/a**2+p[1]**2-1,'orbit_on_ellipse')
    L=(p[1]-q[1],q[0]-p[0],det(p,q));x,y,z=L
    zero((a*a-lam)*x*x+(1-lam)*y*y-z*z,'all_six_dual_caustic_tangencies')
zero((a*C-a)**2+S*S-1,'diagonal_unit_length')
zero(1-C-C/a,'off_axis_reflection_normal')
# The outgoing diagonal at an axial vertex mirrors the incoming one.
zero((1-C)**2*a*a+S*S-1,'axis_reflection_equal_length')
tangents=[(x/a**2,y,s.Integer(1)) for x,y in P]
T=[tuple(s.factor(z) for z in solve(x,y)) for x,y in zip(tangents,tangents[1:]+tangents[:1])]
expectedT=[(a,1/h),(0,(a+1)/h),(-a,1/h),(-a,-1/h),(0,-(a+1)/h),(a,-1/h)]
for x,y in zip(T,expectedT):
    for u,v in zip(x,y):zero(u-v,'outer_tangent_intersection_formula')
Q=[tuple(s.factor(z) for z in q) for q in anti(T,(c,0))]
Qminus=[tuple(s.factor(z) for z in q) for q in anti(T,(-c,0))]
for i,q in enumerate(Q):
    for k in (0,1):zero(q[k]+Qminus[(i+3)%6][k],'symbolic_antipedal_central_equivariance')
    for j in (i,(i+1)%6):
        u,v=T[j];zero((u-c)*(q[0]-u)+v*(q[1]-v),'antipedal_line_incidence')
def red(x):
    num,den=s.fraction(s.factor(x));relation=c*c-a*a+1
    return s.factor(s.rem(num,relation,c)/s.rem(den,relation,c))
d=1/h**2;D=(a+1)*(1-d)/2;E=c*(1+d)/2;Z=a*(1+d);FF=c*d;w=(a+1)/h
Y0=w-c*E/w;Y1=c*D/w
expectedQ=[(D-E,Y0+Y1),(-D-E,Y0-Y1),(-Z+FF,0),(-D-E,-Y0+Y1),(D-E,-Y0-Y1),(Z+FF,0)]
for q,r in zip(Q,expectedQ):
    for u,v in zip(q,r):zero(red(u-v),'six_vertex_antipedal_formula')
expectedB=-4*a*(a+1)*(a*a-2*a-2)/h**3
zero(red(area(Q)-expectedB),'full_symbolic_antipedal_area')
zero(red(area(expectedQ)-(2*Y0*(D+Z)+2*Y1*(E+FF))),'paired_shoelace_formula')
zero(red(2*Y0*(D+Z)+2*Y1*(E+FF)-expectedB),'hand_area_simplification')
aa=1+s.sqrt(3);zero(aa*aa-2*aa-2,'exact_critical_root')
zero(aa*aa-1-(2*aa+1),'critical_focus_equals_h')
# General normal-chord lambda identity, A=a^2, B=b^2, u=sin^2(theta).
A,B,u=s.symbols('A B u');N=A*u+B*(1-u)
zero(A*A*u+B*B*(1-u)-(A-B)**2*u*(1-u)-N*N,'normal_chord_lambda_identity')
# Rational central polygons, including star traversal, test the equivariance
# of actual antipedal line intersections. No billiard property is inferred here.
for half in range(2,11):
 for seed in range(1,7):
    params=[F(j+seed,half+2*seed) for j in range(half)]
    upper=[(3*(1-v*v)/(1+v*v),4*v/(1+v*v)) for v in params]
    boundary=upper+[(-x,-y) for x,y in upper];n=2*half
    for step in range(1,n//2):
        if math.gcd(step,n)!=1:continue
        T0=[boundary[(i*step)%n] for i in range(n)]
        for focus in [(F(0),F(0)),(F(1,7),F(-1,11))]:
            good=all(det((p[0]-focus[0],p[1]-focus[1]),(q[0]-focus[0],q[1]-focus[1]))!=0 for p,q in zip(T0,T0[1:]+T0[:1]))
            if not good:continue
            qq=anti(T0,focus);rr=anti(T0,(-focus[0],-focus[1]))
            ck(area(qq)==area(rr),'rational_signed_area_equality')
            for i,q in enumerate(qq):
                ck(rr[(i+half)%n]==(-q[0],-q[1]),'rational_antipedal_equivariance')
                for j in (i,(i+1)%n):
                    x,y=T0[j];ck((x-focus[0])*(q[0]-x)+(y-focus[1])*(q[1]-y)==0,'rational_antipedal_incidence')
# Finite rational parameter controls verify the exact family on both sides of zero.
for j in range(1,101):
    t0=F(j,175);cv=F(1-t0*t0,1+t0*t0);av=F(1-t0*t0,2*t0*t0)
    ck(av>1 and 0<cv*cv<1,'strict_caustic_parameter_controls')
print(json.dumps({'status':'PASS','exact_assertions':sum(counts.values()),'counts':dict(sorted(counts.items())),'sympy_version':s.__version__,'scope':'Formal symbolic identities and finite rational controls; universal statements require the geometric proof and credited classical symmetry.'},indent=2,sort_keys=True))
