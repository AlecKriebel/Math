"""Commit/push only actual PR311 publication completion, with persisted foreign baseline."""
from pathlib import Path
from datetime import datetime,timezone
import sys,json,hashlib,os,stat,subprocess
P=Path(__file__).resolve().parent;R=P.parent;A=P/'audits/pr311_30005303'
sys.path.insert(0,str(A))
from root_submission_gate import current_clearance,window,load,pin,sha,utc,QUEUE,RELEASE,operational_clearance,acquire_shared_write_window
from root_checkpoint_tree_guard import live_pins, tree_pins, staged_tree, committed_tree
NAME='checkpoint_311_completed_publication_031'
write_window=acquire_shared_write_window()
window();clear=current_clearance();operational_clearance()
result=load(A/'CURRENT_PUBLICATION_STATUS.json')
assert result['status']=='MERGED_PUBLISHED_AND_TRACKER_VERIFIED' and result['workflow_completion_percent']==100
assert result['unresolved_findings']==0 and result['all_eleven_public_metadata_fields_equal'] and result['both_whole_public_files_equal'] and result['one_tracker_row_exact_readback']
D=P/('private_'+NAME);D.mkdir(exist_ok=False)
def git(*a):return subprocess.check_output(['/usr/bin/git',*a],cwd=R,env=dict(os.environ,GIT_OPTIONAL_LOCKS='0'))
parent=git('rev-parse','HEAD').decode().strip()
assert parent==result['actual_merge'] and git('branch','--show-current')==b'main\n'
assert git('ls-remote','origin','refs/heads/main').decode().split()[0]==parent
assert not git('diff','--cached','--raw','-z')
files=[P/n for n in ['RESEARCH_LOG.md','SHARED_GIT_WINDOW_STATUS.json','inventory.json','checkpoint_311_final_clearance_030_receipt.json','root_checkpoint_tree_guard.py',Path(__file__).name]]
public_names=['README.md','RESEARCH_LOG.md','CURRENT_PACKAGE_STATUS.json','CURRENT_PUBLICATION_STATUS.json','COMPLETION_ATTEMPT.json','BRANCH_REFRESH_ATTEMPT.json','queue_repair_receipt.json','repaired_snapshot_manifest.json','ACTUAL_MERGE_ATTEMPT.json','ACTUAL_MERGE_VERIFICATION.json','ROOT_EXACT_LIVE_PREMERGE.json','ROOT_POST_MERGE_VERIFICATION.json','published_pr_body.txt','published_pr_body_update_preexecution.json','queue_publication_receipt.json','native_publication_note_receipt.json','root_submission_gate.py','root_integrate_claimed.py','root_verify_post_merge.py','root_record_publication_completion.py','CURRENT_OPERATIONAL_OPERATOR_PINS_V02.json','ROOT_OPERATIONAL_REPAIR_V02.json','ROOT_OPERATIONS_REVIEW01_AUTHENTICATION.json','ROOT_GWS_RETRY_AUDIT_AUTHENTICATION.json','OPERATIONS_REVIEW01_FINDINGS.md','GWS_RETRY_SOURCE_AUDIT.md','OPERATIONS_REVIEW02_REPORT.md','OPERATIONS_REVIEW02_SEAL.json','ROOT_OPERATIONS_REVIEW02_ADJUDICATION.json','OPERATIONS_REVIEW03_REPORT.md','OPERATIONS_REVIEW03_SEAL.json','ROOT_OPERATIONS_REVIEW03_ADJUDICATION.json','CURRENT_OPERATIONAL_OPERATOR_PINS_V03.json','ROOT_OPERATIONAL_REPAIR_V03.json','OPERATIONAL_PUBLISHING_CLEARANCE.json']
files += [A/n for n in public_names]
optional=['ROOT_SHARED_PR73_RELEASE_VERIFICATION.json','ROOT_HEAD_RECONCILIATION_VERIFICATION.json','HEAD_RECONCILIATION_ATTEMPT.json','repaired_snapshot_manifest_before_shared_release.json','ROOT_SHARED_PR73_COORDINATION_RECORD.json']
files += [A/n for n in optional if (A/n).is_file()]
publication=['public_identity.py','run_zenodo_step.py','verify_public_record.py','append_tracker.py','PUBLICATION.md','PUBLIC_RECORD_VERIFICATION.json','TRACKER_COMPLETE.json','tracker_row_request.json','tracker_append_preexecution.json','tracker_append_execution.json','tracker_readback_preexecution.json','tracker_readback_execution.json']
for step in ['stage','inspect_draft','publish','inspect_published']:
 publication += [step+'_'+n+'.json' for n in ['preexecution','execution','receipt']]
