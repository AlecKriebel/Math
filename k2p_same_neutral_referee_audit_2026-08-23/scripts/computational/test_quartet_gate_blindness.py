#!/usr/bin/env python3
"""Demonstrate that the quartet gate is blind to printed Fourier semantics.

All copies and mutations are made in the audit output directory.  The sealed
submission is opened read-only.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
from pathlib import Path


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def mutate_once(text: str, old: str, new: str, code: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{code}: expected one occurrence, observed {count}")
    return text.replace(old, new)


def run_variant(project: Path, output: Path, name: str, mutate_article, mutate_proof):
    root = output / name
    if root.exists():
        shutil.rmtree(root)
    article_dir = root / "proof_compression_submission/article"
    closure_dir = root / "work/quartet_separation_closure"
    article_dir.mkdir(parents=True)
    closure_dir.mkdir(parents=True)
    sources = {
        "article": project / "proof_compression_submission/article/main.tex",
        "proof": project / "work/quartet_separation_closure/PROOF.md",
        "verifier": project / "work/quartet_separation_closure/verify_quartet_logic.py",
        "certificate": project / "work/quartet_separation_closure/quartet_logic_certificate.json",
    }
    article = article_dir / "main.tex"
    proof = closure_dir / "PROOF.md"
    verifier = closure_dir / "verify_quartet_logic.py"
    certificate = closure_dir / "quartet_logic_certificate.json"
    article.write_text(mutate_article(sources["article"].read_text()))
    proof.write_text(mutate_proof(sources["proof"].read_text()))
    shutil.copy2(sources["verifier"], verifier)
    shutil.copy2(sources["certificate"], certificate)
    proc = subprocess.run(
        ["python3", "-B", str(verifier)], cwd=closure_dir,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
    )
    return {
        "variant": name,
        "exit_status": proc.returncode,
        "stdout": proc.stdout,
        "stdout_sha256": hashlib.sha256(proc.stdout.encode()).hexdigest(),
        "source_sha256": {key: sha(path) for key, path in sources.items()},
        "mutated_sha256": {
            "article": sha(article), "proof": sha(proof),
            "verifier": sha(verifier), "certificate": sha(certificate),
        },
        "verifier_and_certificate_unchanged": (
            sha(verifier) == sha(sources["verifier"])
            and sha(certificate) == sha(sources["certificate"])
        ),
        "passed": proc.returncode == 0 and "PASS" in proc.stdout,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    project = args.project.resolve()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)

    spectrum = run_variant(
        project, output, "mutated_spectrum",
        lambda text: mutate_once(text, r"(1,s_e,g_e,s_e)", r"(1,s_e,s_e,g_e)", "SPECTRUM_PATTERN"),
        lambda text: text,
    )

    def article_polynomial(text: str) -> str:
        text = text.replace("q_{GGGG}-q_{GGTT}-q_{GTTG}+q_{GTGT}",
                            "q_{CCCC}-q_{CCTT}-q_{CTTC}+q_{CTCT}")
        text = text.replace("q_{GGGG}-q_{GGTT}", "q_{CCCC}-q_{CCTT}")
        return text

    def proof_polynomial(text: str) -> str:
        return (text.replace("q_{GGGG}-q_{GGTT}-q_{GTTG}+q_{GTGT}",
                             "q_{CCCC}-q_{CCTT}-q_{CTTC}+q_{CTCT}")
                    .replace("q_{GGGG}-q_{GGTT}", "q_{CCCC}-q_{CCTT}"))

    polynomial = run_variant(project, output, "mutated_polynomial_labels", article_polynomial, proof_polynomial)
    result = {
        "schema": "quartet-gate-semantic-blindness-v1",
        "claim": "The current quartet verifier does not bind either the printed spectrum convention or printed polynomial coordinate labels.",
        "variants": [spectrum, polynomial],
        "status": "PASS" if spectrum["passed"] and polynomial["passed"] else "FAIL",
    }
    payload = dict(result)
    result["payload_sha256"] = hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    report = output / "quartet_gate_blindness.json"
    report.write_text(json.dumps(result, sort_keys=True, indent=2) + "\n")
    print(json.dumps({"status": result["status"], "payload_sha256": result["payload_sha256"]}, sort_keys=True))


if __name__ == "__main__":
    main()
