from pathlib import Path
import concurrent.futures, datetime, hashlib, json, subprocess, urllib.request
A=Path(__file__).resolve().parent
sources=[('OWR','https://publications.mfo.de/bitstream/handle/mfo/3705/OWR_2019_51.pdf?sequence=4'),('2608.01884v2','https://arxiv.org/pdf/2608.01884v2'),('2609.20401v1','https://arxiv.org/pdf/2609.20401v1'),('2609.24640v1','https://arxiv.org/pdf/2609.24640v1'),('2401.12904v2','https://arxiv.org/pdf/2401.12904v2'),('1705.08493v1','https://arxiv.org/pdf/1705.08493v1'),('2001.08905v1','https://arxiv.org/pdf/2001.08905v1'),('1610.00477v1','https://arxiv.org/pdf/1610.00477v1'),('1511.08477v3','https://arxiv.org/pdf/1511.08477v3')]
def get(row):
 name,url=row
 result={'name':name,'url':url,'retrieved_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 try:
  with urllib.request.urlopen(url,timeout=45) as r:raw=r.read();result['status']=r.status;result['final_url']=r.url
  if not raw.startswith(b'%PDF'):raise RuntimeError('not PDF')
  p=A/'sources/private'/(name+'.pdf');p.write_bytes(raw)
  subprocess.run(['pdftotext','-layout',str(p),str(p.with_suffix('.txt'))],check=True,capture_output=True)
  result.update(bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),private_path=str(p.relative_to(A)))
 except Exception as ex:result['error']=str(ex)
 return result
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:results=list(ex.map(get,sources))
(A/'PRIMARY_FETCH_RECEIPTS.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2))
