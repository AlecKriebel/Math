"""Checkpoint the second source gate and gated publication preparation."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,os,subprocess,stat
P=Path(__file__).resolve().parent;R=P.parent;A=P/'audits/pr311_30005303';NAME='checkpoint_311_publication_preparation_029'
sha=lambda b:hashlib.sha256(b).hexdigest();utc=lambda:datetime.now(timezone.utc).isoformat();load=lambda p:json.loads(p.read_bytes())
D=P/('private_'+NAME);D.mkdir(exist_ok=False)
def req(c,message):
 if not c:raise RuntimeError(message)
def git(*args):return subprocess.check_output(['/usr/bin/git',*args],cwd=R,env=dict(os.environ,GIT_OPTIONAL_LOCKS='0'))
def window():req(not load(P/'SHARED_GIT_WINDOW_STATUS.json')['shared_git_writes_paused'],'Git window held')
window();parent=git('rev-parse','HEAD').decode().strip()
req(parent=='3d577b9c99c83aeae38f933f423dac3332dce5cc' and git('branch','--show-current')==b'main\n','Wrong head/branch')
req(not git('diff','--cached','--raw','-z') and git('ls-remote','origin','refs/heads/main').decode().split()[0]==parent,'Index/remote differs')
req(load(A/'ROOT_PRIORITY_DECISION_03.json')['bounded_priority_audit_percent']==100,'Priority not adjudicated')
req(load(A/'ROOT_PREPRINT_REPAIR_V02.json')['status']=='PASS_V02_LABEL_REPAIRS_AND_PORTABLE_SUBMISSION_PREPARATION','Repair/reproduction not passed')
req(load(A/'ROOT_PREPRINT01_ADJUDICATION.json')['sealed_review_authenticated'],'First review not authenticated')
files=[P/n for n in ['RESEARCH_LOG.md','SHARED_GIT_WINDOW_STATUS.json','checkpoint_311_review_repairs_028_receipt.json',Path(__file__).name]]
files += [A/n for n in ['README.md','RESEARCH_LOG.md','CURRENT_PACKAGE_STATUS.json','ROOT_PREPRINT02_SOURCE_GATE.json','root_preprint02_source_gate.py','ROOT_OPERATIONAL_PREPARATION_V02.json','root_submission_gate.py','root_refresh_claimed_queue.py','root_integrate_claimed.py','root_verify_post_merge.py','publication/run_zenodo_step.py','publication/verify_public_record.py','publication/append_tracker.py','accepted_pr_body.txt','merge_body.txt']]
allow=P/(NAME+'_allowlist.json');paths={str(p.relative_to(R)) for p in files}|{str(allow.relative_to(R))}
req(all(p.is_file() and not p.is_symlink() for p in files),'Selected path missing/symlink')
def foreign():
 index={};body={}
 for item in git('ls-files','--stage','-z').split(b'\0'):
  if item:
   meta,path=item.split(b'\t',1)
   if path.decode() not in paths:index.setdefault(path,[]).append(meta)
 for path in git('diff','--name-only','-z').split(b'\0'):
  if path and path.decode() not in paths:
   p=R/path.decode();body[path]=(p.exists(),p.read_bytes() if p.is_file() else None,stat.S_IMODE(p.stat().st_mode) if p.exists() else None)
 return index,body
before=foreign();stamp=utc()
s=load(P/'SHARED_GIT_WINDOW_STATUS.json');s.update(utc=stamp,descending_git_checkpoint_preparing=True,descending_311_priority_complete=True,
 descending_311_priority_percent=100,descending_311_bounded_priority_audit_percent=100,descending_311_workflow_percent=65,
 descending_checkpoint_scope='Second source-only gate authenticated, exactly31 named package/submission/historical-build inputs released for NEW full review; merge/publication operators prepared only. Active second-reviewer namespace excluded, no publication clearance.')
(P/'SHARED_GIT_WINDOW_STATUS.json').write_text(json.dumps(s,indent=2)+'\n')
for p in [P/'RESEARCH_LOG.md',A/'RESEARCH_LOG.md']:
 with p.open('a') as f:f.write('\n'+stamp+' — PR311 prepared publication checkpoint: second source-only gate and27evidence/report pins authenticated; exactly31named v02 package/submission/original-build inputs released for NEWfullreview. Seven prepared operators syntaxchecked,hard-gated by absent finalclearance. Original29files/2of5authorhistory and narrow own QUEUE updates are bound by planned immutable-object integration; no native state/history rewriting or additional authorsearch. Production deposit and exact-once GWS append operators require actual merge, whole-file public readback and fresh duplicate/layout checks. Active review02 namespace excluded. Math100%,boundedpriority100%,workflow65%; no publication/merge clearance.\n')
allow.write_text(json.dumps(dict(utc=utc(),paths=sorted(paths),pins={str(p.relative_to(R)):dict(bytes=p.stat().st_size,sha256=sha(p.read_bytes()),mode=oct(stat.S_IMODE(p.stat().st_mode))) for p in files},
 math_percent=100,bounded_priority_percent=100,workflow_percent=65,publication_ready=False),indent=2)+'\n')
for phase,args in [('stage',['/usr/bin/git','add','--',*sorted(paths)]),('commit',['/usr/bin/git','commit','--only','-m','Prepare guarded PR311 publication after second source-only review gate','--',*sorted(paths)]),('push',['/usr/bin/git','push','origin','main'])]:
 window();req(foreign()==before,'Foreign change before '+phase)
 j=dict(argv=args,cwd=str(R),started_utc=utc(),operator_sha256=sha(Path(__file__).read_bytes()))
 (D/(phase+'_spec.json')).write_text(json.dumps(j,indent=2)+'\n');r=subprocess.run(args,cwd=R,capture_output=True)
 for k,b in [('stdout',r.stdout),('stderr',r.stderr)]: (D/(phase+'.'+k)).write_bytes(b)
 j.update(ended_utc=utc(),exit_code=r.returncode,stdout_sha256=sha(r.stdout),stderr_sha256=sha(r.stderr));(D/(phase+'_execution.json')).write_text(json.dumps(j,indent=2)+'\n')
 req(r.returncode==0 and foreign()==before,'Phase failed or foreign mutation '+phase)
head=git('rev-parse','HEAD').decode().strip();changed=set(git('diff-tree','--no-commit-id','--name-only','-r',head).decode().splitlines())
req(changed<=paths and git('ls-remote','origin','refs/heads/main').decode().split()[0]==head,'Scope/remote mismatch')
req(all(git('show',head+':'+rel)==(R/rel).read_bytes() for rel in paths),'Commit body mismatch')
req(not git('diff','--cached','--raw','-z') and foreign()==before,'Index/foreign mismatch')
j=dict(utc=utc(),status='PASS_PR311_PUBLICATION_PREPARATION_CHECKPOINT_PUSHED',parent=parent,commit=head,changed_paths=len(changed),allowlist_paths=len(paths),
 entire_index_empty=True,remote_main_exact=True,foreign_index_body_modes_preserved=True,math_percent=100,bounded_priority_percent=100,workflow_percent=65,
 preprint_ready=False,immutable_publication_clearance=False,goal_complete=False,captures=str(D))
(P/(NAME+'_receipt.json')).write_text(json.dumps(j,indent=2)+'\n')
s=load(P/'SHARED_GIT_WINDOW_STATUS.json');s.update(utc=utc(),descending_git_checkpoint_preparing=False,last_owned_checkpoint=head,last_owned_checkpoint_pushed=True)
(P/'SHARED_GIT_WINDOW_STATUS.json').write_text(json.dumps(s,indent=2)+'\n');print(json.dumps(j,indent=2))
