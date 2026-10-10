#!/usr/bin/env python3
"""Independent audit only: exact algebra + nonvalidated fixed-step RK4 controls.
Run from any working directory. Does not import or modify frozen code.
Requires Python 3, NumPy, SymPy; optional --output result.json.
"""
import argparse, hashlib, json, math, platform, sys
from pathlib import Path
import numpy as np
import sympy as S

T=2*math.pi
checks=[]
def verified(name,condition):
    assert bool(condition),name
    checks.append(name)

t, R, ep, alpha, beta = S.symbols('t R ep alpha beta',real=True)
a,b,c,d,e=S.symbols('a b c d e',real=True)
B=S.cos(t)+S.sin(t); C=S.cos(t)*S.sin(t)
H=S.sin(t)+1-S.cos(t); J=S.sin(t)**2/2
K=S.integrate(C*H,(t,0,t))
u=[R,R**2*H,R**3*(H**2+J),R**4*(H**3+2*H*J+K)]
series=sum(ep**k*u[k] for k in range(4))
f=ep*B*series**2+ep**2*C*series**3+ep**4*(-alpha*series+beta*S.cos(t)**2*series**3)
for k in [1,2,3]:
    target=S.expand(f).coeff(ep,k)
    verified(f'full perturbation recurrence order {k}',S.trigsimp(S.diff(u[k],t)-target)==0)
    verified(f'zero initial and terminal coefficient order {k}',S.simplify(u[k].subs(t,0))==0 and S.simplify(u[k].subs(t,2*S.pi))==0)
u4prime=S.expand(f).coeff(ep,4)
q_integrated=S.integrate(S.expand_trig(S.expand(u4prime)),(t,0,2*S.pi))
Q=S.pi*R*(-2*alpha+beta*R**2-R**4/2)
verified('full fourth-order coefficient integral',S.simplify(q_integrated-Q)==0)
q=Q.subs({alpha:S.Rational(1,2),beta:2})
for sign in [-1,1]:
    z=2+sign*S.sqrt(2); root=S.sqrt(z)
    verified(f'exact root {sign}',S.simplify(q.subs(R,root))==0)
    verified(f'exact derivative {sign}',S.simplify(S.diff(q,R).subs(R,root)-2*S.pi*z*(2-z))==0)
# Derive the full harmonic reciprocal-square solution by solving coefficients.
k0,k1,k2=S.symbols('k0 k1 k2',real=True)
z=k0+k1*S.cos(2*t)+k2*S.sin(2*t)
sol=S.solve([2*a*k0+d,2*k2+2*a*k1+d,-2*k1+2*a*k2+e],[k0,k1,k2])
expected={k0:-d/(2*a),k1:(e-a*d)/(2*(1+a*a)),k2:-(d+a*e)/(2*(1+a*a))}
verified('independent harmonic linear solve',all(S.simplify(sol[k]-expected[k])==0 for k in expected))
amp2=S.factor(sol[k1]**2+sol[k2]**2)
verified('reciprocal positivity reduction',S.simplify(sol[k0]**2-amp2-(d*d-a*a*e*e)/(4*a*a*(a*a+1)))==0)
# Schwarzian-to-curvature and variational identity without importing supplied check.
w,v,j3,j4=S.symbols('w v j3 j4',positive=True)
h=w**S.Rational(-1,2)
h2=S.diff(h,w,2)*v*v+S.diff(h,w)*j3
verified('h curvature Schwarzian identity',S.simplify(h2+S.Rational(1,2)*(j3/w-S.Rational(3,2)*(v/w)**2)*h)==0)
x,y,aa,bb,cc=S.symbols('x y aa bb cc',nonzero=True)
ff=lambda x: aa*x+bb*x*x+cc*x**3
verified('reciprocal pair identity',S.factor((ff(y)-ff(x))/(y-x)-ff(x)/x-ff(y)/y+aa-cc*x*y)==0)
# Original planar conversion, including theta dot.
xx,yy,rr,ang=S.symbols('x y r ang',real=True)
F=a+b*xx+c*yy+d*xx**2+e*xx*yy
fx=-yy+xx*F; fy=xx+yy*F
verified('angular speed identity',S.expand(xx*fy-yy*fx-(xx*xx+yy*yy))==0)
verified('radial identity',S.expand(xx*fx+yy*fy-(xx*xx+yy*yy)*F)==0)

