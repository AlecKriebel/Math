#!/usr/bin/env python3
"""Independent exact finite controls; no submitted program is imported or run.

These checks supplement the analytic proof. Infinite-dimensional completeness,
Fredholm continuation and strong-adjoint compact multiplication are documented
in INDEPENDENT_DERIVATION.md, not certified by finite checks.
"""
from fractions import Fraction as F
from math import factorial
from pathlib import Path
import json, datetime

checks=[]
def check(name,condition,evidence):
    assert condition,name
    checks.append({'name':name,'pass':True,'evidence':evidence})
def val(x): return str(x)
# Gaussian rational coefficients: (real, imaginary).
def add(a,b):return(a[0]+b[0],a[1]+b[1])
def mul(a,b):return(a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def scale(a,b):return(a[0]*b,a[1]*b)
def ipower(n):return [(F(1),F(0)),(F(0),F(1)),(F(-1),F(0)),(F(0),F(-1))][n%4]
def e_coeff(n):return scale(ipower(n),F(1,factorial(n))) if n>=0 else(F(0),F(0))
for n in range(0,65):
    fc=add(add(e_coeff(n),mul((F(0),F(-1)),e_coeff(n-1))),scale(e_coeff(n-2),-1))
    gc=add(add(scale(e_coeff(n-2),1),mul((F(0),F(3)),e_coeff(n-1))),scale(e_coeff(n),-3))
    if n==0:
        fc=add(fc,(F(-1),F(0)));gc=add(gc,(F(3),F(0)))
    wantf=scale(ipower(n),F((n-1)**2,factorial(n))) if n>=2 else(F(0),F(0))
    wantg=scale(ipower(n),-F((n-1)*(n-3),factorial(n))) if n>=2 else(F(0),F(0))
    check(f'taylor_formula_n{n}',fc==wantf and gc==wantg,{'f':[val(x) for x in fc],'g':[val(x) for x in gc]})
for n in range(4,65):
    check(f'numerator_majorant_n{n}',(n-1)**2<=n*n and abs((n-1)*(n-3))<=n*n,{'upper_numerator':n*n})
check('fifth_ratio_geometric_tail_e',sum((F(1,factorial(k)) for k in range(4)),F(0))+F(1,24)/(1-F(1,5))==F(87,32),{'upper_e':'87/32','reason':'(4+k)! >= 24*5^k'})
check('scalar_remainder_tail_less_than_one',2*F(87,32)-F(9,2)==F(15,16)<1,{'upper_sum_n2_over_factorial_n_ge4':'15/16'})
check('Frobenius_numerator_C2',2**2+1**2+1**2==6,{'eigenvalues_I_plus_eeT':[2,1,1]})
check('C2_HS_constant',F(6,64)*F(32,3)==1,{'pi_squared_cancelled':True,'HS_squared_upper':1})
check('remainder_HS_constant',F(3,4)*2*F(4,3)==2,{'pi_cancelled':True,'HS_upper_coefficient':2})
check('J_over_6pi_norm',F(4,3)/6==F(2,9),{'operator_norm':'2/9'})
check('Ck_operator_norm_at_half',1+F(2,9)*F(1,2)+2*F(1,2)**2==F(29,18)<2,{'coefficient_upper':'29/18'})
for l in range(1,501):
    s=F(l,2*l+1)-F(1,3)
    check(f'ball_shift_degree_{l}',s==F(l-1,3*(2*l+1)) and (s==0 if l==1 else s>=F(1,15)),{'S0_eigenvalue':val(s),'multiplicity':2*l+1})
for l in range(2,500):
    diff=F(l+1,2*l+3)-F(l,2*l+1)
    check(f'ball_gap_monotonic_{l}',diff==F(1,(2*l+3)*(2*l+1))>0,{'difference':val(diff)})
check('contour_gap_and_static_resolvent',F(1,15)-F(1,30)==F(1,30),{'radius':'1/30','resolvent_bound':30})
check('perturbed_resolvent_bound',F(30)/(1-F(30,60))==60,{'epsilon_upper':'1/60','bound':60})
check('Riesz_projection_constant',F(1,30)*60*30==60 and 60*2==120,{'epsilon_factor':60,'kappa_squared_factor':120})
check('graph_constant',120/(1-F(1,2))==240,{'factor':240})
check('graph_H_error_constant',2+2*240==482,{'factor':482})
check('trace_error_constant',3*482==1446,{'factor':1446})
k=F(1,10000);eps=2*k*k;eta=120*k*k
check('explicit_frequency_kernel_range',k<=F(1,2),{'kappa':val(k)})
check('explicit_frequency_resolvent',eps<=F(1,60),{'epsilon_upper':val(eps)})
check('explicit_frequency_graph',eta<=F(1,2),{'eta_upper':val(eta),'graph_upper':val(240*k*k)})
margin=F(2,3)-1446*k
check('explicit_frequency_trace_margin',margin==F(7831,15000)>0,{'negative_trace_coefficient':val(-margin),'trace_upper':val(-margin*k**3)})
check('strict_trace_frequency_threshold',F(2,3)/1446==F(1,2169) and k<F(1,2169),{'sufficient_positive_real_frequency':'0 < kappa < 1/2169'})
# Additional independent quadratic compression check (not needed for trace proof).
newton_double_without_pi_squared=8*(F(1,3)-F(1,15))
check('ball_Newton_double_integral',newton_double_without_pi_squared==F(32,15),{'integral_over_pi_squared':val(newton_double_without_pi_squared)})
quad=-F(1,8)*F(3,4)*F(4,3)*newton_double_without_pi_squared
check('constant_vector_quadratic_compression',quad==F(-4,15),{'PC2_on_constants':'-4I/15'})
for j in range(1,101):
    removed=sum((F(1,2)**(3*j+3*kidx+12) for kidx in range(1,501)),F(0))
    upper=F(1,2)**(3*j+12)/7
    check(f'removal_volume_ratio_j{j}',removed<upper<1,{'upper_ratio_to_ball_volume':val(upper),'finite_500_term_partial_sum_less_than_geometric_total':True})
result={'created_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat().replace('+00:00','Z'),'arithmetic':'exact fractions and integer Gaussian-rational coefficients only','ordinary_floating_eigenvalue_diagnostics':'none','count':len(checks),'all_passed':all(c['pass'] for c in checks),'checks':checks}
path=Path(__file__).parent/'private/exact_controls_output.json'
path.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'output':str(path),'count':len(checks),'all_passed':result['all_passed'],'negative_trace_coefficient':val(-margin),'no_floating_eigenvalues':True}))
