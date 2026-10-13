#!/usr/bin/env python3
"""Additional adversarial sparse audit; writes only its own results.json.

The control flow independently reconstructs each rational descent stage and
checks it against dense factorization on feasible inputs. The audited sparse
valuation and Pade routines are checked against that dense reference. Both
paths use the project's finite-field arithmetic, and the dense reference uses
its explicitly small-test-only exhaustive prime oracle. This is finite evidence
for the conditional sparse reduction, not certification of the upstream theorem.
"""

from datetime import datetime, timezone
import hashlib
import itertools
import json
from pathlib import Path
import random
import sys
import time

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "code"))
import finite_fields as ff
import sparse_cartier as sc


EXPECTED_INPUT_HASHES = {
    "manuscript/main.tex": "fbabb3ecaf36fa49416e6b7c0bbc32e73be26902bda9d66e9f85228ef6733d58",
    "SPARSE_CANDIDATE_DERIVATION.md": "d67ab2e57978ebadb5b43a80523fba38d2843e301edaad57fe6a173713f67ce5",
    "code/sparse_cartier.py": "33dfca735400ec29ef34e787e691b1c9f060420962c17a8cd11d2f5de17c5693",
    "code/test_sparse_cartier.py": "03a5e204d7e54f96f39a0adfcc543989db1a76213340b35755b86f086d7d3067",
    "code/finite_fields.py": "4d8fc155249d053229033af123fda2fc2c57bd3c51b91ddb4484cb4755a47ec3",
    "agent_notes/sparse_rational_independent_checks.py": "58e07366ae8e5738a5001d125313c8debaf15e68bd067748c775ef6bfa38b0a0",
    "agent_notes/sparse_extension_independent_checks.py": "7493b54c2c0a93d665852078c44c436afd58754d92cdae09c163cfbf01ad4f74",
}


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def input_hashes():
    return {name: sha256(ROOT / name) for name in EXPECTED_INPUT_HASHES}


def degree(f):
    return len(f) - 1


def dense(K, U):
    return ff.trim(K, [U.get(i, K.zero) for i in range(max(U) + 1)])


def audit_one(K, f, stats):
    original = ff.trim(K, f)
    assert original
    truth = ff.factor(K, original, ff.exhaustive_prime_split_oracle)
    D = sum(degree(g) for g, e in truth.factors)
    terms = sc.normalized_sparse(K, enumerate(original))
    shift = min(terms)
    U = {n - shift: a for n, a in terms.items()}
    V = (K.one,)
    ledger = {(K.zero, K.one): shift} if shift else {}
    weight, k, t = 1, 0, len(terms)
    N = degree(original)
    b = max(1, N.bit_length())

    while max(U) > 0:
        Ud = dense(K, U)
        F = ff.exact_div(K, Ud, V)
        uf = ff.factor(K, Ud, ff.exhaustive_prime_split_oracle)
        vf = ff.factor(K, V, ff.exhaustive_prime_split_oracle)
        frad = {g for g, e in ff.factor(K, F, ff.exhaustive_prime_split_oracle).factors}
        expectedG, AU, AV = (K.one,), (K.one,), (K.one,)
        signed = {}

        for g, e in uf.factors:
            assert sc.quotient_multiplicity(K, U, g) == e
            r = e % K.p
            assert r <= len(U) - 1
            if r:
                expectedG = ff.mul(K, expectedG, g)
                AU = ff.mul(K, AU, sc.dense_power(K, g, r))
                signed[g] = r
        assert sc.logarithmic_denominator(K, U, []) == expectedG

        for g, e in vf.factors:
            r = e % K.p
            if r:
                AV = ff.mul(K, AV, sc.dense_power(K, g, r))
                signed[g] = signed.get(g, 0) - r

        HU = ff.polynomial_pth_root(K, ff.exact_div(K, Ud, AU))
        HV = ff.polynomial_pth_root(K, ff.exact_div(K, V, AV))
        H = ff.exact_div(K, HU, HV)
        newU = {n // K.p: sc.coefficient_root(K, c)
                for n, c in U.items() if n % K.p == 0}
        W = ff.trim(K, [sc.coefficient_root(K, AU[j])
                        for j in range(0, len(AU), K.p)])
        newV = ff.mul(K, W, HV)
        newUd = dense(K, newU)

        assert ff.mul(K, W, HU) == newUd
        assert ff.exact_div(K, newUd, newV) == H
        hrad = {g for g, e in ff.factor(K, H, ff.exhaustive_prime_split_oracle).factors}
        assert hrad <= frad
        DF = sum(degree(g) for g in frad)
        assert degree(V) <= k * D
        assert degree(expectedG) <= (k + 1) * D
        assert degree(newV) <= degree(V) + DF
        assert degree(AU) <= min(K.p - 1, len(U) - 1) * sum(degree(g) for g, e in uf.factors)
        assert len(newU) <= t and max(newU) <= max(U) // K.p
        assert newU[0] != K.zero and newV[0] != K.zero

        for g, r in signed.items():
            ledger[g] = ledger.get(g, 0) + weight * r
        stats["stages"] += 1
        stats["negative_stages"] += int(any(r < 0 for r in signed.values()))
        stats["max_denominator_degree"] = max(stats["max_denominator_degree"], degree(newV))
        U, V = newU, newV
        weight *= K.p
        k += 1
        assert k <= b

    assert len(V) == 1
    got = ff.Factorization(original[-1], tuple(sorted((g, e) for g, e in ledger.items() if e)))
    assert got == truth
    stats["inputs"] += 1


