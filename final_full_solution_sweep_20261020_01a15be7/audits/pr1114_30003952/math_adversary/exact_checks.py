#!/usr/bin/env python3
"""New standard-library exact regression checks; no analytic certification."""
from fractions import Fraction as F
import json


def q(a=0, b=0):
    return (F(a), F(b))


def add(x, y):
    return (x[0] + y[0], x[1] + y[1])


def neg(x):
    return (-x[0], -x[1])


def mul(x, y):
    return (x[0] * y[0] + 3 * x[1] * y[1],
            x[0] * y[1] + x[1] * y[0])


def inv(x):
    d = x[0] ** 2 - 3 * x[1] ** 2
    if d == 0:
        raise ValueError('zero quadratic-field divisor')
    return (x[0] / d, -x[1] / d)


def mat(rows):
    return tuple(tuple(x if isinstance(x, tuple) else q(x) for x in row)
                 for row in rows)


def mm(a, b):
    return tuple(tuple(add(mul(a[i][0], b[0][j]), mul(a[i][1], b[1][j]))
                       for j in range(2)) for i in range(2))


def det(a):
    return add(mul(a[0][0], a[1][1]), neg(mul(a[0][1], a[1][0])))


def mi(a):
    d = inv(det(a))
    return tuple(tuple(mul(d, x) for x in row) for row in
                 ((a[1][1], neg(a[0][1])), (neg(a[1][0]), a[0][0])))


I = mat(((1, 0), (0, 1)))


def mp(a, n):
    if n < 0:
        return mp(mi(a), -n)
    out = I
    for _ in range(n):
        out = mm(out, a)
    return out


def reduce_word(word):
    out = []
    for x in word:
        if out and out[-1] == -x:
            out.pop()
        else:
            out.append(x)
    return tuple(out)


def inverse_word(word):
    return tuple(-x for x in reversed(word))


ID = ((1,), (2,), (3,))
A = ((1, 2, -1), (1,), (3,))
AI = ((2,), (-2, 1, 2), (3,))
B = ((1,), (2, 3, -2), (2,))
BI = ((1,), (3,), (-3, 2, 3))


def act(phi, word):
    return reduce_word(y for x in word for y in
                       (phi[x - 1] if x > 0 else inverse_word(phi[-x - 1])))


def compose(phi, psi):
    return tuple(act(phi, word) for word in psi)


def word_action(word):
    out = ID
    for x in word:
        out = compose(out, {1: A, -1: AI, 2: B, -2: BI}[x])
    return out


def finite_checks():
    passed = []
    rejected = []

    def check(name, condition):
        if condition is not True:
            raise RuntimeError('failed: ' + name)
        passed.append(name)

    def reject(name, false_condition):
        if false_condition is not False:
            raise RuntimeError('mutation survived: ' + name)
        rejected.append(name)

    u = mat(((1, 1), (0, 1)))
    v = mat(((1, 0), (-1, 1)))
    Q = mm(mm(u, v), u)
    R = mm(u, v)
    minus = mat(((-1, 0), (0, -1)))
    P = mat(((1, q(F(-1, 2))), (0, q(0, F(1, 2)))))
    rotation = mat(((q(F(1, 2)), q(0, F(1, 2))),
                    (q(0, F(-1, 2)), q(F(1, 2)))))
    check('matrix_braid', Q == mm(mm(v, u), v))
    check('common_negative_identity', mp(Q, 2) == mp(R, 3) == minus)
    check('finite_orders', mp(Q, 4) == mp(R, 6) == I)
    check('reconstruct_u', mm(mi(R), Q) == u)
    check('reconstruct_v', mm(mi(Q), mp(R, 2)) == v)
    check('positive_coordinate_determinant', det(P) == q(0, F(1, 2)))
    check('exact_rotation_conjugacy', mm(mm(P, R), mi(P)) == rotation)
    check('rotation_determinant', det(rotation) == q(1))
    check('inverse_p_squared_frobenius',
          sum((mul(x, x)[0] for row in mi(P) for x in row), F()) == F(8, 3)
          and all(mul(x, x)[1] == 0 for row in mi(P) for x in row))
    check('r_squared_frobenius', sum(x[0]**2 for row in R for x in row) == 3)
    # ||P_t||_F^2 = 2+(2-sqrt(3))*(t^2-t) <= 2 on [0,1].
    coefficient = add(mul(q(0, F(1, 2)), q(0, F(1, 2))), q(F(5, 4)))
    check('path_norm_quadratic_coefficient', add(coefficient, q(0, -1)) == q(2, -1))
    check('safe_linear_trajectory_margin', 2*F(1, 64) == F(1, 32))
    check('safe_common_disk_margin', 4*F(1, 512) < F(1, 64))
    check('strict_collar_nesting', F(1, 4096) < F(1, 2048) < F(1, 1024) < F(1, 512))
    check('unit_annular_lift_difference', F(0)-F(1) == -1)
    check('offset_equation_plus', (1-1) % 12 == 0 and (1-1)//12 == 0)
    check('offset_equation_minus_impossible', (-1-1) % 12 != 0)
    check('artin_inverses', compose(A, AI) == compose(AI, A) == compose(B, BI) == compose(BI, B) == ID)
    check('artin_braid', word_action((1, 2, 1)) == word_action((2, 1, 2)))
    check('simultaneous_inverse_braid', word_action((-1, -2, -1)) == word_action((-2, -1, -2)))
    check('x_square_y_cube', word_action((1, 2, 1)*2) == word_action((1, 2)*3))
    check('sixth_product_nontrivial', word_action((1, 2)*6) != ID)
    check('sixth_product_central_a', word_action((1, 2)*6+(1,)) == word_action((1,)+(1, 2)*6))
    check('sixth_product_central_b', word_action((1, 2)*6+(2,)) == word_action((2,)+(1, 2)*6))
    check('abstract_a_reconstruction', word_action((-2,-1,1,2,1)) == A)
    check('abstract_b_reconstruction', word_action((-1,-2,-1,1,2,1,2)) == B)
    reject('one_sided_inverse', word_action((-1,2,-1)) == word_action((2,-1,2)))
    badP = mat(((1, q(F(1, 2))), (0, q(0, F(1, 2)))))
    reject('wrong_coordinate_sign', mm(mm(badP,R),mi(badP)) == rotation)
    reject('wrong_common_cube', mp(mat(((0,1),(1,1))),3) == minus)
    reject('oversized_common_disk', 4*F(1,8) < F(1,64))
    reject('reversed_collar', F(1,1024) < F(1,2048))
    reject('zero_winding_central_equation', (0-1) % 12 == 0)
    reject('double_winding_central_equation', (2-1) % 12 == 0)
    reject('common_nonzero_offset', 1+12*1 in (-1,1))
    reject('unequal_offsets_braid_exponents', 2*1+0 == 1+2*0)
    return {'status':'pass', 'positive_checks':passed, 'negative_controls':rejected,
            'positive_count':len(passed), 'negative_count':len(rejected),
            'scope':'Exact finite algebraic regression evidence. Universal smoothness, ODE, topology and gluing are established only by written analytic reasoning.'}


if __name__ == '__main__':
    print(json.dumps(finite_checks(), sort_keys=True, separators=(',', ':')))
