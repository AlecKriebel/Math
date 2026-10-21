"""Exact finite check of the coefficient used in Karpenko's 2023 proof.

This is a reproduction of a published polynomial step, not a proof of the
geometric criterion connecting that step to a generic Grassmannian index.
No source-author program, floating point or third-party library is used.
"""
import hashlib
import itertools
import json


def need(condition, message):
    if not condition:
        raise RuntimeError(message)


def multiply_mod2(a, b):
    out = set()
    for u in a:
        for v in b:
            term = tuple(x + y for x, y in zip(u, v))
            if term in out:
                out.remove(term)
            else:
                out.add(term)
    return out


def direct_product():
    out = {(0, 0, 0, 0, 0)}
    for subset in itertools.product((0, 1), repeat=4):
        factor = {(1, 0, 0, 0, 0)}
        for i, bit in enumerate(subset):
            if bit:
                monomial = [0] * 5
                monomial[i + 1] = 1
                factor.add(tuple(monomial))
        out = multiply_mod2(out, factor)
    return out


def recursive_product():
    # f_{m-1}(x)=f_m(x)^2+f_m(x) f_m(x_m) over F2.
    out = {(1, 0, 0, 0, 0)}
    for variable in (4, 3, 2, 1):
        square = {tuple(2 * e for e in t) for t in out}
        evaluated = set()
        for term in out:
            t = list(term)
            t[variable] += t[0]
            t[0] = 0
            t = tuple(t)
            if t in evaluated:
                evaluated.remove(t)
            else:
                evaluated.add(t)
        out = square.symmetric_difference(multiply_mod2(out, evaluated))
    return out


def main():
    direct = direct_product()
    recursive = recursive_product()
    need(direct == recursive, "Independent expansion orders disagree")
    need(all(sum(t) == 16 for t in direct), "Incorrect degree")
    need({t[0] for t in direct} == {1, 2, 4, 8, 16}, "Not linearized")
    coefficient = sorted(t[1:] for t in direct if t[0] == 8)
    target = (0, 0, 4, 4)
    need(target in coefficient, "Published e8 witness monomial absent")
    # Terms containing x_i^8 vanish in the flag ring modulo 2. All remaining
    # terms already satisfy the flag basis bounds a_i<i (i=5,6,7,8).
    surviving = [t for t in coefficient if max(t) < 8]
    need(all(all(e < i for e, i in zip(t, (5, 6, 7, 8))) for t in surviving),
         "Unreduced flag basis monomial")
    need(target in surviving, "Witness lost under flag relations")
    need(len(surviving) == len(set(surviving)), "Duplicate coefficient term")
    encoded = json.dumps(sorted(direct), separators=(",", ":")).encode()
    print(json.dumps({
        "status": "PASS", "field": "F2", "variables": ["x", "x5", "x6", "x7", "x8"],
        "linear_factors": 16, "polynomial_terms": len(direct),
        "expansion_algorithms": ["all subset linear factors", "linearized recursion"],
        "expansions_equal": True, "x_exponents": [1, 2, 4, 8, 16],
        "coefficient_of_x8": coefficient, "surviving_flag_basis_terms": surviving,
        "witness": {"monomial": "x7^4*x8^4", "coefficient_mod2": 1},
        "canonical_polynomial_sha256": hashlib.sha256(encoded).hexdigest(),
        "scope": "Finite polynomial/basis check only. Chow presentation, index criterion, torsion exponent and genericity remain explicitly cited theorems."
    }, indent=2))


if __name__ == "__main__":
    main()
