#!/usr/bin/env python3
"""Independent exact algebra checks for the credited jet-lifting proof."""
import json
from pathlib import Path
import sympy as s
x,y,z,t,e,u=s.symbols('x y z t e u')
checks={}
def ck(name,value):
    assert bool(value),name
    checks[name]='PASS'

def trunc(f,m,relation=None):
    f=s.expand(f)
    f=sum(c*t**k[0] for k,c in s.Poly(f,t).terms() if k[0]<m)
    if relation is not None:
        f=s.rem(f,relation,e)
    return s.expand(f)

def comp(P,Q,vs,m,relation=None):
    return [trunc(f.subs(dict(zip(vs,Q)),simultaneous=True),m,relation) for f in P]

def decompose(F,vs):
    n=len(vs);cur=list(F);data=[]
    for i in range(n-1):
        H=s.integrate(cur[i],vs[-1])
        cur[i]=s.expand(cur[i]-s.diff(H,vs[-1]))
        cur[-1]=s.expand(cur[-1]+s.diff(H,vs[i]))
        for (a,b),coef in s.Poly(H,vs[i],vs[-1]).terms():
            d=a+b
            if not d: continue
            V=s.Matrix(d+1,d+1,lambda j,q:s.binomial(d,j)*s.Integer(q)**j)
            rhs=s.zeros(d+1,1);rhs[b]=coef
            cs=V.inv()*rhs
            for q,c in enumerate(cs):
                if c:
                    h=s.expand(c*d*(vs[i]+q*vs[-1])**(d-1))
                    v=[0]*n;v[i]=q;v[-1]=-1
                    data.append((h,v))
    assert s.diff(cur[-1],vs[-1])==0
    if cur[-1]:
        v=[0]*n;v[-1]=1;data.append((cur[-1],v))
    return data

# Rational determinant formula and reconstruction of nonhomogeneous binary data.
for d in range(0,7):
    V=s.Matrix(d+1,d+1,lambda j,q:s.binomial(d,j)*s.Integer(q)**j)
    expected=s.prod(s.binomial(d,j) for j in range(d+1))*s.prod(k-j for j in range(d+1) for k in range(j+1,d+1))
    ck(f'vandermonde_exact_d{d}',V.det()==expected)

vs=[x,y,z]
Fs=[
    [y*z, x*z, x*y],
    [2*x*z, 3*y*z*z, -z*z-2*y*z**3],
    [e*y+2*x*z, z*x+y, -z*z],
]
# Replace the deliberately non-divergence-free second/third inputs by their
# canonical last-component correction; the rejected-input diagnostic is explicit.
for k,F in enumerate(Fs):
    div=s.expand(sum(s.diff(f,v) for f,v in zip(F,vs)))
    if k: ck(f'nonzero_divergence_detected_{k}',div!=0)
    F[-1]=s.expand(F[-1]-s.integrate(div,z))
    ck(f'divergence_zero_{k}',sum(s.diff(f,v) for f,v in zip(F,vs))==0)
    data=decompose(F,vs)
    ck(f'vector_reconstruction_{k}',all(s.expand(sum(h*v[i] for h,v in data)-F[i])==0 for i in range(3)))
    for j,(h,v) in enumerate(data):
        ck(f'invariance_{k}_{j}',s.expand(h.subs({a:a+u*b for a,b in zip(vs,v)},simultaneous=True)-h)==0)
        P=[a+t*h*b for a,b in zip(vs,v)]
        M=[a-t*h*b for a,b in zip(vs,v)]
        ck(f'exact_inverse_{k}_{j}',all(s.expand(f.subs(dict(zip(vs,P)),simultaneous=True)-a)==0 for f,a in zip(M,vs)))
        ck(f'exact_jacobian_{k}_{j}',s.expand(s.Matrix(P).jacobian(vs).det())==1)

# Independent nonlinear finite-jet elimination, with explicit elementary factors.
def lift_control(name,target,m,relation=None):
    vs=[x,y]
    residual=[trunc(f,m,relation) for f in target]
    reconstructed=vs[:]
    factors=0
    for r in range(1,m):
        F=[s.expand(f).coeff(t,r) for f in residual]
        div=sum(s.diff(f,v) for f,v in zip(F,vs))
        ck(f'{name}_divergence_r{r}',trunc(div,m,relation)==0)
        data=decompose(F,vs)
        correction=vs[:]
        inverse=vs[:]
        for h,v in data:
            P=[a+t**r*h*b for a,b in zip(vs,v)]
            Mi=[a-t**r*h*b for a,b in zip(vs,v)]
            correction=comp(correction,P,vs,m,relation)
            inverse=comp(Mi,inverse,vs,m,relation)
            factors+=1
        ck(f'{name}_correction_inverse_r{r}',comp(inverse,correction,vs,m,relation)==vs)
        residual=comp(inverse,residual,vs,m,relation)
        reconstructed=comp(reconstructed,correction,vs,m,relation)
        ck(f'{name}_next_jet_r{r}',all(trunc(f-a,r+1,relation)==0 for f,a in zip(residual,vs)))
    ck(f'{name}_full_jet',residual==vs and all(trunc(f-g,m,relation)==0 for f,g in zip(reconstructed,target)))
    ck(f'{name}_target_jacobian',trunc(s.Matrix(target).jacobian(vs).det()-1,m,relation)==0)
    return factors

P=[x+t*y*y,y]
Q=[x,y+t*x]
target=comp(P,Q,[x,y],4)
counts={'nonlinear_Q':lift_control('nonlinear_Q',target,4)}
# A nilpotent-coefficient automorphism not triangular in x,y.
Pnil=[x+t*e*x*x,y-2*t*e*x*y]
counts['dual_numbers']=lift_control('dual_numbers',Pnil,4,e**2)
# Reduced ring with zero divisors; e and 1-e are orthogonal idempotents.
Pid=[x+t*e*y*y,y]
Qid=[x,y+t*(1-e)*x*x]
TID=comp(Pid,Qid,[x,y],4,e**2-e)
counts['idempotent_ring']=lift_control('idempotent_ring',TID,4,e**2-e)
# Constant reduction can be nonlinear. Removal only uses its actual inverse.
sig0=[x+y*y,y];sig0inv=[x-y*y,y]
full=comp(sig0,target,[x,y],4)
ck('nonlinear_constant_reduction',comp(sig0inv,full,[x,y],4)==target)
# One variable and m=1 boundary diagnostics.
ck('one_variable_Q_derivative',s.diff(x+e+t+t*t*e,x)==1)
ck('one_variable_translation_inverse',s.expand((x+e+t+t*t*e).subs(x,x-e-t-t*t*e))==x)
ck('m1_constant_lift',comp(sig0,sig0inv,[x,y],1)==[x,y])
# Positive-characteristic obstruction is explicitly outside Q-algebra scope.
for p in (2,3,5):
    f=x+t*x**p;g=x-t*x**p
    ck(f'char{p}_inverse',s.Poly(trunc(f.subs(x,g)-x,2),x,t,modulus=p).is_zero)
    ck(f'char{p}_jacobian',s.Poly(s.diff(f,x)-1,x,t,modulus=p).is_zero)
result={'status':'PASS','assertions':len(checks),'checks':checks,'lift_factor_counts':counts,'sympy_version':s.__version__,'scope':'Bounded independent controls only; arbitrary-ring validity is established by the audited polynomial proof.'}
Path(__file__).with_name('independent_results.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='checks'},indent=2))
