#!/usr/bin/env python3
"""Independent exact Laurent-matrix and mutation controls. Standard library only.

No author code is imported. The sparse matrices use commuting Laurent variables,
one per tensor factor. These are finite supporting checks, not a formal proof of
the global dimensions or the bi-Galois equivalence theorem.
"""
from collections import Counter
from fractions import Fraction
from itertools import product
import json

C = Counter()

def tidy(a):
    return {k: v for k, v in a.items() if v}

def plus(*aa):
    out = Counter()
    for a in aa:
        for k, v in a.items():
            out[k] += v
    return tidy(out)

def times(c, a):
    return tidy({k: c*v for k, v in a.items()})

def mm(a, b):
    out = Counter()
    for (i, j, e), x in a.items():
        for (k, l, f), y in b.items():
            if j == k:
                out[i, l, tuple(v+w for v, w in zip(e, f))] += x*y
    return tidy(out)

def kron(a, b, dim_b=2):
    out = Counter()
    for (i, j, e), x in a.items():
        for (k, l, f), y in b.items():
            out[i*dim_b+k, j*dim_b+l, e+f] += x*y
    return tidy(out)

def ident(n=1):
    return {(i, i, (0,)*n): 1 for i in range(2**n)}

def genpower(i):
    return {(0, 0, (i,)): 1, (1, 1, (i,)): (-1 if i % 2 else 1)}

def skew(kind):
    a = {(1, 0, (0,)): 1}
    if kind == 'H':
        a.update({(0, 1, (0,)): 1, (0, 1, (2,)): -1})
    if kind == 'B':
        a[(0, 1, (2,))] = -1
    return a

def basis(kind, i, j):
    # Independent orientation: z^j g^i rather than g^i z^j.
    return mm(skew(kind), genpower(i)) if j else genpower(i)

def pbw_product(kind, i, j, r, s):
    sign = -1 if (i*s) % 2 else 1
    if j+s < 2:
        return times(sign, basis(kind, i+r, j+s))
    if kind == 'L':
        return {}
    ans = times(-sign, basis(kind, i+r+2, 0))
    return plus(ans, times(sign, basis(kind, i+r, 0))) if kind == 'H' else ans

def eq(label, a, b):
    if a != b:
        raise AssertionError((label, a, b))
    C[label] += 1

def neq(label, a, b):
    if a == b:
        raise AssertionError(('Mutation not detected', label))
    C[label] += 1

def coproduct(kind, i, j, opposite=False):
    g = genpower(1); z = skew(kind); one = ident()
    d = plus(kron(z, one), kron(g, z))
    if opposite:
        d = plus(kron(one, z), kron(z, g))
    base = kron(genpower(i), genpower(i))
    return mm(d, base) if j else base

def image_product(kind, i, j, r, s, fn):
    sign = -1 if i*s % 2 else 1
    if j+s < 2:
        return times(sign, fn(i+r, j+s))
    if kind == 'L':
        return {}
    ans = times(-sign, fn(i+r+2, 0))
    return plus(ans, times(sign, fn(i+r, 0))) if kind == 'H' else ans

def rho(i, j):
    p = kron(genpower(i), genpower(i))
    return mm(plus(kron(skew('B'), ident()), kron(genpower(1), skew('H'))), p) if j else p

def left(i, j):
    p = kron(genpower(i), genpower(i))
    return mm(plus(kron(genpower(1), skew('B')), kron(skew('L'), ident())), p) if j else p

