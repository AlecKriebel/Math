#!/usr/bin/env python3
"""Independent symbolic, endpoint-coordinate and closed-orbit controls for k405."""
from pathlib import Path
from fractions import Fraction as F
from itertools import combinations
from math import gcd
import hashlib,json
import sympy as s
counts={}
def ck(name,ok):
    if not ok:raise RuntimeError(name)
    counts[name]=counts.get(name,0)+1

def dot(x,y):return sum(a*b for a,b in zip(x,y))
def det(x,y):return x[0]*y[1]-x[1]*y[0]
def sub(x,y):return tuple(a-b for a,b in zip(x,y))
def neg(x):return tuple(-a for a in x)
# Absolute-coordinate line system, different from the submitted focus-translated one.
def anti(P,Q,h):
    r=(P[0]-h,P[1]);t=(Q[0]-h,Q[1]);D=det(r,t)
    if D==0:raise RuntimeError("Singular antipedal line system")
    p=dot(P,r);q=dot(Q,t)
    return ((p*t[1]-r[1]*q)/D,(r[0]*q-p*t[0])/D)

a,b,C,S,U,V,h=s.symbols('a b C S U V h',nonzero=True)
P=(a*(C*U+S*V),b*(S*U-C*V));Q=(a*(C*U-S*V),b*(S*U+C*V))
D2=C*C/a**2+S*S/b**2;lam=V*V/D2;K=a*a*b*b-lam*(a*a-b*b)
actual=tuple(x+y for x,y in zip(anti(P,Q,h),anti(neg(P),neg(Q),h)))
target=(2*h+2*h*K*C*C/(a*a*(b*b-lam)),2*h*K*S*C/(a*b*(b*b-lam)))
def residual(expr):
    num=s.fraction(s.factor(expr))[0]
    for var,rel in [(C,C*C+S*S-1),(U,U*U+V*V-1),(h,h*h-a*a+b*b)]:num=s.rem(num,rel,var)
    return s.factor(num)
for j in range(2):ck('universal_focal_pair_identity',residual(actual[j]-target[j])==0)
ck('universal_support_denominator',residual(U*U-h*h*C*C/a**2-(b*b-lam)*D2)==0)
ck('universal_K_reduction',residual(h*h*(C*C-U*U)-b*b+K*D2)==0)
mean_c2,L,N,r=s.symbols('mean_c2 L N r',nonzero=True)
Lexpr=2*a*b*r*N*(1/b**2-(a*a-b*b)*mean_c2/(a*a*b*b))
Hex=s.simplify(a*a/(a*a-b*b)*(1-b*Lexpr/(2*a*r*N)))
ck('universal_perimeter_mean',s.simplify(Hex-mean_c2)==0)

# Independently generate two rational endpoints, rather than rational chord
# midpoint/half-angle variables. Recover lambda from the chord's line equation.
parameters=sorted({F(k,d) for d in range(1,5) for k in range(-6,7)})
chords=0
for aa,bb,cc in [(5,3,4),(13,12,5),(17,8,15)]:
    a,b,c=map(F,(aa,bb,cc))
    points=[(a*(1-t*t)/(1+t*t),b*2*t/(1+t*t)) for t in parameters]
    for P,Q in combinations(points,2):
        if det(P,Q)==0:continue
        if det(P,Q)<0:P,Q=Q,P
        nx=Q[1]-P[1];ny=P[0]-Q[0];height=nx*P[0]+ny*P[1]
        W=a*a*nx*nx+b*b*ny*ny
        lam=(W-height*height)/(nx*nx+ny*ny)
        if not 0<lam<b*b:continue
        chords+=1
        C2=a*a*nx*nx/W;SC=a*b*nx*ny/W;D2=(nx*nx+ny*ny)/W
        K=a*a*b*b-lam*c*c
        ck('endpoint_support',height>0 and height*height==W-lam*(nx*nx+ny*ny))
        E=sub(Q,P)
        ck('endpoint_length_identity',dot(E,E)==4*a*a*b*b*lam*D2*D2)
        Pd=(-a*P[1]/b,b*P[0]/a);Qd=(-a*Q[1]/b,b*Q[0]/a)
        ck('endpoint_first_variation',2*dot(E,sub(Qd,Pd))==8*lam*D2*c*c*SC)
        for h in (c,-c):
            ck('focus_inside_support',height-h*nx>0 and height+h*nx>0)
            X=anti(P,Q,h);Y=anti(neg(P),neg(Q),h)
            ck('absolute_focal_pair',X[0]+Y[0]==-2*h+2*h*K*C2/(a*a*(b*b-lam)) and
               X[1]+Y[1]==2*h*K*SC/(a*b*(b*b-lam)))
            for Z,R,T in [(X,P,Q),(Y,neg(P),neg(Q))]:
                ck('antipedal_defining_lines',dot(sub(Z,R),(R[0]-h,R[1]))==0 and dot(sub(Z,T),(T[0]-h,T[1]))==0)
        ck('origin_pair',anti(P,Q,F(0))==neg(anti(neg(P),neg(Q),F(0))))

