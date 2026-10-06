"""Read-only verification of every public member and the exact public inventory."""
from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import sys

root = Path(__file__).resolve().parent
manifest_path = root / 'SHA256SUMS.json'
manifest = json.loads(manifest_path.read_text())
expected = manifest['files']
actual = sorted(str(path.relative_to(root)) for path in root.rglob('*') if path.is_file() and 'private' not in path.relative_to(root).parts and '__pycache__' not in path.relative_to(root).parts and path.name != 'SHA256SUMS.json')
errors = []
if actual != sorted(expected):
    errors.append('public inventory differs')
for name, item in expected.items():
    path = root / name
    if not path.is_file():
        errors.append(name + ': missing')
        continue
    data = path.read_bytes()
    if len(data) != item['bytes'] or sha256(data).hexdigest() != item['sha256']:
        errors.append(name + ': bytes or hash differ')
print(json.dumps({'UTC': datetime.now(timezone.utc).isoformat(), 'PID': os.getpid(), 'status': 'PASS' if not errors else 'FAIL', 'public_members_checked': len(expected), 'REPORT_sha256': sha256((root/'REPORT.md').read_bytes()).hexdigest(), 'RESULT_sha256': sha256((root/'RESULT.json').read_bytes()).hexdigest(), 'manifest_sha256': sha256(manifest_path.read_bytes()).hexdigest(), 'errors': errors}, sort_keys=True))
sys.exit(bool(errors))
