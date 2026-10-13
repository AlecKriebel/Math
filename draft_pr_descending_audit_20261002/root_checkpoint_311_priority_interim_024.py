"""One-shot scoped interim checkpoint before the ascending exclusive writer window."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,subprocess,stat
P=Path(__file__).resolve().parent;R=P.parent;A=P/'audits/pr311_30005303';NAME='checkpoint_311_priority_interim_024'
sha=lambda b:hashlib.sha256(b).hexdigest();utc=lambda:datetime.now(timezone.utc).isoformat();load=lambda p:json.loads(p.read_bytes())
D=P/('private_'+NAME);D.mkdir(exist_ok=False)
def req(c,label):
    if not c:raise RuntimeError(label)
def git(*args):return subprocess.check_output(['/usr/bin/git',*args],cwd=R,env=dict(os.environ,GIT_OPTIONAL_LOCKS='0'))
def window():req(not load(P/'SHARED_GIT_WINDOW_STATUS.json')['shared_git_writes_paused'],'Shared window already paused')
window();req(git('branch','--show-current')==b'main\n' and not git('diff','--cached','--raw','-z'),'Wrong branch/index')
parent=git('rev-parse','HEAD').decode().strip();req(parent=='84dd5af8ee06c08a0c0a0b7147aeec005d4160a3','Unexpected parent')
req(git('ls-remote','origin','refs/heads/main').decode().split()[0]==parent,'Remote differs')
req(load(A/'ROOT_PRIORITY_LAW_CHECKS.json')['status']=='PASS_PRIOR_LAWS_AND_EXACT_SUBMITTED_ROTATION','Law verification missing')
files=[P/n for n in ['RESEARCH_LOG.md','SHARED_GIT_WINDOW_STATUS.json','checkpoint_311_math_023_receipt.json',Path(__file__).name]]
files += [A/n for n in ['RESEARCH_LOG.md','ROOT_PRIORITY_INTERIM.md','ROOT_PRIORITY_LAW_CHECKS.json','root_verify_priority_laws.py','ROOT_PRIORITY_PAGE_RENDERS.json','root_render_priority_pages.py']]
allow=P/(NAME+'_allowlist.json');paths={str(p.relative_to(R)) for p in files}|{str(allow.relative_to(R))}
def foreign():
    index={};bodies={}
    for item in git('ls-files','--stage','-z').split(b'\0'):
        if item:
            meta,path=item.split(b'\t',1)
            if path.decode() not in paths:index.setdefault(path,[]).append(meta)
    for path in git('diff','--name-only','-z').split(b'\0'):
        if path and path.decode() not in paths:
            p=R/path.decode();bodies[path]=(p.exists(),p.read_bytes() if p.is_file() else None,stat.S_IMODE(p.stat().st_mode) if p.exists() else None)
    return index,bodies
before=foreign();stamp=utc()
shared=load(P/'SHARED_GIT_WINDOW_STATUS.json');shared.update(utc=stamp,descending_git_checkpoint_preparing=True,descending_311_priority_percent=50,
    descending_311_workflow_percent=40,descending_checkpoint_scope='Interim C2/C3 exact primary-law attribution; C1 priority remains pending. Preparing exclusive PR66 window.')
(P/'SHARED_GIT_WINDOW_STATUS.json').write_text(json.dumps(shared,indent=2)+'\n')
for p in [P/'RESEARCH_LOG.md',A/'RESEARCH_LOG.md']:
    with p.open('a') as f:f.write('\n'+stamp+' — PR311 interim priority checkpoint: independent root exact16-cell rotation of Gandolfi–Lenarda Lemma5.2, publication13April2017, full MTP2/global-Markov/quartic checks and seven primary pages visually read. C2/C3 qualifying prior accepted; C1 historical comparison pending. Math100%, priority50%, workflow40%; no publication/merge. Saving before requested exclusive PR66 Git window.\n')
req(all(p.is_file() and not p.is_symlink() for p in files),'Missing selected file')
allow.write_text(json.dumps(dict(utc=utc(),paths=sorted(paths),pins={str(p.relative_to(R)):dict(bytes=p.stat().st_size,sha256=sha(p.read_bytes())) for p in files},
    mathematical_percent=100,priority_percent=50,workflow_percent=40,publication_clearance=False),indent=2)+'\n')
for phase,args in [('stage',['/usr/bin/git','add','--',*sorted(paths)]),('commit',['/usr/bin/git','commit','--only','-m','Record exact prior C4 attribution in PR311 priority audit','--',*sorted(paths)]),('push',['/usr/bin/git','push','origin','main'])]:
    window();req(foreign()==before,'Foreign change before '+phase)
    j=dict(argv=args,cwd=str(R),started_utc=utc(),program_sha256=sha(Path(__file__).read_bytes()))
    (D/(phase+'_preexecution.json')).write_text(json.dumps(j,indent=2)+'\n');r=subprocess.run(args,cwd=R,capture_output=True)
    for k,b in [('stdout',r.stdout),('stderr',r.stderr)]: (D/(phase+'.'+k)).write_bytes(b)
    j.update(ended_utc=utc(),exit_code=r.returncode,stdout_sha256=sha(r.stdout),stderr_sha256=sha(r.stderr));(D/(phase+'.json')).write_text(json.dumps(j,indent=2)+'\n')
    req(r.returncode==0,phase+' failed');req(foreign()==before,'Foreign change after '+phase)
head=git('rev-parse','HEAD').decode().strip();changed=set(git('diff-tree','--no-commit-id','--name-only','-r',head).decode().splitlines())
req(changed<=paths and git('ls-remote','origin','refs/heads/main').decode().split()[0]==head,'Scope/remote mismatch')
req(all(git('show',head+':'+rel)==(R/rel).read_bytes() for rel in paths),'Published body mismatch')
req(not git('diff','--cached','--raw','-z') and foreign()==before,'Foreign/index mismatch')
j=dict(utc=utc(),status='PASS_PR311_INTERIM_PRIORITY_CHECKPOINT_PUSHED',parent=parent,commit=head,changed_paths=len(changed),allowlist_paths=len(paths),
    entire_index_empty=True,remote_main_exact=True,foreign_index_body_modes_preserved=True,mathematical_percent=100,priority_percent=50,workflow_percent=40,
    priority_complete=False,publication_ready=False,goal_complete=False,captures=str(D))
(P/(NAME+'_receipt.json')).write_text(json.dumps(j,indent=2)+'\n')
shared=load(P/'SHARED_GIT_WINDOW_STATUS.json');shared.update(utc=utc(),descending_git_checkpoint_preparing=False,last_owned_checkpoint=head,last_owned_checkpoint_pushed=True)
(P/'SHARED_GIT_WINDOW_STATUS.json').write_text(json.dumps(shared,indent=2)+'\n');print(json.dumps(j,indent=2))
