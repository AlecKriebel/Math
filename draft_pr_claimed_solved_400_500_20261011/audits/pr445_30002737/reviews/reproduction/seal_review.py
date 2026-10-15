#!/usr/bin/env python3
"""Positive authored-only manifest, excluding its own circular digest."""
from pathlib import Path
from datetime import datetime, timezone
import ast
import hashlib
import json

HERE = Path(__file__).resolve().parent
TOP_LEVEL = ['REPORT.md', 'RESULT.json', 'RESEARCH_LOG.md', 'run_reproduction.py',
             'download_sources.py', 'fetch_frozen_blobs.py', 'exact_controls.py',
             'run_exact_controls.py', 'seal_review.py']
paths = [HERE / name for name in TOP_LEVEL] + sorted((HERE / 'records').glob('*.json'))
for path in paths:
    if not path.is_file():
        raise RuntimeError(f'Missing authored artifact: {path}')
    if path.suffix == '.py' and any(isinstance(n, ast.Assert) for n in ast.walk(ast.parse(path.read_text()))):
        raise RuntimeError(f'New controlling code contains assert: {path}')
result = json.loads((HERE / 'RESULT.json').read_text())
for key in ['pr', 'problem_id', 'blocking_findings', 'required_repairs', 'central_mathematical_gaps']:
    if type(result[key]) is not int:
        raise TypeError(f'Result field must be an integer: {key}')
if result['reviewer'] != '/root/pr445_reproduction':
    raise RuntimeError('Wrong reviewer identity')
entries = [{'path': str(path.relative_to(HERE)), 'bytes': path.stat().st_size,
            'sha256': hashlib.sha256(path.read_bytes()).hexdigest()} for path in paths]
manifest = {'schema_version': 1, 'pr': 445, 'problem_id': 30002737,
            'frozen_head': '3242c84e06db7e99012c7fe581adde5c3f89fc89',
            'reviewer': '/root/pr445_reproduction',
            'sealed_at_utc': datetime.now(timezone.utc).isoformat(),
            'policy': 'Positive authored-only list; private sources/fixtures/copies/cache excluded; manifest excludes itself',
            'files': entries}
(HERE / 'PUBLIC_FILES.json').write_text(json.dumps(manifest, indent=2)+'\n')
saved = json.loads((HERE / 'PUBLIC_FILES.json').read_text())
for entry in saved['files']:
    path = HERE / entry['path']
    if path.stat().st_size != entry['bytes'] or hashlib.sha256(path.read_bytes()).hexdigest() != entry['sha256']:
        raise RuntimeError(f'Seal verification failed: {path}')
print(f'Sealed and verified {len(entries)} authored artifacts.')
