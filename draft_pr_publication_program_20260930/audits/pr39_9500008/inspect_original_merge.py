"""ROOT whole automatic queue/conflict/original-tree inspection; no reviewed imports."""
from pathlib import Path
import hashlib
import json
import subprocess
import datetime

A = Path(__file__).resolve().parent
R = A.parents[2]
Q = 'unsolved_math_prioritization/QUEUE.md'
H = '652b8115080e5e97b2274cb602de3faf8c551f20'
M = '6f7cdb80ac4ed9d7e1179380de540a4eb5d9a534'
sha = lambda b: hashlib.sha256(b).hexdigest()
run = lambda *x: subprocess.check_output(['git', *x], cwd=R)

assert run('rev-parse', 'HEAD').decode().strip() == M
assert run('rev-parse', 'MERGE_HEAD').decode().strip() == H
assert run('diff', '--name-only', '--diff-filter=U').decode().splitlines() == [Q]
pre = (A / 'integration_queue_before.md').read_bytes()
assert run('show', ':2:' + Q) == pre
assert run('show', ':3:' + Q) == run('show', H + ':' + Q)
assert run('show', ':1:' + Q) == run('show', run('merge-base', M, H).decode().strip() + ':' + Q)
raw = (R / Q).read_bytes()
assert b'<<<<<<<' in raw and b'>>>>>>>' in raw
rows = json.loads((A / 'snapshot_manifest.json').read_bytes())['files']
prefix = 'unsolved_math_prioritization/attempts/9500008/'
expected = {prefix + x['path'] for x in rows} | {Q}
assert set(run('diff', '--cached', '--name-only').decode().splitlines()) == expected
for x in rows:
    p = R / prefix / x['path']
    b = p.read_bytes()
    assert type(x['size']) is int and not p.is_symlink() and len(b) == x['size'] and sha(b) == x['sha256']
    assert b == (A / 'source_snapshot' / x['path']).read_bytes()
    entries = run('ls-files', '--stage', '-z', '--', prefix + x['path']).decode().split('\0')[:-1]
    assert entries == [x['mode'] + ' ' + x['git_blob'] + ' 0\t' + prefix + x['path']]
result = {'schema': 'pr39-root-actual-original-merge-inspection/v1',
          'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
          'head': M, 'merge_head': H, 'whole_queue_sha256': sha(raw), 'only_conflict': Q,
          'complete_stage1_2_3_bytes_compared': True, 'original16_scientific_files_exact': True,
          'staged_paths': sorted(expected), 'manual_queue_resolution_pending': True,
          'initial_own_inline_schema_failure': {'tool_chunk': '829516', 'exit_code': 1,
              'pid': None, 'launch_clock': None, 'source_channel': 'complete inline source in tool call',
              'complete_visible_output': 'Traceback (most recent call last):\n  File "<stdin>", line 8, in <module>\nKeyError: \'bytes\'\n',
              'qualification': 'Snapshot rows use size, not bytes. Failed before writes. Candidate and merge were unchanged.'}}
p = A / 'ROOT_AUTOMATIC_MERGE_INSPECTION.json'
with p.open('x') as f:
    f.write(json.dumps(result, indent=2, sort_keys=True) + '\n')
print(json.dumps({'status': 'PASS', 'root_reviewed_automatic_merge_sha256': sha(p.read_bytes()),
                  'whole_queue_sha256': sha(raw), 'original_count': len(rows)}))
