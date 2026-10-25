from pathlib import Path
from urllib.request import urlopen,Request
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime,timezone
import hashlib,json
R=Path(__file__).resolve().parents[2]; M=json.loads((R/'sources/published-source/sources/PINNED_MANIFEST.json').read_text()); C=R/'sources/primary/.cache/pinned-oai';C.mkdir(parents=True,exist_ok=True)
def get(x):
 u=f"https://raw.githubusercontent.com/openai/math/{M['commit']}/{x['path']}";p=C/x['path'];p.parent.mkdir(parents=True,exist_ok=True)
 d={'path':x['path'],'url':u,'retrieved_utc':datetime.now(timezone.utc).isoformat()}
 try:
  with urlopen(Request(u,headers={'User-Agent':'Research source scope review'}),timeout=35) as z:b=z.read();d.update(status=z.status,headers=dict(z.headers))
  p.write_bytes(b);h=hashlib.sha256(b).hexdigest();d.update(bytes=len(b),sha256=h,expected_sha256=x['sha256'],expected_bytes=x['bytes'],matches_published_pin=h==x['sha256'] and len(b)==x['bytes'])
 except Exception as e:d['error']=repr(e)
 return d
with ThreadPoolExecutor(max_workers=6) as ex: rows=list(ex.map(get,M['files']))
(R/'sources/primary/pinned_oai_source_receipts.json').write_text(json.dumps({'commit':M['commit'],'files':rows},indent=2)+'\n')
print(json.dumps({'files':len(rows),'all_match':all(x.get('matches_published_pin') for x in rows),'errors':[x for x in rows if x.get('error')]},indent=2))
