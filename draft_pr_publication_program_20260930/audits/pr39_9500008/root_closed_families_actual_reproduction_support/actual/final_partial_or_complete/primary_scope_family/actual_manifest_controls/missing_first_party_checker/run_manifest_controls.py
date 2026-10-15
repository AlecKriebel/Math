"""Test exact family closure on copied actual own-root files."""
from pathlib import Path
import json
import shutil
import subprocess

HERE = Path(__file__).resolve().parent
CONTROL = HERE / "actual_manifest_controls"
MANIFEST = "PRIMARY_SCOPE_FAMILY_MANIFEST.json"


def run(argv):
    p = subprocess.run(argv, cwd=HERE, capture_output=True, text=True)
    return {"argv": argv, "returncode": p.returncode, "stdout": p.stdout, "stderr": p.stderr}


def main():
    assert not CONTROL.exists(), "Never replace preserved controls."
    tool = str(HERE / "check_family_manifest.py")
    first = run(["/usr/bin/python3", tool, "build"])
    assert first["returncode"] == 0
    original = json.loads((HERE / MANIFEST).read_text())
    paths = list(original["first_party_members"]) + list(original["foreign_source_materials_and_extractions"]) + [MANIFEST]
    result = []
    CONTROL.mkdir()
    for name in ["baseline", "nested_manifest_same_basename", "missing_first_party_checker", "foreign_pdf_corrupted"]:
        root = CONTROL / name
        root.mkdir()
        for rel in paths:
            target = root / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(HERE / rel, target)
        if name == "nested_manifest_same_basename":
            p = root / "nested" / MANIFEST
            p.parent.mkdir()
            p.write_text("Undeclared first-party member must be rejected.\n")
        elif name == "missing_first_party_checker":
            (root / "check_original_packet.py").unlink()
        elif name == "foreign_pdf_corrupted":
            p = root / "foreign_sources/1302.6958v4.pdf"
            p.write_bytes(p.read_bytes() + b"changed")
        checked = run(["/usr/bin/python3", tool, "verify", str(root)])
        assert (checked["returncode"] == 0) == (name == "baseline"), checked
        result.append({"control": name, **checked})
    out = {"all_expected_outcomes_observed": True, "controls": result,
           "scope": "Actual own-root exact-membership and byte-seal controls; nested manifest basenames are never exempt."}
    (HERE / "MANIFEST_NEGATIVE_CONTROL_RESULTS.json").write_text(json.dumps(out, indent=2) + "\n")
    # Final closure includes the preserved control copies and result, unlike the
    # earlier baseline manifest copied into each isolated test root.
    final = run(["/usr/bin/python3", tool, "build"])
    assert final["returncode"] == 0
    print(json.dumps({"control_results": result, "final_closure": final}, indent=2))


if __name__ == "__main__":
    main()
