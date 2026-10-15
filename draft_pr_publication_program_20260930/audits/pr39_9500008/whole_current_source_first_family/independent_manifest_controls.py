"""Own exact-path closure controls; all temporary fixtures stay in this scope."""
from pathlib import Path
import sys
import json
import tempfile
sys.dont_write_bytecode = True
from close_manifest import inventory, verify_inventory

p = Path(__file__).parent.resolve()
out = {}
with tempfile.TemporaryDirectory(prefix="manifest_controls_", dir=p) as folder:
    q = Path(folder)
    (q / "nested").mkdir()
    (q / "checker.py").write_text("own checker fixture\n")
    (q / "foreign.pdf").write_bytes(b"own fake foreign binding fixture")
    (q / "MANIFEST.json").write_text("excluded exact top-level\n")
    (q / "nested" / "MANIFEST.json").write_text("must retain nested basename\n")
    foreign = {"foreign.pdf": "fixture"}
    rows = inventory(q, foreign)
    assert any(x["path"] == "nested/MANIFEST.json" for x in rows)
    assert not any(x["path"] == "MANIFEST.json" for x in rows)
    out["baseline"] = verify_inventory(q, rows, foreign)
    (q / "checker.py").unlink()
    try:
        verify_inventory(q, rows, foreign)
    except AssertionError as e:
        out["missing_first_party_rejected"] = str(e)
    else:
        raise AssertionError("missing file accepted")
    (q / "checker.py").write_text("own checker fixture\n")
    (q / "foreign.pdf").write_bytes(b"changed foreign fixture")
    try:
        verify_inventory(q, rows, foreign)
    except AssertionError as e:
        out["corrupted_foreign_rejected"] = str(e)
    else:
        raise AssertionError("corrupt foreign accepted")
    (q / "foreign.pdf").write_bytes(b"own fake foreign binding fixture")
    (q / "escape").symlink_to(p / "SOURCE_FIRST_SEAL.md")
    try:
        inventory(q, foreign)
    except ValueError as e:
        out["symlink_rejected"] = str(e)
    else:
        raise AssertionError("symlink accepted")
    (q / "escape").unlink()
    out["nested_same_basename_retained"] = True
out["passed"] = True
(p / "INDEPENDENT_MANIFEST_CONTROL_RESULTS.json").write_text(json.dumps(out, indent=2) + "\n")
print(json.dumps(out, indent=2))
