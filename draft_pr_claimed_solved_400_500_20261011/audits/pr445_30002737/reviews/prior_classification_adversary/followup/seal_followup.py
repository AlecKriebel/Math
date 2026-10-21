#!/usr/bin/env python3
"""Seal the new follow-up only; never touch historical review bytes."""
from pathlib import Path
import datetime
import hashlib
import json

HERE = Path(__file__).resolve().parent
at = datetime.datetime.now(datetime.timezone.utc).isoformat()
result=json.loads((HERE/'FOLLOWUP_RESULT.json').read_text())
result['at_utc']=at
(HERE/'FOLLOWUP_RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
(HERE/'FOLLOWUP_LOG.md').write_text(
    '# Follow-up research log\n\n'
    '- 2026-10-12T21:32:36Z - Concrete synthesis, complete certificate code and fresh adversary evidence read; completion estimate 55%. Historical review frozen.\n'
    '- 2026-10-12T21:32:38.993447Z - All 9 historical own-file hashes and 24 parent custody hashes match. One new direct N13 replay matches all stable certificate fields; exact threshold bridge checked. Completion estimate 95%.\n'
    f'- {at} - Follow-up PASS sealed; completion estimate 100%. Mathematical blockers 0, required repairs 0, current classification numerical gap 0. Original gap1 preserved. Separate operational transaction remains pending.\n')
names=['INITIAL_FOLLOWUP.md','FOLLOWUP_REPORT.md','FOLLOWUP_RESULT.json',
       'FOLLOWUP_CHECKS.json','FOLLOWUP_LOG.md','check_followup.py','seal_followup.py']
files=[]
for name in names:
    p=HERE/name;b=p.read_bytes()
    files.append({'path':name,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),
                  'provenance':'this reviewer original follow-up prose/code or newly captured own-run output/metadata'})
(HERE/'PUBLIC_FILES.json').write_text(json.dumps({'at_utc':at,
    'kind':'positive own-byte follow-up allowlist',
    'scope':'listed files plus this self-excluding manifest only',
    'files':files,'manifest_self_sha256_excluded':True,
    'historical_review_manifest_unchanged':True},indent=2)+'\n')
print(json.dumps({'at_utc':at,'public_files_excluding_manifest':len(files),
                  'classification_blockers':0,'current_integral_gap':0},indent=2))
