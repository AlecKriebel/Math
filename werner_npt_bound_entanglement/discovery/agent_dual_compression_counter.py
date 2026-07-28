"""Exact check of the n=2 compression stable-rank counterexample.

This is a deterministic symbolic check.  It constructs
    U = span{(|01>-|10>)/sqrt(2), |11>}
    V = span{(|01>-|10>)/sqrt(2), |00>}
and compresses (I-F/2)^{tensor 2} to U tensor V.
"""

import sympy as sp


D_LOCAL = 3
D_SIDE = D_LOCAL**2


def side_vector(entries):
    vector = sp.zeros(D_SIDE, 1)
    for (i, j), value in entries.items():
        vector[i * D_LOCAL + j] = value
    return vector


def partial_swap_element(a, b, c, e, subset):
    """Return <a,b|F_subset|c,e> exactly."""
    total = 0
    for a_index in range(D_SIDE):
        a_digits = list(divmod(a_index, D_LOCAL))
        for b_index in range(D_SIDE):
            b_digits = list(divmod(b_index, D_LOCAL))
            bra = sp.conjugate(a[a_index]) * sp.conjugate(b[b_index])
            if bra == 0:
                continue
            c_digits = a_digits.copy()
            e_digits = b_digits.copy()
            for site in subset:
                c_digits[site], e_digits[site] = (
                    e_digits[site],
                    c_digits[site],
                )
            c_index = c_digits[0] * D_LOCAL + c_digits[1]
            e_index = e_digits[0] * D_LOCAL + e_digits[1]
            total += bra * c[c_index] * e[e_index]
    return sp.simplify(total)


def compression():
    root_two = sp.sqrt(2)
    antisymmetric = side_vector({(0, 1): 1 / root_two, (1, 0): -1 / root_two})
    u_vectors = [antisymmetric, side_vector({(1, 1): 1})]
    v_vectors = [antisymmetric, side_vector({(0, 0): 1})]
    pairs = [(i, j) for i in range(2) for j in range(2)]
    matrix = sp.zeros(4)
    for row, (i, j) in enumerate(pairs):
        for column, (k, ell) in enumerate(pairs):
            value = 0
            for mask in range(4):
                subset = [site for site in range(2) if mask & (1 << site)]
                value += sp.Rational(-1, 2) ** len(subset) * partial_swap_element(
                    u_vectors[i],
                    v_vectors[j],
                    u_vectors[k],
                    v_vectors[ell],
                    subset,
                )
            matrix[row, column] = sp.simplify(value)
    return matrix


if __name__ == "__main__":
    compressed = compression()
    expected = sp.Matrix(
        [
            [sp.Rational(3, 4), 0, 0, sp.Rational(1, 2)],
            [0, sp.Rational(1, 2), 0, 0],
            [0, 0, sp.Rational(1, 2), 0],
            [sp.Rational(1, 2), 0, 0, 1],
        ]
    )
    assert compressed == expected
    characteristic = sp.factor(compressed.charpoly().as_expr())
    assert characteristic == (
        (2 * sp.Symbol("lambda") - 1) ** 2
        * (4 * sp.Symbol("lambda") ** 2 - 7 * sp.Symbol("lambda") + 2)
        / 16
    )
    ratio = sp.simplify(
        2 * (sp.Rational(7, 8) + sp.sqrt(17) / 8) / sp.trace(compressed)
    )
    assert ratio == (7 + sp.sqrt(17)) / 11
    assert sp.sqrt(17) > 4
    print(compressed)
    print(characteristic)
    print("2*operator_norm/trace =", ratio, "> 1")
