"""Independent exact controls, authored before any submitted helper was read."""
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import datetime,json,hashlib
import sympy as S

out=Path(__file__).resolve().parent
checks={}
def check(name,condition,evidence):
    assert condition,name
    checks[name]={'pass':True,'evidence':str(evidence)}
h,a,eps,t,r,A,R,rho,k=S.symbols('h a eps t r A R rho k',positive=True)
e=S.sin(S.pi*r)/(S.sqrt(2*S.pi)*r)
check('radial_mode_norm',S.integrate(4*S.pi*r*r*e*e,(r,0,1))==1,'4*pi integral r^2 e(r)^2 dr=1')
check('radial_eigen_equation',S.simplify(-S.diff(e,r,2)-2*S.diff(e,r)/r-S.pi**2*e)==0,'-e_rr-2e_r/r=pi^2 e')
check('radial_origin_limit',S.limit(e,r,0)==S.pi/S.sqrt(2*S.pi),'finite regular radial origin')
q=S.integrate(h*S.sin(S.pi*(1-t))/S.pi,(t,S.Rational(1,2)-h,S.Rational(1,2)+h))
v=S.integrate(h*S.cos(S.pi*(1-t)),(t,S.Rational(1,2)-h,S.Rational(1,2)+h))
check('pulse_position',S.simplify(q-2*h*S.sin(S.pi*h)/S.pi**2)==0,q)
check('pulse_velocity',S.simplify(v)==0,v)
gap=2*h*h-S.pi*q+q*q/2
series=S.series(gap,h,0,8)
check('pulse_gap_leading_coefficient',S.simplify(S.limit(gap/h**4,h,0)-(S.pi**2/3+2/S.pi**2))==0,series)
check('pulse_growth_ratio_zero',S.limit(gap/(2*h**3),h,0)==0,S.series(gap/(2*h**3),h,0,5))
b=S.pi*eps/(2*a)
trialq=S.integrate(a*S.sin(S.pi*(1-t))/S.pi,(t,S.Rational(1,2)-b,S.Rational(1,2)+b))
trialgap=S.pi*eps-(S.pi+eps)*trialq+trialq**2/2
check('perturbed_trial_negative_leading',S.limit(trialgap/eps**2,eps,0)==-S.Rational(1,2),S.series(trialgap,eps,0,5))
qb=A/S.pi+R*A**5
identity=A-S.pi*qb+qb**2/2-(A*A/(2*S.pi**2)-S.pi*R*A**5+R*A**6/S.pi+R*R*A**10/2)
check('weaker_growth_square_identity',S.expand(identity)==0,'exact polynomial identity in A,R,pi')
envelope=S.integrate((k-2*t*t)**2,(t,-S.sqrt(k/2),S.sqrt(k/2)))
check('dual_envelope_L2_squared',S.simplify(envelope-8*S.sqrt(2)*k**S.Rational(5,2)/15)==0,envelope)
check('reported_dual_constant_safe',S.simplify(envelope/(S.sqrt(2)*k**S.Rational(5,2)))==S.Rational(8,15),'exact envelope squared norm is 8/15 of the reported squared upper bound')
# Exact continuum integrals of all 3^8 profiles on eight equal cells, not samples at cell centers.
N=8;tested=0;minimum=None
for values in product((Q(0),Q(1,2),Q(1)),repeat=N):
    mass=sum(values,Q(0))/N
    moment=sum((val*((Q(i+1,N)-Q(1,2))**3-(Q(i,N)-Q(1,2))**3)/3 for i,val in enumerate(values)),Q(0))
    slack=moment-mass**3/12
    assert slack>=0
    minimum=slack if minimum is None else min(minimum,slack)
    tested+=1
check('bathtub_continuum_profiles',tested==6561 and minimum==0,f'{tested} rational profiles; minimum slack={minimum}; includes zero/full cap and centered saturation')
# All-dimension exponent identities needed by the functional argument.
check('critical_interpolation_exponents',Q(4,12)+Q(1,6)==Q(1,2) and Q(4,4)==1,'four factors in L^4_t L^12_x, one in L^infty_t L^6_x -> L^1_t L^2_x')
check('BSS_exponents',Q(1,4)+Q(3,12)==Q(3,2)-1 and Q(3,4)+Q(2,12)<=1,'dimension3,p4,q12,gamma1 satisfy both BSS Theorem1.1 inequalities')
result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','checks':checks,'checks_count':len(checks),'bathtub_profiles':tested,'before_submitted_helper_reading':True,'limits':'Exact scalar/symbolic/finite controls support the written functional-analytic proof. They do not simulate or certify the nonlinear PDE, prove general compactness, assign numerical PDE constants, or certify novelty.','source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
(out/'fresh-controls.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False,indent=2))
