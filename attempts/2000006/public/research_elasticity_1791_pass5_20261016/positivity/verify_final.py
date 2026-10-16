#!/usr/bin/env python3
"""Supplemental exact checks, not substitutes for the Sobolev comparison proofs."""
import json
from pathlib import Path
import sympy as s

checks={}
def zero(name,x):
    checks[name]=bool(s.simplify(s.expand(x))==0)
def inner(A,B):
    return sum(x*y for x,y in zip(A,B))
t=s.symbols('t',real=True)
f=s.symbols('f0:9'); aa=s.symbols('a0:9')
F=s.Matrix(3,3,f); A=s.Matrix(3,3,aa)
J=F.det(); j=A.det(); M1=inner(F.cofactor_matrix(),A); M2=inner(A.cofactor_matrix(),F)
path=((1-t)*F+t*A).det()
bern=(1-t)**3*J+t*(1-t)**2*M1+t**2*(1-t)*M2+t**3*j
zero('general_cubic_bernstein_expansion',path-bern)
zero('determinant_initial_derivative',s.diff(path,t).subs(t,0)-(M1-3*J))
zero('determinant_final_derivative',s.diff(path,t).subs(t,1)-(3*j-M2))
zero('mixed_coefficients_reversal',((1-t)*A+t*F).det()-bern.subs(t,1-t))

JJ,m1,m2,jj=s.symbols('J m1 m2 j',positive=True)
poly=(1-t)**3*JJ+t*(1-t)**2*m1+t**2*(1-t)*m2+t**3*jj
zero('barrier_initial_derivative',s.diff(poly**-2,t).subs(t,0)-(6/JJ**2-2*m1/JJ**3))
sec=((1-t)**-6-1)/t
zero('uniform_secant_bound_at_half',sec.subs(t,s.Rational(1,2))-126)
zero('initial_barrier_source_coefficient',s.limit(sec,t,0)-6)
# Convexity establishes increasing secant slopes on (0,1); both derivatives are positive.
zero('inverse_six_first_derivative',s.diff((1-t)**-6,t)-6*(1-t)**-7)
zero('inverse_six_second_derivative',s.diff((1-t)**-6,t,2)-42*(1-t)**-8)

u=s.Matrix(s.symbols('u0:3')); v=s.Matrix(s.symbols('v0:3'))
Ar=F+u*v.T; jr=Ar.det()
zero('rank_one_first_mixed_identity',inner(F.cofactor_matrix(),Ar)-(2*J+jr))
zero('rank_one_second_mixed_identity',inner(Ar.cofactor_matrix(),F)-(J+2*jr))
zero('rank_one_barrier_source_recovery',(6/JJ**2-2*(2*JJ+jj)/JJ**3)-(2/JJ**2-2*jj/JJ**3))
zero('unchanged_endpoint_mixed_identity',inner(F.cofactor_matrix(),F)-3*J)
zero('unchanged_region_barrier_cancellation',2*(3*JJ)/JJ**3-6/JJ**2)

ss,q=s.symbols('scale q',positive=True)
Fr=s.diag(ss,ss,ss*q)
zero('radial_first_mixed_minor',s.trace(Fr.cofactor_matrix())-ss**2*(1+2*q))
zero('radial_second_mixed_minor',s.trace(Fr)-ss*(2+q))
zero('radial_mixed_moment',s.trace(Fr.cofactor_matrix())/Fr.det()**3-ss**-7*(1+2*q)/q**3)
r,k=s.symbols('r k',positive=True); L=s.log(s.E/r); scale=r**s.Rational(1,2)*L**k
zero('radial_moment_integral_density',r**2*scale**-7-r**s.Rational(-3,2)*L**(-7*k))
C=s.diag(-2,-s.Rational(1,2),1)
zero('compatible_obstruction_positive_endpoint_determinant',C.det()-1)
zero('compatible_obstruction_first_mixed_negative',s.trace(C.cofactor_matrix())+s.Rational(3,2))
zero('compatible_obstruction_second_mixed_negative',s.trace(C)+s.Rational(3,2))

# Coefficients in the elementary positive-density derivative bound.
a,b,c=s.symbols('a b c',positive=True)
zero('cofactor_term_derivative_bound_coefficient',3*b*2/3-2*b)
zero('determinant_square_derivative_bound_coefficient',2*c/(3*s.sqrt(3)*s.sqrt(3))-2*c/9)
zero('young_bound_original_gradient_coefficient',1+s.Rational(5,6)-s.Rational(11,6))

alpha,T=s.symbols('alpha T',positive=True)
zero('log_modulus_integral_primitive',s.diff(T**(1-alpha)/(1-alpha),T)-T**(-alpha))
zero('log_modulus_product_exponent',(1-alpha)-2*alpha-(1-3*alpha))
zero('critical_log_modulus_exponent',(1-3*alpha).subs(alpha,s.Rational(1,3)))
zero('unit_log_modulus_integral_primitive',s.diff(s.log(T),T)-1/T)

out={'checks':checks,'all_symbolic_checks_passed':all(checks.values()),'symbolic_check_count':len(checks),'coupled_endpoint_existence_proved_for_arbitrary_minimizer':False,'unconditional_gradient_modulus_proved':False,'benchmark_resolved':False}
Path(__file__).with_name('FINAL_CHECKS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
if not out['all_symbolic_checks_passed']:raise SystemExit(1)
