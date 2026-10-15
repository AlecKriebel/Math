"""Read actual native PR214 science/provenance bytes before the authorized merge."""
from pathlib import Path
from datetime import datetime, timezone
import base64
import hashlib
import json
import subprocess
import time

R = Path(__file__).resolve().parent.parent / 'preprint'
PUB = R.parent / 'publication'
GH = '/opt/homebrew/Cellar/gh/2.85.0/bin/gh'
B = 'repos/AlecKriebel/Math/'
PREFIX = 'unsolved_math_prioritization/attempts/30005244/'
assert not (PUB / 'PR_MERGED.json').exists(), 'Already merged; read-only reconciliation only'
p = json.loads((PUB / 'PR_PREPARED.json').read_text())
head = p['prepared_head']
clear = json.loads((R / 'FINAL_CLEARANCE.json').read_text())
assert clear['release_cleared'] and clear['fresh_manuscript_reviews'] >= 2
assert clear['final_frozen_clean_reviews'] >= 1 and not clear['unresolved_mandatory_findings']
z = json.loads((PUB / 'ZENODO_VERIFIED_PUBLICATION.json').read_text())
t = json.loads((PUB / 'TRACKER_VERIFIED_APPEND.json').read_text())
assert z['submitted'] and z['metadata_and_files_verified']
assert t['verified'] and t['doi_url'] == z['doi_url']
T = PUB / 'private_transport' / datetime.now(timezone.utc).strftime('native_merge_%Y%m%dT%H%M%S%fZ')
T.mkdir(parents=True, exist_ok=False)
seq = 0


def api(method, path, payload=None, graphql=False):
    global seq
    seq += 1
    args = [GH, 'api', '--method', method, path if graphql else B + path]
    if payload is not None:
        f = T / f'{seq:03d}-request.json'
        f.write_text(json.dumps(payload))
        args += ['--input', str(f)]
    r = subprocess.run(args, capture_output=True, timeout=60)
    (T / f'{seq:03d}-stdout.json').write_bytes(r.stdout)
    (T / f'{seq:03d}-stderr.txt').write_bytes(r.stderr)
    if r.returncode:
        raise RuntimeError(f'Native call{seq} failed; reconcile before another mutation')
    return json.loads(r.stdout)


pr = api('GET', 'pulls/214')
assert pr['state'] == 'open' and not pr['merged'] and pr['head']['sha'] == head
cache = {}


def tree_entries(sha):
    if sha not in cache:
        result = api('GET', 'git/trees/' + sha)
        assert not result['truncated']
        cache[sha] = {x['path']: x for x in result['tree']}
    return cache[sha]


def native_blob(path):
    sha = p['tree']
    parts = path.split('/')
    for i, part in enumerate(parts):
        row = tree_entries(sha)[part]
        if i < len(parts) - 1:
            assert row['type'] == 'tree'
        else:
            assert row['type'] == 'blob'
        sha = row['sha']
    return sha


identities = []
for row in p['included_owned_pins']:
    sha = native_blob(row['path'])
    assert sha == row['git_blob_sha1']
    identities.append({'path': row['path'], 'native_blob_sha1': sha,
                       'bytes': row['bytes'], 'sha256': row['sha256'],
                       'native_tree_identity_verified': True})
readbacks = []


def match(local, path):
    raw = local.read_bytes()
    item = api('GET', 'contents/' + path + '?ref=' + head)
    if item.get('encoding') == 'base64':
        remote = base64.b64decode(item['content'])
    else:
        remote = base64.b64decode(api('GET', 'git/blobs/' + item['sha'])['content'])
    assert remote == raw
    readbacks.append({'native_path': path, 'native_blob': item['sha'], 'bytes': len(raw),
                      'sha256': hashlib.sha256(raw).hexdigest(), 'byte_identical': True})


F = PUB / 'native_current_source'
for local in sorted(F.rglob('*')):
    if local.is_file():
        match(local, PREFIX + local.relative_to(F).as_posix())
for row in clear['submission_files']:
    local = R / row['path']
    raw = local.read_bytes()
    assert len(raw) == row['bytes'] and hashlib.sha256(raw).hexdigest() == row['sha256']
    match(local, local.relative_to(Path('/Users/alec/Documents/Math')).as_posix())
q = api('GET', 'contents/unsolved_math_prioritization/QUEUE.md?ref=' + head)
raw_queue = base64.b64decode(q['content'])
target = [x for x in raw_queue.decode().splitlines() if '30005244 / OWR-11101924-008' in x]
assert target == [p['target_queue_row']]
assert target[0].split('|')[8].strip() == 'claimed_solved' and z['doi_url'] in target[0]
qpin = next(x for x in p['included_owned_pins'] if x['path'] == 'unsolved_math_prioritization/QUEUE.md')
assert len(raw_queue) == qpin['bytes'] and hashlib.sha256(raw_queue).hexdigest() == qpin['sha256']
receipt = {'utc': datetime.now(timezone.utc).isoformat(), 'status': 'PASS', 'head': head,
           'actual_current_source_original_archive_and_submission_readbacks': readbacks,
           'all_included_owned_native_tree_identities': identities,
           'exact_queue_row': target[0], 'metadata_and_files_verified': True,
           'tracker_verified': True, 'release_status_only_native_delta': True}
(PUB / 'NATIVE_SCIENTIFIC_READBACK.json').write_text(json.dumps(receipt, indent=2) + '\n')
if pr['draft']:
    result = api('POST', 'graphql', {'query': 'mutation($id: ID!) { markPullRequestReadyForReview(input:{pullRequestId:$id}) { pullRequest { id isDraft } } }',
                                    'variables': {'id': pr['node_id']}}, graphql=True)
    assert not result.get('errors') and result['data']['markPullRequestReadyForReview']['pullRequest']['isDraft'] is False
for attempt in range(8):
    pr = api('GET', 'pulls/214')
    assert pr['state'] == 'open' and not pr['merged'] and not pr['draft'] and pr['head']['sha'] == head
    if pr['mergeable'] is not None:
        break
    time.sleep(3)
assert pr['mergeable'] is True, 'Conflict or unknown native mergeability; resolve without forcing main'
request = {'sha': head, 'merge_method': 'merge',
           'commit_title': 'Merge PR #214: audited geometric DDA spectral theorem and published preprint'}
(PUB / 'NATIVE_MERGE_REQUEST.json').write_text(json.dumps(request, indent=2) + '\n')
result = api('PUT', 'pulls/214/merge', request)
assert result['merged'] is True
pr = api('GET', 'pulls/214')
assert pr['merged'] and pr['state'] == 'closed' and pr['merge_commit_sha'] == result['sha']
assert pr['head']['sha'] == head
receipt = {'utc': datetime.now(timezone.utc).isoformat(), 'PR': 214, 'url': pr['html_url'],
           'merged': True, 'merge_commit': result['sha'], 'reviewed_head': head,
           'doi_url': z['doi_url'], 'tracker_range': t['updated_range'],
           'case_completion_percent': 100, 'program_counts': [42, 19, 19, 0],
           'full_goal_active_incomplete': True}
(PUB / 'PR_MERGED.json').write_text(json.dumps(receipt, indent=2) + '\n')
print(json.dumps(receipt, indent=2))
