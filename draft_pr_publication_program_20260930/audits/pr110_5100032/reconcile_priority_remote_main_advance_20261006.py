from pathlib import Path
import datetime,hashlib,json,os,subprocess
A=Path(__file__).resolve().parent; C=A.parents[2]
D=A/'priority_remote_main_reconciliation_20261006';D.mkdir(exist_ok=False)
old='18bafd0d6a15a26b4897bec8ec15a69e30b0a23e'
records=[]
def require(c,m):
    if not c:raise RuntimeError(m)
def git(*args):
    start=datetime.datetime.now(datetime.timezone.utc).isoformat()
    p=subprocess.Popen(['git',*args],cwd=C,stdout=subprocess.PIPE,stderr=subprocess.PIPE);o,e=p.communicate();n=len(records)
    for name,b in [('stdout',o),('stderr',e)]:(D/(str(n)+'.'+name+'.bin')).write_bytes(b)
    records.append({'argv':['git',*args],'PID':p.pid,'UTC_start':start,'UTC_end':datetime.datetime.now(datetime.timezone.utc).isoformat(),'exit_code':p.returncode,'stdout_bytes':len(o),'stderr_bytes':len(e),'stdout_sha256':hashlib.sha256(o).hexdigest(),'stderr_sha256':hashlib.sha256(e).hexdigest()})
    (D/'PROCESS_JOURNAL.json').write_text(json.dumps(records,indent=2)+'\n');require(p.returncode==0,e.decode());return o
new=git('rev-parse','refs/remotes/pr110-priority-main').decode().strip()
git('merge-base','--is-ancestor',old,new)
changed=[x.decode() for x in git('diff','--name-only','-z',old,new).split(b'\0') if x]
require(not any(x.startswith('draft_pr_publication_program_20260930/') or Path(x).name=='AGENTS.md' for x in changed),'program or policy collision')
require(git('symbolic-ref','--short','HEAD').strip()==b'main','branch')
require(git('rev-parse','HEAD').decode().strip()==old,'HEAD changed')
require(not git('diff','--cached','--name-only','-z'),'staged work')
require(git('ls-remote','https://github.com/AlecKriebel/Math.git','refs/heads/main').decode().split()[0]==new,'remote advanced again')
pins=[]
for relative in json.loads((A/'SOURCE_MATH_CHECKPOINT_SELECTION_20261006.json').read_text())['paths']:
    b=(C/relative).read_bytes();pins.append({'file':relative,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()})
commits=git('log','--format=%H %s',old+'..'+new).decode()
git('merge','--ff-only',new)
require(git('rev-parse','HEAD').decode().strip()==new and not git('diff','--cached','--name-only','-z'),'FF or index')
for row in pins:
    b=(C/row['file']).read_bytes();require(len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256'],'body changed')
r={'schema':'pr110-priority-remote-main-reconciliation/v1','UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_operator_PID':os.getpid(),'old':old,'new':new,'branch':'main','remote_changed_paths':changed,'no_program_or_policy_collision':True,'preserved_remote_commits':commits,'source_math_full_bodies_unchanged':pins,'index_empty':True,'primary_checkout_mutated':False,'remote_mutated':False,'new_central_proof_search_turns':0}
(D/'RECEIPT.json').write_text(json.dumps(r,indent=2,sort_keys=True)+'\n');print(json.dumps({k:v for k,v in r.items() if k!='source_math_full_bodies_unchanged'}))
