"""Retrieve primary comparison papers with contemporaneous complete native captures."""
from pathlib import Path
from datetime import datetime,timezone
from concurrent.futures import ThreadPoolExecutor
import hashlib,json,shutil,subprocess
A=Path(__file__).resolve().parent;D=A/'priority_sources_private/native_retrieval001'
D.mkdir(parents=True,exist_ok=False)
sha=lambda b:hashlib.sha256(b).hexdigest();utc=lambda:datetime.now(timezone.utc).isoformat()
jobs=[('GMS2006','https://math.berkeley.edu/~bernd/AOS0092.pdf','1aa0d14f5822f7e5664180b92bb3c0f97e022d8276134ae949eaf4ceccc42441'),
      ('LUZ2021','https://par.nsf.gov/servlets/purl/10339054','8b205ebbaec009a67e2a8d47578262dbe0717a42aa3e3feff75e8527ac674705'),
      ('Fallat2017','https://arxiv.org/pdf/1510.01290','f23ef1ec315f931f9af8bc270096efa5c09081e901b2224ff75e5f9004596b3f'),
      ('KR2007','https://www.microsoft.com/en-us/research/wp-content/uploads/2007/01/PAMI07-QPBO.pdf','447685d9ff5acf753829bfd0db4c3654e70be12d59841f3bf9d3864fccb18096')]
def run(folder,label,args):
    spec=dict(argv=args,cwd=str(A),started_utc=utc(),program_sha256=sha(Path(__file__).read_bytes()))
    (folder/(label+'_spec.json')).write_text(json.dumps(spec,indent=2)+'\n')
    r=subprocess.run(args,cwd=A,capture_output=True)
    for k,b in [('stdout',r.stdout),('stderr',r.stderr)]: (folder/(label+'.'+k)).write_bytes(b)
    spec.update(ended_utc=utc(),exit_code=r.returncode,stdout_bytes=len(r.stdout),stderr_bytes=len(r.stderr),stdout_sha256=sha(r.stdout),stderr_sha256=sha(r.stderr))
    (folder/(label+'_execution.json')).write_text(json.dumps(spec,indent=2)+'\n');return r,spec
def fetch(job):
    name,url,oldhash=job;F=D/name;F.mkdir()
    r,spec=run(F,'fetch',['/usr/bin/curl','--fail','--silent','--show-error','--location','--max-time','45',url])
    result=dict(source=name,url=url,native_fetch=spec,original_author_binding_sha256=oldhash)
    if r.returncode or not r.stdout.startswith(b'%PDF-'):
        result.update(status='FETCH_FAILED_OR_NON_PDF',source_read=False);return result
    pdf=F/(name+'.pdf');pdf.write_bytes(r.stdout)
    result.update(status='PRIMARY_PDF_RETRIEVED_NOT_YET_READ',bytes=len(r.stdout),sha256=sha(r.stdout),matches_original_author_pdf=sha(r.stdout)==oldhash)
    for label,args in [('pdfinfo',[shutil.which('pdfinfo'),str(pdf)]),('extract',[shutil.which('pdftotext'),'-layout',str(pdf),str(F/(name+'.txt'))])]:
        q,e=run(F,label,args);result[label]=e
        if q.returncode:result['status']='EXTRACTION_FAILED';return result
    result['extracted_text_sha256']=sha((F/(name+'.txt')).read_bytes());return result
with ThreadPoolExecutor(max_workers=4) as pool:results=list(pool.map(fetch,jobs))
receipt=dict(utc=utc(),status='PRIMARY_SOURCE_FETCH_RESULTS_NO_PRIORITY_VERDICT',sources=results,
    source_bodies_not_read_yet=True,mathematical_percent=100,priority_percent=5,workflow_percent=35,
    copyrighted_sources_private=True,publication_ready=False)
(A/'ROOT_PRIORITY_SOURCE_RETRIEVAL.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
