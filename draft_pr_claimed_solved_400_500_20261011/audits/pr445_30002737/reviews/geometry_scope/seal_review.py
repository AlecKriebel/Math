#!/usr/bin/env python3
"""Create a positive authored-only manifest; never include private source payloads."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PAYLOAD = (
    'REPORT.md', 'RESULT.json', 'RESEARCH_LOG.md', 'INITIAL_RECONSTRUCTION.md',
    'SOURCE_ACQUISITION.json', 'geometry_controls.py',
    'geometry_controls_results.json', 'seal_review.py',
)
files = []
for name in PAYLOAD:
    path = ROOT / name
    if not path.is_file() or path.is_symlink():
        raise ValueError('Missing or indirect authored payload: '+name)
    data = path.read_bytes()
    files.append({'path': name, 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest(), 'origin': 'authored_by_reviewer'})
result = json.loads((ROOT/'RESULT.json').read_text())
if result['pr'] != 445 or result['problem_id'] != '30002737' or result['frozen_head'] != '3242c84e06db7e99012c7fe581adde5c3f89fc89':
    raise ValueError('Review identity mismatch')
if any(type(result[k]) is not int for k in ('blocking_findings', 'required_repairs', 'central_mathematical_gaps')):
    raise ValueError('Counts must be integers')
manifest = {
    'schema_version': 1,
    'pr': 445,
    'problem_id': '30002737',
    'frozen_head': result['frozen_head'],
    'reviewer': result['reviewer'],
    'policy': 'Positive authored-only payload; no glob promotion, foreign source bytes, extracted source text, source renders, catalogue response, private/, cache or environment directories. PUBLIC_FILES.json is the index and has no self-hash.',
    'files': files,
    'excluded_directory_prefixes': ['private/', '__pycache__/', '.venv/', 'cache/'],
}
(ROOT/'PUBLIC_FILES.json').write_text(json.dumps(manifest, indent=2)+'\n')
print(json.dumps({'authored_payload_files':len(files), 'total_payload_bytes':sum(f['bytes'] for f in files), 'identity_check':'PASS', 'integer_counts_check':'PASS'},indent=2))
