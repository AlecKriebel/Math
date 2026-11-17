#!/usr/bin/env python3
"""Reproduce finite exact checks and validate the public package's inventory.

Standard library only. This does not prove the analytic theorem, build Lean,
extract its axioms, or establish priority. Those limits are recorded explicitly.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as F
import hashlib
import json
import os
from pathlib import Path
import platform
import random
import re
import shutil
import subprocess
import sys
import tempfile

PIN = "adc7f1241b42e322a6451854ab7e4b4c146bf78a"
TITLE = "Even Minkowski uniqueness as a consequence of logarithmic Brunn–Minkowski"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(command: list[str], cwd: Path, timeout: int = 120) -> dict:
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    result = subprocess.run(command, cwd=cwd, env=env, text=True,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                            timeout=timeout, check=False)
    if result.returncode:
        raise RuntimeError(f"Failed command {command!r}:\n{result.stdout}")
    return {"command": command, "exit_status": result.returncode,
            "output": result.stdout.strip()}


def boundary_checks() -> dict:
    # Equal-volume coordinate boxes: each signed L0 atom is V/2.
    cases = 0
    for n in range(2, 9):
        a = [F(1)] * n
        b = [F(2), F(1, 2)] + [F(1)] * (n - 2)
        va = F(2) ** n
        vb = F(2) ** n
        for width in b:
            vb *= width
        assert va == vb and a != b
        for widths, volume in ((a, va), (b, vb)):
            for width in widths:
                surface_atom = volume / (2 * width)
                assert width * surface_atom == volume / 2
                assert width * surface_atom / n == volume / (2 * n)
        # At t=4 and p=1/2 the box strict-Jensen comparison is rational.
        mean_rp = (F(2) + F(1, 2) + n - 2) / n
        assert mean_rp > 1
        cases += 1
    # For rational p choose a perfect denominator power, so no float enters.
    scaling_cases = 0
    for n in range(2, 9):
        for p in (F(0), F(1, 4), F(1, 2), F(3, 4)):
            q = p.denominator
            base = F(2)
            c = base ** q
            determinant_scale = c ** (n - 1)
            support_scale = base ** int(q * (1 - p))
            assert support_scale * determinant_scale == base ** int(q * (n - p))
            assert n - p > 0
            scaling_cases += 1
    return {"box_dimensions": list(range(2, 9)), "box_cases": cases,
            "scaling_cases": scaling_cases,
            "arithmetic": "fractions.Fraction", "status": "pass"}


def endpoint_checks() -> dict:
    """Check the manuscript's differentiated identity without PDE simulation."""
    rng = random.Random(20261006)
    count = 0
    for m in range(1, 6):  # tangent dimension m=n-1, including n=2
        for _ in range(40):
            diagonal = [F(rng.randrange(1, 7)) for _ in range(m)]
            inverse = [1 / d for d in diagonal]
            h = F(rng.randrange(1, 6))
            w = F(rng.randrange(-4, 5))
            grad = [F(rng.randrange(-4, 5)) for _ in range(m)]
            A = [[F(0) for _ in range(m)] for _ in range(m)]
            for i in range(m):
                for j in range(i, m):
                    A[i][j] = A[j][i] = F(rng.randrange(-4, 5))
            # Impose precisely the first derivative tr(Q^-1 A)=-w.
            A[0][0] = diagonal[0] * (
                -w - sum(inverse[i] * A[i][i] for i in range(1, m)))
            first_trace = sum(inverse[i] * A[i][i] for i in range(m))
            assert first_trace == -w
            Qww = [[2 * w * A[i][j]
                    - (w * w * diagonal[i] if i == j else 0)
                    + 2 * h * grad[i] * grad[j]
                    for j in range(m)] for i in range(m)]
            trace_square = sum(inverse[i] * A[i][j] * inverse[j] * A[j][i]
                               for i in range(m) for j in range(m))
            trace_second = sum(inverse[i] * Qww[i][i] for i in range(m))
            gradient_energy = sum(inverse[i] * grad[i] ** 2 for i in range(m))
            assert trace_second - trace_square == (
                -trace_square - (m + 2) * w ** 2 + 2 * h * gradient_energy)
            assert trace_square >= 0
            count += 1
    return {"cases": count, "tangent_dimensions": [1, 2, 3, 4, 5],
            "seed": 20261006, "arithmetic": "fractions.Fraction",
            "status": "pass",
            "scope": "finite algebra checks, not a global PDE proof"}


def check_payload(root: Path) -> dict:
    manifest = root / "PACKAGE_CONTENTS.json"
    if not manifest.is_file():
        return {"status": "not_applicable", "reason": "working tree, not extracted archive"}
    contents = json.loads(manifest.read_text(encoding="utf-8"))
    for item in contents["files"]:
        relative = Path(item["path"])
        if relative.is_absolute() or ".." in relative.parts:
            raise RuntimeError("Unsafe payload manifest path")
        p = root / relative
        assert p.is_file(), f"Missing payload: {relative}"
        assert p.stat().st_size == item["bytes"], f"Size mismatch: {relative}"
        assert sha(p) == item["sha256"], f"Hash mismatch: {relative}"
    return {"status": "pass", "files": len(contents["files"]),
            "manifest_sha256": sha(manifest)}


