"""Independent implementation of the rational Frobenius sparse research route.

The elementary dense field/factoring routines are the project's frozen reference
implementation. Their small-test prime oracle enumerates small F_p ONLY and is
not the uniform dense factoring input theorem. The sparse control flow, Padé,
exact identity, exponent-digit multiplicity, signed carry, and sections never
enumerate a field, integer factors, multiplicities, or the characteristic.
"""

import hashlib
import itertools
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "code"))
import finite_fields as ff
from sparse_extension_independent_checks import multiplicity


def dense_to_sparse(K, f):
    return [(e, c) for e, c in enumerate(f) if c != K.zero]


def sparse_times_dense(K, f, g):
    answer = {}
    for e, c in f:
        for j, a in enumerate(g):
            if a != K.zero:
                answer[e + j] = K.add(answer.get(e + j, K.zero), K.mul(c, a))
    return {e: c for e, c in answer.items() if c != K.zero}


def derivative_sparse(K, f):
    return [(e - 1, K.mul(c, K.element(e))) for e, c in f
            if e and e % K.p]


def logarithmic_denominator(K, u):
    assert u[0][0] == 0
    du = derivative_sparse(K, u)
    B = 1
    attempts = []
    while True:
        f = {e: c for e, c in u if e <= 2 * B}
        fp = {e: c for e, c in du if e < 2 * B}
        inverse = K.inv(f[0])
        series = []
        for k in range(2 * B):
            c = fp.get(k, K.zero)
            for j in range(1, k + 1):
                c = K.sub(c, K.mul(f.get(j, K.zero), series[k - j]))
            series.append(K.mul(c, inverse))
        columns = [[series[k - i] if k >= i else K.zero
                    for k in range(B, 2 * B)] for i in range(1, B + 1)]
        target = [K.neg(series[k]) for k in range(B, 2 * B)]
        solution = ff.solve_columns(K, columns, target)
        attempts.append(B)
        if solution is not None:
            Q = ff.trim(K, [K.one] + solution)
            P = ff.trim(K, [sum_field(K, [K.mul(Q[i], series[k - i])
                                         for i in range(min(k, len(Q) - 1) + 1)])
                            for k in range(B)])
            common = ff.gcd(K, P, Q)
            P, Q = ff.exact_div(K, P, common), ff.exact_div(K, Q, common)
            if sparse_times_dense(K, du, Q) == sparse_times_dense(K, u, P):
                return ff.monic(K, Q), attempts
        B *= 2


def sum_field(K, terms):
    result = K.zero
    for term in terms:
        result = K.add(result, term)
    return result


def dense_power(K, g, e):
    result = (K.one,)
    while e:
        if e & 1:
            result = ff.mul(K, result, g)
        e >>= 1
        if e:
            g = ff.mul(K, g, g)
    return result


def p_inverse_coefficient(K, c):
    return K.pow(c, K.p ** (K.m - 1))


