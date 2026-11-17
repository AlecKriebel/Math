"""One direct GET per exact deployed target; no browser/UI claim or retries."""
from pathlib import Path
from datetime import datetime,timezone
from concurrent.futures import ThreadPoolExecutor
from urllib.request import Request,urlopen
import hashlib,json
P=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
W=Path('/Users/alec/Desktop/alec-dev/aleckriebel.com')
R=P/'verification/mink-riesz-k3-live-root-20261117'
S=P/'verification/mink-riesz-k3-stage-sol-20261117'
sha=lambda b:hashlib.sha256(b).hexdigest()
d=json.loads((R/'DEPLOYMENT_FINAL.json').read_bytes())
assert d['status']=='HOSTING_DEPLOYED_LOCAL_GUARDS_EXACT'
assert d['commit']=='4cc09d6bbbad61aa11077c5002cf84a1e93b1344'
assert not (R/'HTTP_FINAL.json').exists() and not (R/'HTTP_ATTEMPTS.json').exists()
t=json.loads((S/'TARGETS.json').read_bytes())
paths=t['additions_public_relative']+t['modifications_public_relative']
assert len(paths)==len(set(paths))==15
def check(path):
 url='https://aleckriebel.com/'+(path[:-10] if path.endswith('index.html') else path)
 result={'local_path':path,'URL':url,'started_UTC':datetime.now(timezone.utc).isoformat(),'attempt':1}
 try:
  expected=(W/'public'/path).read_bytes()
  with urlopen(Request(url,headers={'User-Agent':'AlecKriebel research catalogue file verification'}),timeout=45) as response:
   raw=response.read();result.update(status=response.status,final_URL=response.geturl(),content_type=response.headers.get_content_type(),bytes=len(raw),SHA256=sha(raw))
  assert result['status']==200 and result['final_URL']==url and raw==expected
  if path.endswith('.pdf'):assert result['content_type']=='application/pdf' and raw.startswith(b'%PDF-')
  if path.endswith('.zip'):assert raw.startswith(b'PK')
  result['whole_deployed_bytes_match_reviewed_local']=True
 except Exception as e:result['failure']=repr(e)
 result['finished_UTC']=datetime.now(timezone.utc).isoformat()
 return result
with ThreadPoolExecutor(max_workers=5) as pool:results=list(pool.map(check,paths))
with (R/'HTTP_ATTEMPTS.json').open('x') as f:json.dump(results,f,indent=2);f.write('\n')
assert not any('failure' in r for r in results),'Preserved failed direct GET; no retry'
final={'UTC':datetime.now(timezone.utc).isoformat(),'status':'ALL15_DIRECT_HTTPS_WHOLE_FILE_CHECKS_PASS',
 'commit':d['commit'],'hosting_version':d['new_live_version'],'file_checks':15,'results':results,
 'all_PDF_bytes_and_MIME_verified':True,'actual_UI_desktop_mobile_or_iframe_display':False,'AA':None,'automatic_retries':0}
with (R/'HTTP_FINAL.json').open('x') as f:json.dump(final,f,indent=2);f.write('\n')
print(json.dumps({k:v for k,v in final.items() if k!='results'}))
