"""ROOT postexit reconciliation of the closed PR48 WHOLE audit."""
from pathlib import Path,PurePosixPath
import datetime as dt,hashlib,json,os,stat,sys
R=Path('/Users/alec/Documents/Math');A=Path(__file__).absolute().parent
F=A/'current_whole_adversary_family';B=A.parent/'pr45_9900007'
assert __debug__ and not sys.flags.optimize
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
m=load(F/'MANIFEST.json')
assert sha(raw(F/'MANIFEST.json'))=='060aac8a645879155b1f3ae0a8026a201c0e63303ca24b6bd7b1374046ac30c8'
assert m['schema']=='pr48-whole-current-independent-self-only-closure/v1' and m['self_excluded']==['MANIFEST.json']
assert type(m['files_count']) is int and m['files_count']==len(m['files'])==162 and len(m['directories'])==38
owned=[]
for row in m['files']:
 assert set(row)=={'path','bytes','sha256','full_mode'} and type(row['bytes']) is int and row['full_mode']=='0444'
 n=row['path'];assert PurePosixPath(n).as_posix()==n and not {'.','..'}.intersection(PurePosixPath(n).parts)
 r=ref(F/n);assert r['bytes']==row['bytes'] and r['sha256']==row['sha256'] and r['full_mode']==0o444;owned.append(r)
assert stat.S_IMODE((F/'MANIFEST.json').stat().st_mode)==0o444
assert {p.relative_to(F).as_posix() for p in F.rglob('*') if p.is_file()}=={r['path'] for r in m['files']}|{'MANIFEST.json'}
assert {p.relative_to(F).as_posix() for p in F.rglob('*') if p.is_dir()}==set(m['directories'])
v=load(F/'VERDICT.json')
assert sha(raw(F/'AUDIT.md'))=='a063b1ef1b5bc2ed2e036c0485dc18f02ef659b158513063cfd840ec1ff24441'
assert sha(raw(F/'VERDICT.json'))=='b2085ad227b4270addab9b57e6f61bf3f3aec15924e50d2d39b4e1cffbac04a3'
assert v['mandatory_mathematical_corrections']==v['mandatory_source_or_packet_corrections']==[] and v['status_recommendation']=='unsolved' and v['future_acceptance_approved'] is False
allowed={'unsolved_math_prioritization/QUEUE.md','unsolved_math_prioritization/state.json','unsolved_math_prioritization/history.jsonl','draft_pr_publication_program_20260930/inventory.json'}
external={};dated=[];reads=0
for name,key in [('WHOLE_READBACK_RESULT.json','body_bindings'),('SUPPLEMENTAL_READBACK_RESULT.json','read_bindings')]:
 o=load(F/name);assert o['status'].startswith('PASS_') and o['future_acceptance_approved'] is False
 for row in o[key]:
  p=Path(row['path']);r=ref(p);reads+=1
  old={k:row[k] for k in ['path','bytes','sha256','full_mode']};assert type(old['bytes']) is int and type(old['full_mode']) is int
  n=dict(old,path=p.relative_to(R).as_posix())
  if F in p.parents:
   assert r['bytes']==n['bytes'] and r['sha256']==n['sha256'] and r['full_mode']==0o444;continue
  if r!=n:
   assert r['path'] in allowed;dated.append(dict(evidence_source=name,historical_whole_row=n,current_row=r,fresh_native_authority=False))
  if r['path'] in external and external[r['path']]!=n:
   assert r['path'] in allowed
   dated.append(dict(evidence_source=name,earlier_historical_row=external[r['path']],later_historical_row=n,fresh_native_authority=False))
  external[r['path']]=n
final=load(F/'FINAL_EVIDENCE_CONTROL_RESULT_V2.json');assert final['status'].startswith('PASS_') and final['no_future_child_or_acceptance_certified'] is True
for row in final['bindings']:
 p=Path(row['path']);r=ref(p);assert r['bytes']==row['bytes'] and r['sha256']==row['sha256'];reads+=1
captures=[]
for name in ['root_pr48_whole_current_closure_actual_capture','root_pr48_whole_current_closed_readback_actual_capture']:
 d=B/name;c=load(d/'CAPTURE.json');assert {p.name for p in d.iterdir()}=={'CAPTURE.json','prelaunch_operator.py','stdout.bin','stderr.bin'}
 assert c['schema']=='root-explicit-command-capture/v1' and c['actual_execution'] is True and c['completed'] is True and type(c['exit_code']) is int and c['exit_code']==0 and c['operator_unchanged'] is True
 assert sha(raw(d/'prelaunch_operator.py'))==c['operator_sha256']
 for k in ['stdout','stderr']:
  b=raw(d/c[k]['path']);assert type(c[k]['bytes']) is int and len(b)==c[k]['bytes'] and sha(b)==c[k]['sha256']
 assert raw(d/'stderr.bin')==b''
 result=load(d/'stdout.bin');assert result['manifest_sha256']==sha(raw(F/'MANIFEST.json'))
 captures.append(dict(complete_capture=c,complete_members=[ref(p) for p in sorted(d.iterdir())],complete_stdout_object=result))
