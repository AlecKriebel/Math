#!/usr/bin/env python3
"""Independent controls, written before reading any submitted checker.
Finite algebra/integration tests do not validate an unknown PDE constant or solve the PDE.
"""
from pathlib import Path
from collections import Counter
from fractions import Fraction as F
from itertools import product
from datetime import datetime,timezone
import json,hashlib,sys
import sympy as s
import mpmath as mp
HERE=Path(__file__).resolve().parent
counts=Counter(); data={}; started=datetime.now(timezone.utc).isoformat()
def check(name,statement):
 if not bool(statement): raise AssertionError(name)
 counts[name]+=1
# Exhaust all step densities in {0,1/2,1} on eight time cells.
# Integrate the moment exactly on each cell, instead of evaluating midpoints.
N=8
moments=[]
for i in range(N):
 l=F(i,N)-F(1,2);r=F(i+1,N)-F(1,2)
 moments.append((r**3-l**3)/3)
for entries in product([F(0),F(1,2),F(1)],repeat=N):
 A=sum(entries)/N; r2=sum(x*x for x in entries)/N
 I=sum(x*m for x,m in zip(entries,moments))
 check('exact_step_mass_moment',I>=A**3/12)
 check('exact_step_norm_relations',A*A<=r2<=A and 0<=A<=1)
# Exact density saturation shows the moment bound has the right normalization,
# including empty and full mass, and arbitrary positive rational caps.
for rho in [F(1,10),F(1),F(7,3)]:
 for k in range(17):
  A=rho*F(k,16);b=A/(2*rho)
  I=2*rho*b**3/3
  check('exact_bathtub_equality',I==A**3/(12*rho*rho))
# Symbolic integrals for arbitrary eigenmode pulses with center c and halfwidth b.
a,b,c,t,h,eps,p,R,A=s.symbols('a b c t h eps p R A',positive=True,real=True)
x=s.integrate(a*s.sin(s.pi*t)/s.pi,(t,c-b,c+b))
vel=s.integrate(-a*s.cos(s.pi*t),(t,c-b,c+b))
check('linear_endpoint_general_center',s.trigsimp(x-2*a*s.sin(s.pi*b)*s.sin(s.pi*c)/s.pi**2)==0)
check('linear_velocity_general_center',s.trigsimp(vel+2*a*s.sin(s.pi*b)*s.cos(s.pi*c)/s.pi)==0)
xh=s.simplify(x.subs({a:h,b:h,c:s.Rational(1,2)}))
check('centered_velocity_exact_zero',s.simplify(vel.subs(c,s.Rational(1,2)))==0)
gap=2*h**2-s.pi*xh+xh*xh/2
ser=s.series(gap,h,0,8).removeO().expand()
check('pulse_leading_coefficient',s.simplify(ser.coeff(h,4)-(s.pi**2/3+2/s.pi**2))==0)
check('pulse_next_coefficient',s.simplify(ser.coeff(h,6)-(-s.pi**4/60-s.Rational(2,3)))==0)
check('pulse_no_lower_orders',all(ser.coeff(h,j)==0 for j in range(4)))
ndc=(2*h**2-s.pi*xh)/(2*h**3)+xh*xh/(4*h**3)
check('NDC_expression_equals_linear_gap_ratio',s.simplify(ndc-gap/(2*h**3))==0)
check('NDC_leading_coefficient',s.simplify(s.series(ndc,h,0,4).removeO().coeff(h,1)-(s.pi**2/6+1/s.pi**2))==0)
# Retain fixed cap amplitude a while narrowing support in the target perturbation.
xe=s.simplify(x.subs({b:s.pi*eps/(2*a),c:s.Rational(1,2)}))
pert=s.pi*eps-(s.pi+eps)*xe+xe*xe/2
per=s.series(pert,eps,0,5).removeO().expand()
check('perturbed_trial_negative_quadratic',s.simplify(per.coeff(eps,2)+s.Rational(1,2))==0)
check('perturbed_trial_cubic_coefficient',s.simplify(per.coeff(eps,3)-s.pi**5/(24*a*a))==0)
# Directly integrate the exact quadratic majorant of g_epsilon squared.
d,z=s.symbols('d z',positive=True,real=True)
major=s.integrate((d-2*z*z)**2,(z,-s.sqrt(d/2),s.sqrt(d/2)))
check('dual_majorant_exact_integral',s.simplify(major-8*s.sqrt(2)*d**s.Rational(5,2)/15)==0)
check('dual_height_support_bound',s.simplify(major/(s.sqrt(2)*d**s.Rational(5,2)))==s.Rational(8,15))
# Algebraic L1-growth identity with p as a symbolic positive constant.
bound=A/p+R*A**5
q=s.expand(A-p*bound+bound*bound/2)
expected=A*A/(2*p*p)-p*R*A**5+R*A**6/p+R*R*A**10/2
check('L1_growth_polynomial_identity',s.expand(q-expected)==0)
# Critical interpolation: four L12 factors and one L6 factor give spatial L2;
# four time-L4 factors and one time-Linfty factor give time-L1.
check('quintic_spatial_holder',4*F(1,12)+F(1,6)==F(1,2))
check('quintic_temporal_holder',4*F(1,4)==1)
check('interpolation_10_exponent',F(4,5)*F(1,12)+F(1,5)*F(1,6)==F(1,10))
check('BSS_energy_scaling',F(1,4)+3*F(1,12)==F(3,2)-1)
check('BSS_boundary_admissibility',3*F(1,4)+2*F(1,12)<=1)
# Independent exponent-family check: amplitude h^alpha, width h^beta.
family=[]
for alpha,beta in [(F(1),F(1)),(F(1,2),F(1)),(F(3,2),F(1)),(F(1),F(2)),(F(2),F(1)),(F(3),F(1))]:
 exps={'weighted_first_order_ratio':2*beta-alpha,'terminal_square_ratio':beta,'quartic_ratio':2*alpha+3*beta,'quintic_error_ratio':3*alpha+4*beta,'velocity_cost_ratio':8*alpha+9*beta}
 expected_decay=alpha<2*beta
 check('pulse_family_threshold',all(v>0 for v in exps.values())==expected_decay)
 family.append({'alpha':str(alpha),'beta':str(beta),'ratio_exponents':{k:str(v) for k,v in exps.items()},'decay':expected_decay})
