"""Reproducible examples and dimension/call certificates, small toy oracle only."""

import json

from finite_fields import FiniteField, exhaustive_prime_split_oracle, factor, mul


def encoded_polynomial(f):
    return [list(a) for a in f]


def run_example(label, p, h, generators):
    K = FiniteField(p, h)
    original = (K.one,)
    for coefficients, multiplicity in generators:
        g = K.poly(coefficients)
        for _ in range(multiplicity):
            original = mul(K, original, g)
    answer = factor(K, original, exhaustive_prime_split_oracle)
    return {"label": label, "characteristic": p, "extension_degree": K.m,
            "field_modulus": list(h), "input": encoded_polynomial(original),
            "unit": list(answer.unit),
            "factors": [{"polynomial": encoded_polynomial(g), "multiplicity": e}
                        for g, e in answer.factors],
            "reconstruction_and_frobenius_verification": answer.verify(K, original),
            "statistics": K.stats.as_dict()}


def main():
    examples = [
        run_example("extension degree one, repeated factors", 3, [0, 1],
                    [([0, 1], 2), ([1, 1], 3), ([1, 0, 1], 1)]),
        run_example("characteristic two with coefficient pth roots", 2, [1, 1, 1],
                    [([(0, 1), 1], 4), ([(1, 1), 1], 3)]),
        run_example("odd characteristic, nonprime extension field", 3, [1, 0, 1],
                    [([(0, 1), 1], 2), ([(1, 1), 1], 1), ([1, 0, 1], 1)]),
        run_example("all eight component values over F8", 2, [1, 1, 0, 1],
                    [([value, 1], 1) for value in
                     [(a, b, c) for a in range(2) for b in range(2) for c in range(2)]]),
    ]
    print(json.dumps({"scope": "conditional reduction; exhaustive prime oracle for small tests only",
                      "examples": examples}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
