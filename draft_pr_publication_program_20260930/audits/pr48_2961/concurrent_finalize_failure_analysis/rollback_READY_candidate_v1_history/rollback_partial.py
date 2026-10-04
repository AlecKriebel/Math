"""UNEXECUTED ROOT-only exact selected rollback; never runs original helpers."""
from pathlib import Path, PurePosixPath
import argparse
import datetime as dt
import hashlib
import json
import os
import stat
import subprocess
import sys
import tempfile
import traceback
import uuid

P = Path(__file__).absolute().parent
A = P.parent
R = A.parents[2]
K = R / 'unsolved_math_prioritization/attempts/2961'
D = A / 'root_partial_finalize_v6_quarantine'
ADMIN = ['status.json', 'readiness.json', 'review/review_summary.json', 'review/verdict.json']
NEW_K = ['ACCEPTANCE.md', 'MANIFEST.json', 'acceptance.json']
NEW_A = ['acceptance.json', 'integration_finalization.json', 'remote_merge_receipt.json']
INVENTORY = 'draft_pr_publication_program_20260930/inventory.json'
COMMANDS = []
BASELINE = None

def need(value, message):
    if not value:
        raise ValueError(message)

def sha(body):
    return hashlib.sha256(body).hexdigest()

def safe(name):
    need(type(name) is str and name and '\\' not in name and '\0' not in name, 'Literal path')
    p = PurePosixPath(name)
    need(not p.is_absolute() and p.as_posix() == name and not {'.', '..', '.git', '__pycache__'}.intersection(p.parts), 'Canonical relative path')
    return name

def regular(path):
    need(path.is_file() and not path.is_symlink() and all(not q.is_symlink() for q in path.parents), 'Regular nonsymlink selected body')
    return path

def raw(path):
    regular(path)
    before = path.stat()
    with path.open('rb') as stream:
        opened = os.fstat(stream.fileno())
        body = stream.read()
        end = os.fstat(stream.fileno())
    after = path.stat()
    identity = lambda z: (z.st_dev, z.st_ino, z.st_mode, z.st_size, z.st_mtime_ns, z.st_ctime_ns)
    need(all(identity(z) == identity(before) for z in [opened, end, after]), 'Stable complete opened body/mode')
    return body

def ref(path):
    body = raw(path)
    return dict(path=safe(path.relative_to(R).as_posix()), bytes=len(body), sha256=sha(body), full_mode=stat.S_IMODE(path.stat().st_mode))

def checked(row):
    need(type(row) is dict and set(row) == {'path', 'bytes', 'sha256', 'full_mode'} and type(row['bytes']) is int and row['bytes'] >= 0 and type(row['full_mode']) is int and 0 <= row['full_mode'] <= 0o7777, 'Typed complete descriptor')
    need(ref(R / safe(row['path'])) == row, 'Exact full body/mode preimage')
    return raw(R / row['path'])

def parse(body):
    def pairs(items):
        value = {}
        for key, data in items:
            need(key not in value, 'Duplicate JSON key')
            value[key] = data
        return value
    return json.loads(body, object_pairs_hook=pairs, parse_constant=lambda x: (_ for _ in ()).throw(ValueError(x)))

def encode(value):
    return (json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + '\n').encode()

def put(path, body, mode=0o644):
    need(not path.exists() and not path.is_symlink() and all(not q.is_symlink() for q in path.parents), 'Absent regular output only')
    with path.open('xb') as stream:
        stream.write(body)
        os.fchmod(stream.fileno(), mode)
        stream.flush()
        os.fsync(stream.fileno())
    need(stat.S_IMODE(path.stat().st_mode) == mode and raw(path) == body, 'Whole output/mode readback')

