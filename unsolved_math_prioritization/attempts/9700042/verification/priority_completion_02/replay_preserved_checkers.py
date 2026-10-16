"""Replay original code bytes with receipt outputs redirected by __file__ only.

The source code is not patched; its original SHA is authenticated. Assertions are
required to be active. This reads and executes reviewed project code, not source
PDF material. All generated files remain in this completion-audit folder.
"""
import contextlib
import datetime
import hashlib
import io
import json
from pathlib import Path
import sys

if sys.flags.optimize:
    raise RuntimeError("Assertions must be active")
HERE = Path(__file__).resolve().parent
BASE = HERE.parent
SPECS = [
    ("priority_recent_01/verify_corollary_geometry.py", "GEOMETRY_CHECKS.json"),
    ("priority_disposition_01/check_sequence_constraints.py", "verification_receipt.json"),
]
receipt = {"started_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
           "execution": "python3 -I -S -B; assertions active",
           "transformation": "Original source bytes unmodified. Only execution namespace __file__ points inside priority_completion_02 to redirect output receipts.",
           "runs": []}
for relative_source, output_name in SPECS:
    source = BASE / relative_source
    raw = source.read_bytes()
    original_output = source.with_name(output_name).read_bytes()
    out = io.StringIO()
    namespace = {"__file__": str(HERE / source.name), "__name__": "__main__"}
    with contextlib.redirect_stdout(out):
        exec(compile(raw, relative_source, "exec"), namespace)
    generated = (HERE / output_name).read_bytes()
    unchanged = original_output == source.with_name(output_name).read_bytes()
    same = json.loads(generated) == json.loads(original_output)
    if not (unchanged and same):
        raise RuntimeError("Replay did not reproduce the preserved receipt or modified it")
    receipt["runs"].append({"source": relative_source, "source_bytes": len(raw),
        "source_sha256": hashlib.sha256(raw).hexdigest(), "exit": "normal",
        "receipt": output_name, "receipt_sha256": hashlib.sha256(generated).hexdigest(),
        "preserved_receipt_unchanged": unchanged, "semantic_match_preserved_receipt": same,
        "result": json.loads(generated)})
receipt["finished_at_utc"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
receipt["status"] = "PASS"
(HERE / "REPLAY_RECEIPT.json").write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps(receipt, indent=2))
