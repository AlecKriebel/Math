from pathlib import Path
import datetime
import hashlib
import json
import subprocess

A = Path(__file__).resolve().parent
R = A.parent
HEAD = '9946a67cf8a1f7e3130d2a12de902db05875283a'
PRIVATE = A / 'private_runs' / 'portable_candidate'
manifest = json.loads((R / 'snapshot_manifest.json').read_text())
assert manifest['head'] == HEAD
bindings = []
for entry in manifest['files']:
    git_bytes = subprocess.check_output(['git', 'show', HEAD + ':' + entry['path']])
    public_bytes = (R / 'snapshot' / entry['path']).read_bytes()
    private_bytes = (PRIVATE / entry['path']).read_bytes()
    digest = hashlib.sha256(git_bytes).hexdigest()
    assert git_bytes == public_bytes == private_bytes
    assert digest == entry['sha256'] and len(git_bytes) == entry['bytes']
    bindings.append({'path': entry['path'], 'sha256': digest, 'bytes': len(git_bytes),
                     'git_snapshot_private_equal': True})
assert len(bindings) == 44
target = PRIVATE / 'problems' / '30002762_conjugation_norms'
replays = []
for i in (1, 2, 3):
    start = datetime.datetime.now(datetime.timezone.utc).isoformat()
    run = subprocess.run(['python3', str(target / f'check_turn_{i}.py')],
                         cwd=target, capture_output=True)
    expected = (target / f'TURN_{i}_CHECKS.json').read_bytes()
    assert run.returncode == 0 and not run.stderr and run.stdout == expected
    (A / 'private_runs' / f'scoped_turn{i}.stdout').write_bytes(run.stdout)
    (A / 'private_runs' / f'scoped_turn{i}.stderr').write_bytes(run.stderr)
    replays.append({'turn': i, 'exit_code': run.returncode,
                    'started_utc': start,
                    'finished_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
                    'stdout': run.stdout.decode(), 'stderr': run.stderr.decode(),
                    'stdout_sha256': hashlib.sha256(run.stdout).hexdigest(),
                    'stderr_sha256': hashlib.sha256(run.stderr).hexdigest(),
                    'stored_receipt_byte_exact': True})
seal = json.loads((A / 'PRECOMPARISON_SEAL.json').read_text())
for entry in seal['files']:
    b = (A / entry['path']).read_bytes()
    assert len(b) == entry['bytes'] and hashlib.sha256(b).hexdigest() == entry['sha256']
result = {'head': HEAD, 'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
          'pass': True, 'all44_git_snapshot_private_bindings': bindings,
          'precomparison_seal_still_exact': True, 'scoped_replays': replays}
(A / 'SCOPED_REPLAY_BINDINGS.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({'pass': True, 'bindings': len(bindings), 'head': HEAD,
                  'scoped_assertions': {x['turn']: json.loads(x['stdout'])['assertions'] for x in replays},
                  'precomparison_seal_still_exact': True}, indent=2))
