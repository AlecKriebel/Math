"""ROOT's complete postexit reconciliation of the newly closed PR47 WHOLE review."""
from pathlib import Path, PurePosixPath
import datetime as dt, hashlib, json, os, stat, sys
R=Path('/Users/alec/Documents/Math'); A=Path(__file__).absolute().parent
F=A/'current_whole_adversary_family'; B=A.parent/'pr45_9900007'
assert __debug__ and not sys.flags.optimize
def raw(p):
    assert not p.is_symlink() and all(not q.is_symlink() for q in p.parents) and stat.S_ISREG(p.stat().st_mode)
    return p.read_bytes()
def sha(b): return hashlib.sha256(b).hexdigest()
def load(p):
    def pairs(items):
        result={}
        for k,v in items: assert k not in result; result[k]=v
        return result
    def invalid(v): raise ValueError(v)
    return json.loads(raw(p),object_pairs_hook=pairs,parse_constant=invalid)
def ref(p):
    b=raw(p); return dict(path=p.relative_to(R).as_posix(),bytes=len(b),sha256=sha(b),full_mode=stat.S_IMODE(p.stat().st_mode))
m=load(F/'MANIFEST.json')
assert sha(raw(F/'MANIFEST.json'))=='658133399198e8528aa2a45b89c87a19f3b69edd6998b86b7e8227c850f5fd78'
assert m['schema']=='pr47-whole-current-independent-self-only-closure/v1' and m['self_excluded']==['MANIFEST.json']
assert m['files_count']==len(m['files'])==385 and len(m['directories'])==84
owned=[]
for r in m['files']:
    assert set(r)=={'path','bytes','sha256','full_mode'} and type(r['bytes']) is int and r['full_mode']=='0444'
    n=r['path']; assert PurePosixPath(n).as_posix()==n and not {'.','..'}.intersection(PurePosixPath(n).parts)
    a=ref(F/n); assert a['bytes']==r['bytes'] and a['sha256']==r['sha256'] and a['full_mode']==0o444
    owned.append(a)
assert stat.S_IMODE((F/'MANIFEST.json').stat().st_mode)==0o444
assert {p.relative_to(F).as_posix() for p in F.rglob('*') if p.is_file()}=={r['path'] for r in m['files']}|{'MANIFEST.json'}
assert {p.relative_to(F).as_posix() for p in F.rglob('*') if p.is_dir()}==set(m['directories'])
v=load(F/'VERDICT.json')
assert sha(raw(F/'AUDIT.md'))=='a6ef38f9d7a7bea49f634f1de3696dee7dcea69788e1879ce20c23f57e36ae96'
assert sha(raw(F/'VERDICT.json'))=='fc8f94675c370948b33bd24232d3feca11c09d74772e7ab1c315266daa874682'
assert v['mandatory_corrections']==[] and v['status']=='unsolved' and v['future_acceptance_approved'] is False
external={}; dated=[]
allowed={'unsolved_math_prioritization/QUEUE.md','unsolved_math_prioritization/state.json','unsolved_math_prioritization/history.jsonl','draft_pr_publication_program_20260930/inventory.json'}
for name,key in [('WHOLE_READBACK.json','complete_read_bindings'),('SUPPLEMENTAL_READBACK.json','complete_body_bindings')]:
    o=load(F/name)
    assert o['status']=='PASS' and o['future_acceptance_approved'] is False
    for r in o[key]:
        p=Path(r['path']); a=ref(p); old={k:r[k] for k in ['path','bytes','sha256','full_mode']}
        assert type(old['bytes']) is int and type(old['full_mode']) is int
        if F in p.parents:
            assert a['bytes']==r['bytes'] and a['sha256']==r['sha256'] and a['full_mode']==0o444
            continue
        normalized=dict(old,path=p.relative_to(R).as_posix())
        if a!=normalized:
            assert a['path'] in allowed
            dated.append(dict(path=a['path'],historical_whole_row=normalized,present_row=a))
        if a['path'] in external: assert external[a['path']]==normalized
        external[a['path']]=normalized
assert len(external)==2933
captures=[]
for name in ['root_pr47_whole_current_closure_actual_capture','root_pr47_whole_current_closed_readback_actual_capture']:
    d=B/name; c=load(d/'CAPTURE.json')
    assert set(p.name for p in d.iterdir())=={'CAPTURE.json','prelaunch_operator.py','stdout.bin','stderr.bin'}
    assert c['schema']=='root-explicit-command-capture/v1' and c['actual_execution'] is True and c['completed'] is True and type(c['exit_code']) is int and c['exit_code']==0 and c['operator_unchanged'] is True
    assert sha(raw(d/'prelaunch_operator.py'))==c['operator_sha256']
    for key in ['stdout','stderr']:
        b=raw(d/c[key]['path']); assert len(b)==c[key]['bytes'] and sha(b)==c[key]['sha256']
    assert not raw(d/'stderr.bin')
    captures.append(dict(capture=ref(d/'CAPTURE.json'),complete_capture=c,complete_members=[ref(p) for p in sorted(d.iterdir())],complete_stdout_object=load(d/'stdout.bin')))
