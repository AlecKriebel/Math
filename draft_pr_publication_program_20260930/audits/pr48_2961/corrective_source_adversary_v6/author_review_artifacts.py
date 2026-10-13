"""Own artifact author. Only reads fixed sources/evidence; no candidate loading."""
from pathlib import Path, PurePosixPath
import datetime as dt
import hashlib
import json
import os
import stat

F = Path(__file__).absolute().parent
A = F.parent
R = F.parents[3]
P = A / 'post_push_foreign_epoch_preparation_v6'
OLD = A / 'corrective_source_adversary_v5'
M5 = A / 'corrective_source_adversary_v5_m5_addendum'
CAPROOT = A.parent / 'pr45_9900007'
READY = 'c41aa5d82d4b6240ea496b180d6b73fbff09d02574942c4741cadd5c80b19e26'
MF = 'aea1b2933d03cc7c20bad7341e11d0dc5e675949810c34eb051707f0c43bc159'
NOW = dt.datetime.now(dt.timezone.utc).isoformat()

def need(value, message):
    if not value:
        raise ValueError(message)

def sha(body):
    return hashlib.sha256(body).hexdigest()

def raw(path):
    need(path.is_file() and not path.is_symlink() and all(not q.is_symlink() for q in path.parents), 'Regular fixed evidence')
    return path.read_bytes()

def ref(path):
    body = raw(path)
    return dict(path=path.relative_to(R).as_posix(), bytes=len(body), sha256=sha(body), full_mode=stat.S_IMODE(path.stat().st_mode))

def load(path):
    def pairs(items):
        result = {}
        for key, value in items:
            need(key not in result, 'Duplicate key')
            result[key] = value
        return result
    return json.loads(raw(path), object_pairs_hook=pairs, parse_constant=lambda x: (_ for _ in ()).throw(ValueError(x)))

def put(name, value):
    body = value.encode() if type(value) is str else (json.dumps(value, indent=2, sort_keys=True) + '\n').encode()
    with (F / name).open('xb') as stream:
        stream.write(body)

def family(path, mode):
    files, dirs = [], ['.']
    for q in sorted(path.rglob('*')):
        need(not q.is_symlink(), 'No symlink')
        if q.is_file():
            need(stat.S_IMODE(q.stat().st_mode) == mode, 'Exact full member mode')
            files.append(q.relative_to(path).as_posix())
        elif q.is_dir():
            need(stat.S_IMODE(q.stat().st_mode) == 0o755, 'Full directory mode')
            dirs.append(q.relative_to(path).as_posix())
        else:
            raise ValueError('Nonregular topology')
    need(stat.S_IMODE(path.stat().st_mode) == 0o755, 'Family root mode')
    need(set(dirs) == {'.'} | {q.as_posix() for n in files for q in PurePosixPath(n).parents if q.as_posix() != '.'}, 'No extra empty directory')
    return dict(path=path.relative_to(R).as_posix(), payload_names=files, payload_count=len(files), directory_names=sorted(dirs), full_file_mode=mode)

def check_row(row):
    need(ref(R / row['path']) == row, 'Complete body/fullmode binding')

need(sha(raw(P / 'SOURCE_READY.json')) == READY and sha(raw(P / 'SOURCE_MANIFEST.json')) == MF, 'Genuine current exact V6 closed source')
source_ready = load(P / 'SOURCE_READY.json')
source_self = load(P / 'SOURCE_MANIFEST.json')
need(source_self['schema'] == 'pr48-post-push-epoch-source-closure/v6' and source_self['files_count'] == 38 and len(source_self['files']) == 38, 'Genuine38 source schema')
for row in source_self['files']:
    body = raw(P / row['path'])
    need(len(body) == row['bytes'] and sha(body) == row['sha256'], 'Every complete actual closed V6 source body')
current = [family(P, 0o444), family(OLD, 0o444), family(M5, 0o444)]
need([z['payload_count'] for z in current] == [39, 26, 14], 'Exact current and preserved closed review counts')
need(current[0]['payload_names'] == sorted(source_ready['closure_payload_files'] + ['SOURCE_MANIFEST.json']), 'Complete current source names')
for row in source_ready['source_files']:
    q = R / row['path']
    need(len(raw(q)) == row['bytes'] and sha(raw(q)) == row['sha256'], 'Exact operative source triple')
need(source_self['file_modes'] == [dict(path=n, full_mode=0o444) for n in current[0]['payload_names']] and source_self['directory_modes'] == [dict(path=n, full_mode=0o755) for n in current[0]['directory_names']], 'Entire fullmode-bearing current source domains')

