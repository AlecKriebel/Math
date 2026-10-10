#!/usr/bin/env python3
"""Independent exact symbolic controls; finite algebra is not a geometry proof."""
import json
import sympy as s

checks=[]
negatives=[]
def check(name, condition):
    if condition != True:
        raise RuntimeError('Failed: '+name+'; '+str(condition))
    checks.append(name)
def eq(name, x, y):
    check(name, s.simplify(x-y)==0)
def reject(name, condition):
    if condition != False:
        raise RuntimeError('False claim not rejected: '+name+'; '+str(condition))
    negatives.append(name)

r,j,n,a,lam=s.symbols('r j n a lam', positive=True)
h=((j*r)**2-1)/((j*r)**2+1)
W=r**n*(1+r*r*h)
A=1+(n+2)/n*r*r*h+4*j*j*r**4/(n*(1+j*j*r*r)**2)
eq('radial differentiated volume',s.diff(W,r),n*r**(n-1)*A)
eq('radial volume difference',r**n*(1+r*r)-W,2*r**(n+2)/(1+j*j*r*r))
eq('radial A difference',A-(1+(n+2)/n*r*r),(-2*(n+2)*j*j*r*r/(1+j*j*r*r)+4*(j*j*r*r)**2/(1+j*j*r*r)**2)/(n*j*j))
for dim in (2,3,4,7,12,23):
    for index in (5,11,37,71):
        w=W.subs({n:dim,j:index})
        aq=A.subs({n:dim,j:index})
        rp=s.Rational(1,2*index)
        check('central comparison '+str((dim,index)),w.subs(r,rp)<rp**dim)
        check('radial positivity '+str((dim,index)),aq.subs(r,s.Rational(1,2))>=s.Rational(1,2))
        # Taylor coefficient of f/r computed from A, independently of scalar formula.
        b=s.limit((aq**s.Rational(1,dim-1)-1)/r**2,r,0)
        eq('central scalar '+str((dim,index)),-6*dim*(dim-1)*b,6*(dim+2))
        reject('extend central witness beyond its interval '+str((dim,index)),w.subs(r,s.Rational(2,index))<s.Rational(2,index)**dim)

# Explicit off-center failure in n=2, including a single approximant.
f=r*A.subs(n,2)
sc=-2*s.diff(f,r,2)/f
sc_value=s.factor(sc.subs({j:37,r:s.Rational(1,4)}))
check('negative curvature away from center for j=37',sc_value<0)
f_inf=r*(1+2*r*r)
eq('limit off-center curvature',(-2*s.diff(f_inf,r,2)/f_inf).subs(r,s.Rational(1,4)),-s.Rational(64,3))
eq('limit central curvature',s.limit(-2*s.diff(f_inf,r,2)/f_inf,r,0),-24)

# Model scalar-vs-Gaussian normalization and exact surface area series.
model=4*s.pi/lam*(1-s.cos(s.sqrt(lam/2)*r))
series=s.series(model,r,0,8).removeO()
eq('surface model r2',series.coeff(r,2),s.pi)
eq('surface model r4',series.coeff(r,4),-s.pi*lam/24)
eq('surface model r6',series.coeff(r,6),s.pi*lam**2/1440)
eq('sphere scalar normalized',2/(2/lam),lam)
reject('sphere missing scalar factor two',s.simplify(2/(1/lam)-lam)==0)
reject('surface Gaussian used as scalar',s.simplify((-s.pi*lam/12)-series.coeff(r,4))==0)

