#!/usr/bin/env python3
"""Exact supplemental checks for the authored pass-3 constitutive proofs."""
import json
from pathlib import Path
import sympy as s

checks = {}
a,b,c,d,t,h,j,J,u,v = s.symbols('a b c d t h j J u v', positive=True)

def zero(name, expression):
    checks[name] = bool(s.simplify(expression) == 0)

def norm2(M):
    return sum(z*z for z in M)

def density(M):
    K=M.cofactor_matrix()
    return a*norm2(M)**3+b*norm2(K)**s.Rational(3,2)+c*M.det()**2+d*M.det()**-2

zero('barrier_bregman_identity', J**-2-j**-2+2*j**-3*(J-j)-(J-j)**2*(2*J+j)/(j**3*J**2))
zero('barrier_bregman_reciprocal_remainder', (J-j)**2*(2*J+j)/(j**3*J**2)-(1/J-1/j)**2-2*(J-j)**2/(j**3*J))
zero('barrier_midpoint_identity', u**-2+v**-2-8/(u+v)**2-(u-v)**2*(u*u+4*u*v+v*v)/(u*u*v*v*(u+v)**2))
zero('barrier_midpoint_positive_remainder', u**-2+v**-2-8/(u+v)**2-(1/u-1/v)**2-2*(u-v)**2/(u*v*(u+v)**2))
zero('quadratic_midpoint_constant', u*u+v*v-2*((u+v)/2)**2-(u-v)**2/2)

f=s.symbols('f0:9')
F=s.Matrix(3,3,f)
r=s.symbols('r0:3')
for row in range(3):
    R=s.zeros(3,3)
    for k in range(3):
        R[row,k]=r[k]
    M=F+h*R
    zero(f'row_{row}_det_affine', s.diff(M.det(),h,2))
    checks[f'row_{row}_cofactor_affine']=all(s.simplify(s.diff(x,h,2))==0 for x in M.cofactor_matrix())

E12=s.zeros(3,3); E12[0,1]=1
E33=s.zeros(3,3); E33[2,2]=1
shear=s.diff(density(t*s.eye(3)+h*E12),h,2).subs(h,0)
longitudinal=s.diff(density(t*s.eye(3)+h*E33),h,2).subs(h,0)
zero('conformal_shear_stiffness',shear-(54*a+3*s.sqrt(3)*b)*t**4)
zero('conformal_longitudinal_stiffness',longitudinal-((126*a+10*s.sqrt(3)*b+2*c)*t**4+6*d*t**-8))
zero('exact_lh_condition_ratio',longitudinal/shear-((126*a+10*s.sqrt(3)*b+2*c)/(54*a+3*s.sqrt(3)*b)+6*d/(54*a+3*s.sqrt(3)*b)*t**-12))

x=s.symbols('x0:3', positive=True)
S=sum(x); T=x[0]*x[1]+x[0]*x[2]+x[1]*x[2]
U=[6*a*S*S*xi+3*b*s.sqrt(T)*xi*(S-xi)+2*c*s.prod(x) for xi in x]
for i,jj,kk in [(0,1,2),(0,2,1),(1,2,0)]:
    zero(f'principal_difference_{i}_{jj}', U[i]-U[jj]-(x[i]-x[jj])*(6*a*S*S+3*b*s.sqrt(T)*x[kk]))
zero('stress_trace_six_H',sum(U)-6*(a*S**3+b*T**s.Rational(3,2)+c*s.prod(x)))
A0=27*a+3*s.sqrt(3)*b+c
zero('conformal_U_equals_two_H',U[0].subs({xi:t*t for xi in x})-2*A0*t**6)

uu=s.symbols('u0:3', real=True)
zero('deviator_pairwise_identity',sum((uu[i]-uu[jj])**2 for i in range(3) for jj in range(i+1,3))-3*sum((xi-sum(uu)/3)**2 for xi in uu))
zero('single_row_cutoff_determinant',s.diag(1,1,t/2-t).det()+t/2)

# Exact generic rank-one formula at the conformal point, before |u||v|=1.
z,n=s.symbols('z n', real=True)
# n=|u|^2 |v|^2; L=t(z I-v tensor u), so |L|^2=t^2(n+z^2).
formula=54*a*t**4*n+72*a*t**4*z*z+3*s.sqrt(3)*b*t**4*(n+z*z)+4*s.sqrt(3)*b*t**4*z*z+2*c*t**4*z*z+6*d*t**-8*z*z
zero('general_conformal_rankone_formula',formula-((54*a+3*s.sqrt(3)*b)*t**4*n+((72*a+7*s.sqrt(3)*b+2*c)*t**4+6*d*t**-8)*z*z))

out={'checks':checks, 'all_symbolic_checks_passed':all(checks.values()), 'symbolic_check_count':len(checks), 'unconditional_higher_integrability_proved':False, 'benchmark_resolved':False}
path=Path(__file__).with_name('CONSTITUTIVE_CHECKS.json')
path.write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
if not out['all_symbolic_checks_passed']:
    raise SystemExit(1)
