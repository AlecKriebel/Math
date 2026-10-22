"""Observe the exact reviewed root without altering its bytes or child commands.

Arguments: SOURCE_DIRECTORY OUTPUT_DIRECTORY. Run with -I -S -B [and -O].
All ephemeral and retained writes stay under OUTPUT_DIRECTORY.
"""
from pathlib import Path
import hashlib
import json
import os
import subprocess
import sys
import tempfile

PIN = "13233e679fd24dffcf87407d934dcce80af7eb23132fe490227ce6edb62d85b9"
source, output = map(lambda x: Path(x).resolve(), sys.argv[1:])
output.mkdir(parents=True, exist_ok=True)
scratch = output / "scratch"
scratch.mkdir()
os.environ["TMPDIR"] = str(scratch)
tempfile.tempdir = str(scratch)
raw = output / "private_raw"
raw.mkdir()
events = []
original_run = subprocess.run

def sha(data):
    return hashlib.sha256(data).hexdigest()

def normalize(value):
    if isinstance(value, str):
        return value.replace(str(source), "<original-packet>").replace(str(output), "<audit-run>").replace(sys.executable, "<python>")
    if isinstance(value, (list, tuple)):
        return [normalize(x) for x in value]
    return value

def observed_run(args, *positional, **kwargs):
    run = original_run(args, *positional, **kwargs)
    ident = "%03d" % (len(events) + 1)
    stdout, stderr = run.stdout or b"", run.stderr or b""
    (raw / (ident + ".stdout")).write_bytes(stdout)
    (raw / (ident + ".stderr")).write_bytes(stderr)
    child_flags = []
    if args[0] == sys.executable:
        child_flags = args[1:args.index("-c")]
    record = {"id": ident, "command_role_normalized": normalize(args), "cwd_role_normalized": normalize(str(kwargs.get("cwd", ""))), "returncode": run.returncode, "stdout_actual_bytes": len(stdout), "stdout_actual_sha256": sha(stdout), "stderr_actual_bytes": len(stderr), "stderr_actual_sha256": sha(stderr), "stdout_text_normalized": normalize(stdout.decode(errors="replace")), "stderr_text_normalized": normalize(stderr.decode(errors="replace")), "python_requested_flags": child_flags}
    if args[0] == sys.executable:
        record["bootstrap_sha256"] = sha(args[args.index("-c") + 1].encode())
        record["kind"] = args[-1]
    else:
        record["kind"] = "patch"
        record["stdin_actual_bytes"] = len(kwargs.get("input", b""))
        record["stdin_actual_sha256"] = sha(kwargs.get("input", b""))
    events.append(record)
    return run

data = (source / "verify_packet.py").read_bytes()
if sha(data) != PIN:
    raise RuntimeError("Root verifier differs from reviewed pin")
subprocess.run = observed_run
original_argv = sys.argv[:]
sys.argv = [str(source / "verify_packet.py")]
try:
    exec(compile(data, str(source / "verify_packet.py"), "exec", optimize=0), {"__name__": "__main__", "__file__": str(source / "verify_packet.py")})
finally:
    sys.argv = original_argv
    subprocess.run = original_run
    receipt = {"root_sha256": sha(data), "root_compilation_optimize": 0, "root_effective_flags": {name: getattr(sys.flags, name) for name in ("optimize", "isolated", "no_site", "dont_write_bytecode", "ignore_environment", "safe_path")}, "python_version": sys.version, "python_executable_role": "same-system-python-as-launcher", "events": events, "counts": {kind: sum(e["kind"] == kind for e in events) for kind in ("positive", "negative", "patch")}, "count_corrupt_positive": sum(e["kind"] == "positive" and e["returncode"] != 0 for e in events), "child_flag_note": "Requested child flags are captured from actual commands. Root isolation/no-site/bytecode flags do not propagate unless explicitly included. Child bootstrap always compiles the frozen checker AST with optimize=0."}
    (output / "TRACE.json").write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n")