c,q=[r['complete_capture'] for r in captures]
assert c['pid']==m['actual_closing_pid']==28458 and q['pid']==29104
assert dt.datetime.fromisoformat(c['started_utc'])<dt.datetime.fromisoformat(m['created_utc'])<dt.datetime.fromisoformat(c['finished_utc'])<dt.datetime.fromisoformat(q['started_utc'])<dt.datetime.fromisoformat(q['finished_utc'])
extra=['ROOT_ACTUAL_CURRENT_FREEZE_INSPECTION.json','ROOT_NEW_SOURCE_ADVERSARY_RECORD.json','ROOT_CURRENT_PARTIAL_SCOPE_CERTIFICATE.md','ROOT_PRIMARY_READ_LEDGER.json','ROOT_SCIENCE_CARD.json','ROOT_CURRENT_INPUT_PREIMAGES.json','ROOT_EVIDENCE_BINDINGS.json','ROOT_WHOLE_CURRENT_CLOSURE_PRELAUNCH_SOURCE.py']
record=dict(schema='pr48-root-complete-closed-whole-inspection/v1',status='PASS_ROOT_COMPLETE_CLOSED_WHOLE_INSPECTION',created_utc=dt.datetime.now(dt.timezone.utc).isoformat(),actual_readback_pid=os.getpid(),complete_VERDICT_object=v,closed_whole_manifest=ref(F/'MANIFEST.json'),closed_whole_manifest_sha256=sha(raw(F/'MANIFEST.json')),whole_report=ref(F/'AUDIT.md'),whole_verdict=ref(F/'VERDICT.json'),candidate_manifest=ref(A/'reviewed_candidate/MANIFEST.json'),candidate_manifest_sha256=v['candidate_manifest_sha256'],normalized_complete_first_party_members=owned,normalized_complete_external_input_bindings=[external[n] for n in sorted(external)],individually_bound_foreign_inputs=len(external),first_party_members=len(owned),complete_binding_reads=reads,complete_actual_closing_and_postclosing_readback_captures=captures,ROOT_evidence_and_actual_prerequisite_bindings=[ref(A/n) for n in extra],personal_report_and_verdict_fully_read=True,all_first_party_whole_bytes_and_modes_checked=True,all_external_individual_whole_bytes_checked=True,exact_self_only_recursive_closure_checked=True,closing_and_postexit_capture_chronology_checked=True,ROOT_actual_inner52_complete_read=True,frozen_inner50_honest_prefix=True,dated_native4_current_HEAD_not_future_acceptance_authority=True,legitimate_dated_native_changes=dated,mandatory_defects=[],mandatory_corrections=[],original_substantive_attempts=2,turn_limit=5,duplicate_id=30004403,duplicate_shared_budget=True,new_substantive_attempts=0,audit_turns=0,full_problem_solved_by_project=False,full_target_resolved=False,ambient_four_bound_only_on_included_product_subgroup=True,all_powers_bound_on_included_subgroup=True,future_execution_approved=False,future_acceptance_approved=False,paper_created=False,new_DOI_created=False,tracker_row_created=False,human_peer_review_claimed=False,source_and_failure_qualification='ROOT personally read the full25719-byte AUDIT, entire verdict, closer and separate verifier; every162 closed member and complete independent external binding was read after actual closure/readback exit. Historical fixture modes are dated; own closure is full0444. All failures and corrected metadata remain preserved. Credited smooth perfectness, displacement and no-index2 handle theorems remain imported premises. The product bound and signed averaging obstruction do not solve the full Diff-infinity-0 four-manifold question. Fresh13/current main and protected foreign state are required for acceptance. Primary text reading does not authenticate PDF bytes/pixels. Extensive AI use; unrefereed.')
out=A/'ROOT_WHOLE_CURRENT_REVIEW.json'
with out.open('xb') as h:h.write((json.dumps(record,indent=2,allow_nan=False)+'\n').encode());h.flush();os.fsync(h.fileno())
print(json.dumps(dict(status=record['status'],record=ref(out),actual_pid=os.getpid(),members=len(owned),external_inputs=len(external),dated_native_changes=len(dated),future_acceptance_approved=False),indent=2))
