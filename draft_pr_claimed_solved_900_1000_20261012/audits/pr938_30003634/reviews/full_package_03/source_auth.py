import concurrent.futures,hashlib,json,urllib.request
from pathlib import Path
from datetime import datetime,timezone
R=Path(__file__).resolve().parent;S=R.parents[1]/'private/root_primary'
urls={
'owr':'https://publications.mfo.de/bitstream/handle/mfo/3612/OWR_2017_50.pdf?isAllowed=y&sequence=1',
'otto':'https://msp.org/agt/2014/14-5/agt-v14-n5-p05-s.pdf',
'gg':'https://www.numdam.org/item/10.24033/bsmf.2496.pdf',
'erle':'https://da.lib.kobe-u.ac.jp/da/kernel/E0003685/E0003685.pdf',
'toffoli':'https://epub.uni-regensburg.de/52299/1/the-atiyahpatodisinger-rho-invariant-and-signatures-of-links.pdf',
'calegari':'https://math.uchicago.edu/~dannyc/books/scl/scl.pdf',
'kawasaki2025':'https://msp.org/agt/2025/25-2/agt-v25-n2-p15-s.pdf',
'chh_v3':'https://arxiv.org/pdf/1003.4977v3'}
def download(item):
 name,url=item;utc=datetime.now(timezone.utc).isoformat()
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'independent-mathematical-source-audit/1.0'}),timeout=45) as response:b=response.read();final=response.url
  if not b.startswith(b'%PDF'):raise RuntimeError('Not PDF')
  pin=hashlib.sha256(b).hexdigest();local=S/(name+'.pdf');same=local.exists() and hashlib.sha256(local.read_bytes()).hexdigest()==pin
  path=local if same else R/'private'/(name+'.pdf')
  if not same:path.write_bytes(b)
  return dict(name=name,url=url,final_url=final,utc=utc,bytes=len(b),sha256=pin,source_file=str(path),reused_only_after_fresh_network_hash_match=same,status='PASS')
 except Exception as e:return dict(name=name,url=url,utc=utc,status='ACCESS_FAILURE',error=str(e))
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:rows=list(pool.map(download,urls.items()))
(R/'SOURCE_PINS.json').write_text(json.dumps({'utc':datetime.now(timezone.utc).isoformat(),'primary_downloads':rows,'raw_bodies_publicly_redistributed':False},indent=2)+'\n')
for row in rows:print(row['name'],row['status'],row.get('sha256'),flush=True)
