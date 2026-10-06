"""Push a scoped public-safe audit checkpoint under an acknowledged Git window."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import os
import stat
import subprocess
import sys

if sys.flags.optimize or not __debug__ or not sys.flags.ignore_environment or not sys.flags.dont_write_bytecode:
    raise RuntimeError('Invoke -E -B, no -O')
A = Path(__file__).resolve().parent
P = A.parents[1]
R = P.parent
C = P / 'audits/pr45_9900007'
F = A / 'ROOT_attributed_acceptance_checkpoint_20261004'
F.mkdir(exist_ok=False)
D = F / 'private_actual_git_commands'
D.mkdir()
(D / 'PRELAUNCH_SOURCE.py').write_bytes(Path(__file__).read_bytes())
records = []

def sha(body):
    return hashlib.sha256(body).hexdigest()

def read(path):
    return json.loads(path.read_bytes())

def require(condition, message):
    if not condition:
        raise RuntimeError(message)

def run(*argv):
    command = ['git', '--no-optional-locks', *argv]
    start = dt.datetime.now(dt.timezone.utc).isoformat()
    child = subprocess.Popen(command, cwd=R, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = child.communicate()
    label = str(len(records) + 1)
    (D / (label + '.stdout')).write_bytes(out)
    (D / (label + '.stderr')).write_bytes(err)
    records.append({'argv': command, 'actual_pid': child.pid, 'start_utc': start, 'finish_utc': dt.datetime.now(dt.timezone.utc).isoformat(), 'exit_code': child.returncode, 'stdout_bytes': len(out), 'stdout_sha256': sha(out), 'stderr_bytes': len(err), 'stderr_sha256': sha(err)})
    (D / 'COMMANDS.json').write_text(json.dumps(records, indent=2) + '\n')
    require(child.returncode == 0, 'Git command failed: ' + err.decode(errors='replace'))
    return out

def names(body):
    return {p.decode() for p in body.split(b'\0') if p}

def pin(name):
    path = R / name
    if not path.exists():
        return {'absent': True}
    require(path.is_file() and not path.is_symlink(), 'Unexpected path type')
    body = path.read_bytes()
    return {'bytes': len(body), 'sha256': sha(body), 'mode': stat.S_IMODE(path.stat().st_mode)}

window_path = R / 'draft_pr_descending_audit_20261002/SHARED_GIT_WINDOW_STATUS.json'
window_body = window_path.read_bytes()

def window():
    row = read(window_path)
    require(window_path.read_bytes() == window_body and row.get('shared_git_writes_paused') is True and row.get('paused_for') == 'PR65 attributed prior-result integration 20261004' and row.get('dirty_tracked_bodies_modes_frozen_after_acknowledgement') is True and row.get('all_staged_path_count') == 0 and not row.get('owned_staged_paths') and row.get('local_main_at_pause') == row.get('remote_main_at_pause'), 'Fresh exclusive window not acknowledged')
    require(dt.datetime.fromisoformat(row['utc']) >= dt.datetime(2026, 10, 4, 15, 53, 43, tzinfo=dt.timezone.utc), 'Stale acknowledgement')
    return row

w = window()
require(run('branch', '--show-current').strip() == b'main' and not run('diff', '--cached', '--name-only', '-z'), 'Branch/index drift')
base = run('rev-parse', 'HEAD').decode().strip()
acceptance = read(A / 'native_attributed_result_operations_20261004/NATIVE_ACCEPTANCE_RESULT.json')
merge = read(A / 'native_attributed_result_operations_20261004/NATIVE_MERGE_RESULT.json')
require(base == acceptance['acceptance_commit'] == run('ls-remote', '--heads', 'origin', 'main').decode().split()[0] and merge['base'] == w['local_main_at_pause'], 'Main/remote/acknowledged merge chain drift')
require(read(A / 'ROOT_attributed_acceptance_readback_20261004/READBACK.json')['status'] == 'PASS', 'Independent acceptance readback absent')
progress = read(P / 'CURRENT_PROGRESS.json')
require(progress['current_PR'] == 65 and not progress['current_priority_clearance'] and not progress['current_publication_authorization'] and not progress['persistent_goal_complete'] and not progress['current_qualified_package_ready'] and progress['current_PR_workflow_percent'] == 95 and progress['current_audited_outcome'] == 'already_solved', 'Ready gate drift')
root_files = ['RESEARCH_LOG.md','ROOT_authenticate_provided_sources_20261004.py','ROOT_read_provided_sources_20261004.py','ROOT_prepare_provided_source_disposition_20261004.py','ROOT_adjudicate_provided_sources_20261004.py','ROOT_integrate_attributed_prior_result_20261004.py','ROOT_readback_attributed_acceptance_20261004.py','ROOT_commit_attributed_acceptance_checkpoint_20261004.py','ROOT_PUBLISHED_PR_BODY_20261004.md','ROOT_PROVIDED_SOURCE_FINAL_DISPOSITION_20261004.json','ROOT_PROVIDED_SOURCE_PRIORITY_ADJUDICATION_20261004.md','PUBLICATION_PACKAGE_V1_SUPERSEDED_20261004.json']
roots = [A / name for name in root_files] + [P / 'CURRENT_PROGRESS.json']
folders = ['provided_primary_sources_20261004','provided_source_mechanism_audit_20261004','provided_source_analytic_audit_20261004','provided_source_HL2019_status_audit_20261004','provided_priority_final_adversary_20261004','ROOT_provided_source_reading_20261004','attributed_prior_result_preparation_20261004','ROOT_provided_source_final_readback_20261004','ROOT_adjudication_stream_schema_recovery_20261004','native_attributed_result_operations_20261004','ROOT_attributed_acceptance_readback_20261004']
for name in folders:
    folder=A/name
    roots.extend(p for p in folder.rglob('*') if p.is_file() and p.suffix in {'.md','.json','.jsonl','.py','.sha256'})
captures=['root_pr65_provided_sources_intake_GitHub_head_20261004_actual_capture','root_pr65_provided_primary_PDF_authentication_20261004_actual_capture','root_pr65_provided_sources_ROOT_private_render_20261004_actual_capture','root_pr65_provided_sources_concrete_disposition_20261004_actual_capture','root_pr65_provided_sources_final_adjudication_20261004_actual_capture','root_pr65_provided_sources_final_adjudication_schema_recovery_20261004_actual_capture','root_pr65_attributed_native_merge_20261004_actual_capture','root_pr65_attributed_merge_GitHub_readback_20261004_actual_capture','root_pr65_attributed_native_mirror_20261004_actual_capture','root_pr65_attributed_PR_metadata_correction_20261004_actual_capture','root_pr65_attributed_acceptance_ROOT_readback_20261004_actual_capture']
for name in captures:
    folder=C/name
    require(read(folder/'CAPTURE.json')['status'] == ('FAIL' if name=='root_pr65_provided_sources_final_adjudication_20261004_actual_capture' else 'PASS'),'Unexpected actual capture status')
    roots.append(folder)
rel = [p.relative_to(R).as_posix() for p in roots]
selected = names(run('diff', '--name-only', '-z', '--', *rel)) | names(run('ls-files', '--others', '--exclude-standard', '-z', '--', *rel))
require(selected and all(any(name == root or name.startswith(root + '/') for root in rel) for name in selected), 'Scope mismatch')
blocked_parts = {'primary_sources', 'private_actual_git_commands', 'publication_package_v1', 'reviewable_note_v1', 'ROOT_priority_search_20261004', '__pycache__', 'disposable_package', 'pdf_render', 'rendered', 'compiled', 'before_package'}
require(all(not any(part in blocked_parts for part in Path(name).parts) and not name.endswith(('.pdf', '.png', '.pyc', '.tex', '.zip')) for name in selected), 'Private/manuscript/package scope violation')
foreign = {name: pin(name) for name in names(run('diff', '--name-only', '-z')) - selected}
owned = {name: pin(name) for name in sorted(selected)}
native = {name: pin(name) for name in ['unsolved_math_prioritization/QUEUE.md', 'unsolved_math_prioritization/state.json', 'unsolved_math_prioritization/history.jsonl']}
plan = {'UTC': dt.datetime.now(dt.timezone.utc).isoformat(), 'actual_controller_pid': os.getpid(), 'base': base, 'acknowledgement_sha256': sha(window_body), 'owned': owned, 'foreign': foreign, 'native_to_preserve': native, 'priority_clearance': False, 'publication': False, 'native_attributed_merge_already_verified': True, 'source_receipt_streams_and_copyrighted_sources_excluded': True, 'unpublished_package_excluded': True, 'selected_review_manifests_describe_the_full_local_audit_not_Git_inclusion': True}
plan_path = F / 'PLAN.json'
plan_path.write_text(json.dumps(plan, indent=2) + '\n')
plan_name = plan_path.relative_to(R).as_posix()
selected.add(plan_name)
owned[plan_name] = pin(plan_name)

def preserve():
    window()
    require(names(run('diff', '--name-only', '-z')) - selected == set(foreign), 'Foreign tracked-path set drift')
    for name, expected in {**foreign, **owned, **native}.items():
        require(pin(name) == expected, 'Body/mode drift: ' + name)

preserve()
run('add', '--', *sorted(selected))
require(names(run('diff', '--cached', '--name-only', '-z')) == selected, 'Staging scope mismatch')
for name, expected in owned.items():
    require(sha(run('show', ':' + name)) == expected['sha256'], 'Index byte mismatch')
preserve()
run('commit', '-m', 'Record PR65 supplied-source priority correction and verified attributed acceptance')
commit = run('rev-parse', 'HEAD').decode().strip()
require(run('show', '-s', '--format=%P', commit).decode().strip() == base and names(run('diff-tree', '--no-commit-id', '--name-only', '-r', '-z', commit)) == selected, 'Commit scope mismatch')
require(run('ls-remote', '--heads', 'origin', 'main').decode().split()[0] == base, 'Remote advanced')
preserve()
run('push', 'origin', 'main')
require(run('ls-remote', '--heads', 'origin', 'main').decode().split()[0] == commit and not run('diff', '--cached', '--name-only', '-z'), 'Push/index verification failed')
preserve()
receipt = {'UTC': dt.datetime.now(dt.timezone.utc).isoformat(), 'actual_controller_pid': os.getpid(), 'commit': commit, 'base': base, 'remote_main': commit, 'owned_path_count': len(selected), 'foreign_tracked_paths_preserved': len(foreign), 'index_empty': True, 'native_QUEUE_state_history_unchanged': True, 'current_PR_workflow_percent': 100, 'priority_clearance': False, 'PR65_publication_authorized': False, 'PR65_attributed_merge_complete': True, 'PR65_new_publication': False, 'publication_package_included': False, 'goal_complete': False, 'acceptance_commit': acceptance['acceptance_commit'], 'merge_commit': merge['merge_commit'], 'audited_outcome': 'already_solved', 'accepted_as': 'attributed_partial_prior_result', 'new_DOI': None, 'receipt_created_after_push_not_embedded_in_own_commit': True}
(F / 'RECEIPT.json').write_text(json.dumps(receipt, indent=2) + '\n')
print(json.dumps(receipt, indent=2))
