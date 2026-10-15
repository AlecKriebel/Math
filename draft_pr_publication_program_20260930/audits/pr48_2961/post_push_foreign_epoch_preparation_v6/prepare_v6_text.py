"""Own bounded textual preparation; never imports/compiles production sources."""
from pathlib import Path
import datetime as dt,hashlib,json,stat
P=Path(__file__).absolute().parent;A=P.parent;R=A.parents[2];OLD=A/'post_push_foreign_epoch_preparation_v5'
def sha(b):return hashlib.sha256(b).hexdigest()
def ref(p):
 b=p.read_bytes();return dict(path=p.relative_to(R).as_posix(),bytes=len(b),sha256=sha(b),full_mode=stat.S_IMODE(p.stat().st_mode))
def put(name,b):
 with (P/name).open('xb') as f:f.write(b)
runtime=['epoch_common.py','author_post_push_foreign_epoch_v5.py','execute_post_push_foreign_epoch_phase_v5.py','run_post_push_foreign_epoch_phase_v5.py','inspect_complete_actual_post_epoch_v5.py','integrate_reviewed_partial_epoch_v5.py','state_mirror_reconciliation_epoch_v5.py','close_SOURCE_family.py','verify_closed_SOURCE_family.py']
changes=[]
for name in runtime:
 old=(OLD/name).read_bytes();s=old.decode();s=s.replace('_v5','_v6').replace('_V5','_V6').replace('/v5','/v6').replace('V5 source','V6 source').replace('Exact V5','Exact V6').replace('Seven-key V5','Seven-key V6').replace('Typed V5','Typed V6').replace('SOURCE_V5','SOURCE_V6')
 if name=='author_post_push_foreign_epoch_v5.py':
  before="c.clock(last)<=c.clock(e['utc'])";after="last<=c.clock(e['utc'])"
  if s.count(before)!=1:raise ValueError('Exactly one typed-time predicate correction')
  s=s.replace(before,after)
 if name=='epoch_common.py':
  before="'M4_AND_SUPERSEDED_V4_BINDINGS.json']";after="'M4_AND_SUPERSEDED_V4_BINDINGS.json','M5_AND_SUPERSEDED_V5_BINDINGS.json']"
  if s.count(before)!=1:raise ValueError('Exact new source-evidence dependency addition')
  s=s.replace(before,after)
 newname=name.replace('_v5','_v6');new=s.encode();put(newname,new)
 normalized=s.replace('_v6','_v5').replace('_V6','_V5').replace('/v6','/v5').replace('V6 source','V5 source').replace('Exact V6','Exact V5').replace('Seven-key V6','Seven-key V5').replace('Typed V6','Typed V5').replace('SOURCE_V6','SOURCE_V5')
 if name=='author_post_push_foreign_epoch_v5.py':normalized=normalized.replace(after,before)
 if name=='epoch_common.py':normalized=normalized.replace(after,before)
 if normalized.encode()!=old:raise ValueError(('No extra normalized source difference',name))
 changes.append(dict(old=ref(OLD/name),new=ref(P/newname),only_declared_changes=True))
for name in ['ACTUAL_REJECTED_V1_SOURCE_BINDINGS.json','M2_AND_SUPERSEDED_V2_BINDINGS.json','M3_AND_SUPERSEDED_V3_BINDINGS.json','M4_AND_SUPERSEDED_V4_BINDINGS.json','NATIVE_SOURCE_DATE_SURVEY.json']:put(name,(OLD/name).read_bytes())
c=json.loads((OLD/'CONTRACT.json').read_bytes());c['schema']='pr48-post-push-epoch-SOURCE-contract/v6';c['new_source_manifest_schema']='pr48-post-push-epoch-source-closure/v6';c['actual_epoch_schema']='pr48-ROOT-post-push-per-phase-foreign-epoch/v6';c['actual_new_phase_capture_schema']='ROOT_actual_explicit_post_push_epoch_phase_capture_v6';c['mode_contract']='pr48-source-operator-dependency-full07777/v6';c['mandatory_M5']='V5 actual author41530 passed an already-aware validated_prefix datetime into the strict string clock parser. V6 compares last directly to clock(epoch UTC); clock remains strict.';c['superseded_closed_V5_READY_sha256']=sha((OLD/'SOURCE_READY.json').read_bytes());c['superseded_closed_V5_manifest']=ref(OLD/'SOURCE_MANIFEST.json');c['existing_actual_ROOT_operator_reused']=ref(A/'capture_root_command.py');c['future']['actual_live_ROOT_operator_copy']=None;c['future']['existing_actual_ROOT_operator_authority']='Existing installed A48 c1ae full0644 is required, reused unchanged; preparer has not copied it.';put('CONTRACT.json',(json.dumps(c,indent=2,sort_keys=True)+'\n').encode())
d=A/'root_finalize_foreign_epoch_v5_author_capture';cap=json.loads((d/'CAPTURE.json').read_bytes());stderr=(d/'stderr.bin').read_bytes()
if cap['pid']!=41530 or cap['exit_code']!=1 or len(stderr)!=984 or sha(stderr)!='273f198044f53ca186bfeafd3803c96f201e8a78b8944a26dcd599563a26c5ba':raise ValueError('Genuine M5 failure identity')
partial=A/'root_finalize_foreign_epoch_v5_readonly';native=['draft_pr_publication_program_20260930/inventory.json',*['unsolved_math_prioritization/'+n for n in ['QUEUE.md','state.json','history.jsonl','catalog.json','assessments.json','queue.py','policy.json','manifest.json','cache/problems.json','cache/research_results.json','cache/catalog.sqlite','review_v2/related_target_groups.json']]]
failure=dict(schema='pr48-M5-actual-failed-V5-SOURCE-bindings/v1',source_observed_utc=dt.datetime.now(dt.timezone.utc).isoformat(),read_only_source_observation_not_new_child=True,entire_actual_failed_CAP4=cap,complete_actual_failed_CAP4_members=[ref(q) for q in sorted(d.iterdir())],entire_actual_stderr_UTF8=stderr.decode(),V5_source_manifest=ref(OLD/'SOURCE_MANIFEST.json'),V5_source_ready=ref(OLD/'SOURCE_READY.json'),partial_actual_readonly_members=[ref(q) for q in sorted(partial.iterdir())],partial_actual_readonly_directory_fullmode=stat.S_IMODE(partial.stat().st_mode),existing_installed_c1ae=ref(A/'capture_root_command.py'),current_native13_dated_readonly_descriptors=[ref(R/n) for n in native],absent_actual_V5_epoch_observed=not (A/'ROOT_POST_PUSH_V5_FINALIZE_FOREIGN_EPOCH.json').exists(),V6_runtime_or_ROOT_approval_claimed=False,independent_M5_review=None)
put('M5_AND_SUPERSEDED_V5_BINDINGS.json',(json.dumps(failure,indent=2,sort_keys=True)+'\n').encode());put('NORMALIZED_SOURCE_CHANGE_MAP.json',(json.dumps(dict(schema='pr48-V5-to-V6-narrow-SOURCE-map/v1',proposed_or_production_compiled_imported_executed=False,changes=changes),indent=2,sort_keys=True)+'\n').encode())
print(json.dumps(dict(status='SOURCE_V6_TEXT_ONLY_WRITTEN',normalized_sources=len(changes),production_executed=False,actual_M5_pid=cap['pid'],existing_operator_unchanged=True)))
