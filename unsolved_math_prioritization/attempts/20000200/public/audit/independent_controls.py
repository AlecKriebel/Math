#!/usr/bin/env python3
"""Independent exact controls for the fixed-pair inverse-signature audit.

Checks algebraic identities, not the global theorem. General jet variables
are used rather than treating already-simplified invariant formulas as input.
"""
from pathlib import Path
import hashlib, json, math
import sympy as s

I = s.I
checks = []
def check(name, got, want=0):
    residual = s.cancel(got-want)
    assert residual == 0, (name,residual)
    checks.append({"name":name,"passed":True})
def truth(name, predicate):
    assert predicate, name
    checks.append({"name":name,"passed":True})

z0,z1,z2,z3,w0,w1,w2,w3 = s.symbols('z0 z1 z2 z3 w0 w1 w2 w3')
jets = [(z0,z1),(z1,z2),(z2,z3),(w0,w1),(w1,w2),(w2,w3)]
def D(f):
    return s.cancel(sum(s.diff(f,v)*vp for v,vp in jets))
x1,y1=(z1+w1)/2,(z1-w1)/(2*I)
x2,y2=(z2+w2)/2,(z2-w2)/(2*I)
g=s.cancel(x1*x1+y1*y1)
delta=s.cancel(x1*y2-y1*x2)
u=s.cancel(delta**2/g**3)
v=s.cancel((g*D(delta)-s.Rational(3,2)*delta*D(g))/g**3)
h=s.cancel(z2/z1-w2/w1)
check('generic metric from Cartesian jets',g,z1*w1)
check('generic signed tangent logarithmic derivative',h,2*I*delta/g)
check('generic curvature-square formula',u,-h*h/(4*g))
check('generic signed-curvature derivative formula',v,I*D(u)/h)
rho=s.cancel(D(u)/(2*v))
sigma=s.cancel(rho/u)
omega=s.cancel((I*D(u)/v-D(u)/u)/2)
a=s.cancel(2*I*z1/h)
check('generic canonical root logarithmic derivative',D(a)/a,omega)
check('generic positive form',a*rho,z1)
check('generic negative form',sigma/a,w1)
check('generic positive ODE primitive',D(z0/a)+omega*z0/a,rho)
check('generic negative ODE primitive',D(w0*a)-omega*w0*a,sigma)

# Work independently in the quadratic function field E: y^2=x^3-x.
x,y,t=s.symbols('x y t')
f=x**3-x
fp=s.diff(f,x)
def reduceE(expr):
    num,den=s.fraction(s.cancel(expr))
    mod=y*y-f
    den_inv=s.invert(den,mod,y)
    return s.cancel(s.rem(num*den_inv,mod,y))
def DE(expr):
    return reduceE(s.diff(expr,x)+s.diff(expr,y)*fp/(2*y))
def checkE(name, got, want=0):
    check(name,reduceE(got-want),0)
# An actual genus-one signature candidate with integral residues and a
# nontrivial torsion residue divisor, but failed holomorphic correction.
U=x
V=I*x*y/(2*(y+x))
W=reduceE((I*DE(U)/V-DE(U)/U)/2)
checkE('elliptic holomorphic-obstruction canonical omega',W,1/(2*x)+1/y)
checkE('elliptic target recovers y',2*V*x/(I*x-2*V),y)
checkE('elliptic holomorphic obstruction survives order two',2*W-1/x,2/y)
truth('elliptic residual nonzero',reduceE(2/y)!=0)
F=s.expand(4*t*t*x-(x*x-1)*(I*x-2*t)**2)
checkE('elliptic holomorphic-obstruction implicit target',F.subs(t,V))
truth('elliptic holomorphic-obstruction target irreducible',s.Poly(F,x,t,extension=I).is_irreducible)
# Distinct target whose omega is genuinely half-logarithmic despite integral
# residues. P=(0,0)-O is nonprincipal, but 2P-2O=div(x).
U2=y
V2=I*y*fp/(5*x*x-3)
W2=reduceE((I*DE(U2)/V2-DE(U2)/U2)/2)
checkE('elliptic order-two logarithmic omega',W2,1/(2*x))
ratio=reduceE(V2/(I*U2))
x2recover=reduceE((3*ratio-1)/(5*ratio-3))
checkE('elliptic order-two target recovers x squared',x2recover,x*x)
checkE('elliptic order-two target recovers x',U2*U2/(x2recover-1),x)
checkE('elliptic order-two logarithmic certificate',2*W2,1/x)
# Homogeneous-line minimal exponent equals actual birational source degree.
slopes=0
for AA in range(-9,10):
    for BB in range(1,10):
        if math.gcd(abs(AA),BB)!=1 or AA in (0,BB,-BB):
            continue
        g0=math.gcd(abs(BB-AA),abs(BB+AA))
        aa,bb=(BB-AA)//g0,(BB+AA)//g0
        n=s.Rational(AA-BB,2*BB).q
        assert n==abs(aa+bb)
        assert math.gcd(abs(aa),abs(bb))==1
        slopes+=1
truth('homogeneous-line minimal exponent and source degree',slopes>50)
# Local pole-bound sharpness, including the positive residue resonance.
for kk in [1,2,5,11]:
    A=t**(-kk)+t
    theta=s.Rational(kk)/t
    check(f'resonance pole k={kk}',s.diff(A,t)+theta*A,kk+1)
for pole in [2,3,5]:
    kk=4
    theta=t**(-pole)
    rhs=s.diff(t**(-kk),t)+theta*t**(-kk)
    truth(f'irregular pole bound s={pole}',s.limit(rhs*t**(kk+pole),t,0)==1)
# Exactness by trace in an explicit ramified extension t=s^m.
for mm in [2,3,5]:
    # trace of s^j is m*t^(j/m) if m divides j, otherwise zero.
    Fcoeff={0:s.Integer(7),1:s.Integer(3),2*mm:s.Integer(2),-mm:s.Integer(5)}
    normalized_trace=sum(c*t**(j//mm) for j,c in Fcoeff.items() if j%mm==0)
    trace_derivative=sum(c*s.Rational(j,mm)*t**(j//mm-1) for j,c in Fcoeff.items() if j%mm==0 and j)
    check(f'ramified trace commutes with derivative m={mm}',s.diff(normalized_trace,t),trace_derivative)

receipt={"all_passed":True,"count":len(checks),"homogeneous_slopes_checked":slopes,"sympy_version":s.__version__,"coefficient_model":"Exact Q(i) rational and quadratic-function-field arithmetic","scope":"Independent algebraic controls; global theorem and arithmetic algorithm audited by proof, not implemented here","checks":checks}
out=Path(__file__).with_name('INDEPENDENT_CONTROLS.json')
out.write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({k:v for k,v in receipt.items() if k!='checks'},indent=2))
