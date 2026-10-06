#!/usr/bin/env python3
"""Run a byte-identical copy of the 135-assertion author script in ignored tmp."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import shutil
import subprocess
import sys

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / 'source_snapshot'
COPY = HERE / 'tmp' / 'author_reproduction'
COPY.mkdir(parents=True, exist_ok=True)
snapshot_files = ('PARTIAL_RESULTS.md', 'verify.py', 'verification.json', 'input_record.json', 'SOURCES.md')
digest = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
before = {name: digest(SOURCE / name) for name in snapshot_files}
shutil.copyfile(SOURCE / 'verify.py', COPY / 'verify.py')
run = subprocess.run([sys.executable, '-B', str(COPY / 'verify.py')], cwd=COPY, capture_output=True, text=True)
after = {name: digest(SOURCE / name) for name in snapshot_files}
receipt = json.loads((COPY / 'verification.json').read_text()) if (COPY / 'verification.json').exists() else None
original = json.loads((SOURCE / 'verification.json').read_text())
out = {'checked_at_utc': datetime.now(timezone.utc).isoformat(), 'python': sys.version,
       'frozen_head': 'dae2b77074945443e1b91c92f641ff9feff12235',
       'frozen_hashes_before': before, 'frozen_hashes_after': after,
       'copy_sha256': digest(COPY / 'verify.py'), 'exit_code': run.returncode,
       'stdout': run.stdout, 'stderr': run.stderr, 'receipt': receipt,
       'receipt_matches_frozen': receipt == original,
       'frozen_files_unchanged': before == after}
(HERE / 'evidence' / 'author_reproduction.json').write_text(json.dumps(out, indent=2) + '\n')
assert run.returncode == 0 and receipt['assertions'] == 135
assert receipt == original and before == after
print(json.dumps({'status': 'passed', 'assertions': receipt['assertions'],
                  'receipt_matches_frozen': receipt == original, 'frozen_files_unchanged': before == after}, indent=2))