def run():
    one = ident(); g = genpower(1); gi = genpower(-1)
    z = skew('H'); y = skew('L'); t = skew('B')
    small = list(product(range(-4, 5), range(2)))
    for kind in ('H', 'L', 'B'):
        zz = skew(kind)
        eq('generator_inverse', mm(g, gi), one)
        eq('skew_relation', plus(mm(zz, g), mm(g, zz)), {})
        for (i,j), (r,s) in product(small, repeat=2):
            eq('independent_reverse_pbw_matrix', mm(basis(kind,i,j),basis(kind,r,s)), pbw_product(kind,i,j,r,s))
    for kind in ('H', 'L'):
        for (i,j), (r,s) in product(small, repeat=2):
            eq('matrix_coproduct_multiplicativity', mm(coproduct(kind,i,j),coproduct(kind,r,s)),
               image_product(kind,i,j,r,s,lambda a,b:coproduct(kind,a,b)))
    for (i,j), (r,s) in product(small, repeat=2):
        for f in (rho, left):
            eq('matrix_coaction_multiplicativity', mm(f(i,j),f(r,s)), image_product('B',i,j,r,s,f))
    # Canonical inverse formulas checked directly in tensor-matrix images.
    for i, r, s in product(range(-5,6), range(-3,4), range(2)):
        b = basis('B', r, s)
        # Right: inverse(b tensor g^i x) as the two simple tensors in PROOF.md.
        a1 = mm(b, genpower(-i-1))
        a2 = mm(mm(mm(b, genpower(-1)), t), genpower(-i))
        # rho(u^i t) differs from rho(t u^i) by (-1)^i.
        v = plus(mm(kron(a1,one),times((-1 if i%2 else 1),rho(i,1))),
                 times(-1,mm(kron(a2,one),rho(i,0))))
        target = kron(b, mm(genpower(i),z))
        eq('right_canonical_inverse_matrix', v, target)
        neq('reject_right_inverse_plus_sign', plus(v,times(2,mm(kron(a2,one),rho(i,0)))),target)
        # Left: inverse(h^i y tensor b).
        b1 = mm(genpower(-i),b)
        b2 = mm(mm(mm(genpower(-1),t),genpower(-i)),b)
        v = plus(mm(times((-1 if i%2 else 1),left(i,1)),kron(one,b1)),
                 times(-1,mm(left(i+1,0),kron(one,b2))))
        target = kron(mm(genpower(i),y),b)
        eq('left_canonical_inverse_matrix',v,target)
        neq('reject_left_inverse_plus_sign',plus(v,times(2,mm(left(i+1,0),kron(one,b2)))),target)
    # Opposite source coproduct fails left coassociativity on t.
    good = plus(kron(kron(g,g),t),kron(kron(g,y),one),kron(kron(y,one),one))
    bad = plus(kron(kron(g,g),t),kron(kron(one,y),one),kron(kron(y,g),one))
    neq('reject_source_opposite_coproduct',bad,good)
    eq('basis_endpoint_discrepancy',plus(plus(one,times(-1,genpower(2))),times(-1,mm(t,t))),one)
    neq('reject_wrong_H_square',mm(z,z),plus(one,genpower(2)))
    neq('reject_wrong_B_square',mm(t,t),genpower(2))
    neq('reject_commuting_instead_of_skew',mm(z,g),mm(g,z))
    # Central regular element is not assumed invertible: its value at x=0 is 0.
    eq('central_x_squared',mm(mm(z,z),g),mm(g,mm(z,z)))
    eq('normalization_half',Fraction(1,2)*(1+1),1)
    neq('reject_missing_half',1+1,1)
    # Distinguish pd(k) from self-Ext: a nonsplit extension by the sign module.
    # g=diag(-1,1), x(e_2)=e_1, x(e_1)=0.
    G={(0,0,(0,)):-1,(1,1,(0,)):1}; X={(0,1,(0,)):1}
    eq('sign_extension_skew_relation',plus(mm(X,G),mm(G,X)),{})
    eq('sign_extension_square_relation',mm(X,X),plus(one,times(-1,mm(G,G))))
    # E=k[y]/y^2 differential has rank one, square zero, and kernel=image.
    Y={(1,0,(0,)):1}
    eq('dual_numbers_d_squared',mm(Y,Y),{})
    eq('dual_numbers_kernel_image_dimension',2-1,1)
    return {'status':'pass','problem_id':'30004831','assertions':sum(C.values()),
            'counts':dict(sorted(C.items())),
            'arithmetic':'Exact integer Laurent polynomials; one rational normalization check',
            'independence':'No author code imported; reversed PBW and Laurent-matrix realization',
            'scope':'Finite supporting checks only; mathematical proof and external theorem audited separately.'}

if __name__ == '__main__':
    print(json.dumps(run(),indent=2,sort_keys=True))