files += [A/'publication'/n for n in publication]
files += [R/QUEUE,R/RELEASE]
allow=P/(NAME+'_allowlist.json')
paths={str(p.relative_to(R)) for p in files}|{str(allow.relative_to(R))}
assert all(p.is_file() and not p.is_symlink() for p in files)
q=load(A/'queue_publication_receipt.json');n=load(A/'native_publication_note_receipt.json')
assert sha(git('show','HEAD:'+QUEUE))==q['before_sha256'] and sha((R/QUEUE).read_bytes())==q['after_sha256']
assert q['only_pipe_cells']==[12] and q['all_other_queue_bytes_unchanged']
assert sha(git('show','HEAD:'+RELEASE))==n['original_release_sha256'] and sha((R/RELEASE).read_bytes())==n['published_release_sha256']
original=load(A/'snapshot_manifest.json')
for e in original['files']:
 if e['path']!=QUEUE:assert sha((R/e['path']).read_bytes())==e['sha256'] and not git('diff','--name-only','--',e['path'])
def foreign():
 idx={};bodies={}
 for item in git('ls-files','--stage','-z').split(b'\0'):
  if item:
   meta,path=item.split(b'\t',1)
   if path.decode() not in paths:idx.setdefault(path,[]).append(meta)
 for b in git('diff','--name-only','-z').split(b'\0'):
  if b and b.decode() not in paths:
   p=R/b.decode();bodies[b]=(p.exists(),p.read_bytes() if p.is_file() else None,stat.S_IMODE(p.stat().st_mode) if p.exists() else None)
 return idx,bodies
before=foreign();(D/'foreign_index_before.bin').write_bytes(git('ls-files','--stage','-z'))
bodypins={}
for rel,(exists,raw,mode) in before[1].items():
 e=dict(exists=exists,mode=mode,body_file=None)
 if raw is not None:
  name=sha(rel)+'.body';(D/name).write_bytes(raw);e.update(body_file=name,bytes=len(raw),sha256=sha(raw))
 bodypins[rel.decode()]=e
