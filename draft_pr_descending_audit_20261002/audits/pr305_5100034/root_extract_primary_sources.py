"""Retain native PDF extractions/renders; record content observations separately."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib,json,subprocess
A=Path(__file__).resolve().parent
D=A/'root_primary_extractions_private';D.mkdir(exist_ok=False)
sha=lambda b:hashlib.sha256(b).hexdigest()
utc=lambda:datetime.now(timezone.utc).isoformat()
def run(label,args):
    j={'argv':args,'cwd':str(D),'started_utc':utc()}
    (D/(label+'.preexecution.json')).write_text(json.dumps(j,indent=2)+'\n')
    r=subprocess.run(args,cwd=D,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    j.update(ended_utc=utc(),exit_code=r.returncode)
    for key,b in [('stdout',r.stdout),('stderr',r.stderr)]:
        (D/(label+'.'+key)).write_bytes(b)
        j[key]={'bytes':len(b),'sha256':sha(b)}
    (D/(label+'.execution.json')).write_text(json.dumps(j,indent=2)+'\n')
    if r.returncode:raise RuntimeError((label,r.returncode,r.stderr))
for name in ['arxiv-v11','published','stachel2022']:
    source=A/'root_sources_private'/(name+'.pdf')
    run(name+'_text',['/opt/homebrew/bin/pdftotext','-layout',str(source),str(D/(name+'.txt'))])
for name,page in [('arxiv-v11',9),('published',9),('stachel2022',13)]:
    run(name+'_render',['/opt/homebrew/bin/pdftoppm','-f',str(page),'-l',str(page),'-scale-to','1800','-png','-singlefile',str(A/'root_sources_private'/(name+'.pdf')),str(D/(name+'_target'))])
pins={str(p.relative_to(D)):{'bytes':p.stat().st_size,'sha256':sha(p.read_bytes()),'mode':format(p.stat().st_mode&0o777,'04o')} for p in sorted(D.iterdir()) if p.is_file()}
j={'utc':utc(),'status':'PASS_NATIVE_EXTRACTIONS_AND_RENDERS_ONLY_CONTENT_READING_PENDING','files':pins}
(A/'ROOT_PRIMARY_EXTRACTION_RECEIPT.json').write_text(json.dumps(j,indent=2)+'\n')
print(json.dumps(j,indent=2))
