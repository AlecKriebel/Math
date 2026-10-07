#!/usr/bin/env python3
"""Push only this effort through a private index based on remote main.
Leaves the shared checkout, its branch and index untouched; never force-pushes.
Usage: python3 research/checkpoint_owned.py MESSAGE RECEIPT_BASENAME
"""
from pathlib import Path
import subprocess,os,tempfile,hashlib,json,datetime,sys
project=Path(__file__).resolve().parents[1];root=project.parent
if len(sys.argv)!=3: raise SystemExit(__doc__)
rel=str(project.relative_to(root))
def run(args,env=None):
 return subprocess.check_output(['git',*args],cwd=root,env=env,text=True).strip()
if run(['branch','--show-current'])!='main': raise SystemExit('Shared checkout is not on main')
head=run(['rev-parse','HEAD']);index=root/'.git/index';before=hashlib.sha256(index.read_bytes()).hexdigest()
(project/'work').mkdir(exist_ok=True)
for attempt in range(4):
 run(['-c','gc.auto=0','fetch','--no-tags','origin','main'])
 base=run(['ls-remote','origin','refs/heads/main']).split()[0]
 fd,ip=tempfile.mkstemp(prefix='private-index-',dir=project/'work');os.close(fd);os.unlink(ip)
 env=os.environ.copy();env['GIT_INDEX_FILE']=ip
 try:
  run(['read-tree',base],env);run(['add','--',rel],env)
  tree=run(['write-tree'],env)
  if tree==run(['rev-parse',base+'^{tree}']): raise SystemExit('No owned changes')
  commit=run(['commit-tree',tree,'-p',base,'-m',sys.argv[1]],env)
  push=subprocess.run(['git','push','origin',commit+':refs/heads/main'],cwd=root,text=True,capture_output=True)
  if push.returncode==0: break
 finally: Path(ip).unlink(missing_ok=True)
else: raise SystemExit('Remote moved repeatedly; shared state was not changed')
after=hashlib.sha256(index.read_bytes()).hexdigest();head_after=run(['rev-parse','HEAD'])
receipt={'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'base':base,'commit':commit,'remote_main_observed':run(['ls-remote','origin','refs/heads/main']).split()[0],'changed_paths':run(['diff-tree','--no-commit-id','--name-only','-r',commit]).splitlines(),'shared_head_before':head,'shared_head_after':head_after,'shared_index_sha256_before':before,'shared_index_sha256_after':after,'private_index_used':True,'push_stdout':push.stdout,'push_stderr':push.stderr}
(project/'receipts'/sys.argv[2]).write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
