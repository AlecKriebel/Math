"""Read-only primary website HTML capture, including a source-ID route probe."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
import hashlib,json,urllib.request

ROOT=Path(__file__).resolve().parent
URLS={
 'eulersolve_index':'https://eulersolve.org/papers/',
 'eulersolve_source_id_probe':'https://eulersolve.org/papers/owr-16633-006/',
 'springer_mastroianni_totik_2010':'https://link.springer.com/article/10.1007/s00365-009-9047-1',
 'springer_ivanov_totik_1990':'https://link.springer.com/article/10.1007/BF01891406',
 'springer_kroo_2016':'https://link.springer.com/article/10.1007/s10474-016-0593-2',
 'springer_kroo_2026':'https://link.springer.com/article/10.1007/s00365-025-09722-7',
}

def fetch(item):
 key,url=item
 rec={'id':key,'requested_url':url,'retrieved_utc':datetime.now(timezone.utc).isoformat()}
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=30) as resp:
   body=resp.read();rec.update(final_url=resp.url,status=resp.status,content_type=resp.headers.get('Content-Type'))
  p=ROOT/'_local'/'primary'/(key+'.html');p.write_bytes(body)
  rec.update(bytes=len(body),sha256=hashlib.sha256(body).hexdigest(),local_path=str(p.relative_to(ROOT)))
 except Exception as e:rec['error']=str(e)
 return rec

if __name__=='__main__':
 with ThreadPoolExecutor(max_workers=6) as pool:records=list(pool.map(fetch,URLS.items()))
 (ROOT/'WEB_RETRIEVAL_RECEIPT.json').write_text(json.dumps(records,indent=2)+'\n')
 print(json.dumps(records,indent=2))
