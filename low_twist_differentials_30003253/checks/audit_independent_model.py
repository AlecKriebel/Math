"""Independent horizontal-tensor audit of the incidence-polynomial calculation.

This uses W(x,u), Euler contraction in u, and three tangent vector fields,
not the incidence quotient used by branch_integrality.py. Exact QQ ranks.
"""
from __future__ import annotations

import json
from pathlib import Path
import sympy as s
from branch_integrality import kernel

X = x, y, z = s.symbols('x y z')
U = u, v, w = s.symbols('u v w')


def powers(n):
    return [(i, j, n-i-j) for i in range(n+1) for j in range(n-i+1)]


def monomial(vs, es):
    return s.prod(v**e for v, e in zip(vs, es))


def exact_rank(rows, cols):
    M = s.Matrix(rows) if rows else s.zeros(0, cols)
    return s.polys.matrices.DomainMatrix.from_Matrix(M).rank()


def linear_normal_form(expr, divisor):
    """True sparse lexicographic normal form, independent of SymPy rem/Groebner.

    A single nonzero divisor is a Groebner basis for its principal ideal.
    Indivisible leading terms move to the remainder; division must continue.
    """
    work = s.Poly(expr, *X, domain=s.QQ).as_dict()
    F = s.Poly(divisor, *X, domain=s.QQ).as_dict()
    leading = max(F)
    coefficient = F[leading]
    result = {}
    while work:
        term = max(work)
        value = work[term]
        if all(a >= b for a, b in zip(term, leading)):
            shift = tuple(a-b for a, b in zip(term, leading))
            factor = value/coefficient
            for power, c in F.items():
                key = tuple(a+b for a, b in zip(power, shift))
                work[key] = work.get(key, 0)-factor*c
                if work[key] == 0:
                    del work[key]
        else:
            result[term] = value
            del work[term]
    return result


def horizontal_dimension(branches, r, k):
    if k-r < 0:
        return 0, 0
    terms = [monomial(X, a)*monomial(U, b)
             for a in powers(k-r) for b in powers(r)]
    euler = [s.Poly(sum(t*s.diff(T, q) for t, q in zip(X, U)),
                    *X, *U, domain=s.QQ).as_dict() for T in terms]
    mons = sorted(set().union(*(d.keys() for d in euler)))
    rows = [[d.get(m, 0) for d in euler] for m in mons]
    ambient = len(terms)-exact_rank(rows, len(terms))
    for F in branches:
        Fx, Fy, Fz = [s.diff(F, t) for t in X]
        for tangent in [(0, Fz, -Fy), (-Fz, 0, Fx), (Fy, -Fx, 0)]:
            cols = [linear_normal_form(T.subs(dict(zip(U, tangent)), simultaneous=True),
                                       F) for T in terms]
            mons = sorted(set().union(*(d.keys() for d in cols)))
            rows.extend([[d.get(m, 0) for d in cols] for m in mons])
    return ambient, len(terms)-exact_rank(rows, len(terms))


def main():
    tangent_lines = [x+2*t*y+t*t*z for t in range(5)]
    cases = [
        ('line_k_below_2r', [z], 2, 3),
        ('line_order_3', [z], 3, 6),
        ('line_order_1', [z], 1, 2),
        ('line_order_2', [z], 2, 4),
        ('smooth_conic_order_1_below', [x*z-y*y], 1, 2),
        ('smooth_conic_order_1', [x*z-y*y], 1, 3),
        ('smooth_conic_order_2', [x*z-y*y], 2, 4),
        ('transformed_conic_regression_order_1', [x*z-y*y-y*z-z*z], 1, 3),
        ('transformed_conic_regression_order_2', [x*z-y*y-y*z-z*z], 2, 4),
        ('smooth_cubic_order_2_below', [x**3+y**3+z**3], 2, 5),
        ('smooth_cubic_order_2', [x**3+y**3+z**3], 2, 6),
        ('five_tangent_lines', tangent_lines, 2, 4),
        ('six_snc_lines', [x+t*y+t**3*z for t in range(1,7)], 2, 5),
    ]
    change = {x:x+y, y:y+z, z:x+2*z}
    if not (s.Matrix([[1,1,0],[0,1,1],[1,0,2]]).det() != 0):
        raise AssertionError('Audit integrity check failed')
    cases.append(('five_tangent_lines_changed_coordinates',
                  [F.subs(change, simultaneous=True) for F in tangent_lines], 2, 4))
    results = []
    for name, branches, r, k in cases:
        ambient, dimension = horizontal_dimension(branches, r, k)
        incidence = kernel(branches, r, k)
        if not ((ambient, dimension) == (incidence['ambient_dimension'], incidence['dimension'])):
            raise AssertionError('Audit integrity check failed')
        results.append(dict(name=name, order=r, twist=k,
                            ambient_dimension=ambient, branch_integral_dimension=dimension))
        print(name, ambient, dimension, flush=True)
    # A squarefree hypothesis is essential, not merely convenient.
    reduced = kernel([z], 2, 4)['dimension']
    if not (reduced == 5):
        raise AssertionError('Audit integrity check failed')
    try:
        kernel([z*z], 2, 4)
    except ValueError as error:
        rejected = str(error)
    else:
        raise AssertionError('Nonreduced input must be rejected')
    output = dict(coefficient_field='QQ', sympy_version=s.__version__,
                  method='Euler-horizontal symmetric tensors; three gradient tangent fields; independent sparse lex normal form',
                  tests=results, nonreduced_input_guard_example=dict(
                      reduced_line_dimension=reduced, squared_line_rejected=rejected))
    Path(__file__).with_name('audit_independent_results.json').write_text(
        json.dumps(output, indent=2)+'\n')
    print('PASS: all independent-model comparisons', flush=True)


if __name__ == '__main__':
    main()
