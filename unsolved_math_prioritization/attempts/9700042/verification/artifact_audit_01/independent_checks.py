"""Independent finite replay and bounded validation-format controls.

Arguments: SOURCE_DIRECTORY OUTPUT_DIRECTORY. Invoke under -I -S -B.
Reviewed packet code is authenticated before any execution. Temporary copies are
small and strictly local to OUTPUT_DIRECTORY. This is not a hostile-code sandbox.
"""
from pathlib import Path
import ast
import hashlib
import json
import os
import shutil
import stat
import subprocess
import sys
import tempfile

source, output = map(lambda x: Path(x).resolve(), sys.argv[1:])
scratch = output / "independent_scratch"
scratch.mkdir(exist_ok=True)
raw = output / "independent_private_raw"
raw.mkdir(exist_ok=True)
cwd = output / "unrelated_cwd"
cwd.mkdir(exist_ok=True)
tempfile.tempdir = str(scratch)
PIN = "13233e679fd24dffcf87407d934dcce80af7eb23132fe490227ce6edb62d85b9"
CHECKERS = (
    ("verify_resume_turn1.py", "TURN_C1_CHECKS.json"),
    ("verify_resume_turn4.py", "TURN_C4_CHECKS.json"),
    ("audit_c1/check_independent.py", "audit_c1/INDEPENDENT_CHECKS.json"),
    ("audit_a/check_independent_c4.py", "audit_a/INDEPENDENT_CHECKS.json"),
    ("audit_b/independent_checks.py", "audit_b/INDEPENDENT_CHECKS.json"),
)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def emit(name, value):
    (output / name).write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")

def normalize(text, directory):
    return text.replace(str(directory), "<independent-fixture>").replace(str(source), "<original-packet>")

manifest = json.loads((source / "PACKET_MANIFEST.json").read_bytes())
records = {r["path"]: r for r in manifest["files"]}
for rel, record in records.items():
    data = (source / rel).read_bytes()
    if (len(data), sha(data), hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()) != (record["bytes"], record["sha256"], record["git_blob"]):
        raise RuntimeError("Source changed since assigned-head authentication")
root_bytes = (source / "verify_packet.py").read_bytes()
if sha(root_bytes) != PIN:
    raise RuntimeError("Root verifier pin mismatch")
namespace = {"__name__": "reviewed_verifier_definitions_only", "__file__": str(source / "verify_packet.py")}
exec(compile(root_bytes, "<reviewed-verifier>", "exec", optimize=0), namespace)
authenticate = namespace["authenticate"]

# Independently validate packet semantics and the declared historical boundary.
relocations = []
for record in manifest["relocated_authored_artifacts"]:
    data = (source / record["packet_path"]).read_bytes()
    relocations.append({"audit_origin": record["audit_origin"], "packet_path": record["packet_path"], "bytes_match": len(data) == record["bytes"], "sha256_match": sha(data) == record["sha256"]})
historical = []
for directory in ("audit_a", "audit_b", "audit_c1"):
    audit = json.loads((source / directory / "AUDIT_MANIFEST.json").read_bytes())
    inventory = audit.get("files", audit.get("artifacts", []))
    included, historical_only = [], []
    for record in inventory:
        same = [r["path"] for r in records.values() if r["sha256"] == record["sha256"] and r["bytes"] == record["bytes"]]
        target = {"historical_path": record["path"], "same_bytes_in_packet_at": same}
        (included if same else historical_only).append(target)
    historical.append({"audit": directory, "inventory_count": len(inventory), "represented_by_same_bytes": included, "not_represented_by_same_bytes": historical_only, "meaning": "Historical inventory; packet README and packet manifest explicitly state that absent historical entries are omitted."})
semantics = {"payload_record_count": len(manifest["files"]), "unique_payload_path_count": len(records), "total_with_self": len(records)+1, "manifest_excludes_itself": "PACKET_MANIFEST.json" not in records, "turns": manifest["turns"], "accepted_revision": manifest["accepted_revision"], "accepted_revision_sha256_matches": sha((source / manifest["accepted_revision"]).read_bytes()) == manifest["accepted_revision_sha256"], "relocations": relocations, "historical_inventories": historical}
emit("MANIFEST_SEMANTICS.json", semantics)

