#!/usr/bin/env python3
"""Deterministic final-byte audit for the order-12 frontier manuscript."""

from __future__ import annotations

import hashlib
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile

CONDITIONAL_VERDICT = "ACCEPT_RELEASE_BYTES_CONDITIONAL_ONLY_ON_ATOMIC_TAG_PUSH"
TAGGED_VERDICT = "ACCEPT_RELEASE_BYTES_TAG_BOUND"
BASELINE = "b9b74a38415dac6ef11bb7cbc55badf224affadd"
EPOCH = "1785074656"
TAG = "gamma-theta-order12-frontier-v1.0.0"
ROOT = Path(__file__).resolve().parents[3]
PAPER = ROOT / "gamma_theta_eternal_domination/paper/order12_frontier"
DOC_PDF = ROOT / "docs/papers/gamma-theta-order-12-frontier/paper.pdf"

EXPECTED = {
    "README.md": ("5dd9578ca712c5449a6146544b4002f5aefb73b055cba405f9388b9065394cc0", 2351),
    "main.bbl": ("f9789755c4ec0c83b1e2493f5301e7d4d4dfaa4398810aa9e28d22148da4849a", 2484),
    "main.blg": ("36a26a35030c17e6a29ed5fa683a298f907726cf9a3af844f8f4d3b56dd6020e", 191),
    "main.log": ("645879feb11804aaffd0e18c617c4616d4fdd6d39014197f795c753aa2110ac0", 12311),
    "main.pdf": ("b35d4bd795ddfbfa61be18bdd60ddb6d23492b0a63a7449e2ec0190170e6e9d2", 130163),
    "main.tex": ("44e49d6dbf90174ca27f5b65e99e55a9852fb6deafb0ba3dd78770c53e0faa9e", 48891),
    "references.bib": ("8471090ae03babda7794aea6bbcbc6fbcb36ffa8a859a86005bbb0b7ae2f9ec6", 4534),
}


def need(ok: bool, message: str) -> None:
    if not ok:
        raise SystemExit(f"FAIL: {message}")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


for name, (sha, size) in EXPECTED.items():
    path = PAPER / name
    need(path.is_file() and not path.is_symlink(), f"bad artifact: {path}")
    need(path.stat().st_size == size and digest(path) == sha, f"byte mismatch: {name}")

need(
    {p.name for p in PAPER.iterdir()}
    == {"README.md", "main.bbl", "main.blg", "main.log", "main.pdf",
        "main.tex", "qa.json", "references.bib"},
    "unexpected manuscript package entry",
)
need(DOC_PDF.is_file() and not DOC_PDF.is_symlink(), "bad docs PDF")
need(DOC_PDF.read_bytes() == (PAPER / "main.pdf").read_bytes(), "docs PDF differs")

source = (PAPER / "main.tex").read_text(encoding="utf-8")
base = subprocess.run(
    ["git", "show", f"{BASELINE}:gamma_theta_eternal_domination/paper/order12_frontier/main.tex"],
    cwd=ROOT, check=True, stdout=subprocess.PIPE,
).stdout.decode("utf-8")
replacements = [
    (
        "  urlcolor=blue\n}",
        "  urlcolor=blue,\n"
        "  pdftitle={A Certified Order-Twelve Extension of the gamma--theta Frontier in One-Guard Eternal Domination},\n"
        "  pdfauthor={Alec Kriebel},\n"
        "  pdfsubject={One-guard eternal domination and clique covering},\n"
        "  pdfkeywords={eternal domination, domination number, clique cover, gamma--theta conjecture}\n}",
    ),
    ("\\author{Author metadata to be supplied before submission}", "\\author{Alec Kriebel}"),
    (
        "The accompanying archive contains the formulas, proofs, verifiers,\n"
        "manifests, reviews, literature-source identifiers, and exact hashes cited\n"
        "above.  A permanent public archive identifier is to be inserted before\n"
        "submission.",
        "The formulas, proofs, verifiers, manifests, reviews,\n"
        "literature-source identifiers, and exact hashes cited above are publicly\n"
        "archived in the tagged release\n"
        "\\href{https://github.com/AlecKriebel/Math/releases/tag/gamma-theta-order12-frontier-v1.0.0}\n"
        "{\\texttt{gamma-theta-order12-frontier-v1.0.0}}.\n"
        "The corresponding human-readable\n"
        "\\href{https://aleckriebel.github.io/Math/research/gamma-theta-conjecture/}\n"
        "{project page} records the active campaign status.",
    ),
]
for old, new in replacements:
    need(base.count(old) == 1, "baseline replacement anchor changed")
    base = base.replace(old, new)
