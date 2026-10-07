#!/usr/bin/env python3
"""Hash read inputs and reproduce exact checks into this audit directory only."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import difflib
import subprocess
import sys

audit = Path(__file__).resolve().parent
project = audit.parents[2]
candidate = project / "reviews/package_v4/source-and-verification"
candidate_v2 = project / "reviews/package_v2/source-and-verification"
candidate_v3 = project / "reviews/package_v3/source-and-verification"
upstream_root = project / "sources/upstream_pinned"
manuscript = "preprints/Global-classical-solutions-of-the-three-dimensional-relativistic-Vlasov-Maxwell-system-September-23-2026"
sections = upstream_root / manuscript / "build/sections"
pinned_manifest = json.loads((candidate / "PINNED_SOURCE.json").read_text())

def sha256(file_path):
    return hashlib.sha256(file_path.read_bytes()).hexdigest()

inputs = [candidate / name for name in (
    "main.tex", "SUPPLEMENT_UNIFORM_LEMMA_CHAIN.md",
    "SUPPLEMENT_OCCUPATION_AUDIT.md", "rational_selection_certificate.py",
    "PINNED_SOURCE.json")]
inputs += [sections / (name + ".tex") for name in (
    "setup", "occupation", "direct", "direction", "selection", "closure",
    "cancellation")]
receipt = {
    "timestamp_utc": datetime.now(timezone.utc).isoformat(),
    "upstream_commit": pinned_manifest["commit"],
    "final_package_version": "package_v4",
    "inputs": [],
    "reproduction": [],
    "limits": "A source hash authenticates the reviewed text, not its mathematical correctness."
}
delta_receipt = {
    "timestamp_utc": receipt["timestamp_utc"],
    "v2_main_sha256": sha256(candidate_v2 / "main.tex"),
    "v3_main_sha256": sha256(candidate_v3 / "main.tex"),
    "v4_main_sha256": sha256(candidate / "main.tex"),
    "scope_marker": "\\section{Local theory, uniqueness and nonneutral continuation}",
    "unchanged_core_before_local_theory": (
        (candidate_v2 / "main.tex").read_bytes().split(b"\\section{Local theory, uniqueness and nonneutral continuation}")[0]
        == (candidate / "main.tex").read_bytes().split(b"\\section{Local theory, uniqueness and nonneutral continuation}")[0]),
    "unchanged_supporting_files": []
}
assert delta_receipt["unchanged_core_before_local_theory"]
v3_main = (candidate_v3 / "main.tex").read_bytes()
v4_main = (candidate / "main.tex").read_bytes()
v4_without_formatting = v4_main
for insertion in (
    b"\\begingroup\\small\\raggedright\n",
    b"\\setlength{\\itemsep}{3pt}\n",
    b"\\endgroup\n"):
    assert v4_without_formatting.count(insertion) == 1
    v4_without_formatting = v4_without_formatting.replace(insertion, b"", 1)
delta_receipt["exact_bibliography_formatting_additions_removed"] = 3
delta_receipt["v3_equals_v4_after_removing_exact_formatting_additions"] = (
    v3_main == v4_without_formatting)
assert delta_receipt["v3_equals_v4_after_removing_exact_formatting_additions"]
main_diff = "".join(difflib.unified_diff(
    v3_main.decode().splitlines(keepends=True),
    v4_main.decode().splitlines(keepends=True),
    fromfile="package_v3/main.tex", tofile="package_v4/main.tex"))
(audit / "V3_TO_V4_MAIN.diff").write_text(main_diff)
for name in (
    "SUPPLEMENT_UNIFORM_LEMMA_CHAIN.md", "SUPPLEMENT_OCCUPATION_AUDIT.md",
    "rational_selection_certificate.py", "PINNED_SOURCE.json"):
    match = (candidate_v2 / name).read_bytes() == (candidate / name).read_bytes()
    match_v3 = (candidate_v3 / name).read_bytes() == (candidate / name).read_bytes()
    assert match, name
    assert match_v3, name
    delta_receipt["unchanged_supporting_files"].append({
        "name": name, "sha256": sha256(candidate / name),
        "byte_identical_to_v2": match, "byte_identical_to_v3": match_v3})
(audit / "V4_DELTA_RECEIPT.json").write_text(json.dumps(delta_receipt, indent=2) + "\n")
before = {}
for file_path in inputs:
    digest = sha256(file_path)
    before[str(file_path)] = digest
    entry = {"path": str(file_path), "sha256": digest}
    if file_path.is_relative_to(upstream_root):
        key = str(file_path.relative_to(upstream_root))
        expected = pinned_manifest["sha256"][key]
        entry["expected_pinned_sha256"] = expected
        entry["pinned_hash_match"] = digest == expected
        assert digest == expected, file_path
    receipt["inputs"].append(entry)

for name, script_path in (
    ("independent_exact_arithmetic", audit / "independent_exact_arithmetic.py"),
    ("frozen_rational_selection_certificate", candidate / "rational_selection_certificate.py")
):
    completed = subprocess.run([sys.executable, str(script_path)], cwd=audit,
                               capture_output=True, text=True, check=False)
    (audit / (name + ".stdout.json")).write_text(completed.stdout)
    (audit / (name + ".stderr.txt")).write_text(completed.stderr)
    receipt["reproduction"].append({
        "name": name,
        "script_sha256": sha256(script_path),
        "exit_code": completed.returncode,
        "stdout_sha256": hashlib.sha256(completed.stdout.encode()).hexdigest(),
        "stderr_sha256": hashlib.sha256(completed.stderr.encode()).hexdigest()
    })
    assert completed.returncode == 0, name
    json.loads(completed.stdout)

receipt["all_inputs_preserved"] = all(
    sha256(Path(file_path)) == digest for file_path, digest in before.items())
assert receipt["all_inputs_preserved"]
(audit / "SOURCE_RECEIPT.json").write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps({
    "status": "all seven upstream proof-file hashes match the pin",
    "checks_exit_zero": len(receipt["reproduction"]),
    "all_inputs_preserved": receipt["all_inputs_preserved"],
    "receipt": str(audit / "SOURCE_RECEIPT.json")
}, indent=2))
