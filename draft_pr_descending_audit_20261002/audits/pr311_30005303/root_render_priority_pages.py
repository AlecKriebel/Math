"""Render decisive primary pages for a subsequent root visual read."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,subprocess
A=Path(__file__).resolve().parent;D=A/'priority_sources_private/decisive_render001';D.mkdir(exist_ok=False)
sha=lambda b:hashlib.sha256(b).hexdigest();utc=lambda:datetime.now(timezone.utc).isoformat()
jobs=[('GL415','native_retrieval003/GL2016/GL2016.pdf',11),('GL416','native_retrieval003/GL2016/GL2016.pdf',12),
      ('GL417','native_retrieval003/GL2016/GL2016.pdf',13),('KS13','native_retrieval002/KS2024v1/KS2024v1.pdf',13),
      ('KS7','native_retrieval002/KS2024v1/KS2024v1.pdf',7),('KZ151','native_retrieval002/KZ2004/KZ2004.pdf',5),
      ('GMS1480','native_retrieval001/GMS2006/GMS2006.pdf',18)]
receipts=[]
for name,rel,page in jobs:
    p=A/'priority_sources_private'/rel;args=['/opt/homebrew/bin/pdftoppm','-f',str(page),'-l',str(page),'-singlefile','-scale-to','1800','-png',str(p),str(D/name)]
    j=dict(argv=args,cwd=str(A),started_utc=utc(),source_sha256=sha(p.read_bytes()),operator_sha256=sha(Path(__file__).read_bytes()))
    (D/(name+'_preexecution.json')).write_text(json.dumps(j,indent=2)+'\n');r=subprocess.run(args,cwd=A,capture_output=True)
    for k,b in [('stdout',r.stdout),('stderr',r.stderr)]: (D/(name+'.'+k)).write_bytes(b)
    j.update(ended_utc=utc(),exit_code=r.returncode,stdout_sha256=sha(r.stdout),stderr_sha256=sha(r.stderr))
    assert r.returncode==0
    image=D/(name+'.png');j.update(image_path=str(image),image_sha256=sha(image.read_bytes()))
    receipts.append(j)
j=dict(actual_utc=utc(),status='RENDERED_NOT_YET_VISUALLY_READ',renders=receipts)
p=A/'ROOT_PRIORITY_PAGE_RENDERS.json';assert not p.exists();p.write_text(json.dumps(j,indent=2)+'\n');print(json.dumps(j,indent=2))
