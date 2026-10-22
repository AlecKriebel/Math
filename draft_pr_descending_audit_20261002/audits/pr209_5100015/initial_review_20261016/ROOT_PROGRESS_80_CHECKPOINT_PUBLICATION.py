"""Publish only PR209's reviewed readiness checkpoint; no scientific PR release.

Immutable Git objects permit unchanged-blob inheritance and pre-ref rebasing.
Every actual main-ref write is nonforce, durably intended, and attempted once.
The publication/append/native-PR helpers are never executed by this program.
"""
from pathlib import Path
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor
import base64
import gzip
import hashlib
import json
import os
import subprocess
import sys
import threading

D = Path(__file__).resolve().parent
C, ROOT = D.parent, D.parents[3]
P, PUB, B = D.parents[2], C / 'publication', C / 'preprint'
GH = '/opt/homebrew/Cellar/gh/2.85.0/bin/gh'
BASE = 'repos/AlecKriebel/Math/'
OUT = D / 'PROGRESS_80_CHECKPOINT_PUBLICATION_RECEIPT.json'
if OUT.exists():
    raise RuntimeError('A completed checkpoint already exists; never repeat publication')
if os.statvfs(D).f_bavail * os.statvfs(D).f_frsize < 192 * 1024 * 1024:
    raise RuntimeError('Insufficient durable space even for incremental checkpoint journals')
T = D / 'private_transport' / datetime.now(timezone.utc).strftime('progress80_%Y%m%dT%H%M%S%fZ')
T.mkdir()
SEQ = 0
LOCK = threading.Lock()


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def blob(raw):
    return hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()


def write(path, raw):
    with Path(path).open('xb') as handle:
        handle.write(raw)
        handle.flush()
        os.fsync(handle.fileno())
    require(Path(path).read_bytes() == raw, 'Durable journal readback differs')


def record(path, value):
    write(path, (json.dumps(value, indent=2) + '\n').encode())


def packed(path, raw):
    body = gzip.compress(raw, mtime=0)
    write(path, body)
    require(gzip.decompress(Path(path).read_bytes()) == raw, 'Lossless transport journal differs')


def api(method, path, payload=None, source=None):
    global SEQ
    for attempt in range(3 if method == 'GET' else 1):
        with LOCK:
            SEQ += 1
            number = SEQ
        prefix = T / f'{number:04d}'
        args = [GH, 'api', '--method', method, BASE + path]
        raw = None
        if payload is not None:
            raw = json.dumps(payload).encode()
            if source is None:
                packed(str(prefix) + '-request.json.gz', raw)
            else:
                original = Path(source).read_bytes()
                start, end = b'{"content": "', b'", "encoding": "base64"}'
                require(raw == start + base64.b64encode(original) + end,
                        'Binary request cannot be reconstructed from immutable source')
                recipe = dict(codec='exact-base64-source-with-json-envelope',
                    source=Path(source).relative_to(ROOT).as_posix(),
                    source_bytes=len(original), source_sha256=sha(original),
                    prefix=start.decode(), suffix=end.decode(),
                    request_bytes=len(raw), request_sha256=sha(raw))
                recipe_path = Path(str(prefix) + '-request.RECONSTRUCTION.json')
                record(recipe_path, recipe)
                saved = json.loads(recipe_path.read_bytes())
                source_bytes = (ROOT / saved['source']).read_bytes()
                reconstructed = saved['prefix'].encode() + base64.b64encode(source_bytes) + saved['suffix'].encode()
                require(len(source_bytes) == saved['source_bytes'] and sha(source_bytes) == saved['source_sha256']
                        and reconstructed == raw and sha(reconstructed) == saved['request_sha256'],
                        'Durable exact request recipe is invalid')
            args += ['--input', '-']
        try:
            run = subprocess.run(args, input=raw, capture_output=True, text=False, timeout=90)
        except subprocess.TimeoutExpired as error:
            packed(str(prefix) + '-stdout.partial.gz', error.stdout or b'')
            packed(str(prefix) + '-stderr.partial.gz', error.stderr or b'')
            record(str(prefix) + '-OUTCOME_UNKNOWN.json', dict(method=method, path=path,
                type=type(error).__name__, timeout=error.timeout,
                no_write_retry=True))
            if method == 'GET' and attempt < 2:
                continue
            raise
        packed(str(prefix) + '-stdout.json.gz', run.stdout)
        packed(str(prefix) + '-stderr.bin.gz', run.stderr)
        record(str(prefix) + '-CALL.json', dict(method=method, path=path,
            actual_exit=run.returncode, attempt=attempt, write_retry=False))
        if run.returncode:
            if method == 'GET' and attempt < 2:
                continue
            raise RuntimeError('Retained native call failed; no native write retry')
        return json.loads(run.stdout)
    raise RuntimeError('Read-only attempts exhausted')


