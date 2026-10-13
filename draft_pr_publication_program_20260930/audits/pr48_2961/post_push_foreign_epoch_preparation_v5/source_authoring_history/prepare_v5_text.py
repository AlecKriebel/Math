"""Narrow text transformation only; no candidate/ROOT operator execution."""
from pathlib import Path
import datetime as dt,hashlib,json,stat
R=Path('/Users/alec/Documents/Math');A=R/'draft_pr_publication_program_20260930/audits/pr48_2961';O=A/'post_push_foreign_epoch_preparation_v4';P=A/'post_push_foreign_epoch_preparation_v5';NOW=dt.datetime.now(dt.timezone.utc).isoformat()
def ref(q):
 b=q.read_bytes();return dict(path=q.relative_to(R).as_posix(),bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),full_mode=stat.S_IMODE(q.stat().st_mode))
def put(n,b):
 q=P/n;q.parent.mkdir(parents=True,exist_ok=True)
 with q.open('xb') as f:f.write(b)
rows=[ref(q) for q in sorted(O.rglob('*')) if q.is_file()];assert len(rows)==24 and all(z['full_mode']==0o644 for z in rows);assert not (O/'SOURCE_MANIFEST.json').exists();assert ref(O/'SOURCE_READY.json')['sha256']=='4a2ca334cfea92fb44dfebb874de8d4b0827292b0ab3fb7e82a57de3b8746771'
actors=['author_post_push_foreign_epoch','execute_post_push_foreign_epoch_phase','run_post_push_foreign_epoch_phase','inspect_complete_actual_post_epoch','integrate_reviewed_partial_epoch','state_mirror_reconciliation_epoch'];renames={n+'_v4.py':n+'_v5.py' for n in actors};changes=[]
for old in ['epoch_common.py','close_SOURCE_family.py','verify_closed_SOURCE_family.py']+[n+'_v4.py' for n in actors]:
 b=(O/old).read_bytes();s=b.decode()
 if old not in ['integrate_reviewed_partial_epoch_v4.py','state_mirror_reconciliation_epoch_v4.py']:
  for x,y in renames.items():s=s.replace(x,y)
  s=s.replace('post_push_foreign_epoch_preparation_v4','post_push_foreign_epoch_preparation_v5')
  for name in ['pr48-source-operator-dependency-full07777','pr48-post-push-epoch-SOURCE-readiness','pr48-post-push-epoch-source-closure','pr48-ROOT-post-push-per-phase-foreign-epoch','pr48-epoch-actual-memory-readonly','pr48-root-post-epoch-actual-memory-readonly','pr48-root-post-runtime-evidence']:s=s.replace(name+'/v4',name+'/v5')
  for x,y in [('ROOT_actual_explicit_post_push_epoch_phase_capture_v4','ROOT_actual_explicit_post_push_epoch_phase_capture_v5'),('ROOT_explicit_post_push_epoch_phase_prelaunch_v4','ROOT_explicit_post_push_epoch_phase_prelaunch_v5'),('ROOT_POST_PUSH_V4_','ROOT_POST_PUSH_V5_'),('_foreign_epoch_v4_readonly','_foreign_epoch_v5_readonly'),('ROOT_POST_EPOCH_V4_','ROOT_POST_EPOCH_V5_'),('root_complete_actual_post_epoch_v4_inspection_capture','root_complete_actual_post_epoch_v5_inspection_capture')]:s=s.replace(x,y)
  if old in ['close_SOURCE_family.py','verify_closed_SOURCE_family.py']:s=s.replace('V4','V5')
 if old=='epoch_common.py':
  anchor='def operator_binding(directory):';helper="def actual_outer_parent(directory):\n    need(directory.is_absolute() and directory.parent==A and directory.is_dir() and not directory.is_symlink() and all(not q.is_symlink() for q in directory.parents) and directory.resolve(strict=True)==directory and A.resolve(strict=True)==A,'Actual ROOT outer must have exact canonical nonsymlink A48 parent');return directory_binding(A)\n"
  assert s.count(anchor)==1;s=s.replace(anchor,helper+anchor)
  s=s.replace('def operator_binding(directory):\n    z=','def operator_binding(directory):\n    actual_outer_parent(directory);z=')
  s=s.replace('def live_operator_binding(directory):\n    live,','def live_operator_binding(directory):\n    actual_outer_parent(directory);live,')
  s=s.replace("'M3_AND_SUPERSEDED_V3_BINDINGS.json']","'M3_AND_SUPERSEDED_V3_BINDINGS.json','M4_AND_SUPERSEDED_V4_BINDINGS.json']")
 new=renames.get(old,old);put(new,s.encode());changes.append(dict(original=ref(O/old),derived=ref(P/new),byte_identical=b==s.encode()))
for name in ['ACTUAL_REJECTED_V1_SOURCE_BINDINGS.json','M2_AND_SUPERSEDED_V2_BINDINGS.json','M3_AND_SUPERSEDED_V3_BINDINGS.json','NATIVE_SOURCE_DATE_SURVEY.json']:put(name,(O/name).read_bytes())
c=json.loads((O/'CONTRACT.json').read_bytes())
for key in ['schema','new_source_manifest_schema','actual_epoch_schema']:c[key]=c[key].replace('/v4','/v5')
c['actual_new_phase_capture_schema']=c['actual_new_phase_capture_schema'].replace('_v4','_v5');c['mode_contract']='pr48-source-operator-dependency-full07777/v5';c['actual_ROOT_outer_parent_required']=(A.relative_to(R)).as_posix();c['superseded_unclosed_V4_READY_sha256']='4a2ca334cfea92fb44dfebb874de8d4b0827292b0ab3fb7e82a57de3b8746771';c['mandatory_M4']='Only exact canonical nonsymlink A48-parent ROOT outer directories may bind the A48 live c1ae operator. Other audit parents fail before live context.';put('CONTRACT.json',(json.dumps(c,indent=2)+'\n').encode())
h=dict(schema='pr48-first-party-M4-and-superseded-V4-bindings/v5',observed_utc=NOW,method='Filesystem complete body/SHA/fullmode reads only',superseded_V4=dict(ROOT_closed=False,payload_count=24,READY_sha256='4a2ca334cfea92fb44dfebb874de8d4b0827292b0ab3fb7e82a57de3b8746771',complete_payloads=rows,directories=[dict(path=q.relative_to(R).as_posix(),full_mode=stat.S_IMODE(q.stat().st_mode)) for q in [O]+sorted(q for q in O.rglob('*') if q.is_dir())]),source_changes=changes,source_mode_observations_are_dated_creation_modes=True,ROOT_reported_M4='Genuine private child12372 reproduced other-parent operator permission drift; full report/verdict bindings will be added when completed and read',independent_M4_binding=None,future_ROOT_candidate_approval=False,production_executed=False);put('M4_AND_SUPERSEDED_V4_BINDINGS.json',(json.dumps(h,indent=2)+'\n').encode());put('RESEARCH_LOG.md',('# PR48 post-push SOURCE V5 log\n\n'+NOW+' — ROOT assigned exact-parent M4 repair after actual private counterexample12372. Complete control source read. Separate V5 changes only versions and shared exact absolute/canonical/nonsymlink A48 outer-parent predicate invoked before retained/live operator bindings. Unclosed24 V4 bodies/full0644 preserved. Full M4 report/verdict pending reading before READY. Source repair50%; corrective review0%; actual recovery0%; mathematical discovery0%.\n').encode())
print(json.dumps(dict(status='TEXT_PREPARATION_ONLY_WAIT_M4_REPORT',old24_unchanged=True,candidate_executed=False)))
