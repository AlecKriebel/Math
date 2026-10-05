"""Exact in-place completed SOURCE collector; no Git/native writes or blanket staging."""
import os,stat
from pathlib import Path
from common import *
from selection import *
P=R/'draft_pr_publication_program_20260930';fixed={};dirs={}
EXCLUDED_FINALIZATION_ROOT='actual_source_finalization_capture'
def addfile(f):
 z=plain_ref(f);need(z['path'] not in fixed or fixed[z['path']]==z,'Different duplicate');fixed[z['path']]=z;return z
def complete(d,count):
 need(d.is_dir() and not d.is_symlink(),'Whole regular completed directory');rows=[]
 for f in [d]+sorted(d.rglob('*')):
  need(not f.is_symlink(),'No selected symlink');s=f.lstat()
  if stat.S_ISDIR(s.st_mode):
   rel=str(f.relative_to(R));dirs[rel]=dict(path=rel,full_mode=stat.S_IMODE(s.st_mode))
  else:rows.append(addfile(f))
 need(len(rows)==count,'Exact observed whole-directory file count');return rows
def indexed(d,marker,pin):
 f=d/marker;need(digest(f.read_bytes())==pin,'Existing exact source index');j=load(f)
 rows=j.get('files',j.get('source_rows_except_READY'));need(isinstance(rows,list),'Literal known source row schema');seen=set()
 for z in rows:
  name=z.get('relative_path',z['path']);q=Path(name)
  q=q if q.is_absolute() else (path(name) if name.startswith('draft_pr_publication_program_20260930/') else d/q)
  need(q.is_relative_to(d) and '..' not in q.parts,'Source row inside this selected family');seen.add(q);actual=plain_ref(q)
  need(actual['bytes']==z['bytes'] and actual['sha256']==z['sha256'],'Indexed complete source bytes')
  mode=z.get('full_mode_07777',z.get('full_mode',z.get('mode')));need(mode is not None,'Indexed full permission mode')
  need(actual['full_mode']==(int(mode,8) if isinstance(mode,str) else mode),'Indexed complete07777 mode')
 need({q for q in d.rglob('*') if q.is_file()}-seen=={f},'Only exact literal self-index exclusion');return plain_ref(f)
def ownpaths():
 out={str(q.relative_to(R)) for q in N.rglob('*') if q.is_file() and q.name!='RESEARCH_LOG.md'
      and not {EXCLUDED_READBACK_ROOT,EXCLUDED_FINALIZATION_ROOT}&set(q.relative_to(N).parts)}
 for q in N.glob('source_*_actual_capture'):
  out|={str((q/v).relative_to(R)) for v in ['CAPTURE.json','prelaunch_operator.py','prelaunch_common.py','stdout.bin','stderr.bin']}
 out|={str((N/v).relative_to(R)) for v in ['SCOPE_PREVERIFICATION.json','SCOPE.json','SOURCE_VERIFICATION.json','SOURCE_READY.json']}
 return sorted(out)
