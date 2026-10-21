"""Read-only network retrieval of selected primary reading copies; no source execution."""
import datetime,hashlib,json,urllib.request
from pathlib import Path
B=Path(__file__).resolve().parent
jobs=[
 ('ferudun14_v11.pdf','https://eulersolve.org/papers/amr-050-0014/paper.pdf?v=5ff816c279e3'),
 ('ferudun21.pdf','https://eulersolve.org/papers/amr-050-0021/paper.pdf?v=34ff068237a7'),
 ('pedallike_2009.02581v3.pdf','https://arxiv.org/pdf/2009.02581v3'),
 ('topics_2108.08293v1.pdf','https://arxiv.org/pdf/2108.08293v1')]
rows=[]
for name,url in jobs:
 row={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'url':url,'file':'private_reading/'+name}
 try:
  req=urllib.request.Request(url,headers={'User-Agent':'Independent mathematics research audit'})
  with urllib.request.urlopen(req,timeout=30) as r:data=r.read(4000000);row.update(status=r.status,final_url=r.url,content_type=r.headers.get('Content-Type'))
  if not data.startswith(b'%PDF'):raise ValueError('Response is not a PDF')
  (B/row['file']).write_bytes(data);row.update(bytes=len(data),sha256=hashlib.sha256(data).hexdigest())
 except Exception as e:row['error']=str(e)
 rows.append(row)
(B/'RETRIEVAL_RECEIPT.json').write_text(json.dumps(rows,indent=2)+'\n')
print(json.dumps(rows,indent=2))
