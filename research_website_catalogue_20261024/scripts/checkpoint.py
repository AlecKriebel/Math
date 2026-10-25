"""Push only this programme through an isolated Git index; preserve shared checkout."""
from pathlib import Path
from datetime import datetime, timezone
import json, os, subprocess, tempfile, sys

PROGRAM = Path(__file__).resolve().parents[1]
REPO = PROGRAM.parent
def git(*args, env=None):
    result=subprocess.run(['git','-c','gc.auto=0',*args], cwd=REPO, env=env, text=True, stdout=subprocess.PIPE)
    if result.returncode:
        print(result.stdout)
        result.check_returncode()
    return result.stdout.strip()

assert git('branch','--show-current') == 'main'
git('fetch','origin','main')
parent=git('rev-parse','origin/main')
fd,index=tempfile.mkstemp(prefix='research-catalogue-index-')
os.close(fd); os.unlink(index)
env=dict(os.environ, GIT_INDEX_FILE=index)
try:
    git('read-tree',parent,env=env)
    git('add','--',PROGRAM.name+'/',env=env)
    files=git('diff','--cached','--name-only',parent,env=env).splitlines()
    assert all(p.startswith(PROGRAM.name+'/') for p in files)
    if not files:
        print('No new programme changes'); raise SystemExit(0)
    # Archived source is retained byte for byte, including original whitespace.
    git('diff','--cached','--check',parent,'--',PROGRAM.name+'/',
        ':!'+PROGRAM.name+'/papers/*/sources/published-source/**',env=env)
    tree=git('write-tree',env=env)
    message=sys.argv[1] if len(sys.argv)>1 else 'Checkpoint Zenodo research website catalogue'
    commit=subprocess.check_output(['git','-c','gc.auto=0','commit-tree',tree,'-p',parent],input=message+'\n',cwd=REPO,env=env,text=True).strip()
    git('push','origin',commit+':refs/heads/main')
    receipt={'utc':datetime.now(timezone.utc).isoformat(),'commit':commit,'parent':parent,'files':len(files),'scope':PROGRAM.name,'local_branch_and_shared_index_unchanged':True}
    (PROGRAM/'verification/PUSH_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt))
finally:
    if os.path.exists(index): os.unlink(index)
