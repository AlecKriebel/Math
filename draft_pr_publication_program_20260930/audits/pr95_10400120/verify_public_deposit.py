from pathlib import Path
import datetime, hashlib, json, os, urllib.request
A=Path(__file__).resolve().parent;D=A/'published_download_verification_20261005';D.mkdir(exist_ok=False)
def require(ok,message):
    if not ok:raise RuntimeError(message)
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def load(p):return json.loads(p.read_text())
def dump(p,x):p.write_text(json.dumps(x,indent=2,sort_keys=True)+'\n')
records=[]
def fetch(url,name):
    require(url.startswith('https://zenodo.org/'),'unexpected download authority')
    require(Path(name).name==name,'unsafe download name');started=now()
    with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Math-Independent-Publication-Verification/1.0'}),timeout=45) as response:
        b=response.read();status=response.status;resolved=response.url
    (D/name).write_bytes(b)
    records.append({'url':url,'resolved_url':resolved,'UTC_start':started,'UTC_end':now(),'http_status':status,'file':name,'bytes':len(b),'sha256':sha(b)})
    dump(D/'HTTP_READS.json',{'actual_PID':os.getpid(),'records':records});require(status==200,'HTTP status');return b
ready=load(A/'ROOT_READY_FOR_PUBLICATION.json');require(ready['publication_clearance'],'review gate')
pub=load(A/'actual_operations/zenodo_publish/stdout.bin');require(pub['state']=='published' and pub['environment']=='production','publication')
expected={e['file']:e for e in ready['upload_pins']}
require(len(expected)==7 and set(expected)=={e['name'] for e in pub['files']},'reviewed publication file set')
for e in pub['files']:
    pin=expected[e['name']];require(e['size']==pin['bytes'] and e['sha256']==pin['sha256'],'published pin')
remote=json.loads(fetch('https://zenodo.org/api/records/'+str(pub['id']),'record.json'))
require(str(remote['id'])==str(pub['id']) and remote['doi']==pub['doi'],'published identity')
require(set(expected)=={e['key'] for e in remote['files']} and len(remote['files'])==7,'public file set')
for e in remote['files']:
    pin=expected[e['key']];b=fetch(e['links']['self'],e['key'])
    require(len(b)==pin['bytes'] and sha(b)==pin['sha256'],'public reviewed bytes '+e['key'])
result={'schema':'pr95-published-download-verification/v1','UTC':now(),'actual_PID':os.getpid(),
 'verified':True,'record_id':pub['id'],'DOI':pub['doi'],'record_url':pub['record_url'],
 'all_seven_downloaded_bytes_match_reviewed_payloads':True,'files':records,
 'metadata_exactness_verification':'Repository Zenodo kit publication and read-only inspect receipts; accepted narrow normalizations preserved separately.',
 'metadata_normalizations':pub['metadata_normalizations'],'priority_clearance':False,
 'qualified_publication_user_authorized':True,'human_peer_review':False}
dump(A/'ROOT_PUBLIC_DEPOSIT_VERIFICATION.json',result)
print(json.dumps({k:v for k,v in result.items() if k!='files'}))
