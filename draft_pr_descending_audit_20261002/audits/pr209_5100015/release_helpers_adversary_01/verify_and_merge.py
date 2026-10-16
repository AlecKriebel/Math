"""Read actual native PR209 science/provenance bytes before the authorized merge."""
import sys
if not __debug__ or sys.flags.optimize:
    raise RuntimeError('Release helpers refuse optimized Python before any action')
from release_binding import context,binding,unchanged,publication,tracker,acquire,exclusive_json,pr_identity,require,digest,durable_mkdir
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
PREFIX = 'unsolved_math_prioritization/attempts/5100015/'
assert not (PUB / 'PR_MERGED.json').exists(), 'Already merged; read-only reconciliation only'
require(not (PUB/'NATIVE_MERGE_REQUEST.json').exists(),'Prior merge intent exists: read-only reconciliation only')
prepared_raw=(PUB/'PR_PREPARED.json').read_bytes()
p=json.loads(prepared_raw)
prepared_receipt_sha256=hashlib.sha256(prepared_raw).hexdigest()
head = p['prepared_head']
_RELEASE_LOCK=acquire(PUB)
CTX=context(R)
clear=CTX['clear']
assert clear['release_cleared'] and clear['fresh_manuscript_reviews'] >= 2
assert clear['final_frozen_clean_reviews'] >= 1 and not clear['unresolved_mandatory_findings']
assert not clear['unresolved_optional_findings']
z=publication(R,PUB,CTX)
t=tracker(R,PUB,CTX,z)
require(p.get('release_binding')==binding(CTX),'Prepared PR belongs to another release')
require(p.get('publication_receipt_sha256')==digest(PUB/'ZENODO_VERIFIED_PUBLICATION.json') and p.get('tracker_receipt_sha256')==digest(PUB/'TRACKER_VERIFIED_APPEND.json'),'Prepared native receipts changed')
assert z['submitted'] and z['metadata_and_files_verified']
assert t['verified'] and t['doi_url'] == z['doi_url']
T = PUB / 'private_transport' / datetime.now(timezone.utc).strftime('native_merge_%Y%m%dT%H%M%S%fZ')
durable_mkdir(T,exist_ok=False)
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


pr = api('GET', 'pulls/209')
pr_identity(pr,head)
assert not pr['merged']
actual_commit=api('GET','git/commits/'+head)
require(actual_commit['tree']['sha']==p['tree'] and [x['sha'] for x in actual_commit['parents']]==[clear['original_native_head'],p['main_parent']],'Actual commit tree/parents disagree with prepared receipt')
cache = {}


def tree_entries(sha):
    if sha not in cache:
        result = api('GET', 'git/trees/' + sha)
        assert not result['truncated']
        cache[sha] = {x['path']: x for x in result['tree']}
    return cache[sha]


def native_blob(path):
    sha = actual_commit['tree']['sha']
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
target = [x for x in raw_queue.decode().splitlines() if '5100015 / AMR-050-0015' in x]
assert target == [p['target_queue_row']]
assert target[0].split('|')[8].strip() == 'claimed_solved' and z['doi_url'] in target[0]
qpin = next(x for x in p['included_owned_pins'] if x['path'] == 'unsolved_math_prioritization/QUEUE.md')
assert len(raw_queue) == qpin['bytes'] and hashlib.sha256(raw_queue).hexdigest() == qpin['sha256']
delta=api('GET','compare/'+p['main_parent']+'...'+head)
assert len(delta['files'])<300
assert {x['filename'] for x in delta['files']} <= {x['path'] for x in p['included_owned_pins']}
assert all(x['status']!='removed' for x in delta['files'])
receipt = {'utc': datetime.now(timezone.utc).isoformat(), 'status': 'PASS', 'head': head,
           'actual_current_source_original_archive_and_submission_readbacks': readbacks,
           'all_included_owned_native_tree_identities': identities,
           'exact_queue_row': target[0], 'metadata_and_files_verified': True,
           'tracker_verified': True, 'release_status_only_native_delta': True}
(PUB / 'NATIVE_SCIENTIFIC_READBACK.json').write_text(json.dumps(receipt, indent=2) + '\n')
# Native readbacks can be lengthy. Refresh the actual PR and every accepted
# local release/receipt binding immediately before the ready transition.
pr=api('GET','pulls/209')
pr_identity(pr,head)
require(not pr['merged'],'PR merged during native readback: reconcile read-only')
unchanged(R,CTX)
require(publication(R,PUB,CTX)==z,'Accepted publication receipt changed')
require(tracker(R,PUB,CTX,z)==t,'Accepted tracker receipt changed')
require(digest(PUB/'PR_PREPARED.json')==prepared_receipt_sha256,'Accepted prepared receipt changed')
if pr['draft']:
    exclusive_json(PUB/'NATIVE_READY_ATTEMPT.json',dict(utc=datetime.now(timezone.utc).isoformat(),head=head,release_binding=binding(CTX)))
    result = api('POST', 'graphql', {'query': 'mutation($id: ID!) { markPullRequestReadyForReview(input:{pullRequestId:$id}) { pullRequest { id isDraft } } }',
                                    'variables': {'id': pr['node_id']}}, graphql=True)
    assert not result.get('errors') and result['data']['markPullRequestReadyForReview']['pullRequest']['isDraft'] is False
for attempt in range(8):
    pr = api('GET', 'pulls/209')
    pr_identity(pr,head,False)
    assert not pr['merged']
    if pr['mergeable'] is not None:
        break
    time.sleep(3)
assert pr['mergeable'] is True, 'Conflict or unknown native mergeability; resolve without forcing main'
request = {'sha': head, 'merge_method': 'merge',
           'commit_title': 'Merge PR #209: audited outer center-pedal area product and published preprint'}
unchanged(R,CTX)
require(publication(R,PUB,CTX)==z and tracker(R,PUB,CTX,z)==t,'Accepted release receipts changed before merge')
require(digest(PUB/'PR_PREPARED.json')==prepared_receipt_sha256,'Prepared receipt changed before merge')
exclusive_json(PUB/'NATIVE_MERGE_REQUEST.json',dict(request,release_binding=binding(CTX)))
result = api('PUT', 'pulls/209/merge', request)
assert result['merged'] is True
pr = api('GET', 'pulls/209')
assert pr['merged'] and pr['state'] == 'closed' and pr['merge_commit_sha'] == result['sha']
pr_identity(pr,head,False,state='closed')
receipt = {'utc': datetime.now(timezone.utc).isoformat(), 'PR': 209, 'url': pr['html_url'],
           'merged': True, 'merge_commit': result['sha'], 'reviewed_head': head,
           'doi_url': z['doi_url'], 'tracker_range': t['updated_range'],
           'case_completion_percent': 100, 'program_counts': [45, 22, 22, 0],
           'full_goal_active_incomplete': True,'release_binding':binding(CTX)}
(PUB / 'PR_MERGED.json').write_text(json.dumps(receipt, indent=2) + '\n')
print(json.dumps(receipt, indent=2))
