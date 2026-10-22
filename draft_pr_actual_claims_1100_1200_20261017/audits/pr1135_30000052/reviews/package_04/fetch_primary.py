#!/usr/bin/env python3
from pathlib import Path
import urllib.request,hashlib,json,datetime
ROOT=Path(__file__).resolve().parent
URLS={
 'novak.pdf':'https://ems.press/content/serial-article-files/45858',
 'ferudun.pdf':'https://eulersolve.org/papers/owr-723-005/paper.pdf?v=edb268431856',
 'su.pdf':'https://math.hmc.edu/su/wp-content/uploads/sites/10/2019/06/A-LeVeque-type.pdf',
 'aif.pdf':'https://aif.centre-mersenne.org/item/10.5802/aif.2298.pdf',
 'zenodo.json':'https://zenodo.org/api/records/23372668',
 'github_pr.json':'https://api.github.com/repos/AlecKriebel/Math/pulls/1135',
 'github_commit.json':'https://api.github.com/repos/AlecKriebel/Math/commits/e809a9c40f4ccdaced6f45f10b1dc8b7725a2119',
}
rows=[]
for name,url in URLS.items():
 row={'url':url,'retrieved_utc':datetime.datetime.now(datetime.UTC).isoformat(),'local_private_file':name}
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Independent-mathematical-audit/1.0'}),timeout=45) as f:
   data=f.read();row.update(status=f.status,final_url=f.url,content_type=f.headers.get('Content-Type'))
  (ROOT/'sources/private'/name).write_bytes(data)
  row.update(bytes=len(data),sha256=hashlib.sha256(data).hexdigest())
 except Exception as e: row['error']=str(e)
 rows.append(row)
(ROOT/'SOURCE_FETCH.json').write_text(json.dumps(rows,indent=2)+'\n')
print(json.dumps(rows,indent=2))
