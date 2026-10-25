from pathlib import Path
import urllib.request, hashlib,json,datetime,concurrent.futures,subprocess
ROOT=Path(__file__).resolve().parent
CACHE=ROOT/'cache'/'primary-sources';CACHE.mkdir(parents=True,exist_ok=True)
items=[('szemberg0711v1','https://arxiv.org/pdf/0711.0584v1'),('primer0810v2','https://arxiv.org/pdf/0810.0728v2'),('adjoint1011v1','https://arxiv.org/pdf/1011.0979v1'),('bauer9903v1','https://arxiv.org/pdf/math/9903072v1'),('fuentes0511v2','https://arxiv.org/pdf/math/0511547v2'),('canonical0801v1','https://arxiv.org/pdf/0801.3245v1'),('ein-lazarsfeld1993','https://www.numdam.org/item/AST_1993__218__177_0.pdf'),('owr2009-21','https://publications.mfo.de/bitstream/handle/mfo/328/OWR_2009_21.pdf')]
def fetch(item):
 name,url=item
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'ResearchScope/1.0'}),timeout=45) as r: data=r.read();resolved=r.url
  if not data.startswith(b'%PDF'): raise ValueError('Not PDF: '+str(data[:40]))
  out=CACHE/(name+'.pdf');out.write_bytes(data)
  subprocess.run(['pdftotext','-layout',str(out),str(out.with_suffix('.txt'))],check=True)
  result={'name':name,'url':url,'resolved_url':resolved,'retrieved_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'cached_path':str(out),'status':'retrieved'}
 except Exception as e: result={'name':name,'url':url,'status':'unavailable','error':str(e)}
 return result
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool: records=list(pool.map(fetch,items))
(ROOT/'primary-source-receipts.json').write_text(json.dumps(records,indent=2)+'\n')
for r in records: print(r['name'],r['status'],r.get('sha256',r.get('error')))