def claim():
    pr = api('GET', 'pulls/209')
    require(pr['state'] == 'open' and pr['draft'] is True and
            pr['head']['sha'] == 'fd09a95b479f376234835a4494693bb1316c85ec',
            'Original scientific PR changed; stop checkpoint publication')
    intake = json.loads((D / 'INTAKE.json').read_bytes())
    queue = api('GET', 'contents/unsolved_math_prioritization/QUEUE.md?ref=' + pr['head']['sha'])
    body = base64.b64decode(queue['content'])
    require(queue['sha'] == intake['Queue_blob'] and sha(body) == intake['Queue_sha256'] and
            intake['queue_row'] in body.decode().splitlines() and
            intake['queue_row'].split('|')[8].strip() == 'claimed_solved',
            'Exact original eligible QUEUE row changed')


CACHE = {}


def rows(tree):
    if tree not in CACHE:
        response = api('GET', 'git/trees/' + tree)
        require(response.get('truncated') is False, 'Truncated native tree')
        CACHE[tree] = {x['path']: {k: x[k] for k in ('mode', 'type', 'sha')} for x in response['tree']}
        require(len(CACHE[tree]) == len(response['tree']), 'Duplicate native tree paths')
    return CACHE[tree]


def at(tree, path):
    pieces = path.split('/')
    for index, name in enumerate(pieces):
        item = rows(tree).get(name)
        if item is None:
            return None
        if index + 1 < len(pieces) and item['type'] != 'tree':
            raise RuntimeError('Native parent path is not a tree')
        tree = item['sha']
    return item


def difference(left, right, prefix=''):
    if left == right:
        return []
    a, b = rows(left) if left else {}, rows(right) if right else {}
    result = []
    for name in sorted(set(a) | set(b)):
        x, y = a.get(name), b.get(name)
        if x == y:
            continue
        if (x is None or x['type'] == 'tree') and (y is None or y['type'] == 'tree'):
            result += difference(x['sha'] if x else None, y['sha'] if y else None, prefix + name + '/')
        else:
            result.append(dict(path=prefix + name, old=x, new=y))
    return result


sys.path.insert(0, str(PUB))
import release_binding as rb
ctx = rb.context(B)
exports = rb.public_exports(B, PUB, ctx)
require(len(exports) == 1593, 'Unexpected cleared public packet')
expected = {(C / name).relative_to(ROOT).as_posix(): raw for name, raw in exports.items()}
extras = [B / 'FINAL_CLEARANCE.json', PUB / 'PUBLIC_EXPORT_MANIFEST.json',
    D / 'ROOT_FINAL_PUBLICATION_READINESS.json', D / 'CURRENT_AUDIT_STATE.json',
    P / 'CURRENT_GOAL_SELECTION_20261013.json', P / 'RESEARCH_LOG.md',
    D / 'RESEARCH_LOG.md', Path(__file__)]
for path in extras:
    expected[path.relative_to(ROOT).as_posix()] = path.read_bytes()
case_prefix = C.relative_to(ROOT).as_posix() + '/'
outside = {path.relative_to(ROOT).as_posix() for path in extras if not path.is_relative_to(C)}
require(all(path.startswith(case_prefix) or path in outside for path in expected), 'Foreign checkpoint scope')
require(all(not any(part.startswith(('private', 'secret', 'credential')) for part in path.split('/'))
            for path in expected), 'Private checkpoint path')
