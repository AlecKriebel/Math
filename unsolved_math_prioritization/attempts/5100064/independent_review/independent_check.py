"""Independent k905 inversion/contact audit; no author module imported."""
from fractions import Fraction as F
from collections import Counter
import json,math
import sympy as sp
C=Counter()
def ck(v,k):
    assert v,k
    C[k]+=1
def zero(v,k):ck(sp.cancel(v)==0,k)
def det(p,q):return p[0]*q[1]-p[1]*q[0]
def area(v):return sum(det(p,q) for p,q in zip(v,v[1:]+v[:1]))/2
def invert(p,f):
    x,y=p[0]-f[0],p[1]-f[1];d=x*x+y*y
    return (f[0]+x/d,f[1]+y/d)
x,y,c=sp.symbols('x y c');plus=invert((x,y),(c,0));minus=invert((-x,-y),(-c,0))
for a,b in zip(plus,minus):zero(a+b,'formal_inversion_equivariance')
u,v=sp.symbols('u v');r=u*u+v*v
rect=[(u,v),(-u,v),(-u,-v),(u,-v)]
transformed=[invert(p,(c,0)) for p in rect]
D=(r+c*c)**2-4*c*c*u*u
zero(D-((u-c)**2+v*v)*((u+c)**2+v*v),'denominator_positive_factorization')
# Derive area as width times sum of the two vertical half-heights.
width=sp.factor(transformed[0][0]-transformed[1][0]);heights=sp.factor(transformed[0][1]+transformed[1][1])
zero(width-2*u*(r-c*c)/D,'inverted_trapezoid_width')
zero(heights-2*v*(r+c*c)/D,'inverted_trapezoid_height_sum')
zero(area(transformed)-width*heights,'direct_rectangle_shoelace')
a,b=sp.symbols('a b',positive=True);ss=a*a+b*b;lam=a*a*b*b/ss
contacts=[(a**3/ss,b**3/ss),(-a**3/ss,b**3/ss),(-a**3/ss,-b**3/ss),(a**3/ss,-b**3/ss)]
P=[(a,0),(0,b),(-a,0),(0,-b)]
for p,q,t in zip(P,P[1:]+P[:1],contacts):
    l,m,h=q[1]-p[1],p[0]-q[0],det(p,q)
    zero((a*a-lam)*l*l+(b*b-lam)*m*m-h*h,'axis_family_dual_tangency')
    zero(l*t[0]+m*t[1]-h,'axis_family_contact_on_chord')
    zero(det((t[0]-p[0],t[1]-p[1]),(q[0]-p[0],q[1]-p[1])),'axis_family_named_chord_collinearity')
    zero(t[0]**2/(a*a-lam)+t[1]**2/(b*b-lam)-1,'axis_family_contact_on_caustic')
    zero(t[0]*(q[0]-p[0])/(a*a-lam)+t[1]*(q[1]-p[1])/(b*b-lam),'axis_family_tangent_direction')
expr=sp.cancel((width*heights).subs({u:a**3/ss,v:b**3/ss}))
num,den=sp.fraction(expr)
expr=sp.cancel(sp.rem(num,c*c-a*a+b*b,c)/sp.rem(den,c*c-a*a+b*b,c))
zero(expr-4*(2*b*b-a*a)*(2*a*a-b*b)/(a**3*b**3),'axis_family_closed_area')
# The exact claimed zero, without any floating-point approximation.
A=sp.sqrt(2);T=[(2*A/3,sp.Rational(1,3)),(-2*A/3,sp.Rational(1,3)),(-2*A/3,-sp.Rational(1,3)),(2*A/3,-sp.Rational(1,3))]
P=[(A,0),(0,1),(-A,0),(0,-1)]
for i in range(4):
    p=P[i];q=P[(i+1)%4];t=T[i];previous=P[i-1]
    zero(t[0]*t[0]+t[1]*t[1]-1,'four_contact_unit_circle')
    side=(q[0]-p[0],q[1]-p[1]);incoming=(p[0]-previous[0],p[1]-previous[1])
    zero(side[0]**2+side[1]**2-3,'four_equal_side_length')
    difference=(incoming[0]-side[0],incoming[1]-side[1]);normal=(p[0]/2,p[1])
    zero(det(difference,normal),'four_reflection_normal')
    ck(sp.simplify(difference[0]*normal[0]+difference[1]*normal[1])>0,'four_reflection_outward')
    parameter=sp.simplify(((t[0]-p[0])*side[0]+(t[1]-p[1])*side[1])/3)
    ck(0<parameter<1,'physical_segment_contact')
for sign in (1,-1):
    inv=[tuple(sp.simplify(z) for z in invert(p,(sign,0))) for p in T]
    ck(len(set(inv))==4,'four_distinct_inverse_vertices')
    for (x,y),(u,v) in zip(inv,T):
        ck(x==sp.Rational(sign,2),'four_inverse_line')
        ck(sp.simplify((u-sign)**2+v*v)>0,'four_inverse_denominator_positive')
        returned=invert((x,y),(sign,0))
        for z,w in zip(returned,(u,v)):ck(sp.simplify(z-w)==0,'four_inversion_involution')
    ck(sp.simplify(area(inv))==0,'four_exact_zero_signed_area')
# Independent rational centrally paired polygons, with arbitrary traversal step.
for half in range(2,18):
 for seed in range(1,5):
    params=[F(j+seed,half+seed) for j in range(half)]
    first=[(5*(1-t*t)/(1+t*t),8*t/(1+t*t)) for t in params]
    poly=first+[(-x,-y) for x,y in first];N=2*half
    for step in range(1,half):
        if math.gcd(N,step)>1:continue
        ordered=[poly[i*step%N] for i in range(N)]
        V=[invert(t,(F(3),F(0))) for t in ordered];W=[invert(t,(F(-3),F(0))) for t in ordered]
        ck(len(set(V))==N,'rational_inversion_injectivity')
        ck(area(V)==area(W),'rational_signed_area_equality')
        for i,z in enumerate(V):
            ck(W[(i+half)%N]==(-z[0],-z[1]),'rational_half_period_equivariance')
            ck(invert(z,(F(3),F(0)))==ordered[i],'rational_involution')
print(json.dumps({'status':'PASS','exact_assertions':sum(C.values()),'counts':dict(sorted(C.items())),'sympy_version':sp.__version__,'scope':'Separate exact algebra, implicit chord contacts, and inversion controls. The analytic proof and primary classical symmetry establish the universal result.'},indent=2,sort_keys=True))