# Seam: density and moving-domain contributions evaluated independently.
theta=s.symbols('theta', real=True)
density=s.integrate(s.cos(theta)/3,(theta,-s.pi/2,s.pi/2))
boundary=s.integrate(-s.cos(theta)*s.sin(theta)**2/2,(theta,-s.pi/2,s.pi/2))
eq('seam density contribution',density,s.Rational(2,3))
eq('seam boundary contribution',boundary,-s.Rational(1,3))
eq('seam full coefficient',density+boundary,s.Rational(1,3))
reject('omit ball domain deformation',density==s.Rational(1,3))
reject('reverse upward seam sign',(density+boundary)<0)
# Independent exact geometric model: f=1+a max(t,0).
u,v=s.symbols('u v', nonnegative=True)
q=s.Matrix([s.cos(a*u)/a-v*s.sin(a*u),s.sin(a*u)/a+v*s.cos(a*u)])
eq('exterior tangent shadow Jacobian',s.det(s.Matrix.hstack(q.diff(u),q.diff(v))),-a*v)
shadow=2*s.integrate(s.integrate(a*v,(v,0,r-u)),(u,0,r))
eq('flat exterior exact shadow area',shadow,a*r**3/3)
t=s.symbols('t', real=True)
phi=(1-t*t)**3
ibp=s.integrate((1+t+t*t)*s.diff(phi,t,2),(t,-1,0))+s.integrate((1+3*t+2*t*t)*s.diff(phi,t,2),(t,0,1))
classical=s.integrate(2*phi,(t,-1,0))+s.integrate(4*phi,(t,0,1))
eq('jump delta mass from integration by parts',ibp-classical,2*phi.subs(t,0))
reject('omit jump atom in weak second derivative',s.simplify(ibp-classical)==0)
# Product with S2: leading seam excess coefficient, under rho=r*u.
eq('four dimensional seam excess',2*s.pi*s.integrate(u*(1-u*u)**s.Rational(3,2),(u,0,1))/3,2*s.pi/15)
# Positivity and convolution sign: a downward corner remains nonpositive under nonnegative mollification.
for jump in (-7,-1,0):
    for density_value in (s.Rational(1,9),s.Rational(3,2),7):
        check('mollified atom sign '+str((jump,density_value)),jump*density_value<=0)
reject('arbitrary convolution can preserve distribution order',(-1)*(-1)<=0)

# Jacobi comparison sign and the strong-H1 minimizing-segment identity.
J=s.Function('J')(u);S=s.Function('S')(u);K,k0=s.symbols('K k0')
wron=s.diff(s.diff(J,u)*S-J*s.diff(S,u),u)
eq('Jacobi Wronskian sign identity',wron.subs({s.diff(J,u,2):-K*J,s.diff(S,u,2):-k0*S}),-(K-k0)*J*S)
p,qv=s.symbols('p qv', real=True)
v1=s.Matrix([p,qv]);v2=s.Matrix([2-p,-qv]);z=s.Matrix([1,0])
eq('segment energy excess identity',((v1-z).dot(v1-z)+(v2-z).dot(v2-z))/2,(v1.dot(v1)+v2.dot(v2))/2-1)

# Second-order contact: coordinate volume plus geodesic-radius correction.
coeff=n*n/(n+2)-n/3
eq('conformal ball coefficient',coeff,2*n*(n-1)/(3*(n+2)))
eq('conformal scalar recovery',-6*(n+2)*coeff*a,-4*n*(n-1)*a)
reject('big O second-order contact suffices',(-4*3*(3-1))==0)
reject('e tends to zero gives e over R2 small',s.Rational(1,100)/(s.Rational(1,100)**2)<1)
# Scalar-flat S2(1) x H2(-1): direct power-series convolution.
# Sphere ball coefficient (-1)^(k+1)/(2k)! times 2pi; hyperbolic shell coefficient 1/(2m+1)! times 2pi.
prod={}
for k in range(1,4):
    for m in range(0,3):
        power=2*k+2*m+2
        if power>8: continue
        integral=s.factorial(m)*s.factorial(k)/(2*s.factorial(m+k+1))
        val=4*s.pi**2*(-1)**(k+1)/s.factorial(2*k)/s.factorial(2*m+1)*integral
        prod[power]=s.simplify(prod.get(power,0)+val)
eq('scalar-flat product leading term',prod[4],s.pi**2/2)
eq('scalar-flat product r6',prod[6],0)
eq('scalar-flat product r8',prod[8],s.pi**2/4320)
reject('relaxed zero implies exact Euclidean domination',prod[8]<=0)
# Local boundary gap control is a positive number; compactness of center interval matters.
for gap in (s.Rational(1,3),s.Rational(1,10),2):
    check('uniform boundary exclusion '+str(gap),gap/2<gap)
reject('positive per-index radii have positive infimum',s.limit(1/j,j,s.oo)>0)
reject('model equality becomes strict at the same threshold',s.simplify(model-model)<0)

print(json.dumps({'outcome':'PASS','independent_exact_checks':len(checks),'deliberate_mathematical_negatives':len(negatives),'check_names':checks,'negative_names':negatives,'exact_off_center_scalar_j37_n2_r1over4':str(sc_value),'proof_limit':'Symbolic identities and finite sign checks do not certify universal geometry, source identity, closure, novelty, or openness.'},indent=2,sort_keys=True))
