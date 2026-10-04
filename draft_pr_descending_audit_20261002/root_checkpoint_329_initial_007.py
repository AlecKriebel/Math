"""Publish only root-owned PR329 intake/audit checkpoint, preserving foreign state."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,subprocess
P=Path(__file__).resolve().parent;R=P.parent;A=P/'audits/pr329_20000450'
PREFIX='checkpoint_329_initial_007'
utc=lambda:datetime.now(timezone.utc).isoformat();sha=lambda b:hashlib.sha256(b).hexdigest()
load=lambda p:json.loads(p.read_bytes())
def window():assert not load(P/'SHARED_GIT_WINDOW_STATUS.json')['shared_git_writes_paused']
assert not (P/(PREFIX+'_receipt.json')).exists() and not (P/(PREFIX+'_stage.json')).exists()
assert load(A/'ROOT_LOCAL_GIT_VERIFICATION.json')['status']=='PASS_COMPLETE_PR329_LOCAL_GIT_DIFF_BLOBS_MODES_MATCH_FROZEN_API'
paths=set()
def add(p):
    assert p.is_file() and not p.is_symlink() and p.resolve().is_relative_to(P)
    assert not any(part.startswith('private_') or part.endswith('_private') or part in {'__pycache__','.runtime'} for part in p.relative_to(R).parts)
    paths.add(str(p.relative_to(R)))
for n in ['RESEARCH_LOG.md','SHARED_GIT_WINDOW_STATUS.json','inventory.json','STATUS_FILTER_LEDGER.json',
          'checkpoint_344_completion_006_receipt.json','root_prepare_329_checkpoint_007.py',Path(__file__).name]:add(P/n)
for p in A.iterdir():
    if p.is_file() and not p.name.startswith('.'):add(p)
allow=P/(PREFIX+'_allowlist.json');paths.add(str(allow.relative_to(R)))
allow.write_text(json.dumps({'utc':utc(),'paths':sorted(paths),'math_percent':45,'workflow_percent':22,
    'scope':'Root-owned original-source, complete22-file/API/localGit freeze, first candidate audit and current native replay summaries. Active/arithmetic/division/geometry namespaces, private raw source/API/Git/run streams, original snapshot bodies and runtime excluded. No329 acceptance/merge/paper/publication.'},indent=2)+'\n')
def git(*args):return subprocess.check_output(['git',*args],cwd=R,env=dict(os.environ,GIT_OPTIONAL_LOCKS='0'))
assert git('branch','--show-current')==b'main\n'
assert not git('diff','--name-only','--diff-filter=U') and not git('diff','--cached','--raw','-z')
assert subprocess.run(['git','rev-parse','-q','--verify','MERGE_HEAD'],cwd=R,capture_output=True).returncode!=0
def foreign():
    entries={};bodies={}
    for item in git('ls-files','--stage','-z').split(b'\0'):
        if item:
            meta,name=item.split(b'\t',1)
            if name.decode() not in paths:entries.setdefault(name,[]).append(meta)
    for name in git('diff','--name-only','-z').split(b'\0'):
        if name and name.decode() not in paths:
            f=R/name.decode();bodies[name]={'exists':f.exists(),'bytes':f.read_bytes() if f.is_file() else None,'mode':f.stat().st_mode&0o7777 if f.exists() else None}
    return entries,bodies
window();before=foreign();parent=git('rev-parse','HEAD').decode().strip()
assert parent=='bd5c59ad2b9f2c57c82aa1fe7b0466fe3ea92e1b'
assert git('ls-remote','origin','refs/heads/main').decode().split()[0]==parent
for label,argv in [('stage',['git','add','-f','--',*sorted(paths)]),
   ('commit',['git','commit','--only','-m','Checkpoint source-first adversarial audit of PR329 pentagonal torsion','--',*sorted(paths)]),
   ('push',['git','push','origin','main'])]:
    window();started=utc();(P/(PREFIX+'_'+label+'_preexecution.json')).write_text(json.dumps({'utc':started,'argv':argv,'orchestrator_sha256':sha(Path(__file__).read_bytes())},indent=2)+'\n')
    r=subprocess.run(argv,cwd=R,capture_output=True)
    for k,b in [('stdout',r.stdout),('stderr',r.stderr)]: (P/(PREFIX+'_'+label+'.'+k)).write_bytes(b)
    (P/(PREFIX+'_'+label+'.json')).write_text(json.dumps({'argv':argv,'started_utc':started,'ended_utc':utc(),'exit_code':r.returncode,'stdout_sha256':sha(r.stdout),'stderr_sha256':sha(r.stderr)},indent=2)+'\n')
    assert r.returncode==0,(label,r.stderr.decode(errors='replace'));assert foreign()==before
commit=git('rev-parse','HEAD').decode().strip()
changed=set(git('diff-tree','--no-commit-id','--name-only','-r',commit).decode().splitlines());assert changed<=paths
assert git('ls-remote','origin','refs/heads/main').decode().split()[0]==commit
for p in paths:
    f=R/p;assert git('show',commit+':'+p)==f.read_bytes()
    mode=git('ls-tree',commit,'--',p).decode().split()[0];assert mode==('100755' if f.stat().st_mode&0o111 else '100644')
assert not git('diff','--cached','--raw','-z')
j={'utc':utc(),'status':'PASS_PR329_INITIAL_AUDIT_CHECKPOINT_PUSHED','parent':parent,'commit':commit,
    'changed_owned_paths':len(changed),'allowlist_paths':len(paths),'all_allowlisted_Git_disk_bytes_modes_equal':True,
    'remote_main_exact':True,'entire_index_empty':True,'foreign_index_dirty_bodies_modes_preserved':True,
    'mathematical_verification_percent':45,'workflow_percent':22,'priority_or_publication_clearance':False,'persistent_goal_complete':False}
(P/(PREFIX+'_receipt.json')).write_text(json.dumps(j,indent=2)+'\n')
s=load(P/'SHARED_GIT_WINDOW_STATUS.json');s.update(utc=utc(),last_owned_checkpoint=commit,last_owned_checkpoint_pushed=True,descending_git_checkpoint_preparing=False)
(P/'SHARED_GIT_WINDOW_STATUS.json').write_text(json.dumps(s,indent=2)+'\n')
with (P/'RESEARCH_LOG.md').open('a') as f:f.write('\n'+utc()+' — PR329 initial adversarial audit checkpoint pushed '+commit+'. Foreign index/dirty tracked bodies/modes preserved; remote/main and all scoped bytes/modes exact. Math45%, workflow22%; full mathematics/priority/paper/publication remain pending, original1/5 unchanged.\n')
print(json.dumps(j,indent=2))
