from pathlib import Path
import json,urllib.request,hashlib,datetime,os
A=Path(__file__).resolve().parent;D=A/'published_download_verification_20261005';D.mkdir(exist_ok=False)
def require(c,m):
 if not c:raise RuntimeError(m)
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
records=[]
def fetch(url,filename):
 t=now()
 with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Math independent verification'}),timeout=45) as r:b=r.read();status=r.status;resolved=r.url
 p=D/filename;p.write_bytes(b);records.append({'url':url,'resolved_url':resolved,'UTC_start':t,'UTC_end':now(),'http_status':status,'file':filename,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()});(D/'HTTP_READS.json').write_text(json.dumps({'PID':os.getpid(),'records':records},indent=2)+'\n');require(status==200,'HTTP failed');return b
pub=json.loads((A/'actual_operations/zenodo_publish/stdout.bin').read_bytes());require(pub['state']=='published','not published')
remote=json.loads(fetch('https://zenodo.org/api/records/'+str(pub['id']),'record.json'));require(remote['doi']==pub['doi'],'DOI')
expected={r['name']:r for r in pub['files']};require(set(expected)=={r['key'] for r in remote['files']},'file set')
for row in remote['files']:
 r=expected[row['key']];b=fetch(row['links']['self'],row['key']);require(len(b)==r['size'] and hashlib.sha256(b).hexdigest()==r['sha256'],'download bytes '+row['key'])
x={'schema':'pr91-published-download-check/v1','UTC':now(),'actual_PID':os.getpid(),'DOI':pub['doi'],'record_url':pub['record_url'],'all_seven_downloaded_bytes_match_reviewed_payloads':True,'files':records,'metadata_exactness_verification':'Repository Zenodo kit publication and inspect receipts: no metadata normalizations.'};(A/'ROOT_PUBLIC_DEPOSIT_VERIFICATION.json').write_text(json.dumps(x,indent=2)+'\n');print(json.dumps({k:v for k,v in x.items() if k!='files'}))