def finite_stage_audit():
    stats = {"inputs": 0, "stages": 0, "negative_stages": 0,
             "fields": [], "max_denominator_degree": 0}
    rng = random.Random(10072026)
    parameters = [
        (2, (0, 1), 8, 150, 28),
        (3, (0, 1), 5, 120, 20),
        (5, (0, 1), 3, 80, 16),
        (2, (1, 1, 1), 4, 100, 15),
        (3, (1, 0, 1), 3, 80, 12),
        (2, (1, 1, 0, 1), 2, 60, 12),
    ]
    for p, h, exhaustive_cap, random_count, random_cap in parameters:
        K = ff.FiniteField(p, h)
        elements = list(K.elements_for_testing())
        start = stats["inputs"]
        for n in range(exhaustive_cap + 1):
            for prefix in itertools.product(elements, repeat=n):
                audit_one(K, prefix + (K.one,), stats)
        for _ in range(random_count):
            n = rng.randrange(random_cap + 1)
            f = tuple(rng.choice(elements) if rng.random() < 0.55 else K.zero
                      for i in range(n)) + (rng.choice(elements[1:]),)
            audit_one(K, f, stats)
        stats["fields"].append({"p": p, "m": K.m, "modulus": list(h),
                                "exhaustive_degree_cap": exhaustive_cap,
                                "random_input_count": random_count,
                                "random_degree_cap": random_cap,
                                "inputs": stats["inputs"] - start})

    assert stats["inputs"] == 2855
    assert stats["stages"] == 5758
    assert stats["negative_stages"] == 66
    assert stats["max_denominator_degree"] == 14
    return stats


