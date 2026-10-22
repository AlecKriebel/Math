#!/usr/bin/env python3
"""Independent rational-polynomial controls. Standard library only; no SymPy.

Re-derives the 43 authored algebraic controls with sparse polynomial arithmetic,
exact sphere moments, formal radial jets, and Fraction witnesses. This does not
verify any analytic theorem or import/execute the author's verification code.
"""
from fractions import Fraction as Q
from math import prod
import json

class P:
    def __init__(self, value=0):
        if isinstance(value, P):
            self.d = dict(value.d)
        elif isinstance(value, dict):
            self.d = {k: Q(v) for k, v in value.items() if v}
        else:
            self.d = {(): Q(value)} if value else {}
    def __add__(self, other):
        d = dict(self.d)
        for k, v in P(other).d.items():
            d[k] = d.get(k, 0) + v
        return P(d)
    __radd__ = __add__
    def __neg__(self):
        return P({k: -v for k, v in self.d.items()})
    def __sub__(self, other):
        return self + (-P(other))
    def __rsub__(self, other):
        return P(other) - self
    def __mul__(self, other):
        d = {}
        for ka, a in self.d.items():
            for kb, b in P(other).d.items():
                power = dict(ka)
                for name, exponent in kb:
                    power[name] = power.get(name, 0) + exponent
                key = tuple(sorted((name, e) for name, e in power.items() if e))
                d[key] = d.get(key, 0) + a*b
        return P(d)
    __rmul__ = __mul__
    def __truediv__(self, scalar):
        return self * (1/Q(scalar))
    def __pow__(self, exponent):
        if not isinstance(exponent, int):
            raise ValueError('Integral exponent required')
        if exponent < 0:
            if len(self.d) != 1:
                raise ValueError('Negative powers require a single nonzero monomial')
            key, coefficient = next(iter(self.d.items()))
            return P({tuple((name, e*exponent) for name, e in key): coefficient**exponent})
        result = P(1)
        for _ in range(exponent):
            result *= self
        return result
    def derivative(self, name):
        d = {}
        for key, coefficient in self.d.items():
            power = dict(key)
            exponent = power.get(name, 0)
            if exponent:
                power[name] -= 1
                out = tuple(sorted((n, e) for n, e in power.items() if e))
                d[out] = d.get(out, 0) + exponent*coefficient
        return P(d)
    def substitute(self, replacements):
        result = P()
        for key, coefficient in self.d.items():
            term = P(coefficient)
            for name, exponent in key:
                if name in replacements:
                    term *= P(replacements[name])**exponent
                else:
                    term *= variable(name, exponent)
            result += term
        return result
    def scalar(self):
        if any(key for key in self.d):
            raise ValueError('Polynomial still contains variables')
        return self.d.get((), Q(0))

def variable(name, exponent=1):
    return P({((name, exponent),): 1})

def equivalent(a, b=0):
    return not (P(a)-P(b)).d

checks=[]
def check(name, condition):
    if not condition:
        raise RuntimeError('FAILED: '+name)
    checks.append(name)

def eq(name, a, b=0):
    check(name, equivalent(a,b))

a,b,c,q,k,t = map(variable, ['a','b','c','q','k','t'])
quadratic=lambda x,y: ((x-y)**2-x**2)/2+x*y
fourth=lambda x,y: (x-y)**4-x**4+4*x**3*y

eq('quadratic Bregman', quadratic(a,q), q**2/2)
# k is the scaling of q, i.e. geometric rho squared in the prose report.
eq('scaled quadratic Bregman', quadratic(a,q)-quadratic(b,k*q), (1-k**2)*q**2/2)
eq('fourth-power Bregman', fourth(a,q), 6*a**2*q**2-4*a*q**3+q**4)
residual=((a-b-c)**4+(a-b+c)**4)/2-a**4+4*a**3*b-6*a**2*c**2
eq('parity Hessian residual', residual,
   6*a**2*b**2-4*a*b**3+b**4+(-12*a*b+6*b**2)*c**2+c**4)
