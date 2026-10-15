"""READ ONLY recovery of the completed75% main write. Never pushes a ref."""
from pathlib import Path
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor
import base64
import hashlib
import json
import subprocess
import time

ROOT = Path('/Users/alec/Documents/Math')
D = Path(__file__).resolve().parent
T = D / 'private_transport/checkpoint_20261015T090304709703Z'
W = T / 'read_only_reconciliation'
W.mkdir(exist_ok=True)
GH = '/opt/homebrew/Cellar/gh/2.85.0/bin/gh'
B = 'repos/AlecKriebel/Math/'
COMMIT = '57e426d66b2d953422b92235a636139a929e91bc'
PARENT = 'cb2504c65d87c14597fbd33cff98ad5f1d6ff0ee'
request = json.loads((T / '09-request.json').read_text())


def get(path, label):
    result = subprocess.run([GH, 'api', B + path], capture_output=True, timeout=60)
    (W / (label + '-stdout.json')).write_bytes(result.stdout)
    (W / (label + '-stderr.txt')).write_bytes(result.stderr)
    assert result.returncode == 0, 'Read-only request failed; retain outcome and reconcile'
    return json.loads(result.stdout)


commit = get('git/commits/' + COMMIT, 'commit')
assert [x['sha'] for x in commit['parents']] == [PARENT]
assert commit['tree']['sha'] == json.loads((T / '09-stdout.json').read_text())['sha']
assert json.loads((T / '11-stdout.json').read_text())['object']['sha'] == COMMIT
cache = {}


def listing(sha):
    if sha not in cache:
        data = get('git/trees/' + sha, 'tree-' + sha)
        assert not data['truncated']
        cache[sha] = {x['path']: x for x in data['tree']}
    return cache[sha]


expected = {}
pins = []
for entry in request['tree']:
    path = entry['path']
    raw = (ROOT / path).read_bytes()
    if 'content' in entry:
        assert raw == entry['content'].encode(), path
    sha = hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
    if 'sha' in entry:
        assert sha == entry['sha'], path
    tree = commit['tree']['sha']
    for component in path.split('/'):
        row = listing(tree)[component]
        tree = row['sha']
    assert row['type'] == 'blob' and tree == sha, path
    if sha in expected:
        assert expected[sha] == raw
    expected[sha] = raw
    pins.append({'path': path, 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest(), 'native_blob_sha1': sha})


def check_blob(item):
    sha, raw = item
    time.sleep(0.12)
    data = get('git/blobs/' + sha, 'blob-' + sha)
    actual = base64.b64decode(data['content'])
    assert actual == raw and data['sha'] == sha
    return sha


with ThreadPoolExecutor(max_workers=3) as pool:
    verified = set(pool.map(check_blob, expected.items()))
assert verified == set(expected)
main = get('git/ref/heads/main', 'main')['object']['sha']
if main != COMMIT:
    assert get('compare/' + COMMIT + '...' + main, 'ancestry')['status'] == 'ahead'
pr = get('pulls/214', 'PR214')
assert pr['state'] == 'open' and pr['draft'] and pr['head']['sha'] == '36d5ef15098163e74bf14c2e696f560ce592affd'
receipt = {'utc': datetime.now(timezone.utc).isoformat(), 'commit': COMMIT, 'parent': PARENT,
           'main_readback': main, 'case_completion_percent': 75, 'owned_files': pins,
           'actual_native_byte_readbacks': [dict(row, byte_identical=True, method='Actual native tree identity plus actual Git blob bytes; identical blobs fetched once') for row in pins],
           'unique_actual_blob_byte_readbacks': len(verified), 'all_original_owned_paths_verified': True,
           'original_PR_head_unchanged': pr['head']['sha'], 'full_goal_active_incomplete': True,
           'counts': [41, 18, 18, 0], 'local_Git_or_index_mutations': 0,
           'recovery': 'Initial push completed; one original content read-back request failed. This recovery performed only GET requests and local receipt writes. No mutation repeated.',
           'transport_receipts': str(T)}
(D / 'MANUSCRIPT_REPAIR_CHECKPOINT_PUBLICATION_RECEIPT.json').write_text(json.dumps(receipt, indent=2) + '\n')
print(json.dumps({k: v for k, v in receipt.items() if k not in ['owned_files', 'actual_native_byte_readbacks']}, indent=2))
