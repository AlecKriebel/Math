"""Re-fetch and hash primary bodies. Foreign bytes confined to ignored tmp."""
from pathlib import Path
from datetime import datetime,timezone
from concurrent.futures import ThreadPoolExecutor
import hashlib,json,urllib.request
base=Path(__file__).resolve().parent;parent=base.parent
sources=json.loads((parent/'reviewed_candidate/source_provenance.json').read_text())['sources']
sources += [
 {'local_basename':'kn-author-final.pdf','url':'https://sites.math.washington.edu/~novik/publications/sphere-products.pdf','sha256':'d6ac2df9d45fd803fa10b8d61ee5c01c5819074bc1c4279814030b10e646c2fa','bytes':185246},
 {'local_basename':'rs-book.djvu','url':'https://www.maths.gla.ac.uk/~mpowell/Rourke%20C.P.%2C%20Sanderson%20B.J.%20Introduction%20to%20piecewise-linear%20topology%20%28Springer%2C%201972%29.djvu','sha256':'f35d9f3dbe0ef110044ce3a7b080ddafb8791410c243794aecd76d444782fa92','bytes':1441873},
 {'local_basename':'shiota-yokoi.pdf','url':'https://www.ams.org/journals/tran/1984-286-02/S0002-9947-1984-0760983-2/S0002-9947-1984-0760983-2.pdf'}]
def fetch(s):
 row={'requested_url':s['url'],'utc':datetime.now(timezone.utc).isoformat(),'local_foreign_path':'tmp/sources/'+s['local_basename']}
 try:
  req=urllib.request.Request(s['url'],headers={'User-Agent':'Independent mathematical source audit'})
  with urllib.request.urlopen(req,timeout=45) as r:data=r.read();row['resolved_url']=r.geturl();row['http_status']=r.status;row['content_type']=r.headers.get('Content-Type')
  target=base/row['local_foreign_path'];target.parent.mkdir(exist_ok=True);target.write_bytes(data)
  row.update(bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),is_pdf=data.startswith(b'%PDF'),is_djvu=data.startswith(b'AT&TFORM'))
  row['expected_sha256']=s.get('sha256');row['matches_recorded_bytes']=('sha256' not in s or row['sha256']==s['sha256']) and ('bytes' not in s or len(data)==s['bytes'])
 except Exception as e:row['error']=repr(e)
 return row
(base/'tmp/sources').mkdir(exist_ok=True)
with ThreadPoolExecutor(max_workers=5) as ex:rows=list(ex.map(fetch,sources))
result={'utc':datetime.now(timezone.utc).isoformat(),'rows':rows,'scope':'Re-fetch establishes byte reproducibility only; primary theorem content checked independently. Foreign source files ignored.'}
(base/'SOURCE_RECEIPTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
