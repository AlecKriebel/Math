"""Fetch primary PDFs privately and distinguish exact historical bindings."""
from pathlib import Path
import concurrent.futures,datetime,hashlib,json,subprocess,urllib.request
A=Path(__file__).resolve().parent;S=A/'snapshot/problems/30004322_arrangement_seshadri';D=A/'root_raw_sources';D.mkdir(exist_ok=True)
entries=json.loads((S/'SOURCE_MANIFEST.json').read_text())['files']+json.loads((S/'SOURCE_ADDITION_FINAL.json').read_text())['files']
urls={'owr2019-53.pdf':'https://ems.press/content/serial-article-files/46833','pokora2017.pdf':'https://arxiv.org/pdf/1711.09364v3','curve-config.pdf':'https://www.cmi.ac.in/~krishna/sc-curve-config.pdf','hanumanthu-harbourne2021.pdf':'https://www.cmi.ac.in/~krishna/supersolvable-line-arrangements.pdf','janasz-pokora2020.pdf':'https://aimspress.com/aimspress-data/era/2020/2/PDF/1935-9179_2020_2_795.pdf'}
def fetch(item):
 name,url=item;r={'name':name,'url':url,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Math independent audit'}),timeout=45) as response:b=response.read();r['final_url']=response.url
  assert b.startswith(b'%PDF'),name;(D/name).write_bytes(b)
  e=next(x for x in entries if x['path'].endswith('/'+name));r.update(bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),historical_binding_exact=(len(b)==e['bytes'] and hashlib.sha256(b).hexdigest()==e['sha256']))
  z=subprocess.run(['pdftotext','-layout',str(D/name),str(D/(name+'.txt'))],capture_output=True);assert z.returncode==0,z.stderr.decode();r['extracted']=True
 except Exception as error:r['error']=repr(error)
 return r
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:results=list(pool.map(fetch,urls.items()))
out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'results':results,'fetched_primary_PDFs':sum('error' not in x for x in results),'exact_PDF_bindings':sum(x.get('historical_binding_exact',False) for x in results),'historical_processed_PNG_not_reproduced':1,'public_wrapper_raw_sources':0,'semantic_read_and_visual_inspection_pending':True,'root_candidate_read_before_fresh_source_fetch':True}
(A/'root_primary_receipt.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
