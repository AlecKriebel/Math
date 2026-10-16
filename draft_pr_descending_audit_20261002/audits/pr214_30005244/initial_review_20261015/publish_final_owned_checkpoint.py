"""Guarded85%/100% owned native main checkpoint with durable write receipt.

No local Git mutations. An uncertain write requires separate read-only recovery.
"""
from pathlib import Path
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor
import argparse
import base64
import hashlib
import json
import subprocess
import time

p = argparse.ArgumentParser()
p.add_argument('--stage', choices=['final-ready', 'complete'], required=True)
args = p.parse_args()
ROOT = Path('/Users/alec/Documents/Math')
D = Path(__file__).resolve().parent
R = D.parent / 'preprint'
PUB = D.parent / 'publication'
P = D.parent.parent.parent
percent = 85 if args.stage == 'final-ready' else 100
name = 'FINAL_READY_CHECKPOINT' if percent == 85 else 'COMPLETION_CHECKPOINT'
WRITE = D / (name + '_WRITE_RECEIPT.json')
RECEIPT = D / (name + '_PUBLICATION_RECEIPT.json')
assert not WRITE.exists() and not RECEIPT.exists(), 'Existing write: reconcile read-only'
clear = json.loads((R / 'FINAL_CLEARANCE.json').read_text())
assert clear['release_cleared'] and clear['fresh_manuscript_reviews'] >= 2 and not clear['unresolved_mandatory_findings']
for row in clear['submission_files']:
    raw = (R / row['path']).read_bytes()
    assert len(raw) == row['bytes'] and hashlib.sha256(raw).hexdigest() == row['sha256']
if percent == 100:
    merged = json.loads((PUB / 'PR_MERGED.json').read_text())
    assert merged['merged'] and merged['case_completion_percent'] == 100
GH = '/opt/homebrew/Cellar/gh/2.85.0/bin/gh'
B = 'repos/AlecKriebel/Math/'
T = D / 'private_transport' / datetime.now(timezone.utc).strftime(name + '_%Y%m%dT%H%M%S%fZ')
T.mkdir(parents=True, exist_ok=False)
seq = 0


def api(method, path, payload=None):
    global seq
    seq += 1
    args = [GH, 'api', '--method', method, B + path]
    if payload is not None:
        f = T / f'{seq:03d}-request.json'
        f.write_text(json.dumps(payload))
        args += ['--input', str(f)]
    r = subprocess.run(args, capture_output=True, timeout=60)
    (T / f'{seq:03d}-stdout.json').write_bytes(r.stdout)
    (T / f'{seq:03d}-stderr.txt').write_bytes(r.stderr)
    if r.returncode:
        raise RuntimeError(f'Native call{seq} failed: reconcile saved state before another mutation')
    return json.loads(r.stdout)


pr = api('GET', 'pulls/214')
if percent == 85:
    assert pr['state'] == 'open' and pr['draft'] and pr['head']['sha'] == '36d5ef15098163e74bf14c2e696f560ce592affd'
else:
    assert pr['merged'] and pr['head']['sha'] == merged['reviewed_head'] and pr['merge_commit_sha'] == merged['merge_commit']
paths = [p for p in D.iterdir() if p.is_file()]
for folder in ['submitted', 'root_reproduction', 'root_manuscript_review01_replay', 'root_manuscript_review02_replay']:
    paths += [p for p in (D / folder).rglob('*') if p.is_file() and not any(x.startswith('private') or x == '__pycache__' for x in p.parts)]
for F in [*D.glob('*adversary*'), *D.glob('priority_*'), D / 'root_priority_01', *R.glob('fresh_review_*')]:
    m = F / 'SAFE_AUTHORED_MANIFEST.json'
    if not m.exists():
        continue
    paths.append(m)
    obj = json.loads(m.read_text())
    rows = obj if isinstance(obj, list) else obj.get('safe_authored_files', obj.get('files'))
    for row in rows:
        p = Path(row.get('path', row.get('file')))
        p = p if p.is_absolute() else F / p
        assert p.resolve().is_relative_to(F.resolve())
        raw = p.read_bytes()
        assert len(raw) == row['bytes'] and hashlib.sha256(raw).hexdigest() == row['sha256']
        paths.append(p)
paths += [p for p in R.iterdir() if p.is_file()]
for folder in ['verification', 'pr_update', 'history']:
    paths += [p for p in (R / folder).rglob('*') if p.is_file() and '__pycache__' not in p.parts]