old_ledger_path = OLD / 'FIXED_INPUT_BINDINGS.json'
old_ledger = load(old_ledger_path)
need(old_ledger['fixed_rows_count'] == len(old_ledger['fixed_rows']) == 295 and len({z['path'] for z in old_ledger['fixed_rows']}) == 295, 'Distinct complete in-place predecessor bindings')
for row in old_ledger['fixed_rows']:
    check_row(row)
for descriptor in old_ledger['exact_preserved_families']:
    found = family(R / descriptor['path'], descriptor['full_file_mode'])
    need(found['payload_names'] == descriptor['payload_names'] and found['directory_names'] == descriptor['directory_names'], 'Historical family exact topology retained')

direct = {}
def add(path):
    row = ref(path)
    need(row['path'] not in direct or direct[row['path']] == row, 'No conflicting repeated evidence')
    direct[row['path']] = row

for descriptor in current:
    for name in descriptor['payload_names']:
        add(R / descriptor['path'] / name)

caps = []
directories = [dict(path=A.relative_to(R).as_posix(), full_mode=0o755)]
names = ['root_pr48_m5_adverse_source_close_actual_capture', 'root_pr48_m5_adverse_source_readback_actual_capture', 'root_pr48_v6_SOURCE_close_v2_actual_capture', 'root_pr48_v6_SOURCE_readback_actual_capture']
for name, pid in zip(names, [56763, 57284, 63767, 64372]):
    d = CAPROOT / name
    need({q.name for q in d.iterdir()} == {'CAPTURE.json', 'prelaunch_operator.py', 'stdout.bin', 'stderr.bin'} and stat.S_IMODE(d.stat().st_mode) == 0o700, 'True ROOT CAP4 typed directory')
    cap = load(d / 'CAPTURE.json')
    need(cap['schema'] == 'root-explicit-command-capture/v1' and cap['pid'] == pid and type(cap['pid']) is int and cap['actual_execution'] is True and cap['completed'] is True and cap['exit_code'] == 0 and cap['status'] == 'PASS' and cap['operator_unchanged'] is True, 'Genuine completed child')
    for stream in ['stdout', 'stderr']:
        b = raw(d / (stream + '.bin'))
        need(cap[stream] == dict(path=stream + '.bin', bytes=len(b), sha256=sha(b)), 'Entire retained true stream')
    need(raw(d / 'stderr.bin') == b'' and sha(raw(d / 'prelaunch_operator.py')) == cap['operator_sha256'] == 'c1ae969ccbbc48ed6fb486e96184da94329291a46b27d2b891ecb87185c909ec', 'Exact ROOT snapshot, full clean stderr')
    for q in d.iterdir():
        need(stat.S_IMODE(q.stat().st_mode) == 0o644, 'Every complete real CAP member mode')
        add(q)
    caps.append(dict(capture=ref(d / 'CAPTURE.json'), complete_capture=cap))
    directories.append(dict(path=d.relative_to(R).as_posix(), full_mode=0o700))

failed = A / 'root_finalize_foreign_epoch_v5_author_capture'
partial = A / 'root_finalize_foreign_epoch_v5_readonly'
for q in sorted(failed.iterdir()):
    add(q)
for q in sorted(partial.iterdir()):
    add(q)
failure_cap = load(failed / 'CAPTURE.json')
need(failure_cap['pid'] == 41530 and failure_cap['exit_code'] == 1 and sha(raw(failed / 'stderr.bin')) == '273f198044f53ca186bfeafd3803c96f201e8a78b8944a26dcd599563a26c5ba', 'Genuine original M5 failure')
directories += [dict(path=failed.relative_to(R).as_posix(), full_mode=0o700), dict(path=partial.relative_to(R).as_posix(), full_mode=0o755)]
add(A / 'capture_root_command.py')
need(direct[(A / 'capture_root_command.py').relative_to(R).as_posix()]['full_mode'] == 0o644 and sha(raw(A / 'capture_root_command.py')) == 'c1ae969ccbbc48ed6fb486e96184da94329291a46b27d2b891ecb87185c909ec', 'Actual reused live c1ae source full0644')
for row in directories + old_ledger['additional_genuine_outer_directories'] + [old_ledger['additional_genuine_outer_directory']]:
    q = R / row['path']
    need(q.is_dir() and not q.is_symlink() and stat.S_IMODE(q.stat().st_mode) == row['full_mode'], 'Every fixed exact directory role mode')

