"""Publish owned blobs on remote main without modifying shared checkout/index.

Only small tree objects are built. This avoids materializing the shared giant
index on a nearly full disk. Every existing unrelated remote tree entry is kept.
"""
from pathlib import Path
import os,subprocess,json,datetime,sys
root=Path(__file__).resolve().parents[2]
project=Path(__file__).resolve().parents[1]
message=sys.argv[1]
def git(*args,data=None):
    return subprocess.check_output(['git',*args],cwd=root,input=data)
paths=[str(p.relative_to(root)) for p in project.rglob('*') if p.is_file()]
ignored=git('check-ignore','-z','--stdin',data=('\0'.join(paths)+'\0').encode()).split(b'\0')
ignored={p.decode() for p in ignored if p}
updates={}
for rel in sorted(set(paths)-ignored):
    blob=git('hash-object','-w','--',rel).decode().strip()
    node=updates
    parts=Path(rel).parts
    for part in parts[:-1]: node=node.setdefault(part,{})
    node[parts[-1]]=blob

def tree_update(base,changes):
    entries={}
    if base:
        for item in git('ls-tree','-z',base).split(b'\0'):
            if not item: continue
            header,name=item.split(b'\t',1);mode,kind,sha=header.split()
            entries[name.decode()]=(mode.decode(),kind.decode(),sha.decode())
    for name,value in changes.items():
        if isinstance(value,dict):
            old=entries.get(name)
            if old and old[1]!='tree': raise RuntimeError('File/directory collision: '+name)
            entries[name]=('040000','tree',tree_update(old[2] if old else None,value))
        else: entries[name]=('100644','blob',value)
    data=b''.join(f'{mode} {kind} {sha}\t{name}\0'.encode() for name,(mode,kind,sha) in sorted(entries.items()))
    return git('mktree','-z',data=data).decode().strip()

for attempt in range(4):
    subprocess.run(['git','fetch','--no-auto-gc','origin','main'],cwd=root,check=True)
    base=git('rev-parse','origin/main').decode().strip()
    tree=tree_update(git('rev-parse',base+'^{tree}').decode().strip(),updates)
    commit=git('commit-tree',tree,'-p',base,'-m',message).decode().strip()
    run=subprocess.run(['git','push','origin',commit+':refs/heads/main'],cwd=root,capture_output=True,text=True)
    if run.returncode==0:
        receipt={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'parent':base,'commit':commit,'tree':tree,'branch':'main','owned_files':len(set(paths)-ignored),'method':'direct tree objects preserving unrelated remote entries','shared_checkout_and_index':'not modified','push_stdout':run.stdout,'push_stderr':run.stderr}
        (project/'receipts/latest_git_checkpoint.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt,indent=2));break
    if 'fetch first' not in run.stderr and 'non-fast-forward' not in run.stderr: raise RuntimeError(run.stderr)
else: raise RuntimeError('Four concurrent remote advances prevented safe push; shared state untouched.')
