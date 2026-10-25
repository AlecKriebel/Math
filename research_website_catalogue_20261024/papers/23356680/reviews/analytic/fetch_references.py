"""Reacquire primary references; cache binaries/text and retain a fresh hash manifest.
Run after installing pypdf. Does not touch paper sources, reports or verdicts.
"""
from pathlib import Path
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor
import hashlib,json,subprocess
from pypdf import PdfReader
root=Path(__file__).resolve().parent
cache=root/'.reference-cache';cache.mkdir(exist_ok=True)
refs=[('mvw-v1','https://arxiv.org/pdf/2503.08553v1'),('lw-enarea','https://www.mi.uni-koeln.de/~alytchak/preprints/enarea.pdf'),('ks-1993','https://intlpress.com/site/pub/files/_fulltext/journals/cag/1993/0001/0004/CAG-1993-0001-0004-a004.pdf'),('lw-enarea-arxiv-v2','https://arxiv.org/pdf/1507.02670v2'),('lw-plateau-v2','https://arxiv.org/pdf/1502.06571v2'),('owr-2025-30','https://ems.press/content/serial-article-files/52249?nt=1')]
def acquire(item):
 name,url=item;path=cache/(name+'.pdf')
 try:
  done=subprocess.run(['curl','-L','--fail','--silent','--show-error','--max-time','35',url,'-o',str(path)],capture_output=True,text=True)
  if done.returncode:raise RuntimeError(done.stderr)
  data=path.read_bytes()
  if data[:4]!=b'%PDF':raise ValueError('Not a PDF')
  reader=PdfReader(path)
  (cache/(name+'.txt')).write_text('\n\n'.join(f'---PAGE {i+1}---\n'+(p.extract_text() or '') for i,p in enumerate(reader.pages)))
  return {'name':name,'url':url,'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data),'pages':len(reader.pages),'status':'downloaded','timestamp_utc':datetime.now(timezone.utc).isoformat()}
 except Exception as e:return {'name':name,'url':url,'status':'failed','error':str(e)}
if __name__=='__main__':
 results=list(ThreadPoolExecutor(max_workers=3).map(acquire,refs))
 output=root/'reference_acquisition_replay.json'
 output.write_text(json.dumps(results,indent=2)+'\n')
 print(json.dumps(results,indent=2))