private = load(F / 'PRIVATE_TIMING_ACTUAL_CAPTURE' / 'CAPTURE.json')
result = load(F / 'PRIVATE_TIMING_ACTUAL_CAPTURE' / 'stdout.bin')
need(private['pid'] == result['actual_pid'] == 63897 and private['exit_code'] == 0 and private['status'] == 'PASS' and result['count'] == len(result['controls']) == 23 and all(z['expected_acceptance'] is z['observed_acceptance'] for z in result['controls']), 'Actual independent23 controls')
need(raw(F / 'PRIVATE_TIMING_ACTUAL_CAPTURE' / 'stderr.bin') == b'' and private['source_sha256'] == sha(raw(F / 'private_timing_models.py')) and private['operator_sha256'] == sha(raw(F / 'run_private_timing_models.py')), 'Private prelaunch source/caller and entire streams')
for stream in ['stdout', 'stderr']:
    b = raw(F / 'PRIVATE_TIMING_ACTUAL_CAPTURE' / (stream + '.bin'))
    need(private[stream] == dict(path=stream + '.bin', bytes=len(b), sha256=sha(b)), 'Complete actual private stream binding')

obs = dict(schema='pr48-v6-independent-fixed-source-evidence/v1', observed_utc=NOW, actual_own_artifact_author_pid=os.getpid(), source_ready_sha256=READY, actual_closed_source_manifest_sha256=MF, current_SOURCE_complete_payload_plus_self=39, direct_fixed_rows_count=len(direct), direct_fixed_rows=[direct[n] for n in sorted(direct)], prior_fixed_ledger=ref(old_ledger_path), prior_fixed_rows_verified_in_place=295, exact_current_families=current, exact_directory_modes=directories, entire_true_current_and_M5_ROOT_CAPs=caps, historical_failed_V5_CAP=failure_cap, previous_V5_PASS_is_incomplete_dated_history=True, M5_closed_adverse_SELF=ref(M5 / 'SELF_MANIFEST.json'), dated_first_V6_closure_attempt=dict(source='ROOT collaboration report', outcome='outer mkdir ENOSPC before child; no actual CAP/PID or successful closure claimed', path=(CAPROOT / 'root_pr48_v6_SOURCE_close_actual_capture').relative_to(R).as_posix()), production_executed=False, native_live_snapshot_required_at_future_review_closure=False, qualification='Direct files and the 295 historical fixed rows are bound in place. Historical native13 observations and absent V5 epoch describe past reads, not future live equality. No whole native/cache corpus was copied or reaudited. Genuine completed ROOT SOURCE custody is separate from prospective production authority.')
put('OBSERVATIONS.json', obs)
verdict = dict(schema='pr48-post-push-epoch-independent-SOURCE-verdict/v1', status='PASS_SOURCE_ONLY', utc=NOW, source_ready_sha256=READY, mandatory_findings=[], production_executed=False, future_acceptance_approved=False, review_continuity='Same M1/M2/M3/M4/M5 corrective reviewer; initial V6 scope saved before implementation read. Guided actual failure and previous incomplete SOURCE PASS disclosed; no blind new mathematics family.', M5_typed_datetime_repair_verified=True, M1_M2_M3_M4_guards_unchanged_verified=True, complete_current_source_payloads=38, current_ROOT_SOURCE_manifest_sha256=MF, direct_fixed_rows=len(direct), historical_fixed_rows_verified_in_place=295, actual_private_controls=dict(caller_pid=63896, pid=63897, checks=23, capture='PRIVATE_TIMING_ACTUAL_CAPTURE/CAPTURE.json', whole_stdout_sha256=private['stdout']['sha256'], whole_stderr_sha256=private['stderr']['sha256']), original_science17_original_first3_and22_ROOT_contract_unchanged=True, mathematical_credit=0, source_review_completion_percent=100, actual_recovery_completion_percent=0, remaining_gap='ROOT full reading and genuine review-evidence closure/readback; then distinct actual V6 per-role epochs and final three executions, complete mixed-six 22-key ROOT post. PR49 requires its own explicit V6 consumer revision. No current acceptance completion or new mathematical result is certified.')
put('VERDICT.json', verdict)
report = '''# PR48 V6 independent corrective SOURCE review

V6 passes this complete corrective SOURCE review with no mandatory finding. This is the same independent investigator who found M1–M5; the prior implementation history and the actual V5 runtime failure guided the audit. Initial scope was saved before reading the V6 implementation. The conclusion concerns fixed SOURCE consistency and private countermodels. It gives no actual epoch, finalization, mirror, post-inspection or mathematical discovery credit.

The genuine V5 author child41530 exited1 on2026-10-03 at17:54:45.637546UTC. Its entire984-byte stderr records `ValueError: UTC literal`. `validated_prefix()` returns an aware UTC datetime, whereas the old author line53 called the strict string parser on that datetime. The in-memory epoch object was never published: the failing comparison precedes the exclusive epoch write. The retained failed CAP4 and partial PRELAUNCH_SOURCE/READONLY_LEDGER remain fixed. Their observations of native bodies and absent epoch are historical, not promises about future live state. The closed V5 PASS and SOURCE custody remain unchanged and are explicitly incomplete history after M5.

I read all nine current operative/closure/readback sources as text, complete author/caller/adapter type flow, inspector, derived finalizer and mirror, full contract, prose, private code/results, binding records, textual authoring sources and both READY versions. The complete independent change map records all literal filename/path/schema substitutions and all residual differences. The only runtime predicate residual is author line53: `last <= c.clock(e['utc'])`. The only common residual is the new M5 evidence member. The finalizer and mirror are byte-identical to V5. All other seven compared bodies have no residual beyond declared identities. Original V3 science helpers, native mirror revision2 and historical receipts stay literal; they are not normalized into new authority.

Common lines387–391 initialize `last` by parsing a genuine original prefix finish string, update it with each genuine completed prior role finish, and return the datetime. Author line53 now consumes that value directly, while push finish and epoch time still enter the strict string parser. Caller line28 already used the direct comparison; adapter line28 validates the prefix without reparsing its return. All other `clock()` uses remain string boundaries. Common lines48–51 still reject nonstrings, surrounding whitespace, naive values and nonzero UTC offsets. The correction neither widens the parser nor omits push/prefix chronology.

Independent handwritten private models were genuinely launched by own caller63896/child63897 on2026-10-03 at18:25:47.317072–18:25:47.342685UTC, exit0. All23 assertions passed. These cover all three role return/consume boundaries, the old M5 rejection, equality, future prefix/push rejection, reversed child and role intervals, datetime/bool/integer/naive/nonUTC/whitespace/malformed literal rejection, and inability of a naive datetime to pass direct comparison. Full prelaunch source/caller/argv, actual PID/UTC and both split streams are retained. Stdout4756 bytes SHA80d0ff10e6519aedb470af59d1e48b3374de6799f59fbb4b9c08ea93c8fa1286; stderr empty. These are type-flow countermodels, not executions of proposed production code.

The complete unchanged custody predicates retain M1–M4 repairs. Common source_read binds full07777 mode and stable opened identity/body. The exact canonical nonsymlink outer parent is A48 full0755 in both retained and live operator bindings. The actual live A48/capture_root_command.py must be full0644/c1ae and byte-equal to the full0644 retained snapshot. Genuine outer directories are0700; source/runtime/prelaunch/dependency directories remain0755. Author, caller and inspector mode records propagate this typed actual identity before and after children and into final readback. Existing actual A48 c1ae2593-byte source is genuinely present at full0644, parent0755, and reused unchanged. Its installation by ROOT was not my work. Future adjacent V6 actors still require literal copies and full mode equality; no copy or production execution was performed by this reviewer.

The foreign and native envelope is unchanged: each role needs a fresh descendant HEAD, whole clean index and complete current foreign body/fullmode domain; original foreign rows remain dated. Whole current QUEUE is authenticated against fresh HEAD/index, preserves unrelated rows and the accepted2961 row, and requires absence of30004403. The other twelve native bodies and all13 full modes remain exact. Only the two actual owned logs may append. Post refuses unreviewed QUEUE drift after the mirror. Exclusive outputs and honest failed-child receipts remain required; no retry after partial writes is authorized. SOURCE mode and epoch approval checks remain independent of original scientific gates.

Original closed53 source,17 scientific pins, genuine first three successful captures and the exact22-key original ROOT contract remain unchanged. The inspector still requires the exact ordered old3/new3 actors, complete source/argv/fullmode/capture evidence, all22 typed scientific post values and exact native accounting. The unsolved shared2961/30004403 partial result remains the qualified low-dimensional/product/subgroup result and signed averaging obstruction. Original2/5, new0 and audit0 remain; there is no full-group solution, paper, DOI or tracker write.

Final READY c41aa5d82d4b6240ea496b180d6b73fbff09d02574942c4741cadd5c80b19e26 pins38 payloads and two relative directories. The dated preliminary READY81540e51 is preserved byte-exact, unclosed and superseded. ROOT genuinely closed current SOURCE by child63767 at18:25:34.158987–18:25:34.220397UTC and separately read it by64372 at18:26:25.712388–18:26:25.765594UTC. Actual manifest aea1b2933d03cc7c20bad7341e11d0dc5e675949810c34eb051707f0c43bc159 has38+self39 bodies all0444 and directories0755. I verified full CAP4 streams and exact current body/mode/topology. This completed custody is separate from my earlier dated0644 observation and from production authority. ROOT reported an earlier outer-mkdir ENOSPC before child at the first close name; no nonexistent CAP/PID or successful closure is invented.

The lean observations bind current39, previous closed review26, genuine closed M5 addendum14, all current/M5 true CAP4s, failed V5 CAP4/partial members and actual live c1ae individually. The predecessor295 fixed body/fullmode rows and their exact preserved families were rechecked in place through their fixed ledger. Their mathematical contents are historical context; this audit did not repeat unrelated SQL/mode corpora or copy old bodies. Native snapshots in source evidence remain qualified dated observations. Genuine adverse56763/57284 custody is not V6 approval.

Strongest verified claim: the complete fixed V6 SOURCE is internally consistent with the narrow typed-time correction, unchanged custody and original scientific conditions, and survived the23 independent private falsification controls. Exact remaining gap: ROOT must read and close/read this review evidence, then perform genuinely distinct V6 per-role author/finalize/mirror/post actions and the complete mixed-six22-key inspection. PR49 needs a separate reviewed V6 consumer. Concurrent state drift may cause a safe refusal. SOURCE review100%; actual recovery0%; new mathematics0%. No future PASS is asserted.
'''
put('REPORT.md', report)
put('RESEARCH_LOG.md', '# PR48 V6 independent corrective SOURCE log\n\n' + NOW + ': SOURCE review100%; actual recovery0%; mathematical discovery0%. Mechanism: full source-normalized continuity plus actual independent23 typed chronology models. No mandatory defect remains in fixed SOURCE. Genuine failed41530 and closed M5/V5 history remain immutable; new V6 ROOT source custody is separately observed. Exact gap is actual per-role production and complete22 post, followed by separate PR49 consumer review. Initial scope before implementation read is retained. No native/Git/remote/candidate/ROOT-helper execution or external contact by this reviewer.\n')
files = sorted(q.relative_to(F).as_posix() for q in F.rglob('*') if q.is_file()) + ['READY.json']
files = sorted(files)
dirs = sorted({'.'} | {q.as_posix() for n in files for q in PurePosixPath(n).parents if q.as_posix() != '.'})
for q in F.rglob('*'):
    need(not q.is_symlink() and stat.S_IMODE(q.stat().st_mode) == (0o644 if q.is_file() else 0o755), 'Own ready full modes/topology')
