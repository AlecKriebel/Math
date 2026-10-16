import concurrent.futures,hashlib,json,urllib.request
from pathlib import Path
from datetime import datetime,timezone
R=Path(__file__).resolve().parent;A=R.parents[1]
old=json.loads((A/'reviews/full_package_03/SOURCE_PINS.json').read_bytes())['primary_downloads']+json.loads((A/'reviews/full_package_03/ADDITIONAL_SOURCE_PINS.json').read_bytes())['primary_downloads']
def auth(row):
 name=row['name'];url=row['url'];utc=datetime.now(timezone.utc).isoformat()
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'independent-mathematical-source-audit/1.0'}),timeout=45) as response:b=response.read();final=response.url
  if not b.startswith(b'%PDF'):raise RuntimeError('Not PDF')
  pin=hashlib.sha256(b).hexdigest();cached=Path(row['source_file']);same=cached.is_file() and hashlib.sha256(cached.read_bytes()).hexdigest()==pin
  p=cached if same else R/'private'/(name+'.pdf')
  if not same:p.write_bytes(b)
  return dict(name=name,url=url,final_url=final,utc=utc,bytes=len(b),sha256=pin,source_file=str(p),reused_only_after_fresh_network_hash_match=same,status='PASS')
 except Exception as error:return dict(name=name,url=url,utc=utc,status='ACCESS_FAILURE',error=str(error))
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:rows=list(pool.map(auth,old))
(R/'SOURCE_PINS.json').write_text(json.dumps({'utc':datetime.now(timezone.utc).isoformat(),'primary_downloads':rows,'raw_bodies_publicly_redistributed':False},indent=2)+'\n')
for x in rows:print(x['name'],x['status'],x.get('sha256'),flush=True)
