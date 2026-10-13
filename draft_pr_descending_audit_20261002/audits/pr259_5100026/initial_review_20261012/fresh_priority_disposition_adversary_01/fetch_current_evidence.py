"""Read-only fresh evidence retrieval. All downloaded bodies remain private."""
from pathlib import Path
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor
import hashlib, json, urllib.request

HERE = Path(__file__).resolve().parent
PRIVATE = HERE / 'private_reading'
PRIVATE.mkdir(exist_ok=True)
TARGETS = [
 ('current_zenodo_record.json', 'https://zenodo.org/api/records/23071366?fresh-adversary=20261012'),
 ('current_datacite.json', 'https://api.datacite.org/dois/10.5281/zenodo.23071366'),
 ('current_zenodo_main.pdf', 'https://zenodo.org/api/records/23071366/files/main.pdf/content'),
]
def get(item):
 name, url = item
 r = {'name': name, 'url': url, 'method': 'GET', 'started_utc': datetime.now(timezone.utc).isoformat()}
 try:
  req = urllib.request.Request(url, headers={'User-Agent': 'Independent mathematical source audit'})
  with urllib.request.urlopen(req, timeout=35) as response:
   body=response.read(); r.update(status=response.status, final_url=response.geturl(), headers=dict(response.headers))
  (PRIVATE/name).write_bytes(body)
  r.update(bytes=len(body), sha256=hashlib.sha256(body).hexdigest(), md5=hashlib.md5(body).hexdigest())
 except Exception as e:
  r['error']=repr(e)
 r['finished_utc']=datetime.now(timezone.utc).isoformat()
 return r
with ThreadPoolExecutor(max_workers=3) as pool:
 receipts=list(pool.map(get,TARGETS))
(HERE/'FRESH_GET_RECEIPTS.json').write_text(json.dumps({'method_policy':'GET only; no communication to individuals', 'receipts':receipts},indent=2)+'\n')
print(json.dumps([{k:v for k,v in r.items() if k in ['name','status','bytes','sha256','error']} for r in receipts],indent=2))
