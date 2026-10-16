"""Fresh public primary-source retrieval; bodies stay in excluded scratch."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import datetime, hashlib, json, subprocess, urllib.request
R=Path(__file__).absolute().parent
W=R.parent/'whole_preprint_round03_scratch'/'primary'
SOURCES={
 'owr':'https://ems.press/content/serial-article-files/46279',
 'rs_journal':'https://www.cambridge.org/core/services/aop-cambridge-core/content/view/A716CDDA53B187EB87C28202DBCBBD94/S0010437X12000188a.pdf/div-class-title-some-projective-surfaces-of-gk-dimension-4-div.pdf',
 'rs_v2':'https://arxiv.org/pdf/1101.0737v2',
 'ns_v1':'https://arxiv.org/pdf/1206.0760v1',
 'ns_v2':'https://arxiv.org/pdf/1206.0760v2',
 'rz_v2':'https://arxiv.org/pdf/math/0409405v2',
 'campbell':'https://era.ed.ac.uk/server/api/core/bitstreams/ca9b4e97-4142-4f02-b516-c99c7584481c/content',
 'ns_metadata':'https://arxiv.org/abs/1206.0760v2',
 'av_metadata':'https://api.crossref.org/works/10.1016/0021-8693(90)90207-A',
}
def fetch(item):
 name,url=item
 row={'key':name,'url':url,'retrieved_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Independent mathematical source review'}),timeout=50) as f:
   body=f.read();row.update(final_url=f.url,status=f.status,content_type=f.headers.get('Content-Type'))
  ext='.pdf' if body.startswith(b'%PDF-') else '.html' if b'<html' in body[:1000].lower() else '.json'
  p=W/(name+ext);p.write_bytes(body)
  row.update(path=p.name,bytes=len(body),sha256=hashlib.sha256(body).hexdigest(),pdf=ext=='.pdf')
  if ext=='.pdf':
   proc=subprocess.run(['/opt/homebrew/bin/pdftotext','-layout',str(p),str(W/(name+'.txt'))],capture_output=True,text=True)
   row['pdftotext_returncode']=proc.returncode
 except Exception as e: row['error']=str(e)
 return row
if __name__=='__main__':
 W.mkdir(parents=True,exist_ok=True)
 with ThreadPoolExecutor(max_workers=5) as pool: rows=list(pool.map(fetch,SOURCES.items()))
 (R/'PRIMARY_RETRIEVALS.json').write_text(json.dumps(rows,indent=2)+'\n')
 print(json.dumps([{k:r[k] for k in ('key','bytes','pdf','error') if k in r} for r in rows],indent=2))
