import concurrent.futures,hashlib,json,subprocess,urllib.request
from pathlib import Path
from datetime import datetime,timezone
R=Path(__file__).resolve().parent;A=R.parents[1]
urls={
'owr_ems':'https://ems.press/content/serial-article-files/46709',
'diprisa_framba_published':'https://content.ems.press/assets/public/full-texts/serials/rmi/41/5/14298907/online/10.4171-rmi-1573.pdf',
'kuzbary_v2':'https://arxiv.org/pdf/2009.04641v2',
'bk2015':'https://msp.org/agt/2015/15-5/agt-v15-n5-p11-s.pdf'}
def fetch(item):
 name,url=item
 try:
  with urllib.request.urlopen(url,timeout=40) as f:b=f.read();final=f.url
  if not b.startswith(b'%PDF'):raise RuntimeError('non-PDF')
  pin=hashlib.sha256(b).hexdigest();path=None
  # Only re-use source files from the settled selected-target priority family.
  for family in ['recent_priority','classical_priority']:
   for p in (A/'reviews'/family/'private').glob('*.pdf'):
    if hashlib.sha256(p.read_bytes()).hexdigest()==pin:path=p;break
   if path:break
  reused=path is not None
  if not path:path=R/'private'/(name+'.pdf');path.write_bytes(b)
  subprocess.run(['pdftotext','-layout',str(path),str(R/'private'/(name+'.txt'))],check=True)
  return dict(name=name,url=url,final_url=final,bytes=len(b),sha256=pin,utc=datetime.now(timezone.utc).isoformat(),source_file=str(path),reused_only_after_fresh_network_hash_match=reused,status='PASS')
 except Exception as e:return dict(name=name,url=url,status='ACCESS_FAILURE',error=str(e))
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:rows=list(pool.map(fetch,urls.items()))
(R/'ADDITIONAL_SOURCE_PINS.json').write_text(json.dumps({'utc':datetime.now(timezone.utc).isoformat(),'primary_downloads':rows,'raw_bodies_publicly_redistributed':False},indent=2)+'\n')
for row in rows:print(row['name'],row['status'],row.get('sha256'))
