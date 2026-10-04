"""Capture own final inspector, then close only this family's created files."""
from pathlib import Path, PurePosixPath
import datetime as dt
import hashlib
import json
import os
import stat
import subprocess
import sys
import traceback

HERE = Path(__file__).absolute().parent
R = HERE.parents[3]
def now(): return dt.datetime.now(dt.timezone.utc).isoformat()
def sha(b): return hashlib.sha256(b).hexdigest()
def dump(x): return (json.dumps(x, indent=2, allow_nan=False) + '\n').encode()
assert __debug__ and os.environ.get('PYTHONOPTIMIZE', '') in ('', '0')
assert not (HERE / 'SELF_MANIFEST.json').exists()
src = HERE / 'inspect_before_closure.py'; body = src.read_bytes(); operator = Path(__file__).read_bytes()
dest = HERE / 'FINAL_INSPECTION_ACTUAL_CAPTURE'; dest.mkdir(exist_ok=False)
for label, raw in [('PRELAUNCH_SOURCE.py', body), ('PRELAUNCH_OPERATOR.py', operator)]:
    with (dest / label).open('xb') as f: f.write(raw); f.flush(); os.fsync(f.fileno())
argv = ['/usr/bin/python3', '-B', str(src)]
cap = {'schema': 'pr44-source-adversary-actual-final-inspection-capture/v1', 'operator_pid': os.getpid(), 'argv': argv, 'cwd': str(R), 'started_utc': now(), 'source_sha256': sha(body), 'operator_sha256': sha(operator), 'actual_execution': False, 'completed': False, 'pid': None, 'exit_code': None, 'stdin_supplied': False}
try:
    with (dest / 'stdout.bin').open('xb') as out, (dest / 'stderr.bin').open('xb') as err:
        child = subprocess.Popen(argv, cwd=R, stdin=subprocess.DEVNULL, stdout=out, stderr=err, env=dict(os.environ, PYTHONOPTIMIZE='0'))
        cap.update(actual_execution=True, pid=child.pid)
        try: cap['exit_code'] = child.wait(timeout=120); cap['completed'] = True
        except BaseException: child.kill(); cap['exit_code'] = child.wait(); raise
except BaseException: cap['failure'] = traceback.format_exc()
finally:
    cap['finished_utc'] = now()
    for channel in ['stdout', 'stderr']:
        p = dest / (channel + '.bin')
        if p.exists():
            raw = p.read_bytes(); cap[channel] = {'path': p.name, 'bytes': len(raw), 'sha256': sha(raw)}
    cap['source_unchanged'] = src.read_bytes() == body; cap['operator_unchanged'] = Path(__file__).read_bytes() == operator
    cap['status'] = 'PASS' if cap['actual_execution'] is True and cap['completed'] is True and cap['exit_code'] == 0 and cap['source_unchanged'] and cap['operator_unchanged'] and 'failure' not in cap else 'FAIL_PRESERVED'
    (dest / 'CAPTURE.json').write_bytes(dump(cap))
assert cap['status'] == 'PASS', 'Final inspection failed; preserve source and full streams'
with (HERE / 'RESEARCH_LOG.md').open('a') as f:
    f.write(now() + ' — final independent own inspection actually completed; source audit100%, discovery0%. Two positive own control runs20467 checks/107 rejected cases; all366 foreign inputs plus exact template/cache references verified again. Original2/5,new0,audit0; no production execution or new whole-current PASS. Close authored files only, full0444, sole self exclusion.\n')
members, dirs = [], []
for p in sorted(HERE.rglob('*')):
    assert not p.is_symlink() and not any(q.is_symlink() for q in p.parents)
    name = p.relative_to(HERE).as_posix()
    if stat.S_ISREG(p.stat().st_mode):
        p.chmod(0o444); raw = p.read_bytes(); assert stat.S_IMODE(p.stat().st_mode) == 0o444
        members.append({'path': name, 'bytes': len(raw), 'sha256': sha(raw)})
    else:
        assert stat.S_ISDIR(p.stat().st_mode); dirs.append(name)
needed = {q.as_posix() for row in members for q in PurePosixPath(row['path']).parents if q.as_posix() != '.'}
assert set(dirs) == needed
value = {'schema': 'pr44-new-current-source-adversary-self-only-closure/v1', 'utc': now(), 'status': 'CLOSED_CLEAN_SOURCE_ONLY_ADVERSARY', 'files_count': len(members), 'files': members, 'directories': dirs, 'self_excluded': ['SELF_MANIFEST.json'], 'full_permission_mode': '0444', 'foreign_inputs_manifest': 'INDIVIDUAL_FOREIGN_INPUTS.json', 'foreign_primary_bodies_copied': False, 'captured_readonly_Git_project_diff_is_procedural_stream_not_mathematical_authorship': True, 'production_execution_or_import': False, 'first_failed_own_run_syntax_only_AST_inspection_disclosed': True, 'positive_controls_strictly_text_only': True, 'new_whole_current_gate': 'PENDING', 'original_substantive_attempts': 2, 'new_substantive_attempts': 0, 'audit_turns': 0, 'source_audit_completion_percent': 100, 'full_discovery_completion_percent': 0}
mf = HERE / 'SELF_MANIFEST.json'; mf.write_bytes(dump(value)); mf.chmod(0o444)
assert stat.S_IMODE(mf.stat().st_mode) == 0o444
for row in members:
    p = HERE / row['path']; raw = p.read_bytes(); assert len(raw) == row['bytes'] and sha(raw) == row['sha256'] and stat.S_IMODE(p.stat().st_mode) == 0o444
assert {p.relative_to(HERE).as_posix() for p in HERE.rglob('*') if p.is_file()} == {r['path'] for r in members} | {'SELF_MANIFEST.json'}
print(json.dumps({'status': value['status'], 'files_count': len(members), 'manifest_bytes': len(mf.read_bytes()), 'manifest_sha256': sha(mf.read_bytes()), 'actual_final_inspector_pid': child.pid, 'production_execution': False}, indent=2))
