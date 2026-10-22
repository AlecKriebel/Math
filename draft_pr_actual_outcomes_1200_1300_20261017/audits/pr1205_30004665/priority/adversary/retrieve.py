from pathlib import Path
import urllib.request,json,hashlib,datetime,concurrent.futures
root=Path(__file__).parent
(root/'sources').mkdir(exist_ok=True)
urls={
'repo_metadata.json':'https://api.github.com/repos/mironovd/crystal',
'repo_commits.json':'https://api.github.com/repos/mironovd/crystal/commits?per_page=100',
'd4_history.json':'https://api.github.com/repos/mironovd/crystal/commits?path=crystal_D_4.out.xz&per_page=100',
'd4_data.xz':'https://raw.githubusercontent.com/mironovd/crystal/master/crystal_D_4.out.xz',
'ghkk_sage.txt':'https://raw.githubusercontent.com/mironovd/crystal/master/crystal_GHKK_support.sage',
'repo_readme.txt':'https://raw.githubusercontent.com/mironovd/crystal/master/README.md',
'abstract2023.pdf':'https://pca-pdmi.ru/2023/files/51/FpolyNewton-pca.pdf',
'slides2023.pdf':'https://pca-pdmi.ru/2023/files/51/F-poly-Newton%283%29.pdf',
'slides2024.pdf':'https://pca-pdmi.ru/2024/files/30/coefficients-pre2.pdf',
'preprint2022.pdf':'https://easychair.org/publications/preprint/z55N/open',
'easychair2022.html':'https://easychair.org/publications/preprint/z55N',
'conference2023.html':'https://pca-pdmi.ru/2023/',
'conference2024.html':'https://pca-pdmi.ru/2024/',
}
def get(item):
 name,url=item
 try:
  req=urllib.request.Request(url,headers={'User-Agent':'Math-independent-priority-audit/1.0'})
  with urllib.request.urlopen(req,timeout=45) as r:
   data=r.read(); final=r.url; headers=dict(r.headers)
  (root/'sources'/name).write_bytes(data)
  return dict(file=name,url=url,final_url=final,bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),retrieved_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),headers=headers)
 except Exception as e: return dict(file=name,url=url,error=str(e))
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:
 results=list(ex.map(get,urls.items()))
(root/'RETRIEVALS.json').write_text(json.dumps(results,indent=2)+'\n')
for r in results: print({k:r[k] for k in ['file','bytes','sha256','error'] if k in r})
