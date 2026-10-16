import json,urllib.request,hashlib,concurrent.futures
from pathlib import Path
items={'own_pr':'https://api.github.com/repos/AlecKriebel/Math/pulls/200','own_repository':'https://api.github.com/repos/AlecKriebel/Math','ferudun_zenodo':'https://zenodo.org/api/records/23093258','ferudun_datacite':'https://api.datacite.org/dois/10.5281/zenodo.23093258'}
def fetch(item):
 key,url=item
 try:
  req=urllib.request.Request(url,headers={'User-Agent':'Independent-publication-package-read-only-audit','Accept':'application/json'})
  with urllib.request.urlopen(req,timeout=25) as r:raw=r.read(1000000)
  data=json.loads(raw);Path('private_readings/'+key+'.json').write_bytes(raw)
  if key=='own_pr':fields={k:data.get(k) for k in ['html_url','created_at','state']};fields['head_sha']=data.get('head',{}).get('sha')
  elif key=='own_repository':fields={k:data.get(k) for k in ['html_url','private','created_at']}
  elif key=='ferudun_zenodo':fields={k:data.get(k) for k in ['id','created','updated','doi']};fields['files']=[{k:f.get(k) for k in ['key','checksum','size']} for f in data.get('files',[])]
  else:
   attrs=data['data']['attributes'];fields={k:attrs.get(k) for k in ['doi','created','registered','state','dates']}
  return key,{'url':url,'status':'read','selected_fields':fields,'raw_sha256':hashlib.sha256(raw).hexdigest()}
 except Exception as e:return key,{'url':url,'status':'unavailable','error':str(e)}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:results=dict(pool.map(fetch,items.items()))
Path('METADATA_WITNESSES.json').write_text(json.dumps(results,indent=2)+'\n');print(json.dumps(results,indent=2))