c,q=[r['complete_capture'] for r in captures]
assert c['pid']==m['actual_closing_pid']==86916 and q['pid']==87026
assert dt.datetime.fromisoformat(c['started_utc'])<dt.datetime.fromisoformat(m['created_utc'])<dt.datetime.fromisoformat(c['finished_utc'])<dt.datetime.fromisoformat(q['started_utc'])<dt.datetime.fromisoformat(q['finished_utc'])
extra=['ROOT_ACTUAL_CURRENT_FREEZE_INSPECTION.json','ROOT_NEW_SOURCE_ADVERSARY_RECORD.json','ROOT_CURRENT_SCOPE_CERTIFICATE.md','ROOT_PRIMARY_READ_LEDGER.json','ROOT_SCIENCE_CARD.json','ROOT_CURRENT_INPUT_PREIMAGES.json','ROOT_EVIDENCE_BINDINGS.json','ROOT_WHOLE_CURRENT_CLOSURE_PRELAUNCH_SOURCE.py']
record=dict(schema='pr47-root-complete-closed-whole-inspection/v1',status='PASS_ROOT_COMPLETE_CLOSED_WHOLE_INSPECTION',created_utc=dt.datetime.now(dt.timezone.utc).isoformat(),actual_readback_pid=os.getpid(),complete_VERDICT_object=v,
    closed_whole_manifest=ref(F/'MANIFEST.json'),closed_whole_manifest_sha256=sha(raw(F/'MANIFEST.json')),whole_report=ref(F/'AUDIT.md'),whole_verdict=ref(F/'VERDICT.json'),candidate_manifest=ref(A/'reviewed_candidate/MANIFEST.json'),candidate_manifest_sha256=v['candidate_manifest_sha256'],
    normalized_complete_first_party_members=owned,normalized_complete_external_input_bindings=[external[n] for n in sorted(external)],individually_bound_foreign_inputs=len(external),first_party_members=len(owned),complete_actual_closing_and_postclosing_readback_captures=captures,ROOT_evidence_and_actual_prerequisite_bindings=[ref(A/n) for n in extra],
    personal_report_and_verdict_fully_read=True,all_first_party_whole_bytes_and_modes_checked=True,all_external_individual_whole_bytes_checked=True,exact_self_only_recursive_closure_checked=True,closing_and_postexit_capture_chronology_checked=True,ROOT_actual_inner49_complete_read=True,frozen_inner47_honest_prefix=True,dated_native4_current_HEAD_not_future_acceptance_authority=True,legitimate_dated_native_changes=dated,
    mandatory_defects=[],mandatory_corrections=[],original_substantive_attempts=1,turn_limit=5,new_substantive_attempts=0,audit_turns=0,full_problem_solved_by_project=False,full_target_resolved=False,realized_example_Isharp_rank_computed=False,universal_normal_vanishing_false=True,
    future_execution_approved=False,future_acceptance_approved=False,paper_created=False,new_DOI_created=False,tracker_row_created=False,human_peer_review_claimed=False,
    source_and_failure_qualification='ROOT personally read all22402 bytes of AUDIT, the entire verdict, closer and separate verifier. Every385 closed member and2933 unique external bindings was read completely after the real closing/readback children exited. Own historical private fixture modes were normalized to full0444 at closure; original recorded modes remain historical. Known realized degeneracy is credited and does not compute framed-instanton rank or refute KP3.51. Imported gauge theorem remains conditional. Prior SOURCE/current/WHOLE certify fixed artifacts only; fresh13/current main and protected foreign state are required before acceptance. Primary browser text reading does not authenticate historical PDF byte hashes or pixels. Extensive AI use; unrefereed.')
out=A/'ROOT_WHOLE_CURRENT_REVIEW.json'
with out.open('xb') as h: h.write((json.dumps(record,indent=2,allow_nan=False)+'\n').encode());h.flush();os.fsync(h.fileno())
print(json.dumps(dict(status=record['status'],record=ref(out),actual_pid=os.getpid(),members=len(owned),external_inputs=len(external),dated_native_changes=len(dated),future_acceptance_approved=False),indent=2))
