#!/usr/bin/env python3
"""Adversarial second reconstruction of the PDE reviewer's m=3 path.
Uses the algebra audit's independently differentiated reactions. No project or
PDE-reviewer imports. Explicit exceptions survive optimized Python.
"""
import json
from pathlib import Path
import sympy as s
from independent_algebra_check import model,check,COUNTS
R=s.Rational
e,lam,t,v,z=s.symbols('e lam t v z',real=True)
G,Y,x,f,A=model(3)
Hess=[s.hessian(fi,x) for fi in f]
def B(u,w):return s.Matrix([(u.T*T*w)[0] for T in Hess])
r=s.Matrix([1,-1-R(16,9)*e-e**2/2,-e,R(1,2)-R(13,18)*e])
d=[s.factor(vv/r[i]) for i,vv in enumerate(A*r)]
D=s.diag(*d);M=A-D;c=s.Matrix([0,4,2,1]);F=-B(r,r)/4
check(s.simplify(M*r)==s.zeros(4,1),'critical_right_vector')
ell=M.T.nullspace()[0];ell=ell/ell[-1]
check(s.simplify(ell.T*M)==s.zeros(1,4),'critical_left_vector')
w0=A.col_join(c.T).gauss_jordan_solve(F.col_join(s.zeros(1,1)))[0]
w2=(A-4*D).inv()*F
check(s.simplify(A*w0-F)==s.zeros(4,1),'zero_mode_equation')
check(s.simplify(c.T*w0)==s.zeros(1,1),'zero_mode_mass_gauge')
check(s.simplify((A-4*D)*w2-F)==s.zeros(4,1),'second_harmonic_equation')
cubic=s.factor((ell.T*(B(r,w0)+B(r,w2)/2))[0]/(ell.T*r)[0])
check(s.limit(cubic,e,0)==R(6,1379),'printed_cubic_constant')
check(s.limit((cubic-R(6,1379))/e,e,0)==R(421985,11409846),'printed_cubic_linear_term')
# Direct determinant, independent of the reviewer's boundary-polynomial entry.
char=s.Poly((lam*s.eye(4)-A+t*D).det(method='domain-ge'),lam)
g1=lam+2+t*d[0];g2=lam+1+t*d[1];gm=lam+5+t*d[2];gz=lam+4+t*d[3]
reduced=g2*(g1*gm*gz-4*g1-4*gm+gz)-(gz*(4*g1+gm)-36)
check(s.factor(char.as_expr()-reduced)==0,'direct_determinant_boundary_identity')
a1,a2,a3,a4=char.all_coeffs()[1:]
H2=s.factor(a1*a2-a3);H3=s.factor(a3*H2-a1*a1*a4)
certs={}
def positive_on_interval(expr,label,spatial=False):
 expr=s.factor(expr.subs({e:1/(1000*(1+z)),t:1+v}))
 num,den=s.fraction(expr);gens=(v,z) if spatial else (z,)
 pn,pd=s.Poly(num,*gens),s.Poly(den,*gens)
 if pd.coeff_monomial(1)<0:pn=-pn;pd=-pd
 check(all(co>0 for co in pn.coeffs()) and all(co>0 for co in pd.coeffs()),'positive_coefficients_'+label)
 check(pn.coeff_monomial(1)>0 and pd.coeff_monomial(1)>0,'positive_constant_'+label)
 certs[label]={'numerator_terms':len(pn.terms()),'denominator_terms':len(pd.terms())}
for i,di in enumerate(d):positive_on_interval(di,f'D{i+1}')
positive_on_interval(cubic,'cubic')
positive_on_interval(-(ell.T*r)[0],'negative_left_right_pairing')
for name,expr in [('a1',a1),('a2',a2),('a3',a3),('a4_over_t_minus_1',s.cancel(a4/(t-1))),('H2',H2),('H3',H3)]:
 positive_on_interval(expr,name,True)
eta=s.factor((ell.T*D*r)[0]/(ell.T*r)[0]);positive_on_interval(eta,'transversality')
check(s.factor(eta-(s.diff(a4,t).subs(t,1)/a3.subs(t,1)))==0,'transversality_characteristic_identity')
out={'status':'PASS','checks':COUNTS,'diffusion':[str(i) for i in d],'cubic':str(cubic),'eta':str(eta),'certificates':certs,'domain':'0<epsilon<=1/1000; t>=1','claim_scope':'m=3 only; exact symbolic interval certificates, not finite numerical sampling'}
Path('near_threshold_crosscheck_results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
