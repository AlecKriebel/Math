from pathlib import Path
import datetime as dt,hashlib,json,os,subprocess,sys,time,urllib.request
sys.dont_write_bytecode=True
Q=Path(__file__).resolve().parent
SOURCES={582:('https://ems.press/content/serial-article-files/46844',[29]),585:('https://ems.press/content/serial-article-files/46224?nt=1',[24]),618:('https://ems.press/content/serial-article-files/46883',[59,60]),623:('https://publications.mfo.de/bitstream/handle/mfo/3111/OWR_2009_09.pdf?isAllowed=y&sequence=1',[5,6,50,51])}
def sha(b):return hashlib.sha256(b).hexdigest()
def now():return dt.datetime.now(dt.timezone.utc).isoformat()
records=[]
for n,(url,pages) in SOURCES.items():
 for attempt in range(3):
  try:
   with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Independent-mathematical-source-identity-review/1.0'}),timeout=45) as resp:b=resp.read();status=resp.status;final=resp.url
   break
  except Exception:
   if attempt==2:raise
   time.sleep(attempt+1)
 assert b.startswith(b'%PDF-') and status==200
 folder=Q/f'private/primary_{n}';folder.mkdir(parents=True,exist_ok=True);p=folder/'source.pdf';p.write_bytes(b)
 text=subprocess.run(['pdftotext','-layout',str(p),'-'],capture_output=True,check=True).stdout.decode();(folder/'source.txt').write_text(text);split=text.split('\f');excerpts=[]
 for page in pages:
  (folder/f'page_{page}.txt').write_text(split[page-1]);base=folder/f'page_{page}';subprocess.run(['pdftoppm','-f',str(page),'-l',str(page),'-singlefile','-r','100','-png',str(p),str(base)],capture_output=True,check=True);excerpts.append(dict(pdf_page=page,text_sha256=sha((folder/f'page_{page}.txt').read_bytes()),rendered_sha256=sha(base.with_suffix('.png').read_bytes())))
 records.append(dict(pr=n,url=url,final_url=final,http_status=status,bytes=len(b),sha256=sha(b),pages=excerpts,scope='Original target identity only; no new proof or priority audit. Fulltext and renderedpages remain private.'))
 print(json.dumps(dict(pr=n,bytes=len(b),pages=pages)),flush=True)
(Q/'primary_source_receipts.json').write_text(json.dumps(dict(at=now(),sources=records),indent=2)+'\n')
