"""Complete ROOT postclosing WHOLE evidence readback; no future acceptance authority."""
from pathlib import Path,PurePosixPath
import datetime as dt,hashlib,json,os,stat
R=Path('/Users/alec/Documents/Math');A=Path(__file__).absolute().parent;F=A/'current_whole_adversary_family';B=A.parent/'pr45_9900007'
assert __debug__
def raw(p):
 assert not p.is_symlink() and not any(q.is_symlink() for q in p.parents) and stat.S_ISREG(p.stat().st_mode)
 return p.read_bytes()
def sha(b):return hashlib.sha256(b).hexdigest()
def ref(p):
 b=raw(p);return dict(path=p.relative_to(R).as_posix(),bytes=len(b),sha256=sha(b),full_mode=stat.S_IMODE(p.stat().st_mode))
def load(p):return json.loads(raw(p))
m=load(F/'MANIFEST.json');assert sha(raw(F/'MANIFEST.json'))=='be3fa099c6a080d5f9cddcf42f39ac51b51c8f89cd76d09fb5d360a99d1990e2'
assert m['schema']=='pr46-whole-current-independent-self-only-closure/v1' and m['self_excluded']==['MANIFEST.json'] and len(m['files'])==m['files_count']==245 and len(m['directories'])==49
owned=[]
for r in m['files']:
 p=F/r['path'];a=ref(p);assert a['bytes']==r['bytes'] and a['sha256']==r['sha256'] and a['full_mode']==0o444
 owned.append(a)
assert stat.S_IMODE((F/'MANIFEST.json').stat().st_mode)==0o444
assert {p.relative_to(F).as_posix() for p in F.rglob('*') if p.is_file()}=={r['path'] for r in m['files']}|{'MANIFEST.json'}
assert {p.relative_to(F).as_posix() for p in F.rglob('*') if p.is_dir()}==set(m['directories'])
v=load(F/'VERDICT.json');assert v['mandatory_corrections']==[] and v['future_acceptance_approved'] is False and v['recommended_status']=='already_solved'
assert sha(raw(F/'AUDIT.md'))=='bc77100839ac65c4c59d9c003a7992747e00407b041ea895f1bf9a00a43d4cce'
rb=load(F/'READBACK_RESULT.json');external=[];dated=[]
allowed={'draft_pr_publication_program_20260930/inventory.json','unsolved_math_prioritization/QUEUE.md','unsolved_math_prioritization/state.json','unsolved_math_prioritization/history.jsonl'}
for r in rb['all_unique_reads']:
 p=Path(r['path']);a=ref(p)
 if a['bytes']!=r['bytes'] or a['sha256']!=r['sha256'] or a['full_mode']!=r['full_mode']:
  assert a['path'] in allowed
  dated.append(dict(path=a['path'],historical_whole_row=r,present_row=a))
 external.append(dict(path=p.relative_to(R).as_posix(),bytes=r['bytes'],sha256=r['sha256'],full_mode=r['full_mode']))
assert len(external)==1946
captures=[]
for n in ['root_pr46_whole_closure_actual_capture','root_pr46_whole_closed_readback_actual_capture']:
 C=B/n;c=load(C/'CAPTURE.json');assert c['actual_execution'] is True and c['completed'] is True and c['exit_code']==0 and c['operator_unchanged'] is True
 assert {p.name for p in C.iterdir()}=={'CAPTURE.json','prelaunch_operator.py','stdout.bin','stderr.bin'}
 for k in ['stdout','stderr']:
  b=raw(C/c[k]['path']);assert len(b)==c[k]['bytes'] and sha(b)==c[k]['sha256']
 assert not raw(C/'stderr.bin');captures.append(dict(capture=ref(C/'CAPTURE.json'),complete_capture=c,complete_members=[ref(p) for p in sorted(C.iterdir())],complete_stdout_object=load(C/'stdout.bin')))
