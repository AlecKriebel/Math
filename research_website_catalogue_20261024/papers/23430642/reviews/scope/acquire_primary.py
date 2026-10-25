from pathlib import Path
import concurrent.futures,datetime,urllib.request,hashlib,json,subprocess
base=Path(__file__).resolve().parent
out=base/'.reference-cache';out.mkdir(exist_ok=True)
urls={
 'disser-skutella-journal.pdf':'https://www2.mathematik.tu-darmstadt.de/~disser/pdfs/DisserSkutella18.pdf',
 'adsul-journal-nsf.pdf':'https://par.nsf.gov/servlets/purl/10317978',
 'adsul-arxiv-v4.pdf':'https://arxiv.org/pdf/1812.04611v4',
 'owr38-2018.pdf':'https://ems.press/content/serial-article-files/46760',
 'gilboa-zemel.pdf':'https://www.tau.ac.il/~igilboa/pdf/Gilboa_Zemel_Nash_Complexity.pdf',
 'conitzer-sandholm.pdf':'https://www.cs.cmu.edu/~conitzer/nashGEB08.pdf',
 'erickson-fox-lkhamsuren.pdf':'https://ekfox.web.illinois.edu/publications/holiest/holiest.pdf'}
def fetch(item):
 name,url=item;r={'name':name,'url':url}
 try:
  req=urllib.request.Request(url,headers={'User-Agent':'ResearchReview/1.0'})
  with urllib.request.urlopen(req,timeout=45) as response:
   b=response.read();r.update(resolved_url=response.geturl(),content_type=response.headers.get('Content-Type'))
  assert b.startswith(b'%PDF'), 'response is not PDF'
  p=out/name;p.write_bytes(b)
  subprocess.run(['pdftotext','-layout',str(p),str(p.with_suffix('.txt'))],check=True)
  info=subprocess.check_output(['pdfinfo',str(p)],text=True)
  pages=int(next(x.split(':')[1].strip() for x in info.splitlines() if x.startswith('Pages:')))
  r.update(status='saved',path=str(p),sha256=hashlib.sha256(b).hexdigest(),bytes=len(b),pages=pages,retrieved_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
 except Exception as e:r.update(status='error',error=repr(e))
 return r
with concurrent.futures.ThreadPoolExecutor(max_workers=7) as ex:results=list(ex.map(fetch,urls.items()))
(base/'primary_source_receipts.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2))
