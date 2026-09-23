#!/usr/bin/env python3
"""Exact supplementary checks from preprint review round 2, including integration correction."""
from fractions import Fraction as F
from itertools import product
from math import factorial


def polar(p, vectors):
    d = len(vectors)
    total = F(0)
    for signs in product((-1, 1), repeat=d):
        point = tuple(sum(s * v[j] for s, v in zip(signs, vectors))
                      for j in range(len(vectors[0])))
        weight = 1
        for s in signs:
            weight *= s
        total += weight * p(point)
    return total / (2**d * factorial(d))


def check(label, d, p, z1, z2):
    values = [polar(p, [z1] * k + [z2] * (d-k))
              for k in range(d+1)]
    assert values[0] == p(z2) and values[d] == p(z1)
    gaps = [values[d]**k * values[0]**(d-k) - values[k]**d
            for k in range(d+1)]
    assert all(v > 0 for v in values)
    assert gaps[0] == gaps[d] == 0
    assert all(g > 0 for g in gaps[1:d])
    assert z1[0] * z2[1] - z1[1] * z2[0] != 0
    eye = [(F(1), F(0)), (F(0), F(1))]
    for k in range(d-1):
        rest = [z1] * k + [z2] * (d-2-k)
        B = [[polar(p, rest + [a, b]) for b in eye] for a in eye]
        assert B[0][0] > 0
        assert B[0][0] * B[1][1] - B[0][1]**2 > 0
    print(label, "PASS", len(values), "classes,", d-1, "slices")


for exponent in (1, 8, 80):
    delta = F(1, 10**exponent)
    h = F(1, 10**((exponent+1)//2 + 2))
    p = lambda z, delta=delta: ((z[0]**2-z[1]**2)**2
                               + 2*delta*z[0]**2*z[1]**2)
    check("nonconvex delta=1e-" + str(exponent), 4, p,
          (1+h, 1-h), (F(1), F(1)))

for lam in (F(0), F(1, 10**40), F(10**40)):
    p = lambda z, lam=lam: (z[0]**2+z[1]**2)**2 + lam*z[1]**4
    h = F(1, 10**12) if lam > 1 else F(1, 8)
    check("degenerate minimum lambda=" + str(lam), 4, p,
          (F(1), h), (F(1), F(0)))

lam = F(10**80)
p = lambda z: z[0]**2 + lam*z[1]**2
check("anisotropic quadratic lambda=1e80", 2, p,
      (F(1), F(1, 10**42)), (F(1), F(0)))

# For z1=(1+h,1-h), z2=(1,1), the k=2 tensor value below
# follows by expanding p_delta(t*z1+s*z2) and dividing by 6.
h = F(1, 4)
for delta in (F(1, 10**8), F(1, 10**80)):
    p0 = 2*delta
    p1 = 2*delta + (16-4*delta)*h*h + 2*delta*h**4
    n2 = 2*delta + (16-4*delta)*h*h/6
    actual_p = lambda z, delta=delta: ((z[0]**2-z[1]**2)**2
                                       + 2*delta*z[0]**2*z[1]**2)
    z1, z2 = (1+h, 1-h), (F(1), F(1))
    assert p1 == actual_p(z1)
    assert n2 == polar(actual_p, [z1, z1, z2, z2])
    assert p0**2 * p1**2 - n2**4 < 0
print("fixed-perturbation negative controls PASS")

p0 = lambda z: (z[0]**2-z[1]**2)**2
assert p0((F(1), F(1))) == 0
print("excluded nonnegative endpoint PASS")