def main():
 start=now();final=(N/'SOURCE_VERIFICATION.json').exists()
 if final:need(load(N/'SOURCE_VERIFICATION.json')['status']=='PASS_READONLY_SOURCE_CHECKS','Actual earlier consistency check')
 families=[]
 for rel,count,marker,pin in FAMILIES:
  q=P/rel;i=indexed(q,marker,pin);rows=complete(q,count)
  families.append(dict(root=str(q.relative_to(R)),files=count,bytes=sum(z['bytes'] for z in rows),existing_index=i,
    custody='Existing completed custody retained; no new mathematical/priority/ROOT-review credit'))
 extra=[]
 for rel,count,role in EXTRA_DIRECTORIES:
  rows=complete(P/rel,count);extra.append(dict(root=str((P/rel).relative_to(R)),files=count,bytes=sum(z['bytes'] for z in rows),role=role))
 outside=[addfile(P/v) for v in ROOT_FILES]
 for rel,pin in OUTSIDE_PINS.items():need(digest((P/rel).read_bytes())==pin,'Exact authorized outside body/log; refuse legitimate later updates')
 caps=[]
 for name,pid in CAPS:
  q=P/'audits/pr45_9900007'/name;j=load(q/'CAPTURE.json');rows=complete(q,4)
  need({Path(z['path']).name for z in rows}=={'CAPTURE.json','prelaunch_operator.py','stdout.bin','stderr.bin'},'Complete literal CAP4 topology')
  need(j['pid']==pid and j['exit_code']==0 and j['actual_execution'] and j['completed'] and j['operator_unchanged'] and j['status']=='PASS','Actual completed ROOT operation')
  need(digest((q/'prelaunch_operator.py').read_bytes())==j['operator_sha256'],'Full capture operator')
  for key in ['stdout','stderr']:
   z=plain_ref(q/(key+'.bin'));need(z['bytes']==j[key]['bytes'] and z['sha256']==j[key]['sha256'],'Whole actual ROOT stream')
  caps.append(dict(root=str(q.relative_to(R)),actual_pid=pid,started_utc=j['started_utc'],finished_utc=j['finished_utc'],metadata=plain_ref(q/'CAPTURE.json'),new_checkpoint_ROOT_authority=False))
 # Quarantine references retain historical copies inside the owned archive;
 # canonical/native paths referenced in receipts are never followed into scope.
 qr=load(P/'audits/pr48_2961/root_partial_finalize_v6_quarantine/QUARANTINE_RECEIPT.json')
 rr=load(P/'audits/pr48_2961/ROOT_PARTIAL_FINALIZE_V6_ROLLBACK_RECEIPT.json')
 need(rr['overall_rollback_success_claimed'] and rr['actual_pid']==40863 and not rr['Git_index_body_or_ref_or_staging_mutated'],'Completed selected rollback, not acceptance')
 for key,directory,pid,pin in [('checkpoint1915-private','checkpoint1915-private_4307x_rt',43975,'9a1e6a5986329c96933f5b439489d09053d63037f4dae15dd65f7ffad8ae7c38'),('checkpoint1915-reconciled','checkpoint1915-reconciled_a2exeqna',44225,'b614e4b1c3f594c10852fb52e1fa05cade94a1e462ab6c2dfc231a4a3a41185c')]:
  q=P/'storage_compression_20261003'/directory;need(digest((q/'receipt.json').read_bytes())==pin,'Exact genuine compression receipt')
  j=load(q/'receipt.json');need(j['status']=='COMPRESSED' and j['source_replaced'] and j['operator_pid']==pid and j['saved_allocated_bytes']>0,'Completed compression only')
  need(j['before']['sha256']==j['after']['sha256'] and digest((q/'helper.prelaunch.py').read_bytes())==j['helper_sha256'],'Preserved original logical bytes/executed source')
 readback=P/'storage_compression_20261003/checkpoint1915_metadata_readback_20261003/RESULT.json';j=load(readback)
 need(digest(readback.read_bytes())=='ff94b37dc52776d81895c97cea9d37302020aeb28f2abbcf6a5dd0a0be10ce05' and j['actual_preparer_pid']==46427 and j['status']=='PASS_BOTH_CHECKPOINT1915_READBACKS','Separate actual dated fullmetadata readback')
 forbidden=['unsolved_math_prioritization/QUEUE.md','unsolved_math_prioritization/catalog.json','unsolved_math_prioritization/state.json','unsolved_math_prioritization/history.json','.git/index']
 forbidden += [str((P/v).relative_to(R)) for v in ['inventory.json','review_state.json','review_history.json']]
 need(not set(fixed)&set(forbidden),'No live native/shared inventory/index body')
 scope=dict(schema='ROOT-exact-owned-research-checkpoint-scope/v1',source_only=True,started_utc=start,prepared_utc=now(),actual_collector_pid=os.getpid(),
  fixed_files=[fixed[k] for k in sorted(fixed)],fixed_directories=[dirs[k] for k in sorted(dirs)],completed_fixed_families=families,completed_extra_directories=extra,
  outside_actual_ROOT_records_and_authorized_logs=outside,actual_ROOT_CAP4_sets=caps,ROOT_log_marker_suffix=ROOT_LOG_MARKER_SUFFIX,
  runtime_stamped_log_paths=[str((N/'RESEARCH_LOG.md').relative_to(R))],new_preparation_source_paths=ownpaths(),forbidden_native_paths=forbidden,
  excluded_future_output_roots=[str((N/v).relative_to(R)) for v in [EXCLUDED_READBACK_ROOT,EXCLUDED_FINALIZATION_ROOT]],
  exclusions=['active V7/current62','canonical native/shared inventory/QUEUE/state/history and live Git index','private corpora/PDFs/index/reconciled-index bodies','other chats','prior80414/80480 failed capture already checkpointed1915'],
  formal_completed_acceptance='37/180',formal_completed_percent=20.5556,selected_rollback_complete_native_acceptance_pending=True,mathematical_discovery_changed=False,
  ROOT_review_of_this_SOURCE_not_claimed=True,stage_commit_push_executed=False,native_acceptance_changed=False,
  current_modes_are_literal_not_rewritten_historical_metadata=True,quarantine_is_historical_evidence_not_canonical_acceptance=True,
  guard='ROOT must checkpoint before V7 execution; any later fixed log/body/mode update requires honest refusal and new source binding, not silent adoption')
 output=N/('SCOPE.json' if final else 'SCOPE_PREVERIFICATION.json');exclusive(output,encoded(scope))
 print(encoded(dict(status='PREPARED_EXACT_COMPLETED_SOURCE_SCOPE_ONLY',scope=plain_ref(output),actual_pid=os.getpid(),final_scope=final,fixed_files=len(fixed),
  fixed_directories=len(dirs),selected_bytes=sum(z['bytes'] for z in fixed.values()),whole_families=len(families),extra_directories=len(extra),CAP4_sets=len(caps))).decode(),end='')
if __name__=='__main__':main()
