#!/usr/bin/env python3
"""Commit only explicit owned paths on current remote main using an isolated index.
Does not move local HEAD, modify shared index/worktree, create branches or releases.
"""
import argparse,hashlib,json,os,pathlib,subprocess,tempfile,datetime
REPO=pathlib.Path('/Users/alec/Documents/Math')
PROJECT=REPO/'openai_followon_multispecies_vlasov_maxwell'
def run(args,env=None,data=None):
 return subprocess.check_output(['git',*args],cwd=REPO,env=env,input=data).decode().strip()
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else None
p=argparse.ArgumentParser();p.add_argument('--message',required=True);p.add_argument('--receipt',required=True);p.add_argument('paths',nargs='+');a=p.parse_args()
paths=[]
for arg in a.paths:
 f=(REPO/arg).resolve()
 if not f.is_relative_to(PROJECT) or not f.is_file():raise SystemExit('Only explicit existing owned project files allowed')
 if '/sources/upstream_pinned/' in str(f) or '/sources/triage/' in str(f):raise SystemExit('Audit source copies are not checkpoint files')
 paths.append((str(f.relative_to(REPO)),f.read_bytes(),f.stat().st_mode & 0o111))
head=run(['rev-parse','HEAD']);branch=run(['symbolic-ref','--short','HEAD'])
if branch!='main':raise SystemExit('Main-only policy requires shared checkout on main')
idx=pathlib.Path(run(['rev-parse','--git-path','index']));idx=idx if idx.is_absolute() else REPO/idx
before=digest(idx)
receipt={'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'message':a.message,'shared_head_before':head,'shared_index_sha256_before':before,'files':{n:hashlib.sha256(b).hexdigest() for n,b,x in paths},'attempts':[]}
with tempfile.TemporaryDirectory(prefix='private-index-',dir=PROJECT/'receipts') as td:
 env=os.environ.copy();env['GIT_INDEX_FILE']=str(pathlib.Path(td)/'index')
 for attempt in range(5):
  parent=run(['ls-remote','origin','refs/heads/main']).split()[0]
  run(['fetch','--no-write-fetch-head','origin',parent])
  run(['read-tree',parent],env)
  for n,b,x in paths:
   blob=run(['hash-object','-w','--stdin'],data=b)
   run(['update-index','--add','--cacheinfo','100755' if x else '100644',blob,n],env)
  tree=run(['write-tree'],env)
  if tree==run(['rev-parse',parent+'^{tree}']):
   receipt['unchanged']=True;receipt['remote_commit']=parent;break
  commit=run(['commit-tree',tree,'-p',parent],data=(a.message+'\n').encode())
  outcome=subprocess.run(['git','push','origin',commit+':refs/heads/main'],cwd=REPO,capture_output=True,text=True)
  receipt['attempts'].append({'parent':parent,'commit':commit,'exit_code':outcome.returncode,'output':outcome.stdout+outcome.stderr})
  if outcome.returncode==0:
   receipt['remote_commit']=commit;break
  if 'non-fast-forward' not in outcome.stderr and 'fetch first' not in outcome.stderr:raise SystemExit(outcome.stderr)
 else:raise SystemExit('Concurrent pushes prevented checkpoint after 5 safe attempts')
receipt['shared_head_after']=run(['rev-parse','HEAD']);receipt['shared_index_sha256_after']=digest(idx)
receipt['shared_state_preserved']=(receipt['shared_head_before']==receipt['shared_head_after'] and before==receipt['shared_index_sha256_after'])
receipt['remote_verified']=run(['merge-base','--is-ancestor',receipt['remote_commit'],run(['ls-remote','origin','refs/heads/main']).split()[0]])==''
out=(PROJECT/'receipts'/a.receipt).resolve()
if not out.is_relative_to(PROJECT/'receipts'):raise SystemExit('Receipt must be project-local')
out.write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({'commit':receipt['remote_commit'],'shared_state_preserved':receipt['shared_state_preserved'],'remote_verified':receipt['remote_verified'],'receipt':str(out)}))