# Closed six-bounce orbit with independently verified reflection, tangency and
# direct antipedal centroid. This checks a nonzero centroid and the factor 1/2.
hexagons=0
for aa,bb in [(5,3),(5,4),(13,5)]:
    a=s.Rational(aa);b=s.Rational(bb);c=s.sqrt(a*a-b*b)
    x=a*a/(a+b);y=b*s.sqrt(b*(2*a+b))/(a+b)
    P=[(a,s.Integer(0)),(x,y),(-x,y),(-a,s.Integer(0)),(-x,-y),(x,-y)]
    lam=a*a*b*b/(a+b)**2
    lengths=[b,2*x,b,b,2*x,b]
    total=4*b+4*x
    for i in range(6):
        A=P[i];B=P[(i+1)%6];Prev=P[(i-1)%6]
        ck('six_orbit_outer_ellipse',s.simplify(A[0]**2/a**2+A[1]**2/b**2-1)==0)
        ck('six_orbit_edge_length',s.simplify(dot(sub(B,A),sub(B,A))-lengths[i]**2)==0)
        normal=(B[1]-A[1],A[0]-B[0]);v=dot(normal,A)
        ck('six_orbit_caustic',s.simplify(v*v-(a*a-lam)*normal[0]**2-(b*b-lam)*normal[1]**2)==0)
        incoming=tuple(z/lengths[(i-1)%6] for z in sub(A,Prev));outgoing=tuple(z/lengths[i] for z in sub(B,A))
        ck('six_orbit_reflection',s.simplify(det(sub(incoming,outgoing),(A[0]/a**2,A[1]/b**2)))==0)
    H=s.simplify(a*a/(a*a-b*b)*(1-b*total/(2*a*(a*b/(a+b))*6)))
    ck('six_orbit_mean',H==(2*a+b)/(3*(a+b)))
    for focus in (c,-c,s.Integer(0)):
        vertices=[anti(P[i],P[(i+1)%6],focus) for i in range(6)]
        centroid=[s.simplify(sum(z[j] for z in vertices)/6) for j in range(2)]
        ck('six_orbit_direct_centroid',centroid==[-focus/3,s.Integer(0)])
        for j in range(3):ck('six_orbit_distinctness',P[j]!=P[j+3])
    hexagons+=1

rotations=0
for n in range(4,82,2):
    for p in range(1,n):
        if gcd(p,n)!=1:continue
        rotations+=1
        ck('primitive_even_halfturn',p%2==1 and (p*(n//2))%n==n//2)
for odd in range(3,42,2):
    n=2*odd
    ck('repeated_odd_not_halfturn',(2*(n//2))%n==0 and n//2!=0)

root=Path(__file__).parent
out={'problem_id':5100023,'status':'PASS_INDEPENDENT_SYMBOLIC_AND_EXACT_CONTROLS','assertions':sum(counts.values()),'groups':counts,
     'independent_endpoint_chords':chords,'exact_six_bounce_orbits':hexagons,'primitive_even_rotation_cases':rotations,
     'artifact_sha256':hashlib.sha256((root/'author_replay/PROOF.md').read_bytes()).hexdigest(),
     'verifier_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
     'limitations':'The all-period finite-action and first-variation arguments are proved analytically in the reviewed artifact; finite controls are not a billiard-dynamics or novelty certificate. Primitive even period and nondegenerate elliptical caustic only.'}
print(json.dumps(out,indent=2,sort_keys=True))
