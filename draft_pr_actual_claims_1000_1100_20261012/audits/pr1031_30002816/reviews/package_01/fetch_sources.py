from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import urllib.request,hashlib,json,datetime,subprocess
R=Path(__file__).resolve().parent
P=R.parent.parent/'publication'
allitems=json.loads((P/'evidence/priority_review_01/sources/SOURCE_PINS.json').read_text())['sources']
ids={'owr2015','harvey_lawson1982','fawzi2021','fawzi2019v1','rostalski2010slides','theta_bookchapter2013','curvature2021v2','bsv2016_arxiv','gpt_lifts2013','lifting_simplicity2022','vrana_levay2009','grabowski_kus_marmo2012','barvinok_blekherman2005','orbitopes2011','theta_gpt2010'}
def fetch(e):
 out={'id':e['id'],'url':e['url'],'version':e.get('version'),'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'inspected_as_prior_report':False}
 try:
  req=urllib.request.Request(e['url'],headers={'User-Agent':'Independent mathematical source verification'})
  with urllib.request.urlopen(req,timeout=60) as response:
   b=response.read();out['final_url']=response.url
  path=R/'sources/raw'/(e['id']+'.pdf');path.write_bytes(b)
  out.update(bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),pdf_signature=b.startswith(b'%PDF'),raw_path=str(path.relative_to(R)))
  if out['pdf_signature']:
   text=path.with_suffix('.txt');rr=subprocess.run(['pdftotext','-layout',str(path),str(text)],capture_output=True)
   out.update(extraction_exit=rr.returncode,extraction_stderr=rr.stderr.decode(),text_sha256=hashlib.sha256(text.read_bytes()).hexdigest())
 except Exception as exc:out['error']=str(exc)
 return out
with ThreadPoolExecutor(max_workers=8) as ex:rows=list(ex.map(fetch,[e for e in allitems if e['id'] in ids]))
(R/'sources/SOURCE_FETCH_RECEIPT.json').write_text(json.dumps(rows,indent=2)+'\n')
for x in rows:print(x['id'],x.get('bytes'),x.get('error'),x.get('sha256'))
