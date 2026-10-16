#!/usr/bin/env python3
"""Supplemental exact checks for pass-4 one-sided repair estimates."""
import json
from pathlib import Path
import sympy as s

checks={}
t,r,J,eps,d=s.symbols('t r J eps d',positive=True)
def zero(name,x):
    checks[name]=bool(s.simplify(x)==0)

q=((1+t*(r-1))**-2-1)/t
zero('barrier_secant_closed_form',q+(r-1)*(2+t*(r-1))/(1+t*(r-1))**2)
zero('barrier_secant_monotonic_derivative',s.diff(q,t)-(r-1)**2*(3+t*(r-1))/(1+t*(r-1))**3)
zero('barrier_secant_endpoint_derivative',s.limit(q,t,0)-2+2*r)
cost=((1-t)**-2-1)/t
zero('zero_jacobian_endpoint_cost',cost-(2-t)/(1-t)**2)
zero('sharp_source_coefficient_limit',s.limit(cost,t,0)-2)
zero('cost_above_two_factorization',cost-2-t*(3-2*t)/(1-t)**2)
zero('cost_below_six_factorization',6-cost-(1-2*t)*(4-3*t)/(1-t)**2)

qv,eta,k1,k2=s.symbols('qv eta k1 k2',real=True)
Fv=s.Matrix([[1,0,0],[0,1,0],[k1,k2,1+eta*(qv-1)]])
zero('compatible_endpoint_determinant',Fv.det()-((1-eta)+eta*qv))
zero('compatible_segment_determinant',((1-t)*s.eye(3)+t*Fv).det()-((1-t)+t*Fv.det()))
checks['compatible_gradient_difference_rank_at_most_one']=all(s.simplify(x)==0 for x in (Fv-s.eye(3)).cofactor_matrix())

# The exact determinant part of the barrier-normalized relative-minor excess.
barrier=(eps*r)**-2-eps**-2+2*eps**-3*(eps*r-eps)
zero('normalized_barrier_relative_energy',eps**2*barrier-(r**-2+2*r-3))
zero('normalized_barrier_vanishes_at_unit_det',(eps**2*barrier).subs(r,1))
A=s.diag(1,1,eps); M=s.diag(2,s.Rational(1,2),1)
zero('volume_preserving_comparison_det',M.det()-1)
zero('unweighted_comparison_gap',sum(x*x for x in A*M-A)-s.Rational(5,4))
zero('comparison_determinant_unchanged',(A*M).det()-A.det())

a,b,c=s.symbols('a b c',positive=True)
def norm2(F):return sum(x*x for x in F)
def H(F):return a*norm2(F)**3+b*norm2(F.cofactor_matrix())**s.Rational(3,2)+c*F.det()**2
F=A*M; K=F.cofactor_matrix(); KA=A.cofactor_matrix()
D6=norm2(F)**3-norm2(A)**3-6*norm2(A)**2*sum(x*y for x,y in zip(A,F-A))
D3=norm2(K)**s.Rational(3,2)-norm2(KA)**s.Rational(3,2)-3*s.sqrt(norm2(KA))*sum(x*y for x,y in zip(KA,K-KA))
zero('normalized_gradient_bregman_vanishes',s.limit(eps**2*D6,eps,0))
zero('normalized_cofactor_bregman_vanishes',s.limit(eps**2*D3,eps,0))

# Radial marginal obstruction: source and target logarithms and exact Jacobians.
radius,kappa=s.symbols('radius kappa',positive=True)
L=s.log(s.E/radius)
scale=radius**s.Rational(1,2)*L**kappa
R=radius*scale
qrad=s.Rational(3,2)-kappa/L
zero('radial_radius_derivative',s.diff(R,radius)-scale*qrad)
Jrad=scale**3*qrad
zero('radial_jacobian_formula',Jrad-radius**s.Rational(3,2)*L**(3*kappa)*qrad)
zero('inverse_jacobian_target_formula',1/Jrad-1/(R*L**(2*kappa)*qrad))
zero('critical_barrier_integral_density',radius**2/Jrad**2-1/(radius*L**(6*kappa)*qrad**2))
# Logarithm equality checked by expanding powers on the positive radius interval.
log_target=1-s.Rational(3,2)*s.log(radius)-kappa*s.log(L)
zero('target_logarithm_relation',log_target-(s.Rational(3,2)*L-s.Rational(1,2)-kappa*s.log(L)))

out={'checks':checks,'all_symbolic_checks_passed':all(checks.values()),'symbolic_check_count':len(checks),'uniformly_positive_rankone_repair_constructed_for_arbitrary_minimizer':False,'unconditional_higher_integrability_proved':False,'benchmark_resolved':False}
Path(__file__).with_name('REPAIR_CHECKS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
if not out['all_symbolic_checks_passed']:raise SystemExit(1)