def check_upstream(root: Path, upstream: Path) -> dict:
    inventory = json.loads((root / "sources/UPSTREAM_INVENTORY.json").read_text())
    result = run(["git", "rev-parse", "HEAD"], upstream)
    assert result["output"] == PIN, "The supplied checkout is not at the recorded source pin"
    for item in inventory["files"]:
        p = upstream / item["path"]
        assert p.is_file(), f"Missing upstream input: {item['path']}"
        assert p.stat().st_size == item["bytes"], f"Upstream size mismatch: {item['path']}"
        assert sha(p) == item["sha256"], f"Upstream hash mismatch: {item['path']}"
    return {"status": "pass", "pin": PIN, "files": len(inventory["files"]),
            "scope": "read-only byte/version check; no Lean build"}


def compile_clean(root: Path, engine: str | None) -> dict:
    engine = engine or shutil.which("tectonic") or shutil.which("pdflatex")
    if not engine:
        raise RuntimeError("No TeX engine found; supply --tex-engine PATH")
    scratch = root / "verification" / ".scratch"
    scratch.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="clean-tex-", dir=scratch) as temp:
        target = Path(temp)
        shutil.copyfile(root / "main.tex", target / "main.tex")
        version = run([engine, "--version"], target)
        if "tectonic" in Path(engine).name.lower():
            command = [engine, "--keep-logs", "--keep-intermediates",
                       "--outdir", str(target), "main.tex"]
            build = run(command, target, 180)
        else:
            command = [engine, "-interaction=nonstopmode", "-halt-on-error",
                       "-output-directory", str(target), "main.tex"]
            run(command, target, 180)
            build = run(command, target, 180)
        pdf = target / "main.pdf"
        assert pdf.read_bytes().startswith(b"%PDF-"), "No exported PDF"
        log = (target / "main.log").read_text(errors="replace")
        for marker in ("Undefined control sequence", "LaTeX Error:",
                       "There were undefined references", "Citation `"):
            assert marker not in log, f"Compile diagnostic: {marker}"
        return {"status": "pass", "engine_version": version["output"],
                "command": build["command"], "exit_status": build["exit_status"],
                "pdf_bytes": pdf.stat().st_size, "pdf_sha256": sha(pdf),
                "log_sha256": sha(target / "main.log"),
                "note": "fresh temporary-directory build; visual inspection is separate"}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--upstream", type=Path, help="separate read-only checkout at the exact pin")
    parser.add_argument("--compile", action="store_true", help="also compile standalone TeX in a fresh directory")
    parser.add_argument("--tex-engine", help="Tectonic or pdfLaTeX executable")
    parser.add_argument("--output", type=Path, help="optional JSON receipt; never changes manuscript/PDF")
    args = parser.parse_args()
    root = args.root.resolve()
    main_source = (root / "main.tex").read_text(encoding="utf-8")
    assert not re.search(r"\\(?:input|include|bibliography)\s*\{", main_source), "TeX must be standalone"
    assert "\\begin{thebibliography}" in main_source
    deposit = json.loads((root / "zenodo-deposit.json").read_text(encoding="utf-8"))
    metadata = deposit["metadata"]
    assert metadata["title"] == TITLE
    assert metadata["creators"] == [{"name": "Kriebel, Alec", "orcid": "0009-0001-9320-500X"}]
    assert metadata["publication_date"] == "2026-10-06"
    assert metadata["license"] == "cc-by-4.0"
    assert [f["name"] for f in deposit["files"]] == ["paper.pdf", "source-and-verification.zip", "README.md"]
    report = {"status": "pass", "python": sys.version, "platform": platform.platform(),
              "limitations": ["finite checks do not replace mathematical proofs",
                              "no Lean kernel/axiom/Comparator verification",
                              "no priority certification or human peer review"],
              "payload": check_payload(root), "boundary_checks": boundary_checks(),
              "endpoint_checks": endpoint_checks(), "tensor_checks": [],
              "source_sha256": sha(root / "main.tex"),
              "deposit_manifest_sha256": sha(root / "zenodo-deposit.json")}
    for relative in ("agent_notes/upstream_audit_tensor_certificate.py",
                     "agent_notes/moment_dependencies_tensor_check.py"):
        result = run([sys.executable, relative], root)
        result["script_sha256"] = sha(root / relative)
        report["tensor_checks"].append(result)
    if (root / "paper.pdf").is_file():
        assert (root / "paper.pdf").read_bytes().startswith(b"%PDF-")
        report["exported_pdf_sha256"] = sha(root / "paper.pdf")
    if args.upstream:
        report["upstream"] = check_upstream(root, args.upstream.resolve())
    if args.compile:
        report["clean_compile"] = compile_clean(root, args.tex_engine)
    serialized = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        output = args.output.resolve()
        assert output.is_relative_to(root), "Receipt must remain within the project folder"
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(serialized, encoding="utf-8")
    print(serialized, end="")


if __name__ == "__main__":
    main()
