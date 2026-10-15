#!/usr/bin/env python3
"""Fetch exact primary versions privately; publish receipts, never snapshots."""
import concurrent.futures, datetime, hashlib, json, urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'primary_reading'
OUT.mkdir(exist_ok=True)
URLS={
 'dhw2010.pdf':'https://eccc.weizmann.ac.il/report/2010/078/download/',
 'dell2014-v1.pdf':'https://arxiv.org/pdf/1206.1775v1',
 'dell2014-v1.src':'https://arxiv.org/src/1206.1775v1',
 'mcquillan-v1.pdf':'https://arxiv.org/pdf/1301.2880v1',
 'mcquillan-v1.src':'https://arxiv.org/src/1301.2880v1',
 'rsz-v2.pdf':'https://arxiv.org/pdf/1409.3905v2',
 'rsz-v2.src':'https://arxiv.org/src/1409.3905v2',
 'barvinok-v1.pdf':'https://arxiv.org/pdf/1601.07518v1',
 'barvinok-v1.src':'https://arxiv.org/src/1601.07518v1',
 'barvinok-v5.pdf':'https://arxiv.org/pdf/1601.07518v5',
 'barvinok-v5.src':'https://arxiv.org/src/1601.07518v5',
 'jvv1986.pdf':'https://www2.stat.duke.edu/homeweb/scs/Courses/Stat376/Papers/ConvergeRates/RandomizedAlgs/JerrumValiantVaziraniTCS1986.pdf',
 'yi-v1.pdf':'https://arxiv.org/pdf/2609.04079v1',
 'yi-v1.src':'https://arxiv.org/src/2609.04079v1',
 'cai-liu1904-v1.pdf':'https://arxiv.org/pdf/1904.10493v1',
 'cai-liu1904-v1.src':'https://arxiv.org/src/1904.10493v1',
}
def get(item):
 name,url=item
 when=datetime.datetime.now(datetime.timezone.utc).isoformat()
 try:
  req=urllib.request.Request(url,headers={'User-Agent':'Independent mathematical source review'})
  with urllib.request.urlopen(req,timeout=60) as r:
   data=r.read(); final=r.url; ct=r.headers.get('Content-Type')
  (OUT/name).write_bytes(data)
  return {'file':name,'url':url,'resolved_url':final,'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data),'content_type':ct,'retrieved_utc':when}
 except Exception as e: return {'file':name,'url':url,'retrieved_utc':when,'error':str(e)}
if __name__=='__main__':
 with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool: rows=list(pool.map(get,URLS.items()))
 (ROOT/'SOURCE_RECEIPTS.json').write_text(json.dumps(rows,indent=2)+'\n')
 for row in rows: print(row['file'],row.get('bytes'),row.get('sha256'),row.get('error',''))
