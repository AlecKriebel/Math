"""Capture complete outputs and verify every original frozen binding."""
from pathlib import Path
import datetime
import hashlib
import json
import subprocess
import sys

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parent
REPO = HERE.parents[3]
SNAPSHOT = AUDIT / "snapshot"
PREFIX = "unsolved_math_prioritization/attempts/2303016"
TARGET = SNAPSHOT / PREFIX
HEAD = "f4039c9c093b10e651ee7fd2e6379073b84238c7"
BASE = "efd29c05204703acca9a0860812f54b94fae54b1"
INTERPRETER = Path("/Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr378_30004322/sources_effective_review/private_runtime/bin/python")
PRIVATE = HERE / "private" / "replays"
PRIVATE.mkdir(parents=True, exist_ok=True)
checks = 0
commands = []
bindings = []


def require(value):
    global checks
    if not value:
        raise AssertionError("frozen packet or complete replay mismatch")
    checks += 1


def sha(data):
    return hashlib.sha256(data).hexdigest()


def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def capture(label, argv, cwd):
    start = utc()
    result = subprocess.run([str(x) for x in argv], cwd=cwd, capture_output=True)
    end = utc()
    outputs = {}
    for stream, data in [("stdout", result.stdout), ("stderr", result.stderr)]:
        path = PRIVATE / (label + "." + stream)
        path.write_bytes(data)
        outputs[stream] = {"path":path.relative_to(HERE).as_posix(), "bytes":len(data), "sha256":sha(data)}
    commands.append({"label":label, "argv":[str(x) for x in argv], "cwd":str(cwd),
                     "started_utc":start, "finished_utc":end, "returncode":result.returncode,
                     **outputs})
    require(result.returncode == 0)
    require(result.stderr == b"")
    return result.stdout


def manifest(path, root):
    rows = json.loads(path.read_bytes())["files"]
    names = [row["path"] for row in rows]
    require(len(set(names)) == len(names))
    for row in rows:
        relative = Path(row["path"])
        require(not relative.is_absolute() and ".." not in relative.parts)
        file = root / relative
        require(file.is_file() and not file.is_symlink())
        raw = file.read_bytes()
        require(len(raw) == row["bytes"] and sha(raw) == row["sha256"])
        bindings.append({"manifest":str(path), **row})
    return len(rows)


seal = json.loads((HERE / "CODE_SEAL.json").read_bytes())
for row in seal["files"]:
    file = Path(row["absolute_path"])
    raw = file.read_bytes()
    require(len(raw) == row["bytes"] and sha(raw) == row["sha256"])

snapshot_manifest = json.loads((AUDIT / "snapshot_manifest.json").read_bytes())
require(snapshot_manifest["head"] == HEAD and snapshot_manifest["base"] == BASE)
require(snapshot_manifest["target_prefix"] == PREFIX)
snapshot_rows = snapshot_manifest["files"]
require(len(snapshot_rows) == 22)
for i, row in enumerate(snapshot_rows):
    raw = (SNAPSHOT / row["path"]).read_bytes()
    require(len(raw) == row["bytes"] and sha(raw) == row["sha256"])
    actual = capture("git_blob_" + str(i), ["git", "show", HEAD + ":" + row["path"]], REPO)
    require(raw == actual)
    require(hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest() == row["git_blob_sha"])

tree = capture("git_target_tree", ["git", "ls-tree", "-r", "-z", HEAD, "--", PREFIX,
                                   "unsolved_math_prioritization/QUEUE.md"], REPO)
tree_rows = {}
for entry in tree.split(b"\0"):
    if not entry:
        continue
    metadata, name = entry.split(b"\t", 1)
    mode, kind, oid = metadata.split(b" ")
    require(mode == b"100644" and kind == b"blob")
    require(name.decode() not in tree_rows)
    tree_rows[name.decode()] = oid.decode()
require(tree_rows == {row["path"]:row["git_blob_sha"] for row in snapshot_rows})

