# Publication adapter: all original algebra retained; external-document checks omitted.
# Run through replay.py, which gives this script its original relative directory.
#!/usr/bin/env python3
"""Independent exact arithmetic for pass 2; no numerical minimization claims."""
import hashlib
import json
from pathlib import Path
import sympy as s

root = Path(__file__).resolve().parents[1]
checks = []
def check(name, condition):
    assert condition, name
    checks.append({'name': name, 'passed': True})

a1,a2,a3 = s.symbols('a1 a2 a3', real=True)
gamma = a1+a2+a3-3
barrier = a1+a2-3-3*gamma
positive = 4*a1+a3-6
eta = 2*(3*a1+a2+2*a3-6)
check('anisotropic third-row exponent gap', s.expand(positive-barrier-eta)==0)
check('balanced anisotropic exponent gap', s.expand(eta.subs(a2,6-4*a1-a3)-2*(a3-a1))==0)
alpha=s.symbols('alpha', positive=True)
check('hard-truncation barrier divergence exponent', s.expand(barrier.subs({a1:1-alpha,a2:1-alpha,a3:1+5*alpha})+11*alpha+1)==0)
check('hard-truncation positive divergence exponent', s.expand(positive.subs({a1:1-alpha,a2:1-alpha,a3:1+5*alpha})-alpha+1)==0)

z,rho,r,R=s.symbols('z rho r R', positive=True)
sigma, ell, m=s.symbols('sigma ell m', positive=True)
Pc,Ps,Bc,Bs,Un=s.symbols('Pc Ps Bc Bs Un', real=True)
# Resolve the stationarity identity algebraically, keeping shell density formal.
core=Pc-3*Bc
shell=3*m*Bs-m*Ps+2*ell*rho**(-3)*Ps-ell*rho**(-3)*Un
sol=s.solve(core+shell, Bc)[0]
sol_total=s.solve((core+shell).subs(Bs,z-Bc), Bc)[0]
expected=sigma*z+(1-sigma)*Pc/3+(2*(r/rho)**3-sigma)*Ps/3-(r/rho)**3*Un/3
check('concentric comparison coefficients', s.simplify(sol_total.subs({m:sigma/(1-sigma),ell:r**3/(1-sigma)})-expected)==0)
# The boundary collar inequality is 0 <= 16 P -9/4 Bi +15/4 (Bt-Bi).
P,Bi,Bt=s.symbols('P Bi Bt', real=True)
check('boundary collar constants', s.solve(16*P-s.Rational(9,4)*Bi+s.Rational(15,4)*(Bt-Bi),Bi)[0]==s.Rational(8,3)*P+s.Rational(5,8)*Bt)

beta,n1,n2,n3,L=s.symbols('beta n1 n2 n3 L', real=True)
n=s.Matrix([n1,n2,n3]); w=beta*s.Matrix([n1,n2,-5*n3])
M=s.eye(3)+w*n.T
Delta=1+beta*(n1*n1+n2*n2-5*n3*n3)
check('compatible ellipsoid determinant lemma', s.factor(M.det()-Delta)==0)
check('compatible ellipsoid inverse lemma', all(s.simplify(t)==0 for t in M*(s.eye(3)-w*n.T/Delta)-s.eye(3)))
check('unit-sphere determinant simplification', s.simplify(Delta.subs(n1*n1,1-n2*n2-n3*n3)-(1+beta*(1-6*n3*n3)))==0)
for label,power,endpoint in [('inverse gradient',5,s.Rational(9,5)),('inverse cofactor',4,s.Rational(9,4)),('inverse determinant',3,s.Integer(3))]:
    check(label+' critical power',power*endpoint-3==6)
check('inverse gradient Holder weights',s.Rational(3,5)+s.Rational(2,5)==1 and 3*s.Rational(3,5)==s.Rational(9,5) and -2*s.Rational(2,5)==-s.Rational(4,5))
check('inverse cofactor Holder weights',s.Rational(3,8)+s.Rational(5,8)==1 and 6*s.Rational(3,8)==s.Rational(9,4) and -2*s.Rational(5,8)==-s.Rational(5,4))

# An independent continuous-tensor/unbounded-pressure construction.
r=s.symbols('r',positive=True)
log=s.log(s.E/r)
q=1/log
p=2*s.log(log)-1/log
check('independent abstract pressure identity',s.simplify(s.diff(p,r)+s.diff(q,r)+2*q/r)==0)
# This identity is local near zero; distributional extension follows from vanishing sphere flux.

sources=[]  # No external source documents are bundled or reverified.
result={'scope':'Public algebra replay only; historical source-document checks are omitted. No benchmark resolution is asserted.', 'checks':checks,'total_checks':len(checks),'source_metadata_checked':sources,'benchmark_proved':False,'benchmark_counterexample':False}
out=Path(__file__).with_name('AUDIT_CHECKS.json')
out.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'total_checks':len(checks),'passed':True,'output':str(out)},indent=2))
