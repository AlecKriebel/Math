#!/usr/bin/env python3
"""Exact controls for the reconstruction of the credited 2007 theorem."""
from pathlib import Path
import hashlib,json,math
import sympy as s
checks={}
def ck(name,v):
    assert bool(v),name
    checks[name]='PASS'
x,y,z,t,e=s.symbols('x y z t e')
# Binary homogeneous powers span: invert actual Vandermonde/binomial matrices.
for d in range(1,8):
    V=s.Matrix(d+1,d+1,lambda j,q:s.binomial(d,j)*s.Integer(q)**j)
    ck(f'vandermonde_invertible_{d}',V.det()!=0)
    for j in range(d+1):
        rhs=s.zeros(d+1,1);rhs[j]=1;c=V.inv()*rhs
        rebuilt=sum(c[q]*(x+q*y)**d for q in range(d+1))
        ck(f'power_decomposition_{d}_{j}',s.expand(rebuilt-x**(d-j)*y**j)==0)
# Exact shear invariants, Jacobians and polynomial inverses, with coefficients
# depending on another variable and a formal coefficient e.
for d in range(1,5):
    for q in [-1,0,2]:
        h=(1+e*z*z)*d*(x+q*y)**(d-1)
        P=s.Matrix([x+t*q*h,y-t*h,z])
        ck(f'invariant_linear_form_{d}_{q}',s.expand(P[0]+q*P[1]-x-q*y)==0)
        hp=h.subs({x:P[0],y:P[1],z:P[2]},simultaneous=True)
        ck(f'shear_coefficient_invariant_{d}_{q}',s.expand(hp-h)==0)
        ck(f'shear_jacobian_{d}_{q}',s.expand(P.jacobian([x,y,z]).det())==1)
        ck(f'shear_inverse_{d}_{q}',s.expand(P[0]-t*q*hp)==x and s.expand(P[1]+t*hp)==y)
# A nonreduced Q-algebra control, R=Q[e]/(e^2).
def modvar(f,var,m):
    return s.Poly(s.expand(f),var).rem(s.Poly(var**m,var)).as_expr()
P=[x+t*e*x*x,y-2*t*e*x*y]
Q=[x-t*e*x*x,y+2*t*e*x*y]
ck('nilpotent_coefficient_jacobian',modvar(s.Matrix(P).jacobian([x,y]).det()-1,e,2)==0)
ck('nilpotent_coefficient_inverse',all(modvar(Q[i].subs({x:P[0],y:P[1]},simultaneous=True)-[x,y][i],e,2)==0 for i in range(2)))
# General divergence-free decomposition by integration in the last variable.
for k in range(1,7):
    H1=x**k*y*z*z+e*y**2*z
    H2=(x+1)*y**k*z**3
    F=s.Matrix([s.diff(H1,z),s.diff(H2,z),-s.diff(H1,x)-s.diff(H2,y)+x*y])
    ck(f'divergence_input_{k}',s.expand(sum(s.diff(F[i],v) for i,v in enumerate([x,y,z])))==0)
    cur=list(F)
    for i,var in enumerate([x,y]):
        H=s.integrate(cur[i],z);cur[i]=s.expand(cur[i]-s.diff(H,z));cur[2]=s.expand(cur[2]+s.diff(H,var))
        ck(f'integrated_component_{k}_{i}',cur[i]==0)
    ck(f'last_component_is_shear_{k}',s.diff(cur[2],z)==0)
# Full finite t-adic lifting in SL2: reconstruct a truncated nonnilpotent
# exponential by actual polynomial products of three square-zero shears.
I=s.eye(2);A=s.Matrix([[1,2],[-3,-1]])
Nup=s.Matrix([[0,1],[0,0]]);Nlow=s.Matrix([[0,0],[1,0]]);M=s.Matrix([[1,1],[-1,-1]])
for j,N in enumerate([Nup,Nlow,M]):
    ck(f'linear_shear_square_zero_{j}',N*N==s.zeros(2))
    ck(f'linear_shear_determinant_{j}',s.expand((I+t*N).det())==1)
def trmat(B,m):return B.applyfunc(lambda f:modvar(f,t,m))
for modulus in range(2,8):
    target=sum((t**j*A**j/s.factorial(j) for j in range(modulus)),s.zeros(2))
    ck(f'target_special_mod_{modulus}',modvar(target.det()-1,t,modulus)==0)
    lift=I
    for r in range(1,modulus):
        residual=trmat(lift.adjugate()*target,modulus)
        F=residual.applyfunc(lambda f:s.expand(f).coeff(t,r))
        ck(f'jet_divergence_{modulus}_{r}',F.trace()==0)
        a,b,c=F[0,0],F[0,1],F[1,0]
        ck(f'linear_decomposition_{modulus}_{r}',F==a*M+(b-a)*Nup+(c+a)*Nlow)
        correction=(I+t**r*a*M)*(I+t**r*(b-a)*Nup)*(I+t**r*(c+a)*Nlow)
        lift=(lift*correction).applyfunc(s.expand)
        ck(f'next_jet_matches_{modulus}_{r}',trmat(lift-target,r+1)==s.zeros(2))
    ck(f'full_lift_jacobian_{modulus}',s.expand(lift.det())==1)
    ck(f'full_lift_matches_{modulus}',trmat(lift-target,modulus)==s.zeros(2))
# Characteristic-p scope control at square-zero t: valid below, nonlinear
# and therefore nonliftable in the determinant-one one-variable domain case.
for p in [2,3,5,7]:
    f=x+t*x**p;g=x-t*x**p
    comp=modvar(f.subs(x,g)-x,t,2)
    ck(f'char_p_square_zero_inverse_{p}',s.Poly(comp,x,t,modulus=p).is_zero)
    ck(f'char_p_jacobian_one_{p}',s.Poly(s.diff(f,x)-1,x,t,modulus=p).is_zero)
r={'passed':len(checks),'failed':0,'sympy_version':s.__version__,'artifact_sha256':hashlib.sha256(Path(__file__).with_name('KNOWN_THEOREM.md').read_bytes()).hexdigest(),'checks':checks,'scope':'Exact finite controls for a credited known theorem; no discovery or exhaustive ring verification is claimed.'}
Path(__file__).with_name('verification.json').write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps({k:v for k,v in r.items() if k!='checks'}))
