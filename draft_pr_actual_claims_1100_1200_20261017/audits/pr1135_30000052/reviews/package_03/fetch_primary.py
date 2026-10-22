"""Fresh read-only primary retrievals; copyrighted bodies remain ignored."""
from pathlib import Path
from urllib.request import Request,urlopen
import hashlib,json,datetime,concurrent.futures
HERE=Path(__file__).resolve().parent
SOURCES={
 'owr.pdf':'https://ems.press/content/serial-article-files/45858',
 'ferudun.pdf':'https://eulersolve.org/papers/owr-723-005/paper.pdf?v=edb268431856',
 'zenodo.json':'https://zenodo.org/api/records/23372668',
 'pr.json':'https://api.github.com/repos/AlecKriebel/Math/pulls/1135',
 'repo.json':'https://api.github.com/repos/AlecKriebel/Math',
 'commit.json':'https://api.github.com/repos/AlecKriebel/Math/commits/e809a9c40f4ccdaced6f45f10b1dc8b7725a2119',
 'su.pdf':'https://math.hmc.edu/su/wp-content/uploads/sites/10/2019/06/A-LeVeque-type.pdf',
 'anderson.pdf':'https://aif.centre-mersenne.org/item/10.5802/aif.2298.pdf',
}
def fetch(item):
 name,url=item; row={'name':name,'requested_url':url,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 try:
  with urlopen(Request(url,headers={'User-Agent':'Independent mathematical source verification'}),timeout=60) as r:
   raw=r.read();row.update(status=r.status,final_url=r.url,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),content_type=r.headers.get('Content-Type'))
  (HERE/'sources/private'/name).write_bytes(raw)
 except Exception as e:row['error']=str(e)
 return row
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:rows=list(pool.map(fetch,SOURCES.items()))
(HERE/'SOURCE_FETCH.json').write_text(json.dumps(rows,indent=2)+'\n')
print(json.dumps(rows,indent=2))
