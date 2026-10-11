#!/usr/bin/env python3
"""Reproduce original programs in this family's isolated copy only."""
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json
import shutil
import subprocess
import sys

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / "source_snapshot"
DESTINATION = HERE / "isolated_original_replay"
shutil.copytree(SOURCE, DESTINATION, dirs_exist_ok=True)
receipt = {"utc": datetime.now(timezone.utc).isoformat(), "python": sys.version,
           "scripts": [], "source_copy_hashes": []}
for original in sorted(SOURCE.rglob("*")):
    if not original.is_file():
        continue
    relative = original.relative_to(SOURCE)
    digest = hashlib.sha256(original.read_bytes()).hexdigest()
    assert digest == hashlib.sha256((DESTINATION / relative).read_bytes()).hexdigest()
    receipt["source_copy_hashes"].append({"path": str(relative), "sha256": digest, "copy_identical": True})
for script, output in (("check_coupling.py", "check_results.json"),
                       ("review/independent_checks.py", "review/independent_results.json")):
    run = subprocess.run([sys.executable, script], cwd=DESTINATION, text=True, capture_output=True)
    stem = Path(script).stem
    (HERE / (stem + "_replay.stdout")).write_text(run.stdout)
    (HERE / (stem + "_replay.stderr")).write_text(run.stderr)
    old = (SOURCE / output).read_bytes()
    new = (DESTINATION / output).read_bytes()
    receipt["scripts"].append({"script": script, "returncode": run.returncode,
                               "source_script_sha256": hashlib.sha256((SOURCE / script).read_bytes()).hexdigest(),
                               "result_bytes_identical": old == new,
                               "result_sha256": hashlib.sha256(new).hexdigest(), "result": json.loads(new)})
    assert run.returncode == 0 and old == new
patch = (HERE.parent / "pr_input/diff.patch").read_text()
checked = []
for section in patch.split("diff --git ")[1:]:
    lines = section.splitlines()
    path = lines[0].split(" b/", 1)[1]
    if path.endswith("QUEUE.md"):
        checked.append({"path": path,
                        "queue_postimage_row": [line[1:] for line in lines if line.startswith("+| 49")][0]})
        continue
    postimage = "\n".join(line[1:] for line in lines if line.startswith("+") and not line.startswith("+++")) + "\n"
    relative = path.split("attempts/10000043/", 1)[1]
    assert postimage.encode() == (SOURCE / relative).read_bytes()
    checked.append({"path": path, "postimage_sha256": hashlib.sha256(postimage.encode()).hexdigest(),
                    "snapshot_identical": True})
assert len(checked) == 16
receipt["exact_diff_postimages"] = checked
receipt["reviewed_partial_byte_identical"] = (SOURCE / "PARTIAL.md").read_bytes() == (SOURCE / "review/reviewed_partial.md").read_bytes()
assert receipt["reviewed_partial_byte_identical"]
(HERE / "ORIGINAL_REPLAY_RECEIPT.json").write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps({"scripts": [{"script": item["script"], "returncode": item["returncode"],
                              "assertions": item["result"]["assertions"], "result_bytes_identical": item["result_bytes_identical"]}
                             for item in receipt["scripts"]],
                  "source_files": len(receipt["source_copy_hashes"]), "diff_files": len(checked)}))