# High precision numerical diagnostics for formulas, never called PDE certificates.
mp.mp.dps=80
numeric=[]
for j in range(2,10):
 hh=mp.mpf(2)**(-j);xx=2*hh*mp.sin(mp.pi*hh)/mp.pi**2
 gg=2*hh**2-mp.pi*xx+xx**2/2
 target=mp.pi**2/3+2/mp.pi**2
 check('high_precision_positive_pulse_gap',gg>0)
 check('high_precision_pulse_asymptotic',abs(gg/hh**4-target)<12*hh**2)
 # A pulse shifted to quarter time loses the critical cancellation.
 shifted=2*hh**2-mp.pi*(xx/mp.sqrt(2))+(xx/mp.sqrt(2))**2/2
 check('negative_shifted_pulse_restores_first_order',shifted/(2*hh**3)>mp.mpf('0.29')/hh)
 # Quadratic control regularization adds beta2/2 to normalized gap, exactly.
 check('negative_beta2_restores_growth',gg/(2*hh**3)+mp.mpf('0.5')>=mp.mpf('0.5'))
 numeric.append({'h':str(hh),'linear_gap_over_h4':mp.nstr(gg/hh**4,25),'linear_gap_over_L2sq':mp.nstr(gg/(2*hh**3),25)})
# Actual g_epsilon formula on a dense bounded mesh, with independently integrated norm.
for ee in [mp.mpf(10)**(-j) for j in range(1,7)]:
 width=mp.acos(1/(1+ee/mp.pi))/mp.pi
 g=lambda zz:max(mp.mpf('0'),(1+ee/mp.pi)*mp.cos(mp.pi*zz)-1)
 norm=mp.sqrt(mp.quad(lambda zz:g(zz)**2,[-width,0,width]))
 check('high_precision_actual_dual_L2_bound',norm<=2**mp.mpf('.25')*mp.pi**mp.mpf('-1.25')*ee**mp.mpf('1.25'))
 for k in range(65):
  zz=mp.mpf(k)/128
  check('high_precision_pointwise_dual_bound',g(zz)<=max(mp.mpf(0),ee/mp.pi-2*zz*zz)+mp.mpf('1e-75'))
# Geometric normalization of the radial mode (angular factor included).
r=s.symbols('r',positive=True)
check('unit_ball_mode_L2_normalization',s.integrate(4*s.pi*s.sin(s.pi*r)**2/(2*s.pi),(r,0,1))==1)
e=s.sin(s.pi*r)/(s.sqrt(2*s.pi)*r)
check('radial_eigen_equation',s.simplify(-s.diff(e,r,2)-2*s.diff(e,r)/r-s.pi**2*e)==0)
check('radial_regular_origin',s.limit(e,r,0)==s.pi/s.sqrt(2*s.pi))
check('radial_Dirichlet_boundary',s.simplify(e.subs(r,1))==0)
data.update({'started_utc':started,'finished_utc':datetime.now(timezone.utc).isoformat(),'assertions':sum(counts.values()),'counts':dict(counts),'pulse_series':str(ser),'perturbed_trial_series':str(per),'dual_majorant_integral':str(s.simplify(major)),'pulse_families':family,'high_precision_diagnostics':numeric,'python':sys.version,'sympy':s.__version__,'mpmath':mp.__version__,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'scope':'Exact rational/algebraic controls plus separately identified 80-digit numerical diagnostics. These do not approximate a nonlinear wave solution, establish unknown PDE constants, or prove compactness/universal quantifiers.'})
(HERE/'fresh-control-results.json').write_text(json.dumps(data,indent=2)+'\n')
print(json.dumps(data,indent=2))
