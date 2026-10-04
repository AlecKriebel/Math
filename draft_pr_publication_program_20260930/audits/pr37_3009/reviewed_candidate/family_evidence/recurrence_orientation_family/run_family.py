#!/usr/bin/env python3
"""Exact execution receipt wrapper; preserve failures rather than suppress them."""
from pathlib import Path
import datetime
import hashlib
import json
import subprocess
import sys

HERE = Path(__file__).resolve().parent
receipts_path = HERE / "family_execution_receipts.json"
receipts = json.loads(receipts_path.read_text()) if receipts_path.exists() else []
for name in ["check_independent_controls.py", "replay_original.py"]:
    script = HERE/name
    command = [sys.executable, str(script)]
    p = subprocess.run(command, cwd=HERE, capture_output=True, text=True)
    r = {"timestamp_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
         "command": command, "cwd": str(HERE),
         "script_sha256": hashlib.sha256(script.read_bytes()).hexdigest(),
         "return_code": p.returncode, "stdout": p.stdout, "stderr": p.stderr}
    receipts.append(r)
    receipts_path.write_text(json.dumps(receipts, indent=2)+"\n")
    print(json.dumps({"script": name, "return_code": p.returncode,
                      "stderr": p.stderr, "stdout_characters": len(p.stdout)}))
    if p.returncode != 0:
        raise SystemExit(p.returncode)
