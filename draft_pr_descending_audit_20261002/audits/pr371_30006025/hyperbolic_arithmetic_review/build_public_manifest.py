#!/usr/bin/env python3
"""Build the explicit owned public inventory; all private payloads excluded."""
from pathlib import Path
import datetime, hashlib, json
ROOT = Path(__file__).resolve().parent
PRIVATE = {'private_sources','private_replays','__pycache__'}
files = []
for path in sorted(ROOT.rglob('*')):
    rel = path.relative_to(ROOT)
    if not path.is_file() or any(p in PRIVATE for p in rel.parts) or str(rel) == 'PUBLIC_MANIFEST.json':
        continue
    data = path.read_bytes()
    files.append({'path':str(rel), 'bytes':len(data), 'sha256':hashlib.sha256(data).hexdigest()})
manifest = {
    'review_root':'hyperbolic_arithmetic_review',
    'generated_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'candidate_head':'51fddd150e8da33f4cf17b1a642a0ffd3466bf5d',
    'verdict':'PASS_SCOPED_ORIGINAL_UNSOLVED_5_OF_5',
    'paths_relative_to':'this review root',
    'self_excluded':'PUBLIC_MANIFEST.json',
    'private_excluded':sorted(PRIVATE),
    'files':files,
}
(ROOT/'PUBLIC_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps({'status':'BUILT','public_files':len(files)},sort_keys=True))
