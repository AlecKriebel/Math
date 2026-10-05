"""Fresh primary follow-up downloads; retain actual streams, without scientific verdict."""
from pathlib import Path
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor
import hashlib,json,subprocess
A=Path(__file__).resolve().parent;D=A/'priority_sources_private/native_retrieval002'
D.mkdir(parents=True,exist_ok=False)
sha=lambda b:hashlib.sha256(b).hexdigest();utc=lambda:datetime.now(timezone.utc).isoformat()
jobs=[('KS2024v1','https://arxiv.org/pdf/2411.03139v1'),('KS_current','https://arxiv.org/pdf/2411.03139'),('KZ2004','https://www.robots.ox.ac.uk/~cvrg/trinity2005/kolmogorov_zabih_pami04.pdf')]
def run(F,label,args):
    j=dict(argv=args,cwd=str(A),started_utc=utc(),program_sha256=sha(Path(__file__).read_bytes()))
    (F/(label+'_spec.json')).write_text(json.dumps(j,indent=2)+'\n')
    r=subprocess.run(args,cwd=A,capture_output=True)
    for k,b in [('stdout',r.stdout),('stderr',r.stderr)]: (F/(label+'.'+k)).write_bytes(b)
    j.update(ended_utc=utc(),exit_code=r.returncode,stdout_bytes=len(r.stdout),stderr_bytes=len(r.stderr),stdout_sha256=sha(r.stdout),stderr_sha256=sha(r.stderr))
    (F/(label+'_execution.json')).write_text(json.dumps(j,indent=2)+'\n');return r,j
def fetch(job):
    name,url=job;F=D/name;F.mkdir()
    r,j=run(F,'fetch',['/usr/bin/curl','--fail','--silent','--show-error','--location','--max-time','45',url]);result=dict(source=name,url=url,fetch=j,read=False)
    if r.returncode or not r.stdout.startswith(b'%PDF-'): result['status']='FETCH_FAILED_OR_NON_PDF';return result
    p=F/(name+'.pdf');p.write_bytes(r.stdout);result.update(status='RETRIEVED_NOT_YET_READ',bytes=len(r.stdout),sha256=sha(r.stdout))
    for label,args in [('info',['/opt/homebrew/bin/pdfinfo',str(p)]),('extract',['/opt/homebrew/bin/pdftotext','-layout',str(p),str(F/(name+'.txt'))])]:
        q,e=run(F,label,args);result[label]=e
        if q.returncode:result['status']='EXTRACTION_FAILED';return result
    result['text_sha256']=sha((F/(name+'.txt')).read_bytes());return result
with ThreadPoolExecutor(max_workers=3) as pool: results=list(pool.map(fetch,jobs))
j=dict(actual_utc=utc(),status='RETRIEVAL_ONLY_NO_PRIORITY_VERDICT',sources=results)
p=A/'ROOT_PRIORITY_FOLLOWUP_RETRIEVAL.json';assert not p.exists();p.write_text(json.dumps(j,indent=2)+'\n');print(json.dumps(j,indent=2))
