"""Exact k610 identities and the two distinct admissible domain exceptions.

Uses only fractions and pre-existing SymPy. No floating-point root is used.
"""
import sympy as s
from fractions import Fraction as F
from collections import Counter
import json
count=Counter()
def ck(x,label):
    assert x,label
    count[label]+=1
def zero(x,label):ck(s.cancel(s.simplify(x))==0,label)
def det(u,v):return u[0]*v[1]-u[1]*v[0]
def dot(u,v):return u[0]*v[0]+u[1]*v[1]
def sub(u,v):return (u[0]-v[0],u[1]-v[1])
def anti(P,Foc):
    Q=[];D=[]
    for i,p in enumerate(P):
        q=P[(i+1)%len(P)];n=sub(p,Foc);m=sub(q,Foc)
        d=det(n,m);h=dot(n,p);k=dot(m,q);D.append(d)
        Q.append(((h*m[1]-n[1]*k)/d,(n[0]*k-h*m[0])/d))
    return Q,D
def area(Q):return sum(det(p,Q[(i+1)%len(Q)]) for i,p in enumerate(Q))/2

x,y,c=s.symbols('x y c',nonzero=True)
P=[(x,y),(-x,y),(-x,-y),(x,-y)]
Q,D=anti(P,(c,0));Qminus,Dminus=anti(P,(-c,0))
H=(x*x+y*y-c*c)/y;L=-x-y*y/(x+c);T=x+y*y/(x-c)
expected=[(-c,H),(L,0),(-c,-H),(T,0)]
for i,q in enumerate(Q):
    for d in (0,1):
        zero(q[d]-expected[i][d],'rectangle_vertex_formula')
        zero(Qminus[(i+2)%4][d]+q[d],'rectangle_equivariance')
    for p in (P[i],P[(i+1)%4]):
        zero(dot(sub(p,(c,0)),sub(q,p)),'rectangle_line_incidence')
    zero(Dminus[(i+2)%4]-D[i],'rectangle_finite_locus_equality')
zero(area(Q)-2*x*(x*x+y*y-c*c)**2/(y*(x*x-c*c)),'rectangle_signed_area')
zero(s.prod(D)-16*x*x*y**4*(x*x-c*c),'rectangle_determinant_product')

R=s.symbols('R',positive=True)
lam=R/(R+1);alpha2=R-lam;beta2=1-lam
zero(alpha2-R*R/(R+1),'caustic_major_axis')
zero(beta2-1/(R+1),'caustic_minor_axis')
zero(alpha2-beta2-(R-1),'confocal_foci')
zero(alpha2/R+beta2-1,'diamond_side_tangency')
x2=R**3/(R+1)**2;y2=1/(R+1)**2
zero(x2-(R-1)-(-R*R+R+1)/(R+1)**2,'singularity_factor')
zero(x2+y2-(R-1)-(2-R)/(R+1),'collapse_factor')

# All four intersections exist at the exact collapse and all equal -F+.
P2=[(2*s.sqrt(2)/3,s.Rational(1,3)),(-2*s.sqrt(2)/3,s.Rational(1,3)),(-2*s.sqrt(2)/3,-s.Rational(1,3)),(2*s.sqrt(2)/3,-s.Rational(1,3))]
Q2,D2=anti(P2,(s.Integer(1),s.Integer(0)))
for q,d in zip(Q2,D2):
    ck(s.simplify(d)!=0,'collapse_finite_intersections')
    zero(q[0]+1,'collapse_x');zero(q[1],'collapse_y')
zero(area(Q2),'collapse_zero_area')

phi=(1+s.sqrt(5))/2
zero((-R*R+R+1).subs(R,phi),'golden_ratio_singularity')
ck(phi>1,'golden_ratio_outer_nondegenerate')
ck(lam.subs(R,phi)>0 and lam.subs(R,phi)<1,'golden_ratio_strict_caustic')
ck(s.simplify((x2+y2-(R-1)).subs(R,phi))!=0,'golden_ratio_not_collapse')
# At c=x, the right pair becomes y-coordinate=+/-y, genuinely parallel.
zero(D[3].subs(c,x),'parallel_pair_determinant')
ck(y!=0,'parallel_offsets_distinct')

# Source-independent Euclidean equivariance on rational centrally symmetric
# polygons. Domain checks are explicit; no claim these are billiard samples.
for half in range(2,9):
    for seed in range(1,16):
        params=[F(j+seed,half+seed) for j in range(1,half+1)]
        upper=[(2*(1-v*v)/(1+v*v),2*v/(1+v*v)) for v in params]
        poly=upper+[(-xx,-yy) for xx,yy in upper]
        focus=(F(seed,1000),F(0))
        plus,dp=anti(poly,focus);minus,dm=anti(poly,(-focus[0],F(0)))
        for i,q in enumerate(plus):
            ck(dp[i]!=0,'rational_finite_domain')
            ck(dm[(i+half)%len(poly)]==dp[i],'rational_domain_equivariance')
            ck(minus[(i+half)%len(poly)]==(-q[0],-q[1]),'rational_vertex_equivariance')
        ck(area(plus)==area(minus),'rational_signed_area_equality')

print(json.dumps({'status':'PASS','exact_assertions':sum(count.values()),'families':dict(sorted(count.items())),'sympy_version':s.__version__,'scope':'Exact finite identities and exceptional-domain certificates; universal geometric proof and source input are in PROOF.md.'},indent=2,sort_keys=True))
