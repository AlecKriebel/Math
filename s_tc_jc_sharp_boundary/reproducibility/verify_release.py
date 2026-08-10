#!/usr/bin/env python3
"""Fail-closed verifier for the sharpness-only release."""
from __future__ import annotations

import hashlib
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "MANIFEST.sha256"
INDEPENDENT_SCRIPT_SHA256 = "93a29ea6fdd1eba1671cf720a3929c2e2cab6ef5882c89a355d7cef04406c639"
INDEPENDENT_INSTANCE_SHA256 = "cca38c3928c7eb768f5dabf480d8eae16ef5a08b7576ffe2780e6a7deaeb337b"
INDEPENDENT_CERTIFICATE_SHA256 = "38266537a7966d83bdb94c6fb90fa68f93fbd227b82579f1bf311005925366d7"
IGNORED_PARTS = {".git", "__pycache__", ".pytest_cache", ".mypy_cache", "tmp"}
IGNORED_SUFFIXES = {".pyc", ".pyo"}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def included(path: Path) -> bool:
    rel = path.relative_to(ROOT)
    if path == MANIFEST or not path.is_file():
        return False
    if any(part in IGNORED_PARTS for part in rel.parts):
        return False
    if path.suffix in IGNORED_SUFFIXES or path.name == ".DS_Store":
        return False
    return True


def verify_manifest() -> None:
    if not MANIFEST.is_file():
        raise AssertionError("MANIFEST.sha256 is missing")
    expected: dict[str, str] = {}
    for line_number, raw in enumerate(MANIFEST.read_text(encoding="utf-8").splitlines(), 1):
        digest, separator, rel = raw.partition("  ")
        if separator != "  " or len(digest) != 64 or not rel:
            raise AssertionError(f"malformed manifest line {line_number}")
        if rel in expected:
            raise AssertionError(f"duplicate manifest path: {rel}")
        expected[rel] = digest

    actual_paths = {
        path.relative_to(ROOT).as_posix()
        for path in ROOT.rglob("*")
        if included(path)
    }
    if set(expected) != actual_paths:
        missing = sorted(set(expected) - actual_paths)
        unexpected = sorted(actual_paths - set(expected))
        raise AssertionError(f"manifest path mismatch; missing={missing}, unexpected={unexpected}")
    for rel, wanted in expected.items():
        got = sha256(ROOT / rel)
        if got != wanted:
            raise AssertionError(f"hash mismatch for {rel}: {got} != {wanted}")
    print(f"VERIFIED manifest ({len(expected)} files)")


def run_exact(label: str, command: list[str], env: dict[str, str] | None = None) -> str:
    completed = subprocess.run(
        command,
        cwd=ROOT,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    print(completed.stdout, end="")
    if completed.returncode != 0:
        raise AssertionError(f"{label} failed with exit code {completed.returncode}")
    print(f"VERIFIED {label}")
    return completed.stdout


def verify_scope_contract() -> None:
    manuscript = " ".join(
        (ROOT / "source/paper/main.tex").read_text(encoding="utf-8").split()
    )
    readme = " ".join((ROOT / "README.md").read_text(encoding="utf-8").split())
    required = [
        "Weakly Tree-Child Level-2 Networks",
        "For every $n\\ge4$",
        "Let $X$ be nonempty",
        "replace leaf $2$ in both networks",
        "settles neither identifiability inside $\\TCs$ nor",
        "triangle-free subclass of $\\TCw$",
        "Earlier automated drafts overclaimed a",
        "global positive classification",
    ]
    for text in required:
        if text not in manuscript:
            raise AssertionError(f"required scope statement missing from manuscript: {text}")
    if "unresolved, not refuted" not in readme:
        raise AssertionError("README does not preserve the positive theorem's unresolved status")
    if "Generic Identifiability of Strongly Tree-Child Level-2" in manuscript:
        raise AssertionError("withdrawn positive title leaked into active manuscript")
    pdf = ROOT / "submission/Weakly_Tree_Child_Level2_JC_Ambiguity.pdf"
    if not pdf.is_file() or pdf.stat().st_size < 50_000:
        raise AssertionError("submission PDF is missing or implausibly small")
    print("VERIFIED manuscript scope and submission-PDF contract")


def verify_independent() -> None:
    script = ROOT / "reproducibility/independent/verify_sharpness.py"
    instance = ROOT / "reproducibility/independent/instance.json"
    expected = ROOT / "reproducibility/independent/expected_certificate.json"
    if sha256(script) != INDEPENDENT_SCRIPT_SHA256:
        raise AssertionError("independent verifier source hash changed")
    if sha256(instance) != INDEPENDENT_INSTANCE_SHA256:
        raise AssertionError("independent primitive instance hash changed")
    if sha256(expected) != INDEPENDENT_CERTIFICATE_SHA256:
        raise AssertionError("expected independent certificate hash changed")
    with tempfile.TemporaryDirectory(prefix="stc-jc-independent-") as tmp:
        generated = Path(tmp) / "certificate.json"
        env = os.environ.copy()
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        env["PYTHONHASHSEED"] = "0"
        output = run_exact(
            "independent sharpness implementation",
            [sys.executable, str(script), "--instance", str(instance), "--output", str(generated)],
            env,
        )
        if "PASS final_verdict=PROVED" not in output:
            raise AssertionError("independent verifier did not emit its proved verdict")
        if sha256(generated) != INDEPENDENT_CERTIFICATE_SHA256:
            raise AssertionError("independent certificate digest changed")
        if generated.read_bytes() != expected.read_bytes():
            raise AssertionError("independent certificate bytes differ from expected certificate")


def main() -> None:
    verify_manifest()
    verify_scope_contract()
    primary_output = run_exact(
        "primary symbolic implementation",
        [sys.executable, str(ROOT / "reproducibility/verify_primary.py")],
        {**os.environ, "PYTHONDONTWRITEBYTECODE": "1", "PYTHONHASHSEED": "0"},
    )
    if "[PROVED] CERTIFICATE COMPLETE" not in primary_output:
        raise AssertionError("primary implementation did not emit its proved verdict")
    verify_independent()
    print("VERIFIED: all sharpness-release gates passed")


if __name__ == "__main__":
    main()
