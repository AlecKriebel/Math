#!/usr/bin/env python3
"""Exact checks for the authored partial results; standard library only.

No surface diffeomorphism, symplectomorphism, or Lagrangian realization is
computed. The finite Hurwitz example is independent of Horikawa monodromy.
"""
from collections import deque
from fractions import Fraction
from math import gcd
import json

def require(condition, message):
    """Always-active check, including under Python -O and -OO."""
    if not condition:
        raise RuntimeError(message)


MOD = 3
I = (1, 0, 0, 1)
NEG_I = (2, 0, 0, 2)
A = (1, 1, 0, 1)
B = (1, 0, 1, 1)
P = (0, 1, 2, 0)


def mul(x, y):
    a, b, c, d = x
    e, f, g, h = y
    return ((a*e+b*g)%3, (a*f+b*h)%3,
            (c*e+d*g)%3, (c*f+d*h)%3)


def neg(x):
    return tuple((-z)%3 for z in x)


def inv(x):
    a, b, c, d = x
    require((a*d-b*c)%3 == 1, 'check failed: (a*d-b*c)%3 == 1')
    return (d, (-b)%3, (-c)%3, a)


def conj(x, y):
    return mul(mul(x, y), inv(x))


def product(xs):
    out = I
    for x in xs:
        out = mul(out, x)
    return out


def closure(gens):
    seen = {I}
    todo = deque([I])
    while todo:
        x = todo.popleft()
        for g in gens:
            y = mul(x, g)
            if y not in seen:
                seen.add(y)
                todo.append(y)
    return seen


def quotient(x):
    return min(x, neg(x))


def qmul(x, y):
    return quotient(mul(x, y))


def qinv(x):
    return quotient(inv(x))


def qconj(x, y):
    return qmul(qmul(x, y), qinv(x))


def qproduct(xs):
    return quotient(product(xs))


def order_three_lift(x):
    choices = [y for y in (x, neg(x)) if product([y]*3) == I]
    require(len(choices) == 1 and choices[0] != I, 'check failed: len(choices) == 1 and choices[0] != I')
    return choices[0]


def hurwitz_orbit(t, group):
    """Braid group, plus all simultaneous inner conjugations in G."""
    seen = {t}
    todo = deque([t])
    while todo:
        x = todo.popleft()
        neighbors = []
        for i in range(len(x)-1):
            a, b = x[i:i+2]
            neighbors.append(x[:i]+(qconj(a,b),a)+x[i+2:])
            neighbors.append(x[:i]+(b,qconj(qinv(b),a))+x[i+2:])
        for g in group:
            neighbors.append(tuple(qconj(g,z) for z in x))
        for y in neighbors:
            if y not in seen:
                seen.add(y)
                todo.append(y)
    return seen


def check_finite_example():
    group = closure([A,B])
    require(len(group) == 24 and P in group and NEG_I in group, 'check failed: len(group) == 24 and P in group and NEG_I in group')
    qgroup = {quotient(x) for x in group}
    require(len(qgroup) == 12, 'check failed: len(qgroup) == 12')
    C = mul(A,B)
    require(mul(C,C) == NEG_I and mul(P,P) == NEG_I, 'check failed: mul(C,C) == NEG_I and mul(P,P) == NEG_I')
    require(conj(P,C) == neg(C), 'check failed: conj(P,C) == neg(C)')
    t = tuple(map(quotient,(A,B,inv(B),inv(A))))
    tp = tuple(map(quotient,(conj(P,A),conj(P,B),inv(B),inv(A))))
    require(qproduct(t) == qproduct(tp) == quotient(I), 'check failed: qproduct(t) == qproduct(tp) == quotient(I)')
    require(product(map(order_three_lift,t)) == I, 'check failed: product(map(order_three_lift,t)) == I')
    require(product(map(order_three_lift,tp)) == NEG_I, 'check failed: product(map(order_three_lift,tp)) == NEG_I')
    orbit_t = hurwitz_orbit(t,qgroup)
    orbit_tp = hurwitz_orbit(tp,qgroup)
    require((len(orbit_t), len(orbit_tp)) == (216, 144),
            'check failed: complete orbit cardinalities must be 216 and 144')
    require(orbit_t.isdisjoint(orbit_tp), 'check failed: orbit_t.isdisjoint(orbit_tp)')
    for x in orbit_t:
        require(product(map(order_three_lift,x)) == I, 'check failed: product(map(order_three_lift,x)) == I')
    for x in orbit_tp:
        require(product(map(order_three_lift,x)) == NEG_I, 'check failed: product(map(order_three_lift,x)) == NEG_I')
    return {
        'upstairs_group_order':len(group), 'quotient_group_order':len(qgroup),
        'tuple_product_in_quotient':'identity for both',
        'canonical_lift_products':['I','-I'],
        'hurwitz_and_conjugation_orbit_sizes':[len(orbit_t),len(orbit_tp)],
        'orbits_disjoint':True,
        'scope':'finite quotient example only, not a Horikawa monodromy computation',
    }


