#!/usr/bin/env python3
# Reader edition: explicit runtime checks; results go only to stdout.
"""Exact controls for the authored local calculations, not the proofs."""
import itertools
import json
from pathlib import Path
import sympy as sp
x, y, z = sp.symbols('x y z')
p = x * (x - z)
q = y * (y - z)
r = (x - y) ** 2 - z ** 2
b = 3 * x - y - z
c = y - x
h1 = sp.Matrix([p * (-x + 3 * y - z), q * (3 * x - y - z)])
h2 = sp.Matrix([-p * q, -p * q])
h3 = sp.Matrix([-p * r, 0])
a = -3 * x * y + x * z + 3 * y ** 2 + z ** 2
d = y * (x - y - z)
e = z - x - y
f1 = sp.Matrix([-y * (x - z) * (x - y - z)] * 2)
f2 = sp.Matrix([y * (-2 * x ** 2 + 3 * x * y + 3 * x * z - y ** 2 - 3 * z ** 2), (x - z) * a])
f3 = sp.Matrix([y * (y - z) * r, 0])

def vanishes(poly):
    return sp.expand(poly) == 0

def divisible(poly, div):
    return sp.Poly(poly, x, y, z).rem(sp.Poly(div, x, y, z)).is_zero

def mutual_ideal_equal(left, right, modulus):
    kw = {'modulus': modulus} if modulus else {'domain': sp.QQ}
    gl = sp.groebner(left, x, y, z, order='lex', **kw)
    gr = sp.groebner(right, x, y, z, order='lex', **kw)
    return all((gl.reduce(f)[1] == 0 for f in right)) and all((gr.reduce(f)[1] == 0 for f in left))

def standard_monomials(gens, modulus):
    kw = {'modulus': modulus} if modulus else {'domain': sp.QQ}
    gb = sp.groebner(gens, x, y, z, order='lex', **kw)
    leading = [tuple(pol.LM(order='lex').exponents) for pol in gb.polys]
    bounds = []
    for i in range(3):
        pure = [mon[i] for mon in leading if mon[i] > 0 and sum(mon) == mon[i]]
        if not pure:
            raise RuntimeError('Quotient is not certified zero-dimensional')
        bounds.append(min(pure))
    std = []
    for exponents in itertools.product(*(range(n) for n in bounds)):
        if not any((all((a >= b for a, b in zip(exponents, mon))) for mon in leading)):
            std.append(str(x ** exponents[0] * y ** exponents[1] * z ** exponents[2]))
    return {'groebner_basis': [str(pol.as_expr()) for pol in gb.polys], 'standard_monomials': std, 'length': len(std)}
exact = {}
exact['original_relation'] = all((vanishes(v) for v in p * h1 + b * h2 + c * h3))
exact['deletion_relation'] = all((vanishes(v) for v in a * f1 + d * f2 + e * f3))
exact['original_tangency'] = all((divisible(h[0], p) and divisible(h[1], q) and divisible(h[0] - h[1], r) for h in [h1, h2, h3]))
exact['deletion_tangency'] = all((divisible(f[0], y) and divisible(f[1], x - z) and divisible(f[0] - f[1], (y - z) * (x - y + z)) and divisible(f[0] + f[1], x - y - z) for f in [f1, f2, f3]))
exact['explicit_epi_relation'] = vanishes(p.subs(z, 0) - x * sp.Rational(1, 2) * (b + c).subs(z, 0))
exact['original_reduced_column'] = all((vanishes(v) for v in sp.Matrix([[1, -x / 2, -x / 2], [0, 1, 0], [0, 0, 1]]) * sp.Matrix([x ** 2, 3 * x - y, y - x]) - sp.Matrix([0, 3 * x - y, y - x])))
exact['four_plane_reduced_column'] = sp.Matrix([[1, 1, -1], [0, 1, 0], [0, 0, 1]]) * sp.Matrix([x + y, -y, x]) == sp.Matrix([0, -y, x])
exact['deletion_eliminations'] = vanishes(a.subs(z, x + y) - (2 * x * x + 4 * y * y)) and vanishes(d.subs(z, x + y) + 2 * y * y)
fields = []
for modulus in [None, 3, 5, 7, 11]:
    D = standard_monomials([p, b, c], modulus)
    F = standard_monomials([a, d, e], modulus)
    row = {'field': 'Q' if modulus is None else 'F' + str(modulus), 'original_ideal_equality': mutual_ideal_equal([p, b, c], [y - x, z - 2 * x, x * x], modulus), 'deletion_ideal_equality': mutual_ideal_equal([a, d, e], [z - x - y, x * x, y * y], modulus), 'original_ext': D, 'deletion_ext': F}
    row['pass'] = row['original_ideal_equality'] and row['deletion_ideal_equality'] and (D['length'] == 2) and (F['length'] == 4)
    fields.append(row)
result = {'scope': 'Exact controls; all-field and arbitrary-map proofs are in ungraded_local_obstructions.md.', 'exact_checks': exact, 'fields': fields, 'all_pass': all(exact.values()) and all((row['pass'] for row in fields))}
if not result['all_pass']:
    raise RuntimeError(result)
print(json.dumps(result, indent=2))
