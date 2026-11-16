#!/usr/bin/env python3
"""Finite custody only. Default/--check reads; --seal creates two terminal files."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os
import sys

P = Path("/Users/alec/Documents/Math/research_website_catalogue_20261024/papers")
SEALS = {
    "23444050": "0c3c12b44e1e3cf13de1d782aa6b51e8762eedf65a59c1e8d95a6702f497ce73",
    "23334001": "f5c9bc9f35fadc509fd1bba6758c2447601012c3b861144b17524a4948609ab6",
    "23394004": "143d753527d1854267e41bfd5874a3d57ad8762094784ab8d10694bdeb288f59",
}
R = Path(__file__).absolute().parent
record = R.parent.parent.name
assert record in SEALS and R == P / record / "reviews" / "scope"
assert not Path(__file__).is_symlink()
CONTROLS = ("MANIFEST.json", "FINAL.json")

def pin(path):
    assert path.is_file() and not path.is_symlink(), str(path)
    data = path.read_bytes()
    return {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}

def check_initial_and_references():
    seal = R / "INITIAL_SEAL.json"
    assert pin(seal)["sha256"] == SEALS[record], "initial seal changed"
    initial = json.loads(seal.read_text())
    for item in initial["finite_initial_payload"]:
        path = R / item["path"]
        data = path.read_bytes()
        if item["path"] == "RESEARCH_LOG.md":
            data = data[:item["bytes"]]
        assert len(data) == item["bytes"]
        assert hashlib.sha256(data).hexdigest() == item["SHA256"], item["path"]
    refs = json.loads((R / "primary/SOURCE_PINS.json").read_text())
    for item in refs["references"]:
        actual = pin(Path(item["path"]))
        assert actual == {k: item[k] for k in ("bytes", "sha256")}, item["path"]

def inventory():
    files, directories = [], []
    for base, dirs, names in os.walk(R, followlinks=False):
        here = Path(base)
        assert not here.is_symlink()
        directories.append(here.relative_to(R).as_posix())
        for name in dirs:
            assert not (here / name).is_symlink()
        for name in names:
            path = here / name
            rel = path.relative_to(R).as_posix()
            actual = pin(path)
            if rel not in CONTROLS:
                files.append({"path": rel, **actual})
    return sorted(files, key=lambda x: x["path"]), sorted(directories)

def verify_final():
    final = json.loads((R / "FINAL.json").read_text())
    manifest_path = R / "MANIFEST.json"
    assert pin(manifest_path) == final["manifest"]
    manifest = json.loads(manifest_path.read_text())
    files, directories = inventory()
    assert files == manifest["files"] and directories == manifest["directories"]
    assert manifest["exact_terminal_controls_excluded"] == list(CONTROLS)
    return final, manifest

def seal():
    assert not any((R / name).exists() for name in CONTROLS), "already terminal"
    for name in CONTROLS:
        with (R / name).open("x") as handle:
            handle.write("")
    files, directories = inventory()
    manifest = {
        "schema": "finite-scope-manifest-v1", "record": int(record),
        "owned_root": str(R), "files": files, "directories": directories,
        "exact_terminal_controls_excluded": list(CONTROLS),
        "terminal_controls_created_before_inventory": True,
    }
    (R / "MANIFEST.json").write_text(json.dumps(manifest, indent=2) + "\n")
    final = {
        "schema": "independent-scientific-scope-final-v1", "record": int(record),
        "UTC": datetime.now(timezone.utc).isoformat(), "status": "COMPLETE",
        "manifest": pin(R / "MANIFEST.json"), "report": pin(R / "REPORT.md"),
        "initial_seal": pin(R / "INITIAL_SEAL.json"),
        "current_helper": pin(Path(__file__).absolute()),
        "helper_current_body_personally_read_before_execution": True,
        "actual_owned_files_including_terminal_controls": len(files) + 2,
        "actual_owned_directories_including_root": len(directories),
        "scientific_code_executions": [], "stored_scientific_results_read": False,
        "current_root_or_opposite_family_findings_read": False,
        "archived_review_judgment_bodies_read": False,
        "completion_estimate_percent": 100, "follow_up": None,
        "publication_authority": False, "all_owned_bytes_and_extent_frozen": True,
        "post_final_helper_or_render_execution_authorized": False,
    }
    (R / "FINAL.json").write_text(json.dumps(final, indent=2) + "\n")
    check_initial_and_references()
    verify_final()
    return {"status": "SEALED", "FINAL": pin(R / "FINAL.json"),
            "MANIFEST": pin(R / "MANIFEST.json"), "files": len(files) + 2,
            "directories_including_root": len(directories)}

args = sys.argv[1:]
assert args in ([], ["--check"], ["--seal"]), "unsupported arguments"
check_initial_and_references()
if args == ["--seal"]:
    result = seal()
elif (R / "FINAL.json").exists():
    final, manifest = verify_final()
    result = {"status": "FROZEN_READ_ONLY", "files": len(manifest["files"]) + 2}
else:
    assert not (R / "MANIFEST.json").exists(), "partial terminal controls"
    files, directories = inventory()
    result = {"status": "DRAFT_READ_ONLY", "files": len(files),
              "directories_including_root": len(directories)}
print(json.dumps({"record": int(record), **result}, indent=2))