# Eliminate the square root by evaluating only even c powers.
parity=Q(0)
for monomial, coefficient in residual.d.items():
    power=dict(monomial)
    if power.get('c',0)%2:
        raise RuntimeError('Unexpected odd c monomial in paired residual')
    parity += coefficient*Q(1,2)**power.get('a',0)*Q(1,10)**power.get('b',0)*Q(1,10)**(power.get('c',0)//2)
eq('parity exact negative witness', parity, -Q(309,10000))
check('parity witness geometrically feasible', Q(1,10)<=4*Q(1,2)*Q(1,10))
eq('witness vector modulus u', Q(1,2)+0, Q(1,2))
eq('witness vector modulus v', Q(1,20)+Q(1,20), Q(1,10))
eq('witness vector dot', 4*Q(1,2)*Q(1,20), Q(1,10))
# Largest argument is 2/5 + sqrt(1/10); square both positive sides.
check('paired arguments in potential domain', Q(1,10)<(1-Q(2,5))**2)
left=fourth(Q(1,10),Q(1,100)); right=fourth(Q(1,2),Q(1,180))
eq('calibration left remainder',left,Q(561,100000000))
eq('calibration right remainder',right,Q(48241,1049760000))
eq('calibration exact negative difference',left-right,-Q(1654369,41006250000))
check('both Bregman remainders positive',left>0 and right>0)
u2,uv,v2=map(variable,['u2','uv','v2'])
energy=((1-u2-2*t*uv-t**2*v2)**2-(1-u2)**2)/4+(1-u2)*t*uv
eq('quartic energy expansion',energy,t**2*(-(1-u2)*v2/2+uv**2)+t**3*uv*v2+t**4*v2**2/4)
# Divide the density identity by r^(N-1), and use independent formal jets.
f,fp,fpp,z,zp,N,aa=map(variable,['f','fp','fpp','z','zp','N','aa'])
ri=variable('r',-1)
lhs=(fp*z+f*zp)**2+((N-1)*ri**2-aa)*f**2*z**2
# The last three terms are (r^(N-1) f f' z^2)' / r^(N-1).
rhs=f**2*zp**2+(N-1)*ri*f*fp*z**2+(fp**2+f*fpp)*z**2+2*f*fp*z*zp
ode=-(N-1)*ri*fp+(N-1)*ri**2*f-aa*f
eq('radial ground-state modulo ODE',(lhs-rhs).substitute({'fpp':ode}))

def odd_double_factorial(m):
    return prod(range(1,m+1,2))

def sphere_mean(poly, n):
    """Normalized exact sphere moments, with x_j=r theta_j."""
    out=P()
    for monomial, coefficient in poly.d.items():
        powers=dict(monomial)
        exponents=[powers.get('x'+str(j),0) for j in range(n)]
        if any(e%2 for e in exponents):
            continue
        degree=sum(exponents)
        moment=Q(prod(odd_double_factorial(e-1) for e in exponents),
                 prod(n+2*j for j in range(degree//2)))
        out += coefficient*moment*variable('r')**degree
    return out

r=variable('r')
for n in range(2,7):
    x=[variable('x'+str(j)) for j in range(n)]
    s=sum(v**2 for v in x)
    psi=x[0]*(1-s)**2
    grad=[psi.derivative('x'+str(j)) for j in range(n)]
    expected=[(1-s)**2*(1 if j==0 else 0)-4*x[0]*x[j]*(1-s) for j in range(n)]
    check('gradient polynomial N='+str(n),all(equivalent(g,h) for g,h in zip(grad,expected)))
    factor=[(1-s)*((1-s)*(1 if j==0 else 0)-4*x[0]*x[j]) for j in range(n)]
    check('clamped gradient factor N='+str(n),all(equivalent(g,h) for g,h in zip(grad,factor)))
    means=[sphere_mean(g,n) for g in grad]
    m=(n-(n+4)*r**2)*(1-r**2)/n
    check('dipole spherical mean N='+str(n),equivalent(means[0],m) and all(equivalent(y) for y in means[1:]))
    eq('nonzero mean at origin N='+str(n),means[0].substitute({'r':0}),1)

# Squaring delta=epsilon/sqrt(C) gives delta^2=epsilon^2/C.
C=variable('C'); eps=variable('eps')
delta_squared=eps**2*C**(-1)
eq('epsilon normalization',delta_squared**(-1)/4,C*eps**(-2)/4)
negative=C*t**2/2+t**4; positive=C*t**2/2
for order in range(3):
    if order:
        negative=negative.derivative('t'); positive=positive.derivative('t')
    eq('C2 matching derivative '+str(order),negative.substitute({'t':0}),positive.substitute({'t':0}))
eq('negative-side second derivative',negative,C+12*t**2)
eq('negative-side domination',(C*t**2/2+t**4)-C*t**2/2,t**4)
eq('t4 no quadratic lower bound ratio',t**4*(t**2/2)**(-1),2*t**2)
if len(checks)!=43:
    raise RuntimeError('Unexpected independent control count')
print(json.dumps({'result':'PASS','checks':len(checks),'method':'Python standard-library Fraction arithmetic, sparse rational polynomials, and exact normalized sphere moments; no SymPy and no import of authored scripts.', 'names':checks,'negative_witnesses':{'parity':str(parity),'calibration':str(left-right)},'scope':'Independent algebraic controls; analytic proofs require the accompanying audit, and the full general-potential target remains unsolved.'},indent=2,sort_keys=True))
