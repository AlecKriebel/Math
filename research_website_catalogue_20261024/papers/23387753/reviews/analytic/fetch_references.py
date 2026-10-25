from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime,timezone
import subprocess,hashlib,json
from pypdf import PdfReader
r=Path(__file__).resolve().parent;c=r/'.reference-cache';c.mkdir(exist_ok=True)
refs=[('timar-v1','https://arxiv.org/pdf/1805.10690v1'),('bhs-v1','https://arxiv.org/pdf/math/9906002v1'),('bt-v1','https://arxiv.org/pdf/1505.06069v1'),('hm-published','https://projecteuclid.org/journals/electronic-communications-in-probability/volume-14/issue-none/Some-two-dimensional-finite-energy-percolation-processes/10.1214/ECP.v14-1446.pdf'),('pemantle-v1','https://arxiv.org/pdf/math/0404043v1'),('hm-published-mirror','https://www.maths.tcd.ie/EMIS/journals/EJP-ECP/article/download/1446/1446-4872-1-PB.pdf')]
def get(item):
 n,u=item;p=c/(n+'.pdf')
 try:
  done=subprocess.run(['curl','-L','--max-time','30','--fail','--silent','--show-error',u,'-o',str(p)],capture_output=True,text=True)
  if done.returncode:raise ValueError(done.stderr)
  data=p.read_bytes()
  if data[:4]!=b'%PDF':raise ValueError('Not PDF')
  reader=PdfReader(p);p.with_suffix('.txt').write_text('\n\n'.join(f'PAGE {i+1}\n'+(pg.extract_text() or '') for i,pg in enumerate(reader.pages)))
  return {'name':n,'url':u,'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data),'pages':len(reader.pages),'status':'downloaded','timestamp_utc':datetime.now(timezone.utc).isoformat()}
 except Exception as e:return {'name':n,'url':u,'status':'failed','error':str(e)}
if __name__=='__main__':
 results=list(ThreadPoolExecutor(max_workers=5).map(get,refs));(r/'reference_acquisition_replay.json').write_text(json.dumps(results,indent=2)+'\n');print(json.dumps(results,indent=2))
