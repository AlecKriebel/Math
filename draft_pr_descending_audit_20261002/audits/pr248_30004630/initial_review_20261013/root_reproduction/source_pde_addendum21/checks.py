"""Exact controls for the optional addendum; no imported submitted checker code."""
from datetime import datetime, timezone
from pathlib import Path
import json
import sympy as s

checks=[]
def verify(label, condition):
    assert bool(condition), label
    checks.append(label)

A,R,E,rho,eps,k,z,b=s.symbols('A R E rho eps k z b',positive=True,real=True)
x=s.symbols('x',real=True)
p=s.pi
q=lambda v:A-p*v+v**2/2
endpoint=A/p+R*A**5
verify('composite derivative and its monotonicity domain',s.diff(q(x),x)==x-p)
verify('one-sided substitution exact factorization',s.simplify(q(b-z)-q(b)-z*(p-b)-z**2/2)==0)
expanded=A**2/(2*p**2)-p*R*A**5+R*A**6/p+R**2*A**10/2
verify('actual endpoint error substitution expansion',s.simplify(q(endpoint)-expanded)==0)
remainder=A**2/(4*p**2)*(1-4*p**3*R*A**3)+R*A**6/p+R**2*A**10/2
verify('quadratic absorption factorization',s.simplify(q(endpoint)-A**2/(4*p**2)-remainder)==0)
verify('zero remainder constant edge case',s.simplify(q(endpoint).subs(R,0)-A**2/(2*p**2))==0)
verify('first endpoint radius gives quarter pi',s.simplify((p**2/4)/p)==p/4)
verify('second endpoint radius is sufficient including R zero',s.simplify(R*(p/(4*(1+R))) /(p/4))==R/(1+R))
verify('error absorption radius is sufficient',s.simplify(4*p**3*R/(4*p**3*(1+R)))==R/(1+R))
verify('monotonicity radius cannot be silently dropped',s.simplify(q(p+1)-q(p))==s.Rational(1,2))

# Cancellation of the target-only constant, including nonradial perturbations
# represented by independent endpoint dot product w_y and target dot product w_d.
y2,d2,w2,w_y,w_d=s.symbols('y2 d2 w2 w_y w_d',real=True)
base=(y2+d2-2*p*x)/2
pert=(y2+d2+w2+2*w_d-2*p*x-2*w_y)/2
base_zero=d2/2
pert_zero=(d2+w2+2*w_d)/2
verify('exact target change identity after zero comparison',s.simplify(pert-pert_zero-(base-base_zero)+w_y)==0)

verify('cubic entry rate squared coefficient',s.simplify((s.sqrt(12*rho**2*E*eps))**2-12*rho**2*E*eps)==0)
verify('L1 response coefficient from k',s.simplify(E/(1/(4*p**2))-4*p**2*E)==0)
verify('capped L2 upper coefficient',s.simplify((2*p*s.sqrt(rho*E))**2-4*p**2*rho*E)==0)
verify('upper target threshold gives growth neighborhood',s.simplify(12*rho**2*E*(z**2/(12*rho**2*E))-z**2)==0)

Cg=2**s.Rational(1,4)*p**(-s.Rational(5,4))
c=1/(8*Cg)
verify('lower radius linear term coefficient',s.simplify(Cg*c)==s.Rational(1,8))
verify('rough lower remainder exponent',s.Rational(3,4)*5==s.Rational(15,4))
verify('rough lower remainder after epsilon squared',s.Rational(15,4)-2==s.Rational(7,4))
verify('strict rough lower contradiction margin',s.Rational(1,8)+s.Rational(1,16)<s.Rational(1,4))
verify('fixed nu trial remainder exponent higher than comparison',10>2)
verify('rate pair compatible on small epsilon',s.Rational(3,4)>s.Rational(1,2))
verify('quantitative non-Lipschitz quotient exponent',s.Rational(3,4)-1==-s.Rational(1,4))

out=dict(status='PASS',utc=datetime.now(timezone.utc).isoformat(),assertions=len(checks),checks=checks,sympy_version=s.__version__,scope='Exact algebra and exponent controls only; DERIVATION.md supplies all analytic estimates, monotonicity domains, feasibility, existence, and optimizer quantifiers. No nonlinear PDE simulation or numerical constant is claimed.')
Path(__file__).with_name('CHECKS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
