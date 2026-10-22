from pathlib import Path
import concurrent.futures,datetime as dt,hashlib,json,subprocess,urllib.request
Q=Path(__file__).resolve().parent
items=[('pr0521_owr','https://ems.press/content/serial-article-files/46702?nt=1'),('pr0533_owr','https://publications.mfo.de/bitstream/handle/mfo/3111/OWR_2009_09.pdf?isAllowed=y&sequence=1'),('pr0563_problem','https://arxiv.org/pdf/1809.07200v2'),('pr0570_owr','https://publications.mfo.de/bitstream/handle/mfo/4442/OWR_2026_08.pdf?isAllowed=y&sequence=1')]
def get(item):
 name,url=item;p=Q/'private/primary'/name;p.parent.mkdir(parents=True,exist_ok=True)
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Independent-coverage-review/1.0'}),timeout=60) as f:b=f.read();status=f.status;final=f.url
  assert b.startswith(b'%PDF');p.with_suffix('.pdf').write_bytes(b);subprocess.run(['pdftotext','-layout',str(p.with_suffix('.pdf')),str(p.with_suffix('.txt'))],capture_output=True,check=True);return dict(name=name,url=url,status=status,final_url=final,at=dt.datetime.now(dt.timezone.utc).isoformat(),bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),pdf_path=str(p.with_suffix('.pdf').relative_to(Q)),text_sha256=hashlib.sha256(p.with_suffix('.txt').read_bytes()).hexdigest())
 except Exception as e:return dict(name=name,url=url,error=str(e),at=dt.datetime.now(dt.timezone.utc).isoformat())
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:r=list(pool.map(get,items))
(Q/'primary_source_receipts.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
