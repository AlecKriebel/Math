#!/usr/bin/env python3
"""Exact internal-consistency replay for the cut assignment table.

The supplied file is small enough to load directly.  This verifies every
embedded graph/tensor/polynomial/sign cross-link.  It intentionally does not
claim primitive-universe exhaustiveness because the primitive compiler modules
needed to regenerate that universe are absent from the package.
"""

from __future__ import annotations

import argparse
from collections import Counter
from math import comb
from hashlib import sha256
import json
from pathlib import Path

from direction_sign_logic import bernstein_strict_sign, compact_sha, verify_sign_record


def file_sha(path: Path) -> str:
    h = sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def verify_partial_certificate(certificate: dict) -> dict:
    """Independently replay a Bernstein-in-inheritance sign certificate."""
    import sympy as sp

    partial = certificate["partial_certificate"]
    inheritance = tuple(sp.Symbol(name) for name in partial["inheritance_variables"])
    degrees = tuple(int(value) for value in partial["degrees"])
    rebuilt = sp.Integer(0)
    nonzero = 0
    strict = 0
    weak_signs = set()
    for row in partial["coefficients"]:
        index = tuple(int(value) for value in row["index"])
        if row["zero"]:
            coefficient_expression = sp.Integer(0)
        else:
            nonzero += 1
            item = row["coefficient_certificate"]
            coefficient_expression = sp.sympify(item["expression"])
            product_expression = sp.Rational(item["coefficient"])
            sign = 1 if sp.Rational(item["coefficient"]) > 0 else -1
            all_strict = True
            for factor_row in item["factors"]:
                factor = sp.sympify(factor_row["factor"])
                exponent = int(factor_row["exponent"])
                product_expression *= factor**exponent
                symbols = tuple(sorted(factor.free_symbols, key=str))
                try:
                    direct_factor_sign = bernstein_strict_sign(factor, symbols)
                    factor_strict = True
                except ValueError:
                    direct_factor_sign = None
                    factor_strict = False
                if direct_factor_sign is not None:
                    factor_sign = direct_factor_sign
                elif exponent % 2 == 0:
                    # A crossing factor can still be weakly nonnegative after
                    # an even power; its stored base sign is conventional and
                    # disappears after exponentiation.
                    factor_sign = int(factor_row["factor_sign"])
                else:
                    raise AssertionError("odd weak-only factor has no sign proof")
                if factor_strict != bool(factor_row["strict_on_open_cube"]):
                    raise AssertionError(("coefficient factor strictness", str(factor), factor_strict, factor_row["strict_on_open_cube"]))
                if factor_sign != int(factor_row["factor_sign"]):
                    raise AssertionError(("coefficient factor sign", str(factor), exponent, factor_sign, factor_row["factor_sign"]))
                sign *= factor_sign**exponent
                all_strict &= factor_strict
            if sp.expand(coefficient_expression - product_expression) != 0:
                raise AssertionError("partial coefficient factorization")
            if sign != int(item["weak_sign"]):
                raise AssertionError("partial coefficient sign")
            if all_strict != bool(item["strict"]):
                raise AssertionError("partial coefficient strictness")
            weak_signs.add(sign)
            strict += int(all_strict)
        basis = sp.Integer(1)
        for variable, i, degree in zip(inheritance, index, degrees):
            basis *= comb(degree, i) * variable**i * (1 - variable) ** (degree - i)
        rebuilt += coefficient_expression * basis
    if len(partial["coefficients"]) != partial["coefficient_count"]:
        raise AssertionError("partial coefficient count")
    if nonzero != partial["nonzero_count"] or (strict > 0) != bool(partial["at_least_one_coefficient_strict"]):
        raise AssertionError("partial nonzero/strict count")
    if weak_signs != {int(partial["total_sign"])}:
        raise AssertionError("partial total sign")
    if sp.expand(sp.sympify(certificate["expression"]) - rebuilt) != 0:
        raise AssertionError("partial Bernstein reconstruction")
    if int(certificate["total_sign"]) != int(partial["total_sign"]):
        raise AssertionError("outer partial sign")
    return {"coefficient_count": len(partial["coefficients"]), "nonzero": nonzero, "strict": strict}