def check_parameters(r):
    d=8*r-8
    e=40*r-4
    sig=-24*r
    pg=4*r-2
    bp=8*r-3
    bm=32*r-3
    require(12*(pg+1)-d == e, 'check failed: 12*(pg+1)-d == e')
    require(Fraction(d-2*e,3) == sig, 'check failed: Fraction(d-2*e,3) == sig')
    require(bp+bm == e-2 and bp-bm == sig, 'check failed: bp+bm == e-2 and bp-bm == sig')
    # Gram matrices in the report, in the stated bases.
    gx=((0,2),(2,0))
    gy=((-4*r,2),(2,0))
    saturated=((-r,1),(1,0))
    det=lambda m:m[0][0]*m[1][1]-m[0][1]*m[1][0]
    require(det(gx)==det(gy)==-4 and det(saturated)==-1, 'check failed: det(gx)==det(gy)==-4 and det(saturated)==-1')
    kx=(1,2*r-2)
    ky=(2,3*r-2)
    square=lambda m,v:sum(v[i]*m[i][j]*v[j] for i in range(2) for j in range(2))
    require(square(gx,kx)==square(saturated,ky)==d, 'check failed: square(gx,kx)==square(saturated,ky)==d')
    require(-r*ky[0]+ky[1]==r-2, 'check failed: -r*ky[0]+ky[1]==r-2')
    require(gcd(*ky)==(1 if r%2 else 2), 'check failed: gcd(*ky)==(1 if r%2 else 2)')
    require(2-2*(20*r-5)==2+(2-2*(20*r-4))==12-40*r, 'check failed: 2-2*(20*r-5)==2+(2-2*(20*r-4))==12-40*r')
    # Blowup grid: six sections, 4r fibers, 24r A_1 nodes.
    require(Fraction(-6,2)==-3, 'check failed: Fraction(-6,2)==-3')
    require(-3+1==-2, 'check failed: -3+1==-2')
    # Formal characteristic vector and possible sphere class in the odd lattice.
    kval=[3]*(4*r-1)+[1]*(4*r-2)+[1]*(32*r-3)
    signs=[1]*bp+[-1]*bm
    av=[0]*len(kval)
    for j in range(r-1): av[bp+j]=-1
    av[bp+r-1]=1
    require(sum(s*k*k for s,k in zip(signs,kval))==d, 'check failed: sum(s*k*k for s,k in zip(signs,kval))==d')
    require(sum(s*a*a for s,a in zip(signs,av))==-r, 'check failed: sum(s*a*a for s,a in zip(signs,av))==-r')
    require(sum(s*a*k for s,a,k in zip(signs,av,kval))==r-2, 'check failed: sum(s*a*k for s,a,k in zip(signs,av,kval))==r-2')
    pencils=[]
    for k in (1,2,4,8):
        genus=1+k*(k+1)*d//2
        base=k*k*d
        nodes=e+d*(3*k*k+2*k)
        require(e+base==4-4*genus+nodes, 'check failed: e+base==4-4*genus+nodes')
        pencils.append({'k':k,'genus':genus,'base_points':base,'nodes':nodes})
    return {'r':r,'K_squared':d,'p_g':pg,'euler':e,'signature':sig,
            'b2_plus':bp,'b2_minus':bm,'canonical_divisibility_Y':gcd(*ky),
            'complement_absolute_determinants':[4,1],
            'pencil_arithmetic':pencils}


def main():
    params=[check_parameters(r) for r in range(2,32)]
    finite=check_finite_example()
    require(params[1]['pencil_arithmetic'][0]=={'k':1,'genus':17,'base_points':16,'nodes':196}, "check failed: params[1]['pencil_arithmetic'][0]=={'k':1,'genus':17,'base_points':16,'nodes':196}")
    print(json.dumps({'status':'passed','parameter_checks':params,
                      'finite_partial_conjugation_counterexample':finite,
                      'limits':['Finite tests supplement symbolic proofs; they do not prove all parameters.',
                                'No source text, external dataset, or random input is used.',
                                'No full solution of KP-4.94 is asserted.']},indent=2))

if __name__=='__main__':
    main()
