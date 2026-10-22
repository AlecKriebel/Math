from pathlib import Path
import urllib.request,json,hashlib,datetime,subprocess,base64,shutil
from concurrent.futures import ThreadPoolExecutor
ROOT=Path(__file__).resolve().parent; S=ROOT/'sources'; R=ROOT/'receipts'
tasks=[('https://arxiv.org/pdf/2202.02551v3','circumcenter_2022.pdf'),('https://arxiv.org/pdf/2009.02581v3','pedal_curves_2020.pdf'),('https://arxiv.org/pdf/1008.0110v1','pedal_triangles_2010.pdf')]
def fetch(pair):
 url,name=pair; item={'url':url,'relative_path':'sources/'+name,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 try:
  with urllib.request.urlopen(url,timeout=45) as r: data=r.read(); item['status']=r.status
  p=S/name;p.write_bytes(data);item.update(bytes=len(data),sha256=hashlib.sha256(data).hexdigest())
  res=subprocess.run(['/opt/homebrew/bin/pdftotext','-layout',str(p),str(p.with_suffix('.txt'))],capture_output=True,text=True); item.update(extraction_exit=res.returncode,extraction_stderr=res.stderr)
 except Exception as e: item['error']=repr(e)
 return item
with ThreadPoolExecutor(max_workers=3) as p: records=list(p.map(fetch,tasks))
cache=Path('/Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr255_5100022/initial_review_20261013/priority_recent_adversary_01/sources')
for name in ['bicentric_hexagons_2024.pdf','bicentric_hexagons_2024.txt','bicentric_2021.pdf','bicentric_2021.txt']:
 data=(cache/name).read_bytes(); (S/name).write_bytes(data);records.append({'source_cache':str(cache/name),'relative_path':'sources/'+name,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
gh='/opt/homebrew/Cellar/gh/2.85.0/bin/gh'
res=subprocess.run([gh,'api','repos/AlecKriebel/Math/pulls/110/files?per_page=100'],capture_output=True,text=True); (R/'pr110_file_paths.json').write_text(res.stdout)
if res.returncode: raise RuntimeError(res.stderr)
paths=[x['filename'] for x in json.loads(res.stdout) if x['filename'].endswith('/PROOF.md')]
sha='3d159f0a00d0bd7ff8d558d6fbc75af5094f7a35'
for path in paths:
 res=subprocess.run([gh,'api',f'repos/AlecKriebel/Math/contents/{path}?ref={sha}'],capture_output=True,text=True)
 (R/'pr110_corrected_proof_provider.json').write_text(res.stdout); (R/'pr110_corrected_proof_provider.stderr').write_text(res.stderr)
 if res.returncode: continue
 d=json.loads(res.stdout);data=base64.b64decode(d['content']);(S/'pr110_earlier_PROOF.md').write_bytes(data);records.append({'PR':110,'ref':sha,'native_path':path,'blob':d['sha'],'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
(R/'SECONDARY_LEAD_RECEIPTS.json').write_text(json.dumps(records,indent=2)+'\n');print(json.dumps(records,indent=2))
