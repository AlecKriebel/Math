"""Publish only this effort on remote main; preserve shared checkout/index/HEAD."""
import json, os, subprocess, tempfile
from datetime import datetime, timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
HERE=ROOT/'paper_inventory_20261024'
def run(*args,env=None):
    return subprocess.check_output(args,cwd=ROOT,env=env,text=True).strip()
assert run('git','branch','--show-current')=='main'
run('git','fetch','origin','main')
parent=run('git','rev-parse','origin/main')
fd,name=tempfile.mkstemp(prefix='paper-inventory-index-');os.close(fd);os.unlink(name)
env=dict(os.environ,GIT_INDEX_FILE=name)
try:
    run('git','read-tree',parent,env=env)
    run('git','add','--','paper_inventory_20261024',env=env)
    staged=run('git','diff','--cached','--name-only',parent,env=env).splitlines()
    if any(not p.startswith('paper_inventory_20261024/') or '/sources/' in p or 'sheet_snapshot' in p for p in staged):
        raise RuntimeError('Checkpoint escaped public effort scope')
    tree=run('git','write-tree',env=env)
    if tree==run('git','rev-parse',parent+'^{tree}'):
        print(json.dumps({'status':'unchanged','remote_main':parent}));raise SystemExit
    commit=run('git','commit-tree',tree,'-p',parent,'-m','Checkpoint complete-paper inventory and evidence-grounded assessments',env=env)
    run('git','push','origin',commit+':refs/heads/main')
    remote=run('git','ls-remote','origin','refs/heads/main').split()[0]
    if remote!=commit: raise RuntimeError('Remote main verification mismatch')
    receipt={'utc':datetime.now(timezone.utc).isoformat(),'commit':commit,'parent':parent,'remote_main_verified':True,'paths':staged,'shared_head_unchanged':run('git','rev-parse','HEAD'),'method':'isolated index, remote-main parent, no working checkout mutation'}
    (HERE/'outputs/checkpoint_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt))
finally:
    Path(name).unlink(missing_ok=True)
