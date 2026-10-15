"""Own readonly SOURCE/pin author; never imports or runs proposed rollback."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import os
import stat
import subprocess

P = Path(__file__).absolute().parent
A = P.parent
R = A.parents[2]
K = R / 'unsolved_math_prioritization/attempts/2961'
MERGE = '209581a4627b01745974837fe7adab62ab8c0af7'
ADMIN = ['status.json', 'readiness.json', 'review/review_summary.json', 'review/verdict.json']
NEW_K = ['ACCEPTANCE.md', 'MANIFEST.json', 'acceptance.json']
NEW_A = ['acceptance.json', 'integration_finalization.json', 'remote_merge_receipt.json']
INV = 'draft_pr_publication_program_20260930/inventory.json'
reads = []

def need(value, message):
    if not value:
        raise ValueError(message)

def sha(body):
    return hashlib.sha256(body).hexdigest()

def raw(path):
    need(path.is_file() and not path.is_symlink() and all(not q.is_symlink() for q in path.parents), 'Regular selected source/input')
    before = path.stat()
    body = path.read_bytes()
    after = path.stat()
    need((before.st_dev, before.st_ino, before.st_mode, before.st_size, before.st_mtime_ns, before.st_ctime_ns) == (after.st_dev, after.st_ino, after.st_mode, after.st_size, after.st_mtime_ns, after.st_ctime_ns), 'Stable full read')
    return body

def ref(path):
    b = raw(path)
    return dict(path=path.relative_to(R).as_posix(), bytes=len(b), sha256=sha(b), full_mode=stat.S_IMODE(path.stat().st_mode))

def load(path):
    return json.loads(raw(path))

def put(name, value):
    body = value.encode() if type(value) is str else (json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + '\n').encode()
    with (P / name).open('xb') as stream:
        stream.write(body)

def normalized(row):
    return dict(path=row['path'], bytes=row['bytes'], sha256=row['sha256'], full_mode=row['worktree_mode'])

def git(*args):
    argv = ['git', *args]
    env = dict(os.environ, GIT_OPTIONAL_LOCKS='0', GIT_LITERAL_PATHSPECS='1')
    for n in ['GIT_DIR', 'GIT_WORK_TREE', 'GIT_INDEX_FILE', 'GIT_OBJECT_DIRECTORY', 'GIT_ALTERNATE_OBJECT_DIRECTORIES']:
        env.pop(n, None)
    started = dt.datetime.now(dt.timezone.utc).isoformat()
    child = subprocess.Popen(argv, cwd=R, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
    out, err = child.communicate()
    reads.append(dict(argv=argv, pid=child.pid, started_utc=started, finished_utc=dt.datetime.now(dt.timezone.utc).isoformat(), exit_code=child.returncode, entire_stdout_utf8=out.decode(), entire_stderr_utf8=err.decode(), stdout_bytes=len(out), stdout_sha256=sha(out), stderr_bytes=len(err), stderr_sha256=sha(err), actual_readonly_child=True))
    need(child.returncode == 0 and not err, 'Actual readonly source observation failure')
    return out

footprint_path = A / 'selected_partial_rollback_adversary_family/ACTUAL_FOOTPRINT.json'
footprint = load(footprint_path)
need(footprint['read_only'] is True and footprint['ROOT_approval_claimed'] is False and footprint['canonical_total_files'] == 1958 and footprint['changed_existing_admin_count'] == 4, 'Genuine independent readonly footprint, not SOURCE approval')
head = git('rev-parse', 'HEAD').decode().strip()
need(head == footprint['current_HEAD'] and git('branch', '--show-current') == b'main\n', 'Actual current main baseline separate from historical failure')
index = R / '.git/index'
indexbody = raw(index)
indexrow = dict(absolute_path=str(index), bytes=len(indexbody), sha256=sha(indexbody), full_mode=stat.S_IMODE(index.stat().st_mode))
need(indexrow == {**{k:footprint['current_real_index_after'][k] for k in ['bytes', 'sha256']}, 'absolute_path':str(index), 'full_mode':footprint['current_real_index_after']['worktree_mode']}, 'Actual fresh whole index matches independent dated snapshot')
need(git('diff', '--cached', '--name-only', '-z') == b'', 'Actual cached index clean')
dated_foreign = sorted([normalized(z['actual']) for z in footprint['protected_foreign7']], key=lambda z:z['path'])
foreign = sorted([ref(R / z['path']) for z in dated_foreign], key=lambda z:z['path'])
need(all(z['full_mode'] == old['full_mode'] == 0o644 for z, old in zip(foreign, dated_foreign)), 'Same exact seven authorized regular paths; fresh bodies retain exact full modes')
native = sorted([normalized(z['actual']) for z in footprint['protected_native12']], key=lambda z:z['path'])
logs = sorted([normalized(z['actual']) for z in footprint['protected_owned_logs2']], key=lambda z:z['path'])
for row in foreign + native + logs:
    need(ref(R / row['path']) == row, 'Whole current body/fullmode protection verified directly')
own = {INV} | {str((K / n).relative_to(R)) for n in ADMIN}
dirty = sorted(n for n in git('diff', '--name-only', '-z').decode().split('\0')[:-1] if n not in own)
need(set(dirty) <= {z['path'] for z in foreign}, 'No unlisted current tracked foreign dirt')
overlay_path = A / 'integration_check.json'
overlay = load(overlay_path)['canonical_overlay_files']
need(len(overlay) == len({z['path'] for z in overlay}) == 1955, 'Exact original1955 overlay')
manifest_path = K / 'MANIFEST.json'
manifest = load(manifest_path)
need(manifest['files_count'] == len(manifest['files']) == 1957 and manifest['self_excluded'] == ['MANIFEST.json'], 'Actual partial strict1957+self')
expected = {z['path']: z for z in manifest['files']}
need(len(expected) == 1957 and {q.relative_to(K).as_posix() for q in K.rglob('*') if q.is_file()} == set(expected) | {'MANIFEST.json'}, 'Full exact current canonical1958 topology')
need(all(not q.is_symlink() and (q.is_file() or q.is_dir()) and stat.S_IMODE(q.stat().st_mode) == (0o444 if q.is_file() else 0o755) for q in K.rglob('*')), 'Full complete current canonical modes')
for name, row in expected.items():
    b = raw(K / name)
    need(len(b) == row['bytes'] and sha(b) == row['sha256'], 'Every complete current canonical body')
original = {z['path']: z for z in overlay}
for name in set(original) - set(ADMIN):
    need(expected[name] == original[name], 'All1951 unchanged original canonical bodies')
for name in ADMIN:
    body = git('show', MERGE + ':' + str((K / name).relative_to(R)))
    need(len(body) == original[name]['bytes'] and sha(body) == original[name]['sha256'], 'Whole actual original merge blob equals overlay')
paths = sorted([INV] + [str((K / n).relative_to(R)) for n in ADMIN + NEW_K] + [str((A / n).relative_to(R)) for n in NEW_A])
need(len(paths) == 11 and len(set(paths)) == 11, 'Exact literal eleven owned partial paths')
partial = [ref(R / n) for n in paths]
fixed = {}
fixed_dirs = []
for n in ['root_finalize_foreign_epoch_v6_phase_capture', 'root_finalize_actual_capture', 'root_finalize_foreign_epoch_v6_author_capture', 'root_finalize_foreign_epoch_v6_readonly']:
    d = A / n
    fixed_dirs.append(dict(path=d.relative_to(R).as_posix(), full_mode=stat.S_IMODE(d.stat().st_mode)))
    for q in d.rglob('*'):
        if q.is_file():
            fixed[ref(q)['path']] = ref(q)
        elif q.is_dir():
            fixed_dirs.append(dict(path=q.relative_to(R).as_posix(), full_mode=stat.S_IMODE(q.stat().st_mode)))
for q in [A / 'ROOT_POST_PUSH_V6_FINALIZE_FOREIGN_EPOCH.json', A / 'post_push_foreign_epoch_preparation_v6/SOURCE_READY.json', A / 'post_push_foreign_epoch_preparation_v6/SOURCE_MANIFEST.json', A / 'corrective_source_adversary_v6/SELF_MANIFEST.json', A / 'integration_inventory_before.json', overlay_path]:
    fixed[ref(q)['path']] = ref(q)
original_inventory = ref(A / 'integration_inventory_before.json')
need(original_inventory['sha256'] == '171061fc88b5ca06e200cc2cead9d11fe1e7435f8f98435907937bdc0f9df0d8', 'Exact source inventory preimage')
need(raw(index) == indexbody and git('rev-parse', 'HEAD').decode().strip() == head, 'Actual source observation HEAD/index stable')
for row in foreign + native + logs:
    need(ref(R / row['path']) == row, 'Current full protection remains exact through SOURCE binding')
plan = dict(schema='pr48-exact-partial-V6-rollback-plan/v1', utc=dt.datetime.now(dt.timezone.utc).isoformat(), SOURCE_author_actual_pid=os.getpid(), actual_restore_performed=False, original_merge_commit=MERGE, historical_failed_epoch_HEAD=footprint['historical_failed_HEAD'], historical_failed_epoch_index=footprint['historical_failed_capture_index_before'], index_drift_causation_established=False, current_head=head, current_index=indexrow, partial11=partial, partial_manifest=ref(manifest_path), original_overlay=ref(overlay_path), inventory_original=original_inventory, unrelated_native12=native, foreign_rows=foreign, earlier_dated_independent_foreign_rows=dated_foreign, current_foreign_dirty_paths=dirty, owned_logs=logs, fixed_failed_evidence=[fixed[n] for n in sorted(fixed)], fixed_directory_modes=sorted(fixed_dirs, key=lambda z:z['path']), source_observation_from_independent_footprint=ref(footprint_path), no_historical_native_or_foreign_snapshot_promoted_to_current=True, quarantine_count=11, other1951_canonical_full_mode_after=0o444, restored4_ADMIN_full_mode_after=0o644, Git_coordination_index_lock_metadata_create_and_remove_planned=True, actual_Git_index_body_ref_or_staging_write_planned=False, V7_SOURCE_or_acceptance_approved=False)
put('PLAN.json', plan)
put('SOURCE_READS.json', dict(schema='pr48-rollback-preparer-actual-readonly-source-observations/v1', actual_own_source_author_pid=os.getpid(), utc=dt.datetime.now(dt.timezone.utc).isoformat(), complete_readonly_commands=reads, native_body_corpus_copied=False, complete_canonical1958_bodies_read_in_place=True, actual_index_whole_body_consumed_in_memory_not_retained=True, index=indexrow, ROOT_approval_claimed=False, proposed_rollback_import_compile_execute=False))
names = sorted([q.name for q in P.iterdir() if q.is_file()] + ['SOURCE_READY.json'])
need(len(names) == len(set(names)) and all(not q.is_symlink() and q.is_file() and stat.S_IMODE(q.stat().st_mode) == 0o644 for q in P.iterdir()), 'Own flat prepared SOURCE topology')
ready = dict(schema='pr48-partial-V6-rollback-SOURCE-readiness/v1', status='READY_SOURCE_ONLY_WAIT_INDEPENDENT_AND_ROOT_REVIEW', source_only=True, utc=dt.datetime.now(dt.timezone.utc).isoformat(), production_executed=False, actual_restore_performed=False, mathematical_credit=0, source_preparation_percent=100, actual_recovery_percent=0, payload_count=len(names), payload_names=names, source_rows_except_READY=[ref(P / n) for n in names if n != 'SOURCE_READY.json'], helper=ref(P / 'rollback_partial.py'), plan=ref(P / 'PLAN.json'), strict_prepared_helper_full_mode_at_ROOT_RUN=0o644, source_closure_claimed=False, Git_coordination_lock_metadata_planned=True, Git_index_body_ref_or_staging_mutation_planned=False, independent_adversarial_SOURCE_verdict=None, future_actual_ROOT_restore_capture=None, future_actual_ROOT_restore_receipt=None, future_V7_SOURCE=None)
put('SOURCE_READY.json', ready)
print(json.dumps(dict(status=ready['status'], actual_own_source_author_pid=os.getpid(), READY=ref(P / 'SOURCE_READY.json'), helper=ref(P / 'rollback_partial.py'), plan=ref(P / 'PLAN.json'), current_head=head, current_index=indexrow, payload_count=len(names), native_mutation=False, rollback_execution=False)))
