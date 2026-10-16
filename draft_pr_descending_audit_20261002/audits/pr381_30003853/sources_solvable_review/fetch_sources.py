#!/usr/bin/env python3
"""Fresh primary-source retrieval, with locally retained unredistributed bytes."""
from pathlib import Path
import concurrent.futures, datetime, hashlib, json, subprocess, urllib.request
ROOT = Path(__file__).resolve().parent
SOURCES = {
 "owr2018": "https://ems.press/content/serial-article-files/46748",
 "bgk": "https://arxiv.org/pdf/0807.5138v1",
 "guba_sapir": "https://arxiv.org/pdf/math/0301225v2",
 "golan": "https://arxiv.org/pdf/2609.14702v1",
 "farley": "https://arxiv.org/pdf/2606.27753v2",
 "bleak_algebraic": "https://arxiv.org/pdf/math/0602038v2",
 "bleak_geometric": "https://arxiv.org/pdf/math/0602036v2",
}
def fetch(item):
 name, url = item
 start = datetime.datetime.now(datetime.timezone.utc).isoformat()
 try:
  with urllib.request.urlopen(url, timeout=60) as response:
   data = response.read()
   meta = dict(status=response.status, final_url=response.url, headers=dict(response.headers))
  path = ROOT / 'raw_sources' / (name + '.pdf')
  path.write_bytes(data)
  if not data.startswith(b'%PDF-'):
   raise ValueError('Not PDF bytes')
  subprocess.run(['pdftotext', '-layout', str(path), str(path.with_suffix('.txt'))], check=True)
  return dict(name=name, url=url, retrieved_utc=start, bytes=len(data), sha256=hashlib.sha256(data).hexdigest(), pdf=True, **meta)
 except Exception as exc:
  return dict(name=name, url=url, retrieved_utc=start, error=repr(exc))
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
 records = list(pool.map(fetch, SOURCES.items()))
receipt = dict(created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(), records=records)
(ROOT / 'SOURCE_RECEIPT.json').write_text(json.dumps(receipt, indent=2) + '\n')
print(json.dumps(receipt, indent=2))
