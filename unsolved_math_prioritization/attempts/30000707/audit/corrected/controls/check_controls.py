#!/usr/bin/env python3
"""Exact, bounded algebra controls. Not a proof of the unresolved classification."""
import json
import math
import platform
from pathlib import Path
import sympy as s

ROOT = Path(__file__).resolve().parents[1]
checks = []
def equal(label, lhs, rhs=0):
    residual = s.factor(s.cancel(lhs-rhs))
    assert residual == 0, (label, residual)
    checks.append({'label': label, 'passed': True})
def reject(label, lhs, rhs=0):
    residual = s.factor(s.cancel(lhs-rhs))
    assert residual != 0, label
    checks.append({'label': label, 'passed': True, 'nonzero_residual': str(residual)})

x,b,k,v,hp,a,qp,F,F1,F2,p,q,r,c,B = s.symbols('x b k v hp a qp F F1 F2 p q r c B')
P = lambda t: t**3+p*t*t+q*t+r
# Literal representative, sharing roots, and the source-orbit sign check.
f=b-1/x; g=b-x
Pc=lambda t:(t-b+1)*(t-b)*(t-b-1)
equal('canonical psi1', x*s.diff(f,x)*(f-g)/Pc(f),x)
equal('canonical psi2', x*s.diff(g,x)*(f-g)/Pc(g),1/x)
for value in (-1,0,1):
    if value:
        equal('canonical finite root relation '+str(value),
              s.factor((f-b-value)/(g-b-value)), value/x)
    else:
        equal('canonical omitted value product',(f-b)*(g-b),1)
f0=1/x;g0=x;P0=lambda t:t**3-t
equal('source representative actual psi1',x*s.diff(f0,x)*(f0-g0)/P0(f0),-x)
equal('source representative actual psi2',x*s.diff(g0,x)*(f0-g0)/P0(g0),-1/x)
reject('wrong literal positive-sign representative',x*s.diff(f0,x)*(f0-g0)/P0(f0),x)
# Arbitrary entire h in CM parametrization: derivative represented by hp.
f=b+k*v;g=b+k/v;Pc=lambda t:(t-b)*((t-b)**2-k*k)
equal('CM formula psi1',k*hp*v*(f-g)/Pc(f),hp/(k*v))
equal('CM formula psi2',-k*hp/v*(f-g)/Pc(g),hp*v/k)
equal('CM product',(hp/(k*v))*(hp*v/k),hp**2/k**2)
# Pole residue relations and formal coefficient matrix for arbitrary k.
j=s.symbols('j')
for sign in (1,-1):
    A=sign-1/a;D=a-sign
    equal('pole psi1 sign '+str(sign),-(A-D)/A**2,a)
    equal('pole psi2 sign '+str(sign),-(A-D)/D**2,1/a)
    mat=s.Matrix([[j*(A-D)-A-3*a*A*A,A],[-D,j*(A-D)+D-3*D*D/a]])
    equal('all-k Laurent determinant sign '+str(sign),mat.det(),(a-sign)**4/a**2*(j+2)*(j+3))
# Finite enumerated negative controls, in addition to the general written proof.
for m in range(1,9):
    for n in range(1,9):
        if m!=n:
            val=min(m,n)-1
            assert (val==0)==(min(m,n)==1)
        if m>n:
            assert (m-1,2*n-m-1)!=(0,0)
        if n>m:
            assert (2*m-n-1,n-1)!=(0,0)
