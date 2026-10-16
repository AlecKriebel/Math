from pathlib import Path
import json,subprocess,urllib.request,hashlib,datetime,zipfile,io,base64
from concurrent.futures import ThreadPoolExecutor
ROOT=Path(__file__).resolve().parent; S=ROOT/'sources'; R=ROOT/'receipts'
def download(url,path):
 with urllib.request.urlopen(url,timeout=45) as r: data=r.read(); status=r.status; headers=dict(r.headers)
 path.parent.mkdir(parents=True,exist_ok=True); path.write_bytes(data)
 return data,{'url':url,'relative_path':str(path.relative_to(ROOT)),'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':status,'headers':headers,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}
ids=[23079799,23085904,23087221,23088516,23077039,23071366,23092466,23089778,23090907]
def archive(zid):
 records=[]
 try:
  raw,receipt=download(f'https://zenodo.org/api/records/{zid}',S/f'zenodo/{zid}.json'); records.append(receipt); d=json.loads(raw)
  for f in d.get('files',[]):
   if not f['key'].endswith('.zip'): continue
   data,receipt=download(f['links']['self'],S/f'zenodo/{zid}_{f["key"]}'); receipt.update(provider_checksum=f['checksum'],provider_checksum_matches=(f['checksum']=='md5:'+hashlib.md5(data).hexdigest())); records.append(receipt)
   with zipfile.ZipFile(io.BytesIO(data)) as z:
    for e in z.infolist():
     if e.filename.endswith('.tex'):
      path=Path(e.filename)
      if path.is_absolute() or '..'in path.parts: raise ValueError('unsafe zip path')
      out=S/f'zenodo/original_{zid}'/path; out.parent.mkdir(parents=True,exist_ok=True); out.write_bytes(z.read(e))
 except Exception as e: records.append({'zenodo_id':zid,'error':repr(e)})
 return records
with ThreadPoolExecutor(max_workers=6) as p: records=[x for group in p.map(archive,ids) for x in group]
(R/'ZENODO_ORIGINAL_RECEIPTS.json').write_text(json.dumps(records,indent=2)+'\n')
gh='/opt/homebrew/Cellar/gh/2.85.0/bin/gh'
def api(endpoint,name):
 res=subprocess.run([gh,'api',endpoint],capture_output=True,text=True)
 (R/name).write_text(res.stdout); (R/(name+'.stderr')).write_text(res.stderr)
 if res.returncode: raise RuntimeError(name)
 return json.loads(res.stdout)
sha='551a524e2db65fec90684485ef676d0b4179378d'
tree=api(f'repos/AlecKriebel/Math/git/trees/{sha}?recursive=1','pr204_tree.json')
nodes=[x for x in tree['tree'] if x['path'].endswith('/5100012/PROOF.md')]
if len(nodes)!=1: raise RuntimeError(nodes)
blob=api(f'repos/AlecKriebel/Math/git/blobs/{nodes[0]["sha"]}','pr204_proof_provider.json')
data=base64.b64decode(blob['content']); (S/'pr204_original_PROOF.md').write_bytes(data)
receipt={'ref':sha,'native_path':nodes[0]['path'],'blob':nodes[0]['sha'],'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}
(R/'PR204_SOURCE_AUTHENTICATION.json').write_text(json.dumps(receipt,indent=2)+'\n')
from urllib.parse import urlencode
for term in ['antipedal','5100020','k403']:
 api('search/issues?'+urlencode({'q':f'repo:AlecKriebel/Math is:pr {term}','per_page':100}),f'github_search_{term}.json')
print(json.dumps({'zenodo_records':len(ids),'errors':[x for x in records if 'error'in x],'checksum_all_match':all(x.get('provider_checksum_matches',True) for x in records),'pr204':receipt},indent=2))
