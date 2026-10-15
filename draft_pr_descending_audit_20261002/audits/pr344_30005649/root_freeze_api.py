"""Freeze candidate bytes mechanically without changing the shared Git branch or index."""
from pathlib import Path
from datetime import datetime, timezone
import base64, hashlib, json, subprocess

A = Path(__file__).resolve().parent
R = A.parents[2]
D = A / 'root_capture_private/freeze_api_001'
D.mkdir(exist_ok=False)
H = '86a758b1cc9c94322ce6afc3d17150fa2c90327a'
B = 'bd0b6f8ffe4382fff9f1a7cbaf7755bd058494c4'
sha = lambda b: hashlib.sha256(b).hexdigest()
utc = lambda: datetime.now(timezone.utc).isoformat()
captures = []
def run(args):
    i = len(captures)
    start = utc()
    r = subprocess.run(args, cwd=R, capture_output=True)
    rec = {'argv': args, 'cwd': str(R), 'started_utc': start, 'finished_utc': utc(), 'exit_code': r.returncode}
    for name, b in [('stdout', r.stdout), ('stderr', r.stderr)]:
        (D / (f'{i:03}.' + name)).write_bytes(b)
        rec[name + '_bytes'] = len(b)
        rec[name + '_sha256'] = sha(b)
    (D / f'{i:03}.json').write_text(json.dumps(rec, indent=2) + '\n')
    captures.append(rec)
    assert r.returncode == 0, (args, r.returncode)
    return r.stdout
def api(path):
    return json.loads(run(['gh', 'api', 'repos/AlecKriebel/Math/' + path]))
assert run(['git', 'branch', '--show-current']).strip() == b'main'
main = run(['git', 'rev-parse', 'HEAD'])
index = run(['git', 'ls-files', '-s', '-z'])
before = api('pulls/344')
assert before['state'] == 'open' and before['draft'] and before['head']['sha'] == H
assert before['base']['ref'] == 'main'
listed = api('pulls/344/files?per_page=100')
assert len(listed) == before['changed_files'] == 16
commit = api('git/commits/' + H)
assert commit['sha'] == H
trees = {}
def entry(path):
    oid = commit['tree']['sha']
    parts = path.split('/')
    for i, part in enumerate(parts):
        if oid not in trees:
            tree = api('git/trees/' + oid)
            assert tree['sha'] == oid and not tree['truncated']
            trees[oid] = {e['path']: e for e in tree['tree']}
        e = trees[oid][part]
        if i == len(parts) - 1:
            return e
        assert e['type'] == 'tree' and e['mode'] in {'040000', '40000'}
        oid = e['sha']
S = A / 'snapshot'
S.mkdir(exist_ok=False)
files = []
for row in listed:
    path = row['filename']
    assert row['status'] in {'added', 'modified'}
    assert path == 'unsolved_math_prioritization/QUEUE.md' or path.startswith('problems/30005649_qss_self_duality/')
    e = entry(path)
    assert e['type'] == 'blob' and e['mode'] == '100644' and row['sha'] == e['sha']
    obj = api('git/blobs/' + e['sha'])
    assert obj['sha'] == e['sha'] and obj['encoding'] == 'base64'
    b = base64.b64decode(obj['content'])
    assert len(b) == obj['size'] == e['size']
    assert hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest() == e['sha']
    f = S / path
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_bytes(b)
    f.chmod(0o644)
    files.append({'path': path, 'bytes': len(b), 'sha256': sha(b), 'git_blob_sha': e['sha'], 'mode': e['mode'], 'API_git_object_hash_disk_identical': True})
after = api('pulls/344')
assert after['state'] == 'open' and after['draft'] and after['head']['sha'] == H
assert run(['git', 'rev-parse', 'HEAD']) == main
assert run(['git', 'ls-files', '-s', '-z']) == index
rec = {'utc': utc(), 'status': 'FROZEN_COMPLETE_API_OBJECT_HASH_DISK_SCOPE_LOCAL_GIT_CHECK_PENDING',
       'pr': 344, 'head': H, 'base': B, 'files': files, 'all_files_count': len(files),
       'head_tree': commit['tree']['sha'], 'native_capture_directory': str(D),
       'whole_native_commands': len(captures), 'main_and_shared_index_unchanged': True,
       'no_git_mutation_performed': True, 'local_git_diff_and_blob_verification_pending': True,
       'program_sha256': sha(Path(__file__).read_bytes()),
       'scope': 'Mechanical whole API bytes, Git object hashes and modes only; candidate contents are not read analytically and correctness is not inferred.'}
(A / 'snapshot_manifest.json').write_text(json.dumps(rec, indent=2) + '\n')
print(json.dumps({k: v for k, v in rec.items() if k != 'files'}, indent=2))
