#!/usr/bin/env python3
"""Read-only source/hash checks; stdout by default. No mathematical proof audit.

Usage:
  python3 verify_sources.py
  python3 verify_sources.py --output /absolute/path/new_check.json

An output path is explicit and must not already exist. In particular, rerunning
the default command never replaces the frozen source_check.json or its timestamp.
No network access or source-file mutation is performed.
"""

import argparse
import hashlib
import json
from pathlib import Path
import re
import sys
import unicodedata
from datetime import datetime, timezone


ROOT = Path(__file__).resolve().parent


def sha(data):
    return hashlib.sha256(data).hexdigest()


def norm(text):
    return " ".join(unicodedata.normalize("NFKC", text).split())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path,
                        help="write a NEW report here; default is stdout only")
    args = parser.parse_args()
    if args.output is not None and args.output.exists():
        parser.error("refusing to overwrite an existing report; select a new --output path")

    checks = []

    def check(name, passed, **details):
        checks.append({"name": name, "passed": bool(passed), **details})

    def verify_file(relative, entry, kind):
        path = ROOT / relative
        try:
            data = path.read_bytes()
        except OSError as error:
            check(kind + ": " + relative, False, error=str(error))
            return
        check(kind + ": " + relative,
              len(data) == entry["bytes"] and sha(data) == entry["sha256"],
              bytes=len(data), sha256=sha(data))

    manifest = json.loads((ROOT / "SOURCE_MANIFEST.json").read_text())
    for entry in manifest["sources"]:
        verify_file(entry["file"], entry, "main source")

    independent = ROOT / "independent_status"
    independent_manifest = json.loads((independent / "SOURCE_MANIFEST.json").read_text())
    independent_sources = 0
    for entry in independent_manifest:
        if "error" in entry:
            # Failed retrievals are limitations, never fictitious source files.
            continue
        verify_file("independent_status/sources/" + entry["name"], entry,
                    "independent source")
        independent_sources += 1
        if "text_extraction" in entry:
            derivative = entry["text_extraction"]
            verify_file("independent_status/sources/" + derivative["name"],
                        derivative, "independent text derivative")
            independent_sources += 1

    independent_receipt = json.loads((independent / "RECEIPT.json").read_text())
    for name, entry in independent_receipt["files"].items():
        verify_file("independent_status/" + name, entry, "independent frozen output")

    notebook = (ROOT / "sources/notebook21_fresh.txt").read_text()
    updates = (ROOT / "sources/notebook_updates_fresh.txt").read_text()
    marker = "21.122. Let"
    start = notebook.find(marker)
    check("one complete official problem entry", notebook.count(marker) == 1)
    check("no 21.122 update occurrence", re.search(r"21\.122\b", updates) is None)
    if start >= 0:
        entry = notebook[start:notebook.find("\f", start)]
        check("official PDF page 197", notebook[:start].count("\f") + 1 == 197)
        check("official proposer", "P. Shumyatsky" in entry)
        expected = ("Let w be a group word, and G a profinite group. Is it true that "
                    "the cardinality of the set of w-values in G is either finite "
                    "or at least continuum?")
        check("complete question text", norm(expected) in norm(entry))
        check("cited 2020 result metadata", "977–993" in entry and "102 (2020)" in entry)
    check("update chronology anomaly retained", "November 2026 update" in updates)

    anchors = {
        "sources/dks1907.01344v2.txt": [
            "Every multilinear commutator word is strongly concise.",
            "Every group word w is strongly concise in the class of nilpotent profinite groups.",
            "that is nowhere locally constant"],
        "sources/detomi_virt_nilpotent.txt": [
            "Every group word w is strongly concise in the class of virtually nilpotent profinite groups."],
        "sources/engel2108.11789v1.txt": [
            "strongly concise in the class of finitely generated profinite groups.",
            "such that G/N is locally nilpotent."],
        "sources/heras_zozaya_published.txt": [
            "Suppose that G has an equationally Noetherian subgroup that is dense in G",
            "dense virtually abelian-by-polycyclic subgroup"],
        "sources/shumyatsky2401.15707v2.txt": [
            "then $w(w(G))$ is finite.", "FC$ -generated profinite groups"],
        "sources/zozaya2608.02237v1.txt": [
            "profinite metabelian groups", "not all word maps are polynomial",
            "Suppose that $G=AB$ where $A\\unlhd G$"]}
    for file, phrases in anchors.items():
        text = norm((ROOT / file).read_text())
        for phrase in phrases:
            # PDF wrapping can introduce a word-split hyphen in "Suppose".
            found = norm(phrase) in text
            if not found and "Suppose that G has" in phrase:
                found = norm(phrase).replace("Suppose", "Sup- pose") in text
            check("primary text anchor: " + file + ": " + phrase, found)

    # A frozen authored-output manifest is optional on the first creation run.
    # Once present, default reruns also authenticate all these fixed outputs.
    output_manifest = ROOT / "OUTPUT_MANIFEST.json"
    frozen_count = 0
    if output_manifest.exists():
        frozen = json.loads(output_manifest.read_text())
        for name, entry in frozen["files"].items():
            verify_file(name, entry, "frozen preparation output")
            frozen_count += 1

    failed = [item["name"] for item in checks if not item["passed"]]
    report = {
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "problem": "21.122",
        "purpose": "hashes, complete official-entry identity, and source-text anchors only",
        "not_a_mathematical_proof_or_exhaustive_priority_audit": True,
        "default_behavior": "stdout only; frozen reports are never overwritten",
        "main_source_entries": len(manifest["sources"]),
        "independent_source_entries": independent_sources,
        "independent_receipt_files": len(independent_receipt["files"]),
        "failed_independent_retrievals_recorded": sum("error" in x for x in independent_manifest),
        "frozen_preparation_outputs_checked": frozen_count,
        "check_count": len(checks),
        "all_passed": not failed,
        "failed_checks": failed,
        "checks": checks,
    }
    encoded = json.dumps(report, indent=2) + "\n"
    if args.output is None:
        sys.stdout.write(encoded)
    else:
        # Mode x also protects against races after the existence check above.
        with args.output.open("x") as stream:
            stream.write(encoded)
        print(json.dumps({"output": str(args.output), "all_passed": not failed,
                          "check_count": len(checks), "failed_checks": failed}))
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
