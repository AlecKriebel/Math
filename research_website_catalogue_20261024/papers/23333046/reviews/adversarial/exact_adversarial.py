"""Own exact diagnostics, authored from the already sealed adversarial derivation.

No original source program is imported or run.  Symbolic identities and finite
Artinian arithmetic are controls; the full-series and all-natural-map arguments
are proved in DERIVATION.md.  Every guard survives Python optimization.
"""
import argparse
import itertools
import json
import sys
import sympy as s


def require(condition, tag):
    if not condition:
        raise ValueError(tag)


t, u = s.symbols('t u')
field_relation = s.groebner([u*u+u+1], u, t, modulus=2)


def residual(expression):
    numerator, denominator = s.fraction(s.together(expression))
    n = field_relation.reduce(s.Poly(numerator, u, t, modulus=2).as_expr())[1]
    d = field_relation.reduce(s.Poly(denominator, u, t, modulus=2).as_expr())[1]
    require(d != 0, 'symbolic denominator nonzero')
    return n


def fm(a, b):
    # Polynomial product of two two-bit elements, then u^2=u+1.
    c = ((a & 1) * (b & 1)) ^ (((a & 1)*(b >> 1) ^
         (a >> 1)*(b & 1)) << 1) ^ (((a >> 1)*(b >> 1)) << 2)
    return c ^ (7 if c & 4 else 0)


def add(a, b):
    return tuple(x ^ y for x, y in zip(a, b))


def mul(a, b):
    n = len(a)
    result = [0]*n
    for i in range(n):
        for j in range(n-i):
            result[i+j] ^= fm(a[i], b[j])
    return tuple(result)


def matrix(a, b):
    return [[add(mul(a[i][0], b[0][j]), mul(a[i][1], b[1][j]))
             for j in range(2)] for i in range(2)]


def scale(c, a):
    return [[mul(c, v) for v in row] for row in a]


