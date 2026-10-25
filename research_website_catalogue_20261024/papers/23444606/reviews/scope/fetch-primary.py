from pathlib import Path
from datetime import datetime,timezone
import urllib.request,hashlib,json,subprocess,concurrent.futures
R=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024/papers/23444606/reviews/scope');D=R/'cache/primary-sources';D.mkdir(parents=True,exist_ok=True)
inputs=[
('ek-author','https://elliotakaplan.github.io/Number_systems_with_simplicity_hierarchies_II.pdf','Author-hosted Number systems II; exact date/version to inspect from body'),
('kaplan-thesis2015','https://etd.ohiolink.edu/acprod/odb_etd/ws/send_file/send?accession=ouhonors1429615758&disposition=inline','OhioLINK institutional April 2015 honors thesis'),
('owr2016-60','https://ems.press/content/serial-article-files/46663','Publisher OWR Report60/2016'),
('ek-arxiv-v1','https://arxiv.org/pdf/1512.04001v1','Pinned arXiv1512.04001v1'),
('adh-v3','https://arxiv.org/pdf/1512.02267v3','Pinned arXiv1512.02267v3'),
('kks-v3','https://arxiv.org/pdf/2509.22374v3','Pinned arXiv2509.22374v3'),
('bvh-v1','https://arxiv.org/pdf/2305.02001v1','Pinned arXiv2305.02001v1')]
def get(t):
 name,url,edition=t;row={'name':name,'url':url,'version_description':edition,'retrieved_utc':datetime.now(timezone.utc).isoformat()}
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'ResearchSourceAudit/1.0'}),timeout=50) as r:b=r.read();row.update(resolved_url=r.geturl(),http_status=r.status,content_type=r.headers.get('Content-Type'))
  assert b.startswith(b'%PDF-'),b[:50]
  p=D/(name+'.pdf');p.write_bytes(b);row.update(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),status='acquired')
  out=subprocess.run(['pdftotext','-layout',str(p),str(D/(name+'.txt'))],capture_output=True,text=True);row['text_extraction_returncode']=out.returncode
  pi=subprocess.run(['pdfinfo',str(p)],capture_output=True,text=True);row['pdfinfo']=pi.stdout
 except Exception as e:row.update(status='unavailable',error=str(e))
 return row
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:rows=list(ex.map(get,inputs))
(R/'primary-source-receipts.json').write_text(json.dumps({'created_utc':datetime.now(timezone.utc).isoformat(),'sources':rows},indent=2)+'\n')
print(json.dumps([{k:v for k,v in x.items() if k!='pdfinfo'} for x in rows],indent=2))
