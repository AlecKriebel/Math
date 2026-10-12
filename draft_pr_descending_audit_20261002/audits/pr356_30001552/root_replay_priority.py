#!/usr/bin/env python3
"""Root native readback and explicit replay; captures live outside the audit tree."""
from pathlib import Path
import datetime, hashlib, json, os, stat, subprocess, sys

A = Path(__file__).resolve().parent
N = A / 'priority_review'
def now(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def binding(p):
    b = p.read_bytes()
    return {'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}
def inventory():
    r = {}
    for p in sorted(N.rglob('*')):
        assert not p.is_symlink(), str(p)
        entry = {'mode': stat.S_IMODE(p.stat().st_mode)}
        if p.is_file(): entry.update(type='file', **binding(p))
        else: assert p.is_dir(); entry.update(type='directory')
        r[str(p.relative_to(N))] = entry
    return r
def write(p, x): p.write_text(json.dumps(x, indent=2, sort_keys=True)+'\n')

phase = sys.argv[1]
assert phase in ('preclosure', 'postclosure')
assert (N/'CLOSURE.json').exists() == (phase == 'postclosure')
out = A/'root_replay_private'/('priority_'+phase+'_001')
out.mkdir(parents=True, exist_ok=False)
before = inventory()
write(out/'PREEXECUTION.json', {'utc': now(), 'phase': phase, 'tree': before,
      'orchestrator': binding(Path(__file__))})
env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
commands = [('comparison', 'comparison_check.py', []),
            ('full', 'verify_priority.py', ['--include-external']),
            ('public', 'verify_priority.py', ['--public-only'])]
if phase == 'postclosure': commands = commands[1:]
results = {}
for label, program, flags in commands:
    code = N/program
    (out/(label+'.executed.py')).write_bytes(code.read_bytes())
    argv = ['/opt/homebrew/bin/python3.11', '-B', str(code), *flags]
    started = now()
    p = subprocess.run(argv, cwd=N, env=env, capture_output=True)
    ended = now()
    (out/(label+'.stdout')).write_bytes(p.stdout)
    (out/(label+'.stderr')).write_bytes(p.stderr)
    r = {'argv': argv, 'started_utc': started, 'finished_utc': ended,
         'exit_code': p.returncode, 'executed_code': binding(code),
         'stdout': binding(out/(label+'.stdout')), 'stderr': binding(out/(label+'.stderr'))}
    write(out/(label+'.receipt.json'), r)
    assert p.returncode == 0 and p.stderr == b'', r
    if label == 'comparison':
        assert p.stdout == (N/'comparison.stdout').read_bytes()
    else:
        expected = json.loads((N/'verification_private/integrity_runs'/(label+'.stdout')).read_bytes())
        if label == 'full': expected['native_integrity_receipts'] = 2
        if phase == 'postclosure':
            expected['closure_state'] = 'sealed'
            expected['closure_files_checked'] = 155 if label == 'full' else 18
        assert json.loads(p.stdout) == expected, (label, json.loads(p.stdout), expected)
    assert inventory() == before, 'Audit tree changed during root replay'
    results[label] = r
write(out/'POSTEXECUTION.json', {'utc': now(), 'tree': inventory()})
receipt = {'utc': now(), 'status': 'PASS_EXACT_PRIORITY_NATIVE_REPLAY_'+phase.upper(),
           'files': sum(v['type']=='file' for v in before.values()),
           'directories': sum(v['type']=='directory' for v in before.values()),
           'tree_unchanged': True, 'tree': before, 'runs': results,
           'orchestrator': binding(Path(__file__)),
           'math_completion_percent': 100, 'publication_workflow_percent': 40,
           'priority_scope': 'Bounded inspected-source audit; no universal priority certificate'}
write(A/('ROOT_PRIORITY_'+phase.upper()+'_REPLAY.json'), receipt)
print(json.dumps({k:v for k,v in receipt.items() if k not in ('tree','runs')}, indent=2))
