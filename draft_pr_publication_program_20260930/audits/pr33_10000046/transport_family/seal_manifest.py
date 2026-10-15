#!/usr/bin/env python3
"""Generate or check the exact self-excluding first-party family manifest."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import sys

HERE = Path(__file__).resolve().parent
TARGET = HERE/'FINAL_MANIFEST.json'
EXCLUDED_DIRS = {'references', 'tmp', '__pycache__'}


def entries():
    answer = []
    for path in sorted(HERE.rglob('*')):
        relative = path.relative_to(HERE)
        if not path.is_file() or path == TARGET or any(part in EXCLUDED_DIRS for part in relative.parts):
            continue
        raw = path.read_bytes()
        answer.append({'path': str(relative), 'bytes': len(raw),
                       'sha256': hashlib.sha256(raw).hexdigest()})
    return answer


if '--check' in sys.argv:
    data = json.loads(TARGET.read_text())
    if data['files'] != entries():
        raise AssertionError('manifest differs from exact current first-party files')
    print(json.dumps({'pass': True, 'files': len(data['files']),
                      'manifest_sha256': hashlib.sha256(TARGET.read_bytes()).hexdigest()}))
else:
    data = {'sealed_utc': datetime.now(timezone.utc).isoformat(),
            'scope': 'All regular first-party files recursively in transport_family',
            'self_excluded': 'FINAL_MANIFEST.json',
            'excluded_directories': sorted(EXCLUDED_DIRS),
            'files': entries()}
    TARGET.write_text(json.dumps(data, indent=2)+'\n')
    print(json.dumps({'sealed': True, 'files': len(data['files']),
                      'manifest_sha256': hashlib.sha256(TARGET.read_bytes()).hexdigest()}))
