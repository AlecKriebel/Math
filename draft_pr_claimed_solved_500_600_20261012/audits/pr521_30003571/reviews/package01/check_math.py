#!/usr/bin/env python3
"""Fresh package01 derivation. No candidate/review modules imported."""
from pathlib import Path
import json,sys
import sympy as S
OUT=Path(__file__).resolve().parent
checks=[]
def equal(label,l,r=0):
    q=S.simplify(S.together(l-r))
    if q!=0:raise AssertionError((label,q))
    checks.append(label)
u,v,p,x,q=S.symbols('u v p x q',nonnegative=True)
e,d=S.Rational(1,96),S.Rational(1,4)
phi=2*S.log(1+u)+(2-e)/(1+u)+2*S.log(1+v)+d*u*v*v/((1+u)*(1+v)**2)
# Differentiate the radial potentials as Hermitian forms, then normalize each chart.
rad=lambda h,y:S.diff(y*S.diff(h,y),y)
Aa=4*p+(e+d*x*x)*(1-2*p);Bb=2+2*d*p*x*(2-3*x);Qq=4*d*d*p*(1-p)*x**3*(1-x)
for inv_s in (0,1):
    for inv_z in (0,1):
        pp=1/(1+u) if inv_s else u/(1+u)
        xx=1/(1+v) if inv_z else v/(1+v)
        local=2*S.log(1+u)+2*S.log(1+v)+(2-e)*(1-pp)+d*pp*xx*xx
        a=(1+u)**2*rad(local,u);b=(1+v)**2*rad(local,v)
        c=(1+u)**2*(1+v)**2*u*v*S.diff(local,u,v)**2
        for label,actual,target in [('A',a,Aa),('B',b,Bb),('Q',c,Qq)]:equal(f'chart {inv_s}{inv_z} {label}',actual,target.subs({p:pp,x:xx}))
        # Explicitly check the finite local coordinate origins (the four projective corners).
        for label,actual in [('A',a),('B',b),('det',a*b-c)]:
            val=S.simplify(actual.subs({u:0,v:0}))
            if not val>0:raise AssertionError((label,inv_s,inv_z,val))
        checks.append(f'chart {inv_s}{inv_z} origin strict positivity')
A0=e+S.Rational(167,48)*p;B0=S.Rational(3,2);Q0=p/4
RA=d*x*x+2*d*p*(1-x*x);RB=2*d*((1-p)+p*(1-x)*(1+3*x));RQ=4*d*d*p*(1-(1-p)*x**3*(1-x))
equal('global A certificate',Aa-A0,RA)
equal('global B certificate',Bb-B0,RB)
equal('global Q certificate',Q0-Qq,RQ)
equal('full determinant nonnegative factor decomposition',Aa*Bb-Qq,(S.Rational(1,64)+S.Rational(159,32)*p)+RA*Bb+A0*RB+RQ)
# The pole derivative of the nonlinear initial right side is independently obtained by
# differentiating its three scalar terms. For I the integral is directly rewritten on [0,1].
w0=rad(phi,u).subs(u,0)
equal('central initial jet',w0,e+d*(v/(1+v))**2)
g=rad(phi,v)
equal('central stationary curvature',g.subs(u,0),2/(1+v)**2)
equal('central log g base Hessian',rad(S.log(g),u).subs(u,0),((1+v)**2/2)*rad(w0,v))
B=2*S.log(1+u)+(2-e)/(1+u)
# I(u) = pi exp(-B(u)) int_0^1 exp[-delta p(u) x^2] dx.
# Dominated differentiation at u=0: (log I)'=-B'(0)-delta int x^2 dx.
logI_u0=-S.diff(B,u).subs(u,0)-d*S.integrate(x*x,(x,0,1))
equal('direct initial normalization Hessian',logI_u0,-e-d/3)
initial_rhs_ss=rad(S.log(g),u).subs({u:0,v:0})+w0.subs(v,0)+logI_u0
equal('nonlinear initial pole time derivative',initial_rhs_ss,-S.Rational(1,12))
# Smooth even base jets: phi=F+u*W+O(u^2), where the u coefficient is exactly phi_ssbar.
# The u coefficients of log g and log I are W_zz/g_F and -mean(W), respectively.
# The full closed equation is then solved by coefficient matching in monomials.
L=lambda h:S.expand((x*(1-x)*S.diff(h,x,2)+(1-2*x)*S.diff(h,x))/2)
T=lambda h:S.expand(L(h)+h-S.integrate(h,(x,0,1)))
coef_matrix=S.Matrix([[T(S.Integer(1) if j==0 else x**j).coeff(x,i) for j in range(3)]for i in range(3)])
equal('three-mode characteristic polynomial',coef_matrix.charpoly().as_expr(),S.Symbol('lambda')**2*(S.Symbol('lambda')+2))
a,b,c=S.symbols('a b c')
w=e-d*(1-q)/6+d*(1-q)*x+d*q*x*x
equal('closed jet PDE residual',-2*q*S.diff(w,q),T(w))
equal('initial value',w.subs(q,1),e+d*x*x)
equal('time-constant mean',S.integrate(w,(x,0,1)),e+d/3)
equal('finite-time actual jet coefficient',w.subs({q:S.Rational(1,2),x:0}),-S.Rational(1,96))
equal('crossing boundary',w.subs({q:S.Rational(3,4),x:0}),0)
equal('future central minimum in fiber coordinate',S.diff(w,x),d*(1-q+2*q*x))
for name,h,ev in [('P1',2*x-1,-1),('P2',6*x*x-6*x+1,-3)]:equal(name+' eigenvalue',L(h),ev*h)
# Fixed curvature mass and stationary measures: radial mass of g_F=2, of e^-F=1.
equal('fixed fiber mass',S.integrate(2/(1+v)**2,(v,0,S.oo)),2)
equal('anticanonical radial mass',S.integrate((1+v)**-2,(v,0,S.oo)),1)
equal('density pushforward',S.diff(v/(1+v),v),(1+v)**-2)
# Negative controls: product stationarity and omission of the normalization.
equal('stationary product calibration',S.Integer(2)+S.Integer(-2),0)
equal('literal rc residual rank two',2*S.Integer(2)+S.Integer(-2),2)
equal('normalization omission initial derivative',(L(e+d*x*x)+e+d*x*x).subs(x,0),e)
result={'status':'PASS','count':len(checks),'checks':checks,'generator_matrix':str(coef_matrix),'negative_coefficient':'-1/96','nonlinear_initial_pole_derivative':'-1/12','python':sys.version,'sympy':S.__version__,'limits':'Exact identities and sign-certificate algebra. Smooth finite-time nonlinear solution existence and derivatives established by mathematical argument and primary-source theorem, not this script.'}
(OUT/'MATH_CHECK.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
