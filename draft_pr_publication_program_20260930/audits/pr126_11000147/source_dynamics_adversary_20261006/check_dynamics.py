"""Independent exact torus-dynamics certificate; no submitted verifier imported.

Verification only: no proof-search turns. Every guard is explicit, so -O does
not remove validation. Elements of Q(sqrt(3)) are pairs of rational numbers.
"""
from fractions import Fraction
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os
import sys


def q(a=0, b=0):
    return Fraction(a), Fraction(b)


def add(x, y):
    return x[0] + y[0], x[1] + y[1]


def neg(x):
    return -x[0], -x[1]


def sub(x, y):
    return add(x, neg(y))


def mul(x, y):
    return x[0]*y[0] + 3*x[1]*y[1], x[0]*y[1] + x[1]*y[0]


def inv(x):
    denominator = x[0]*x[0] - 3*x[1]*x[1]
    if denominator == 0:
        raise ValueError('zero field element')
    return x[0]/denominator, -x[1]/denominator


def scale(x, matrix):
    return tuple(tuple(mul(x, y) for y in row) for row in matrix)


def matrix_add(m, n):
    return tuple(tuple(add(m[i][j], n[i][j]) for j in range(2)) for i in range(2))


def matrix_sub(m, n):
    return matrix_add(m, scale(q(-1), n))


def matrix_mul(m, n):
    return tuple(tuple(add(mul(m[i][0], n[0][j]), mul(m[i][1], n[1][j]))
                       for j in range(2)) for i in range(2))


def vector_mul(m, v):
    return tuple(add(mul(row[0], v[0]), mul(row[1], v[1])) for row in m)


def row_mul(v, m):
    return tuple(add(mul(v[0], m[0][j]), mul(v[1], m[1][j])) for j in range(2))


def vector_scale(x, v):
    return tuple(mul(x, y) for y in v)


def determinant(m):
    return sub(mul(m[0][0], m[1][1]), mul(m[0][1], m[1][0]))


def encode(value):
    if isinstance(value, Fraction):
        return str(value)
    if isinstance(value, tuple):
        return [encode(x) for x in value]
    if isinstance(value, dict):
        return {k: encode(v) for k, v in value.items()}
    if isinstance(value, list):
        return [encode(x) for x in value]
    return value


I = ((q(1), q()), (q(), q(1)))
ZERO = scale(q(), I)
UP = q(2, 1)
DOWN = q(2, -1)
checks = []


def require(name, condition):
    if condition is not True:
        raise RuntimeError('failed independent guard: ' + name)
    checks.append(name)


require('reciprocal expansion and contraction factors', mul(UP, DOWN) == q(1))
matrices = {'A': ((3, 1), (2, 1)), 'B': ((1, -2), (-1, 3)),
            'C': ((8, -11), (3, -4))}
