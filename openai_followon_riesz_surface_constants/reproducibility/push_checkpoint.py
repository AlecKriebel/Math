"""Publish only explicitly selected owned files on current remote main; never use shared index."""
from pathlib import Path
import os,subprocess,json,tempfile,datetime,hashlib,argparse
root=Path('/Users/alec/Documents/Math'); p=root/'openai_followon_riesz_surface_constants'
a=argparse.ArgumentParser();a.add_argument('--message',required=True);a.add_argument('--receipt',required=True);a.add_argument('paths',nargs='+'); args=a.parse_args()
def git(*xs,env=None,input=None):
 return subprocess.check_output(['git',*xs],cwd=root,env=env,input=input,text=True).strip()
head=git('rev-parse','HEAD'); branch=git('branch','--show-current')
if branch!='main':raise SystemExit('Checkout is not on main')
index=root/'.git/index'; before=hashlib.sha256(index.read_bytes()).hexdigest() if index.exists() else None
rows=[]
for s in args.paths:
 q=(root/s).resolve()
 if not q.is_relative_to(p.resolve()) or not q.is_file():raise SystemExit(f'Not an owned regular file: {s}')
 if q.is_symlink():raise SystemExit('No symlinks')
 data=q.read_bytes(); rows.append({'path':str(q.relative_to(root)),'sha256':hashlib.sha256(data).hexdigest(),'blob':subprocess.check_output(['git','hash-object','-w','--stdin'],cwd=root,input=data).decode().strip(),'mode':'100755' if os.access(q,os.X_OK) else '100644','bytes':len(data)})
for attempt in range(5):
 parent=git('ls-remote','origin','refs/heads/main').split()[0]
 git('fetch','--no-write-fetch-head','origin',parent)
 with tempfile.TemporaryDirectory(prefix='private-index-',dir=p/'receipts') as d:
  env=dict(os.environ,GIT_INDEX_FILE=str(Path(d)/'index'))
  git('read-tree',parent,env=env)
  for row in rows:git('update-index','--add','--cacheinfo',row['mode'],row['blob'],row['path'],env=env)
  tree=git('write-tree',env=env)
  changed=git('diff-tree','--no-commit-id','--name-only','-r',parent,tree).splitlines()
  if any(not x.startswith('openai_followon_riesz_surface_constants/') for x in changed):raise SystemExit('Non-owned tree change')
  if not changed:commit=parent;break
  commit=git('commit-tree',tree,'-p',parent,input=args.message+'\n')
  res=subprocess.run(['git','push','origin',commit+':refs/heads/main'],cwd=root,capture_output=True,text=True)
  if res.returncode==0:break
  current=git('ls-remote','origin','refs/heads/main').split()[0]
  if current==parent:raise SystemExit(res.stderr)
else:raise SystemExit('Concurrent remote movement: retry later')
remote=git('ls-remote','origin','refs/heads/main').split()[0]
if remote!=commit:
 git('fetch','--no-write-fetch-head','origin',remote)
 if subprocess.run(['git','merge-base','--is-ancestor',commit,remote],cwd=root).returncode:raise SystemExit('Push ancestry not confirmed')
after=hashlib.sha256(index.read_bytes()).hexdigest() if index.exists() else None
r={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'confirmed','commit':commit,'parent':parent,'remote_main_observed':remote,'shared_head_before':head,'shared_head_after':git('rev-parse','HEAD'),'shared_branch':branch,'shared_index_before_sha256':before,'shared_index_after_sha256':after,'changed_owned_paths':changed,'included_files':rows}
(p/'receipts'/args.receipt).write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps({k:v for k,v in r.items() if k not in ['included_files','changed_owned_paths']}))