need(base == source, "main.tex changed outside author/PDF metadata and availability links")
need("Assume the published exhaustive result" in source, "conditional premise missing")
need("universal conjecture remains open" in source, "universal disclaimer missing")
need("\ufffd" not in source, "replacement character in source")

bad_log = re.compile(
    r"LaTeX Warning|Package \S+ Warning|Warning--|Overfull \\\\[hv]box|"
    r"Underfull \\\\[hv]box|undefined (?:citation|reference)|multiply defined|^!",
    re.IGNORECASE | re.MULTILINE,
)
for name in ("main.log", "main.blg"):
    need(not bad_log.search((PAPER / name).read_text(errors="replace")), f"warning in {name}")

need(subprocess.check_output(["tectonic", "--version"], text=True).strip() == "Tectonic 0.16.9",
     "wrong Tectonic version")
with tempfile.TemporaryDirectory(prefix="_audit_", dir=Path(__file__).parent) as temp:
    outputs = []
    for index in (1, 2):
        out = Path(temp) / str(index)
        out.mkdir()
        env = dict(os.environ, SOURCE_DATE_EPOCH=EPOCH)
        subprocess.run(
            ["tectonic", "--keep-logs", "--keep-intermediates", "--outdir", str(out),
             str(PAPER / "main.tex")],
            cwd=ROOT, env=env, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        )
        outputs.append(out)
    for name in ("main.pdf", "main.bbl"):
        data = (outputs[0] / name).read_bytes()
        need(data == (outputs[1] / name).read_bytes(), f"two-build mismatch: {name}")
        need(data == (PAPER / name).read_bytes(), f"retained mismatch: {name}")

info = subprocess.check_output(["pdfinfo", str(PAPER / "main.pdf")], text=True)
for exact in (
    "Title:           A Certified Order-Twelve Extension of the gamma–theta Frontier in One-Guard Eternal Domination",
    "Subject:         One-guard eternal domination and clique covering",
    "Author:          Alec Kriebel",
    "Pages:           17",
    "Form:            none",
    "Encrypted:       no",
):
    need(exact in info, f"PDF metadata mismatch: {exact}")

tag = subprocess.run(
    ["git", "show-ref", "--verify", "--quiet",
     f"refs/tags/{TAG}"], cwd=ROOT,
)
need(tag.returncode in (0, 1), "cannot determine local tag status")
if tag.returncode == 0:
    tagged_paths = {
        **{
            f"gamma_theta_eternal_domination/paper/order12_frontier/{name}":
            (sha, size)
            for name, (sha, size) in EXPECTED.items()
        },
        "docs/papers/gamma-theta-order-12-frontier/paper.pdf":
            EXPECTED["main.pdf"],
    }
    for path, (sha, size) in tagged_paths.items():
        data = subprocess.run(
            ["git", "show", f"{TAG}:{path}"],
            cwd=ROOT, check=True, stdout=subprocess.PIPE,
        ).stdout
        need(len(data) == size and hashlib.sha256(data).hexdigest() == sha,
             f"tagged-byte mismatch: {path}")
    print(TAGGED_VERDICT)
else:
    print(CONDITIONAL_VERDICT)
print(EXPECTED["main.pdf"][0])