paths += [R / 'output/pdf/dipole_spectrum.pdf', R / 'output/dipole_spectrum_verification.zip']
paths += [p for p in PUB.iterdir() if p.is_file()]
paths += [p for p in (PUB / 'native_current_source').rglob('*') if p.is_file()]
paths += [p for p in (P / 'next_selection_after_pr218_20261015').iterdir() if p.is_file()]
paths += [P / 'RESEARCH_LOG.md', P / 'CURRENT_GOAL_SELECTION_20261013.json']
files = {}
for p in sorted(set(paths)):
    assert p.resolve().is_relative_to(P.resolve()) and not p.is_symlink()
    assert not any(x.startswith('private') or x == '__pycache__' for x in p.parts)
    files[p.relative_to(ROOT).as_posix()] = p.read_bytes()
if percent == 100:
    F = PUB / 'native_current_source'
    for p in F.rglob('*'):
        if p.is_file():
            files['unsolved_math_prioritization/attempts/30005244/' + p.relative_to(F).as_posix()] = p.read_bytes()
entries = []
pins = []
expected = {}
for path, raw in sorted(files.items()):
    sha = hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
    expected[sha] = raw
    try:
        entry = dict(path=path, mode='100644', type='blob', content=raw.decode('utf-8'))
    except UnicodeDecodeError:
        blob = api('POST', 'git/blobs', {'content': base64.b64encode(raw).decode(), 'encoding': 'base64'})['sha']
        assert blob == sha
        entry = dict(path=path, mode='100644', type='blob', sha=blob)
    entries.append(entry)
    pins.append(dict(path=path, bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest(), native_blob_sha1=sha))
parent = api('GET', 'git/ref/heads/main')['object']['sha']
base_tree = api('GET', 'git/commits/' + parent)['tree']['sha']
if percent == 100:
    def case_tree(root_tree):
        current = root_tree
        for component in ['unsolved_math_prioritization', 'attempts', '30005244']:
            data = api('GET', 'git/trees/' + current)
            assert not data['truncated']
            found = [x for x in data['tree'] if x['path'] == component]
            assert len(found) == 1 and found[0]['type'] == 'tree'
            current = found[0]['sha']
        return current
    merged_tree = api('GET', 'git/commits/' + merged['merge_commit'])['tree']['sha']
    assert case_tree(base_tree) == case_tree(merged_tree), 'Scientific subtree changed after verified merge: reconcile before updating administrative status'
tree = api('POST', 'git/trees', dict(base_tree=base_tree, tree=entries))['sha']
commit = api('POST', 'git/commits', dict(message=f'Checkpoint PR214 at{percent}%: ' + ('final credited preprint cleared; publication pending' if percent == 85 else 'verified DOI, tracker and native merge complete'), tree=tree, parents=[parent]))['sha']
assert api('PATCH', 'git/refs/heads/main', dict(sha=commit, force=False))['object']['sha'] == commit
write = dict(utc=datetime.now(timezone.utc).isoformat(), commit=commit, parent=parent, tree=tree,
             case_completion_percent=percent, owned_files=pins, byte_readback_status='pending', transport=str(T))
WRITE.write_text(json.dumps(write, indent=2) + '\n')
cache = {}


def listing(sha):
    if sha not in cache:
        data = api('GET', 'git/trees/' + sha)
        assert not data['truncated']
        cache[sha] = {x['path']: x for x in data['tree']}
    return cache[sha]


for row in pins:
    sha = tree
    for part in row['path'].split('/'):
        leaf = listing(sha)[part]
        sha = leaf['sha']
    assert leaf['type'] == 'blob' and sha == row['native_blob_sha1']


def check_blob(item):
    sha, raw = item
    time.sleep(.12)
    r = subprocess.run([GH, 'api', B + 'git/blobs/' + sha], capture_output=True, timeout=60)
    (T / ('blob-' + sha + '-stdout.json')).write_bytes(r.stdout)
    (T / ('blob-' + sha + '-stderr.txt')).write_bytes(r.stderr)
    assert r.returncode == 0
    assert base64.b64decode(json.loads(r.stdout)['content']) == raw
    return sha


with ThreadPoolExecutor(max_workers=3) as pool:
    verified = set(pool.map(check_blob, expected.items()))
assert verified == set(expected)
main = api('GET', 'git/ref/heads/main')['object']['sha']
if main != commit:
    assert api('GET', 'compare/' + commit + '...' + main)['status'] == 'ahead'
result = dict(write, main_readback=main, byte_readback_status='all owned paths verified against actual native tree and blob bytes',
              unique_actual_blob_byte_readbacks=len(verified), counts=[41, 18, 18, 0] if percent == 85 else [42, 19, 19, 0],
              full_goal_active_incomplete=True, local_Git_index_ref_mutations=0)
RECEIPT.write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({k: v for k, v in result.items() if k != 'owned_files'}, indent=2))
