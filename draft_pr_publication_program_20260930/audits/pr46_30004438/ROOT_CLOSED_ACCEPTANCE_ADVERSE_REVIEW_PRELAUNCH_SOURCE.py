"""ROOT's complete negative SOURCE-review reconciliation after actual self closure."""
from pathlib import Path,PurePosixPath
import argparse,datetime as dt,hashlib,json,os,re,stat,sys
R=Path('/Users/alec/Documents/Math');A=Path(__file__).absolute().parent
F=A/'acceptance_source_adversary_family';B=A.parent/'pr45_9900007'
assert __debug__ and not sys.flags.optimize
p=argparse.ArgumentParser();p.add_argument('--expected-manifest-sha256',required=True);p.add_argument('--expected-payload-count',required=True,type=int);p.add_argument('--actual-closing-capture',required=True);p.add_argument('--actual-readback-capture',required=True);a=p.parse_args()
def raw(p):
    assert not p.is_symlink() and all(not q.is_symlink() for q in p.parents) and stat.S_ISREG(p.stat().st_mode)
    return p.read_bytes()
def sha(b):return hashlib.sha256(b).hexdigest()
def load(p):
    def pairs(items):
        d={}
        for k,v in items:assert k not in d;d[k]=v
        return d
    def bad(v):raise ValueError(v)
    return json.loads(raw(p),object_pairs_hook=pairs,parse_constant=bad)
def ref(p):
    b=raw(p);return dict(path=p.relative_to(R).as_posix(),bytes=len(b),sha256=sha(b),full_mode=stat.S_IMODE(p.stat().st_mode))
def safe(n):
    assert type(n) is str and n and not PurePosixPath(n).is_absolute() and PurePosixPath(n).as_posix()==n and not {'.','..','.git','__pycache__'}.intersection(PurePosixPath(n).parts)
    return n
assert re.fullmatch('[0-9a-f]{64}',a.expected_manifest_sha256) and a.expected_payload_count>80
m=load(F/'SELF_MANIFEST.json');assert sha(raw(F/'SELF_MANIFEST.json'))==a.expected_manifest_sha256
assert m['self_excluded']==['SELF_MANIFEST.json'] and type(m['files_count']) is int and m['files_count']==len(m['files'])==a.expected_payload_count
assert m['verdict']=='REJECT_MANDATORY_SOURCE_CORRECTION' and m['future_acceptance_approved'] is False
owned=[]
for r in m['files']:
    assert set(r)=={'path','bytes','sha256','full_mode'} and type(r['bytes']) is int and type(r['full_mode']) is int and r['full_mode']==0o444
    q=ref(F/safe(r['path']));assert q['bytes']==r['bytes'] and q['sha256']==r['sha256'] and q['full_mode']==0o444
    owned.append(q)
assert stat.S_IMODE((F/'SELF_MANIFEST.json').stat().st_mode)==0o444
assert {p.relative_to(F).as_posix() for p in F.rglob('*') if p.is_file()}=={r['path'] for r in m['files']}|{'SELF_MANIFEST.json'}
assert {'.'}|{p.relative_to(F).as_posix() for p in F.rglob('*') if p.is_dir()}=={r['path'] for r in m['directories']}
for r in m['directories']:assert stat.S_IMODE((F/r['path']).stat().st_mode)==r['full_mode']
v=load(F/'VERDICT.json');assert sha(raw(F/'VERDICT.json'))=='b7ae891cd27718aaba174550d4c55c869d450f153fc3f16f47227a7489a644a6'
assert sha(raw(F/'REPORT.md'))=='43b32a4e178335808c70b68a625532c4f3c0bf9723933a1c2895ac929c9bc631'
assert [r['id'] for r in v['mandatory_corrections']]==['S1'] and v['future_acceptance_approved'] is False
old=load(F/'OWN_INPUT_READ_BINDINGS.json');q=load(F/'DATED_NATIVE_CLOSURE_QUALIFICATION_V2.json')
assert len(old['external_bindings'])==old['normalized_external_count']==2611
queue='unsolved_math_prioritization/QUEUE.md';external=[];dated=[]
for r in old['external_bindings']:
    path=Path(r['path']);normalized={k:r[k] for k in ['path','bytes','sha256','full_mode']};normalized['path']=path.relative_to(R).as_posix()
    if normalized['path']==queue:
        hist=raw(F/safe(q['captured_historical_body']['path']))
        assert len(hist)==normalized['bytes']==382073 and sha(hist)==normalized['sha256']=='a1210bbc36ebd6cd4ced6480edb0fe5e01d28bac59ebd2cf4910312853e396be'
        assert hashlib.sha1(b'blob '+str(len(hist)).encode()+b'\0'+hist).hexdigest()==q['historical_blob_sha1']=='d60e9b1df63bebb7b49af7bbb6c6ed64c83681d0'
        assert normalized['full_mode']==0o644 and q['historical_commit']=='e491808c3544ff44e8526d9b24857b5c9ca64208'
        primary=load(F/'PRIVATE_CONTROL_RESULT.json');cap=load(F/'captures/private_source_controls/CAPTURE.json')
        assert primary['actual_pid']==cap['child_pid']==q['observation_primary_actual_child']==55086
        assert primary['started_utc']==q['observation_started_utc'] and primary['finished_utc']==q['observation_finished_utc']
        assert dt.datetime.fromisoformat(cap['started_utc'])<=dt.datetime.fromisoformat(primary['started_utc'])<=dt.datetime.fromisoformat(primary['finished_utc'])<=dt.datetime.fromisoformat(cap['finished_utc'])
        assert primary['native13_before']==primary['native13_after']
        selected=[z for z in primary['native13_before'] if z['path']==queue];assert selected==[normalized]
        dated.append(dict(historical_observation=normalized,historical_recovered_body=ref(F/q['captured_historical_body']['path']),complete_dated_qualification=q,current_live_observation=ref(R/queue),fresh_native_authority=False))
    else:
        assert ref(path)==normalized
        external.append(normalized)
