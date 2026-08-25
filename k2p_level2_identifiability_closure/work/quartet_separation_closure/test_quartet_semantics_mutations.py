#!/usr/bin/env python3
"""Mutations for the literal K2P quartet semantics gate."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
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
AUTHORITATIVE_OUTPUT = HERE / "quartet_semantics_mutation_certificate.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def observed_semantic_marker(output: str, expected: str) -> str:
    """Extract the final exception code without retaining traceback bytes."""

    matches: list[str] = []
    for line in output.splitlines():
        stripped = line.strip()
        diagnostic = (
            stripped.partition(": ")[2]
            if stripped.startswith("QuartetFailure: ")
            else stripped
        )
        code = diagnostic.split(":", 1)[0]
        if code == expected:
            matches.append(code)
    require(
        matches == [expected],
        f"wrong diagnostic marker:{expected}:{matches}",
    )
    return matches[0]


def validate_output_path(output: Path, allow_authoritative_output: bool) -> Path:
    """Keep routine mutation output disposable and outside the source tree.

    ``resolve`` is intentional: an output symlink, or a non-existing output
    below a symlinked directory, must not provide a route back into the source
    checkout.  Resealing the one canonical certificate is a separate explicit
    operation; the override never licenses any other in-tree or external path.
    """

    lexical = Path(os.path.abspath(os.fspath(output)))
    normalized = lexical.parent.resolve() / lexical.name
    resolved = lexical.resolve()
    project = PROJECT.resolve()
    authoritative = AUTHORITATIVE_OUTPUT.parent.resolve() / AUTHORITATIVE_OUTPUT.name
    if allow_authoritative_output:
        if normalized != authoritative or lexical.is_symlink():
            raise SystemExit(
                "QUARTET_MUTATION_OUTPUT_POLICY_FAIL: authoritative override "
                "licenses only the nonsymbolic canonical mutation certificate:"
                f"output={normalized}:canonical={authoritative}:"
                f"is_symlink={lexical.is_symlink()}"
            )
        return normalized
    try:
        resolved.relative_to(project)
    except ValueError:
        return normalized
    raise SystemExit(
        "QUARTET_MUTATION_OUTPUT_POLICY_FAIL: routine output must be outside "
        "the project source tree"
    )


def atomic_write_text(path: Path, text: str) -> None:
    """Fsync a new same-directory file, then replace the output entry.

    Replacement never follows an output-file symlink and breaks any external
    hardlink instead of truncating the shared source inode.
    """

    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=path.parent
    )
    temporary = Path(temporary_name)
    try:
        os.fchmod(descriptor, 0o644)
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
        directory_descriptor = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(directory_descriptor)
        finally:
            os.close(directory_descriptor)
    finally:
        if temporary.exists():
            temporary.unlink()


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
    observed_marker = observed_semantic_marker(result.stdout, expected_marker)
    require(not output.exists(), f"failed mutation wrote certificate:{name}")
    return {
        "case": name,
        "status": "PASS",
        "expected_marker": expected_marker,
        "observed_marker": observed_marker,
        "observed_returncode": result.returncode,
        "failed_mutation_certificate_written": False,
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
    require(result.returncode != 0, "document mutation accepted")
    observed_marker = observed_semantic_marker(result.stdout, marker)
    require(not output.exists(), "document mutation wrote certificate")
    return {
        "case": "printed_formula_reverted_to_wrong_sector",
        "status": "PASS",
        "expected_marker": marker,
        "observed_marker": observed_marker,
        "observed_returncode": result.returncode,
        "failed_mutation_certificate_written": False,
    }


def main() -> None:
    if not __debug__:
        raise SystemExit("QUARTET_MUTATIONS_OPTIMIZED_MODE_FORBIDDEN")
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--allow-authoritative-output", action="store_true")
    args = parser.parse_args()
    output = validate_output_path(args.output, args.allow_authoritative_output)
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
        optimized_output = root / "optimized-certificate.json"
        optimized = subprocess.run(
            [
                sys.executable,
                "-O",
                str(VERIFIER),
                "--output",
                str(optimized_output),
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            check=False,
        )
        optimized_marker = "QUARTET_LOGIC_OPTIMIZED_MODE_FORBIDDEN"
        require(optimized.returncode != 0, "optimized verifier accepted")
        observed_optimized_marker = observed_semantic_marker(
            optimized.stdout, optimized_marker
        )
        require(not optimized_output.exists(), "optimized verifier wrote certificate")
        rows.append(
            {
                "case": "optimized_python",
                "status": "PASS",
                "expected_marker": optimized_marker,
                "observed_marker": observed_optimized_marker,
                "observed_returncode": optimized.returncode,
                "failed_mutation_certificate_written": False,
            }
        )

    payload = {
        "schema": "k2p-quartet-semantics-mutations-v3",
        "status": "PASS",
        "verifier_sha256": sha_file(VERIFIER),
        "spec_sha256": sha_file(SPEC),
        "diagnostic_contract": (
            "Each child must return nonzero, emit the exact stored semantic marker, "
            "and leave its requested verifier-certificate path absent. Raw tracebacks "
            "are deliberately excluded because paths and formatting are nonportable."
        ),
        "case_count": len(rows),
        "cases": rows,
    }
    result = dict(payload)
    result["payload_sha256"] = hashlib.sha256(canonical(payload)).hexdigest()
    atomic_write_text(output, json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("K2P_QUARTET_SEMANTICS_MUTATIONS_PASS")
    print(json.dumps({"cases": len(rows), "payload_sha256": result["payload_sha256"]}, sort_keys=True))


if __name__ == "__main__":
    main()