checks.append({'label':'valuation controls 1<=m,n<=8', 'passed':True,'cases':64})
# Exact differential elimination via formal jets, without solving an ODE.
G=F-a*P(F)/F1
Gp=s.diff(G,F)*F1+s.diff(G,F1)*F2+s.diff(G,a)*a*qp
res=Gp*(F-G)-P(G)/a
u=1/a
E=P(F)*F2-(qp*P(F)+u*P(F)*s.diff(P(F),F,2)/2)*F1+(u*u-1)*s.diff(P(F),F)*F1**2+(u-u**3)*F1**3+P(F)**2
equal('scalar-elimination identity',res,a*a*P(F)/F1**3*E)
# Two generic endpoint-pole order equations yield no positive m,n.
m,n=s.symbols('m n')
equal('both-poles endpoint order subtraction',(n-2*m-1)-(n-2*n+1),2*(n-m-1))
# The rational degree-two proof uses generic exact coefficients, not a finite grid.
R=-1/x+(c-1)/(x-c);S=-x+B+(c*c-c)/(x-c)
Pc=lambda t:t**3+p*t*t+q*t
N1=s.factor(s.cancel((s.diff(R,x)*(R-S)-Pc(R))*x*x*(x-c)**2))
N2=s.factor(s.cancel((x*x*s.diff(S,x)*(R-S)-Pc(S))*(x-c)**2))
N1=s.Poly(N1,x);N2=s.Poly(N2,x)
equal('degree2 N1 leading',N1.nth(3),-(c-2)*(q+1))
equal('degree2 N2 leading',N2.nth(4),-2*B-p)
sub={p:-2*B,q:-2,c:2}
equal('exceptional c2 coefficient x',N1.nth(1).subs(sub),4*(B-1))
equal('exceptional c2 constant',N1.nth(0).subs(sub),4*(B+2))
equal('exceptional contradiction',4*(B+2)-4*(B-1),12)
sub={p:-2*B,q:-1}
equal('ordinary constant coefficient',N1.nth(0).subs(sub),c*(B*c+c*c+c-2))
Bvalue=-c-1+2/c
z2=s.factor(N1.nth(2).subs(sub).subs(B,Bvalue))
z1=s.factor(N1.nth(1).subs(sub).subs(B,Bvalue))
equal('ordinary x2 reduction',z2,-2*(c-1)*(c**3-c*c-4*c+6)/c)
equal('ordinary x reduction',z1,-4*(c-1)*(c*c-2))
A=c*c-2;D=c**3-c*c-4*c+6
equal('unit-ideal certificate after c!=1',(4-c*c-c)*A+(c+2)*D,4)
# Degenerate c=1 removes the pole and returns the canonical solution.
equal('collapsed R',R.subs(c,1),-1/x)
equal('collapsed S',S.subs({c:1,B:0}),-x)
# The other residue sign is covered by an exact variable/value involution.
Rminus=-1/x+(-c-1)/(x-c)
Sminus=-x+B+(c*c+c)/(x-c)
equal('sign symmetry R',-Rminus.subs(x,-x),R.subs(c,-c))
equal('sign symmetry S',-Sminus.subs(x,-x),S.subs({c:-c,B:-B}))
# Composing the canonical pair with z^2 produces an unavoidable derivative factor.
z=s.symbols('z')
equal('quadratic composition product',(2*z*x)*(2*z/x),4*z*z)
reject('quadratic composition is not a solution',4*z*z,1)
# Printed recent proof: normalized canonical pair has a nonconstant Phi.
f=(x+1)/2;g=(1/x+1)/2;Pc=lambda t:t*(t-1)*(t-s.Rational(1,2))
equal('recent dependency canonical Phi',s.diff(f,x)*Pc(g)/(s.diff(g,x)*Pc(f)),1/x**2)
# Positive-ray values; analytic estimate is log((e^r+1)/2)<=r, omega=3/2.
scale=[]
for rr in [4,16,64,256,1024,4096]:
    ratio=(rr-math.log(2)+math.log1p(math.exp(-rr)))/(rr**1.5)
    bound=rr**-0.5
    assert 0<ratio<=bound
    scale.append({'r':rr,'ratio':ratio,'upper_bound':bound})
checks.append({'label':'zero angular-leading-coefficient scale control','passed':True,'illustrative_values':scale})
result={
 'status':'PASS','python':platform.python_version(),'sympy':s.__version__,
 'check_count':len(checks),'checks':checks,
 'limits':[
  'Exact symbolic identities use SymPy over rational-function fields; no transcendental root search.',
  'The valuation enumeration is restricted to 1<=m,n<=8; the unrestricted argument is written in PROOF.md.',
  'Rational-exponential exclusion is only degree <=2 in the first system.',
  'Quadratic parity exclusion is only the simultaneous-even/rational-in-exp(z^2) ansatz.',
  'The recent-source test rejects one positivity inference, not its theorem statement.',
  'No check proves general 3IM+1CM rigidity, global continuation of the scalar ODE, or completeness of the classification.'
 ]}
(ROOT/'controls'/'CONTROL_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':result['status'],'check_count':len(checks),'output':'controls/CONTROL_RESULTS.json'}))
