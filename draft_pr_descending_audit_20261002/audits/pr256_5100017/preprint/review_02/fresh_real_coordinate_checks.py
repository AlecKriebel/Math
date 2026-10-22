"""Fresh exact checks, authored before reading the archived Cartesian proof.

All writes stay next to this script. This is corroboration of the independent
written all-N audit, not a finite numerical substitute for that argument.
"""
from pathlib import Path
from datetime import datetime, timezone
import json
import sympy as s

HERE = Path(__file__).resolve().parent
checks = []

def eq(name, value):
    value = s.simplify(s.factor(s.together(value)))
    assert value == 0, (name, value)
    checks.append(name)
    print('PASS',name,flush=True)

def cross(u, v):
    return u[0]*v[1]-u[1]*v[0]

def moments(points):
    area, moment = s.S.Zero, s.zeros(2, 1)
    for u, v in zip(points, points[1:]+points[:1]):
        a = cross(u, v)
        area += a/2
        moment += a*(u+v)
    return s.simplify(area), moment.applyfunc(s.simplify)

# A completely real edge expansion: linear paired-edge moment has a local
# matrix plus an endpoint difference. Verify in the quotient by both unit
# normal equations. No square roots or orbit-specific values are used.
c, r, p, q, h, k, H, e, D = s.symbols('c r p q h k H e D', real=True)
n, nn = s.Matrix([c,r]), s.Matrix([p,q])
U = s.Matrix([c*c-r*r, 2*c*r])
V = s.Matrix([p*p-q*q, 2*p*q])
Bi = s.Matrix([[U[0],U[1]],[U[1],-U[0]]])/2
Bj = s.Matrix([[V[0],V[1]],[V[1],-V[0]]])/2
wi, wj = h*n, k*nn
direct = s.zeros(2)
for col in range(2):
    m = s.eye(2)[:,col]
    direct[:,col] = -cross(wi,wj)*(Bi+Bj)*m - (
        cross(wi,Bj*m)+cross(Bi*m,wj))*(wi+wj)

def phi(z):
    f = H*z[0]+e*(z[0]**2-z[1]**2)
    g = H*z[1]+2*e*z[0]*z[1]
    return s.Matrix([[g+e*z[1],-f-e*z[0]],
                     [-f+e*z[0],e*z[1]-g]])/4

alpha = cross(U,V)
ux, uy = U+V
nonendpoint = -alpha*s.Matrix([
    [D+2*H+3*e+(2*D+e)*ux, (2*D-e)*uy],
    [(2*D+e)*uy, D+2*H-3*e+(e-2*D)*ux]])/4
expected = phi(U)-phi(V)+nonendpoint
relations = s.groebner([c*c+r*r-1,p*p+q*q-1], c,r,p,q)

def normal_reduce(polynomial):
    pp = s.Poly(s.expand(polynomial), c,r,p,q)
    # Domain EX permits the independent H,e,D coefficients.
    gb = s.groebner([c*c+r*r-1,p*p+q*q-1], c,r,p,q, domain=s.EX)
    return s.expand(gb.reduce(pp.as_expr())[1])

for i in range(2):
    for j in range(2):
        poly = s.Poly(s.expand(direct[i,j]), h,k)
        assert set(poly.monoms()) <= {(2,0),(0,2),(1,1)}
        real = poly.coeff_monomial(h*h)*(H+e*U[0])
        real += poly.coeff_monomial(k*k)*(H+e*V[0])
        real += poly.coeff_monomial(h*k)*(D*(c*p+r*q)+e*(c*p-r*q))
        eq(f'general real linear edge matrix {i}{j}', normal_reduce(4*(real-expected[i,j])))

# Pure cubic term: double-normal matrix has determinant -1, hence pairing
# produces -R^2/8 times alpha times A(U+V)m.
X,Y = s.symbols('X Y', real=True)
m = s.Matrix([X,Y])
eq('cubic determinant real identity', normal_reduce(
    4*cross(Bi*m,Bj*m)-(X*X+Y*Y)*alpha))

