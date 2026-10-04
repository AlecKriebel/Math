"""Fetch only objects; authenticate candidate locally without touching branch/index/files."""
from pathlib import Path
from datetime import datetime,timezone
import subprocess,json,hashlib,os
A=Path(__file__).resolve().parent;R=A.parents[2]
D=A/'root_capture_private/local_git004';D.mkdir(exist_ok=False)
utc=lambda:datetime.now(timezone.utc).isoformat();sha=lambda b:hashlib.sha256(b).hexdigest()
records=[]
def run(args):
    started=utc();r=subprocess.run(args,cwd=R,capture_output=True,env=dict(os.environ,GIT_OPTIONAL_LOCKS='0'));n=len(records)
    j={'argv':args,'started_utc':started,'ended_utc':utc(),'exit_code':r.returncode}
    for k,b in [('stdout',r.stdout),('stderr',r.stderr)]:
        (D/f'{n:03}.{k}.bin').write_bytes(b);j[k+'_bytes']=len(b);j[k+'_sha256']=sha(b)
    (D/f'{n:03}.json').write_text(json.dumps(j,indent=2)+'\n');records.append(j);assert r.returncode==0,(args,r.returncode)
    return r.stdout
assert run(['git','branch','--show-current'])==b'main\n'
assert not json.loads((A.parents[1]/'SHARED_GIT_WINDOW_STATUS.json').read_text())['shared_git_writes_paused']
main=run(['git','rev-parse','HEAD']);index=run(['git','ls-files','-s','-z'])
m=json.loads((A/'snapshot_manifest.json').read_text());H=m['head'];B=m['base']
run(['git','fetch','--no-write-fetch-head','origin',H])
assert run(['git','merge-base',main.decode().strip(),H]).decode().strip()==B
assert set(run(['git','diff','--name-only',B,H]).decode().splitlines())=={e['path'] for e in m['files']}
for e in m['files']:
    p=e['path'];body=run(['git','show',H+':'+p]);assert body==(A/'snapshot'/p).read_bytes()
    row=run(['git','ls-tree',H,'--',p]).decode().strip();meta,name=row.split('\t')
    mode,kind,oid=meta.split();assert name==p and mode==e['mode'] and kind=='blob' and oid==e['git_blob_sha']
assert run(['git','rev-parse','HEAD'])==main and run(['git','ls-files','-s','-z'])==index
j={'utc':utc(),'status':'PASS_COMPLETE_PR329_LOCAL_GIT_DIFF_BLOBS_MODES_MATCH_FROZEN_API',
   'head':H,'base':B,'all22_paths_verified':True,'local_main':main.decode().strip(),
   'branch_index_worktree_unchanged':True,'fetch_scope':'Only immutable candidate commit objects; --no-write-fetch-head; no branch/ref/index/checkout update',
   'native_capture_directory':str(D),'native_command_count':len(records),'program_sha256':sha(Path(__file__).read_bytes()),
   'snapshot_manifest_sha256':sha((A/'snapshot_manifest.json').read_bytes()),'mathematical_acceptance_inferred':False}
(A/'ROOT_LOCAL_GIT_VERIFICATION.json').write_text(json.dumps(j,indent=2)+'\n');print(json.dumps(j,indent=2))
