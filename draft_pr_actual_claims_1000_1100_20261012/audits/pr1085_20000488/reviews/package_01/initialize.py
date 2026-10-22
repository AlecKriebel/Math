from pathlib import Path
import hashlib,json,subprocess,datetime,os
R=Path(__file__).resolve().parent; A=R.parents[1]
def sha(b): return hashlib.sha256(b).hexdigest()
def write(n,o): (R/n).write_text(json.dumps(o,indent=2,sort_keys=True)+'\n')
rows=[]
for p in sorted(A.rglob('*')):
    if R==p or R in p.parents or not p.is_file(): continue
    b=p.read_bytes(); rows.append({'path':p.relative_to(A).as_posix(),'bytes':len(b),'sha256':sha(b)})
write('INPUT_PINS.json',{'captured_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Every existing regular audit file outside this new review; hash only, no copied source bodies.','files':rows})
pins=json.loads((A/'SUBMITTED_PINS.json').read_text()); auth=[]
for row in pins['files']:
    body=subprocess.run(['git','show',pins['head_oid']+':'+row['repository_path']],check=True,capture_output=True).stdout
    snap=(A/row['snapshot_path']).read_bytes()
    if body!=snap or len(body)!=row['bytes'] or sha(body)!=row['sha256']: raise ValueError(row)
    auth.append({'repository_path':row['repository_path'],'bytes':len(body),'sha256':sha(body),'actual_git_blob_equals_submitted':True})
write('GIT_AUTHENTICATION.json',{'head':pins['head_oid'],'files':auth,'shared_branch':subprocess.run(['git','symbolic-ref','--short','HEAD'],check=True,capture_output=True,text=True).stdout.strip(),'shared_head':subprocess.run(['git','rev-parse','HEAD'],check=True,capture_output=True,text=True).stdout.strip()})
print(json.dumps({'frozen_files':len(rows),'actual_git_authenticated':len(auth)}))
