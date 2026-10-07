"""Publish owned files on current remote main, leaving shared checkout/index untouched."""
from pathlib import Path
import os, subprocess, tempfile, json, datetime, sys
root=Path(__file__).resolve().parents[2]
project=Path(__file__).resolve().parents[1]
message=sys.argv[1]
# Take immutable blobs first; no other researchers' paths enter the isolated index.
files=[p for p in project.rglob('*') if p.is_file() and not subprocess.run(['git','check-ignore','-q',str(p.relative_to(root))],cwd=root).returncode==0]
blobs=[]
for p in sorted(files):
    rel=str(p.relative_to(root))
    blob=subprocess.check_output(['git','hash-object','-w','--',rel],cwd=root,text=True).strip()
    blobs.append((rel,blob))
for attempt in range(4):
    subprocess.run(['git','fetch','--no-auto-gc','origin','main'],cwd=root,check=True)
    base=subprocess.check_output(['git','rev-parse','origin/main'],cwd=root,text=True).strip()
    with tempfile.TemporaryDirectory(dir=project/'receipts',prefix='isolated-index-') as td:
        env=os.environ.copy(); env['GIT_INDEX_FILE']=str(Path(td)/'index')
        subprocess.run(['git','read-tree',base],cwd=root,env=env,check=True)
        for rel,blob in blobs:
            subprocess.run(['git','update-index','--add','--cacheinfo','100644',blob,rel],cwd=root,env=env,check=True)
        tree=subprocess.check_output(['git','write-tree'],cwd=root,env=env,text=True).strip()
        commit=subprocess.check_output(['git','commit-tree',tree,'-p',base,'-m',message],cwd=root,text=True).strip()
    result=subprocess.run(['git','push','origin',commit+':refs/heads/main'],cwd=root,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
    if result.returncode==0:
        receipt={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'parent':base,'commit':commit,'tree':tree,'branch':'main','owned_files':len(blobs),'shared_checkout_and_index':'not modified','push_stdout':result.stdout,'push_stderr':result.stderr}
        (project/'receipts/latest_git_checkpoint.json').write_text(json.dumps(receipt,indent=2)+'\n')
        print(json.dumps(receipt,indent=2)); break
    if 'fetch first' not in result.stderr and 'non-fast-forward' not in result.stderr:
        raise RuntimeError(result.stderr)
else:
    raise RuntimeError('Concurrent remote main updates prevented four safe pushes; no shared state modified.')