def verify(mutant):
    labels = []
    def eq(a, b, tag):
        require(residual(a-b) == 0, tag)
        labels.append(tag)
    rho = lambda a: t/(1+a*t)
    for a in [0, 1, u, u+1]:
        for b in [0, 1, u, u+1]:
            eq(rho(a).subs(t, rho(b)), rho(a+b), 'additive action '+str((a,b)))
    y = t*t/(1+t)
    eq(y.subs(t, rho(1)), y, 'first invariant coordinate')
    q_expected = y if mutant == 'quotient_action' else y/(1+y)
    eq(y.subs(t, rho(u)), q_expected, 'nontrivial quotient action')
    eq(t*t+y*t+y, 0, 'quadratic coordinate equation')
    eq(s.diff(y,t), t*t/(1+t)**2, 'quotient derivative')
    eq(y*(1+t)**2/(t*t), 1+t, 'regular lift of coefficient y')
    if mutant == 'zero_section':
        require((1+t).subs(t,0) == 0, 'zero-section restriction changes module')
    sigma = rho(1)
    z = t*t/(1+t)
    eq(sigma.subs(t,sigma), t, 'quotient involution')
    eq(z.subs(t,sigma), z, 'second invariant coordinate')
    weight = 1+t if mutant == 'derivation_weight' else (1+t)**2
    eq(weight*sigma, t+t*t, 'module basis y transforms to y+y2')
    eq(weight*sigma**2, t*t, 'module basis y2 fixed')
    eq(weight, 1+t*t, 'full module constant transforms')
    eq(weight*(1+sigma), 1+t, 'full module invariant generator')
    # z is fixed, so these two basis identities extend to all R0=k[[z]],
    # not merely to a finite list of powers of z.
    dm = s.Matrix([[0,0],[1,0]])
    require(dm*dm == s.zeros(2), 'M differential squares to zero')
    require(dm*s.Matrix([1,0]) == s.Matrix([0,1]), 'M explicit primitive')
    labels.append('M kernel=image=R0*(0,1), by solving a=0')
    # All full-module boundaries specialize to zero at z=0, whereas the
    # invariant generator (1,1) does not. Test actual image membership of
    # this specialization, including the deliberately false vanishing claim.
    boundary_at_zero = (t*s.Matrix([[1,1],[1,1]])).subs(t,0)
    generator = s.Matrix([1,1])
    in_image = boundary_at_zero.row_join(generator).rank() == boundary_at_zero.rank()
    require(in_image == (mutant == 'full_H1_zero'),
            'full module has nonzero R0/z class')
    labels.append('full module kernel=R0*(1,1), image=z*R0*(1,1)')
    A = list(itertools.product(range(4), repeat=2))
    B = list(itertools.product(range(4), repeat=3))
    embed = (lambda a: (a[0],a[1],0)) if mutant == 'linear_injection' else (lambda a: (a[0],0,a[1]))
    require(len(set(map(embed,A))) == 16, 'ring injection distinct images')
    for a in A:
        for b in A:
            require(embed(add(a,b)) == add(embed(a),embed(b)), 'injection additive')
            require(embed(mul(a,b)) == mul(embed(a),embed(b)), 'injection multiplicative')
    labels.append('all 256 A pairs: e maps to w2 injective ring map')
    j = (lambda a:a) if mutant == 'fixed_ring' else (lambda a:(a[0],a[1],a[1]^a[2]))
    require(all(j(j(a))==a for a in B), 'cubic automorphism involutive')
    for a in B:
        for b in B:
            require(j(add(a,b))==add(j(a),j(b)), 'cubic automorphism additive')
            require(j(mul(a,b))==mul(j(a),j(b)), 'cubic automorphism multiplicative')
    fixed = [a for a in B if j(a)==a]
    require(set(fixed)=={a for a in B if a[1]==0}, 'fixed ring has no linear coefficient')
    require(len(fixed)==16, 'fixed-ring cardinality')
    labels.append('all 4096 B pairs, 64 elements: j fixed ring k+k*w2')
    zero, one, w, w2 = (0,0,0),(1,0,0),(0,1,0),(0,0,1)
    C = [[add(one,w),zero if mutant=='conjugator_translation' else w],[zero,one]]
    M = lambda d:[[one,d],[one,one]]
    require(matrix(M(w2),C)==scale(add(one,w),matrix(C,M(zero))),
            'injection kills tangent class by explicit conjugacy')
    require(matrix(M(add(w,w2)),C)==scale(add(one,w),matrix(C,M(w))),
            'cubic parameter-shift conjugacy')
    require(matrix(M(w),M(w))==scale(add(one,w),[[one,zero],[zero,one]]),
            'cubic lift is an involution')
    labels.extend(['injection conjugacy','parameter-shift conjugacy','projective involution'])
    # The literal cubic identity need not persist under an unannounced ring change.
    q0,q1,qw,qw2=(0,0,0,0),(1,0,0,0),(0,1,0,0),(0,0,1,0)
    QC=[[add(q1,qw),qw],[q0,q1]]
    QM=lambda d:[[q1,d],[q1,q1]]
    require(matrix(QM(add(qw,qw2)),QC)!=scale(add(q1,qw),matrix(QC,QM(qw))),
            'unannounced quartic ring fails literal parameter-shift identity')
    labels.append('quartic-ring negative boundary detected')
    return {'status':'PASS','optimization':sys.flags.optimize,'mutant':mutant,
            'checks':labels,'listed_checks':len(labels),
            'finite_ring_elements':{'A':16,'B':64,'fixed_B':16},
            'universal_proof':'DERIVATION.md, not an inference from these diagnostics'}


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--mutant',default='none',choices=['none','quotient_action',
        'zero_section','derivation_weight','full_H1_zero','linear_injection',
        'fixed_ring','conjugator_translation'])
    args=parser.parse_args()
    try:
        answer=verify(args.mutant)
    except ValueError as error:
        print(json.dumps({'status':'REJECT','optimization':sys.flags.optimize,
                          'mutant':args.mutant,'tag':str(error)}))
        sys.exit(1)
    print(json.dumps(answer,indent=2))