def audit(path: Path) -> dict:
    data = json.loads(path.read_text())
    endpoints = data["endpoint_records"]
    singles = data["single_blob_records"]
    if len(endpoints) != data["endpoint_type_count"] or len(singles) != data["single_blob_type_count"]:
        raise AssertionError("top-level type counts")
    if [row["id"] for row in endpoints] != list(range(len(endpoints))):
        raise AssertionError("endpoint IDs")
    if [row["id"] for row in singles] != list(range(len(singles))):
        raise AssertionError("single-blob IDs")

    sign_cache: dict[str, dict] = {}
    graph_keys = set()
    signed = 0
    zero = 0
    for family, rows in (("endpoint", endpoints), ("single_blob", singles)):
        for row in rows:
            graph = row["graph"]
            if sha256(graph["graph_code"].encode()).hexdigest() != graph["graph_sha256"]:
                raise AssertionError((family, row["id"], "graph hash"))
            if compact_sha(graph["switchings"]) != graph["switching_sha256"]:
                raise AssertionError((family, row["id"], "switching hash"))
            if sha256(row["type_key"].encode()).hexdigest() != row["tensor_sha256"]:
                raise AssertionError((family, row["id"], "tensor hash"))
            key = (family, graph["graph_sha256"], graph["switching_sha256"], row["tensor_sha256"])
            if key in graph_keys:
                raise AssertionError((family, row["id"], "duplicate graph/tensor row"))
            graph_keys.add(key)

            tested = row["tested_polynomial"]
            binding = row["sign_binding"]
            if tested.get("zero") is True:
                zero += 1
                if binding is not None or row.get("minor") is not None:
                    raise AssertionError((family, row["id"], "zero row carries strict witness"))
                continue
            signed += 1
            canonical = tested["canonical"]
            term_hash = sha256(json.dumps(canonical["terms"], separators=(",", ":")).encode()).hexdigest()
            if term_hash != canonical["hash"] or term_hash != binding["polynomial_hash"]:
                raise AssertionError((family, row["id"], "polynomial hash"))
            if tested["expression"] != binding["sign_certificate"]["expression"]:
                raise AssertionError((family, row["id"], "expression/sign binding"))
            if canonical["scale"] != binding["derived_scale"]:
                raise AssertionError((family, row["id"], "scale binding"))
            certificate_key = compact_sha(binding["sign_certificate"])
            if certificate_key not in sign_cache:
                certificate = binding["sign_certificate"]
                sign_cache[certificate_key] = (
                    verify_partial_certificate(certificate)
                    if "partial_certificate" in certificate
                    else verify_sign_record({"certificate": certificate})
                )

    endpoint_counts = Counter(row["branch"] for row in endpoints)
    single_counts = Counter(row["classification"] for row in singles)
    if dict(endpoint_counts) != data["endpoint_dichotomy"]:
        raise AssertionError("endpoint dichotomy")
    if dict(single_counts) != data["single_blob_classification"]:
        raise AssertionError("single-blob classification")
    if zero != single_counts["rank_one_all_blocks"]:
        raise AssertionError("rank-one zero count")
    if any(row["displayed_bridge"] != (row["classification"] == "rank_one_all_blocks") for row in singles):
        raise AssertionError("displayed-bridge classification")

    return {
        "path": str(path),
        "sha256": file_sha(path),
        "endpoint_records": len(endpoints),
        "endpoint_dichotomy": dict(endpoint_counts),
        "single_blob_records": len(singles),
        "single_blob_classification": dict(single_counts),
        "signed_records": signed,
        "zero_records": zero,
        "distinct_sign_certificates_recomputed": len(sign_cache),
        "status": "EXACTLY COMPUTED",
        "limit": "internal table consistency only; primitive generator/compiler sources are unavailable",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("assignment", type=Path)
    args = parser.parse_args()
    print(json.dumps(audit(args.assignment), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
