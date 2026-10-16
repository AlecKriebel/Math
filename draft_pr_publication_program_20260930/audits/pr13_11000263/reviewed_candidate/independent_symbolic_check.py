#!/usr/bin/env python3
"""Independent symbolic checks of the reviewed Bigelow/Burau audit.
Written for this adversarial review; does not import the candidate verifier.
Requires SymPy. Finite matrix checks supplement the all-index local proof.
"""
import json
from pathlib import Path
import sympy as s

q,u,a,z=s.symbols('q u a z', nonzero=True)
checks=[]
def eq(label,x,y):
    d=x-y
    vals=list(d) if isinstance(d,s.MatrixBase) else [d]
    assert all(s.cancel(v)==0 for v in vals),label
    checks.append(label)

def generator(n,i):
    b=s.eye(n)
    b[i-1:i+1,i-1:i+1]=s.Matrix([[1-u,u],[1,0]])
    return b

p,t=generator(3,1),generator(3,2)
pinv=s.Matrix([[0,1,0],[1/u,1-1/u,0],[0,0,1]])
tinv=s.Matrix([[1,0,0],[0,0,1],[0,1/u,1-1/u]])
eq('block inverse left',pinv*p,s.eye(3))
eq('block inverse right',p*pinv,s.eye(3))
eq('braid relation',p*t*p,t*p*t)
w=s.Matrix([a,-a/u,0])
eq('arbitrary amplitude forward propagation',p*t*w,s.Matrix([0,a,-a/u]))
eq('arbitrary amplitude inverse propagation',pinv*tinv*w,s.Matrix([0,a/u,-a/u**2]))
v1=s.Matrix([1,-1/u,0]); v2=s.Matrix([0,1/u,-1/u**2]); cov=s.Matrix([[-1,1,0]])
x2=q*pinv+(1-q)*s.eye(3)-p
x3=(q**2*(t*p).inv()-p*t)*x2
eq('X2 factorization',x2,(q-u)*v1*cov)
eq('X3 direct word calculation',x3,(q-u)*(q**2-u)*v2*cov)
eq('exceptional R2 local calculation',(q*tinv+(1-q)*s.eye(3)-t)*v1,(q*pinv*tinv-p*t)*v1)
eq('X2 scalar twist',p*x2,-u*x2)
eq('X3 central twist',(p*t)**3*x3,u**3*x3)
eq('explicit X3 entry',x3[1,0],-(q-u)*(q**2-u)/u)
assert s.cancel(x3[1,0]) != 0
checks.append('explicit nonzero X3 entry')

# Independent whole-word product evaluation over the rational-function field.
for n in (4,5):
    b={i:generator(n,i) for i in range(1,n)}
    def prod(ids):
        out=s.eye(n)
        for i in ids: out=out*b[i]
        return out
    x=q*b[1].inv()+(1-q)*s.eye(n)-b[1]
    xall={2:x}
    for k in range(3,n+1):
        x=((q**(k-1))*prod(range(k-1,0,-1)).inv()-prod(range(1,k)))*x
        x=x.applyfunc(s.cancel); xall[k]=x
    for k in range(3,n):
        left=q**(k-1)*prod(range(k,1,-1)).inv()-prod(range(2,k+1))
        right=q**(k-1)*prod(range(k,0,-1)).inv()-prod(range(1,k+1))
        eq(f'n={n} relation R{k}',left*xall[k],right*xall[k])
    eq(f'n={n} u=q cubed kills X4',xall[4].subs(u,q**3),s.zeros(n))
    assert s.cancel(xall[3][1,0].subs(u,q**3))!=0
    checks.append(f'n={n} u=q cubed preserves X3')

xscalar=q/z+1-q-z
first=q/z+1-q-z-q/z**2+z**2
eq('scalar X2 factor',xscalar,(1-z)*(z+q)/z)
eq('scalar R2 coefficient',first,(z**2-q)*(z**2-z+1)/z**2)
eq('scalar R3 coefficient',q**2/z**2-z**2-q**2/z**3+z**3,(z-1)*(q**2+z**5)/z**3)
eq('scalar R4 coefficient',q**3/z**3-z**3-q**3/z**4+z**4,(z-1)*(q**3+z**7)/z**4)
out={'status':'passed','sympy_version':s.__version__,'symbolic_check_count':len(checks),'checks':checks,'nonzero_X3_entry':str(s.factor(x3[1,0])),'scope':'Symbolic local identities with arbitrary amplitude, finite 4/5-strand word checks, twist specialization, and scalar-route factorization; no finite test is asserted to prove all strand counts.'}
Path(__file__).with_name('independent_symbolic_check.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
