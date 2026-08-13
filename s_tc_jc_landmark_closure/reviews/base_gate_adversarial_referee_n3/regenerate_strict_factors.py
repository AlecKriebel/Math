#!/usr/bin/env python3
"""Regenerate the 27 exact n=3 strict-factor witnesses.

This optional regeneration utility uses SymPy only to discover a convenient
factorization.  ``referee_n3.py`` does not import SymPy: it multiplies every
committed factor over the integers, regenerates every Bernstein coefficient,
and compares the resulting certificate with every primary strict-sign claim.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent.parent
RELATIONS = PROJECT / "primary/certificates/hard_cover_n3_schema3_n3_full.jsonl.gz"
POLYNOMIALS = PROJECT / "primary/certificates/hard_cover_polynomials_n3_schema3_n3_full.jsonl.gz"
SUMMARY_SHA256 = "791844a802af61f64cba937a5adbe9d1d381d3fd7e55165914d4e4c885908e65"


def load(path: Path) -> list[dict]:
    with gzip.open(path, "rt", encoding="utf-8") as handle:
        return [json.loads(line) for line in handle]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=HERE / "strict_factor_certificate.json")
    args = parser.parse_args()

    polynomial_rows = {row["polynomial_id"]: row for row in load(POLYNOMIALS)}
    primary = {}
    for row in load(RELATIONS):
        if row["terminal_classification"] != "strict_open_cube_separation":
            continue
        witness = row["probe_witness"]
        primary[witness["target_pullback_id"]] = witness["target_sign_certificate"]

    records = {}
    failures = []
    for polynomial_id, certificate in sorted(primary.items()):
        row = polynomial_rows[polynomial_id]
        variable_count = int(row["variable_count"])
        symbols = sp.symbols(f"z0:{variable_count}")
        expression = sum(
            sp.Integer(coefficient) * sp.prod(
                symbol ** exponent for symbol, exponent in zip(symbols, exponents)
            )
            for exponents, coefficient in row["terms"]
        )
        content, factors = sp.factor_list(sp.expand(expression), *symbols)
        factor_rows = []
        for factor, multiplicity in factors:
            expanded = sp.expand(factor)
            polynomial = sp.Poly(expanded, *symbols, domain=sp.ZZ)
            factor_rows.append({
                "expanded_sha256": hashlib.sha256(str(expanded).encode()).hexdigest(),
                "multiplicity": int(multiplicity),
                "terms": [[list(exponents), int(coefficient)]
                          for exponents, coefficient in polynomial.terms()],
            })
        expected = [(factor["expanded_sha256"], int(factor["multiplicity"]))
                    for factor in certificate["factors"]]
        actual = [(factor["expanded_sha256"], factor["multiplicity"])
                  for factor in factor_rows]
        if actual != expected:
            failures.append([polynomial_id, actual, expected])
        records[polynomial_id] = {
            "variable_count": variable_count,
            "content": int(content),
            "strict_sign": int(certificate["strict_sign"]),
            "factors": factor_rows,
        }

    payload = {
        "schema": "n3-strict-factor-witness-v1",
        "method": (
            "SymPy 1.14 factor discovery; committed verifier checks exact product "
            "and every Bernstein coefficient using stdlib only"
        ),
        "source_summary_sha256": SUMMARY_SHA256,
        "record_count": len(records),
        "factor_count": sum(len(record["factors"]) for record in records.values()),
        "factor_hash_alignment_failures": failures,
        "records": records,
    }
    args.output.write_text(json.dumps(payload, sort_keys=True, indent=2) + "\n")
    print(json.dumps({
        "status": "VERIFIED" if not failures else "FALSE",
        "records": len(records),
        "factors": payload["factor_count"],
        "output": str(args.output),
    }, sort_keys=True))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
