from pathlib import Path
import urllib.request,hashlib,json,datetime,concurrent.futures
R=Path(__file__).resolve().parent
sources=[('L','https://letu.math.gatech.edu/Papers/PERT_NEW01.pdf'),('H','https://arxiv.org/pdf/math/0605314v1'),('LMO','https://letu.math.gatech.edu/Papers/LMO.pdf'),('GLM','https://letu.math.gatech.edu/Papers/Free_Energy.pdf'),('KLO','https://letu.math.gatech.edu/Papers/LMO_Conjecture.pdf'),('BG','https://d-nb.info/1355311616/34'),('FZ','https://arxiv.org/pdf/2608.29585v1'),('Fang','https://arxiv.org/pdf/2610.21102v1'),('GW','https://arxiv.org/pdf/2603.01619v1'),('O_record','https://msp.org/gtm/2002/04/p024.xhtml'),('O_solutions','https://www.kurims.kyoto-u.ac.jp/~tomotada/solution.html'),('FZ_record','https://arxiv.org/abs/2608.29585v1'),('Fang_record','https://arxiv.org/abs/2610.21102v1'),('Sawin','https://www.worldscientific.com/doi/pdf/10.1142/S0218216523400266'),('Sawin_crossref','https://api.crossref.org/works/10.1142/S0218216523400266'),('AIM','https://aimath.org/pastworkshops/quantumlowdimtoprep.pdf')]
def fetch(item):
 name,url=item;t=datetime.datetime.now(datetime.timezone.utc).isoformat()
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Math-independent-review04/1.0'}),timeout=30) as r:b=r.read();code=r.status;final=r.url;mime=r.headers.get('Content-Type')
  extension='.pdf' if b[:4]==b'%PDF' else '.txt';(R/'private'/(name+extension)).write_bytes(b)
  return {'id':name,'url':url,'utc':t,'status':code,'final_url':final,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'type':mime,'saved_private':True}
 except Exception as e:return {'id':name,'url':url,'utc':t,'error':str(e),'saved_private':False}
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:rows=list(pool.map(fetch,sources))
(R/'SOURCE_RETRIEVALS.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'retrievals':rows,'body_hashing_is_not_reading':True},indent=2)+'\n')
for r in rows:print(r['id'],r.get('status',r.get('error')),r.get('bytes'))
