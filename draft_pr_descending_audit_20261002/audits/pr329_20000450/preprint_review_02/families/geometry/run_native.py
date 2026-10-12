#!/usr/bin/env python3
"""Capture a native command, body hashes, UTC clock, and complete byte streams."""
from pathlib import Path
import datetime, hashlib, json, subprocess, sys

p = Path(__file__).resolve().parent
label, *argv = sys.argv[1:]
start = datetime.datetime.now(datetime.timezone.utc).isoformat()
body_hashes = {}
for arg in argv:
    f = Path(arg)
    if f.is_file():
        body_hashes[str(f.resolve())] = hashlib.sha256(f.read_bytes()).hexdigest()
r = subprocess.run(argv, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
end = datetime.datetime.now(datetime.timezone.utc).isoformat()
(p / (label + '.stdout.txt')).write_bytes(r.stdout)
(p / (label + '.stderr.txt')).write_bytes(r.stderr)
receipt = dict(argv=argv, utc_start=start, utc_end=end, exit_code=r.returncode,
               input_file_sha256=body_hashes,
               stdout_utf8=r.stdout.decode(errors='replace'),
               stderr_utf8=r.stderr.decode(errors='replace'))
(p / (label + '.receipt.json')).write_text(json.dumps(receipt, indent=2) + '\n')
print(json.dumps(receipt, indent=2))
sys.exit(r.returncode)