close,verify=[r['complete_capture'] for r in captures]
assert close['pid']==m['actual_closing_pid']==10245 and verify['pid']==10633
assert dt.datetime.fromisoformat(close['started_utc'])<dt.datetime.fromisoformat(m['created_utc'])<dt.datetime.fromisoformat(close['finished_utc'])<dt.datetime.fromisoformat(verify['started_utc'])<dt.datetime.fromisoformat(verify['finished_utc'])
extra=[A/'ROOT_ACTUAL_CURRENT_FREEZE_INSPECTION.json',A/'ROOT_NEW_SOURCE_ADVERSARY_RECORD.json',A/'ROOT_CURRENT_KNOWN_RESULT_SCOPE_CERTIFICATE.md',A/'ROOT_PRIMARY_READ_LEDGER.json',A/'ROOT_SCIENCE_CARD.json',A/'ROOT_CURRENT_INPUT_PREIMAGES.json',A/'ROOT_EVIDENCE_BINDINGS.json',A/'ROOT_WHOLE_CLOSURE_PRELAUNCH_SOURCE.py']
record=dict(schema='pr46-root-complete-closed-whole-inspection/v1',status='PASS_ROOT_COMPLETE_CLOSED_WHOLE_INSPECTION',created_utc=dt.datetime.now(dt.timezone.utc).isoformat(),actual_readback_pid=os.getpid(),
 complete_VERDICT_object=v,closed_whole_manifest=ref(F/'MANIFEST.json'),closed_whole_manifest_sha256=sha(raw(F/'MANIFEST.json')),whole_report=ref(F/'AUDIT.md'),whole_verdict=ref(F/'VERDICT.json'),candidate_manifest=ref(A/'reviewed_candidate/MANIFEST.json'),candidate_manifest_sha256=v['candidate_manifest_sha256'],
 normalized_complete_first_party_members=owned,normalized_complete_external_input_bindings=external,individually_bound_foreign_inputs=len(external),first_party_members=len(owned),complete_actual_closing_and_postclosing_readback_captures=captures,ROOT_evidence_and_actual_prerequisite_bindings=[ref(p) for p in extra],
 personal_report_and_verdict_fully_read=True,all_first_party_whole_bytes_and_modes_checked=True,all_external_individual_whole_bytes_checked=True,exact_self_only_recursive_closure_checked=True,closing_and_postexit_capture_chronology_checked=True,
 ROOT_actual_inner45_complete_read=True,frozen_inner43_honest_prefix=True,dated_native4_current_HEAD_not_future_acceptance_authority=True,legitimate_dated_native_changes=dated,
 mandatory_defects=[],mandatory_corrections=[],original_substantive_attempts=0,original_source_verification_responses=1,new_substantive_attempts=0,audit_turns=0,full_target_resolved_in_prior_published_literature=True,full_problem_solved_by_project=False,
 future_execution_approved=False,future_acceptance_approved=False,paper_created=False,new_DOI_created=False,tracker_row_created=False,human_peer_review_claimed=False,
 source_and_failure_qualification='ROOT personally fully read complete report/verdict/closer/verifier; all245 first-party members and1946 complete externally bound bodies/modes rechecked after closing child exit. Prior SOURCE/current/WHOLE conclusions certify these fixed artifacts. Final acceptance needs new fresh13/current main and exact preserved foreign dirty state. Literal failed98221 remains evidence. Primary source text/formulas checked; no fresh authentication of historical PDF byte hashes or pixel renders claimed by ROOT. All operative runtime model/effort/deadline fields remain null. Extensive AI use; unrefereed.')
out=A/'ROOT_WHOLE_CURRENT_REVIEW.json'
with out.open('xb') as f:f.write((json.dumps(record,indent=2,allow_nan=False)+'\n').encode());f.flush();os.fsync(f.fileno())
print(json.dumps(dict(status=record['status'],record=ref(out),actual_pid=os.getpid(),members=245,external_inputs=1946,dated_native_changes=len(dated),future_acceptance_approved=False),indent=2))
