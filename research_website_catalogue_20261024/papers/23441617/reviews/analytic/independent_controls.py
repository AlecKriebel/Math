from pathlib import Path
from fractions import Fraction
import sympy as s
import json,time
start=time.time(); results={}; checks=0
h=s.symbols('h',positive=True);r=s.symbols('r',positive=True);t=s.symbols('t',positive=True);eps=s.symbols('eps',positive=True)
# Exact analytic controls, not a numerical approximation of all-curve modulus.
vertical=s.integrate(1/s.sqrt(4-h*h),(h,0,1))
if s.simplify(vertical-s.pi/6)!=0:raise AssertionError('interval vertical-family lower bound')
results['interval_modulus_bounds']={'E_to_S2_lower':'pi/6 via vertical connectors','E_to_S2_upper':'3*pi via density1 on1<|z|<2','vertical_integral':str(vertical),'E_to_real_complement':'infinite: admissibility on upper semicircles gives energy>=integral_0^1 dr/(pi*r)'};checks+=1
# Indicator differences have D(h)=2min(h,1) for positive h.
truncated=2*s.integrate(2/h,(h,eps,1))+2*s.integrate(2/h**2,(h,1,s.oo))
if s.simplify(truncated-(4*s.log(1/eps)+4))!=0:raise AssertionError('critical log divergence')
subcritical=2*s.integrate(2*h/h**s.Rational(3,2),(h,0,1))+2*s.integrate(2/h**s.Rational(3,2),(h,1,s.oo))
if subcritical!=16:raise AssertionError('subcritical comparison')
results['trace_exponent_controls']={'critical_truncated_seminorm':str(truncated),'s_one_quarter_seminorm':str(subcritical),'meaning':'Positive-length characteristic functions fail exactly at the critical/stronger fractional exponent; a subcritical trace alone would not prove the theorem.'};checks+=2
# Exact threshold tests for the actual dyadic majorant, including equality.
for m in range(18):
 for value in [Fraction(2)**m,Fraction(3,2)*Fraction(2)**m,Fraction(2)**(m+1)]:
  total=sum((Fraction(2)**(k+1) for k in range(m+2) if value>Fraction(2)**k),Fraction(0))
  if not (1+total>=value and total<=4*value):raise AssertionError(('dyadic',m,str(value)))
  checks+=1
excess=s.summation(2**(-s.Symbol('k',integer=True,nonnegative=True)-3),(s.Symbol('k',integer=True,nonnegative=True),0,s.oo))
if excess!=s.Rational(1,4):raise AssertionError('outer regularity excess')
results['majorant_control']={'dyadic_threshold_cases':54,'exact_excess_sum':str(excess),'rectangle_area':20};checks+=1
# Point singularity: substitute v=log(1/r) to avoid quadrature at the pole.
v=s.symbols('v',positive=True)
point_energy=2*s.pi*s.integrate(1/v**2,(v,1,s.oo))
point_escape=s.integrate(1/v,(v,1,s.oo))
if point_energy!=2*s.pi or point_escape!=s.oo:raise AssertionError('singleton radial control')
results['singleton_log_density']={'rho':'1/(r*log(1/r)) on0<r<exp(-1), zero elsewhere, infinity at center','squared_area_integral':str(point_energy),'escaping_path_radial_lower_integral':str(point_escape),'meaning':'Modulus from a singleton is zero after scaling; infinity at the endpoint alone would not achieve this.'};checks+=2
# Integrable circle energy need not have r*A(r)->0 along ALL radii.
# A(r)=1/r on I_j=[2^-j,2^-j(1+2^-j)], zero elsewhere.
for j in range(1,129):
 lo=Fraction(1,2**j);hi=lo*(1+lo);gap=Fraction(3,4)*lo
 if not (hi<2*lo and Fraction(1,2**(j+1))*(1+Fraction(1,2**(j+1)))<gap<lo):raise AssertionError(('annulus gap',j))
 checks+=1
results['circle_selection_negative_control']={'spike_annuli':'I_j=[2^-j,2^-j(1+2^-j)]','A_on_spikes':'1/r','integral_bound':'sum_j log(1+2^-j) <= sum_j2^-j =1','rA_spike_value':1,'good_gap_radii':'(3/4)*2^-j','rA_good_value':0,'finite_annulus_checks':128,'meaning':'Only a liminf-zero subsequence is justified; replacing it with a full limit is false.'}
# A locally rectifiable spiral can have infinite endpoint length. q>=1 excludes finite q-cost.
speed_squared=s.simplify(s.diff(t*s.cos(1/t),t)**2+s.diff(t*s.sin(1/t),t)**2)
if s.simplify(speed_squared-(1+t**-2))!=0:raise AssertionError('endpoint spiral')
results['infinite_endpoint_length_control']={'curve':'t*exp(i/t),t>0;endpoint0','speed_squared':str(speed_squared),'length_lower_bound':'integral_0^delta dt/t = infinity','meaning':'q>=1 near the endpoint prevents a finite-cost counterexample based on infinite oscillation.'};checks+=1
results['zero_energy_spike_negative_control']={'rho':'infinity on real axis,zero elsewhere','area_energy':0,'upper_semicircle_cost':0,'admissible_for_interval_to_real_complement':False,'meaning':'Endpoint infinity has zero arclength mass; area-equivalent representatives cannot be interchanged for all-curve admissibility.'}
results['checks']=checks;results['elapsed_seconds']=time.time()-start;results['status']='Exact controls passed; universal assertions are established separately by the analytic derivation.'
Path(__file__).with_name('INDEPENDENT_CONTROL_RESULTS.json').write_text(json.dumps(results,indent=2)+'\n');print(json.dumps({'checks':checks,'elapsed_seconds':results['elapsed_seconds'],'status':results['status']}))