# Each case receives a fresh <215 kB copy; fixtures are deleted immediately.
controls = []
def control(name, mutate, expected):
    with tempfile.TemporaryDirectory(prefix="format-", dir=scratch) as td:
        parent = Path(td)
        fixture = parent / "packet"
        shutil.copytree(source, fixture)
        for file in fixture.rglob("*"):
            if file.is_file():
                file.chmod(0o600)
        mutate(fixture, parent)
        try:
            count = authenticate(fixture)
            accepted, detail = True, {"authenticated_payload_records": count}
        except Exception as exc:
            accepted, detail = False, {"exception_type": type(exc).__name__, "message_normalized": normalize(str(exc), parent)}
        result = {"case": name, "accepted": accepted, "expected_behavior_from_read_code": expected, "matches_expected": accepted == expected, **detail}
        controls.append(result)
        if accepted != expected:
            raise RuntimeError("Unexpected format-control outcome: " + name)

def alter_manifest(fixture, update):
    m = json.loads((fixture / "PACKET_MANIFEST.json").read_bytes())
    update(m)
    (fixture / "PACKET_MANIFEST.json").write_text(json.dumps(m))

def symlink_payload(fixture, parent):
    p = fixture / "TURN_C4_CHECKS.json"
    target = parent / "same-checks.json"
    target.write_bytes(p.read_bytes())
    p.unlink()
    p.symlink_to(target)

def symlink_manifest(fixture, parent):
    p = fixture / "PACKET_MANIFEST.json"
    target = parent / "same-manifest.json"
    target.write_bytes(p.read_bytes())
    p.unlink()
    p.symlink_to(target)

def duplicate_json_key(fixture, parent):
    p = fixture / "PACKET_MANIFEST.json"
    data = p.read_text()
    p.write_text('{"files": [],' + data[1:])

control("unchanged", lambda p,t: None, True)
control("bad_sha256_pin", lambda p,t: alter_manifest(p, lambda m: m["files"][0].update(sha256="0"*64)), False)
control("bad_git_blob_pin", lambda p,t: alter_manifest(p, lambda m: m["files"][0].update(git_blob="0"*40)), False)
control("bad_byte_count_pin", lambda p,t: alter_manifest(p, lambda m: m["files"][0].update(bytes=0)), False)
control("inventory_wrong_container_type", lambda p,t: alter_manifest(p, lambda m: m.update(files={})), False)
control("inventory_path_wrong_type", lambda p,t: alter_manifest(p, lambda m: m["files"][0].update(path=False)), False)
control("missing_file", lambda p,t: (p / "TURN_C4_CHECKS.json").unlink(), False)
control("extra_regular_file", lambda p,t: (p / "EXTRA.txt").write_text("x"), False)
control("altered_proof", lambda p,t: (p / "TURN_C4_BK_POISSON_REVISED.md").write_bytes((p / "TURN_C4_BK_POISSON_REVISED.md").read_bytes()+b"\n"), False)
control("listed_payload_symlink", symlink_payload, False)
control("expected_file_replaced_by_directory", lambda p,t: ((p / "TURN_C4_CHECKS.json").unlink(), (p / "TURN_C4_CHECKS.json").mkdir()), False)
control("extra_empty_directory", lambda p,t: (p / "EXTRA_EMPTY").mkdir(), True)
control("extra_dangling_symlink", lambda p,t: (p / "IGNORED.link").symlink_to("absent-target"), True)
control("extra_fifo_not_read", lambda p,t: os.mkfifo(p / "IGNORED.fifo"), True)
control("manifest_itself_symlink", symlink_manifest, True)
control("duplicate_payload_record", lambda p,t: alter_manifest(p, lambda m: m["files"].append(dict(m["files"][0]))), True)
control("duplicate_json_key_last_wins", duplicate_json_key, True)
control("unvalidated_accepted_revision_metadata", lambda p,t: alter_manifest(p, lambda m: m.update(accepted_revision_sha256="0"*64)), True)
control("unvalidated_turn_count_metadata", lambda p,t: alter_manifest(p, lambda m: m.update(turns="0/5")), True)
control("manifest_whitespace_only_change", lambda p,t: (p / "PACKET_MANIFEST.json").write_text(json.dumps(manifest, separators=(",", ":"))), True)
emit("FORMAT_CONTROLS.json", {"controls": controls, "all_match_read_code": all(r["matches_expected"] for r in controls), "boundary": "Root authenticate is a pinned-payload replay integrity helper, not a full typed schema or a strict all-filesystem-entry validator. External assigned-head authentication separately pins the manifest bytes and regular-entry inventory."})
print("format controls complete: " + str(len(controls)), flush=True)

