"""Save the prepared manuscript and closed priority verdict before shared integration."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,os,subprocess,stat
P=Path(__file__).resolve().parent;R=P.parent;A=P/'audits/pr311_30005303';NAME='checkpoint_311_preprint_026'
sha=lambda b:hashlib.sha256(b).hexdigest();utc=lambda:datetime.now(timezone.utc).isoformat();load=lambda p:json.loads(p.read_bytes())
D=P/('private_'+NAME);D.mkdir(exist_ok=False)
def req(c,message):
 if not c:raise RuntimeError(message)
def git(*args):return subprocess.check_output(['/usr/bin/git',*args],cwd=R,env=dict(os.environ,GIT_OPTIONAL_LOCKS='0'))
def window():req(not load(P/'SHARED_GIT_WINDOW_STATUS.json')['shared_git_writes_paused'],'Git window held')
window();parent=git('rev-parse','HEAD').decode().strip()
req(parent=='997e5f160219b694aadb7fea95cd87a50462bbf6' and git('branch','--show-current')==b'main\n','Wrong head/branch')
req(not git('diff','--cached','--raw','-z') and git('ls-remote','origin','refs/heads/main').decode().split()[0]==parent,'Index/remote differs')
req(load(A/'ROOT_PRIORITY_DECISION_03.json')['bounded_priority_audit_percent']==100,'Priority not adjudicated')
req(load(A/'PREPRINT_PACKAGE_V01_PREPARATION.json')['replay']['exit_code']==0,'Portable reproduction not passed')
files=[P/n for n in ['RESEARCH_LOG.md','SHARED_GIT_WINDOW_STATUS.json','checkpoint_311_priority_025_receipt.json',Path(__file__).name]]
files += [A/n for n in ['.gitignore','RESEARCH_LOG.md','ROOT_PRIORITY_DECISION_03.json','root_finish_priority_03.py','PREPRINT_PACKAGE_V01_PREPARATION.json','root_freeze_preprint_package_v01.py','root_build_preprint_v01.py']]
files += [p for p in (A/'preprint_package_v01').rglob('*') if p.is_file()]
files += [p for p in (A/'closure_priority_adversary/public').iterdir() if p.is_file()]
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
 descending_311_priority_percent=100,descending_311_bounded_priority_audit_percent=100,descending_311_workflow_percent=55,
 descending_checkpoint_scope='Prepared five-page attributed PR311 characterization note and portable verification package; no full preprint-review or publication clearance.')
(P/'SHARED_GIT_WINDOW_STATUS.json').write_text(json.dumps(s,indent=2)+'\n')
for p in [P/'RESEARCH_LOG.md',A/'RESEARCH_LOG.md']:
 with p.open('a') as f:f.write('\n'+stamp+' — PR311 prepared preprint checkpoint: five-page standalone manuscript desktop/native compile passed, allfive renderedpages visually clear, portable11-input plusmanifest package frozen/reproduced,380exactnetwork/5495assignment controls passed. Three independent mathematical/priority families support fully attributed general characterization; boundedpriority100%,math100%,workflow55%. No full preprint adversary yet and no publication/merge. Saving before requested exclusive PR66 attributed-prior integration window.\n')
allow.write_text(json.dumps(dict(utc=utc(),paths=sorted(paths),pins={str(p.relative_to(R)):dict(bytes=p.stat().st_size,sha256=sha(p.read_bytes()),mode=oct(stat.S_IMODE(p.stat().st_mode))) for p in files},
 math_percent=100,bounded_priority_percent=100,workflow_percent=55,publication_ready=False),indent=2)+'\n')
for phase,args in [('stage',['/usr/bin/git','add','--',*sorted(paths)]),('commit',['/usr/bin/git','commit','--only','-m','Prepare attributed PR311 closure note and exact verification package','--',*sorted(paths)]),('push',['/usr/bin/git','push','origin','main'])]:
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
j=dict(utc=utc(),status='PASS_PR311_PREPARED_PREPRINT_CHECKPOINT_PUSHED',parent=parent,commit=head,changed_paths=len(changed),allowlist_paths=len(paths),
 entire_index_empty=True,remote_main_exact=True,foreign_index_body_modes_preserved=True,math_percent=100,bounded_priority_percent=100,workflow_percent=55,
 preprint_ready=False,immutable_publication_clearance=False,goal_complete=False,captures=str(D))
(P/(NAME+'_receipt.json')).write_text(json.dumps(j,indent=2)+'\n')
s=load(P/'SHARED_GIT_WINDOW_STATUS.json');s.update(utc=utc(),descending_git_checkpoint_preparing=False,last_owned_checkpoint=head,last_owned_checkpoint_pushed=True)
(P/'SHARED_GIT_WINDOW_STATUS.json').write_text(json.dumps(s,indent=2)+'\n');print(json.dumps(j,indent=2))
