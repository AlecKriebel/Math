#!/usr/bin/env python3
"""Mutations for the literal K2P quartet semantics gate."""

from __future__ import annotations

import copy
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Callable


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
SPEC = HERE / "QUARTET_SEMANTICS_SPEC.json"
VERIFIER = HERE / "verify_quartet_logic.py"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def run_spec_mutation(
    root: Path,
    name: str,
    mutate: Callable[[dict[str, Any]], None],
    expected_marker: str,
) -> dict[str, Any]:
    spec = json.loads(SPEC.read_text(encoding="utf-8"))
    mutate(spec)
    path = root / f"{name}.json"
    path.write_text(json.dumps(spec, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    output = root / f"{name}-certificate.json"
    result = subprocess.run(
        [
            sys.executable,
            "-B",
            str(VERIFIER),
            "--project",
            str(PROJECT),
            "--spec",
            str(path),
            "--output",
            str(output),
            "--skip-document-binding",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        check=False,
    )
    require(result.returncode != 0, f"mutation accepted:{name}")
    require(expected_marker in result.stdout, f"wrong diagnostic:{name}:{result.stdout}")
    require(not output.exists(), f"failed mutation wrote certificate:{name}")
    return {
        "case": name,
        "status": "PASS",
        "expected_marker": expected_marker,
        "observed_returncode": result.returncode,
        "stdout_sha256": hashlib.sha256(result.stdout.encode()).hexdigest(),
    }


def run_document_mutation(root: Path) -> dict[str, Any]:
    project = root / "document-project"
    spec = json.loads(SPEC.read_text(encoding="utf-8"))
    for contract in spec["document_contracts"]:
        relative = Path(contract["path"])
        destination = project / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(PROJECT / relative, destination)
    article = project / "proof_compression_submission/article/main.tex"
    text = article.read_text(encoding="utf-8")
    old = "F_A&=q_{CCCC}-q_{CCTT}"
    require(text.count(old) == 1, "article mutation anchor")
    article.write_text(text.replace(old, "F_A&=q_{GGGG}-q_{GGTT}"), encoding="utf-8")
    output = root / "document-certificate.json"
    result = subprocess.run(
        [
            sys.executable,
            "-B",
            str(VERIFIER),
            "--project",
            str(project),
            "--spec",
            str(SPEC),
            "--output",
            str(output),
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        check=False,
    )
    marker = "DOCUMENT_LITERAL_BINDING_FAIL"
    require(result.returncode != 0 and marker in result.stdout, "document mutation accepted")
    require(not output.exists(), "document mutation wrote certificate")
    return {
        "case": "printed_formula_reverted_to_wrong_sector",
        "status": "PASS",
        "expected_marker": marker,
        "observed_returncode": result.returncode,
        "stdout_sha256": hashlib.sha256(result.stdout.encode()).hexdigest(),
    }


def main() -> None:
    if not __debug__:
        raise SystemExit("QUARTET_MUTATIONS_OPTIMIZED_MODE_FORBIDDEN")
    with tempfile.TemporaryDirectory(prefix="k2p-quartet-mutations-") as directory:
        root = Path(directory)
        rows = [
            run_spec_mutation(
                root,
                "spectrum_G_T_swap",
                lambda spec: spec["edge_spectrum"].update({"G": "s", "T": "g"}),
                "EQUAL_SECTOR_SPECTRUM_FAIL",
            ),
            run_spec_mutation(
                root,
                "wrong_F_coordinate",
                lambda spec: spec["canonical_formulas"]["F_A"][0].__setitem__(1, "GGGG"),
                "CANONICAL_PULLBACK_FAIL",
            ),
            run_spec_mutation(
                root,
                "wrong_J_coefficient",
                lambda spec: spec["canonical_formulas"]["J_B"][2].__setitem__(0, -1),
                "CANONICAL_PULLBACK_FAIL",
            ),
            run_spec_mutation(
                root,
                "wrong_character_order",
                lambda spec: spec.__setitem__("character_order", ["0", "C", "T", "G"]),
                "CHARACTER_ORDER_CONTRACT_FAIL",
            ),
            run_spec_mutation(
                root,
                "wrong_coordinate_dictionary",
                lambda spec: spec["canonical_coordinates"].__setitem__("QA", "GGTT"),
                "CANONICAL_COORDINATE_CONTRACT_FAIL",
            ),
            run_spec_mutation(
                root,
                "wrong_D_plus_declaration",
                lambda spec: spec["domain"].__setitem__("principal", "0<s<1, 0<g<1, g>=2s-1"),
                "DOMAIN_DECLARATION_CONTRACT_FAIL",
            ),
            run_document_mutation(root),
        ]
        optimized = subprocess.run(
            [sys.executable, "-O", str(VERIFIER)],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            check=False,
        )
        require(
            optimized.returncode != 0
            and "QUARTET_LOGIC_OPTIMIZED_MODE_FORBIDDEN" in optimized.stdout,
            "optimized verifier accepted",
        )
        rows.append(
            {
                "case": "optimized_python",
                "status": "PASS",
                "expected_marker": "QUARTET_LOGIC_OPTIMIZED_MODE_FORBIDDEN",
                "observed_returncode": optimized.returncode,
                "stdout_sha256": hashlib.sha256(optimized.stdout.encode()).hexdigest(),
            }
        )

    payload = {
        "schema": "k2p-quartet-semantics-mutations-v2",
        "status": "PASS",
        "verifier_sha256": sha_file(VERIFIER),
        "spec_sha256": sha_file(SPEC),
        "case_count": len(rows),
        "cases": rows,
    }
    result = dict(payload)
    result["payload_sha256"] = hashlib.sha256(canonical(payload)).hexdigest()
    output = HERE / "quartet_semantics_mutation_certificate.json"
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("K2P_QUARTET_SEMANTICS_MUTATIONS_PASS")
    print(json.dumps({"cases": len(rows), "payload_sha256": result["payload_sha256"]}, sort_keys=True))


if __name__ == "__main__":
    main()
