"""Publish only owned preliminary PR344 priority findings and coordination logs."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, os, subprocess
P = Path(__file__).resolve().parent
R = P.parent
A = P / 'audits/pr344_30005649'
PREFIX = 'checkpoint_344_priority_003'
def utc(): return datetime.now(timezone.utc).isoformat()
def sha(b): return hashlib.sha256(b).hexdigest()
def load(p): return json.loads(p.read_bytes())
def window(): assert not load(P / 'SHARED_GIT_WINDOW_STATUS.json')['shared_git_writes_paused']
assert not (P / (PREFIX + '_receipt.json')).exists()
assert not (P / (PREFIX + '_stage.json')).exists()
progress = load(A / 'ROOT_PRIORITY_PROGRESS_003.json')
assert progress['mathematics_percent'] == 100 and not progress['priority_closed']
assert sha((A / 'ROOT_PRIORITY_COMPARISON_003.md').read_bytes()) == progress['root_note_sha256']
paths = set()
def add(p):
    assert p.is_file() and not p.is_symlink() and p.resolve().is_relative_to(P)
    assert not any(part.startswith('private_') or part.endswith('_private') or part == '__pycache__' for part in p.relative_to(R).parts)
    paths.add(str(p.relative_to(R)))
for name in ['RESEARCH_LOG.md', 'SHARED_GIT_WINDOW_STATUS.json', 'checkpoint_344_priority_002_receipt.json',
             'root_pause_pr57_20261004.py', 'root_resume_pr57_20261004.py', Path(__file__).name]: add(P / name)
for name in ['RESEARCH_LOG.md', 'ROOT_PRIORITY_WORK_LOG.md', 'ROOT_PRIORITY_COMPARISON_003.md',
             'ROOT_PRIORITY_PROGRESS_003.json', 'root_compare_mfo_ems.py', 'ROOT_MFO_EMS_QUESTION_COMPARISON.json',
             'root_priority_retrieve_mfo.py', 'root_priority_retrieve_005.py']: add(A / name)
allow = P / (PREFIX + '_allowlist.json')
paths.add(str(allow.relative_to(R)))
allow.write_text(json.dumps({'utc': utc(), 'paths': sorted(paths), 'math_percent': 100,
                            'priority_percent_estimate': 65, 'workflow_percent': 30,
                            'scope': 'Only root owned provisional stronger classical comparison and exact reading limits, MFO chronology/page equality computation, two new retrieval scripts, research logs, PR57 pause/resume scripts and previous root checkpoint receipt. Private sources/captures and active child namespaces excluded. No final priority verdict, PR merge or publication.'}, indent=2) + '\n')
def git(*args):
    return subprocess.check_output(['git', *args], cwd=R, env=dict(os.environ, GIT_OPTIONAL_LOCKS='0'))
assert git('branch', '--show-current') == b'main\n'
assert not git('diff', '--name-only', '--diff-filter=U')
assert not git('diff', '--cached', '--raw', '-z')
assert subprocess.run(['git', 'rev-parse', '-q', '--verify', 'MERGE_HEAD'], cwd=R, capture_output=True).returncode != 0
def foreign():
    entries = {}
    bodies = {}
    for item in git('ls-files', '--stage', '-z').split(b'\0'):
        if item:
            meta, name = item.split(b'\t', 1)
            if name.decode() not in paths: entries.setdefault(name, []).append(meta)
    for name in git('diff', '--name-only', '-z').split(b'\0'):
        if name and name.decode() not in paths:
            f = R / name.decode()
            bodies[name] = {'exists': f.exists(), 'bytes': f.read_bytes() if f.is_file() else None,
                            'mode': f.stat().st_mode & 0o7777 if f.exists() else None}
    return entries, bodies
window()
before = foreign()
parent = git('rev-parse', 'HEAD').decode().strip()
assert parent == '5884f4fd1237f66ba6759d59b245f8cdbf0c8afa'
assert git('ls-remote', 'origin', 'refs/heads/main').decode().split()[0] == parent
for label, argv in [('stage', ['git', 'add', '-f', '--', *sorted(paths)]),
                    ('commit', ['git', 'commit', '--only', '-m', 'Record stronger classical comparison and bounded priority audit for PR344', '--', *sorted(paths)]),
                    ('push', ['git', 'push', 'origin', 'main'])]:
    window()
    start = utc()
    (P / (PREFIX + '_' + label + '_preexecution.json')).write_text(json.dumps({'utc': start, 'argv': argv, 'orchestrator_sha256': sha(Path(__file__).read_bytes())}, indent=2) + '\n')
    proc = subprocess.run(argv, cwd=R, capture_output=True)
    for name, value in [('stdout', proc.stdout), ('stderr', proc.stderr)]:
        (P / (PREFIX + '_' + label + '.' + name)).write_bytes(value)
    (P / (PREFIX + '_' + label + '.json')).write_text(json.dumps({'argv': argv, 'started_utc': start, 'finished_utc': utc(), 'exit_status': proc.returncode, 'stdout_sha256': sha(proc.stdout), 'stderr_sha256': sha(proc.stderr)}, indent=2) + '\n')
    assert proc.returncode == 0, (label, proc.stderr.decode(errors='replace'))
    assert foreign() == before
commit = git('rev-parse', 'HEAD').decode().strip()
changed = set(git('diff-tree', '--no-commit-id', '--name-only', '-r', commit).decode().splitlines())
assert changed <= paths
assert git('ls-remote', 'origin', 'refs/heads/main').decode().split()[0] == commit
for relative in paths:
    f = R / relative
    assert git('show', commit + ':' + relative) == f.read_bytes(), relative
    mode = git('ls-tree', commit, '--', relative).decode().split()[0]
    assert mode == ('100755' if f.stat().st_mode & 0o111 else '100644'), relative
assert not git('diff', '--cached', '--raw', '-z')
rec = {'utc': utc(), 'status': 'PASS_PR344_PRELIMINARY_PRIORITY_CHECKPOINT_PUSHED',
       'commit': commit, 'parent': parent, 'changed_owned_paths': len(changed), 'allowlist_paths': len(paths),
       'all_allowlisted_git_disk_bytes_modes_equal': True, 'remote_main_exact': True,
       'foreign_index_and_dirty_file_bytes_modes_preserved': True,
       'math_percent': 100, 'priority_percent_estimate': 65, 'workflow_percent': 30,
       'priority_accepted': False, 'pr344_merged_or_published': False, 'persistent_goal_complete': False}
(P / (PREFIX + '_receipt.json')).write_text(json.dumps(rec, indent=2) + '\n')
shared_path = P / 'SHARED_GIT_WINDOW_STATUS.json'
shared = load(shared_path)
shared.update({'utc': utc(), 'last_owned_checkpoint': commit, 'last_owned_checkpoint_pushed': True,
               'descending_git_checkpoint_preparing': False})
shared_path.write_text(json.dumps(shared, indent=2) + '\n')
with (P / 'RESEARCH_LOG.md').open('a') as f:
    f.write('\n### ' + utc() + ' — preliminary PR344 priority checkpoint pushed\n\n'
            'Owned commit ' + commit + ' pushed after exact scoped Git/disk body/mode and remote verification. All foreign index and dirty tracked bodies/modes preserved. Mathematics100%, priority estimated65%, workflow30%; exact application priority remains open. No PR344 merge or publication.\n')
print(json.dumps(rec, indent=2))
