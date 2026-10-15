#!/usr/bin/env python3
"""Exact bounded sanity controls, not a proof of the ACFH theorem."""
import argparse
import itertools
import json
from pathlib import Path


class QuadraticField:
    """F_p[T]/(T^2 + a*T + b), represented as pairs of residues."""

    def __init__(self, p, a, b):
        self.p, self.a, self.b = p, a, b
        assert all((x*x + a*x + b) % p for x in range(p))
        self.zero, self.one = (0, 0), (1, 0)
        self.elements = list(itertools.product(range(p), repeat=2))
        self.nonzero = [x for x in self.elements if x != self.zero]

    def add(self, x, y):
        return ((x[0]+y[0]) % self.p, (x[1]+y[1]) % self.p)

    def mul(self, x, y):
        u, v = x
        w, z = y
        return ((u*w-self.b*v*z) % self.p,
                (u*z+v*w-self.a*v*z) % self.p)

    def power(self, x, n):
        if n < 0:
            assert x != self.zero
            return self.power(self.power(x, self.p*self.p-2), -n)
        result = self.one
        while n:
            if n & 1:
                result = self.mul(result, x)
            x = self.mul(x, x)
            n //= 2
        return result

    def polynomial_map(self, coefficients, theta_power, x):
        assert x != self.zero
        result, iterate = self.one, x
        for c in coefficients:
            result = self.mul(result, self.power(iterate, c))
            iterate = self.power(iterate, theta_power)
        return result


def run():
    fields = []
    for p, a, b in [(2, 1, 1), (3, 0, 1), (5, 0, 2), (7, 0, 1)]:
        f = QuadraticField(p, a, b)
        frob = {x: f.power(x, p) for x in f.elements}
        assert len(set(frob.values())) == p*p
        rho = {y: x for x, y in frob.items()}
        for x in f.elements:
            assert f.power(rho[x], p) == x
            assert rho[frob[x]] == x
            assert len([y for y in f.elements if f.power(y, p) == x]) == 1
        assert rho[f.zero] == f.zero and rho[f.one] == f.one
        for x in f.elements:
            for y in f.elements:
                assert rho[f.mul(x, y)] == f.mul(rho[x], rho[y])
                assert rho[f.add(x, y)] == f.add(rho[x], rho[y])
        for e in range(p*p-1):
            for x in f.nonzero:
                assert f.power(rho[x], e) == rho[f.power(x, e)]
        # In these finite fields inverse Frobenius IS an integer power map.
        # This deliberately prevents interpreting the controls as a generic model.
        assert all(rho[x] == f.power(x, p) for x in f.elements)
        assert any(frob[x] != f.one for x in f.nonzero)
        samples = [(0,), (1,), (-1,), (1, 1), (2, -3, 1), (-2, 0, 3)]
        identity_checks = 0
        for coefficients in samples:
            pPminus1 = [p*c for c in coefficients]
            pPminus1[0] -= 1
            for e in range(p*p-1):
                for x in f.nonzero:
                    value = f.polynomial_map(coefficients, e, x)
                    lhs = f.polynomial_map(pPminus1, e, x)
                    rhs = f.mul(f.power(value, p), f.power(x, -1))
                    assert lhs == rhs
                    identity_checks += 1
        fields.append({
            "p": p, "order": p*p,
            "irreducible_polynomial_coefficients_ascending": [b, a, 1],
            "inverse_frobenius_unique_additive_multiplicative": True,
            "commutes_with_all_tested_power_endomorphisms": True,
            "tested_power_endomorphisms": p*p-1,
            "ring_identity_checks": identity_checks,
            "finite_field_inverse_is_integer_power": p,
            "acf_or_acfh_model": False,
        })

    count = 0
    for p in [2, 3, 5, 7, 11]:
        for length in range(1, 6):
            for coefficients in itertools.product(range(-2, 3), repeat=length):
                q = [p*c for c in coefficients]
                q[0] -= 1
                assert q[0] % p == p-1
                assert any(q)
                count += 1
    return {
        "status": "PASS",
        "test_role": "Exact bounded sanity controls only; no model-theoretic or universal proof certification.",
        "finite_quadratic_fields": fields,
        "integer_polynomial_controls": {
            "primes": [2, 3, 5, 7, 11],
            "coefficient_range": [-2, 2],
            "coefficient_vector_lengths": [1, 5],
            "vectors_tested_including_leading_zero_vectors": count,
            "pP_minus_1_always_nonzero_in_test": True,
            "universal_reason": "The constant coefficient p*a0-1 is -1 modulo p.",
        },
        "proof_location": "PROOF.md",
        "formal_proof_assistant_check": False,
        "independent_audit": "pending",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", type=Path)
    args = parser.parse_args()
    result = run()
    if args.check:
        assert json.loads(args.check.read_text()) == result, "Stored output differs"
        print("PASS: exact controls match stored results")
    else:
        print(json.dumps(result, indent=2, sort_keys=True))
