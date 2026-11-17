"""Single authorized helper invocation; preserve literal streams and native index."""
import datetime, hashlib, json, os, signal, subprocess, sys, time
from pathlib import Path

if not __debug__:
    raise RuntimeError('Checkpoint guards require Python assertions enabled')

P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
OWN = P/'verification/checkpoint-haf-retract-publish-graminitial-20261117'
HELPER = P/'scripts/checkpoint_subtree.py'
EXPECTED_PARENT = '15482acd0ef864af280a864758b2ac6aa24dfbe8'
assert sys.argv[1:] in (['dry-run'], ['push'])
mode = sys.argv[1]
name = 'DRY_RUN' if mode == 'dry-run' else 'PUSH'
release = json.loads((OWN/'WRITEHOLD_RELEASE.json').read_bytes())
assert release['authorization'] == 'WRITEHOLD_RELEASE_TO_CHECKPOINT'
assert release['expected_parent'] == EXPECTED_PARENT
before = HELPER.read_bytes()
pin = dict(bytes=len(before), SHA256=hashlib.sha256(before).hexdigest(), lines=len(before.splitlines()))
assert pin == dict(bytes=6213, SHA256='405b0357fd20a2e14893ce6c3c1a0f81910894ccd8ffaddac4e25014138fb9c0', lines=94)
guard = json.loads((OWN/'GUARDS_BEFORE.json').read_bytes())
assert pin['SHA256'] == guard['helper']['SHA256']
assert HELPER.read_bytes() == before
active, excludes = [], []
candidates = release['authorized_active_verification_paths'] + ['verification/'+OWN.name]
assert len(candidates) == len(set(candidates))
for relative in candidates:
    rel = Path(relative)
    assert not rel.is_absolute() and '..' not in rel.parts and relative.startswith('verification/')
    path = P/rel
    exists = os.path.lexists(path)
    regular = path.is_dir() and not path.is_symlink() if exists else False
    active.append(dict(path=relative, exists=exists, regular_directory=regular))
    if exists:
        assert regular and path.resolve().is_relative_to(P)
        excludes.append(relative)
assert 'verification/'+OWN.name in excludes
assert all(x.startswith('verification/') for x in excludes)
argv = [sys.executable, '-B', str(HELPER)]
if mode == 'dry-run':
    argv.append('--dry-run')
else:
    adoption = json.loads((OWN/'DRY_REVIEW.json').read_bytes())
    assert adoption['status'] == 'APPROVED_FOR_ORDINARY_SCOPED_PUSH'
    assert adoption['expected_parent'] == EXPECTED_PARENT
    assert adoption['dry_run_exit'] == 0 and adoption['dry_audit_exit'] == 0
    assert adoption['current_programme_write_hold_asserted'] is True
    assert HELPER.read_bytes() == before
    argv.append('Checkpoint published hafnian retract, review 141 receipts and Gram initial independent evidence')
argv += ['--exclude-path='+p for p in excludes]
env = dict(os.environ, PATH=str(OWN)+':/usr/bin:/bin:/usr/sbin:/sbin', CHECKPOINT_ADAPTER_MODE=mode, PYTHONOPTIMIZE='0', GIT_OPTIONAL_LOCKS='0', GIT_CONFIG_COUNT='2', GIT_CONFIG_KEY_0='core.hooksPath', GIT_CONFIG_VALUE_0='/dev/null', GIT_CONFIG_KEY_1='core.fsmonitor', GIT_CONFIG_VALUE_1='false')
for key in ('GIT_DIR','GIT_WORK_TREE','GIT_INDEX_FILE','GIT_COMMON_DIR','GIT_OBJECT_DIRECTORY','GIT_ALTERNATE_OBJECT_DIRECTORIES'):
    env.pop(key, None)
started = datetime.datetime.now(datetime.timezone.utc).isoformat()
tick = time.monotonic()
timed_out = False
with (OWN/(name+'.stdout')).open('xb') as out, (OWN/(name+'.stderr')).open('xb') as err:
    process = subprocess.Popen(argv, cwd=P, env=env, stdout=out, stderr=err, start_new_session=True)
    try:
        process.wait(timeout=300)
    except subprocess.TimeoutExpired:
        timed_out = True
        try:
            os.killpg(process.pid, signal.SIGTERM)
        except ProcessLookupError:
            pass
        try:
            process.wait(timeout=3)
        except subprocess.TimeoutExpired:
            pass
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        process.wait()
    completed = process
receipt = dict(schema='one-scoped-checkpoint-helper-invocation-v2', mode=mode, argv=argv, cwd=str(P), started_UTC=started, finished_UTC=datetime.datetime.now(datetime.timezone.utc).isoformat(), elapsed_seconds=time.monotonic()-tick, exit_code=completed.returncode, timed_out=timed_out, automatic_retry_forbidden=True, stdout_bytes=(OWN/(name+'.stdout')).stat().st_size, stderr_bytes=(OWN/(name+'.stderr')).stat().st_size, helper=pin, helper_unchanged=HELPER.read_bytes()==before, helper_full_source_personally_read=True, active_exclusions_discovered_immediately_before_invocation=active, excluded_actual_directories=excludes, internal_isolated_index=True, external_GIT_DIR_override=False, ordinary_nonforce_push_only=mode=='push', protected_native_boundary='Whole HEAD/index/config/config.worktree and logical/loose local heads; complete W/public bytes/modes/topology; FETCH_HEAD, remote-tracking refs and object additions allowed')
with (OWN/(name+'.invocation.json')).open('x') as stream:
    json.dump(receipt, stream, indent=2)
    stream.write('\n')
assert HELPER.read_bytes() == before
if completed.returncode == 0 and not timed_out:
    source = P/'verification'/('checkpoint-subtree-dry-run-20261025.json' if mode=='dry-run' else 'PUSH_RECEIPT.json')
    with (OWN/(name+'.receipt.json')).open('xb') as stream:
        stream.write(source.read_bytes())
    actual = json.loads(source.read_bytes())
    assert actual['parent'] == EXPECTED_PARENT and actual['dry_run'] == (mode=='dry-run')
    assert actual['sibling_root_entries_preserved'] == 159
    assert actual['active_packet_subtrees_left_at_parent'] == excludes
    assert actual['shared_index_sha256_before_and_after'] == '91b10d938f7d737226662bbff3b07016dcc0e501376a045811ab4e930c6fbb11'
print(json.dumps(receipt))
raise SystemExit(124 if timed_out else completed.returncode)
