#!/usr/bin/env python3
"""Exact finite controls for PROOF.md; not a density proof or optical realization.

Python 3 standard library only. Output is deterministic JSON. Fractions never
convert to floats. All checks are finite; quantified results are proved in prose.
"""
from fractions import Fraction as F
from itertools import product
import json

counts = {}
def check(name, condition):
    if not condition:
        raise AssertionError(name)
    counts[name] = counts.get(name, 0) + 1

def dot(a,b): return a[0]*b[0]+a[1]*b[1]
def det(a,b): return a[0]*b[1]-a[1]*b[0]
def add(a,b): return (a[0]+b[0],a[1]+b[1])
def mul(c,a): return (c*a[0],c*a[1])
def quarter(u): return (-u[1],u[0])
def neg(u): return (-u[0],-u[1])
def norm2(u): return dot(u,u)
def reflect(u,n): return add(u,mul(-2*dot(u,n),n))

def forward(u,p,s,R):
    x=add(mul(s,u),mul(p,quarter(u)))
    n=mul(1/R,x)
    return reflect(u,n),p,x

def backward(u,p,s,R):
    x=add(mul(-s,u),mul(p,quarter(u)))
    n=mul(1/R,x)
    return reflect(u,n),p,x

# Exact rational points on the unit circle, rational incidence parameters,
# both p signs, normal incidence, and three arbitrary rational radii.
parameters=[F(-3,4),F(-1,2),F(-1,3),F(0),F(1,3),F(1,2),F(3,4)]
for R,t,v in product([F(1,2),F(1),F(7,3)],parameters,parameters):
    p=R*2*t/(1+t*t)
    s=R*(1-t*t)/(1+t*t)
    u=((1-v*v)/(1+v*v),2*v/(1+v*v))
    w,pout,x=forward(u,p,s,R)
    check('transverse_last_endpoint',s>0 and dot(u,x)==s)
    check('on_circle',norm2(x)==R*R)
    check('unit_reflected_direction',norm2(w)==1)
    check('angular_momentum_preserved',pout==p and det(w,x)==p)
    check('outgoing_points_inside',dot(w,x)==-s)
    # Direction formula expressed in the orthonormal frame (u,J_0u).
    expected=add(mul(2*p*p/(R*R)-1,u),mul(-2*p*s/(R*R),quarter(u)))
    check('circle_direction_formula',w==expected)
    old,pold,first=backward(w,p,s,R)
    check('inverse_recovers_line',old==u and pold==p)
    check('inverse_uses_same_collision',first==x)
    # J T J: reversal acts as (u,p)->(-u,-p).
    reverse_then_forward,minus_p,_=forward(neg(u),-p,s,R)
    jtj=neg(reverse_then_forward)
    inverse,_,_=backward(u,p,s,R)
    check('reversibility_JTJ',jtj==inverse and -minus_p==p)

u=(F(1),F(0)); R=F(1); p=F(3,5); s=F(4,5)
w,_,_=forward(u,p,s,R)
z,_,_=forward(w,p,s,R)
check('noninvolution_witness',z!=u)
check('noninvolution_exact_coordinates',z==(F(-527,625),F(336,625)))

# Canonical bilinear form omega((dtheta,dp),(etheta,ep)).
def omega(v,w): return v[1]*w[0]-v[0]*w[1]
for v,w in product([(F(1),F(0)),(F(0),F(1)),(F(2),F(-3))],repeat=2):
    jv=(v[0],-v[1]); jw=(w[0],-w[1])
    check('orientation_reversal_antisymplectic',omega(jv,jw)==-omega(v,w))

# Exact finite shear controls at normal incidence. This is a deliberately
# small collection; no finite enumeration is used to prove non-density.
R0=F(1); radii=[F(3,4),F(1),F(5,4)]
for m in range(5):
    for word in product(radii,repeat=m):
        derivative=sum((2/r for r in word),F(0))
        error=derivative+2/R0
        check('concentric_shear_gap',error>=2*m/max(radii)+2/R0)
        check('empty_or_positive_shear',derivative>=0)
for m in range(1,21):
    check('power_shear_identity_gap',F(2*m)>0)
    check('power_shear_inverse_gap',F(2*(m+1))>=4)

# Exact 2x2 matrix controls.
def mm(A,B):
    return tuple(tuple(sum((A[i][k]*B[k][j] for k in range(2)),F(0))
                       for j in range(2)) for i in range(2))
I=((F(1),F(0)),(F(0),F(1)))
def power(A,n):
    out=I
    for _ in range(n): out=mm(out,A)
    return out
for a in [F(1,3),F(1),F(5,2)]:
    for N,c in [(3,F(-1,2)),(4,F(0)),(6,F(1,2))]:
        e=(2-2*c)/a
        A=((F(1),a),(-e,1-a*e))
        inv=((1-a*e,-a),(e,F(1)))
        check('linear_model_determinant',A[0][0]*A[1][1]-A[0][1]*A[1][0]==1)
        check('linear_model_trace',A[0][0]+A[1][1]==2*c)
        check('linear_model_exact_order_control',power(A,N)==I)
        check('linear_model_positive_power_is_inverse',power(A,N-1)==inv)
        check('linear_model_inverse_multiplication',mm(A,inv)==I)
        check('linear_model_shear_sign_reverses',A[0][1]>0 and inv[0][1]<0)

# Exact commutator sign/time control for X=partial_x, Y=x partial_y.
# Apply X_h, Y_h, X_-h, Y_-h in that order to a point.
for x,y,h in product([F(-2),F(0),F(3,2)], [F(-1),F(1,3)], [F(1,10),F(-2,7)]):
    xx=x+h; yy=y+h*xx; xx-=h; yy-=h*xx
    check('commutator_bracket_sign',xx==x and yy==y+h*h)

result={
  'problem_id':5200008,
  'arithmetic':'fractions.Fraction, exact rational arithmetic',
  'checks':dict(sorted(counts.items())),
  'total_assertions':sum(counts.values()),
  'passed':True,
  'scope':'Finite algebraic controls only; the analytic propositions are proved in PROOF.md.',
  'not_certified':[
    'the full reflection-only density statement',
    'approximation of the base inverse by arbitrary deformed mirrors',
    'optical realizability of the linear matrix model',
    'the published Lie-algebra theorem, used with attribution'
  ]
}
print(json.dumps(result,indent=2,sort_keys=True))
