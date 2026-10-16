"""Authenticate reused primary bodies without importing prior research verdicts."""
from pathlib import Path
import datetime, hashlib, json, shutil, subprocess
A=Path(__file__).resolve().parent;P=A.parent.parent
out=A/'root_primary_sources_private';out.mkdir(exist_ok=True)
sources=[('finster2011','https://arxiv.org/pdf/1005.4588v3','e24cc72f85e68d4654a05083ea7f222f41e20fcc721ed6d3e2eb156a791df030'),('boulanger2024','https://www.numdam.org/item/10.5802/ahl.211.pdf','5874aafc30ef40dd179cb7a785861e330140a8d9a775236563dd099cacbc8b03')]
rows=[]
for name,url,expected in sources:
 src=P/'audits/pr152_5000006/root_primary_sources'/(name+'.pdf');dst=out/(name+'.pdf');b=src.read_bytes();actual=hashlib.sha256(b).hexdigest()
 if actual!=expected:raise RuntimeError('Primary source body identity drift '+name)
 if dst.exists():raise RuntimeError('Refuse replacing existing source body '+str(dst))
 shutil.copyfile(src,dst);dst.chmod(0o444)
 args=['/opt/homebrew/bin/pdftotext','-layout',str(dst),str(out/(name+'.layout.txt'))]
 result=subprocess.run(args,capture_output=True,text=True)
 if result.returncode:raise RuntimeError(result.stderr)
 rows.append({'title_key':name,'url':url,'body_bytes':len(b),'SHA256':actual,'custody':'Reused existing local primary PDF after complete body hash authentication; no fresh PDF download claimed; public primary landing page independently browsed 2026-10-15. No prior research verdict copied.','source_local':str(src),'destination_private':str(dst),'extraction_argv':args,'extraction_exit':result.returncode})
receipt={'UTC':datetime.datetime.now(datetime.UTC).isoformat(),'sources':rows,'read_depth':'Body acquisition only; later source assessment records exact pages actually read.','publish_original_primary_bodies':False}
(A/'ROOT_PRIMARY_SOURCE_CUSTODY_02.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt))
