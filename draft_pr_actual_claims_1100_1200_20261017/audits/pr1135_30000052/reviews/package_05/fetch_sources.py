#!/usr/bin/env python3
"""Read-only primary retrieval; bodies stay under ignored sources/private."""
from pathlib import Path
import concurrent.futures,datetime,hashlib,json,urllib.request
HERE=Path(__file__).resolve().parent
URLS={
 'owr2004.pdf':'https://ems.press/content/serial-article-files/45858',
 'ferudun2026.pdf':'https://eulersolve.org/papers/owr-723-005/paper.pdf?v=edb268431856',
 'ferudun_page.html':'https://eulersolve.org/papers/owr-723-005/',
 'ferudun_record.json':'https://zenodo.org/api/records/23372668',
 'su2000.pdf':'https://math.hmc.edu/su/wp-content/uploads/sites/10/2019/06/A-LeVeque-type.pdf',
 'anderson2007.pdf':'https://aif.centre-mersenne.org/item/10.5802/aif.2298.pdf',
 'novak_book_draft.pdf':'https://web.maths.unsw.edu.au/~josefdick/preprints/Novak_Wozniakowski_book_2.pdf',
 'pr1135.json':'https://api.github.com/repos/AlecKriebel/Math/pulls/1135',
 'pr1135_files.json':'https://api.github.com/repos/AlecKriebel/Math/pulls/1135/files?per_page=100',
 'source_commit.json':'https://api.github.com/repos/AlecKriebel/Math/commits/e809a9c40f4ccdaced6f45f10b1dc8b7725a2119',
 'repository.json':'https://api.github.com/repos/AlecKriebel/Math',
}
for name in ['ACCEPTANCE.json','ACCEPTANCE.md','AUDIT.md','MANIFEST.json','PROOF.md','README.md','SOURCE_METADATA.json','SOURCE_REVIEW.md','STATUS.json','VERIFICATION.md']:
 URLS['remote_'+name]='https://raw.githubusercontent.com/AlecKriebel/Math/e809a9c40f4ccdaced6f45f10b1dc8b7725a2119/unsolved_math_prioritization/attempts/30000052/'+name

def fetch(item):
 name,url=item;row={'name':name,'url':url,'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 try:
  request=urllib.request.Request(url,headers={'User-Agent':'Independent-mathematical-package-audit/1.0'})
  with urllib.request.urlopen(request,timeout=45) as response:
   body=response.read();row.update(status=response.status,final_url=response.url,bytes=len(body),sha256=hashlib.sha256(body).hexdigest())
  (HERE/'sources/private'/name).write_bytes(body)
 except Exception as error:row.update(error=type(error).__name__+': '+str(error))
 return row

if __name__=='__main__':
 with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:rows=list(pool.map(fetch,URLS.items()))
 (HERE/'SOURCE_FETCH.json').write_text(json.dumps(rows,indent=2,sort_keys=True)+'\n')
 print(json.dumps(rows,indent=2))