# Independent real unit-circle lemma, including zero signed area cases.
xi,yi,xj,yj = s.symbols('xi yi xj yj', real=True)
uu,vv = s.Matrix([xi,yi]),s.Matrix([xj,yj])
aa = cross(uu,vv)
diff = aa*(uu+vv)-(1+uu.dot(vv))*s.Matrix([yj-yi,xi-xj])
gb=s.groebner([xi*xi+yi*yi-1,xj*xj+yj*yj-1],xi,yi,xj,yj)
for j in range(2):
    eq(f'unit-circle real lemma {j}', gb.reduce(s.expand(diff[j]))[1])

# Support conversion from eccentric-angle dot products to unit normals.
A,B,lam=s.symbols('A B lam', positive=True)
hh,ee=(A+B)/2,(A-B)/2
dd=1-lam*(1/A+1/B)
ff=hh*dd+2*lam
eq('eccentric support cosine coefficient',(ff+ee*dd)/A-(1+lam*(1/A-1/B)))
eq('eccentric support sine coefficient',(ff-ee*dd)/B-(1-lam*(1/A-1/B)))
eq('F plus ed identity',ff+ee*dd-(A-lam*(A/B-1)))
eq('F minus ed identity',ff-ee*dd-(B+lam*(1-B/A)))
eq('four-period lambda',dd.subs(lam,A*B/(A+B)))
eq('d to v equality',2*ee*(hh-ff/dd)/((ff/dd)**2-ee**2)+4*ee*lam*dd/(ff**2-ee**2*dd**2))

# The stated squaring identity follows exactly from squared support relation.
sq=(D*(c*p+r*q)+e*(c*p-r*q))**2-(H+e*U[0])*(H+e*V[0])
target=(D*D-e*e)*(c*p+r*q)**2-(H*H-e*e+e*(H-D)*(U[0]+V[0]))
eq('squared support relation',normal_reduce(sq-target))

# General translation checked without geometric support or nonzero area.
coordinates=s.symbols('x0 y0 x1 y1 x2 y2',real=True)
cc=s.Matrix(s.symbols('cx cy',real=True))
triangle=[s.Matrix(coordinates[2*i:2*i+2]) for i in range(3)]
sa,ta=moments(triangle)
sb,tb=moments([x+cc for x in triangle])
eq('signed area translation',sb-sa)
for j in range(2):
    eq(f'signed moment translation {j}',tb[j]-ta[j]-6*sa*cc[j])

# The rectangle case is unrestricted in the pedal point.
aa,bb=s.symbols('aa bb',positive=True)
rect=[s.Matrix([aa,Y]),s.Matrix([X,bb]),s.Matrix([-aa,Y]),s.Matrix([X,-bb])]
sr,tr=moments(rect)
eq('rectangle signed area',sr-2*aa*bb)
for j in range(2):
    eq(f'rectangle signed moment {j}',tr[j]-4*aa*bb*m[j])

# Exact eight-period star from direct Cartesian projection, tangent
# discriminants, physical reflection, and a ray winding algorithm.
a2=s.Rational(221,96)
b2=s.Rational(27625,20736)
ll=s.Rational(125,96)
a,b=s.sqrt(a2),s.sqrt(b2)
pairs=[(0,1),(-s.Rational(12,13),-s.Rational(5,13)),(1,0),
       (-s.Rational(12,13),s.Rational(5,13)),(0,-1),
       (s.Rational(12,13),s.Rational(5,13)),(-1,0),
       (s.Rational(12,13),-s.Rational(5,13))]
