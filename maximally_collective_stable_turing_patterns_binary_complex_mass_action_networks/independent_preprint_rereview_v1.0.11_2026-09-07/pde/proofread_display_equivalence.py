#!/usr/bin/env python3
"""Focused v1.0.11 proofreading; no manuscript or generated-source changes."""
from pathlib import Path
import hashlib
import json
import re
import subprocess

OUT = Path(__file__).resolve().parent
SOURCE = OUT.parent / "source_snapshot"
REPO = OUT.parents[2]
PREFIX = "maximally_collective_stable_turing_patterns_binary_complex_mass_action_networks/"
OLD = "953c836a12b9d9d474521feb4a96e218c1155203"
TARGET = "137ffa9f1a340f621651395ad0236cf1bdadb51c"
records = []


def require(condition, description, **evidence):
    if not condition:
        raise RuntimeError(description)
    records.append({"check": description, "status": "PASS", **evidence})


def git_text(commit, relative):
    return subprocess.check_output(["git", "show", commit + ":" + PREFIX + relative], cwd=REPO).decode()


def selected(text, journal):
    """The inspected body regions have no nested TeX conditionals."""
    def choose(match):
        sections = match.group(1).split(r"\else")
        require(len(sections) <= 2, "inspected conditional has at most one else")
        return sections[0] if journal else (sections[1] if len(sections) == 2 else "")
    return re.sub(r"\\ifsiadsreview(.*?)\\fi", choose, text, flags=re.S)


def compact(text):
    return re.sub(r"\s+", "", text)


def display_tokens(text):
    # Strip only explicit display-layout tokens and equation punctuation.
    text = re.sub(r"\\(?:begin|end)\{(?:split|aligned)\}", "", text)
    for presentation in [r"\[", r"\]", r"\qquad", r"\quad", r"\\", "&", ",", "."]:
        text = text.replace(presentation, "")
    return compact(text)


def region(text, start, end):
    return text[text.index(start):text.index(end)]


for relative, start, end in [
    ("manuscript/main.tex", r"\section{A supercritical stable unit-equilibrium design}", r"\section{Relation to prior work and limitations}"),
    ("manuscript/supplement.tex", r"\section{Improved unit-equilibrium critical profile}", r"\section{Numerical protocol and independent verification}"),
]:
    before = region(git_text(OLD, relative), start, end)
    target = git_text(TARGET, relative)
    snapshot = (SOURCE / relative).read_text()
    require(target == snapshot, relative + ": source snapshot matches target commit")
    after = region(snapshot, start, end)
    require(compact(selected(after, False)) == compact(selected(before, False)),
            relative + ": canonical nonlinear/PDE body unchanged beyond whitespace",
            sha256=hashlib.sha256(compact(selected(after, False)).encode()).hexdigest())

supplement = (SOURCE / "manuscript/supplement.tex").read_text()
spaces = region(supplement, r"\section{Semilinear stability and robustness}", "The identity $c^TA_m=0$")
require(display_tokens(selected(spaces, True)) == display_tokens(selected(spaces, False)),
        "S10 operator and both fixed-mass function spaces are identical in journal/canonical branches")

signs = (SOURCE / "data/sign_certificate_tables.tex").read_text()
old_signs = git_text(OLD, "data/sign_certificate_tables.tex")
require(compact(selected(signs, False)) == compact(old_signs),
        "canonical sign-certificate table is unchanged beyond whitespace")
reference = region(signs, r"\paragraph{Reference coefficient $R_m$.}", "After $m=u+3$, the following coefficients of $P_R$")
require(display_tokens(selected(reference, True)) == display_tokens(selected(reference, False)),
        "P_R coefficients, signs, powers and R_m denominator are identical in journal/canonical branches")

# These are the exact pieces joined by the typographical wrap. No space is
# introduced into the directory/file path itself.
for relative in ["manuscript/main.tex", "manuscript/supplement.tex"]:
    text = (SOURCE / relative).read_text()
    require(r"\texttt{python independent\_verifier/}\\[-0.2em]" in text
            and r"\texttt{verify\_symbolic\_certificates.py}" in text,
            relative + ": displayed command wrap preserves the executable and full path")

for destination in ["arxiv", "biorxiv", "journal"]:
    for name in ["main.tex", "supplement.tex"]:
        expected = (SOURCE / "manuscript" / name).read_text().replace("{../figures/", "{figures/").replace("{../data/", "{data/")
        require((SOURCE / "submission" / destination / "source" / name).read_text() == expected,
                destination + ": " + name + " differs only by intended local asset paths")

result = {"target": TARGET, "baseline": OLD, "scope": "focused nonlinear/PDE proofreading and display equivalence", "status": "PASS", "checks": records}
(OUT / "DISPLAY_EQUIVALENCE_RESULTS.json").write_text(json.dumps(result, indent=2) + "\n")
print("PASS: focused display equivalence and unchanged-source checks")
