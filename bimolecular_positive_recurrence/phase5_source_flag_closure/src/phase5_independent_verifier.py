#!/usr/bin/env python3
"""Independent deterministic verifier for the Phase-V finite components."""
from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
import json
from math import factorial
from pathlib import Path
from random import Random
import subprocess
import sys
from typing import Sequence

HERE = Path(__file__).resolve().parent
PHASE = HERE.parent
PROJECT = PHASE.parent
sys.path.insert(0, str(PROJECT))

from src.generator import Reaction, propensity_factor  # type: ignore  # noqa:E402
from phase5_source_flag_closure.src.bad_sequence_flags import (  # type: ignore  # noqa:E402
    exhaustive_three_species_audit,
)
from phase5_source_flag_closure.src.complete_credit_elimination import (  # type: ignore  # noqa:E402
    envelope_step,
)
from phase5_source_flag_closure.src.episode_library import (  # type: ignore  # noqa:E402
    enumerate_episode_outcomes,
    expected_template_drift,
    shortest_designated_path,
)
from phase5_source_flag_closure.src.global_foster_verifier import (  # type: ignore  # noqa:E402
    calibration_report,
)
from phase5_source_flag_closure.src.rate_monomial_audit import scan_files  # type: ignore  # noqa:E402
from phase5_source_flag_closure.src.source_rate_flag import (  # type: ignore  # noqa:E402
    bimolecular_complexes,
    dot,
    top_availability_or_conservation,
)

MODULES = (
    "phase5_source_flag_closure.src.target_source_residual",
    "phase5_source_flag_closure.src.complete_credit_elimination",
    "phase5_source_flag_closure.src.episode_library",
    "phase5_source_flag_closure.src.source_rate_flag",
    "phase5_source_flag_closure.src.bad_sequence_flags",
    "phase5_source_flag_closure.src.zero_layer_gluing",
    "phase5_source_flag_closure.src.defect_promotion",
    "phase5_source_flag_closure.src.regime_rank",
    "phase5_source_flag_closure.src.bounded_defect_full_audit",
    "phase5_source_flag_closure.src.uniformization",
    "phase5_source_flag_closure.src.global_foster_verifier",
    "phase5_source_flag_closure.src.rate_monomial_audit",
)

KEY_FILES = (
    "theorem_statement.md",
    "complete_credit_elimination.md",
    "source_rate_flag_theorem.md",
    "zero_layer_gluing.md",
    "defect_promotion.md",
    "global_foster_theorem.md",
    "proof_audit.md",
    "technical_summary.md",
    "src/target_source_residual.py",
    "src/complete_credit_elimination.py",
    "src/episode_library.py",
    "src/source_rate_flag.py",
    "src/uniformization.py",
    "main_manuscript.tex",
    "main_manuscript.pdf",
)


def _run_self_tests() -> dict[str, dict[str, object]]:
    results: dict[str, dict[str, object]] = {}
    for module in MODULES:
        cp = subprocess.run(
            [sys.executable, "-m", module],
            cwd=PROJECT,
            env={**__import__("os").environ, "PYTHONPATH": str(PROJECT)},
            text=True,
            capture_output=True,
            timeout=60,
        )
        results[module] = {
            "returncode": cp.returncode,
            "stdout_last_line": cp.stdout.strip().splitlines()[-1] if cp.stdout.strip() else "",
            "stderr": cp.stderr.strip(),
        }
        if cp.returncode:
            raise RuntimeError(f"self-test failed for {module}: {cp.stderr}")
    return results


def _run_pytest() -> dict[str, object]:
    cp = subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            "-q",
            "phase2_trigger_drain/tests",
            "phase5_source_flag_closure/tests",
        ],
        cwd=PROJECT,
        env={**__import__("os").environ, "PYTHONPATH": str(PROJECT)},
        text=True,
        capture_output=True,
        timeout=120,
    )
    if cp.returncode:
        raise RuntimeError(cp.stdout + cp.stderr)
    return {"returncode": cp.returncode, "stdout": cp.stdout.strip()}


def _independent_residual_identity() -> dict[str, int]:
    checked = 0
    complexes = bimolecular_complexes(2)
    for x0 in range(7):
        for x1 in range(7):
            x = (x0, x1)
            enabled = [y for y in complexes if all(xi >= yi for xi, yi in zip(x, y))]
            for t in enabled:
                for s in enabled:
                    lhs = Fraction(propensity_factor(x, t), propensity_factor(x, s))
                    rhs = Fraction(
                        factorial(x0 - s[0]) * factorial(x1 - s[1]),
                        factorial(x0 - t[0]) * factorial(x1 - t[1]),
                    )
                    if lhs != rhs:
                        raise AssertionError("independent residual identity failed")
                    checked += 1
    return {"small_state_identities": checked}


