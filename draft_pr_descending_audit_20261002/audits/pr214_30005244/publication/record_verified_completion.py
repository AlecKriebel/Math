"""Local administrative completion only after verified native merge; no providers."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json

PUB = Path(__file__).resolve().parent
D = PUB.parent / 'initial_review_20261015'
R = PUB.parent / 'preprint'
P = PUB.parent.parent.parent
F = PUB / 'native_current_source'
m = json.loads((PUB / 'PR_MERGED.json').read_text())
z = json.loads((PUB / 'ZENODO_VERIFIED_PUBLICATION.json').read_text())
t = json.loads((PUB / 'TRACKER_VERIFIED_APPEND.json').read_text())
assert m['merged'] and m['doi_url'] == z['doi_url'] == t['doi_url']
assert z['submitted'] and z['metadata_and_files_verified'] and t['verified']
assert not (F / 'MERGE_RECEIPT.json').exists(), 'Completion already recorded locally'
now = datetime.now(timezone.utc).isoformat()
prepared = json.loads((PUB / 'PR_PREPARED.json').read_text())
queue_pin = next(row for row in prepared['included_owned_pins'] if row['path'] == 'unsolved_math_prioritization/QUEUE.md')
(F / 'MERGE_RECEIPT.json').write_text(json.dumps(m, indent=2) + '\n')
p = F / 'CANDIDATE.md'
old = 'native merge remains pending exact readback.'
text = p.read_text()
assert text.count(old) == 1
p.write_text(text.replace(old, 'native merge was subsequently verified at ' + m['merge_commit'] + '; see MERGE_RECEIPT.json.'))
p = F / 'FINAL_DISPOSITION.md'
text = p.read_text()
assert text.count('Native merge is pending exact scientific readback.') == 1
p.write_text(text.replace('Native merge is pending exact scientific readback.', 'Native merge is verified at ' + m['merge_commit'] + '; see MERGE_RECEIPT.json.'))
with (F / 'README.md').open('a') as f:
    f.write('\nNative merge verified: ' + m['merge_commit'] + '. MERGE_RECEIPT.json records the accepted head and completed publication/tracker/merge sequence.\n')
with (F / 'RESEARCH_LOG.md').open('a') as f:
    f.write(now + ' — case100%: exact native scientific readback and merge verified at ' + m['merge_commit'] + '. DOI and tracker readbacks are complete; entire descending goal remains active.\n')
for name in ['ACCEPTANCE.json', 'FINAL_ACCEPTANCE.json']:
    p = F / name
    o = json.loads(p.read_text())
    o.update(native_merge_verified=m, case_completion_percent=100)
    p.write_text(json.dumps(o, indent=2) + '\n')
p = F / 'CURRENT_SOURCE_MANIFEST.json'
o = json.loads(p.read_text())
o.update(utc=now, status='claimed_solved_audited_published_merged')
o['current_files'] = []
for f in sorted(F.iterdir()):
    if f.is_file() and f.name != p.name:
        raw = f.read_bytes()
        o['current_files'].append(dict(path=f.name, bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest()))
p.write_text(json.dumps(o, indent=2) + '\n')
for row in json.loads((F / 'ORIGINAL_SUBMISSION_MANIFEST.json').read_text())['files']:
    raw = (F / row['archive_path']).read_bytes()
    assert len(raw) == row['bytes'] and hashlib.sha256(raw).hexdigest() == row['sha256']
p = D / 'CURRENT_AUDIT_STATE.json'
o = json.loads(p.read_text())
o.update(utc=now, stage='verified_publication_tracker_native_merge_complete', completion_percent=100,
         original_head='36d5ef15098163e74bf14c2e696f560ce592affd', head=m['reviewed_head'], Queue_blob=queue_pin['git_blob_sha1'],
         DOI=z['doi'], tracker_range=t['updated_range'], merged_head=m['reviewed_head'],
         merge_commit=m['merge_commit'], counts=[42, 19, 19, 0], preprint_upload_cleared=True)
p.write_text(json.dumps(o, indent=2) + '\n')
p = P / 'CURRENT_GOAL_SELECTION_20261013.json'
o = json.loads(p.read_text())
o.update(utc=now, current_stage='PR214_verified_publication_tracker_native_merge_complete',
         case_completion_percent=100, current_PR_head=m['reviewed_head'], current_DOI=z['doi'],
         current_tracker_range=t['updated_range'], last_native_merge=m['merge_commit'],
         Queue_blob=queue_pin['git_blob_sha1'],
         previous_completed_PR=214, previous_completed_DOI=z['doi'],
         program_counts=[42, 19, 19, 0], previous_completion_counts=[42, 19, 19, 0],
         preprint_upload_cleared=True, overall_goal_active_incomplete=True)
p.write_text(json.dumps(o, indent=2) + '\n')
for p in [P / 'RESEARCH_LOG.md', D / 'RESEARCH_LOG.md']:
    with p.open('a') as f:
        f.write(f'\n## {now} — PR214 checkpoint100%\nQualified credited DDA note and source/verification package published at ' + z['doi_url'] + '. Exact metadata/files verified; tracker appended once with all four cells read back at ' + t['updated_range'] + '. After exact native scientific readback, PR214 merged at ' + m['merge_commit'] + ' from accepted head ' + m['reviewed_head'] + '. Two new sequential manuscript reviews completed after global documentary/precision fixes; bounded priority/source-access limits remain visible. All31 original artifacts and first-review inputs preserved. Counts42/19/19/0. Full descending goal active/incomplete; native100% main checkpoint and next eligible lower selection remain.\n')
print(json.dumps({'case_completion_percent': 100, 'DOI': z['doi'], 'tracker_range': t['updated_range'], 'merge_commit': m['merge_commit'], 'goal_active_incomplete': True}, indent=2))
