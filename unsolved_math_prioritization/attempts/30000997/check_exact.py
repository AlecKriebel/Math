#!/usr/bin/env python3
"""Exact algebra replay for the partial MTW note. Requires SymPy.
This checks encoded identities, not geometric hypotheses, cut loci or global A3w.
"""
import sympy as s
import json, pathlib, platform
checks={}
x,a,z=s.symbols('x a z',real=True)
f=s.cos(x)+a*s.cos(x)**3*s.sin(x)**4
N=1+a*(-49*z**3+55*z*z-12*z);D=1+a*(z*z-z**3)
K=-s.diff(f,x,2)/f
checks['curvature_formula']=s.trigsimp(s.expand_trig((K-(N/D).subs(z,s.sin(x)**2))*f*D.subs(z,s.sin(x)**2)))==0
checks['curvature_positive_decomposition']=s.expand(N-((1-6*a)+a*(1-z)*(49*z*z-6*z+6)))==0
checks['curvature_equator']=s.simplify(K.subs(x,0))==1
checks['curvature_second_derivative']=s.simplify(s.diff(K,x,2).subs(x,0))==-24*a
# Scalar Jacobi recurrence, formal in the curvature Taylor coefficients.
t=s.symbols('t');K0,K1,K2=s.symbols('K0 K1 K2');V=K0+K1*t+K2*t*t/2
C=s.Integer(1);J=t
for n in range(6):
 C+=-s.expand(V*C).coeff(t,n)*t**(n+2)/((n+1)*(n+2))
 J+=-s.expand(V*J).coeff(t,n)*t**(n+2)/((n+1)*(n+2))
expected=1-K0*t*t/3-K1*t**3/12-(K2/60+K0*K0/45)*t**4
checks['jacobi_hessian_taylor']=s.series(t*C/J-expected,t,0,5).removeO().expand()==0
# General two-dimensional tensor expansion, without imposing reflection symmetry.
b,y,r=s.symbols('b y r',nonzero=True,real=True)
H,Ha,Hs,Haa,Has,Hss=s.symbols('H Ha Hs Haa Has Hss')
c,q=s.symbols('c q',real=True)
jet=H+Ha*b+Hs*(y-r)+Haa*b*b/2+Has*b*(y-r)+Hss*(y-r)**2/2
v=s.Matrix([b,y]);A=s.eye(2)+(jet-1)*(s.eye(2)-v*v.T/(b*b+y*y))
u=s.Matrix([c,q]);w=s.Matrix([-q,c]);F=(u.T*A*u)[0]
M=-sum(w[i]*w[j]*s.diff(F,[b,y][i],[b,y][j]) for i in range(2) for j in range(2))
M=s.simplify(M.subs({b:0,y:r}))
P=-Hss;Q=2*(1-H)/r**2;R=-Haa-4*Hs/r+6*(H-1)/r**2
expected=P*c**4+2*Has*c**3*q+R*c*c*q*q+4*Ha/r*c*q**3+Q*q**4
checks['general_null_quartic']=s.simplify(M-expected)==0
checks['equatorial_finite_witness']=s.Rational(2)*s.Rational(1,2)-s.Rational(12,5)*s.Rational(1,8)-8/s.pi**2==s.Rational(7,10)-8/s.pi**2
checks['negative_witness_rational_bound']=s.Rational(7,10)-8/s.Rational(22,7)**2<0
checks['positive_mixed_coefficient_rational_bound']=s.Rational(47,10)-24/s.Integer(3)**2>0
F=r*r+r*s.sin(r)*s.cos(r)-2*s.sin(r)**2
checks['equatorial_inequality_second_derivative']=s.trigsimp(s.diff(F,r,2)-4*s.sin(r)*(s.sin(r)-r*s.cos(r)))==0
checks={k:bool(v) for k,v in checks.items()}
assert all(checks.values()),checks
receipt={'status':'PASS','python':platform.python_version(),'sympy':s.__version__,'checks':checks,'count':len(checks),'scope':'Encoded algebra only. Does not verify global A3w, minimizing cut domains, novelty or proof completeness.'}
pathlib.Path(__file__).with_name('EXACT_CHECK_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