frozen_pins = [dict(path=path, bytes=len(raw), sha256=sha(raw), git_blob_sha1=blob(raw))
               for path, raw in sorted(expected.items())]
record(T / 'FROZEN_CHECKPOINT_INPUTS.json', dict(utc=datetime.now(timezone.utc).isoformat(),
    case_completion_percent=80, files=frozen_pins, exact_cleared_exports=1593,
    publication_tracker_scientific_PR_actions=False, local_Git_index_ref_mutations=0))
prior = json.loads((D / 'PROGRESS_65_REVIEW02_CHECKPOINT_RECEIPT.json').read_bytes())
require(prior['commit'] == 'b109028ff024f7b4df8cbc684c4773a4dd300ae0', 'Unexpected prior checkpoint')
claim()
anchor = api('GET', 'git/commits/' + prior['commit'])
require([x['sha'] for x in anchor['parents']] == [prior['parent']], 'Prior checkpoint ancestry differs')
oldpins = {x['path']: x for x in prior['owned_files']}
oldreads = {x['path']: x for x in prior['actual_native_byte_readbacks']}
known_blobs = set(x['git_blob_sha1'] for x in prior['owned_files'])
current = api('GET', 'git/ref/heads/main')['object']['sha']
main = api('GET', 'git/commits/' + current)
entries, changed = [], []
for path, raw in sorted(expected.items()):
    wanted = dict(mode='100644', type='blob', sha=blob(raw))
    old, fresh = at(anchor['tree']['sha'], path), at(main['tree']['sha'], path)
    require(fresh in (old, wanted), 'Concurrent owned-path change: ' + path)
    if fresh == wanted:
        continue
    changed.append(path)
    try:
        text = raw.decode('utf8')
    except UnicodeDecodeError:
        if wanted['sha'] not in known_blobs:
            result = api('POST', 'git/blobs', dict(content=base64.b64encode(raw).decode(), encoding='base64'), source=ROOT/path)
            require(result['sha'] == wanted['sha'], 'Uploaded native blob identity differs')
            known_blobs.add(wanted['sha'])
        entries.append(dict(path=path, **wanted))
    else:
        entries.append(dict(path=path, mode='100644', type='blob', content=text))
tree = api('POST', 'git/trees', dict(base_tree=main['tree']['sha'], tree=entries))['sha']
delta = difference(main['tree']['sha'], tree)
require({x['path'] for x in delta} == set(changed), 'Initial complete native scope differs')
for path, raw in expected.items():
    require(at(tree, path) == dict(mode='100644', type='blob', sha=blob(raw)), 'Native packet identity differs')
fresh_reads, inherited = [], []
for path, raw in expected.items():
    pin, read = oldpins.get(path), oldreads.get(path)
    if (pin and read and pin['bytes'] == len(raw) and pin['sha256'] == sha(raw) and
            pin['git_blob_sha1'] == blob(raw) and read['sha256'] == sha(raw) and
            read['actual_body_byte_identical'] is True and
            at(anchor['tree']['sha'], path) == dict(mode='100644', type='blob', sha=blob(raw))):
        inherited.append(dict(path=path, sha256=sha(raw), actual_body_byte_identical=True,
            body_readback_inherited_from_unchanged_git_blob=prior['commit'],
            current_native_tree_identity_rechecked=True))
    else:
        fresh_reads.append((path, raw))


def verify_body(item):
    path, raw = item
    response = api('GET', 'git/blobs/' + blob(raw))
    require(response['sha'] == blob(raw) and response.get('encoding') == 'base64' and
            base64.b64decode(response['content']) == raw, 'Actual native body differs: ' + path)
    return dict(path=path, sha256=sha(raw), actual_body_byte_identical=True,
        fresh_body_GET=True, git_blob_sha1=blob(raw))


print(json.dumps(dict(stage='native_objects_verified_before_main_ref', fresh_body_GETs=len(fresh_reads),
    inherited_same_blob_reads=len(inherited), total_files=len(expected))), flush=True)
with ThreadPoolExecutor(max_workers=3) as pool:
    verified = list(pool.map(verify_body, fresh_reads))
