#!/usr/bin/env python3
"""Read a confirmed public Zenodo record and hash every public download; no token."""
import datetime,hashlib,json,pathlib,urllib.request
R=pathlib.Path(__file__).resolve().parents[1]
pub=json.loads((R/'receipts/zenodo_published_inspect.json').read_text())
assert pub['environment']=='production' and pub['state']=='published' and pub['doi']
record=pub['id'];base='https://zenodo.org';headers={'User-Agent':'Math-Multispecies-Preprint-Verification/1.0'}
def get(url):
 assert url.startswith(base+'/'),url
 with urllib.request.urlopen(urllib.request.Request(url,headers=headers),timeout=30) as r:
  assert r.status==200
  return r.read(20*1024*1024)
raw=get(base+'/api/records/'+str(record));remote=json.loads(raw)
assert remote['id']==record and remote['doi']==pub['doi']
assert remote['metadata']['title']==pub['title']
manifest=json.loads((R/'zenodo-deposit.json').read_text())
files={f['key']:f for f in remote['files']};expected={pathlib.Path(f['path']).name for f in manifest['files']};assert set(files)==expected
checks=[]
for f in manifest['files']:
 p=R/f['path'];name=p.name;data=get(base+'/records/'+str(record)+'/files/'+name+'?download=1')
 sha=hashlib.sha256(data).hexdigest();local=hashlib.sha256(p.read_bytes()).hexdigest();assert sha==local
 assert len(data)==p.stat().st_size==files[name]['size']
 md5=hashlib.md5(data).hexdigest();assert files[name]['checksum'] in [md5,'md5:'+md5]
 checks.append({'name':name,'bytes':len(data),'sha256':sha,'md5':md5,'public_download_matches_reviewed_local_file':True})
out={'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'record_id':record,'doi':pub['doi'],
 'record_url':pub['record_url'],'record_public_api_accessible':True,'public_api_response_sha256':hashlib.sha256(raw).hexdigest(),
 'title':remote['metadata']['title'],'creators':remote['metadata']['creators'],'files':checks,'no_api_token_sent':True}
(R/'receipts/zenodo_public_download_verification.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