ready = dict(schema='pr48-v6-independent-review-readiness/v1', utc=NOW, status='READY_SOURCE_REVIEW_WAIT_ROOT', source_ready_sha256=READY, actual_candidate_source_manifest_sha256=MF, report=ref(F / 'REPORT.md'), verdict=ref(F / 'VERDICT.json'), observations=ref(F / 'OBSERVATIONS.json'), independent_controls=ref(F / 'PRIVATE_TIMING_ACTUAL_CAPTURE' / 'CAPTURE.json'), payload_names=files, payload_count=len(files), directory_names=dirs, payload_rows_except_READY=[ref(F / n) for n in files if n != 'READY.json'], production_executed=False, future_acceptance_approved=False, mathematical_credit=0, source_review_completion_percent=100, actual_recovery_completion_percent=0, future_ROOT_evidence_closure=None, future_ROOT_separate_readback=None)
put('READY.json', ready)
print(json.dumps(dict(status='READY_REVIEW_SOURCE_ONLY_WAIT_ROOT', actual_own_author_pid=os.getpid(), READY=ref(F / 'READY.json'), report=ref(F / 'REPORT.md'), verdict=ref(F / 'VERDICT.json'), observations=ref(F / 'OBSERVATIONS.json'), payload_count=len(files), relative_directories=len(dirs)-1, direct_fixed_rows=len(direct), historical_fixed_rows=295, production_executed=False)))
