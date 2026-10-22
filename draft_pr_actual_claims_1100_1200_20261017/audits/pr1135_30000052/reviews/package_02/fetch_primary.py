from pathlib import Path
import urllib.request,hashlib,json,datetime,concurrent.futures
R=Path(__file__).resolve().parent; D=R/'sources/private'
URLS={
'owr.pdf':'https://ems.press/content/serial-article-files/45858',
'ferudun.pdf':'https://eulersolve.org/papers/owr-723-005/paper.pdf?v=edb268431856',
'zenodo.json':'https://zenodo.org/api/records/23372668',
'pr.json':'https://api.github.com/repos/AlecKriebel/Math/pulls/1135',
'commits.json':'https://api.github.com/repos/AlecKriebel/Math/pulls/1135/commits',
'repo.json':'https://api.github.com/repos/AlecKriebel/Math',
'su.pdf':'https://math.hmc.edu/su/wp-content/uploads/sites/10/2019/06/A-LeVeque-type.pdf',
'anderson.pdf':'https://aif.centre-mersenne.org/item/10.5802/aif.2298.pdf',
'book.pdf':'https://web.maths.unsw.edu.au/~josefdick/preprints/Novak_Wozniakowski_book_2.pdf',
}
def fetch(q):
 name,url=q; row={'name':name,'url':url,'timestamp':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Independent mathematical source review'}),timeout=45) as r:
   b=r.read();row.update(status=r.status,final_url=r.url,bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),content_type=r.headers.get('Content-Type'));(D/name).write_bytes(b)
 except Exception as e: row['error']=str(e)
 return row
rows=list(concurrent.futures.ThreadPoolExecutor(max_workers=4).map(fetch,URLS.items()))
(R/'SOURCE_FETCH.json').write_text(json.dumps(rows,indent=2)+'\n');print(json.dumps(rows,indent=2))