points=[s.Matrix([a*u,b*v]) for u,v in pairs]
feet=[]
for i,P in enumerate(points):
    nraw=s.Matrix([P[0]/a2,P[1]/b2])
    feet.append((m+(1-nraw.dot(m))/nraw.dot(nraw)*nraw).applyfunc(s.simplify))
    prev,nxt=points[i-1],points[(i+1)%8]
    vel0,vel1=P-prev,nxt-P
    vel0=(vel0/s.sqrt(vel0.dot(vel0))).applyfunc(s.simplify)
    vel1=(vel1/s.sqrt(vel1.dot(vel1))).applyfunc(s.simplify)
    reflected=vel0-2*vel0.dot(nraw)/nraw.dot(nraw)*nraw
    for j in range(2):
        eq(f'star specular reflection {i} {j}',reflected[j]-vel1[j])
    chord=nxt-P
    coef2=chord[0]**2/(a2-ll)+chord[1]**2/(b2-ll)
    coef1=2*(P[0]*chord[0]/(a2-ll)+P[1]*chord[1]/(b2-ll))
    coef0=P[0]**2/(a2-ll)+P[1]**2/(b2-ll)-1
    eq(f'star caustic discriminant {i}',coef1**2-4*coef2*coef0)
    eq(f'star boundary {i}',P[0]**2/a2+P[1]**2/b2-1)
    assert cross(P,nxt)>0
    checks.append(f'star forward increment less than half turn {i}')
assert len(set(pairs))==8
assert pairs[4:]==[(-u,-v) for u,v in pairs[:4]]

def winding(vertices):
    wn=0
    for u,v in zip(vertices,vertices[1:]+vertices[:1]):
        det=u[0]*v[1]-u[1]*v[0]
        if u[1]<=0<v[1] and det>0: wn+=1
        if v[1]<=0<u[1] and det<0: wn-=1
    return wn
assert winding(pairs)==3 and winding(pairs[::-1])==-3
assert winding([(-u,v) for u,v in pairs])==-3
checks.append('star distinct primitive vertices and exact 3 winding with reversal/reflection')

ss,tt=moments(feet)
R=X*X+Y*Y
expected_area=-s.sqrt(30)*(20736*R-123539)/134784
expected_moment=s.Matrix([-s.sqrt(30)*X*(41472*R-272935)/109512,
                          -s.sqrt(30)*Y*(52992*R-347633)/97344])
eq('star unrestricted polynomial area',ss-expected_area)
for j in range(2):
    eq(f'star unrestricted cubic moment {j}',tt[j]-expected_moment[j])
H0,e0=(a2+b2)/2,(a2-b2)/2
d0=1-ll*(1/a2+1/b2)
F0=H0*d0+2*ll
v0=-4*e0*ll*d0/(F0**2-e0**2*d0**2)
for name,actual,claimed in [('d',d0,-s.Rational(120,221)),('F',F0,s.Rational(2795,1728)),
                            ('v',v0,s.Rational(7,13)),('zero radius squared',-2*F0/d0,s.Rational(123539,20736))]:
    eq('star '+name,actual-claimed)
G=2*F0+d0*R
cc0=F0+2*H0*d0+e0*v0*d0
cc1=2*F0*v0+3*e0*d0+v0*d0*R/2
formula=s.Matrix([X/2-X*(cc0+cc1)/(3*G),Y/2-Y*(cc0-cc1)/(3*G)])
for j in range(2):
    eq(f'star explicit centroid formula numerator {j}',6*ss*formula[j]-tt[j])
zero={X:13*s.sqrt(731)/144,Y:0}
eq('diagnostic zero signed area',ss.subs(zero))
eq('diagnostic nonzero first moment',tt[0].subs(zero)-221*s.sqrt(21930)/10368)
eq('diagnostic zero transverse moment',tt[1].subs(zero))

# Global numerator identities survive reversing and reflecting signed data.
rev_area,rev_moment=moments(feet[::-1])
eq('star reversed area',rev_area+ss)
for j in range(2):
    eq(f'star reversed first moment {j}',rev_moment[j]+tt[j])
reflection=s.diag(-1,1)
reflect_area,reflect_moment=moments([reflection*f for f in feet])
eq('star reflected area',reflect_area+ss)
for j in range(2):
    eq(f'star reflected first moment {j}',reflect_moment[j]+(reflection*tt)[j])

out={'timestamp_utc':datetime.now(timezone.utc).isoformat(),
     'status':'PASS','sympy_version':s.__version__,'assertion_count':len(checks),
     'checks':checks,'mechanism':'real Cartesian paired-edge matrix with exact endpoint potential; unrestricted exact star projections'}
(HERE/'FRESH_EXACT_RECEIPT.json').write_text(json.dumps(out,indent=2)+'\n')
print(f'PASS: {len(checks)} fresh exact assertions')
