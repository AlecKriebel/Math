#!/usr/bin/env python3
"""Exact polynomial certificates for family 047's stabilization and retract.

Run with Python 3 and SymPy 1.14.0.  Every symbolic check is over ZZ.
The full five-component idempotent is certified compositionally through
inverse coordinate maps, rather than by impractical expanded substitution.
Additional rational-point checks exercise the actual factored endomorphism.
No nonpolynomiality assertion is tested or assumed here.
"""
import argparse
import hashlib
import json
import platform
from pathlib import Path
import sympy as sp

checks = []
def check(label, expr):
    poly = sp.Poly(sp.expand(expr), *sorted(expr.free_symbols, key=str)) if expr.free_symbols else sp.sympify(expr)
    assert poly.is_zero if hasattr(poly, 'is_zero') else poly == 0, (label, sp.expand(expr))
    checks.append(label)

p,s,u,F,J,w,x,X,L,M,E,Z = sp.symbols('p s u F J w x X L M E Z')
x0 = s*s + u**3
xact = x0+p*p*F
Hact = xact*xact*F-(1+2*s*xact)*J-p*p*J*J-p*u
# Check the actual derivation, before abbreviating x as an invariant.
derivs = {p:0,s:-3*p*p*xact*u*u,u:-p*p,F:(6*s*xact+3)*u*u,J:3*xact*xact*u*u}
delta = lambda f: sum(sp.diff(f,v)*dv for v,dv in derivs.items())
check('delta(x)=0 in the original five-variable polynomial ring',delta(xact))
check('delta(H)=p^3 in the original five-variable polynomial ring',delta(Hact)-p**3)

D = -3*u*u*w+3*p*p*u*w*w-p**4*w**3
U = u-p*p*w
S = s+p*p*x*D
Fp = F-(1+2*s*x)*D-p*p*x*x*D*D
Jp = J-x*x*D
check('U^3-u^3=p^2 D', U**3-u**3-p*p*D)
check('Phi preserves x=s^2+u^3+p^2 F', S*S+U**3+p*p*Fp-(s*s+u**3+p*p*F))
check('Phi preserves z=sx+p^2J', S*x+p*p*Jp-(s*x+p*p*J))
check('Phi preserves y=s+x(x-u^3)', S+x*(x-U**3)-(s+x*(x-u**3)))
Hp = x*x*Fp-(1+2*S*x)*Jp-p*p*Jp*Jp-p*U
Habbrev = x*x*F-(1+2*s*x)*J-p*p*J*J-p*u
check('Phi(H)=H+p^3w',Hp-Habbrev-p**3*w)
Dinv = -3*U*U*(-w)+3*p*p*U*w*w-p**4*(-w)**3
check('inverse D cocycle',D+Dinv)
check('Phi inverse composition on u', U-p*p*(-w)-u)
check('Phi inverse composition on s', S+p*p*x*Dinv-s)
check('Phi inverse composition on F', Fp-(1+2*S*x)*Dinv-p*p*x*x*Dinv*Dinv-F)
check('Phi inverse composition on J', Jp-x*x*Dinv-J)
# Explicitly certify the reverse composition as well.
Dm = D.subs(w,-w)
Um = u+p*p*w
Sm = s+p*p*x*Dm
Fm = F-(1+2*s*x)*Dm-p*p*x*x*Dm*Dm
Jm = J-x*x*Dm
Dr = D.subs(u,Um)
check('reverse inverse D cocycle',Dm+Dr)
check('reverse composition on u',Um-p*p*w-u)
check('reverse composition on s',Sm+p*p*x*Dr-s)
check('reverse composition on F',Fm-(1+2*Sm*x)*Dr-p*p*x*x*Dr*Dr-F)
check('reverse composition on J',Jm-x*x*Dr-J)
# p,w are fixed in both orders.

# Work over a polynomial coefficient ring with X an independent abbreviation.
a=4*s*s; b=1+2*s*X; c=2*s*X-1; d=X*X
f=a*L+b*M; j=c*L+d*M
check('determinant of (F,J)->(L,M) is one',4*s*s*X*X+(1+2*s*X)*(1-2*s*X)-1)
check('linear inverse recovers L', X*X*f-(1+2*s*X)*j-L)
check('linear inverse recovers M',(1-2*s*X)*f+4*s*s*j-M)
Q=2*X*f*f-2*s*f*j-j*j
C=M*M*(2*X+6*s*X*X+4*s*s*X**3-X**4)
q1=M*(4*X*a*b-2*s*(a*d+b*c)-2*c*d)
q2=2*X*a*a-2*s*a*c-c*c
Q1=q1+q2*L
check('Q constant C and factor Q1',Q-C-L*Q1)
H=L-p*u+p*p*Q+p**4*f**3
xL=X+p*p*f
check('H(L) expansion',xL*xL*f-(1+2*s*xL)*j-p*p*j*j-p*u-H)
Lstar=p*u-p*p*C
check('polynomial root modulo p^3',H.subs(L,Lstar)-p**3*((u-p*C)*Q1.subs(L,Lstar)+p*f.subs(L,Lstar)**3))
h=u-p*Q-p**3*f**3-p*p*w
e0=-w-p*f**3-Q1*h
check('e polynomial certificate',p**3*e0-(L-Lstar)-(p*p*Q1-1)*(H+p**3*w))
Le=Lstar+p**3*E
fe=f.subs(L,Le)
We=-E-(u-p*C+p*p*E)*Q1.subs(L,Le)-p*fe**3
check('polynomial W without division',H.subs(L,Le)+p**3*We)
check('g(q(e))=e: exact polynomial composition',e0.subs({L:Le,w:We}, simultaneous=True)-E)
# q(g(L))-L belongs to the defining ideal, explicitly.
check('q(g(L))-L exact ideal certificate',Lstar+p**3*e0-L-(p*p*Q1-1)*(H+p**3*w))
# The remaining inverse coordinate is certified by a cubic difference quotient.
h1=1+p*p*q1+3*p**4*a*(b*M)**2
h2=p*p*q2+3*p**4*a*a*b*M
h3=p**4*a**3
K=h1+h2*(Z+L)+h3*(Z*Z+Z*L+L*L)
check('cubic difference quotient for q(g(w))-w certificate', H.subs(L,Z)-H-(Z-L)*K)
# Let R=p^2 Q1-1, Root=Lstar+p^3 e0=L+R*(H+p^3w).
# The certified identities imply
# p^3*(W(e0)-w)=-(H+p^3w)*(1+R*K(Root,L)).
# Domain and p!=0 then prove q(g(w))=w in T.

