#!/usr/bin/env python3
"""Read-only, standard-library verification of the complete publication package."""
from pathlib import Path
import hashlib
import json
import runpy


def run():
    root = Path(__file__).resolve().parent
    manifest = json.loads((root / "MANIFEST.json").read_text())
    expected = {item["path"] for item in manifest["files"]} | {"MANIFEST.json"}
    actual = {str(p.relative_to(root)) for p in root.rglob("*")
              if p.is_file() and "__pycache__" not in p.parts}
    assert actual == expected
    for item in manifest["files"]:
        data = (root / item["path"]).read_bytes()
        assert len(data) == item["bytes"]
        assert hashlib.sha256(data).hexdigest() == item["sha256"]
    author = runpy.run_path(str(root / "checks/affine_controls.py"))["run"]()
    assert author == json.loads((root / "checks/affine_results.json").read_text())
    independent = runpy.run_path(str(root / "audit/independent_affine_controls.py"))["run"]()
    assert independent == json.loads((root / "audit/independent_affine_results.json").read_text())
    original = root / "frozen_original" / "attempts"
    expected_changes = {
        "turn_01.md": [("union of right cosets r_i H", "union of left cosets r_i H")],
        "turn_05.md": [("If an open coset Ny were contained in x^G, conjugate it so its center is",
                       "If an open coset Ny, with N open normal in G, were contained in x^G,\nconjugate it so its center is")],
    }
    for path in sorted(original.glob("turn_*.md")):
        text = path.read_text()
        for old, new in expected_changes.get(path.name, []):
            assert text.count(old) == 1
            text = text.replace(old, new)
        assert (root / "attempts" / path.name).read_text() == text
    return {"publication_manifest_passed": True,
            "publication_file_count": len(actual),
            "frozen_original_manifest_passed": independent["manifest_all_entries_passed"],
            "only_two_authorized_wording_clarifications": True,
            "author_control_cases": len(author["cases"]),
            "independent_control_cases": len(independent["cases"]),
            "all_results_match": True,
            "general_resolution_claimed": False}


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