def _independent_envelope_audit() -> dict[str, int]:
    checked = 0
    for remaining in (-0.1, -1, -5, -50, -500):
        for q in (0.1, 0.25, 0.5, 1.0):
            for c0 in (0.0, 1.5, 4.0):
                cert = envelope_step(remaining, c0, q)
                # Concavity and derivative characterize the maximum exactly.
                derivative = 1.0 / cert.maximizer + q * remaining
                if cert.branch == "interior" and abs(derivative) > 1e-10:
                    raise AssertionError("interior envelope derivative is nonzero")
                if cert.branch == "boundary" and 1 + q * remaining < -1e-12:
                    raise AssertionError("wrong boundary envelope branch")
                checked += 1
    return {"calculus_cases": checked}


def _independent_episode_audit() -> dict[str, object]:
    reactions = (
        Reaction((0, 0), (1, 1), Fraction(2)),
        Reaction((1, 1), (0, 1), Fraction(3)),
        Reaction((0, 1), (0, 0), Fraction(5)),
    )
    path = shortest_designated_path(reactions, (0, 0), (0, 1))
    rows = []
    for n in (1, 2, 5, 10, 100, 1000):
        recursion, _ = expected_template_drift(reactions, (n, 0), path)
        branches = enumerate_episode_outcomes(reactions, (n, 0), path)
        enumerated = sum(float(p) * reward for p, reward in branches)
        if abs(recursion - enumerated) > 1e-12:
            raise AssertionError("episode recursion differs from branch enumeration")
        rows.append((n, recursion, len(branches)))
    return {"rows": rows}


def _independent_top_random_audit(cases: int = 20000) -> dict[str, int]:
    rng = Random(731947)
    allc = bimolecular_complexes(4)
    availability = 0
    conservation = 0
    for _ in range(cases):
        C = tuple(y for y in allc if rng.random() < 0.35)
        if not C:
            C = (allc[rng.randrange(len(allc))],)
        I = {i for i in range(4) if rng.random() < 0.6}
        if not I:
            I = {rng.randrange(4)}
        w = [Fraction(0)] * 4
        while not any(w):
            for i in I:
                w[i] = Fraction(rng.randrange(5))
        cert = top_availability_or_conservation(C, I, w)
        if cert.source is not None:
            s, c = cert.source, cert.terminal
            if c is None or dot(w, s) <= dot(w, c):
                raise AssertionError("random availability certificate has no strict gap")
            if any(s[j] > c[j] for j in range(4) if j not in I):
                raise AssertionError("bounded reactant is unavailable")
            availability += 1
        else:
            vector = cert.conservation
            if vector is None or len({dot(vector, y) for y in C}) != 1:
                raise AssertionError("random conservation certificate failed")
            conservation += 1
    return {"cases": cases, "availability": availability, "conservation": conservation}


def _hash_files() -> dict[str, str]:
    result: dict[str, str] = {}
    for relative in KEY_FILES:
        path = PHASE / relative
        result[relative] = sha256(path.read_bytes()).hexdigest()
    return result


def run() -> dict[str, object]:
    stored_audit_path = PHASE / "certificates" / "top_availability_audit.json"
    stored_audit = json.loads(stored_audit_path.read_text())
    recomputed_audit = exhaustive_three_species_audit()
    if stored_audit != recomputed_audit:
        raise AssertionError("stored top-availability audit does not reproduce")

    docs = [PHASE / name for name in KEY_FILES if name.endswith(".md")]
    rate_findings = scan_files(docs)
    if rate_findings:
        raise AssertionError(f"prohibited rate-comparison language found: {rate_findings}")

    result: dict[str, object] = {
        "self_tests": _run_self_tests(),
        "pytest": _run_pytest(),
        "residual_identity": _independent_residual_identity(),
        "envelope": _independent_envelope_audit(),
        "episode": _independent_episode_audit(),
        "top_random_four_species": _independent_top_random_audit(),
        "top_exhaustive_three_species": recomputed_audit,
        "calibrations": calibration_report(),
        "rate_monomial_scan": "clean",
        "file_sha256": _hash_files(),
    }
    canonical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["verification_sha256"] = sha256(canonical.encode("utf-8")).hexdigest()
    return result


def main() -> None:
    result = run()
    destination = PHASE / "certificates" / "independent_verification.json"
    destination.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