(D/'foreign_baseline.json').write_text(json.dumps(dict(utc=utc(),index={k.decode():[v.decode() for v in vs] for k,vs in before[0].items()},dirty_bodies=bodypins),indent=2)+'\n')
selected={str(p.relative_to(R)):pin(p) for p in files}
assert selected[QUEUE]['sha256']==q['after_sha256']
assert selected[RELEASE]['sha256']==n['published_release_sha256']
allow.write_text(json.dumps(dict(utc=utc(),paths=sorted(paths),pins=selected,math_percent=100,bounded_priority_percent=100,workflow_percent=100,publication_DOI=result['doi'],goal_complete=False),indent=2)+'\n')
# The allowlist cannot contain its own checksum. Freeze its completed bytes too.
expected=dict(selected)
expected[str(allow.relative_to(R))]=pin(allow)
(D/'frozen_selected_pins.json').write_text(json.dumps(expected,indent=2)+'\n')
staged=None;commit=None
for phase,args in [('stage',['/usr/bin/git','add','--',*sorted(paths)]),
                   ('commit',None),
                   ('advance_main',None),
                   ('push',['/usr/bin/git','push','origin','main'])]:
 window();current_clearance();assert foreign()==before
 live_pins(R,expected)
 assert git('branch','--show-current')==b'main\n'
 if phase in {'stage','commit','advance_main'}:
  assert git('rev-parse','HEAD').decode().strip()==parent
 else:
  assert git('rev-parse','HEAD').decode().strip()==commit
 assert git('ls-remote','origin','refs/heads/main').decode().split()[0]==parent
 if phase=='stage':assert not git('diff','--cached','--raw','-z')
 if phase=='commit':
  assert staged_tree(git,parent,expected)==staged
  args=['/usr/bin/git','commit-tree',staged,'-p',parent,'-m','Publish verified PR311 research note and register exact DOI tracker row']
 if phase=='advance_main':
  assert staged_tree(git,parent,expected)==staged
  committed_tree(git,commit,parent,staged,expected)
  args=['/usr/bin/git','update-ref','refs/heads/main',commit,parent]
 if phase=='push':
  committed_tree(git,commit,parent,staged,expected)
  # Exact object payload plus server-side expected-old-ref protection. The
  # verified parent is the expected old ref, so this update is a fast-forward.
  args=['/usr/bin/git','push','--force-with-lease=refs/heads/main:'+parent,'origin',commit+':refs/heads/main']
 rec=dict(argv=args,cwd=str(R),started_utc=utc(),operator_sha256=sha(Path(__file__).read_bytes()))
 (D/(phase+'_preexecution.json')).write_text(json.dumps(rec,indent=2)+'\n')
 run=subprocess.run(args,cwd=R,capture_output=True)
 for kind,raw in [('stdout',run.stdout),('stderr',run.stderr)]: (D/(phase+'.'+kind)).write_bytes(raw)
 rec.update(ended_utc=utc(),exit_code=run.returncode,stdout_bytes=len(run.stdout),stderr_bytes=len(run.stderr),stdout_sha256=sha(run.stdout),stderr_sha256=sha(run.stderr))
 (D/(phase+'_execution.json')).write_text(json.dumps(rec,indent=2)+'\n')
 assert run.returncode==0 and foreign()==before
 live_pins(R,expected)
 if phase=='stage':
  staged=staged_tree(git,parent,expected)
  (D/'verified_staged_tree.json').write_text(json.dumps(dict(utc=utc(),tree=staged,parent=parent,pins=expected),indent=2)+'\n')
 if phase=='commit':
  commit=run.stdout.decode().strip()
  assert len(commit)==40 and all(c in '0123456789abcdef' for c in commit)
  committed_tree(git,commit,parent,staged,expected)
  assert git('rev-parse','HEAD').decode().strip()==parent
 if phase=='advance_main':
  assert git('rev-parse','HEAD').decode().strip()==commit
  committed_tree(git,commit,parent,staged,expected)
  assert not git('diff','--cached','--raw','-z')
head=git('rev-parse','HEAD').decode().strip()
changed=set(git('diff-tree','--no-commit-id','--name-only','-r',head).decode().splitlines())
assert changed<=paths and git('ls-remote','origin','refs/heads/main').decode().split()[0]==head
live_pins(R,expected)
committed_tree(git,head,parent,staged,expected)
assert not git('diff','--cached','--raw','-z') and foreign()==before
current_clearance()
receipt=dict(utc=utc(),status='PASS_PR311_PUBLICATION_COMPLETION_CHECKPOINT_PUSHED',parent=parent,commit=head,changed_paths=len(changed),allowlist_paths=len(paths),fixed_verified_tree_commit_and_CAS_main_advance=True,exact_commit_refspec_and_expected_remote_parent_lease=True,lease_update_verified_fast_forward=True,foreign_index_never_rewritten_or_consumed=True,exact_reviewed_live_staged_committed_pins_verified_before_push=True,verified_staged_tree=staged,foreign_index_body_modes_preserved=True,entire_index_empty=True,remote_main_exact=True,math_percent=100,bounded_priority_percent=100,workflow_percent=100,doi=result['doi'],zenodo_record=result['zenodo_record'],tracker_range=result['tracker_range'],goal_complete=False,captures=str(D))
(P/(NAME+'_receipt.json')).write_text(json.dumps(receipt,indent=2)+'\n')
s=load(P/'SHARED_GIT_WINDOW_STATUS.json');s.update(utc=utc(),descending_git_checkpoint_preparing=False,descending_final_acceptance_preparing=False,last_owned_checkpoint=head,last_owned_checkpoint_pushed=True,descending_311_complete=True)
(P/'SHARED_GIT_WINDOW_STATUS.json').write_text(json.dumps(s,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
