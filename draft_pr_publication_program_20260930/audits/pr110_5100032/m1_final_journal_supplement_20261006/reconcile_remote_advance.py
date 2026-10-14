from pathlib import Path
import datetime,hashlib,json,os,subprocess
D=Path(__file__).resolve().parent;A=D.parent;C=A.parents[2]
E=D/'remote_reconciliation';E.mkdir(exist_ok=False)
old='c40562362d60cce52a3128fa17313ad729f0d835';records=[]
def require(c,m):
 if not c:raise RuntimeError(m)
def git(*args):
 start=datetime.datetime.now(datetime.timezone.utc).isoformat();p=subprocess.Popen(['git',*args],cwd=C,stdout=subprocess.PIPE,stderr=subprocess.PIPE);o,e=p.communicate();i=len(records)
 for name,b in [('stdout',o),('stderr',e)]:(E/(str(i)+'.'+name+'.bin')).write_bytes(b)
 records.append({'argv':['git',*args],'PID':p.pid,'UTC_start':start,'UTC_end':datetime.datetime.now(datetime.timezone.utc).isoformat(),'exit_code':p.returncode,'stdout_bytes':len(o),'stderr_bytes':len(e),'stdout_sha256':hashlib.sha256(o).hexdigest(),'stderr_sha256':hashlib.sha256(e).hexdigest()})
 (E/'PROCESS_JOURNAL.json').write_text(json.dumps(records,indent=2)+'\n');require(p.returncode==0,e.decode());return o
new=git('rev-parse','origin/main').decode().strip();git('merge-base','--is-ancestor',old,new)
changed=[x.decode() for x in git('diff','--name-only','-z',old,new).split(b'\0') if x]
require(not any(x.startswith('draft_pr_publication_program_20260930/') or Path(x).name=='AGENTS.md' for x in changed),'scope/policy collision')
require(git('symbolic-ref','--short','HEAD').strip()==b'main' and git('rev-parse','HEAD').decode().strip()==old,'HEAD')
require(not git('diff','--cached','--name-only','-z'),'index')
require(git('ls-remote','https://github.com/AlecKriebel/Math.git','refs/heads/main').decode().split()[0]==new,'remote moved again')
pins=[]
for rel in json.loads((D/'CHECKPOINT_SELECTION.json').read_text())['paths']:
 b=(C/rel).read_bytes();pins.append({'file':rel,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()})
git('merge','--ff-only',new)
require(git('rev-parse','HEAD').decode().strip()==new and not git('diff','--cached','--name-only','-z'),'readback')
for row in pins:
 b=(C/row['file']).read_bytes();require(len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256'],'own body changed')
r={'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_operator_PID':os.getpid(),'old':old,'new':new,'branch':'main','remote_changed_paths':changed,'own_selected_full_bodies_preserved':pins,'no_program_or_policy_collision':True,'index_empty':True,'primary_checkout_mutated':False,'remote_mutated':False,'workflow_percent':35,'publication_percent':0}
(E/'RECEIPT.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:v for k,v in r.items() if k!='own_selected_full_bodies_preserved'}))
