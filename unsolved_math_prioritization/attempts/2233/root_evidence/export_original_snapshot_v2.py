"""ROOT read-only original-head export; does not execute any scientific helper."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import subprocess

A = Path(__file__).resolve().parent
R = A.parents[2]
HEAD = '099ae5e4d06d8789214cfaaece87309c87e914f9'
BASE = '60292bed09f59236aa192cb17aa138f7b4750e1a'
PREFIX = 'unsolved_math_prioritization/attempts/2233/'
commands = []

def run(argv):
    started = dt.datetime.now(dt.timezone.utc).isoformat()
    p = subprocess.Popen(argv, cwd=R, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    index = len(commands)
    for name, body in [('stdout', out), ('stderr', err)]:
        (A / 'original_git_commands_v2' / (str(index) + '.' + name)).write_bytes(body)
    commands.append({'argv': argv, 'cwd': str(R), 'pid': p.pid, 'started_utc': started,
                     'finished_utc': dt.datetime.now(dt.timezone.utc).isoformat(), 'exit_code': p.returncode,
                     'stdout': {'path': str(index) + '.stdout', 'bytes': len(out), 'sha256': hashlib.sha256(out).hexdigest()},
                     'stderr': {'path': str(index) + '.stderr', 'bytes': len(err), 'sha256': hashlib.sha256(err).hexdigest()}})
    assert p.returncode == 0
    return out

def main():
    (A / 'original_git_commands_v2').mkdir()
    (A / 'source_snapshot_v2').mkdir()
    try:
        assert run(['git', 'branch', '--show-current']).strip() == b'main'
        current = run(['git', 'rev-parse', 'HEAD']).decode().strip()
        assert run(['git', 'rev-parse', 'origin/dot/math-2233']).decode().strip() == HEAD
        assert run(['git', 'merge-base', current, HEAD]).decode().strip() == BASE
        tree = run(['git', 'ls-tree', '-r', '-z', HEAD, '--', PREFIX]).decode().split('\0')
        rows = []
        for entry in filter(None, tree):
            fields, name = entry.split('\t')
            mode, kind, oid = fields.split()
            assert kind == 'blob' and mode == '100644' and name.startswith(PREFIX)
            relative = name[len(PREFIX):]
            p = A / 'source_snapshot_v2' / relative
            p.parent.mkdir(parents=True, exist_ok=True)
            raw = run(['git', 'show', HEAD + ':' + name])
            p.write_bytes(raw)
            p.chmod(0o444)
            rows.append({'path': relative, 'size': len(raw), 'sha256': hashlib.sha256(raw).hexdigest(), 'mode': mode, 'git_blob': oid})
        assert len(rows) == 17
        changed = run(['git', 'diff', '--name-only', BASE, HEAD]).decode().splitlines()
        assert set(changed) == {PREFIX + x['path'] for x in rows} | {'unsolved_math_prioritization/QUEUE.md'}
        patch = run(['git', 'diff', BASE, HEAD])
        (A / 'original_diff_v2.patch').write_bytes(patch)
        (A / 'original_diff_v2.patch').chmod(0o444)
        record = {'schema': 'pr42-root-readonly-original-snapshot/v1', 'utc': dt.datetime.now(dt.timezone.utc).isoformat(),
                  'pr': 42, 'id': 2233, 'head': HEAD, 'base': BASE, 'main_at_export': current,
                  'files': rows, 'changed_paths': changed, 'diff_bytes': len(patch), 'diff_sha256': hashlib.sha256(patch).hexdigest(),
                  'original_scientific_helpers_executed': False, 'mathematical_review': 'PENDING', 'new_substantive_attempts': 0, 'audit_turns': 0}
        (A / 'snapshot_manifest_v2.json').write_text(json.dumps(record, indent=2) + '\n')
        (A / 'snapshot_manifest_v2.json').chmod(0o444)
        assert run(['git', 'rev-parse', 'HEAD']).decode().strip() == current
        print(json.dumps({'status': 'PASS_ORIGINAL_EXPORT_ONLY', 'members': len(rows), 'changed': len(changed), 'diff_bytes': len(patch), 'snapshot_manifest_sha256': hashlib.sha256((A / 'snapshot_manifest_v2.json').read_bytes()).hexdigest()}))
    finally:
        (A / 'ORIGINAL_GIT_COMMANDS_V2.json').write_text(json.dumps(commands, indent=2) + '\n')

if __name__ == '__main__':
    main()
