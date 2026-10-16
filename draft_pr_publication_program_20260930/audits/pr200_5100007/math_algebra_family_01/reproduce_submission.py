"""Copy and replay immutable submitted files in this family directory only."""
import ast
import hashlib
import json
from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parent
archive = root.parent / "original_submitted_head"
source = (archive / "verify.py").read_bytes()
proof = (archive / "PROOF.md").read_bytes()
tree = ast.parse(source)
inventory = [{"line": n.lineno, "text": ast.get_source_segment(source.decode(), n)}
             for n in ast.walk(tree) if isinstance(n, ast.Assert)]
summary = {"source_sha256": hashlib.sha256(source).hexdigest(),
           "proof_sha256": hashlib.sha256(proof).hexdigest(),
           "assertions_removed_under_O": inventory, "replays": {}}
for name, options in [("normal", []), ("optimized", ["-O"])]:
    replay = root / ("submitted_replay_" + name)
    replay.mkdir(exist_ok=True)
    (replay / "verify.py").write_bytes(source)
    (replay / "PROOF.md").write_bytes(proof)
    launcher = ("import sys,runpy; sys.path.insert(0," + repr(str(root / "runtime_packages"))
                + "); runpy.run_path(" + repr(str(replay / "verify.py")) + ",run_name='__main__')")
    command = [sys.executable, "-E", "-B", "-P"] + options + ["-c", launcher]
    completed = subprocess.run(command, capture_output=True, text=True)
    (replay / "stdout.txt").write_text(completed.stdout)
    (replay / "stderr.txt").write_text(completed.stderr)
    summary["replays"][name] = {"command": command, "returncode": completed.returncode}
    print(name, "returncode", completed.returncode, flush=True)
    if completed.returncode:
        print(completed.stderr, flush=True)
(root / "reproduction_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
print(json.dumps(summary, indent=2))