# r(j)=1 and rho^2=rho follow from these inverse maps and ev_0*inclusion=1.

# Special-fiber endomorphism: substitute X=s^2+u^3 after factorization.
kappa=sp.expand(q1/M)
W0=-E-u*kappa*M
M0=M+3*u*u*W0
E0=-u*kappa*M0
check('rho on p=0 has W(image)=0',-E0-u*kappa*M0)
check('rho on p=0 is idempotent on M',M0+3*u*u*(-E0-u*kappa*M0)-M0)
check('rho on p=0 is idempotent on E',-u*kappa*(M0+3*u*u*(-E0-u*kappa*M0))-E0)
check('rj on special-fiber M',M0.subs(E,-u*kappa*M)-M)

# Actual factored polynomial endomorphism using only rational arithmetic.
def datum(ss,uu,ff,jj):
    xx=ss*ss+uu**3
    ll=xx*xx*ff-(1+2*ss*xx)*jj
    mm=(1-2*ss*xx)*ff+4*ss*ss*jj
    aa=4*ss*ss; bb=1+2*ss*xx; cc=2*ss*xx-1; dd=xx*xx
    qq1=mm*(4*xx*aa*bb-2*ss*(aa*dd+bb*cc)-2*cc*dd)
    qq2=2*xx*aa*aa-2*ss*aa*cc-cc*cc
    qq=2*xx*ff*ff-2*ss*ff*jj-jj*jj
    return ll,mm,qq,qq1+qq2*ll

def rho(point):
    pp,ss,uu,mm,ee=point
    xx=ss*ss+uu**3
    CC=mm*mm*(2*xx+6*ss*xx*xx+4*ss*ss*xx**3-xx**4)
    ll=pp*uu-pp*pp*CC+pp**3*ee
    ff=4*ss*ss*ll+(1+2*ss*xx)*mm
    jj=(2*ss*xx-1)*ll+xx*xx*mm
    _,_,_,QQ1=datum(ss,uu,ff,jj)
    WW=-ee-(uu-pp*CC+pp*pp*ee)*QQ1-pp*ff**3
    DD=-3*uu*uu*WW+3*pp*pp*uu*WW*WW-pp**4*WW**3
    xx=xx+pp*pp*ff
    SS=ss+pp*pp*xx*DD; UU=uu-pp*pp*WW
    FF=ff-(1+2*ss*xx)*DD-pp*pp*xx*xx*DD*DD
    JJ=jj-xx*xx*DD
    _,MM,QQ,QQ1=datum(SS,UU,FF,JJ)
    EE=-pp*FF**3-QQ1*(UU-pp*QQ-pp**3*FF**3)
    # Returned image coordinates are polynomials; check they lie on H=0.
    xx=SS*SS+UU**3+pp*pp*FF
    assert xx*xx*FF-(1+2*SS*xx)*JJ-pp*pp*JJ*JJ-pp*UU == 0
    return pp,SS,UU,MM,EE

points=[(0,0,0,0,0),(0,1,1,2,3),(1,0,1,0,0),(1,1,0,0,0),(1,0,0,1,0),
        (-1,0,1,0,0),(sp.Rational(1,2),0,0,1,sp.Rational(-1,3))]
for n,point in enumerate(points):
    first=rho(point)
    assert rho(first)==first, ('rational idempotence',n)
    checks.append(f'actual factored rho exact rational idempotence point {n}')

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--upstream-root',type=Path,help='Optional read-only pinned source clone root; verify the construction hash if supplied.')
args=parser.parse_args()
construction_hash='fd10c0e2eb35a5572f43263ba88ea893551415c1807f6f6c8ad6158e64caa882'
if args.upstream_root is not None:
    source=args.upstream_root/'preprints'/'An-explicit-failure-of-complex-affine-space-cancellation-September-23-2026'/'build'/'sections'/'02-construction.tex'
    assert hashlib.sha256(source.read_bytes()).hexdigest()==construction_hash, 'Upstream construction hash mismatch'
result={'status':'PASS','symbolic_checks':len(checks)-len(points),'rational_points':len(points),
        'python':platform.python_version(),'sympy':sp.__version__,
        'source_commit':'adc7f1241b42e322a6451854ab7e4b4c146bf78a',
        'construction_sha256':construction_hash,
        'scope':'stabilization, split maps and compositional idempotence only; no nonpolynomiality certificate',
        'checks':checks}
print(json.dumps(result,indent=2))
