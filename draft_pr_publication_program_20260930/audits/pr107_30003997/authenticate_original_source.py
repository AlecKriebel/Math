"""Authenticate eligible PR107's complete incoming attempt and literal queue row."""
from pathlib import Path
import datetime,hashlib,json,os,subprocess
A=Path(__file__).resolve().parent
C=A.parents[2]
D=A/'original_source_authentication_20261006'
D.mkdir(exist_ok=False)
HEAD='cc2ae01897135b35bee135917819e782a220f2c1'
PREFIX='unsolved_math_prioritization/attempts/30003997/'
records=[]
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def require(ok,message):
    if not ok:raise RuntimeError(message)
def dump(p,value):p.write_text(json.dumps(value,indent=2,sort_keys=True)+'\n')
def run(argv):
    start=now();proc=subprocess.Popen(argv,cwd=C,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out,err=proc.communicate();i=len(records)
    (D/(str(i)+'.stdout.bin')).write_bytes(out);(D/(str(i)+'.stderr.bin')).write_bytes(err)
    records.append({'argv':argv,'PID':proc.pid,'UTC_start':start,'UTC_end':now(),'exit_code':proc.returncode,
                    'stdout_file':str(i)+'.stdout.bin','stderr_file':str(i)+'.stderr.bin',
                    'stdout_sha256':hashlib.sha256(out).hexdigest(),'stderr_sha256':hashlib.sha256(err).hexdigest()})
    dump(D/'PROCESS_JOURNAL.json',{'operator_PID':os.getpid(),'records':records})
    require(proc.returncode==0,err.decode('utf-8','replace')[:1000]);return out
def git(*args):return run(['/usr/bin/git',*args])
require(git('symbolic-ref','--short','HEAD').strip()==b'main','branch')
meta=json.loads(run(['/opt/homebrew/bin/gh','pr','view','107','--repo','AlecKriebel/Math','--json',
                    'number,state,isDraft,headRefOid,headRefName,baseRefName,title,url,body,files']))
require(meta['state']=='OPEN' and meta['isDraft'] and meta['headRefOid']==HEAD
        and meta['headRefName']=='dot/math-30003997' and meta['baseRefName']=='main','current source identity')
dump(D/'CURRENT_PR_METADATA.json',meta)
git('fetch','--no-tags','https://github.com/AlecKriebel/Math.git',HEAD)
require(git('rev-parse','FETCH_HEAD').strip().decode()==HEAD,'fetch identity')
queue=git('show',HEAD+':unsolved_math_prioritization/QUEUE.md')
rows=[line for line in queue.decode().splitlines() if line.startswith('|') and len(line.split('|'))>12
      and line.split('|')[2].strip().split('/')[0].strip()=='30003997']
require(len(rows)==1,'unique row');cells=rows[0].split('|')
require(cells[8].strip()=='claimed_solved' and cells[9].strip()=='1/5','eligible literal status/budget')
dump(D/'QUEUE_STATUS_PROJECTION.json',{'PR':107,'head':HEAD,'literal_status':cells[8].strip(),
     'original_budget':cells[9].strip(),'selected_row':rows[0],'whole_QUEUE_sha256':hashlib.sha256(queue).hexdigest(),
     'whole_QUEUE_bytes':len(queue),'QUEUE_git_blob_SHA1':git('rev-parse',HEAD+':unsolved_math_prioritization/QUEUE.md').decode().strip(),
     'selected_row_sha256':hashlib.sha256(rows[0].encode()).hexdigest()})
paths=[row['path'] for row in meta['files'] if row['path'].startswith(PREFIX)]
require(paths and len(meta['files'])==len(paths)+1
        and all(row['path'].startswith(PREFIX) or row['path']=='unsolved_math_prioritization/QUEUE.md'
                for row in meta['files']),'incoming path scope')
inventory=git('ls-tree','-r','--name-only',HEAD,'--',PREFIX).decode().splitlines()
require(sorted(inventory)==sorted(paths),'complete original inventory')
pins=[]
for path in sorted(paths):
    relative=path[len(PREFIX):]
    require('..' not in Path(relative).parts and not Path(relative).is_absolute(),'unsafe relative source')
    body=git('show',HEAD+':'+path);blob=git('rev-parse',HEAD+':'+path).decode().strip()
    require(hashlib.sha1(b'blob '+str(len(body)).encode()+b'\0'+body).hexdigest()==blob,'blob byte identity')
    mode=git('ls-tree',HEAD,'--',path).decode().split()[0]
    require(mode in ['100644','100755'],'nonregular original source')
    destination=D/'original_attempt'/relative;destination.parent.mkdir(parents=True,exist_ok=True)
    destination.write_bytes(body)
    pins.append({'path':path,'relative_path':relative,'git_blob_SHA1':blob,'sha256':hashlib.sha256(body).hexdigest(),
                 'bytes':len(body),'Git_mode':mode,'preserved_path':str(destination)})
result={'schema':'pr107-original-native-source-authentication/v1','UTC':now(),'operator_PID':os.getpid(),
        'PR':107,'problem_id':30003997,'source_head':HEAD,'literal_status':'claimed_solved','original_author_effort':'1/5',
        'new_central_proof_search_turns':0,'files':pins,'incoming_body_count':len(pins),
        'complete_native_inventory_authenticated':True,'sourcepair_provenance_audit_pending':True,
        'primary_checkout_mutated':False,'mathematical_clearance':False,'publication_clearance':False}
dump(D/'ORIGINAL_BLOB_MANIFEST.json',result)
(A/'RESEARCH_LOG.md').write_text('# PR107 publication audit log\n\n'+result['UTC']+
  ' — authenticated exact current OPENdraft head and all incoming regular native bodies plus the unique QUEUE status projection. Original claimed_solved1/5, extra proof-search0. Source-pair validation and fresh independent math families are next; no novelty, publication or merge clearance. Source100% (native bodies), mathematics0%, PR107workflow5%; program15/99=15.15%. Primary checkout/index unchanged.\n')
print(json.dumps({k:v for k,v in result.items() if k!='files'}))
