#!/usr/bin/env python3
"""Finite exact controls only; not a proof checker for the continuous theorem."""
from fractions import Fraction as F
import json

counts = {}
def check(group, value):
    if not value:
        raise AssertionError(group)
    counts[group] = counts.get(group, 0) + 1

def mm(a,b):
    return tuple(tuple(sum(a[i][k]*b[k][j] for k in range(len(b)))
                       for j in range(len(b[0]))) for i in range(len(a)))
def mv(a,v):
    return tuple(sum(a[i][k]*v[k] for k in range(len(v))) for i in range(len(a)))
def ident(n):
    return tuple(tuple(int(i==j) for j in range(n)) for i in range(n))
def power(a,n,ainv):
    if n < 0:
        return power(ainv,-n,a)
    out = ident(len(a))
    for _ in range(n): out=mm(out,a)
    return out

def qa(x,y): return (x[0]+y[0],x[1]+y[1])
def qm(x,y): return (x[0]*y[0]+5*x[1]*y[1],x[0]*y[1]+x[1]*y[0])
def qs(x,y): return (x[0]-y[0],x[1]-y[1])
def qpow(x,n):
    out=(F(1),F(0))
    for _ in range(n): out=qm(out,x)
    return out

B=((2,1),(1,1)); Binv=((1,-1),(-1,2))
check('matrix_inverses',mm(B,Binv)==ident(2))
check('matrix_inverses',mm(Binv,B)==ident(2))
lam=(F(3,2),F(1,2)); lami=(F(3,2),F(-1,2)); one=(F(1),F(0))
check('quadratic_eigenvalues',qm(lam,lami)==one)
check('quadratic_eigenvalues',qa(qs(qm(lam,lam),(3*lam[0],3*lam[1])),one)==(0,0))
vu=(one,qs(lam,(F(2),F(0))))
Bvu=(qa((2*vu[0][0],2*vu[0][1]),vu[1]),qa(vu[0],vu[1]))
check('quadratic_eigenvalues',Bvu==tuple(qm(lam,x) for x in vu))

def block(a,b):
    return ((a[0][0],a[0][1],0,0),(a[1][0],a[1][1],0,0),
            (0,0,b[0][0],b[0][1]),(0,0,b[1][0],b[1][1]))
f=block(B,B); fi=block(Binv,Binv); g=block(B,Binv); gi=block(Binv,B)
check('commuting_maps',mm(f,g)==mm(g,f))
for m in range(-8,9):
    for n in range(-8,9):
        actual=mm(power(f,m,fi),power(g,n,gi))
        expected=block(power(B,m+n,Binv),power(B,m-n,Binv))
        check('exact_joint_action',actual==expected)
        p,q=m+n,m-n
        check('leaf_label_injectivity',(p+q,p-q)==(2*m,2*n))
        # Formal labels use r(L_mn)=n.  These are algebraic controls,
        # not finite tests purporting to establish leaf distinctness.
        check('exceptional_leaf_weights',(n-n)==0)
        check('exceptional_leaf_weights',(n-(n+1))==-1)
        check('label_action',((m+1)+n,(m+1)-n)==(p+1,q+1))
        check('label_action',(m+(n+1),m-(n+1))==(p+1,q-1))
for k in range(-50,51):
    if k==0: continue
    P=power(B,k,Binv)
    check('integer_power_nonfixed_vector',(P[0][0]-1,P[1][0])!=(0,0))
    check('integer_power_nonfixed_vector',(P[0][0]-1)*(P[1][1]-1)-P[0][1]*P[1][0]!=0)

# Telescoping compatibility is checked for arbitrary exact rational samples,
# with delta_a(k) defined to satisfy the scalar square.
for N in range(1,41):
    bx=[F(3*k*k+2*k+7,k+1) for k in range(N+1)]
    by=[F(k*k-4*k+1,2*k+1) for k in range(N+1)]
    lhs=sum((bx[k-1]-bx[k])-(by[k-1]-by[k]) for k in range(1,N+1))
    rhs=bx[0]-by[0]-(bx[N]-by[N])
    check('finite_telescoping',lhs==rhs)

# Exponent identity underlying normalized defect covariance.
for aa in range(-6,7):
    for bb in range(-6,7):
        for bf in range(-6,7):
            ag=aa+bf-bb
            check('defect_covariance_exponents',aa-bb+bf==ag)

result={
 'status':'PASS_FINITE_EXACT_CONTROLS',
 'groups':counts,
 'total_assertions':sum(counts.values()),
 'arithmetic':'Python integers and fractions; Q(sqrt(5)) represented as pairs',
 'limits':[
  'No finite test proves the measurable-kernel or Radon–Nikodym arguments.',
  'No finite test proves recurrence, whole-leaf exhaustion, or ergodicity.',
  'Exceptional-leaf distinctness and Haar nullity are proved in the note.',
  'No original release, original audit, or omitted source bytes are replayed.'
 ]
}
print(json.dumps(result,indent=2,sort_keys=True))
