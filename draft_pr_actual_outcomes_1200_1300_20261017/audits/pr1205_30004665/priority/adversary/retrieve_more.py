from pathlib import Path
import urllib.request,json,hashlib,datetime,concurrent.futures
root=Path(__file__).parent
urls={
'd4_introduction_commit.json':'https://api.github.com/repos/mironovd/crystal/commits/573b512df531ec2d349ed05b3aa9f385989e13dd',
'd4_rename_commit.json':'https://api.github.com/repos/mironovd/crystal/commits/0d6e564cf5e69d79c1074d5d1e3e72ac700904d6',
'd4_20200306.xz':'https://raw.githubusercontent.com/mironovd/crystal/573b512df531ec2d349ed05b3aa9f385989e13dd/crystal.D4.out.xz',
'd4_20220529.xz':'https://raw.githubusercontent.com/mironovd/crystal/aedc5e79ce529f4cc93fd33b0a79700b1edee98a/crystal_D_4.out.xz',
'ghkk_20220529.txt':'https://raw.githubusercontent.com/mironovd/crystal/aedc5e79ce529f4cc93fd33b0a79700b1edee98a/crystal_GHKK_support.sage',
'ks2022.pdf':'https://link.springer.com/content/pdf/10.1007/s10801-022-01144-z.pdf',
'owr2021.pdf':'https://ems.press/content/serial-article-files/46898',
'kkn2022.pdf':'https://arxiv.org/pdf/2207.08065v1',
'gks2017.pdf':'https://arxiv.org/pdf/1711.07176v1',
}
def get(item):
 name,url=item
 try:
  req=urllib.request.Request(url,headers={'User-Agent':'Math-independent-priority-audit/1.0'})
  with urllib.request.urlopen(req,timeout=50) as r:
   data=r.read(); final=r.url; headers=dict(r.headers)
  (root/'sources'/name).write_bytes(data)
  return dict(file=name,url=url,final_url=final,bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),retrieved_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),headers=headers)
 except Exception as e: return dict(file=name,url=url,error=str(e))
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex: results=list(ex.map(get,urls.items()))
(root/'RETRIEVALS_MORE.json').write_text(json.dumps(results,indent=2)+'\n')
for r in results: print({k:r[k] for k in ['file','bytes','sha256','error'] if k in r})