certificates = {}
for name, m_int in matrices.items():
    m = tuple(tuple(q(x) for x in row) for row in m_int)
    require(name + ': determinant one', determinant(m) == q(1))
    require(name + ': trace four', add(m[0][0], m[1][1]) == q(4))
    require(name + ': characteristic equation',
            matrix_add(matrix_sub(matrix_mul(m, m), scale(q(4), m)), I) == ZERO)
    inverse = ((m[1][1], neg(m[0][1])), (neg(m[1][0]), m[0][0]))
    require(name + ': two-sided integral lattice inverse',
            matrix_mul(m, inverse) == I and matrix_mul(inverse, m) == I
            and all(x[1] == 0 and x[0].denominator == 1 for row in inverse for x in row))
    # Right eigenvectors use the first row. Every displayed upper-right entry
    # is nonzero, so these are nonzero without a numerical approximation.
    stable = (m[0][1], sub(DOWN, m[0][0]))
    unstable = (m[0][1], sub(UP, m[0][0]))
    require(name + ': nonzero stable and unstable vectors',
            stable[0] != q() and unstable[0] != q())
    require(name + ': stable tangent direction', vector_mul(m, stable) == vector_scale(DOWN, stable))
    require(name + ': unstable tangent direction', vector_mul(m, unstable) == vector_scale(UP, unstable))
    basis = ((stable[0], unstable[0]), (stable[1], unstable[1]))
    require(name + ': transverse tangent splitting', determinant(basis) != q())
    # Measures normal to stable and unstable foliations. These are pullback
    # scaling equations, not pushforward scaling equations.
    normal_stable = (sub(DOWN, m[0][0]), neg(m[0][1]))
    normal_unstable = (sub(UP, m[0][0]), neg(m[0][1]))
    require(name + ': stable-foliation normal annihilation',
            add(mul(normal_stable[0], stable[0]), mul(normal_stable[1], stable[1])) == q())
    require(name + ': unstable-foliation normal annihilation',
            add(mul(normal_unstable[0], unstable[0]), mul(normal_unstable[1], unstable[1])) == q())
    require(name + ': stable-foliation pullback expands transverse measure',
            row_mul(normal_stable, m) == vector_scale(UP, normal_stable))
    require(name + ': unstable-foliation pullback contracts transverse measure',
            row_mul(normal_unstable, m) == vector_scale(DOWN, normal_unstable))
    p_up = scale(inv(sub(UP, DOWN)), matrix_sub(m, scale(DOWN, I)))
    p_down = matrix_sub(I, p_up)
    require(name + ': exact complementary spectral projectors',
            matrix_mul(p_up, p_up) == p_up and matrix_mul(p_down, p_down) == p_down
            and matrix_mul(p_up, p_down) == ZERO and matrix_mul(p_down, p_up) == ZERO
            and matrix_add(p_up, p_down) == I)
    require(name + ': exact spectral-projector dynamics',
            matrix_mul(m, p_up) == scale(UP, p_up) and matrix_mul(m, p_down) == scale(DOWN, p_down))
    certificates[name] = dict(matrix=m_int, integral_inverse=inverse,
                              stable_vector=stable, unstable_vector=unstable,
                              stable_foliation_normal=normal_stable,
                              unstable_foliation_normal=normal_unstable,
                              expanding_projector=p_up, contracting_projector=p_down)

# Adversarial controls reject tempting nearby replacements at their actual
# failed prerequisite; no assertion or floating tolerance is involved.
parabolic = ((q(1), q(1)), (q(), q(1)))
require('negative control: a trace-two shear lacks the claimed characteristic polynomial',
        matrix_add(matrix_sub(matrix_mul(parabolic, parabolic), scale(q(4), parabolic)), I) != ZERO)
reverse = ((q(1), q()), (q(), q(-1)))
require('negative control: orientation reversal is not determinant one', determinant(reverse) != q(1))
cover = ((q(2), q()), (q(), q(1)))
require('negative control: an expanding rational lattice covering is not determinant one', determinant(cover) != q(1))

base = Path(__file__).resolve().parent
source = base.parent/'private_primary_source_20261006/mcgbook.pdf'
output = dict(
    created_utc=datetime.now(timezone.utc).isoformat(), operator_pid=os.getpid(),
    python=sys.version, optimization_level=sys.flags.optimize,
    original_head='a1df84a64fa96d53f3a8c6fec9db8bc48bd1533c',
    primary_pdf_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
    check_script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    field='Q(sqrt(3)); encoded field element [rational part, sqrt(3) coefficient]',
    checks_passed=checks, number_of_explicit_guards=len(checks),
    eigenvalues=dict(expanding=UP, contracting=DOWN), certificates=certificates,
    exact_positive_inequality_argument='1 < sqrt(3) < 2 implies 0 < 2-sqrt(3) < 1 < 2+sqrt(3)',
    proof_search_turns_added=0, proof_limits='Certificate supplements the global descent/foliation proof; it is not a substitute for it.'
)
destination = base/('DYNAMICS_CERTIFICATE_O.json' if sys.flags.optimize else 'DYNAMICS_CERTIFICATE.json')
destination.write_text(json.dumps(encode(output), indent=2) + '\n')
print(json.dumps(dict(path=str(destination), operator_pid=os.getpid(), explicit_guards=len(checks),
                      optimization_level=sys.flags.optimize)))
