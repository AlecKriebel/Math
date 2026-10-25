from pathlib import Path
import urllib.request,hashlib,json,datetime,concurrent.futures,subprocess
OUT=Path(__file__).resolve().parent;CACHE=OUT/'cache/primary-sources';CACHE.mkdir(parents=True,exist_ok=True)
items=[
('owr2017-50-published.pdf','https://ems.press/content/serial-article-files/46709?nt=1','Original published OWR2017/50, publication19December2018'),
('gambaudo-ghys-published.pdf','https://www.numdam.org/item/10.24033/bsmf.2496.pdf','Published Bull.Soc.Math.France133(2005),541–579'),
('otto-published.pdf','https://msp.org/agt/2014/14-5/agt-v14-n5-p05-s.pdf','Published AGT14(2014),2627–2654'),
('toffoli-published.pdf','https://epub.uni-regensburg.de/52299/1/the-atiyahpatodisinger-rho-invariant-and-signatures-of-links.pdf','Repository-held published journal article, DOI10.1017/S0013091522000153,2022'),
('calegari-scl-author.pdf','https://math.uchicago.edu/~dannyc/books/scl/scl.pdf','Author-hosted scl book; bibliographic reference MSJMemoirs20(2009); fetched bytes version-bound without claiming equality to finalpublisherfile'),
('kkmmm-published.pdf','https://msp.org/agt/2025/25-2/agt-v25-n2-p15-p.pdf','Published AGT25(2025),1169–1226;16May2025'),
('erle-published.pdf','https://da.lib.kobe-u.ac.jp/da/kernel/E0003685/E0003685.pdf','Repository version of record, KobeJ.Math.16(1999),161–175')]
def get(x):
 name,url,version=x;item={'name':name,'url':url,'version':version,'retrieved_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 try:
  r=urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Research-source-verification/1.0'}),timeout=40);b=r.read();item['resolved_url']=r.geturl()
  if not b.startswith(b'%PDF'):raise ValueError('Response is not PDF')
  p=CACHE/name;p.write_bytes(b)
  item.update(status='acquired',bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
  info=subprocess.run(['pdfinfo',str(p)],capture_output=True,text=True,check=True).stdout
  item['pdfinfo']=info
  subprocess.run(['pdftotext','-layout',str(p),str(p.with_suffix('.txt'))],check=True)
 except Exception as e:item.update(status='failed',error=str(e))
 print(json.dumps({k:v for k,v in item.items() if k!='pdfinfo'}),flush=True)
 return item
with concurrent.futures.ThreadPoolExecutor(max_workers=7) as pool:results=list(pool.map(get,items))
(OUT/'primary-source-receipts.json').write_text(json.dumps(results,indent=2,ensure_ascii=False)+'\n')
