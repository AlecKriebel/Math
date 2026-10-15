"""Native custody for ROOT verification of the classical nonconstancy corollary."""
from pathlib import Path
from datetime import datetime,timezone
import subprocess,hashlib,json
A=Path(__file__).resolve().parent;D=A/'root_classical_nonconstancy_private';D.mkdir(exist_ok=False)
utc=lambda:datetime.now(timezone.utc).isoformat()
sha=lambda b:hashlib.sha256(b).hexdigest()
def run(label,args):
 j={'argv':args,'cwd':str(D),'started_utc':utc()};(D/(label+'.spec.json')).write_text(json.dumps(j,indent=2)+'\n')
 r=subprocess.run(args,cwd=D,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 for k,b in [('stdout',r.stdout),('stderr',r.stderr)]:
  (D/(label+'.'+k+'.bin')).write_bytes(b);j[k]={'bytes':len(b),'sha256':sha(b)}
 j.update(ended_utc=utc(),exit_code=r.returncode);(D/(label+'.execution.json')).write_text(json.dumps(j,indent=2)+'\n')
 assert r.returncode==0,(label,r.returncode)
sources={}
for name,url,expected,page in [('fierobe','https://arxiv.org/pdf/1807.11903v5','002006227b9e8d361e5f9a4d7c48148c718e18acce98ce55a2c6e2584617d3f1',9),('querret','https://www.numdam.org/item/AMPA_1823-1824__14__280_0.pdf','66d10fc03b3559a93241f519beabb353c269d148680a02af585216fc0b798560',6)]:
 p=D/(name+'.pdf');run(name+'_fetch',['/usr/bin/curl','-q','--fail','--location','--max-time','60','--output',str(p),url])
 b=p.read_bytes();assert b.startswith(b'%PDF-') and sha(b)==expected
 t=D/(name+'.txt');run(name+'_extract',['/opt/homebrew/bin/pdftotext','-layout',str(p),str(t)])
 run(name+'_render',['/opt/homebrew/bin/pdftoppm','-f',str(page),'-l',str(page),'-scale-to','1800','-png','-singlefile',str(p),str(D/(name+'_relevant'))])
 sources[name]={'url':url,'pdf_bytes':len(b),'pdf_sha256':sha(b),'text_bytes':t.stat().st_size,'text_sha256':sha(t.read_bytes()),'rendered_pdf_page':page}
j={'utc':utc(),'status':'PASS_EXACT_CLASSICAL_PRIMARY_ACQUISITION_CONTENT_ADJUDICATION_PENDING','sources':sources,'priority_claim':'No older explicit focal-ratio nonconstancy claim inferred from source acquisition. The signed-area formula and circumcenter lemma require an explicit root corollary/hypothesis check.'}
(A/'ROOT_CLASSICAL_NONCONSTANCY_ACQUISITION.json').write_text(json.dumps(j,indent=2)+'\n');print(json.dumps(j,indent=2))
