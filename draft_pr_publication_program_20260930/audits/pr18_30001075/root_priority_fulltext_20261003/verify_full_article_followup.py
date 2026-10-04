"""Check frozen source custody; this computation is not a mathematical review."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import stat
import sys

if sys.flags.optimize:
    raise SystemExit('optimized execution is not permitted')
audit = Path(__file__).resolve().parent.parent
family = audit / 'priority_mechanism_revisit_20261003/full_article_followup_20261003'
receipt = family / 'SOURCE_RECEIPT_FULL_ARTICLE.json'
data = json.loads(receipt.read_bytes())

def check(row):
    p = Path(row['path'])
    if not p.is_absolute():
        p = family / p
    s = p.lstat()
    if not stat.S_ISREG(s.st_mode):
        raise ValueError('ordinary regular file required: ' + str(p))
    raw = p.read_bytes()
    if len(raw) != row['bytes'] or hashlib.sha256(raw).hexdigest() != row['sha256'] or stat.S_IMODE(s.st_mode) != int(row['full_mode_07777'], 8):
        raise ValueError('pin mismatch: ' + str(p))

rows = data['public_handoff_members'] + data['private_inputs_excluded_from_publication']
for row in rows:
    check(row)
expected = {(family / row['path']).resolve() for row in rows} | {receipt.resolve()}
actual = {p.resolve() for p in family.rglob('*') if p.is_file()}
if actual != expected or stat.S_IMODE(receipt.stat().st_mode) != 0o444:
    raise ValueError('exact frozen family file census or receipt mode changed')
for row in data['full_directory_modes']:
    p = family / row['path']
    s = p.lstat()
    if not stat.S_ISDIR(s.st_mode) or stat.S_IMODE(s.st_mode) != int(row['full_mode_07777'], 8):
        raise ValueError('directory mode mismatch')
for name in ['source_pdf_external_in_place', 'historical_parent_snapshot_in_place', 'historical_report_in_place', 'historical_actual_control_in_place']:
    check(data[name])
candidate = audit / 'reviewed_candidate/CANDIDATE.md'
if hashlib.sha256(candidate.read_bytes()).hexdigest() != data['candidate_sha256']:
    raise ValueError('reviewed mathematical input changed')
for page in data['page_reading']:
    check(page['text'])
if len(data['page_reading']) != 30 or not all(page['personal_text_read'] for page in data['page_reading']):
    raise ValueError('incomplete reported read record')
print(json.dumps({
    'status': 'PASS_FROZEN_SOURCE_CUSTODY_ONLY', 'pid': os.getpid(),
    'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'receipt_sha256': hashlib.sha256(receipt.read_bytes()).hexdigest(),
    'files_checked': len(actual), 'public_payloads': len(data['public_handoff_members']),
    'private_payloads_not_redistributed': len(data['private_inputs_excluded_from_publication']),
    'reported_text_pages': len(data['page_reading']),
    'mathematical_or_priority_clearance_by_computation': False,
    'reported_personal_reading_is_attributed_to_family': True
}, indent=2))