def git(*args):
    argv = ['git', *args]
    allowed = ['rev-parse', 'branch', 'diff', 'show', 'ls-tree', 'merge-base']
    need(args and args[0] in allowed, 'Read-only literal Git command')
    env = dict(os.environ, GIT_OPTIONAL_LOCKS='0', GIT_LITERAL_PATHSPECS='1')
    for key in ['GIT_DIR', 'GIT_WORK_TREE', 'GIT_INDEX_FILE', 'GIT_OBJECT_DIRECTORY', 'GIT_ALTERNATE_OBJECT_DIRECTORIES']:
        env.pop(key, None)
    start = dt.datetime.now(dt.timezone.utc).isoformat()
    child = subprocess.Popen(argv, cwd=R, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
    out, err = child.communicate()
    COMMANDS.append(dict(argv=argv, cwd=str(R), pid=child.pid, started_utc=start, finished_utc=dt.datetime.now(dt.timezone.utc).isoformat(), exit_code=child.returncode, actual_execution=True, completed=True, stdout_utf8=out.decode(), stderr_utf8=err.decode(), stdout_bytes=len(out), stdout_sha256=sha(out), stderr_bytes=len(err), stderr_sha256=sha(err)))
    need(child.returncode == 0 and not err, 'Actual readonly command failure retained')
    return out

def index_ref():
    path = R / '.git/index'
    body = raw(path)
    return dict(absolute_path=str(path), bytes=len(body), sha256=sha(body), full_mode=stat.S_IMODE(path.stat().st_mode))

def dirty_domain():
    dirty = git('diff', '--name-only', '-z').decode().split('\0')[:-1]
    own = {INVENTORY} | {str((K / n).relative_to(R)) for n in ADMIN}
    return sorted(n for n in dirty if n not in own)

def fresh_outside_baseline():
    head = git('rev-parse', 'HEAD').decode().strip()
    index = index_ref()
    need(git('branch', '--show-current') == b'main\n' and git('diff', '--cached', '--name-only', '-z') == b'', 'Fresh actual main and clean cached index')
    git('merge-base', '--is-ancestor', plan['original_merge_commit'], head)
    prefix = str(K.relative_to(R)) + '/'
    need(git('ls-tree', '-r', '-z', plan['original_merge_commit'], '--', prefix) == git('ls-tree', '-r', '-z', head, '--', prefix), 'Entire original selected Git tree remains exact in current descendant')
    domain = dirty_domain()
    paths = sorted(set(domain) | {z['path'] for z in plan['foreign_rows']})
    rows = [ref(R / safe(name)) for name in paths]
    value = dict(schema='pr48-actual-runtime-outside-preservation-baseline/v1', utc=dt.datetime.now(dt.timezone.utc).isoformat(), actual_pid=os.getpid(), current_head=head, current_index=index, complete_current_foreign_dirty_paths=domain, protected_rows=rows, original_known_protected_paths=[z['path'] for z in plan['foreign_rows']], outside_scientific_claims_accepted=False, historical_foreign_live_equality_asserted=False)
    need(git('rev-parse', 'HEAD').decode().strip() == head and index_ref() == index and dirty_domain() == domain, 'Fresh outside baseline captured consistently under owned index lock')
    for row in rows:
        checked(row)
    return value

def environment():
    need(BASELINE is not None, 'Actual runtime baseline required')
    need(git('rev-parse', 'HEAD').decode().strip() == BASELINE['current_head'] and git('branch', '--show-current') == b'main\n', 'Exact actual runtime main HEAD')
    need(index_ref() == BASELINE['current_index'] and git('diff', '--cached', '--name-only', '-z') == b'', 'Whole exact runtime raw index and clean cached scope')
    need(dirty_domain() == BASELINE['complete_current_foreign_dirty_paths'], 'Complete exact current foreign tracked dirty domain')
    for row in plan['unrelated_native12'] + BASELINE['protected_rows'] + plan['owned_logs']:
        checked(row)

def canonical(expected):
    names = set(expected)
    seen = set()
    for q in K.rglob('*'):
        need(not q.is_symlink(), 'No canonical symlink')
        if q.is_file():
            seen.add(q.relative_to(K).as_posix())
        else:
            need(q.is_dir() and stat.S_IMODE(q.stat().st_mode) == 0o755, 'Regular canonical directory')
    need(seen == names and stat.S_IMODE(K.stat().st_mode) == 0o755, 'Exact whole canonical topology')
    directories = {q.relative_to(K).as_posix() for q in K.rglob('*') if q.is_dir()}
    wanted_dirs = {q.as_posix() for n in names for q in PurePosixPath(n).parents if q.as_posix() != '.'}
    need(directories == wanted_dirs, 'No extra empty canonical directory')
    for row in expected.values():
        checked(row)

def replace(path, before, body, mode):
    checked(before)
    fd, name = tempfile.mkstemp(prefix='.root-pr48-rollback-', dir=path.parent)
    temp = Path(name)
    try:
        with os.fdopen(fd, 'wb') as stream:
            stream.write(body)
            os.fchmod(stream.fileno(), mode)
            stream.flush()
            os.fsync(stream.fileno())
        checked(before)
        os.replace(temp, path)
        need(raw(path) == body and stat.S_IMODE(path.stat().st_mode) == mode, 'Exact selected replacement readback')
    finally:
        if temp.exists():
            temp.unlink()

def main():
    global plan, BASELINE
    parser = argparse.ArgumentParser()
    parser.add_argument('--execute', action='store_true')
    parser.add_argument('--personally-read-complete-source', action='store_true')
    parser.add_argument('--source-ready-sha256', required=True)
    args = parser.parse_args()
    need(args.execute and args.personally_read_complete_source and __debug__ and P.name == 'partial_finalize_v6_rollback_preparation', 'ROOT explicit complete source reading')
    os.umask(0o022)
    ready_body = raw(P / 'SOURCE_READY.json')
    need(sha(ready_body) == args.source_ready_sha256, 'Exact prepared SOURCE readiness')
    ready = parse(ready_body)
    need(ready['source_only'] is True and ready['production_executed'] is False, 'SOURCE preparation has no actual execution authority')
    for row in ready['source_rows_except_READY']:
        checked(row)
    source_before = ref(Path(__file__))
    need(source_before['full_mode'] == 0o644 and stat.S_IMODE(P.stat().st_mode) == 0o755, 'Unclosed prepared source full0644/0755 at actual ROOT run')
    plan = parse(raw(P / 'PLAN.json'))
    need(plan['schema'] == 'pr48-exact-partial-V6-rollback-plan/v1' and plan['actual_restore_performed'] is False, 'Literal prospective plan')
    BASELINE = fresh_outside_baseline()
    put(A / 'root_partial_finalize_v6_rollback_lock_evidence/CURRENT_OUTSIDE_BASELINE.json', encode(BASELINE))
    for row in plan['fixed_failed_evidence']:
        checked(row)
    for directory, pid in [('root_finalize_foreign_epoch_v6_phase_capture', 80414), ('root_finalize_actual_capture', 80480)]:
        capture = parse(raw(A / directory / 'CAPTURE.json'))
        need(type(capture['pid']) is int and capture['pid'] == pid and capture['actual_execution'] is True and capture['completed'] is True and type(capture['exit_code']) is int and capture['exit_code'] == 1 and capture['status'] == 'FAIL', 'Genuine actual failed V6 operator/adapter remains failure')
        for stream in ['stdout', 'stderr']:
            body = raw(A / directory / (stream + '.bin'))
            need(capture[stream] == dict(path=stream + '.bin', bytes=len(body), sha256=sha(body)), 'Complete actual failed streams authenticated')
    for row in plan['fixed_directory_modes']:
        q = R / safe(row['path'])
        need(q.is_dir() and not q.is_symlink() and all(not a.is_symlink() for a in q.parents) and stat.S_IMODE(q.stat().st_mode) == row['full_mode'], 'Exact preserved evidence directory fullmode')
    need(not D.exists() and not D.is_symlink(), 'Distinct absent quarantine, no blind retry')
    need(not (A / 'ROOT_PARTIAL_FINALIZE_V6_ROLLBACK_RECEIPT.json').exists(), 'Absent ROOT rollback output')
    exact_paths = sorted([INVENTORY] + [str((K / n).relative_to(R)) for n in ADMIN + NEW_K] + [str((A / n).relative_to(R)) for n in NEW_A])
    need(len(exact_paths) == 11 and [z['path'] for z in plan['partial11']] == exact_paths, 'Exact eleven literal owned changed/new paths')
    partial = {z['path']: z for z in plan['partial11']}
    for path, row in partial.items():
        need(row['full_mode'] == (0o444 if path.startswith(str(K.relative_to(R)) + '/') else 0o644), 'Every exact partial role fullmode')
    manifest = parse(checked(plan['partial_manifest']))
    need(manifest['schema'] == 'pr48-accepted-strict-self-excluding-closure/v1' and manifest['self_excluded'] == ['MANIFEST.json'] and type(manifest['files_count']) is int and manifest['files_count'] == len(manifest['files']) == 1957, 'Entire typed partial accepted manifest')
    expected = {z['path']: dict(path=str((K / safe(z['path'])).relative_to(R)), bytes=z['bytes'], sha256=z['sha256'], full_mode=0o444) for z in manifest['files']}
    need(len(expected) == 1957 and 'MANIFEST.json' not in expected, 'Distinct self-excluding canonical domain')
    expected['MANIFEST.json'] = plan['partial_manifest']
    overlay = parse(checked(plan['original_overlay']))['canonical_overlay_files']
    need(len(overlay) == 1955 and len({z['path'] for z in overlay}) == 1955 and set(expected) == {z['path'] for z in overlay} | set(NEW_K), 'Exact original1955 plus new3 topology')
    original = {z['path']: z for z in overlay}
    for name in set(original) - set(ADMIN):
        need(all(expected[name][key] == original[name][key] for key in ['bytes', 'sha256']), 'All other1951 canonical bodies match original overlay')
    need(len(plan['unrelated_native12']) == 12 and len(plan['foreign_rows']) == 7 and len(plan['owned_logs']) == 2, 'Exact unrelated envelopes')
    inventory_body = checked(plan['inventory_original'])
    need(sha(inventory_body) == '171061fc88b5ca06e200cc2cead9d11fe1e7435f8f98435907937bdc0f9df0d8', 'Exact original inventory preimage')
    restored_admin = {}
    for name in ADMIN:
        path = str((K / name).relative_to(R))
        entry = git('ls-tree', '-z', plan['original_merge_commit'], '--', path)
        need(entry.split(b'\t')[0].split()[0:2] == [b'100644', b'blob'], 'Original merge regular administration blob mode')
        body = git('show', plan['original_merge_commit'] + ':' + path)
        need(len(body) == original[name]['bytes'] and sha(body) == original[name]['sha256'], 'Exact original merge administration body bound to original overlay')
        restored_admin[name] = body
    environment()
    canonical(expected)
    for row in plan['partial11']:
        checked(row)
    D.mkdir(mode=0o755)
    retained = []
    operations = []
    try:
        for row in plan['partial11']:
            destination = D / 'bodies' / row['path']
            destination.parent.mkdir(parents=True, exist_ok=True)
            put(destination, checked(row), row['full_mode'])
            retained.append(dict(original=row, retained=ref(destination)))
        need(len(retained) == 11, 'Every changed/new body quarantined before any mutation')
        environment()
        canonical(expected)
        put(D / 'QUARANTINE_RECEIPT.json', encode(dict(schema='pr48-genuine-partial-V6-pre-mutation-quarantine/v1', utc=dt.datetime.now(dt.timezone.utc).isoformat(), actual_pid=os.getpid(), retained_count=11, retained=retained, source=source_before, plan=ref(P / 'PLAN.json'), original_failure_remains_FAIL=True, actual_mutation_started=False, canonical_preimage_count=1958, canonical_preimage_manifest=plan['partial_manifest'], runtime_outside_baseline=ref(A / 'root_partial_finalize_v6_rollback_lock_evidence/CURRENT_OUTSIDE_BASELINE.json'), current_head=BASELINE['current_head'], current_index=BASELINE['current_index'])))
        # Four exact known old blobs and original inventory; selected path CAS at each write.
        environment()
        for name in ADMIN:
            path = K / name
            before = partial[str(path.relative_to(R))]
            replace(path, before, restored_admin[name], 0o644)
            expected[name] = ref(path)
            operations.append(dict(operation='restore_exact_original_ADMIN', after=ref(path)))
        environment()
        replace(R / INVENTORY, partial[INVENTORY], inventory_body, 0o644)
        operations.append(dict(operation='restore_exact_inventory', after=ref(R / INVENTORY)))
        environment()
        for name in NEW_K:
            path = K / name
            checked(partial[str(path.relative_to(R))])
            path.unlink()
            expected.pop(name)
            operations.append(dict(operation='remove_quarantined_new_canonical', path=str(path.relative_to(R))))
        for name in NEW_A:
            path = A / name
            checked(partial[str(path.relative_to(R))])
            path.unlink()
            operations.append(dict(operation='remove_quarantined_new_A_receipt', path=str(path.relative_to(R))))
        environment()
        canonical(expected)
        need(len(expected) == 1955 and ref(R / INVENTORY) == dict(path=INVENTORY, bytes=len(inventory_body), sha256=sha(inventory_body), full_mode=0o644), 'Exact final pending selected footprint')
        need(ref(Path(__file__)) == source_before, 'Actual ROOT source unchanged')
        for row in retained:
            checked(row['retained'])
        for row in plan['fixed_failed_evidence']:
            checked(row)
        put(D / 'COMMANDS.json', encode(COMMANDS))
        receipt = dict(schema='pr48-genuine-exact-partial-V6-rollback/v1', status='PASS_EXACT_SELECTED_ROLLBACK_ONLY', actual_execution=True, actual_pid=os.getpid(), utc=dt.datetime.now(dt.timezone.utc).isoformat(), source=source_before, plan=ref(P / 'PLAN.json'), quarantine_receipt=ref(D / 'QUARANTINE_RECEIPT.json'), complete_operations=operations, retained_count=11, original_failed_capture_rewritten=False, other1951_canonical_bodies_unchanged_and_full0444=True, restored4_ADMIN_full0644=True, inventory_restored_exact=True, original1955_pending_topology_restored=True, current_head=BASELINE['current_head'], current_index=BASELINE['current_index'], runtime_outside_baseline=ref(A / 'root_partial_finalize_v6_rollback_lock_evidence/CURRENT_OUTSIDE_BASELINE.json'), complete_current_outside_rows=BASELINE['protected_rows'], unrelated_native12=plan['unrelated_native12'], original_known_protected_paths=[z['path'] for z in plan['foreign_rows']], owned_logs=plan['owned_logs'], readonly_commands=ref(D / 'COMMANDS.json'), Git_index_body_or_ref_or_staging_mutated=False, V7_execution_or_acceptance_approved=False)
        environment()
        canonical(expected)
        return receipt
    except BaseException:
        failure = dict(schema='pr48-real-partial-V6-rollback-failure/v1', utc=dt.datetime.now(dt.timezone.utc).isoformat(), actual_pid=os.getpid(), status='FAIL_PARTIAL_RECOVERY_REQUIRES_ROOT_INSPECTION', completed_selected_operations=operations, error=traceback.format_exc(), original_failure_rewritten=False, V7_execution_or_acceptance_approved=False)
        if not (D / 'COMMANDS.json').exists():
            put(D / 'COMMANDS.json', encode(COMMANDS))
        put(D / 'FAILURE.json', encode(failure))
        raise

def entry():
    # Standard exclusive coordination lock only. No index body, ref or staging write.
    need('--execute' in sys.argv and '--personally-read-complete-source' in sys.argv and __debug__, 'ROOT explicit source reading before coordination lock')
    position = sys.argv.index('--source-ready-sha256')
    need(position + 1 < len(sys.argv) and sha(raw(P / 'SOURCE_READY.json')) == sys.argv[position + 1], 'Exact SOURCE pin before metadata creation')
    need(P.name == 'partial_finalize_v6_rollback_preparation' and stat.S_IMODE(Path(__file__).stat().st_mode) == 0o644, 'Exact unclosed prepared helper mode')
    directory = A / 'root_partial_finalize_v6_rollback_lock_evidence'
    need(not directory.exists() and not directory.is_symlink(), 'Absent distinct coordination evidence directory')
    os.umask(0o022)
    directory.mkdir(mode=0o755)
    source = raw(Path(__file__))
    put(directory / 'PRELAUNCH_SOURCE.py', source)
    put(directory / 'PRELAUNCH.json', encode(dict(schema='pr48-actual-rollback-lock-prelaunch/v1', actual_pid=os.getpid(), utc=dt.datetime.now(dt.timezone.utc).isoformat(), argv=sys.argv, cwd=str(R), source_sha256=sha(source), source_ready_sha256=sys.argv[position + 1], Git_coordination_metadata_mutation_requested=True, native_execution_not_yet_started=True)))
    lock = R / '.git/index.lock'
    need(lock.parent.is_dir() and not lock.parent.is_symlink() and all(not q.is_symlink() for q in lock.parents), 'Canonical Git metadata directory')
    token = encode(dict(schema='pr48-exclusive-index-coordination-lock/v1', repository=str(R), actual_owner_pid=os.getpid(), utc=dt.datetime.now(dt.timezone.utc).isoformat(), nonce=str(uuid.uuid4()), source_sha256=sha(source), source_ready_sha256=sys.argv[position + 1]))
    put(directory / 'PROPOSED_LOCK_BODY.bin', token)
    owned = None
    exclusive_create_returned = False
    written = 0
    result = None
    error = None
    release = None
    try:
        fd = os.open(lock, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        exclusive_create_returned = True
        try:
            created = os.fstat(fd)
            owned = (created.st_dev, created.st_ino)
            need(stat.S_IMODE(created.st_mode) == 0o600 and created.st_nlink == 1, 'Exact own new coordination inode/mode')
            while written < len(token):
                amount = os.write(fd, token[written:])
                need(amount > 0, 'Lock write progress')
                written += amount
            os.fsync(fd)
        finally:
            os.close(fd)
        need(raw(lock) == token and (lock.stat().st_dev, lock.stat().st_ino) == owned, 'Complete own coordination body/identity')
        put(directory / 'LOCK_OWNERSHIP.json', encode(dict(schema='pr48-actual-owned-index-coordination-lock/v1', actual_pid=os.getpid(), utc=dt.datetime.now(dt.timezone.utc).isoformat(), path=str(lock), device=owned[0], inode=owned[1], full_mode=0o600, body_bytes=len(token), body_sha256=sha(token), body=ref(directory / 'PROPOSED_LOCK_BODY.bin'), exclusive_creation_completed=True)))
        # All current HEAD/index baseline reads in main occur after exclusive acquisition.
        result = main()
    except BaseException:
        error = traceback.format_exc()
    finally:
        if owned is None:
            release = dict(released=False, exclusive_create_returned=exclusive_create_returned, ownership_identity_obtained=False, unproved_or_existing_lock_not_removed=True)
        else:
            try:
                q = lock.lstat()
                need(stat.S_ISREG(q.st_mode) and not lock.is_symlink() and q.st_nlink == 1 and (q.st_dev, q.st_ino) == owned and stat.S_IMODE(q.st_mode) == 0o600 and raw(lock) == token[:written], 'Only exact owned inode/fullmode/known written content may be released')
                q = lock.lstat()
                need(stat.S_ISREG(q.st_mode) and q.st_nlink == 1 and (q.st_dev, q.st_ino) == owned and stat.S_IMODE(q.st_mode) == 0o600, 'Path inode/mode still exact after complete release-body read')
                release = dict(released=True, own_lock_created=True, device=owned[0], inode=owned[1], full_mode=0o600, body_bytes=written, body_sha256=sha(token[:written]), complete_body_written=written == len(token), utc=dt.datetime.now(dt.timezone.utc).isoformat())
                lock.unlink()
            except BaseException:
                release = dict(released=False, own_lock_created=True, foreign_or_altered_lock_not_removed=True, error=traceback.format_exc())
                error = (error or '') + release['error']
        put(directory / 'LOCK_RELEASE_RECEIPT.json', encode(release))
    if error is not None:
        put(directory / 'RUN_FAILURE.json', encode(dict(schema='pr48-actual-rollback-and-lock-failure/v1', actual_pid=os.getpid(), utc=dt.datetime.now(dt.timezone.utc).isoformat(), error=error, lock_release=release, index_body_or_ref_or_staging_written=False, native_restore_success_claimed=False)))
        raise ValueError('Actual rollback/lock failure retained; ROOT inspection required: ' + error)
    need(result is not None and release['released'] is True and ref(Path(__file__))['sha256'] == sha(source), 'Actual rollback and exact owned-lock release completed')
    result.update(coordination_lock_metadata_created_and_removed=True, lock_ownership=ref(directory / 'LOCK_OWNERSHIP.json'), lock_release=ref(directory / 'LOCK_RELEASE_RECEIPT.json'), source_prelaunch=ref(directory / 'PRELAUNCH_SOURCE.py'), index_identity_interval='entire owned-lock critical section; no promise about later background refresh')
    put(A / 'ROOT_PARTIAL_FINALIZE_V6_ROLLBACK_RECEIPT.json', encode(result))
    print(json.dumps(dict(status=result['status'], receipt=ref(A / 'ROOT_PARTIAL_FINALIZE_V6_ROLLBACK_RECEIPT.json'), quarantine_count=11, own_coordination_lock_released=True, V7_execution_or_acceptance_approved=False)))

if __name__ == '__main__':
    entry()