# Independently replay the real patches with the same declared zero-fuzz policy.
patch_results = []
for original, patch, revised in (("TURN_C1_MARKED_DEFECT_BOUND.md", "audit_c1/C1_CLARIFICATION.patch", "audit_c1/TURN_C1_CLARIFIED.md"), ("TURN_C4_BK_POISSON_CANDIDATE.md", "C4_CLARIFICATION.patch", "TURN_C4_BK_POISSON_REVISED.md")):
    with tempfile.TemporaryDirectory(prefix="patch-", dir=scratch) as td:
        directory = Path(td)
        target = directory / "input.md"
        before, patch_bytes, expected = ((source / p).read_bytes() for p in (original, patch, revised))
        target.write_bytes(before)
        command = [shutil.which("patch"), "--batch", "--fuzz=0", str(target)]
        run = subprocess.run(command, input=patch_bytes, cwd=cwd, capture_output=True, timeout=30)
        actual = target.read_bytes()
        context = next(line[1:] for line in patch_bytes.splitlines(keepends=True) if line.startswith(b" ") and line[1:].strip())
        target.write_bytes(before.replace(context, b"INDEPENDENT_CHANGED_CONTEXT\n", 1))
        negative = subprocess.run(command, input=patch_bytes, cwd=cwd, capture_output=True, timeout=30)
        if run.returncode or actual != expected or negative.returncode == 0:
            raise RuntimeError("Independent patch replay/control failed")
        name = "c1" if "C1" in original else "c4"
        (raw / (name+".patch.stdout")).write_bytes(run.stdout)
        (raw / (name+".patch.stderr")).write_bytes(run.stderr)
        (raw / (name+".patch-negative.stdout")).write_bytes(negative.stdout)
        (raw / (name+".patch-negative.stderr")).write_bytes(negative.stderr)
        patch_results.append({"original": original, "patch": patch, "revised": revised, "requested_flags": ["--batch", "--fuzz=0"], "returncode": run.returncode, "actual_output_bytes": len(actual), "actual_output_sha256": sha(actual), "matches_frozen_output_bytes": actual == expected, "stdout_actual_bytes": len(run.stdout), "stdout_actual_sha256": sha(run.stdout), "stdout_text_normalized": normalize(run.stdout.decode(), directory), "damaged_context_returncode": negative.returncode, "damaged_context_stdout_actual_bytes": len(negative.stdout), "damaged_context_stdout_actual_sha256": sha(negative.stdout), "damaged_context_stdout_text_normalized": normalize(negative.stdout.decode(), directory)})
emit("INDEPENDENT_PATCH_REPLAYS.json", patch_results)