def factor_sparse(K, sparse):
    sparse = sorted(sparse)
    shift = sparse[0][0]
    unit = sparse[-1][1]
    u = [(e - shift, c) for e, c in sparse]
    V = (K.one,)
    original_degree = u[-1][0]
    depth = 0
    power = 1
    factors = {(K.zero, K.one): shift} if shift else {}
    steps = []
    while u[-1][0]:
        R, attempts = logarithmic_denominator(K, u)
        visible = ff.factor(K, R, ff.exhaustive_prime_split_oracle).factors
        u_residues = {}
        A_u = (K.one,)
        for g, squarefree_multiplicity in visible:
            assert squarefree_multiplicity == 1
            e, E = multiplicity(K, u, g)
            r = e % K.p
            assert 1 <= r <= len(u) - 1 and r < K.p
            u_residues[g] = r
            A_u = ff.mul(K, A_u, dense_power(K, g, r))
        v_factor = ff.factor(K, V, ff.exhaustive_prime_split_oracle)
        v_residues = {g: e % K.p for g, e in v_factor.factors if e % K.p}
        A_v = (K.one,)
        for g, r in v_residues.items():
            A_v = ff.mul(K, A_v, dense_power(K, g, r))
        H_v = ff.polynomial_pth_root(K, ff.exact_div(K, V, A_v))
        signed = {}
        for g in set(u_residues) | set(v_residues):
            r = u_residues.get(g, 0) - v_residues.get(g, 0)
            if r:
                signed[g] = r
                factors[g] = factors.get(g, 0) + power * r
        new_u = [(e // K.p, p_inverse_coefficient(K, c)) for e, c in u
                 if e % K.p == 0]
        W = ff.trim(K, [p_inverse_coefficient(K, A_u[e])
                        for e in range(0, len(A_u), K.p)])
        new_v = ff.mul(K, W, H_v)
        assert new_u[0][0] == 0 and new_u[0][1] != K.zero
        assert new_v and new_v[0] != K.zero
        assert new_u[-1][0] <= u[-1][0] // K.p
        steps.append({"depth": depth, "numerator_degree": u[-1][0],
                      "denominator_degree": len(V) - 1,
                      "visible_degree": len(R) - 1,
                      "pade_attempts": attempts,
                      "residue_degree": len(A_u) - 1,
                      "new_denominator_degree": len(new_v) - 1,
                      "negative_signed_residues": sum(r < 0 for r in signed.values())})
        u, V = new_u, new_v
        depth += 1
        power *= K.p
    assert len(V) == 1  # V|U invariant and U is now a nonzero constant.
    answer = tuple(sorted((g, e) for g, e in factors.items() if e))
    assert all(e > 0 for _, e in answer)
    assert sum((len(g) - 1) * e for g, e in answer) == original_degree + shift
    return ff.Factorization(unit, answer), steps


def main():
    count = 0
    nontrivial_denominators = negative = 0
    for p, h, maximum_degree in [(2, (0, 1), 7), (3, (0, 1), 5),
                                (2, (1, 1, 1), 3), (2, (1, 1, 0, 1), 2)]:
        K = ff.FiniteField(p, h)
        elements = list(K.elements_for_testing())
        for degree in range(maximum_degree + 1):
            for coefficients in itertools.product(elements, repeat=degree):
                f = tuple(coefficients) + (K.one,)
                sparse = dense_to_sparse(K, f)
                got, steps = factor_sparse(K, sparse)
                want = ff.factor(K, f, ff.exhaustive_prime_split_oracle)
                assert got == want, (p, h, f, got, want)
                assert got.verify(K, f)
                count += 1
                nontrivial_denominators += sum(s["denominator_degree"] > 0 for s in steps)
                negative += sum(s["negative_signed_residues"] for s in steps)
    nonmonic = []
    for p, h in ((2, (1, 1, 1)), (3, (1, 0, 1))):
        K = ff.FiniteField(p, h)
        alpha, beta = K.basis()[1], K.one
        unit = K.add(alpha, K.one)
        g = (K.neg(alpha), K.one)
        j = (K.neg(beta), K.one)
        f = ff.mul(K, dense_power(K, g, 5), dense_power(K, j, 6))
        f = (K.zero,) * 7 + ff.scale(K, f, unit)
        got, steps = factor_sparse(K, dense_to_sparse(K, f))
        assert got.verify(K, f)
        assert got == ff.factor(K, f, ff.exhaustive_prime_split_oracle)
        nonmonic.append({"p": p, "m": 2, "unit": list(unit),
                         "monomial_multiplicity": 7, "other_multiplicities": [5, 6],
                         "stages": len(steps)})
    huge = []
    # Nontrivial section denominator, g irreducible of degree two.
    K = ff.FiniteField(2, (0, 1))
    g = K.poly((1, 1, 1))
    k, pk = 61, 2 ** 61
    sparse = sorted(sparse_times_dense(K, [(i * pk, c) for i, c in enumerate(g)], g).items())
    got, steps = factor_sparse(K, sparse)
    assert got.factors == ((g, pk + 1),)
    huge.append({"p": 2, "terms": len(sparse), "expected": "(X^2+X+1)^(2^61+1)",
                 "steps": steps})
    # Mixed huge multiplicities force a genuinely negative carry, even with N huge.
    K = ff.FiniteField(3, (0, 1))
    left, right = K.poly((-1, 1)), K.poly((1, 1))
    base = ff.mul(K, dense_power(K, left, 7), dense_power(K, right, 2))
    k, pk = 29, 3 ** 30
    sparse = sorted(sparse_times_dense(K, [(0, K.element(-1)), (pk, K.one)], base).items())
    got, steps = factor_sparse(K, sparse)
    assert dict(got.factors) == {left: 7 + pk, right: 2}
    assert sum(s["negative_signed_residues"] for s in steps) > 0
    huge.append({"p": 3, "terms": len(sparse),
                 "expected": "(X-1)^(7+3^30)*(X+1)^2", "steps": steps})
    path = Path(__file__).resolve()
    result = {"test": "independent rational Frobenius sparse factorization",
              "small_exact_dense_factorization_comparisons": count,
              "small_nontrivial_denominator_stages": nontrivial_denominators,
              "small_negative_signed_residues": negative,
              "nonmonic_and_monomial_cases": nonmonic,
              "huge_examples": huge,
              "script_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
              "multiplicity_script_sha256": hashlib.sha256(
                  path.with_name("sparse_extension_independent_checks.py").read_bytes()).hexdigest(),
              "base_arithmetic_sha256": hashlib.sha256(Path(ff.__file__).read_bytes()).hexdigest(),
              "python_version": sys.version,
              "scope": "Sparse control flow exact; dense factoring uses small-field toy oracle. "
                       "No novelty or upstream analytic theorem certification."}
    path.with_suffix(".json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: v for k, v in result.items() if k != "huge_examples"}, indent=2))


if __name__ == "__main__":
    main()
