from pathlib import Path
from datetime import datetime,timezone
import subprocess,os,json,hashlib
base=Path(__file__).resolve().parent
pdf=base.parent/'publication_package_v1'/'integer_endpoint_discontinuity.pdf'
outdir=base/'pdf_review';outdir.mkdir(exist_ok=False)
def utc():return datetime.now(timezone.utc).isoformat()
def pin(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
pre={'operator_pid':os.getpid(),'start_utc':utc(),'argv':['/opt/homebrew/bin/pdftoppm','-r','90','-png',str(pdf),str(outdir/'page')],'cwd':str(base),'input_pdf':pin(pdf.read_bytes()),'prelaunch_operator':pin(Path(__file__).read_bytes())}
(base/'PDF_RENDER_PRELAUNCH.json').write_text(json.dumps(pre,indent=2)+'\n')
p=subprocess.Popen(pre['argv'],cwd=base,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
out,err=p.communicate(timeout=60)
(base/'pdf_render.stdout.bin').write_bytes(out);(base/'pdf_render.stderr.bin').write_bytes(err)
pages=sorted(outdir.glob('page-*.png'))
cap=dict(pre,child_pid=p.pid,end_utc=utc(),exit_code=p.returncode,stdout=pin(out),stderr=pin(err),pages={q.name:pin(q.read_bytes()) for q in pages},actual_execution=True)
(base/'PDF_RENDER_CAPTURE.json').write_text(json.dumps(cap,indent=2)+'\n')
print(json.dumps(cap,indent=2));assert p.returncode==0 and len(pages)==6