for attempt in range(1, 6):
    claim()
    parent = api('GET', 'git/ref/heads/main')['object']['sha']
    base = api('GET', 'git/commits/' + parent)
    overlay = []
    for path, raw in sorted(expected.items()):
        wanted = dict(mode='100644', type='blob', sha=blob(raw))
        fresh = at(base['tree']['sha'], path)
        require(fresh in (at(anchor['tree']['sha'], path), wanted), 'Fresh main changed owned path: ' + path)
        if fresh != wanted:
            overlay.append(dict(path=path, **wanted))
    tree = api('POST', 'git/trees', dict(base_tree=base['tree']['sha'], tree=overlay))['sha']
    changes = difference(base['tree']['sha'], tree)
    require({x['path'] for x in changes} == {x['path'] for x in overlay}, 'Final full native changed-path scope differs')
    for path, raw in expected.items():
        require(at(tree, path) == dict(mode='100644', type='blob', sha=blob(raw)), 'Final tree differs')
        require((ROOT/path).read_bytes() == raw, 'Local checkpoint source changed')
    new = api('POST', 'git/commits', dict(
        message='Checkpoint PR209 at80%: reviewed preprint ready; publication awaits disk space',
        tree=tree, parents=[parent]))['sha']
    require([x['sha'] for x in api('GET', 'git/commits/'+new)['parents']] == [parent], 'Wrong sole commit parent')
    if api('GET', 'git/ref/heads/main')['object']['sha'] != parent:
        record(T / f'ABANDONED_BEFORE_MAIN_{attempt:04d}.json', dict(parent=parent, commit=new, tree=tree,
            main_ref_request_not_issued=True, reason='Concurrent main advance; rebuild from fresh parent'))
        continue
    record(T / 'MAIN_UPDATE_INTENT.json', dict(utc=datetime.now(timezone.utc).isoformat(),
        parent=parent, target=new, tree=tree, force=False, case_completion_percent=80,
        counts=[44,21,21,0], scientific_PR_release=False))
    response = api('PATCH', 'git/refs/heads/main', dict(sha=new, force=False))
    require(response['object']['sha'] == new, 'Main update response differs; read-only recovery required')
    break
else:
    raise RuntimeError('Concurrent main repeatedly advanced before any main-ref request')
actual = api('GET', 'git/commits/'+new)
require([x['sha'] for x in actual['parents']] == [parent] and actual['tree']['sha'] == tree,
        'Actual published checkpoint graph differs')
claim()
latest = api('GET', 'git/ref/heads/main')['object']['sha']
if latest != new:
    ancestry = api('GET', 'compare/'+new+'...'+latest)
    require(ancestry['status'] == 'ahead' and ancestry['merge_base_commit']['sha'] == new,
            'Fresh main no longer contains published checkpoint')
for path, raw in expected.items():
    require(at(tree,path) == dict(mode='100644',type='blob',sha=blob(raw)) and (ROOT/path).read_bytes()==raw,
            'Final immutable checkpoint binding differs')
receipt = dict(utc=datetime.now(timezone.utc).isoformat(), commit=new, parent=parent, tree=tree,
    main_readback=latest, case_completion_percent=80, owned_files=frozen_pins,
    actual_native_byte_readbacks=verified+inherited, actual_changed_paths=[x['path'] for x in changes],
    fresh_main_sole_parent_verified=True, full_native_changed_path_scope_verified=True,
    native_PR_original_unchanged_and_still_claimed=True, preprint_preparation_cleared=True,
    preprint_upload_cleared=True, operational_publication_still_resource_gated=True,
    actual_Zenodo_tracker_native_PR_release_actions=0, counts=[44,21,21,0],
    local_Git_index_ref_mutations=0, goal_active_incomplete=True,
    fresh_actual_native_body_GETs=len(verified), inherited_authenticated_same_blob_readbacks=len(inherited),
    all_current_native_tree_body_identities_rechecked=len(expected), previous_checkpoint=prior['commit'])
record(OUT,receipt)
print(json.dumps({k:v for k,v in receipt.items() if k not in
    {'owned_files','actual_native_byte_readbacks','actual_changed_paths'}},indent=2),flush=True)
