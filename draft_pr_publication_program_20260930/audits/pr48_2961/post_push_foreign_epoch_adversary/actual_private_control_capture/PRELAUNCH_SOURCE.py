"""Independent, bounded evidence reads and handwritten models; no candidate loading."""
from pathlib import Path
import datetime as dt, hashlib, json, os, stat, sys

F = Path(__file__).absolute().parent
A = F.parent
R = A.parents[2]
P = A / 'post_push_foreign_epoch_preparation'
H = A / 'acceptance_preparation_family_v3'
A45 = A.parent / 'pr45_9900007'
READY = '245f1af3127f1258c8262fa9ce8420286631b1f0e327c02a47de171bf2d670b1'
started = dt.datetime.now(dt.timezone.utc).isoformat()
checks = []
observations = []

def need(v, message):
    if not v:
        raise ValueError(message)
def sha(b):
    return hashlib.sha256(b).hexdigest()
def encode(o):
    return (json.dumps(o, indent=2, sort_keys=True, allow_nan=False) + '\n').encode()
def parse(b):
    def pairs(items):
        out = {}
        for k, v in items:
            need(k not in out, 'Duplicate JSON key')
            out[k] = v
        return out
    return json.loads(b, object_pairs_hook=pairs, parse_constant=lambda s: (_ for _ in ()).throw(ValueError(s)))
def same(a, b):
    return type(a) is type(b) and (a.keys() == b.keys() and all(same(a[k], b[k]) for k in a) if type(a) is dict else len(a) == len(b) and all(same(x, y) for x, y in zip(a, b)) if type(a) is list else a == b)
def read(p, role):
    before = p.lstat()
    need(stat.S_ISREG(before.st_mode) and not any(q.is_symlink() for q in p.parents), 'Regular source only')
    b = p.read_bytes()
    after = p.lstat()
    need((before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns, before.st_mode) == (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns, after.st_mode), 'Stable whole input read')
    observations.append(dict(path=p.relative_to(R).as_posix(), bytes=len(b), sha256=sha(b), full_mode=stat.S_IMODE(after.st_mode), role=role, complete_body_read=True, authority='dated observation at private child execution; no future freshness'))
    return b
def control(name, passed, kind):
    need(passed is True, name)
    checks.append(dict(name=name, passed=True, kind=kind))
def put(p, b):
    with p.open('xb') as f:
        f.write(b)
        f.flush()
        os.fsync(f.fileno())

rb = read(P / 'SOURCE_READY.json', 'rejected candidate readiness')
need(sha(rb) == READY, 'Exact reviewed READY')
ready = parse(rb)
names = {Path(z['path']).relative_to(P.relative_to(R)).as_posix() for z in ready['source_files']}
names |= {'SOURCE_READY.json', 'superseded_design_fixed5/epoch_common.py', 'source_authoring_history/revise_common_text.py', 'source_authoring_history/derive_post_text.py'}
need(len(names) == 19 and {q.relative_to(P).as_posix() for q in P.rglob('*') if q.is_file()} == names, 'Exact candidate19')
need({q.relative_to(P).as_posix() for q in P.rglob('*') if q.is_dir()} == {'superseded_design_fixed5', 'source_authoring_history'}, 'Exact candidate2 dirs')
for n in sorted(names - {'SOURCE_READY.json'}):
    b = read(P / n, 'rejected candidate complete source')
    z = next((z for z in ready['source_files'] if z['path'] == (P/n).relative_to(R).as_posix()), None)
    if z is not None:
        need(type(z['bytes']) is int and len(b) == z['bytes'] and sha(b) == z['sha256'], 'Exact readiness body binding')
need(all(z['full_mode'] == 0o644 for z in observations), 'Candidate observed full0644; not ROOT closed')
control('all19 candidate bodies and exact two-directory topology read at supplied READY', True, 'actual whole evidence read')

hm = read(H / 'PREPARATION_MANIFEST.json', 'historical closed original53+self')
need(sha(hm) == '9c525f7b540068af07477e8f794e21596d93e69e49e8dbc52972d3196eb9fda4', 'Original source manifest')
manifest = parse(hm)
need(type(manifest['files_count']) is int and manifest['files_count'] == len(manifest['files']) == 53, 'Original53')
for z in manifest['files']:
    b = read(H / z['path'], 'historical source complete bytes only; semantic read limited to relevant helpers')
    need(len(b) == z['bytes'] and sha(b) == z['sha256'] and observations[-1]['full_mode'] == 0o444, 'Historical closed payload body/full0444')
control('all53 historical SOURCE payload hashes and full0444 checked without loading', True, 'actual whole evidence read')