def large_bit_audit():
    rows = []
    for p, h, k, offset in [
        (2 ** 127 - 1, (0, 1), 7, 3),
        (1000000007, (1, 0, 1), 11, 3),
        (1000000007, (1, 0, 1), 11, 0),
    ]:
        K = ff.FiniteField(p, h)
        alpha = K.one if K.m == 1 else K.basis()[1]
        unit = K.element(17) if K.m == 1 else K.add(K.one, alpha)
        pk = p ** k
        g = (K.neg(alpha), K.one)
        base = sc.dense_power(K, g, offset)
        original = sc.sparse_dense_product(K, {0: K.neg(K.pow(alpha, pk)), pk: K.one}, base)
        original = {n: K.mul(unit, c) for n, c in original.items()}
        assert sc.quotient_multiplicity(K, original, g) == pk + offset
        G = sc.logarithmic_denominator(K, original, [])
        assert G == (g if offset else (K.one,))

        # Known construction has one linear factor. No dense factoring or field
        # enumeration is used for these large-characteristic tests.
        U, V, weight, ledger, steps = original, (K.one,), 1, 0, 0
        while max(U) > 0:
            G = sc.logarithmic_denominator(K, U, [])
            r = sc.quotient_multiplicity(K, U, g) % p if len(G) > 1 else 0
            assert G == (g if r else (K.one,))
            AU = sc.dense_power(K, g, r)
            assert len(V) == 1
            ledger += weight * r
            newU = {n // p: sc.coefficient_root(K, c)
                    for n, c in U.items() if n % p == 0}
            W = ff.trim(K, [sc.coefficient_root(K, AU[j])
                            for j in range(0, len(AU), p)])
            V = ff.mul(K, W, ff.polynomial_pth_root(K, V))
            U = newU
            weight *= p
            steps += 1
        assert ledger == pk + offset and len(V) == 1
        rows.append({"p": p, "modulus": list(h), "k": k, "offset": offset,
                     "characteristic_bits": p.bit_length(), "extension_degree": K.m,
                     "exponent_bits": (pk + offset).bit_length(), "terms": len(original),
                     "steps": steps, "expected_multiplicity": pk + offset,
                     "multiplicity_exact": True, "alpha": list(alpha), "unit": list(unit),
                     "original_sparse_terms": [[n, list(c)] for n, c in sorted(original.items())]})
    assert [(r["characteristic_bits"], r["exponent_bits"], r["steps"]) for r in rows] == [
        (127, 889, 8), (30, 329, 12), (30, 329, 12)]
    return rows


def main():
    before = input_hashes()
    assert before == EXPECTED_INPUT_HASHES, "Frozen input identity changed"
    started = datetime.now(timezone.utc).isoformat()
    timer = time.monotonic()
    small = finite_stage_audit()
    large = large_bit_audit()
    after = input_hashes()
    assert after == before, "An audited input changed during execution"
    result = {
        "test": "Independent extra adversarial sparse stage audit",
        "status": "pass", "started_utc": started,
        "completed_utc": datetime.now(timezone.utc).isoformat(),
        "elapsed_seconds": time.monotonic() - timer,
        "python_version": sys.version, "random_seed": 10072026,
        "script_sha256": sha256(Path(__file__).resolve()),
        "input_sha256": before, "frozen_inputs_unchanged": True,
        "finite_stage_audit": small, "large_bit_audit": large,
        "checks": [
            "visible denominator versus dense factorization",
            "known-factor multiplicities versus dense factorization",
            "U_new = W H_U and V_new divides U_new",
            "new represented polynomial is H_U/H_V",
            "radical containment",
            "denominator degree at level k is at most kD",
            "visible denominator degree at level k is at most (k+1)D",
            "new denominator degree is at most previous degree plus D_F",
            "sparse residue-product degree bound",
            "term count, constant terms, numerator shrinkage and b-stage termination",
            "signed ledger final factorization and original leading unit",
            "large-characteristic and nontrivial coefficient inverse Frobenius",
        ],
        "limitations": [
            "Both feasible-input paths share finite_fields.py arithmetic.",
            "The feasible dense reference uses an exhaustive small-test prime oracle.",
            "Finite checks do not prove the sparse theorem or establish novelty.",
            "No upstream unconditional prime-field theorem certification is supplied.",
        ],
    }
    destination = Path(__file__).resolve().with_name("results.json")
    destination.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": result["status"], "finite_stage_audit": small,
                      "large_bit_case_count": len(large), "output": str(destination)}, sort_keys=True))


if __name__ == "__main__":
    main()
