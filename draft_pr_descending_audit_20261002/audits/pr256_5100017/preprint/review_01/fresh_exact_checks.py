"""Fresh coefficient and Cartesian-star checks, derived from projection/shoelace.

No archived verification code is imported or executed here. The all-period
logical deductions are recorded separately in INDEPENDENT_MECHANISM.md.
"""
from pathlib import Path
import sympy as s
import json, sys, datetime

HERE = Path(__file__).resolve().parent
checks = []

def check(label, value):
    reduced = s.factor(s.cancel(s.expand(value)))
    assert reduced == 0, (label, reduced)
    checks.append(label)

x, y = s.symbols('x y', nonzero=True)
h, k, t, tc, H, e, D = s.symbols('h k t tc H e D')
I = s.I
Z, W = x*x, y*y
Vi, Vj = h*x-t*Z, k*y-t*W
Vic, Vjc = h/x-tc/Z, k/y-tc/W
raw = s.expand((Vic*Vj-Vi*Vjc)*(Vi+Vj))
average = s.expand((raw+raw.subs({x:-x,y:-y}, simultaneous=True))/2)
P = s.Poly(average, t, tc)
c = P.coeff_monomial(t)
b = P.coeff_monomial(tc)
cubic = P.coeff_monomial(t*t*tc)
check('antipodal moment has only linear and cubic terms',
      average-c*t-b*tc-cubic*t*t*tc)
check('directly derived t coefficient',
      c-(k*k*Z-h*h*W+2*h*k*(x**3/y-y**3/x)))
check('directly derived conjugate t coefficient',
      b-(h*h*Z/W-k*k*W/Z+h*k*(x/y-y/x)))
check('directly derived cubic scaling', cubic+(W/Z-Z/W)*(Z+W))

h2 = H+e*(Z+1/Z)/2
k2 = H+e*(W+1/W)/2
hk = D*(y/x+x/y)/2+e*(x*y+1/(x*y))/2
def supports(expr):
    return s.expand(expr).subs({h*h:h2,k*k:k2,h*k:hk}, simultaneous=True)

r = Z/W-W/Z
ss = Z*Z/W-W*W/Z
cp = supports(c)
bp = supports(b)
check('full t coefficient endpoint identity',
      cp-D*ss-3*e*r/2-(D+H)*(Z-W)-e*(Z*Z-W*W))
check('full conjugate t coefficient endpoint identity',
      bp-(D/2+H)*r-e*ss/2-e*(Z-W)/2-e*(1/W-1/Z))
crossZW = (W/Z-Z/W)/(2*I)
check('r cross product normalization', r+2*I*crossZW)
check('s first moment endpoint identity', ss+2*I*crossZW*(Z+W)-(W-Z))
cosdelta = (y/x+x/y)/2
cospsi = (Z+1/Z)/2
cosphi = (W+1/W)/2
target = H*H-e*e+e*(H-D)*(cospsi+cosphi)-(D*D-e*e)*cosdelta**2
check('squared support relation',h2*k2-hk*hk-target)
sindelta=(y/x-x/y)/(2*I)
check('origin-area endpoint identity',
      hk*sindelta-D*crossZW/2-e*((W-1/W)-(Z-1/Z))/(4*I))

U,V=s.symbols('U V', nonzero=True)
crossUV=(V/U-U/V)/(2*I)
dotUV=(V/U+U/V)/2
check('unit-circle division-free moment identity',
      crossUV*(U+V)+I*(1+dotUV)*(V-U))

z,zc,Sz,v,d,F,lam=s.symbols('z zc Sz v d F lam', nonzero=True)
area=(D/2+z*zc/4)*Sz
TV=-2*Sz*((zc/2)*(D*v+3*e/2+v*z*zc/4)+(z/2)*(D/2+H+e*v/2))
centroid=z/2+TV/(6*area)
Dformula=z/2-(z*(D+2*H+e*v)+zc*(2*D*v+3*e+v*z*zc/2))/(3*(2*D+z*zc))
check('full moment-to-centroid algebra',centroid-Dformula)
dformula=z/2-(z*(F+2*H*d+e*v*d)+zc*(2*F*v+3*e*d+v*d*z*zc/2))/(3*(2*F+d*z*zc))
check('D to d formula conversion',Dformula.subs(D,F/d)-dformula)
check('v parameter conversion',
      (2*e*(H-D)/(D*D-e*e)).subs(D,(H*d+2*lam)/d)
      +4*e*lam*d/((H*d+2*lam)**2-e*e*d*d))
check('area ratio conversion',area.subs(D,F/d)/(F*Sz/(2*d))-(2*F+d*z*zc)/(2*F))
check('four-period formula limit',dformula.subs({d:0,v:0})-z/3)

px,py,qx,qy,cx,cy=s.symbols('px py qx qy cx cy')
p=s.Matrix([px,py]); q=s.Matrix([qx,qy]); cc=s.Matrix([cx,cy])
def cross(p,q): return p[0]*q[1]-p[1]*q[0]
def potential(p):
    return s.Matrix([cx*p[0]*p[1]-cy*p[0]**2,
                     cx*p[1]**2-cy*p[0]*p[1]])+2*cc*cross(cc,p)
