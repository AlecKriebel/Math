#!/usr/bin/env python3
"""One ordinary unmodified isolated native route; no repair or retry."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time

K = Path(__file__).resolve().parent
SOURCE = K.parent.parent / "sources/archives/02-gram_locus_support.zip.extracted"
RUNTIME = K / "runtime"
NAMES = ["verify_controls.py", "verify_exact.py", "gram_locus_note.tex"]

def pin(path):
    data = path.read_bytes()
    return {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest(),
            "mode_octal": oct(path.stat().st_mode & 0o7777)}

assert not RUNTIME.exists(), "Runtime already exists; no retry"
RUNTIME.mkdir()
before = {name: pin(SOURCE / name) for name in NAMES}
for name in NAMES:
    shutil.copyfile(SOURCE / name, RUNTIME / name)
    (RUNTIME / name).chmod(0o644)
assert {name: pin(RUNTIME / name) for name in NAMES} == before
argv = [sys.executable, "-E", "-S", "-B", "-P", "verify_controls.py"]
stamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
start = time.monotonic()
result = subprocess.run(argv, cwd=RUNTIME, capture_output=True, timeout=180)
duration = time.monotonic() - start
(K / "NATIVE.stdout.bin").write_bytes(result.stdout)
(K / "NATIVE.stderr.bin").write_bytes(result.stderr)
after = {name: pin(SOURCE / name) for name in NAMES}
copy_after = {name: pin(RUNTIME / name) for name in NAMES}
receipt = {"UTC_start": stamp, "UTC_end": datetime.datetime.now(datetime.timezone.utc).isoformat(),
           "elapsed_seconds": duration, "argv": argv, "cwd": str(RUNTIME),
           "exit_code": result.returncode, "Python_version": sys.version,
           "resolved_executable": os.path.realpath(sys.executable),
           "stdout_bytes": len(result.stdout), "stderr_bytes": len(result.stderr),
           "native_inputs_before": before, "native_inputs_after": after,
           "isolated_inputs_after": copy_after,
           "input_guards_exact": before == after == copy_after,
           "route_invocations": 1, "retry_or_repair": False,
           "internal_deliberate_false_variants_are_part_of_unmodified_driver": True}
(K / "NATIVE_RECEIPT.json").write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps(receipt))
if result.returncode != 0:
    raise SystemExit(result.returncode)
assert before == after == copy_after, "Native input guard failed"