assert len(external)==2610 and len(dated)==1
clockq=load(F/'CHILD_OBSERVATION_CLOCK_QUALIFICATION_V3.json')
assert m['schema']=='pr46-acceptance-source-adversary-self-closure/v3' and a.expected_payload_count==94
assert clockq['actual_failed_V2_ROOT_child']==2427 and clockq['mandatory_finding_unchanged']=='S1'
extra=[]
for r in q['new_fixed_external_receipts']+clockq['new_fixed_external_receipts']:
    path=Path(r['path']);n={k:r[k] for k in ['path','bytes','sha256','full_mode']};n['path']=path.relative_to(R).as_posix();assert ref(path)==n;extra.append(n)
assert len(extra)==10 and len({r['path'] for r in extra})==10
captures=[]
for name,expected in [('root_pr46_acceptance_source_closure_actual_capture',0),('root_pr46_acceptance_source_closed_readback_actual_capture',0),('root_pr46_acceptance_adverse_source_closure_actual_capture',1),('root_pr46_acceptance_adverse_source_closure_v2_actual_capture',1),(a.actual_closing_capture,0),(a.actual_readback_capture,0)]:
    assert Path(name).name==name;d=B/name;c=load(d/'CAPTURE.json')
    assert c['schema']=='root-explicit-command-capture/v1' and c['actual_execution'] is True and c['completed'] is True and type(c['pid']) is int and c['pid']>0 and type(c['exit_code']) is int and c['exit_code']==expected and c['operator_unchanged'] is True
    assert {p.name for p in d.iterdir()}=={'CAPTURE.json','prelaunch_operator.py','stdout.bin','stderr.bin'}
    assert sha(raw(d/'prelaunch_operator.py'))==c['operator_sha256']
    for k in ['stdout','stderr']:
        b=raw(d/c[k]['path']);assert len(b)==c[k]['bytes'] and sha(b)==c[k]['sha256']
    output=load(d/'stdout.bin') if expected==0 else None
    captures.append(dict(complete_capture=c,complete_members=[ref(p) for p in sorted(d.iterdir())],complete_stdout_object=output,complete_failure_stderr_UTF8=raw(d/'stderr.bin').decode() if expected else None))
c,b=[z['complete_capture'] for z in captures[-2:]]
assert c['pid']==m['actual_closing_child_pid'] and dt.datetime.fromisoformat(c['started_utc'])<dt.datetime.fromisoformat(m['created_utc'])<dt.datetime.fromisoformat(c['finished_utc'])<dt.datetime.fromisoformat(b['started_utc'])<dt.datetime.fromisoformat(b['finished_utc'])
assert captures[-2]['complete_stdout_object']['manifest_sha256']==captures[-1]['complete_stdout_object']['manifest_sha256']==a.expected_manifest_sha256
record=dict(schema='pr46-root-complete-closed-adverse-source-inspection/v1',status='PASS_COMPLETE_RECONCILIATION_OF_REJECTED_V1_SOURCE',approved_by_root=True,created_utc=dt.datetime.now(dt.timezone.utc).isoformat(),actual_readback_pid=os.getpid(),complete_VERDICT_object=v,
    closed_adverse_manifest=ref(F/'SELF_MANIFEST.json'),closed_adverse_manifest_sha256=a.expected_manifest_sha256,adverse_report=ref(F/'REPORT.md'),adverse_verdict=ref(F/'VERDICT.json'),normalized_complete_first_party_members=owned,normalized_complete_external_input_bindings=external,individually_bound_unchanged_external_inputs=2610,exact_dated_native_observations=dated,additional_fixed_external_receipts=extra,complete_actual_closing_and_postclosing_readback_captures=captures,
    personal_report_and_verdict_fully_read=True,complete_report_personally_read=True,all_first_party_whole_bytes_and_modes_checked=True,all_external_individual_whole_bytes_checked=True,all_dated_native_observations_historical_body_and_actual_clocks_checked=True,exact_self_only_recursive_closure_checked=True,closing_and_postexit_capture_chronology_checked=True,
    mandatory_corrections=v['mandatory_corrections'],acceptance_source_V1_rejected=True,acceptance_source_V2_reviewed=False,acceptance_source_V2_approved=False,original_substantive_attempts=0,original_source_verification_responses=1,new_substantive_attempts=0,audit_turns=0,
    future_execution_approved=False,future_acceptance_approved=False,fresh_native_authority=False,paper_created=False,new_DOI_created=False,tracker_row_created=False,
    qualification='ROOT personally read full original REPORT/VERDICT and every additive closure-repair supplement/actual final closer/verifier. All closed members and2610 unchanged external bodies/modes were read after real closure/readback exit; exactly one dated native QUEUE is matched to the genuine captured historical Git body/blob and original actual child observation. Operator capture contains child observation times, which are not equated. Real failed84831 and2427 remain failures. ROOT unused diagnosisV1 row-normalization error is explicitly superseded by V2. S1 acceptance ownership correction remains mandatory; this negative record grants no positive repaired-source, execution or merge approval.')
out=A/'ROOT_ACCEPTANCE_ADVERSE_SOURCE_REVIEW.json'
with out.open('xb') as h:h.write((json.dumps(record,indent=2,allow_nan=False)+'\n').encode());h.flush();os.fsync(h.fileno())
print(json.dumps(dict(status=record['status'],actual_pid=os.getpid(),record=ref(out),owned_members=len(owned),unchanged_external_inputs=2610,dated_native_observations=1,future_acceptance_approved=False),indent=2))
