"""Complete literal Git verification after the shared writer window releases."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, os, subprocess

A = Path(__file__).resolve().parent
R = A.parents[2]
P = A.parents[1]
D = A / 'root_capture_private/frozen_git_001'
D.mkdir(exist_ok=False)
sha = lambda b: hashlib.sha256(b).hexdigest()
utc = lambda: datetime.now(timezone.utc).isoformat()
captures = []
def run(args):
    i = len(captures)
    start = utc()
    r = subprocess.run(args, cwd=R, capture_output=True, env=dict(os.environ, GIT_OPTIONAL_LOCKS='0'))
    rec = {'argv': args, 'cwd': str(R), 'started_utc': start, 'completed_utc': utc(), 'exit_code': r.returncode}
    for name, b in [('stdout', r.stdout), ('stderr', r.stderr)]:
        (D / (f'{i:03}.' + name)).write_bytes(b)
        rec[name + '_bytes'] = len(b)
        rec[name + '_sha256'] = sha(b)
    (D / f'{i:03}.json').write_text(json.dumps(rec, indent=2) + '\n')
    captures.append(rec)
    assert r.returncode == 0, (args, r.returncode, r.stderr.decode(errors='replace'))
    return r.stdout
git = lambda *args: run(['git', *args])
assert not json.loads((P / 'SHARED_GIT_WINDOW_STATUS.json').read_bytes())['shared_git_writes_paused']
m = json.loads((A / 'snapshot_manifest.json').read_bytes())
H, B = m['head'], m['base']
assert git('branch', '--show-current').strip() == b'main'
main = git('rev-parse', 'HEAD')
ix = Path(git('rev-parse', '--git-path', 'index').decode().strip())
ix = ix if ix.is_absolute() else R / ix
index = ix.read_bytes()
git('fetch', '--no-tags', 'origin', H)
expected = {e['path'] for e in m['files']}
assert set(git('diff', '--name-only', B, H).decode().splitlines()) == expected
assert git('show', '-s', '--format=%T', H).decode().strip() == m['head_tree']
for e in m['files']:
    path = e['path']
    b = git('show', H + ':' + path)
    assert len(b) == e['bytes'] and sha(b) == e['sha256']
    assert b == (A / 'snapshot' / path).read_bytes()
    meta = git('ls-tree', H, '--', path).split(b'\t', 1)[0].split()
    assert meta == [e['mode'].encode(), b'blob', e['git_blob_sha'].encode()]
pr = json.loads(run(['gh', 'pr', 'view', '356', '--json', 'state,isDraft,headRefOid,baseRefOid']))
assert pr['state'] == 'OPEN' and pr['isDraft'] and pr['headRefOid'] == H and pr['baseRefOid'] == B
Q = 'unsolved_math_prioritization/QUEUE.md'
old, new = git('show', B + ':' + Q), git('show', H + ':' + Q)
aa, bb = old.splitlines(keepends=True), new.splitlines(keepends=True)
assert len(aa) == len(bb)
diff = [i for i, (x, y) in enumerate(zip(aa, bb)) if x != y]
assert len(diff) == 1
i = diff[0]
x, y = aa[i].split(b'|'), bb[i].split(b'|')
assert x[2].strip().split(b' / ')[0] == y[2].strip().split(b' / ')[0] == b'30001552'
assert [j for j, (a, b) in enumerate(zip(x, y)) if a != b] == [8, 9]
assert [x[j].strip() for j in [8, 9]] == [b'queued', b'0/5']
assert [y[j].strip() for j in [8, 9]] == [b'claimed_solved', b'1/5']
assert git('rev-parse', 'HEAD') == main and ix.read_bytes() == index
rec = {'utc': utc(), 'status': 'PASS_LITERAL_GIT_ALL17_PREVIOUSLY_API_FROZEN_FILES',
       'pr': 356, 'head': H, 'base': B, 'all_17_blob_bytes_modes_exact': True,
       'head_tree_exact': True, 'snapshot_manifest_sha256': sha((A / 'snapshot_manifest.json').read_bytes()),
       'only_own_queue_line': i + 1, 'only_queue_pipe_cells': [8, 9],
       'all_other_queue_bytes_unchanged': True, 'entire_shared_index_and_main_unchanged': True,
       'submitted_status': 'claimed_solved', 'author_turns': '1/5',
       'initial_API_manifest_retained_as_dated_history': True,
       'captures': captures, 'program_sha256': sha(Path(__file__).read_bytes())}
(A / 'ROOT_FROZEN_GIT_VERIFICATION.json').write_text(json.dumps(rec, indent=2) + '\n')
print(json.dumps({k: v for k, v in rec.items() if k != 'captures'}, indent=2))
