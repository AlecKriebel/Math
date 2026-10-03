#!/usr/bin/env python3
"""Exact algebra checks for KP-5.17 examples. Not a universal proof verifier."""
import json
from pathlib import Path
from fractions import Fraction as F

# Sparse Q[p,x,y,c,e], with x=sin(q), y=cos(q).
N = 5
ZERO = (0,) * N

def const(a):
    a = F(a)
    return {ZERO: a} if a else {}

def var(j):
    m = list(ZERO); m[j] = 1
    return {tuple(m): F(1)}

def add(*polys):
    out = {}
    for a in polys:
        for m, coefficient in a.items():
            out[m] = out.get(m, F(0)) + coefficient
    return {m: a for m, a in out.items() if a}

def scale(a, k):
    return {m: v * F(k) for m, v in a.items() if v * F(k)}

def mul(a, b):
    out = {}
    for m, u in a.items():
        for n, v in b.items():
            key = tuple(i+j for i, j in zip(m,n))
            out[key] = out.get(key, F(0)) + u*v
    return {m: a for m, a in out.items() if a}

def diff(a, j):
    out = {}
    for m, u in a.items():
        if m[j]:
            n = list(m); n[j] -= 1
            out[tuple(n)] = u*m[j]
    return out

def reduce_circle(a):
    # x^2=1-y^2. Unique remainder of x degree <=1.
    out = {}
    stack = list(a.items())
    while stack:
        m, u = stack.pop()
        if m[1] >= 2:
            n=list(m); n[1]-=2
            stack.append((tuple(n),u))
            n[2]+=2
            stack.append((tuple(n),-u))
        else:
            out[m] = out.get(m,F(0))+u
    return {m:v for m,v in out.items() if v}

def sub(a,b): return add(a,scale(b,-1))
def sq(a): return mul(a,a)
def dq(a): return sub(mul(y,diff(a,1)),mul(x,diff(a,2)))

def substitute(a,j,value):
    out={}
    for m,u in a.items():
        n=list(m); power=n[j]; n[j]=0
        key=tuple(n); out[key]=out.get(key,F(0))+u*F(value)**power
    return {m:v for m,v in out.items() if v}

checks=[]
def eq(label,a,b):
    assert not reduce_circle(sub(a,b)), label
    checks.append(label)
def truth(label, value):
    assert value, label
    checks.append(label)

one=const(1)
p,x,y,c,e=(var(j) for j in range(N))
a,b,k=F(1,8),F(1,2),F(8,9)
ends={}
for s in (-1,1):
    w=add(const(a),scale(x,s*b))
    U=add(scale(y,-s*F(7,18)),scale(mul(x,y),F(1,9)))
    wp=dq(w)
    A=mul(p,sub(one,wp)); B=scale(w,-1)
    phi=add(scale(sq(p),F(1,2)),mul(sub(one,scale(sq(p),F(1,4))),U))
    eq(f'{s}: derivative of U',dq(U),mul(w,sub(one,scale(w,k))))
    eq(f'{s}: d lambda equals omega',sub(diff(A,0),dq(B)),one)
    eq(f'{s}: phi_p',diff(phi,0),mul(p,sub(one,scale(U,F(1,2)))))
    derivative=add(mul(diff(phi,0),A),mul(dq(phi),w))
    claimed=add(mul(sq(p),mul(sub(one,scale(U,F(1,2))),sub(one,wp))),mul(sub(one,scale(sq(p),F(1,4))),mul(sq(w),sub(one,scale(w,k)))))
    eq(f'{s}: Lyapunov identity',derivative,claimed)
    eq(f'{s}: boundary p=2',substitute(phi,0,2),const(2))
    eq(f'{s}: boundary p=-2',substitute(phi,0,-2),const(2))
    eq(f'{s}: interior maximum factorization',sub(const(2),phi),mul(sub(one,scale(sq(p),F(1,4))),sub(const(2),U)))
    eq(f'{s}: Hessian q at critical points',substitute(dq(dq(U)),1,-s*F(1,4)),scale(y,s*F(1,2)))
    ends[s]=(A,B,U,w)

plus,minus=ends[1],ends[-1]
eq('midpoint radial field',scale(add(plus[0],minus[0]),F(1,2)),p)
eq('midpoint angular field',scale(add(plus[3],minus[3]),F(1,2)),const(a))
# lambda_plus-lambda_minus = -d(p sin q).
Fprimitive=scale(mul(p,x),-1)
eq('exact difference dq coefficient',sub(plus[0],minus[0]),dq(Fprimitive))
eq('exact difference dp coefficient',sub(plus[1],minus[1]),diff(Fprimitive,0))
for j,name in ((2,'U'),(3,'w')):
    # q -> q+pi negates x,y; monomial parity gives exact substitution.
    rotated={m:v*((-1)**(m[1]+m[2])) for m,v in plus[j].items()}
    eq('pi rotation of '+name,rotated,minus[j])

truth('w lower bound',a-b==F(-3,8))
truth('w upper bound',a+b==F(5,8))
truth('U coefficient absolute bound',F(7,18)+F(1,18)==F(4,9))
truth('1-kw lower',1-k*F(5,8)==F(4,9))
truth('1-kw upper',1-k*F(-3,8)==F(4,3))
truth('radial phi lower',1-F(4,9)/2==F(7,9))
truth('radial phi upper',1+F(4,9)/2==F(11,9))
truth('Lyapunov p-square coefficient',F(7,18)-F(1,9)*F(25,64)==F(199,576))
truth('uniform Lyapunov p bound',F(199,576)>F(1,3))
truth('uniform Lyapunov angular bound',F(4,9)>F(1,3))
truth('norm p bound',F(9,4)+F(121,81)<4)
truth('norm angular bound',1+F(16,9)<4)
truth('delta',F(1,3)/4==F(1,12))
truth('critical cos-square',1-F(1,4)**2==F(15,16))
truth('critical Hessian-square',F(1,4)*F(15,16)==F(15,64))
truth('midpoint normalized period',2/a==16)

r=sub(p,c)
A=mul(r,add(one,mul(e,y)))
B=mul(e,x)
phi=add(scale(sq(r),F(1,2)),mul(e,y))
eq('cohomology family d lambda',sub(diff(A,0),dq(B)),one)
eq('cohomology family contraction dp',B,mul(e,x))
D=add(mul(diff(phi,0),A),mul(dq(phi),scale(B,-1)))
eq('cohomology family Lyapunov derivative',D,add(mul(sq(r),add(one,mul(e,y))),mul(sq(e),sq(x))))
eq('cohomology derivative in c, dq',diff(A,3),scale(add(one,mul(e,y)),-1))
eq('cohomology derivative in c, dp',diff(B,3),{})
eq('cohomology exact correction',sub(diff(A,3),const(-1)),dq(scale(mul(e,x),-1)))

result={
    'problem_id':3024,
    'status':'PASS',
    'exact_assertions':len(checks),
    'arithmetic':'Python standard library Fraction; exact polynomial identities modulo sin(q)^2+cos(q)^2=1',
    'checks':checks,
    'scope':'Explicit algebra and rational bounds only; no universal homotopy claim, numerical search, or external-theorem verification.'
}
output=json.dumps(result,indent=2,ensure_ascii=False)+'\n'
(Path(__file__).resolve().parent/'verification.json').write_text(output)
print(output,end='')