manifest_counts = {}
for file, root in [
    (TARGET / "TURN_1_MANIFEST.json", TARGET),
    (TARGET / "FINAL_FROZEN_MANIFEST.json", TARGET),
    (TARGET / "final_review/REVIEW_MANIFEST.json", TARGET / "final_review"),
    (TARGET / "PUBLICATION_MANIFEST.json", TARGET),
]:
    manifest_counts[file.name] = manifest(file, root)
require(manifest_counts == {"TURN_1_MANIFEST.json":12, "FINAL_FROZEN_MANIFEST.json":13,
                            "REVIEW_MANIFEST.json":3, "PUBLICATION_MANIFEST.json":20})
publication = json.loads((TARGET / "PUBLICATION_MANIFEST.json").read_bytes())
require(publication["author_manifest_sha256"] == sha((TARGET / "FINAL_FROZEN_MANIFEST.json").read_bytes()))
require(publication["review_manifest_sha256"] == sha((TARGET / "final_review/REVIEW_MANIFEST.json").read_bytes()))
actual_target = sorted(file.relative_to(TARGET).as_posix() for file in TARGET.rglob("*") if file.is_file())
require(actual_target == sorted([row["path"] for row in publication["files"]] + ["PUBLICATION_MANIFEST.json"]))

git_names = capture("git_delta", ["git", "diff", "--name-only", BASE, HEAD], REPO).decode().splitlines()
require(sorted(git_names) == sorted(row["path"] for row in snapshot_rows))
base_queue = capture("git_base_queue", ["git", "show", BASE + ":unsolved_math_prioritization/QUEUE.md"], REPO)
head_queue = (SNAPSHOT / "unsolved_math_prioritization/QUEUE.md").read_bytes()
before = base_queue.splitlines(keepends=True)
after = head_queue.splitlines(keepends=True)
require(len(before) == len(after))
changed_lines = [i for i, (a, b) in enumerate(zip(before, after)) if a != b]
require(len(changed_lines) == 1)
line = changed_lines[0]
left, right = before[line].split(b"|"), after[line].split(b"|")
require(len(left) == len(right))
require(b"2303016 / AMR-022-3016" in left[2])
changed_cells = [i for i, (a, b) in enumerate(zip(left, right)) if a != b]
require(changed_cells == [8, 9])
require(right[8].strip() == b"already_solved" and right[9].strip() == b"1/5")

author = capture("author", [INTERPRETER, TARGET / "verify_turn1.py"], HERE)
require(author == (TARGET / "TURN_1_CHECKS.json").read_bytes())
historical = capture("historical", [INTERPRETER, TARGET / "final_review/check.py", TARGET], HERE)
require(historical == (TARGET / "final_review/CHECKS.json").read_bytes())
independent = capture("independent", [INTERPRETER, HERE / "independent_controls.py"], HERE)
independent_object = json.loads(independent)
require(independent_object["status"] == "PASS")
require(len(independent_object["negative_controls_rejected"]) == 7)

# Complete captured stdout/stderr streams are copied to public artifact paths
# only for the three small computation outputs, not the entire repository queue.
for label in ["author", "historical", "independent"]:
    for stream in ["stdout", "stderr"]:
        (HERE / (label + "." + stream)).write_bytes((PRIVATE / (label + "." + stream)).read_bytes())

result = {"status":"PASS", "completed_utc":utc(), "assertions":checks,
          "original_head":HEAD, "original_base":BASE, "whole_snapshot_files_verified":22,
          "target_files_verified":21, "historical_manifest_counts":manifest_counts,
          "complete_manifest_binding_instances":len(bindings), "all_bindings":bindings,
          "queue_physical_line":line+1, "queue_changed_cells":changed_cells,
          "author_full_output":json.loads(author), "historical_full_output":json.loads(historical),
          "independent_full_output":independent_object, "commands":commands,
          "scope":"Entire frozen local/Git bytes, all nested historical manifest bindings, whole original queue scope, complete author/historical/new outputs. The sealed mathematical derivation is the analytic evidence."}
(HERE / "REPRODUCTION.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
print(json.dumps({"status":"PASS", "assertions":checks, "manifest_binding_instances":len(bindings),
                  "snapshot_files":22, "commands":len(commands), "queue_physical_line":line+1,
                  "independent_assertions":independent_object["assertions"]}, indent=2, sort_keys=True))
