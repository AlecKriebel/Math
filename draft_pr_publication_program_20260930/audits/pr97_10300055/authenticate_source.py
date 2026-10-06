"""Authenticate this eligible PR's incoming native bodies and literal queue row."""
from pathlib import Path
import subprocess,json,hashlib,datetime,os
A=Path(__file__).resolve().parent;C=A.parents[2]
D=A/'original_source_authentication_20261005';D.mkdir(exist_ok=False);records=[]
HEAD='fb50facb2a7389bb272bbf0b5cbd80c24c79b992'
PREFIX='unsolved_math_prioritization/attempts/10300055/'
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def require(ok,message):
    if not ok:raise RuntimeError(message)
def dump(p,d):p.write_text(json.dumps(d,indent=2,sort_keys=True)+'\n')
def run(args):
    start=now();child=subprocess.Popen(args,cwd=C,stdout=subprocess.PIPE,stderr=subprocess.PIPE);out,err=child.communicate();i=len(records)
    for name,b in [('stdout',out),('stderr',err)]:(D/(str(i)+'.'+name+'.bin')).write_bytes(b)
    records.append({'argv':args,'PID':child.pid,'UTC_start':start,'UTC_end':now(),'exit_code':child.returncode,'stdout_file':str(i)+'.stdout.bin','stderr_file':str(i)+'.stderr.bin','stdout_sha256':hashlib.sha256(out).hexdigest(),'stderr_sha256':hashlib.sha256(err).hexdigest()})
    dump(D/'PROCESS_JOURNAL.json',{'actual_operator_PID':os.getpid(),'records':records});require(child.returncode==0,err.decode()[:1000]);return out
def git(*args):return run(['/usr/bin/git',*args])
require(git('symbolic-ref','--short','HEAD').strip()==b'main','branch')
meta=json.loads(run(['/opt/homebrew/bin/gh','pr','view','97','--repo','AlecKriebel/Math','--json','number,state,isDraft,headRefOid,headRefName,baseRefName,title,url,body,files']))
require(meta['state']=='OPEN' and meta['isDraft'] and meta['headRefOid']==HEAD and meta['headRefName']=='dot/math-10300055' and meta['baseRefName']=='main','current PR source identity')
dump(D/'CURRENT_PR_METADATA.json',meta)
git('fetch','--no-tags','https://github.com/AlecKriebel/Math.git',HEAD)
require(git('rev-parse','FETCH_HEAD').strip().decode()==HEAD,'fetched source')
queue=git('show',HEAD+':unsolved_math_prioritization/QUEUE.md');rows=[s for s in queue.decode().splitlines() if '| 10300055 / ' in s];require(len(rows)==1,'unique queue row');cells=rows[0].split('|')
require(cells[8].strip()=='claimed_solved' and cells[9].strip()=='2/5','literal eligible status and budget')
dump(D/'QUEUE_STATUS_PROJECTION.json',{'PR':97,'head':HEAD,'literal_status':cells[8].strip(),'original_budget':cells[9].strip(),'selected_row':rows[0],'whole_QUEUE_sha256':hashlib.sha256(queue).hexdigest(),'whole_QUEUE_bytes':len(queue),'QUEUE_git_blob_SHA1':git('rev-parse',HEAD+':unsolved_math_prioritization/QUEUE.md').decode().strip(),'selected_row_sha256':hashlib.sha256(rows[0].encode()).hexdigest()})
paths=[e['path'] for e in meta['files'] if e['path'].startswith(PREFIX)]
require(len(paths)==19 and len(meta['files'])==20 and all(e['path'].startswith(PREFIX) or e['path']=='unsolved_math_prioritization/QUEUE.md' for e in meta['files']),'incoming changed path scope')
inventory=git('ls-tree','-r','--name-only',HEAD,'--',PREFIX).decode().splitlines();require(sorted(inventory)==sorted(paths),'complete original attempt inventory')
pins=[]
for path in sorted(paths):
    rel=path[len(PREFIX):];require('..' not in Path(rel).parts,'safe original path')
    b=git('show',HEAD+':'+path);blob=git('rev-parse',HEAD+':'+path).decode().strip()
    require(hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==blob,'git blob bytes')
    f=D/'original_attempt'/rel;f.parent.mkdir(parents=True,exist_ok=True);f.write_bytes(b)
    pins.append({'path':path,'relative_path':rel,'git_blob_SHA1':blob,'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b),'preserved_path':str(f)})
out={'schema':'pr97-original-native-source-authentication/v1','UTC':now(),'actual_operator_PID':os.getpid(),'PR':97,'source_head':HEAD,'literal_status':'claimed_solved','original_author_effort':'2/5','new_central_proof_search_turns':0,'files':pins,'incoming_body_count':19,'complete_native_inventory_authenticated':True,'sourcepair_provenance_audit_pending':True,'primary_checkout_mutated':False,'publication_clearance':False}
dump(D/'ORIGINAL_BLOB_MANIFEST.json',out)
print(json.dumps({k:v for k,v in out.items() if k!='files'}))
