"""Checkpoint independently reproduced PR344 supporting-formula defect and proposed repair."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, os, subprocess
P = Path(__file__).resolve().parent
R = P.parent
A = P / 'audits/pr344_30005649'
PREFIX = 'checkpoint_344_formula_finding_001'
def utc(): return datetime.now(timezone.utc).isoformat()
def sha(b): return hashlib.sha256(b).hexdigest()
def load(p): return json.loads(p.read_bytes())
def window(): assert not load(P / 'SHARED_GIT_WINDOW_STATUS.json')['shared_git_writes_paused']
assert not (P / (PREFIX + '_receipt.json')).exists()
assert not (P / (PREFIX + '_stage.json')).exists()
progress = load(A / 'ROOT_PRIORITY_ACCEPTANCE.json')
assert progress['math_percent'] == progress['priority_percent'] == 100
assert progress['status'].startswith('PRIORITY_ACCEPTED')
paths = set()
def add(p):
    assert p.is_file() and not p.is_symlink() and p.resolve().is_relative_to(P)
    assert not any(part.startswith('private_') or part.endswith('_private') or part == '__pycache__' for part in p.relative_to(R).parts)
    paths.add(str(p.relative_to(R)))
for name in ['RESEARCH_LOG.md','SHARED_GIT_WINDOW_STATUS.json','inventory.json',
             'checkpoint_344_preprint_002_receipt.json','root_pause_pr65_final_note_20261004.py',
             'root_resume_pr65_final_note_20261004.py','root_resume_pr65_final_note_20261004_owned_scope.py',
             'root_resume_pr65_final_note_20261004_live_owner.py',Path(__file__).name]:add(P/name)
for name in ['RESEARCH_LOG.md','CURRENT_PREPRINT_STATUS.json','ROOT_MATHEMATICAL_ACCEPTANCE_QUALIFICATION.json',
             'ROOT_PREPRINT02_TIMING_CORRECTION_READBACK.json','root_intrinsic_formula_diagnostic.py',
             'root_reproduce_intrinsic_formula_001.py','root_prepare_formula_repair.py']:add(A/name)
for name in ['CONTROL_FORMULA_CORRECTION.md','intrinsic_formula_regressions.txt']:add(A/'preprint'/name)
allow = P / (PREFIX + '_allowlist.json')
paths.add(str(allow.relative_to(R)))
allow.write_text(json.dumps({'utc': utc(), 'paths': sorted(paths), 'math_percent': 100,
                            'priority_percent_estimate': 100, 'workflow_percent': 60,
                            'scope': 'Independent counterexamples to the generic supplementary helper, qualification of earlier numerical-control acceptance, current progress, prepared correction derivation/regression fragment not yet installed into the current v03 ZIP, shared-window readbacks, and previous checkpoint receipt. Main symbolic theorem remains valid; full second review and public correction integration are pending, followed by a NEW third review. All raw primary bodies/native captures/extracted archives and active reviewer namespace excluded. No merge/deposit/tracker action.'}, indent=2) + '\n')
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
assert parent == '1135765a7fe02d6c2bbeca7bc1a3a4a5259650a9'
assert git('ls-remote', 'origin', 'refs/heads/main').decode().split()[0] == parent
for label, argv in [('stage', ['git', 'add', '-f', '--', *sorted(paths)]),
                    ('commit', ['git', 'commit', '--only', '-m', 'Record independently falsified PR344 supporting formula and proposed correction', '--', *sorted(paths)]),
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
rec = {'utc': utc(), 'status': 'PASS_PR344_FORMULA_FINDING_CHECKPOINT_PUSHED',
       'commit': commit, 'parent': parent, 'changed_owned_paths': len(changed), 'allowlist_paths': len(paths),
       'all_allowlisted_git_disk_bytes_modes_equal': True, 'remote_main_exact': True,
       'foreign_index_and_dirty_file_bytes_modes_preserved': True,
       'math_percent': 100, 'priority_percent_estimate': 100, 'workflow_percent': 60,
       'priority_accepted': True, 'pr344_merged_or_published': False, 'persistent_goal_complete': False}
(P / (PREFIX + '_receipt.json')).write_text(json.dumps(rec, indent=2) + '\n')
shared_path = P / 'SHARED_GIT_WINDOW_STATUS.json'
shared = load(shared_path)
shared.update({'utc': utc(), 'last_owned_checkpoint': commit, 'last_owned_checkpoint_pushed': True,
               'descending_git_checkpoint_preparing': False})
shared_path.write_text(json.dumps(shared, indent=2) + '\n')
with (P / 'RESEARCH_LOG.md').open('a') as f:
    f.write('\n### ' + utc() + ' — PR344 formula finding and prepared repair checkpoint pushed\n\n'
            'Owned commit ' + commit + ' pushed after exact scoped Git/disk body/mode and remote verification. All foreign index and dirty tracked bodies/modes preserved. Mathematics100%, bounded priority review100%, workflow60%; first historical adverse review closed and B1 repaired; second reviewer found the generic dual-kernel helper defect, which ROOT independently reproduced on both runtimes. Main symbolic theorem100%; proposed formula/regression correction passes development checks but is not yet installed in v03. Full second adverse review closure and NEW third review remain mandatory. Historical first priority uncertified. No PR344 merge or publication.\n')
print(json.dumps(rec, indent=2))
