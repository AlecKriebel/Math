#!/usr/bin/env python3
"""Compile the five declared sources in isolation and test required inputs."""

from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent
PROJECT = ROOT / "materials" / "k2p_principal_d_plus_submission_referee"
SOURCE = PROJECT / "proof_compression_submission"
FILES = [
    "article/main.tex",
    "article/references.bib",
    "supplement/supplement.tex",
    "supplement/compression_tables.tex",
    "supplement/certificate_appendix.tex",
]
DEFECTS = [
    re.compile(r"Overfull"),
    re.compile(r"undefined references", re.I),
    re.compile(r"Citation.*undefined", re.I),
    re.compile(r"Reference.*undefined", re.I),
    re.compile(r"Fatal error", re.I),
    re.compile(r"Token not allowed in a PDF string", re.I),
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def copy_sources(target: Path) -> None:
    for relative in FILES:
        destination = target / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(SOURCE / relative, destination)


def compile_one(tree: Path, subdir: str, source: str, output: Path) -> subprocess.CompletedProcess[str]:
    output.mkdir(parents=True, exist_ok=True)
    return subprocess.run(
        ["tectonic", "-X", "compile", source, "--keep-logs", "--outdir", str(output)],
        cwd=tree / subdir,
        capture_output=True,
        text=True,
        check=False,
    )


def require_clean_log(path: Path) -> None:
    text = path.read_text(encoding="utf-8", errors="replace")
    hits = [pattern.pattern for pattern in DEFECTS if pattern.search(text)]
    if hits:
        raise SystemExit(f"build log defects in {path}: {hits}")


def main() -> None:
    if not __debug__:
        raise SystemExit("optimized Python is forbidden")
    if shutil.which("tectonic") is None:
        raise SystemExit("Tectonic is required for the manuscript-build gate")
    with tempfile.TemporaryDirectory(prefix="k2p-five-source-build-") as directory:
        root = Path(directory)
        clean = root / "clean"
        copy_sources(clean)
        article_out = root / "article-output"
        supplement_out = root / "supplement-output"
        article = compile_one(clean, "article", "main.tex", article_out)
        supplement = compile_one(clean, "supplement", "supplement.tex", supplement_out)
        if article.returncode != 0:
            raise SystemExit(f"article build failed:\n{article.stdout}\n{article.stderr}")
        if supplement.returncode != 0:
            raise SystemExit(f"supplement build failed:\n{supplement.stdout}\n{supplement.stderr}")
        article_pdf = article_out / "main.pdf"
        article_log = article_out / "main.log"
        supplement_pdf = supplement_out / "supplement.pdf"
        supplement_log = supplement_out / "supplement.log"
        for path in (article_pdf, article_log, supplement_pdf, supplement_log):
            if not path.is_file():
                raise SystemExit(f"expected build artifact missing: {path}")
        require_clean_log(article_log)
        require_clean_log(supplement_log)

        omission_results = {}
        for label, relative in (
            ("compression_tables", "supplement/compression_tables.tex"),
            ("certificate_appendix", "supplement/certificate_appendix.tex"),
        ):
            tree = root / f"missing-{label}"
            copy_sources(tree)
            (tree / relative).unlink()
            result = compile_one(tree, "supplement", "supplement.tex", root / f"missing-{label}-output")
            if result.returncode == 0:
                raise SystemExit(f"missing required input was accepted: {label}")
            omission_results[label] = "REJECTED"

        print(json.dumps({
            "status": "PASS",
            "source_file_count": len(FILES),
            "article_pdf": {"bytes": article_pdf.stat().st_size, "sha256": sha256(article_pdf)},
            "supplement_pdf": {"bytes": supplement_pdf.stat().st_size, "sha256": sha256(supplement_pdf)},
            "required_input_omissions": omission_results,
        }, sort_keys=True))


if __name__ == "__main__":
    main()