# This new bootstrap independently compiles source bytes with optimize=0. It
# records actual flags from inside the same executing child, then enforces the
# forced-failure gate even when its interpreter has optimize=1.
BOOTSTRAP = r'''
import ast, hashlib, json, pathlib, sys
path = pathlib.Path(sys.argv[1])
data = path.read_bytes()
if hashlib.sha256(data).hexdigest() != sys.argv[2]:
    raise RuntimeError('Independent source pin failed')
flags = {name: getattr(sys.flags, name) for name in ('optimize', 'isolated', 'no_site', 'dont_write_bytecode', 'ignore_environment', 'safe_path')}
print('ACTUAL_FLAGS=' + json.dumps(flags, sort_keys=True), file=sys.stderr, flush=True)
tree = ast.parse(data, filename=str(path))
if sys.argv[3] == 'force_failure':
    index = int(bool(tree.body and isinstance(tree.body[0], ast.Expr) and isinstance(tree.body[0].value, ast.Constant) and isinstance(tree.body[0].value.value, str)))
    tree.body.insert(index, ast.Assert(test=ast.Constant(value=False), msg=ast.Constant(value='INDEPENDENT_FORCED_ASSERTION')))
    ast.fix_missing_locations(tree)
exec(compile(tree, str(path), 'exec', optimize=0), {'__name__': '__main__', '__file__': str(path)})
'''
direct = []
for script, destination in CHECKERS:
    data, expected = (source / script).read_bytes(), (source / destination).read_bytes()
    assertions = sum(isinstance(node, ast.Assert) for node in ast.walk(ast.parse(data)))
    for label, mode in (("normal", []), ("O", ["-O"]), ("I", ["-I"]), ("IO", ["-I", "-O"])):
        with tempfile.TemporaryDirectory(prefix="checker-", dir=scratch) as td:
            directory = Path(td)
            path = directory / Path(script).name
            path.write_bytes(data)
            flags = ["-S", "-B", *mode]
            base = [sys.executable, *flags, "-c", BOOTSTRAP, str(path), sha(data)]
            run = subprocess.run(base + ["positive"], cwd=cwd, capture_output=True, timeout=600)
            actual = path.with_name(Path(destination).name).read_bytes() if run.returncode == 0 else b""
            negative = subprocess.run(base + ["force_failure"], cwd=cwd, capture_output=True, timeout=30)
            actual_flags = json.loads(run.stderr.decode().splitlines()[0].removeprefix("ACTUAL_FLAGS="))
            ident = "%02d" % (len(direct)+1)
            (raw / (ident+".checker.stdout")).write_bytes(run.stdout)
            (raw / (ident+".checker.stderr")).write_bytes(run.stderr)
            (raw / (ident+".checker.output.json")).write_bytes(actual)
            (raw / (ident+".checker-negative.stderr")).write_bytes(negative.stderr)
            record = {"checker": script, "mode_label": label, "requested_flags": flags, "actual_same_process_flags": actual_flags, "checker_sha256": sha(data), "static_assertion_statement_count": assertions, "checker_compilation_optimize": 0, "returncode": run.returncode, "actual_output_bytes": len(actual), "actual_output_sha256": sha(actual), "matches_frozen_output_bytes": actual == expected, "stdout_actual_bytes": len(run.stdout), "stdout_actual_sha256": sha(run.stdout), "stderr_actual_bytes": len(run.stderr), "stderr_actual_sha256": sha(run.stderr), "forced_assertion_returncode": negative.returncode, "forced_assertion_rejected": negative.returncode != 0 and b"INDEPENDENT_FORCED_ASSERTION" in negative.stderr, "forced_assertion_stderr_actual_bytes": len(negative.stderr), "forced_assertion_stderr_actual_sha256": sha(negative.stderr)}
            direct.append(record)
            emit("INDEPENDENT_CHECKER_REPLAYS.json", direct)
            print(json.dumps({"checker": script, "mode": label, "pass": run.returncode == 0 and actual == expected and record["forced_assertion_rejected"]}), flush=True)
            if run.returncode or actual != expected or not record["forced_assertion_rejected"]:
                raise RuntimeError("Independent checker replay failed; inspect private raw receipts")

# Profile the root's exact requested child prefixes separately. These probes
# execute no checker; they report the interpreter flag semantics of those exact
# prefixes. We label them separately from same-process direct instrumentation.
profiles = []
probe = "import json,sys;print(json.dumps({name:getattr(sys.flags,name) for name in ('optimize','isolated','no_site','dont_write_bytecode','ignore_environment','safe_path')},sort_keys=True))"
for mode in ([], ["-O"], ["-I"], ["-I", "-O"]):
    run = subprocess.run([sys.executable, *mode, "-c", probe], cwd=cwd, capture_output=True, timeout=30)
    profiles.append({"requested_flags": mode, "returncode": run.returncode, "separate_probe_actual_flags": json.loads(run.stdout), "stdout_actual_bytes": len(run.stdout), "stdout_actual_sha256": sha(run.stdout), "scope": "Separate same-interpreter/prefix probe; not instrumentation inside an unchanged root child."})
emit("NESTED_FLAG_PREFIX_PROBES.json", profiles)
emit("INDEPENDENT_SUMMARY.json", {"format_controls": len(controls), "independent_patch_positive_runs": len(patch_results), "independent_patch_negative_runs": len(patch_results), "direct_checker_positive_runs": len(direct), "direct_forced_failure_runs": len(direct), "nested_flag_prefix_probes": len(profiles), "all_passed": True, "scope": "Authenticity and finite reproducibility only; no theorem or priority conclusion."})
shutil.rmtree(scratch)
