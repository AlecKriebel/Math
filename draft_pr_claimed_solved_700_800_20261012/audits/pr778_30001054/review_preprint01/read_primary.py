from urllib.request import urlopen,Request
from io import BytesIO
from pypdf import PdfReader
from pathlib import Path
import hashlib,json,datetime
BASE=Path(__file__).resolve().parent
sources=[('GP06','https://math.nyu.edu/inmemoriam/pollack/pubs/dblperm11-26-06.pdf',[0,1,2,3,4,5,6,7,8,9]),('OWR','https://ems.press/content/serial-article-files/46191?nt=1',[13,14,15,16,74]),('DGHP','https://math.nyu.edu/inmemoriam/pollack/pubs/interval.pdf',[0,4]),('HP','https://link.springer.com/content/pdf/10.1007%2Fs00454-013-9532-y.pdf',[71,72,73]),('Novick','https://link.springer.com/content/pdf/10.1007%2Fs00454-012-9457-x.pdf',[0,2,3])]
receipts=[]
for name,url,indices in sources:
 rec={'name':name,'url':url,'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 try:
  r=urlopen(Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=60);data=r.read()
  rec.update(bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),content_type=r.headers.get('Content-Type'),final_url=r.url)
  if not data.startswith(b'%PDF'):raise ValueError('received non-PDF body')
  p=PdfReader(BytesIO(data));rec['pages']=len(p.pages);rec['read_zero_based_pages']=indices
  print('\nSOURCE',name,rec,flush=True)
  for i in indices:
   print('\nPAGE',i+1,'\n',p.pages[i].extract_text(),flush=True)
  rec['status']='READ'
 except Exception as e:rec.update(status='ACCESS_LIMIT',error=repr(e));print(rec,flush=True)
 receipts.append(rec)
(BASE/'PRIMARY_RECEIPTS.json').write_text(json.dumps(receipts,indent=2)+'\n')
