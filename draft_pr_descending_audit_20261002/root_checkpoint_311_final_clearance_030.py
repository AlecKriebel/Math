"""Checkpoint final clean whole-review02 and exact publishing clearance."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,os,subprocess,stat
P=Path(__file__).resolve().parent;R=P.parent;A=P/'audits/pr311_30005303';NAME='checkpoint_311_final_clearance_030'
sha=lambda b:hashlib.sha256(b).hexdigest();utc=lambda:datetime.now(timezone.utc).isoformat();load=lambda p:json.loads(p.read_bytes())
D=P/('private_'+NAME);D.mkdir(exist_ok=False)
def req(c,message):
 if not c:raise RuntimeError(message)
def git(*args):return subprocess.check_output(['/usr/bin/git',*args],cwd=R,env=dict(os.environ,GIT_OPTIONAL_LOCKS='0'))
def window():req(not load(P/'SHARED_GIT_WINDOW_STATUS.json')['shared_git_writes_paused'],'Git window held')
window();parent=git('rev-parse','HEAD').decode().strip()
req(parent=='29c5723c30d78825938e3782676d3e2bbe16a6bb' and git('branch','--show-current')==b'main\n','Wrong head/branch')
req(not git('diff','--cached','--raw','-z') and git('ls-remote','origin','refs/heads/main').decode().split()[0]==parent,'Index/remote differs')
req(load(A/'ROOT_PRIORITY_DECISION_03.json')['bounded_priority_audit_percent']==100,'Priority not adjudicated')
req(load(A/'ROOT_PREPRINT_REPAIR_V02.json')['status']=='PASS_V02_LABEL_REPAIRS_AND_PORTABLE_SUBMISSION_PREPARATION','Repair/reproduction not passed')
req(load(A/'ROOT_PREPRINT01_ADJUDICATION.json')['sealed_review_authenticated'],'First review not authenticated')
files=[P/n for n in ['RESEARCH_LOG.md','SHARED_GIT_WINDOW_STATUS.json','inventory.json','checkpoint_311_publication_preparation_029_receipt.json','root_recover_checkpoint_029_observation.py',Path(__file__).name]]
files += [A/n for n in ['README.md','RESEARCH_LOG.md','CURRENT_PACKAGE_STATUS.json','ROOT_OPERATIONAL_BASELINE_REPAIR.json','CURRENT_OPERATIONAL_OPERATOR_PINS.json','root_submission_gate.py','root_refresh_claimed_queue.py','root_integrate_claimed.py','root_record_publication_completion.py','ROOT_PREPRINT02_ARTIFACT_AUTHENTICATION.json','ROOT_PREPRINT02_ADJUDICATION.json','root_authenticate_reproduce_preprint02.py','ROOT_FINAL_CLOSED_EVIDENCE.json','root_bind_final_closed_evidence.py','root_create_publishing_clearance.py','PUBLISHING_CLEARANCE.json']]
files += [A/'preprint_review_02'/n for n in ['.gitignore','SOURCE_ONLY_CRITERIA.md','FIRST_INDEPENDENT_CONCLUSION.md','SOURCE_ONLY_FREEZE_MANIFEST.json','SOURCE_ONLY_FREEZE_VERIFICATION.json','FINAL_REVIEW_REPORT.md','FINAL_SEAL_MANIFEST.json','FINAL_SEAL_VERIFICATION.json','FINAL_CLOSURE_RECORD.json','PRIMARY_SOURCE_SCOPE.md','PRIMARY_SOURCE_PINS.json','INDEPENDENT_CHECKS.py','INDEPENDENT_CHECK_RESULTS.json','NEGATIVE_CONTROLS.py','NEGATIVE_CONTROL_RESULTS.json','AUDIT_PROVENANCE.py','PROVENANCE_CHECK_RESULTS.json','REBUILD_COMPARISON_RESULTS.json','NAMED_INPUTS_FINAL_CHECK.json','RESEARCH_LOG.md','VERIFY_FINAL_SEAL.py','CLOSE_REVIEW.py','SEAL_REVIEW.py']]
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
# Persist the exact foreign baseline before any mutation for later diagnosis.
foreign_index,foreign_bodies=before
(D/'foreign_index_before.bin').write_bytes(git('ls-files','--stage','-z','--','.'))
bodypins={}
for path,(exists,body,mode) in foreign_bodies.items():
 name=sha(path)+'.body';entry=dict(exists=exists,mode=mode,body_file=None)
 if body is not None:
  (D/name).write_bytes(body);entry.update(body_file=name,bytes=len(body),sha256=sha(body))
 bodypins[path.decode()]=entry
(D/'foreign_before.json').write_text(json.dumps(dict(utc=stamp,index_entries={k.decode():[x.decode() for x in v] for k,v in foreign_index.items()},dirty_bodies=bodypins),indent=2)+'\n')
s=load(P/'SHARED_GIT_WINDOW_STATUS.json');s.update(utc=stamp,descending_git_checkpoint_preparing=True,descending_311_priority_complete=True,
 descending_311_priority_percent=100,descending_311_bounded_priority_audit_percent=100,descending_311_workflow_percent=75,
 descending_checkpoint_scope='Final clean NEWwhole-review02 fullyroot-read and reproduced; exact v02 clearance binds1234readonly scientific/review files. Only closed public-safe review artifacts staged, no primary bodies/private streams uploaded. Merge/publication pending.')
(P/'SHARED_GIT_WINDOW_STATUS.json').write_text(json.dumps(s,indent=2)+'\n')
for p in [P/'RESEARCH_LOG.md',A/'RESEARCH_LOG.md']:
 with p.open('a') as f:f.write('\n'+stamp+' — PR311 final clearance checkpoint: NEWfullreview02 closed with zero required repairs; ROOT complete report/code/scientific-output/readscope and relevant full native streams read,457body+9terminal artifacts authenticated,31released inputs/sourcegate unchanged. Fresh root finite-verifier full2495-byte result and fresh portable archive agree; nine negative outcomes reproduce. All1234readonly scientific/review files and748prior seal rows bound. CP029 successful scoped push/post-push foreign-observation failure preserved honestly; future before body/index baselines persisted. Closed public-safe review subset selected; copyrighted sources/private captures excluded. Math100%,boundedpriority100%,workflow75%; exact original29/2of5 history retained; merge, production deposit and tracker registration pending.\n')
allow.write_text(json.dumps(dict(utc=utc(),paths=sorted(paths),pins={str(p.relative_to(R)):dict(bytes=p.stat().st_size,sha256=sha(p.read_bytes()),mode=oct(stat.S_IMODE(p.stat().st_mode))) for p in files},
 math_percent=100,bounded_priority_percent=100,workflow_percent=75,publication_ready=True),indent=2)+'\n')
for phase,args in [('stage',['/usr/bin/git','add','--',*sorted(paths)]),('commit',['/usr/bin/git','commit','--only','-m','Clear PR311 preprint after new complete adversarial review and reproduction','--',*sorted(paths)]),('push',['/usr/bin/git','push','origin','main'])]:
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
j=dict(utc=utc(),status='PASS_PR311_FINAL_CLEARANCE_CHECKPOINT_PUSHED',parent=parent,commit=head,changed_paths=len(changed),allowlist_paths=len(paths),
 entire_index_empty=True,remote_main_exact=True,foreign_index_body_modes_preserved=True,math_percent=100,bounded_priority_percent=100,workflow_percent=75,
 preprint_ready=True,immutable_publication_clearance=True,goal_complete=False,captures=str(D))
(P/(NAME+'_receipt.json')).write_text(json.dumps(j,indent=2)+'\n')
s=load(P/'SHARED_GIT_WINDOW_STATUS.json');s.update(utc=utc(),descending_git_checkpoint_preparing=False,last_owned_checkpoint=head,last_owned_checkpoint_pushed=True)
(P/'SHARED_GIT_WINDOW_STATUS.json').write_text(json.dumps(s,indent=2)+'\n');print(json.dumps(j,indent=2))
