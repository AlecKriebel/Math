#!/usr/bin/env python3
"""Fail-closed mutations for the literal-map separator certificate.

The principal regression rotates the letters d,e,f in every printed circuit
factor, recomputes the payload seal, and deliberately leaves the literal map
unchanged.  Rejection must therefore come from fresh map expansion rather than
from a stale-hash check.
"""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile


HERE = Path(__file__).resolve().parent
CERTIFICATE = HERE / "K3P_TREE_SUNLET_LITERAL_SEPARATOR_V2.json"
VERIFIER = HERE / "verify_literal_separator_v2.py"


def canonical_bytes(value: dict) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    ).encode("ascii")


def reseal(certificate: dict) -> None:
    certificate.pop("payload_sha256", None)
    certificate["payload_sha256"] = hashlib.sha256(canonical_bytes(certificate)).hexdigest()


def replay(path: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(VERIFIER), "--certificate", str(path)],
        cwd=HERE,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )


def require(condition: bool, message) -> None:
    if not condition:
        raise RuntimeError(message)


def rotate_def_variables(text: str) -> str:
    cycle = {"d": "e", "e": "f", "f": "d"}
    return re.sub(
        r"\b([def])([CGT])\b",
        lambda match: cycle[match.group(1)] + match.group(2),
        text,
    )


def cyclic_factor_rotation(certificate: dict) -> None:
    factor_fields = (
        "literal_sunlet_factor",
        "positive_prefactor",
        "composition_margin",
        "cross_factor",
    )
    for circuit in certificate["circuits"]:
        for field in factor_fields:
            circuit[field] = rotate_def_variables(circuit[field])
    reseal(certificate)


def sign_flip(certificate: dict) -> None:
    circuit = certificate["circuits"][0]
    circuit["factor_sign"] *= -1
    factor = circuit["literal_sunlet_factor"]
    circuit["literal_sunlet_factor"] = factor[1:] if factor.startswith("-") else "-" + factor
    reseal(certificate)


def unsealed_cross_factor_change(certificate: dict) -> None:
    certificate["circuits"][0]["cross_factor"] = "dC*eT+dT*eC*fG"


def run_mutation(name: str, mutate, expected_diagnostic: str, base: dict) -> dict:
    certificate = copy.deepcopy(base)
    mutate(certificate)
    with tempfile.TemporaryDirectory(prefix="k3p-literal-separator-v2-") as directory:
        path = Path(directory) / "certificate.json"
        path.write_text(json.dumps(certificate, indent=2, sort_keys=True) + "\n")
        result = replay(path)
    require(result.returncode != 0, ("mutation survived", name, result.stdout[-2000:]))
    require(
        expected_diagnostic in result.stdout,
        ("wrong mutation diagnostic", name, expected_diagnostic, result.stdout[-2000:]),
    )
    return {
        "name": name,
        "status": "REJECTED",
        "resealed": name != "unsealed_cross_factor_change",
        "expected_diagnostic": expected_diagnostic,
        "diagnostic_observed": True,
    }


def main() -> int:
    base = json.loads(CERTIFICATE.read_text())
    clean = replay(CERTIFICATE)
    require(clean.returncode == 0, ("clean replay failed", clean.stdout[-2000:]))
    cases = [
        run_mutation(
            "cyclic_d_e_f_factor_rotation_after_resealing",
            cyclic_factor_rotation,
            "literal pullback mismatch",
            base,
        ),
        run_mutation(
            "factor_sign_flip_after_resealing",
            sign_flip,
            "literal pullback mismatch",
            base,
        ),
        run_mutation(
            "unsealed_cross_factor_change",
            unsealed_cross_factor_change,
            "payload seal mismatch",
            base,
        ),
    ]
    report = {
        "schema": "k3p-tree-sunlet-literal-separator-v2-mutations-v1",
        "status": "PASS",
        "clean_replays": 1,
        "mutation_count": len(cases),
        "rejected_count": len(cases),
        "survived_count": 0,
        "mutations": cases,
    }
    print("LITERAL_SEPARATOR_V2_MUTATIONS_PASS")
    print(json.dumps(report, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
