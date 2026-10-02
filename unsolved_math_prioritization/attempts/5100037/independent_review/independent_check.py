"""Independent k609 audit: implicit-line projections and exact rational algebra.
No author module is imported. Existing SymPy is used for formal identities.
"""
import json
from fractions import Fraction as F
from collections import Counter
import sympy as sp
C=Counter()
def ok(v,label):
    assert v,label
    C[label]+=1
def zero(v,label):ok(sp.cancel(v)==0,label)
def determinant(p,q):return p[0]*q[1]-p[1]*q[0]
def implicit(p,q):return (p[1]-q[1],q[0]-p[0],determinant(p,q))
def pedal(vertices,point):
    result=[]
    for p,q in zip(vertices,vertices[1:]+vertices[:1]):
        l,m,h=implicit(p,q);den=l*l+m*m
        ok(den>0,'finite_rational_side')
        r=(l*point[0]+m*point[1]-h)/den
        foot=(point[0]-l*r,point[1]-m*r)
        ok(l*foot[0]+m*foot[1]==h,'implicit_projection_incidence')
        result.append(foot)
    return result
def area(v):return sum(determinant(p,q) for p,q in zip(v,v[1:]+v[:1]))/2
# Rational convex centrally symmetric polygons, with unequal axis scaling.
for half in range(2,11):
 for seed in range(1,8):
    ts=[F(j+seed,half+2*seed) for j in range(half)]
    top=[(3*(1-t*t)/(1+t*t),4*t/(1+t*t)) for t in ts]
    vertices=top+[(-x,-y) for x,y in top]
    normals=[implicit(p,q)[:2] for p,q in zip(vertices,vertices[1:]+vertices[:1])]
    coefficient=sum(F(determinant(p,q)*(p[0]*q[0]+p[1]*q[1]),4*(p[0]**2+p[1]**2)*(q[0]**2+q[1]**2)) for p,q in zip(normals,normals[1:]+normals[:1]))
    b0=area(pedal(vertices,(F(0),F(0))))
    ok(b0>0,'origin_area_positive')
    ok(coefficient==0 if half==2 else coefficient>0,'radial_coefficient_sign')
    for M in [(F(1),F(0)),(F(0),F(1)),(F(7,3),F(-8,5)),(F(100),F(300))]:
        feet=pedal(vertices,M);other=pedal(vertices,(-M[0],-M[1]))
        ok(area(feet)==b0+coefficient*(M[0]**2+M[1]**2),'radial_identity')
        ok(area(feet)>0,'arbitrary_point_positive')
        ok(area(feet)==area(other),'central_area_equality')
        for i in range(2*half):ok(other[(i+half)%(2*half)]==(-feet[i][0],-feet[i][1]),'opposite_foot_identity')
# Symbolic star geometry, in coordinates x=a*xi, y=eta, a^2=R.
t=sp.symbols('t');c=(1-t*t)/(1+t*t);s=2*t/(1+t*t)
R=(1-t)*(1+t)**3/(4*t)
lam=sp.factor(R*(1+c)**2/(s*s+R*(1+c)**2))
P=[(1,0),(-c,s),(0,-1),(c,s),(-1,0),(c,-s),(0,1),(-c,-s)]
contacts=[]
for p,q in zip(P,P[1:]+P[:1]):
    l,m,h=implicit(p,q)
    zero((R-lam)*l*l/R+(1-lam)*m*m-h*h,'all_eight_dual_tangencies')
    xi=sp.factor((R-lam)*l/(R*h));eta=sp.factor((1-lam)*m/h)
    zero(l*xi+m*eta-h,'all_eight_contact_incidence')
    zero(R*xi*xi/(R-lam)+eta*eta/(1-lam)-1,'all_eight_contacts_on_caustic')
    contacts.append((xi,eta))
# Squared positive chord ratio and its implied normal parallelism.
d1=R*(1+c)**2+s*s;d2=R*c*c+(1+s)**2
zero(d1*(1+s)**2-d2*(1+c)**2,'off_axis_reflection_lengths')
zero(R*(1+c)*s-c*(1+s),'off_axis_reflection_normal')
# Axial reflection follows exactly from equal side lengths and reflected vectors.
for i in (0,2,4,6):
    p=P[i];left=(p[0]-P[i-1][0],p[1]-P[i-1][1]);right=(P[(i+1)%8][0]-p[0],P[(i+1)%8][1]-p[1])
    zero(R*left[0]**2+left[1]**2-R*right[0]**2-right[1]**2,'axial_reflection_lengths')
    normal=(p[0]/R,p[1])
    zero((left[0]-right[0])*normal[1]-(left[1]-right[1])*normal[0],'axial_reflection_normal')
def normalized_pedal(z):
    out=[]
    for p,q in zip(contacts,contacts[1:]+contacts[:1]):
        l,m,h=map(sp.factor,implicit(p,q));den=sp.factor(l*l/R+m*m)
        r=sp.factor((l*z-h)/den)
        out.append((sp.factor(z-l*r/R),sp.factor(-m*r)))
    return out
B0=sp.factor(area(normalized_pedal(0)));Bp=sp.factor(area(normalized_pedal(1)));Bm=sp.factor(area(normalized_pedal(-1)))
zero(Bp-Bm,'symbolic_linear_area_coefficient_zero')
actual=sp.factor(B0+(Bp-B0)*(R-1)/R)
f=t**7-4*t**6+3*t**5+6*t**4-t**3+5*t-2
G=t**6-2*t**5-3*t**4-8*t**3+3*t*t+2*t-1
expected=-8*t**3*(1-t)**2*(1+t)**2*f/((1+t*t)**2*(t*t-2*t-1)**2*G)
zero(actual-expected,'formal_star_area_identity')
x,y=contacts[0];u,v=contacts[1]
distance=sp.factor(R*(x-u)**2+(y-v)**2)
zero(distance+(1+t)**2*G/(t*(1+t*t)*(t*t-2*t-1)**2),'physical_denominator_identity')
zero(f.subs(t,sp.Rational(3,8))+sp.Rational(98389,2097152),'left_endpoint_exact')
zero(f.subs(t,sp.Rational(2,5))-sp.Rational(8248,78125),'right_endpoint_exact')
for j in range(1,101):
    t0=sp.Rational(3,8)+sp.Rational(j,101)*(sp.Rational(2,5)-sp.Rational(3,8))
    rr=R.subs(t,t0);ll=lam.subs(t,t0)
    ok(rr>1 and 0<ll<1,'strict_elliptical_caustic_controls')
    ok(G.subs(t,t0)<0,'denominator_sign_controls')
    con=[(sp.factor(x.subs(t,t0)),sp.factor(y.subs(t,t0))) for x,y in contacts]
    ok(len(set(con))==8,'eight_distinct_contacts_controls')
    for p,q in zip(con,con[1:]+con[:1]):ok(rr*(p[0]-q[0])**2+(p[1]-q[1])**2>0,'all_finite_inner_sides_controls')
print(json.dumps({'status':'PASS','assertions':sum(C.values()),'counts':dict(sorted(C.items())),'sympy_version':sp.__version__,'method':'Independent implicit-line projection, scaled metric, and formal rational-function identities; finite controls supplement the analytic proof audit.'},indent=2,sort_keys=True))
