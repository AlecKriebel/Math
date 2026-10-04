"""Mechanically freeze exact submitted scope without inspecting the proof contents."""
from pathlib import Path
import base64,datetime,hashlib,json,subprocess
A=Path(__file__).resolve().parent;R=A.parents[2];D=A/'root_capture_private/freeze_001';D.mkdir(exist_ok=False)
H='6be98eac0ba508368218179ecf80020c037dbece';B='efd29c05204703acca9a0860812f54b94fae54b1';records=[]
def sha(b):return hashlib.sha256(b).hexdigest()
def run(args):
 start=datetime.datetime.now(datetime.timezone.utc).isoformat();p=subprocess.run(args,cwd=R,capture_output=True);i=len(records)
 (D/f'{i:03}.stdout').write_bytes(p.stdout);(D/f'{i:03}.stderr').write_bytes(p.stderr)
 e={'argv':args,'started_utc':start,'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'exit_code':p.returncode,'stdout_bytes':len(p.stdout),'stdout_sha256':sha(p.stdout),'stderr_bytes':len(p.stderr),'stderr_sha256':sha(p.stderr)};records.append(e);(D/f'{i:03}.receipt.json').write_text(json.dumps(e,indent=2)+'\n');assert p.returncode==0,(args,p.returncode,p.stderr.decode(errors='replace'));return p.stdout
assert run(['git','branch','--show-current']).strip()==b'main';main=run(['git','rev-parse','HEAD']).decode().strip();index=run(['git','ls-files','-s','-z'])
if subprocess.run(['git','cat-file','-e',H+'^{commit}'],cwd=R,capture_output=True).returncode!=0:run(['git','fetch','--no-tags','origin',H])
pr=json.loads(run(['gh','pr','view','359','--json','state,isDraft,headRefOid,baseRefOid,files']));assert pr['state']=='OPEN' and pr['isDraft'] and pr['headRefOid']==H and pr['baseRefOid']==B
paths=run(['git','diff','--name-only',B,H]).decode().splitlines();assert set(paths)=={x['path'] for x in pr['files']} and len(paths)==len(set(paths))
assert all(x=='unsolved_math_prioritization/QUEUE.md' or x.startswith('problems/30001370_basin_boundaries/') for x in paths)
S=A/'snapshot';S.mkdir(exist_ok=False);files=[]
for path in paths:
 tree=run(['git','ls-tree',H,'--',path]).decode().strip();meta,name=tree.split('\t');mode,kind,oid=meta.split();assert kind=='blob' and mode=='100644' and name==path
 b=run(['git','cat-file','blob',oid]);o=json.loads(run(['gh','api','repos/AlecKriebel/Math/git/blobs/'+oid]));assert o['sha']==oid and o['encoding']=='base64' and o['size']==len(b) and base64.b64decode(o['content'])==b
 f=S/path;f.parent.mkdir(parents=True,exist_ok=True);f.write_bytes(b);f.chmod(0o644)
 files.append({'path':path,'bytes':len(b),'sha256':sha(b),'git_blob_sha':oid,'mode':mode,'git_api_disk_identical':True})
assert run(['git','rev-parse','HEAD']).decode().strip()==main and run(['git','ls-files','-s','-z'])==index
end=json.loads(run(['gh','pr','view','359','--json','state,isDraft,headRefOid']));assert end=={k:pr[k] for k in end}
result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'FROZEN_ALL_SUBMITTED_SCOPE_GIT_API_DISK_EXACT','pr':359,'head':H,'base':B,'files':files,'all_files_count':len(files),'scope':'Mechanical byte/type/mode binding only. No source theorem/proof or candidate correctness is inferred.','main_and_shared_index_unchanged':True,'original_main':main,'native_capture_directory':str(D),'whole_native_commands':len(records)}
(A/'snapshot_manifest.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='files'},indent=2))
