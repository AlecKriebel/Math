#!/usr/bin/env python3
"""Seal this directory's authored review records, or verify an existing seal.

No PDF, OCR, image, or external canonical input is read. `--verify` is read-only.
The integrity manifest deliberately does not hash itself.
"""
import hashlib
from datetime import datetime, timezone
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parent
NAMES=[
    '.gitignore','REPORT.md','VERDICT.json','RESEARCH_LOG.md','source_first.md',
    'source_custody.json','compared_inputs.json','check_goh_candidate.py',
    'exact_checks.json','portable_replay.json','seal_review.py',
]
MANIFEST=ROOT/'AUTHORED_MANIFEST.json'

def compute():
    return {name:{'sha256':hashlib.sha256((ROOT/name).read_bytes()).hexdigest(),
                  'bytes':(ROOT/name).stat().st_size} for name in sorted(NAMES)}

if sys.argv[1:]==['--verify']:
    old=json.loads(MANIFEST.read_text())
    current=compute()
    failures=[name for name in sorted(set(old['files'])|set(current))
              if old['files'].get(name)!=current.get(name)]
    print(json.dumps({'seal_verified':not failures,'checked_files':len(current),
                      'failures':failures},indent=2))
    sys.exit(bool(failures))
if sys.argv[1:]: raise SystemExit('Usage: seal_review.py [--verify]')
record={
    'schema':'authored-source-comparison-seal-v1',
    'sealed_utc':datetime.now(timezone.utc).isoformat(),
    'purpose':'Integrity of this bounded authored source review, not canonical-package acceptance.',
    'third_party_raw_material_included':False,
    'manifest_self_hash_omitted':True,
    'files':compute(),
}
MANIFEST.write_text(json.dumps(record,indent=2,sort_keys=True)+'\n')
print(json.dumps({'seal_written':True,'authored_files':len(record['files'])},indent=2))
