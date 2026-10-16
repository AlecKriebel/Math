#!/usr/bin/env python3
"""Verify the read-only candidate's snapshot, nested manifests and status."""
from pathlib import Path
import hashlib, json, subprocess

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parent
SNAPSHOT = AUDIT/'snapshot'
CANDIDATE = SNAPSHOT/'problems/30006025_geometric_chapuy'
HEAD = '51fddd150e8da33f4cf17b1a642a0ffd3466bf5d'
REPO = HERE.parents[4]
counts = {}
def ck(value, scope):
    assert value, scope
    counts[scope] = counts.get(scope, 0)+1
def hashes(data):
    return hashlib.sha256(data).hexdigest(), hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
def validate_entry(base, entry):
    path = Path(entry['path'])
    ck(not path.is_absolute() and '..' not in path.parts, 'safe_manifest_path')
    data = (base/path).read_bytes()
    sha256, blob = hashes(data)
    size = entry.get('bytes', entry.get('size'))
    ck(len(data) == size, 'manifest_byte_length')
    if 'sha256' in entry:
        ck(sha256 == entry['sha256'], 'manifest_sha256')
    if 'git_blob_sha1' in entry:
        ck(blob == entry['git_blob_sha1'], 'manifest_git_blob')
    if 'git_blob_sha' in entry:
        ck(blob == entry['git_blob_sha'], 'manifest_git_blob')
    if 'sha' in entry:
        ck(blob == entry['sha'], 'manifest_git_blob')

manifest = json.loads((AUDIT/'snapshot_manifest.json').read_text())
ck(manifest['head'] == HEAD, 'snapshot_head')
target_count = 0
for entry in manifest['files']:
    validate_entry(SNAPSHOT, entry)
    data = (SNAPSHOT/entry['path']).read_bytes()
    remote_blob = subprocess.check_output(['git','show',f"{HEAD}:{entry['path']}"], cwd=REPO)
    ck(remote_blob == data, 'git_head_bytes')
    if entry['path'].startswith('problems/30006025_geometric_chapuy/'):
        target_count += 1

turn_entries = 0
for turn in range(1,6):
    mpath = CANDIDATE/f'TURN_{turn}_MANIFEST.json'
    m = json.loads(mpath.read_text())
    ck(m['problem_id'] == 30006025 and m['turn'] == turn, 'turn_identity')
    for entry in m['files']:
        validate_entry(CANDIDATE, entry)
        turn_entries += 1
    if turn > 1:
        prior = hashlib.sha256((CANDIDATE/f'TURN_{turn-1}_MANIFEST.json').read_bytes()).hexdigest()
        ck(prior == m['previous_manifest_sha256'], 'previous_manifest_binding')
    state = json.loads((CANDIDATE/f'TURN_{turn}_STATE.json').read_text())
    ck(state['author_turns_completed'] == turn and state['budget'] == 5, 'author_turn_count')
    ck(state['disposition'] in ('unresolved','unsolved'), 'unsolved_historical_disposition')

author = json.loads((CANDIDATE/'FINAL_AUTHOR_MANIFEST.json').read_text())
ck(author['author_turns'] == 5 and author['original_disposition'] == 'unsolved', 'final_author_status')
for entry in author['files']:
    validate_entry(CANDIDATE, entry)
scope = json.loads((CANDIDATE/'FINAL_PUBLIC_SCOPE.json').read_text())
ck(set(scope['files']) == {e['path'] for e in author['files']}|{'FINAL_AUTHOR_MANIFEST.json'}, 'final_public_scope')

review = CANDIDATE/'independent_review'
review_manifest = json.loads((review/'REVIEW_MANIFEST.json').read_text())
for entry in review_manifest['files']:
    validate_entry(review, entry)
remote = json.loads((review/'REMOTE_BINDING.json').read_text())
for entry in remote['files']:
    validate_entry(CANDIDATE, entry)
    data = subprocess.check_output(['git','show',f"{remote['head']}:problems/30006025_geometric_chapuy/{entry['path']}"], cwd=REPO)
    ck(data == (CANDIDATE/entry['path']).read_bytes(), 'historical_remote_head_bytes')

publication = json.loads((CANDIDATE/'PUBLICATION_MANIFEST.json').read_text())
for entry in publication['files']:
    validate_entry(CANDIDATE, entry)
actual = {str(p.relative_to(CANDIDATE)) for p in CANDIDATE.rglob('*') if p.is_file()}
ck(actual == {e['path'] for e in publication['files']}|{'PUBLICATION_MANIFEST.json'}, 'complete_public_packet_scope')
ck(publication['author_files'] == len(scope['files']), 'publication_author_count')
ck(publication['review_files'] == len(review_manifest['files'])+1, 'publication_review_count')
ck(publication['disposition'] == 'unsolved' and publication['turns'] == '5/5', 'publication_unsolved_status')

# All declared primary-source bindings have sound shape and agree on duplicates.
source_records = {}
for name in ['SOURCE_HASHES.json','SOURCE_ADDENDUM_TURN_2.json','SOURCE_ADDENDUM_TURN_3.json','SOURCE_ADDENDUM_TURN_4.json']:
    for entry in json.loads((CANDIDATE/name).read_text())['files']:
        ck(len(entry['sha256']) == 64 and all(c in '0123456789abcdef' for c in entry['sha256']), 'source_digest_shape')
        ck(entry['bytes'] > 0, 'source_size_positive')
        if entry['path'] in source_records:
            ck(source_records[entry['path']]['sha256'] == entry['sha256'] and source_records[entry['path']]['bytes'] == entry['bytes'], 'duplicate_source_binding')
        source_records[entry['path']] = entry

print(json.dumps({
    'status': 'PASS', 'head': HEAD, 'assertions': sum(counts.values()),
    'by_scope': counts, 'frozen_snapshot_files': len(manifest['files']),
    'candidate_target_files': target_count, 'historical_turn_entries': turn_entries,
    'final_author_entries': len(author['files']), 'author_scope_files': len(scope['files']),
    'review_entries': len(review_manifest['files']), 'historical_remote_blob_entries': len(remote['files']),
    'publication_entries': len(publication['files']), 'primary_source_unique_bindings': len(source_records),
    'limitation': 'Validates source binding declarations, not inaccessible historical private source bytes. Independently refetched primary PDFs are compared in SOURCE_BINDINGS.json. The current remote ref may advance; HEAD is locally resolved.'
}, indent=2, sort_keys=True))
