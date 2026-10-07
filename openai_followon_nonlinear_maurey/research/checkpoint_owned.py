#!/usr/bin/env python3
"""Push only this effort using owned tree objects based on current remote main.
Never writes a shared or private index, resets checkout, or force-pushes.
Usage: python3 research/checkpoint_owned.py MESSAGE RECEIPT_BASENAME
"""
from pathlib import Path
import subprocess,hashlib,json,datetime,sys,stat
project=Path(__file__).resolve().parents[1];root=project.parent;rel=project.name
if len(sys.argv)!=3: raise SystemExit(__doc__)
def raw(args,data=None):return subprocess.check_output(['git',*args],cwd=root,input=data)
def run(args):return raw(args).decode().strip()
if run(['branch','--show-current'])!='main': raise SystemExit('Shared checkout is not on main')
head=run(['rev-parse','HEAD']);index=root/'.git/index';before=hashlib.sha256(index.read_bytes()).hexdigest()
names=sorted(set(x.decode() for x in raw(['ls-files','--cached','--others','--exclude-standard','-z','--',rel]).split(b'\0') if x))
owned={}
for name in names:
 path=root/name
 if not path.is_file() and not path.is_symlink():continue
 parts=Path(name).parts[1:];d=owned
 for part in parts[:-1]: d=d.setdefault(part,{})
 if path.is_symlink():
  import os
  oid=run(['hash-object','-w','--stdin']) if False else raw(['hash-object','-w','--stdin'],os.readlink(path).encode()).decode().strip();mode='120000'
 else: oid=run(['hash-object','-w','--',name]);mode='100755' if path.stat().st_mode&stat.S_IXUSR else '100644'
 d[parts[-1]]=(mode,'blob',oid)
def tree(d):
 entries=[]
 for name,value in d.items():
  mode,kind,oid=('040000','tree',tree(value)) if isinstance(value,dict) else value
  entries.append(f'{mode} {kind} {oid}\t{name}'.encode()+b'\0')
 return raw(['mktree','-z'],b''.join(entries)).decode().strip()
project_tree=tree(owned)
for attempt in range(4):
 run(['-c','gc.auto=0','fetch','--no-tags','origin','main'])
 base=run(['ls-remote','origin','refs/heads/main']).split()[0]
 try:entries=raw(['ls-tree','-z',base]).split(b'\0')
 except subprocess.CalledProcessError:continue
 entries=[e for e in entries if e and e.split(b'\t',1)[1]!=rel.encode()]
 entries.append(f'040000 tree {project_tree}\t{rel}'.encode())
 root_tree=raw(['mktree','-z'],b'\0'.join(entries)+b'\0').decode().strip()
 if root_tree==run(['rev-parse',base+'^{tree}']):commit=base;push_stdout='Owned tree already current';push_stderr='';break
 commit=run(['commit-tree',root_tree,'-p',base,'-m',sys.argv[1]])
 push=subprocess.run(['git','push','origin',commit+':refs/heads/main'],cwd=root,text=True,capture_output=True)
 push_stdout=push.stdout;push_stderr=push.stderr
 if push.returncode==0:break
else:raise SystemExit('Remote moved repeatedly; shared state was not changed')
after=hashlib.sha256(index.read_bytes()).hexdigest();head_after=run(['rev-parse','HEAD'])
receipt={'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'base':base,'commit':commit,'remote_main_observed':run(['ls-remote','origin','refs/heads/main']).split()[0],'owned_tree':project_tree,'changed_paths':run(['diff-tree','--no-commit-id','--name-only','-r',commit]).splitlines(),'shared_head_before':head,'shared_head_after':head_after,'shared_index_sha256_before':before,'shared_index_sha256_after':after,'method':'hash owned blobs and trees; replace only dedicated-folder entry of remote root tree; no index mutation','push_stdout':push_stdout,'push_stderr':push_stderr}
(project/'receipts'/sys.argv[2]).write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt,indent=2))
