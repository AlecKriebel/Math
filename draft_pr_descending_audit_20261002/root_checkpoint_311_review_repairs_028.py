"""Checkpoint the fully repaired version and closed first preprint review."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,os,subprocess,stat
P=Path(__file__).resolve().parent;R=P.parent;A=P/'audits/pr311_30005303';NAME='checkpoint_311_review_repairs_028'
sha=lambda b:hashlib.sha256(b).hexdigest();utc=lambda:datetime.now(timezone.utc).isoformat();load=lambda p:json.loads(p.read_bytes())
D=P/('private_'+NAME);D.mkdir(exist_ok=False)
def req(c,message):
 if not c:raise RuntimeError(message)
def git(*args):return subprocess.check_output(['/usr/bin/git',*args],cwd=R,env=dict(os.environ,GIT_OPTIONAL_LOCKS='0'))
def window():req(not load(P/'SHARED_GIT_WINDOW_STATUS.json')['shared_git_writes_paused'],'Git window held')
window();parent=git('rev-parse','HEAD').decode().strip()
req(parent=='4f20301ee01f17de150192852d84c77a4ab51ee6' and git('branch','--show-current')==b'main\n','Wrong head/branch')
req(not git('diff','--cached','--raw','-z') and git('ls-remote','origin','refs/heads/main').decode().split()[0]==parent,'Index/remote differs')
req(load(A/'ROOT_PRIORITY_DECISION_03.json')['bounded_priority_audit_percent']==100,'Priority not adjudicated')
req(load(A/'ROOT_PREPRINT_REPAIR_V02.json')['status']=='PASS_V02_LABEL_REPAIRS_AND_PORTABLE_SUBMISSION_PREPARATION','Repair/reproduction not passed')
req(load(A/'ROOT_PREPRINT01_ADJUDICATION.json')['sealed_review_authenticated'],'First review not authenticated')
files=[P/n for n in ['RESEARCH_LOG.md','SHARED_GIT_WINDOW_STATUS.json','checkpoint_311_review_gate_027_receipt.json','root_pause_pr73_checkpoint_20261004.py','root_resume_pr73_checkpoint_20261004.py',Path(__file__).name]]
files += [A/n for n in ['README.md','RESEARCH_LOG.md','ROOT_PREPRINT01_ADJUDICATION.json','root_adjudicate_preprint01.py','ROOT_PREPRINT_REPAIR_V02.json','root_repair_freeze_preprint_v02.py','ROOT_CI_MINOR_COUNT_SCOPE_03.json','root_check_minor_count_labels_03.py','CURRENT_PACKAGE_STATUS.json','CURRENT_CORRECTIONS.json']]
files += [p for folder in ['preprint_package_v02','submission_v02'] for p in (A/folder).rglob('*') if p.is_file()]
files += [A/'preprint_review_01'/n for n in ['.gitignore','FINAL_REVIEW.md','FINAL_SEAL_MANIFEST.json','FINAL_SEAL_VERIFICATION.json','INDEPENDENT_CHECK_RESULTS.json','MUTANT_AND_DENSITY_RESULTS.json','ARTIFACT_COMPARISON_RESULTS.json','RESEARCH_LOG.md','independent_checks.py','mutant_controls.py','verify_artifacts.py','capture.py']]
files += [A/'publication_preparation/DRAFT_ZENODO_METADATA.json']
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
 descending_checkpoint_scope='Closed first whole preprint review, three repaired findings, globally clarified historical labels, portable v02 package and exact submission metadata; active second reviewer namespace excluded, no publication clearance.')
(P/'SHARED_GIT_WINDOW_STATUS.json').write_text(json.dumps(s,indent=2)+'\n')
for p in [P/'RESEARCH_LOG.md',A/'RESEARCH_LOG.md']:
 with p.open('a') as f:f.write('\n'+stamp+' — PR311 repaired preprint checkpoint: first complete fresh review root-read/authenticated,376sealed bodies plus9terminalfiles; no mathematical defect, R1–R3 corrected from authentic history and independent counts. All non-count law/invariant/recoding results unchanged; active and different-location reproductions pass,13archive members exactlymatch qualifiedv02, kitlocalcheck passes. Currentcorrectiondocket globally clarifies historical labels; NEWsecondreviewer startedsource-first after repairs. Math100%, boundedpriority100%,workflow65%; no second-review/publication/merge clearance. Closed review manifests inventory private/local files beyond the explicitly public-safe committed subset; no claim all inventory members are uploaded.\n')
allow.write_text(json.dumps(dict(utc=utc(),paths=sorted(paths),pins={str(p.relative_to(R)):dict(bytes=p.stat().st_size,sha256=sha(p.read_bytes()),mode=oct(stat.S_IMODE(p.stat().st_mode))) for p in files},
 math_percent=100,bounded_priority_percent=100,workflow_percent=65,publication_ready=False),indent=2)+'\n')
for phase,args in [('stage',['/usr/bin/git','add','--',*sorted(paths)]),('commit',['/usr/bin/git','commit','--only','-m','Repair PR311 preprint provenance and count scope after full adversarial review','--',*sorted(paths)]),('push',['/usr/bin/git','push','origin','main'])]:
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
j=dict(utc=utc(),status='PASS_PR311_REPAIRED_PREPRINT_CHECKPOINT_PUSHED',parent=parent,commit=head,changed_paths=len(changed),allowlist_paths=len(paths),
 entire_index_empty=True,remote_main_exact=True,foreign_index_body_modes_preserved=True,math_percent=100,bounded_priority_percent=100,workflow_percent=65,
 preprint_ready=False,immutable_publication_clearance=False,goal_complete=False,captures=str(D))
(P/(NAME+'_receipt.json')).write_text(json.dumps(j,indent=2)+'\n')
s=load(P/'SHARED_GIT_WINDOW_STATUS.json');s.update(utc=utc(),descending_git_checkpoint_preparing=False,last_owned_checkpoint=head,last_owned_checkpoint_pushed=True)
(P/'SHARED_GIT_WINDOW_STATUS.json').write_text(json.dumps(s,indent=2)+'\n');print(json.dumps(j,indent=2))