pre = parse(read(A / 'integration_preflight.json', 'genuine dated original preflight'))
pin_names = ['preparation_manifest_sha256']
for n in ['final_plan','final_receipt','final_manifest','reconciliation_capture','previous_mirror','previous_post','fresh_preimage','root_bindings']:
    pin_names += [n, n+'_sha256']
values = {n: pre[n] for n in pin_names}
helper = H / 'integrate_reviewed_partial.py'
helper_body = helper.read_bytes()
last = None
for phase in ['preflight', 'overlay', 'prepush']:
    d = A / ('root_'+phase+'_actual_capture')
    need({q.name for q in d.iterdir()} == {'CAPTURE.json','PRELAUNCH.json','PRELAUNCH_SOURCE.py','PRELAUNCH_OPERATOR.py','stdout.bin','stderr.bin'}, 'Exact original CAP6')
    members = {q.name:read(q, 'genuine dated original '+phase+' CAP6') for q in sorted(d.iterdir())}
    c, launch = parse(members['CAPTURE.json']), parse(members['PRELAUNCH.json'])
    need(c['phase'] == phase and c['status'] == 'PASS' and c['actual_execution'] is True and c['completed'] is True and type(c['pid']) is int and c['pid'] > 0 and type(c['exit_code']) is int and c['exit_code'] == 0, 'Original actual child')
    need(all(same(c[k],v) for k,v in launch.items() if k != 'schema'), 'Whole original prelaunch retained')
    argv = ['/usr/bin/python3','-B',str(helper),'--execute','--preparation-manifest-sha256',values['preparation_manifest_sha256']]
    for n in pin_names[1::2]:
        argv += ['--'+n.replace('_','-'), values[n], '--'+n.replace('_','-')+'-sha256', values[n+'_sha256']]
    argv += [phase]
    if phase == 'overlay':
        overlay = parse(read(A/'integration_check.json', 'genuine dated original overlay record'))
        argv += ['--merge-queue-preimage-sha256',overlay['automatic_merge_queue_preimage_sha256']]
    need(same(c['argv'], argv) and members['PRELAUNCH_SOURCE.py'] == helper_body and sha(members['PRELAUNCH_SOURCE.py']) == c['source_sha256'] and sha(members['PRELAUNCH_OPERATOR.py']) == c['operator_sha256'] == '331cb4cb479113a8dbedc758e328b30a11bc93bcd052535953a4da9fd705095c', 'Original exact actual argv/source/operator')
    for k in ['stdout','stderr']:
        need(c[k]['path'] == k+'.bin' and len(members[k+'.bin']) == c[k]['bytes'] and sha(members[k+'.bin']) == c[k]['sha256'], 'Original whole streams')
    need(members['stderr.bin'] == b'', 'Original clean child stderr')
    need(c['prepared_utc'] <= c['started_utc'] <= c['finished_utc'] and (last is None or last <= c['started_utc']), 'Original phase chronology')
    last = c['finished_utc']
control('three genuine ordered original CAP6s exact argv/source/operator/full streams authenticated', True, 'actual whole evidence read')

root_captures = [('root_pr48_commit_fresh_1312_actual_capture',15396,'PASS',0),('root_pr48_push_fresh_1314_actual_capture',18309,'PASS',0),('root_pr48_finalize_fresh_1314_actual_capture',19622,'FAIL',1)]
for name, pid, status, code in root_captures:
    d = A45/name
    need({q.name for q in d.iterdir()} == {'CAPTURE.json','prelaunch_operator.py','stdout.bin','stderr.bin'}, 'ROOT exact CAP4')
    members = {q.name:read(q, 'ROOT actual '+status+' '+name) for q in sorted(d.iterdir())}
    c = parse(members['CAPTURE.json'])
    need(c['actual_execution'] is True and c['completed'] is True and type(c['pid']) is int and c['pid'] == pid and type(c['exit_code']) is int and c['exit_code'] == code and c['status'] == status, 'Typed ROOT process')
    need(sha(members['prelaunch_operator.py']) == c['operator_sha256'] == 'c1ae969ccbbc48ed6fb486e96184da94329291a46b27d2b891ecb87185c909ec', 'ROOT actual operator')
    for k in ['stdout','stderr']:
        need(c[k]['path'] == k+'.bin' and len(members[k+'.bin']) == c[k]['bytes'] and sha(members[k+'.bin']) == c[k]['sha256'], 'ROOT whole streams')
    if pid == 19622:
        need(c['argv'][-1] == 'finalize' and members['stdout.bin'] == b'' and b'Whole current protected foreign body/fullmode exact' in members['stderr.bin'], 'True pre-child failure retained')
        need(not (A/'root_finalize_actual_capture').exists(), 'Failed outer created no fake phase child CAP')
control('actual commit15396/push18309 and failed pre-child outer19622 full CAP4s retained as distinct outcomes', True, 'actual whole evidence read')