delta = cross(p+cc,q+cc)*(p+q+2*cc)-cross(p,q)*(p+q)-3*cc*cross(p,q)
for j in range(2):
    check('translation moment endpoint potential '+str(j),delta[j]-(potential(q)-potential(p))[j])

A,B,X,Y=s.symbols('A B X Y', real=True)
def moments(poly):
    area=0; mm=s.zeros(2,1)
    for p,q in zip(poly,poly[1:]+poly[:1]):
        v=cross(p,q)
        area+=v/2
        mm+=v*(p+q)
    return s.simplify(area),[s.simplify(mm[j]) for j in range(2)]

rect=[s.Matrix(p) for p in [(A,Y),(X,B),(-A,Y),(X,-B)]]
Srect,Trect=moments(rect)
check('rectangle area',Srect-2*A*B)
check('rectangle x moment',Trect[0]-4*A*B*X)
check('rectangle y moment',Trect[1]-4*A*B*Y)

R=s.Rational
a2,b2,lam=R(221,96),R(27625,20736),R(125,96)
a,bb=s.sqrt(a2),s.sqrt(b2)
normalized=[(0,1),(-R(12,13),-R(5,13)),(1,0),(-R(12,13),R(5,13)),
            (0,-1),(R(12,13),R(5,13)),(-1,0),(R(12,13),-R(5,13))]
poly=[s.Matrix([a*u,bb*v]) for u,v in normalized]
assert len(set(normalized))==8
checks.append('eight distinct vertices, primitive period eight')
Ec=s.diag(a2-lam,b2-lam)
Q=[]
for j,p in enumerate(poly):
    q=poly[(j+1)%8]
    check('ellipse membership '+str(j),p[0]**2/a2+p[1]**2/b2-1)
    L=s.Matrix([q[1]-p[1],p[0]-q[0]])
    level=(L.dot(p))
    check('exact chord-caustic tangency '+str(j),(L.T*Ec*L)[0]-level**2)
    # Unit incoming and outgoing velocities satisfy reflection in the true
    # boundary normal; lengths are computed from actual Cartesian coordinates.
    previous=poly[(j-1)%8]
    incoming=p-previous; outgoing=q-p
    vin=incoming/s.sqrt(incoming.dot(incoming))
    vout=outgoing/s.sqrt(outgoing.dot(outgoing))
    normal=s.Matrix([p[0]/a2,p[1]/b2])
    reflected=vin-2*vin.dot(normal)/normal.dot(normal)*normal
    for axis in range(2):
        check('specular reflection '+str(j)+','+str(axis),vout[axis]-reflected[axis])
    assert s.sign(cross(p,q))==1
    checks.append('origin left of forward chord '+str(j))
    M=s.Matrix([X,Y])
    foot=M+(1-normal.dot(M))/normal.dot(normal)*normal
    Q.append(foot)

Sstar,Tstar=moments(Q)
expectedS=-s.sqrt(30)*(20736*(X*X+Y*Y)-123539)/134784
expectedTx=-s.sqrt(30)*X*(41472*(X*X+Y*Y)-272935)/109512
expectedTy=-s.sqrt(30)*Y*(52992*(X*X+Y*Y)-347633)/97344
check('unrestricted Cartesian star area',Sstar-expectedS)
check('unrestricted Cartesian star x moment',Tstar[0]-expectedTx)
check('unrestricted Cartesian star y moment',Tstar[1]-expectedTy)
pedalzero={X:13*s.sqrt(731)/144,Y:0}
check('diagnostic zero area',Sstar.subs(pedalzero))
check('diagnostic nonzero moment',Tstar[0].subs(pedalzero)-221*s.sqrt(21930)/10368)
check('diagnostic zero y moment',Tstar[1].subs(pedalzero))

# Positive x ray with half-open y convention. Coordinates have positive
# diagonal scaling, so exact rational normalized coordinates suffice.
winding=0; crossings=[]
for j,(p,q) in enumerate(zip(normalized,normalized[1:]+normalized[:1])):
    det=s.expand(p[0]*q[1]-p[1]*q[0])
    change=0
    if p[1]<=0<q[1] and det>0: change=1
    if q[1]<=0<p[1] and det<0: change=-1
    winding+=change; crossings.append(change)
assert winding==3
checks.append('exact half-open oriented ray winding three')
d=1-lam*(1/a2+1/b2)
HH=(a2+b2)/2; ee=(a2-b2)/2
F=HH*d+2*lam
vv=-4*ee*lam*d/(F*F-ee*ee*d*d)
for label,value in [('star d',d+R(120,221)),('star F',F-R(2795,1728)),
                    ('star v',vv-R(7,13)),('star radius',-2*F/d-R(123539,20736))]:
    check(label,value)

receipt={'status':'PASS','timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
         'checks':checks,'check_count':len(checks),'runtime':sys.version,
         'sympy_version':s.__version__,'mechanism':'direct antipodal complex projection expansion and independent Cartesian shoelace',
         'derived_t_coefficient':str(c),'derived_conjugate_t_coefficient':str(b),
         'derived_cubic_coefficient':str(cubic),'star_winding':winding,'star_ray_crossings':crossings,
         'star_area':str(Sstar),'star_moment':list(map(str,Tstar))}
(HERE/'FRESH_EXACT_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
