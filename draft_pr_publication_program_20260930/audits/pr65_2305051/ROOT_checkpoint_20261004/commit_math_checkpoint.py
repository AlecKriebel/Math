"""Publish one explicit owned audit checkpoint under the acknowledged writer window."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import os
import stat
import subprocess

F = Path(__file__).resolve().parent
A = F.parent
P = A.parents[1]
R = P.parent
C = P / 'audits/pr45_9900007'
D = F / 'private_actual_git_commands'
D.mkdir()
(D / 'PRELAUNCH_SOURCE.py').write_bytes(Path(__file__).read_bytes())
commands = []

def sha(body): return hashlib.sha256(body).hexdigest()
def load(path): return json.loads(path.read_bytes())
def run(*parts):
    argv = ['git', '--no-optional-locks', *parts]
    start = dt.datetime.now(dt.timezone.utc).isoformat()
    child = subprocess.Popen(argv, cwd=R, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = child.communicate()
    label = str(len(commands) + 1)
    (D / (label + '.stdout')).write_bytes(out)
    (D / (label + '.stderr')).write_bytes(err)
    commands.append({'argv': argv, 'actual_pid': child.pid, 'started_UTC': start,
                     'finished_UTC': dt.datetime.now(dt.timezone.utc).isoformat(),
                     'exit_code': child.returncode, 'stdout_sha256': sha(out), 'stderr_sha256': sha(err)})
    (D / 'COMMANDS.json').write_text(json.dumps(commands, indent=2) + '\n')
    assert child.returncode == 0, err.decode(errors='replace')
    return out
def names(body): return {p.decode() for p in body.split(b'\0') if p}
def pin(name):
    path = R / name
    if not path.exists(): return {'absent': True}
    assert path.is_file() and not path.is_symlink()
    body = path.read_bytes()
    return {'bytes': len(body), 'sha256': sha(body), 'mode': stat.S_IMODE(path.stat().st_mode)}

window_path = R / 'draft_pr_descending_audit_20261002/SHARED_GIT_WINDOW_STATUS.json'
window_body = window_path.read_bytes()
def window():
    obj = load(window_path)
    assert window_path.read_bytes() == window_body
    assert obj['shared_git_writes_paused'] is True
    assert obj['paused_for'] == 'PR65 mathematical audit checkpoint 20261004'
    assert obj['utc'] == '2026-10-04T05:43:35.388431+00:00'
    assert obj['dirty_tracked_bodies_modes_frozen_after_acknowledgement'] is True
    assert obj['all_staged_path_count'] == 0 and not obj['owned_staged_paths']
    assert obj['local_main_at_pause'] == obj['remote_main_at_pause']
    return obj
w = window()
assert run('branch', '--show-current').strip() == b'main'
assert not run('diff', '--cached', '--name-only', '-z')
base = run('rev-parse', 'HEAD').decode().strip()
assert base == w['local_main_at_pause'] == run('ls-remote', '--heads', 'origin', 'main').decode().split()[0]
progress = load(P / 'CURRENT_PROGRESS.json')
assert progress['current_PR'] == 65 and progress['current_mathematical_audit_percent'] == 100
assert progress['current_priority_clearance'] is False and progress['persistent_goal_complete'] is False
roots = [A / 'original_source_authentication_20261004', A / 'ROOT_reproduction_20261004',
         A / 'ROOT_selected_source_20261004', A / 'universal_bloch_analytic_adversary_20261004',
         A / 'blaschke_factorization_scope_adversary_20261004', F,
         A / 'ROOT_MATHEMATICAL_REVIEW_20261004.md', A / 'RESEARCH_LOG.md', A / '.gitignore',
         P / 'CURRENT_PROGRESS.json',
         P / 'audits/pr57_30003354/root_ordered_resumption_20261004/COMPLETION_CHECKPOINT_RECEIPT.json',
         P / 'audits/pr57_30003354/root_ordered_resumption_20261004/POSTPUSH_PROGRESS_RECONCILIATION.json',
         P / 'audits/pr57_30003354/root_ordered_resumption_20261004/RESEARCH_LOG.md']
for folder in ['root_pr65_original_custody_and_reproduction_20261004_actual_capture',
               'root_pr65_new_family_readback_20261004_actual_capture',
               'root_pr65_progress_checkpoint_preparation_20261004_actual_capture',
               'root_pr57_completion_scoped_push_20261004_actual_capture']:
    path = C / folder
    assert load(path / 'CAPTURE.json')['status'] == 'PASS'
    roots.append(path)
relative = [p.relative_to(R).as_posix() for p in roots]
selected = names(run('diff', '--name-only', '-z', '--', *relative)) | names(run('ls-files', '--others', '--exclude-standard', '-z', '--', *relative))
selected = {n for n in selected if not any(part in Path(n).parts for part in ['private_actual_git_commands', '__pycache__', 'primary_sources'])
            and not n.endswith(('.pdf', '.png', '.pyc'))
            and not n.endswith('/SOURCE_PRELAUNCH_SNAPSHOT.json')
            and not n.endswith('/commands/002_prelaunch_local_status.stdout')}
assert selected and all(any(n == root or n.startswith(root + '/') for root in relative) for n in selected)
assert not any('SHARED_GIT_WINDOW_STATUS' in n or 'classical_priority_mechanism' in n or 'current_priority_sources' in n for n in selected)
foreign = {n: pin(n) for n in names(run('diff', '--name-only', '-z')) - selected}
owned = {n: pin(n) for n in sorted(selected)}
native = {n: pin(n) for n in ['unsolved_math_prioritization/QUEUE.md', 'unsolved_math_prioritization/state.json', 'unsolved_math_prioritization/history.jsonl']}
assert all(not x.get('absent') for x in owned.values())
plan = {'schema': 'PR65-interim-mathematics-scoped-checkpoint/v1', 'UTC': dt.datetime.now(dt.timezone.utc).isoformat(),
        'controller_pid': os.getpid(), 'base': base, 'acknowledgement_sha256': sha(window_body),
        'owned': owned, 'foreign': foreign, 'native_files_to_preserve': native,
        'mathematical_audit_percent': 100, 'PR65_workflow_percent': 25, 'priority_clearance': False,
        'ordered_completed_count': 6, 'dated_denominator': 99, 'goal_complete': False}
planpath = F / 'CHECKPOINT_PLAN.json'
with planpath.open('x') as f: json.dump(plan, f, indent=2); f.write('\n')
planname = planpath.relative_to(R).as_posix()
selected.add(planname); owned[planname] = pin(planname)
def preserve():
    window()
    assert names(run('diff', '--name-only', '-z')) - selected == set(foreign)
    for n, p in foreign.items(): assert pin(n) == p, n
    for n, p in owned.items(): assert pin(n) == p, n
    for n, p in native.items(): assert pin(n) == p, n
preserve()
run('add', '--', *sorted(selected))
assert names(run('diff', '--cached', '--name-only', '-z')) == selected
for n, p in owned.items(): assert sha(run('show', ':' + n)) == p['sha256']
preserve()
run('commit', '-m', 'Audit PR65 explicit Blaschke construction; retain unresolved priority gate')
commit = run('rev-parse', 'HEAD').decode().strip()
assert run('show', '-s', '--format=%P', commit).decode().strip() == base
assert names(run('diff-tree', '--no-commit-id', '--name-only', '-r', '-z', commit)) == selected
assert run('ls-remote', '--heads', 'origin', 'main').decode().split()[0] == base
preserve()
run('push', 'origin', 'main')
assert run('ls-remote', '--heads', 'origin', 'main').decode().split()[0] == commit
assert not run('diff', '--cached', '--name-only', '-z')
preserve()
receipt = {'schema': 'PR65-interim-math-scoped-push/v1', 'UTC': dt.datetime.now(dt.timezone.utc).isoformat(),
           'controller_pid': os.getpid(), 'commit': commit, 'base': base, 'remote_main': commit,
           'owned_path_count': len(selected), 'foreign_tracked_paths_preserved': len(foreign), 'index_empty': True,
           'native_QUEUE_state_history_unchanged': True, 'PR65_math_audit_percent': 100,
           'PR65_workflow_percent': 25, 'priority_clearance': False, 'PR65_merge_or_publication': False,
           'goal_complete': False, 'receipt_created_after_push_not_embedded_in_own_commit': True}
with (F / 'CHECKPOINT_RECEIPT.json').open('x') as f: json.dump(receipt, f, indent=2); f.write('\n')
print(json.dumps(receipt, indent=2))