# Independent fixed-step fourth-order method. No SciPy solver is used.
def rk4(p,r0,n=8192,scaled=False,epsilon=None):
    h=T/n; y=np.array([r0,0.],dtype=np.longdouble)
    a,b,c,d,e=map(np.longdouble,p)
    def rhs(t,y):
        r=y[0]; co=np.cos(np.longdouble(t)); si=np.sin(np.longdouble(t))
        B=b*co+c*si; C=d*co*co+e*co*si
        if scaled:
            eps=np.longdouble(epsilon)
            return np.array([a*r+eps*B*r*r+eps*eps*C*r**3,a+2*eps*B*r+3*eps*eps*C*r*r],dtype=np.longdouble)
        return np.array([a*r+B*r*r+C*r**3,a+2*B*r+3*C*r*r],dtype=np.longdouble)
    for k in range(n):
        t=np.longdouble(k)*np.longdouble(h)
        k1=rhs(t,y);k2=rhs(t+h/2,y+h*k1/2);k3=rhs(t+h/2,y+h*k2/2);k4=rhs(t+h,y+h*k3)
        y+=h*(k1+2*k2+2*k3+k4)/6
    return {'delta':float(y[0]-r0),'log_multiplier':float(y[1])}
base=Path(__file__).resolve().parent.parent
parser=argparse.ArgumentParser(); parser.add_argument('--output',type=Path); parser.add_argument('--packet',type=Path,default=base/'frozen'); args=parser.parse_args()
frozen=json.loads((args.packet/'numerical-results.json').read_text())
controls=[]
for family in frozen['two_cycle_family']:
    p=family['parameters_abcde']
    verified(f"refinement count epsilon {family['epsilon']}",len(family['refined_roots'])==len(family['bracketed_roots'])==2)
    for i,row in enumerate(family['refined_roots']):
        coarse=rk4(p,row['radius'],4096); fine=rk4(p,row['radius'],8192)
        verified(f"independent RK4 periodicity epsilon {family['epsilon']} root {i}",abs(fine['delta'])<2e-11)
        verified(f"independent RK4 exponent epsilon {family['epsilon']} root {i}",abs(fine['log_multiplier']-row['log_multiplier'])<2e-10)
        verified(f"independent RK4 stability epsilon {family['epsilon']} root {i}",(fine['log_multiplier']>0)==(i==0))
        controls.append({'epsilon':family['epsilon'],'root_index':i,'radius':row['radius'],'rk4_4096':coarse,'rk4_8192':fine,'reference_log_multiplier':row['log_multiplier']})
# Constant-amplitude homogeneous cases test both time/stability orientations.
homogeneous=[]
for p in [[.1,0,0,-1,.5],[-.1,0,0,1,.5],[.5,0,0,-1,0],[-.5,0,0,1,0]]:
    a,b,c,d,e=p; z0=-d/(2*a)+(e-a*d)/(2*(1+a*a)); r0=1/math.sqrt(z0)
    got=rk4(p,r0)
    verified(f'homogeneous periodicity {p}',abs(got['delta'])<2e-11)
    verified(f'homogeneous exponent {p}',abs(got['log_multiplier']+4*math.pi*a)<2e-10)
    homogeneous.append({'parameters':p,'radius':r0,'flow':got})
# Sanity checks of scaled displacement against the EXACT return polynomial,
# only in the already-claimed local perturbation family, not a new search.
asymptotic=[]
for eps in [.04,.02,.01]:
    for r0 in [.5,1.,2.]:
        p=[-eps**4/2,1,1,2*eps**2,1]
        got=rk4(p,r0,8192,True,eps)
        measured=got['delta']/eps**4
        predicted=math.pi*r0*(-1+2*r0*r0-r0**4/2)
        asymptotic.append({'epsilon':eps,'scaled_initial_radius':r0,'scaled_displacement':measured,'Q':predicted,'absolute_error':abs(measured-predicted)})
for r0 in [.5,1.,2.]:
    subset=[x for x in asymptotic if x['scaled_initial_radius']==r0]
    verified(f'local coefficient convergence R={r0}',all(subset[k+1]['absolute_error']<subset[k]['absolute_error'] for k in range(2)))
# Exact positive/zero/negative reciprocal minima around the claimed infinity boundary.
boundary=[]
for ee in [1.99,2.,2.01]:
    a,d=.5,-1.; mu=-d/(2*a); amp=math.sqrt(d*d+ee*ee)/(2*math.sqrt(1+a*a))
    boundary.append({'a':a,'d':d,'e':ee,'reciprocal_minimum':mu-amp,'criterion':(-d/a>0 and d*d>a*a*ee*ee)})
verified('boundary strictness',boundary[0]['reciprocal_minimum']>0 and abs(boundary[1]['reciprocal_minimum'])<1e-14 and boundary[2]['reciprocal_minimum']<0)
result={'status':'PASS','note':'Numerical checks are nonvalidated corroboration, not global or finite-epsilon existence certificates. Exact algebra is separately marked.','python':sys.version.split()[0],'sympy':S.__version__,'numpy':np.__version__,'longdouble_mantissa_bits':np.finfo(np.longdouble).nmant,'check_count':len(checks),'checks':checks,'independent_RK4_two_cycle_controls':controls,'independent_homogeneous_controls':homogeneous,'local_coefficient_checks':asymptotic,'infinity_boundary_checks':boundary}
text=json.dumps(result,indent=2)+'\n'
if args.output: args.output.write_text(text)
else: print(text,end='')