# Actual permission mutation occurs only on this independently created private fixture.
fixture_dir = F/'private_fixture'
fixture_dir.mkdir(exist_ok=False)
fixture = fixture_dir/'literal_source.txt'
put(fixture, b'private handwritten source-mode counterexample\n')
os.chmod(fixture,0o644)
original_body = fixture.read_bytes()
original_mode = stat.S_IMODE(fixture.stat().st_mode)
mutations=[]
for mode in [0o600,0o2644,0o4644]:
    os.chmod(fixture,mode)
    observed = stat.S_IMODE(fixture.stat().st_mode)
    old_body_only = fixture.read_bytes() == original_body
    corrected_full = old_body_only and observed == original_mode
    mutations.append(dict(before_full_mode=original_mode, requested_after_full_mode=mode, observed_after_full_mode=observed, complete_body_identical=old_body_only, current_candidate_style_body_only_predicate=old_body_only, required_full_mode_preservation_predicate=corrected_full))
    control('chmod-only counterexample '+oct(mode)+' passes body-only but fails fullmode preservation', old_body_only is True and corrected_full is False and observed == mode, 'actual private chmod; handwritten predicate only')
os.chmod(fixture,0o644)

def typed_mode(v):
    return type(v) is int and 0 <= v <= 0o7777
for v in [0,0o600,0o644,0o444,0o1644,0o2644,0o4644,0o7644,0o7777]:
    control('valid typed fullmode '+oct(v), typed_mode(v), 'handwritten positive')
for name,v in [('bool_true',True),('bool_false',False),('float',420.0),('string','420'),('none',None),('negative',-1),('overflow',0o10000)]:
    control('reject invalid fullmode '+name, typed_mode(v) is False, 'handwritten negative')

def exact_roles(rows):
    return type(rows) is list and len(rows)==6 and rows==['preflight','overlay','prepush','finalize','mirror','post']
correct=['preflight','overlay','prepush','finalize','mirror','post']
control('exact mixed-six roles accepted', exact_roles(correct), 'handwritten positive')
for name,rows in [('missing',correct[:-1]),('duplicate',correct[:3]+['finalize','finalize','post']),('out_of_order',correct[:3]+['mirror','finalize','post']),('extra',correct+['post'])]:
    control('mixed-six reject '+name, exact_roles(rows) is False, 'handwritten negative')

def envelope(before,after,phase):
    allowed={'finalize':{'inventory'},'mirror':{'state','history'},'post':set()}[phase]
    return set(before)==set(after) and all(type(after[n]['mode']) is int and after[n]['mode']==before[n]['mode'] and (n in allowed or same(after[n],before[n])) for n in before)
before={n:dict(body='original-'+n,mode=0o600) for n in ['queue','inventory','state','history','other']}
for phase,names in [('finalize',['inventory']),('mirror',['state','history']),('post',[])]:
    after={n:dict(z) for n,z in before.items()}
    for n in names:after[n]['body']='exact-prescribed-'+n
    control('native allowed bodies with all modes preserved '+phase,envelope(before,after,phase),'handwritten positive')
    wrong={n:dict(z) for n,z in after.items()};wrong['queue']['body']='unauthorized-current-row-change'
    control('native reject QUEUE write '+phase,envelope(before,wrong,phase) is False,'handwritten negative')
    wrong={n:dict(z) for n,z in after.items()};wrong[names[0] if names else 'other']['mode']=0o644
    control('native reject fullmode change even allowed body '+phase,envelope(before,wrong,phase) is False,'handwritten negative')

put(F/'INPUT_OBSERVATIONS.json',encode(dict(schema='pr48-post-push-independent-dated-input-observations/v1',actual_reader_pid=os.getpid(),candidate_ready_sha256=READY,complete_input_body_reads=True,source_only=True,future_live_equality_claimed=False,ROOT_approval=False,rows=observations)))
result=dict(schema='pr48-post-push-independent-private-counterexample-controls/v1',status='PASS_PRIVATE_CONTROLS_M1_COUNTEREXAMPLE_CONFIRMED',actual_pid=os.getpid(),started_utc=started,finished_utc=dt.datetime.now(dt.timezone.utc).isoformat(),candidate_ready_sha256=READY,actual_candidate_imported_compiled_executed=False,actual_Git_native_remote_mutation=False,mathematical_credit=0,checks_count=len(checks),checks=checks,actual_private_chmod_counterexamples=mutations,input_observation_rows=len(observations),no_production_or_ROOT_approval=True)
put(F/'PRIVATE_RESULTS.json',encode(result))
print(json.dumps(dict(status=result['status'],actual_pid=os.getpid(),checks_count=len(checks),input_observation_rows=len(observations),counterexamples=len(mutations))))
