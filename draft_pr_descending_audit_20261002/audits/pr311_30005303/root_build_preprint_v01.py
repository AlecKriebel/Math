"""Produce and render the current standalone manuscript with actual native receipts."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,subprocess,shutil
A=Path(__file__).resolve().parent;P=A/'preprint_v01';D=A/'preprint_build_private_v01';D.mkdir(exist_ok=False)
O=P/'output/pdf';O.mkdir(parents=True,exist_ok=True)
sha=lambda b:hashlib.sha256(b).hexdigest();utc=lambda:datetime.now(timezone.utc).isoformat()
jobs=[]
def run(label,args):
 j=dict(argv=args,cwd=str(P),started_utc=utc(),program_sha256=sha(Path(__file__).read_bytes()))
 (D/(label+'_spec.json')).write_text(json.dumps(j,indent=2)+'\n')
 r=subprocess.run(args,cwd=P,capture_output=True)
 for k,b in [('stdout',r.stdout),('stderr',r.stderr)]: (D/(label+'.'+k)).write_bytes(b)
 j.update(ended_utc=utc(),exit_code=r.returncode,stdout_bytes=len(r.stdout),stderr_bytes=len(r.stderr),stdout_sha256=sha(r.stdout),stderr_sha256=sha(r.stderr))
 (D/(label+'_execution.json')).write_text(json.dumps(j,indent=2)+'\n');jobs.append(j)
 assert r.returncode==0
 return r
source=P/'mtp2_edge_closure.tex';source_sha=sha(source.read_bytes())
run('compile',['/opt/homebrew/bin/tectonic','--keep-logs','--outdir',str(D),str(source)])
pdf=D/'mtp2_edge_closure.pdf';shutil.copyfile(pdf,O/pdf.name)
info=run('pdfinfo',['/opt/homebrew/bin/pdfinfo',str(O/pdf.name)])
text=D/'manuscript.txt';run('extract',['/opt/homebrew/bin/pdftotext','-layout',str(O/pdf.name),str(text)])
run('render',['/opt/homebrew/bin/pdftoppm','-r','110','-png',str(O/pdf.name),str(D/'page')])
log=(D/'mtp2_edge_closure.log').read_text()
assert 'Undefined control sequence' not in log and 'undefined references' not in log and 'undefined citations' not in log
assert sha(source.read_bytes())==source_sha
pages=sorted(D.glob('page-*.png'))
j=dict(actual_utc=utc(),status='BUILT_RENDERED_NOT_YET_VISUALLY_APPROVED',source_sha256=source_sha,
 pdf=dict(path=str(O/pdf.name),bytes=pdf.stat().st_size,sha256=sha(pdf.read_bytes())),
 rendered_pages=[dict(path=str(p),sha256=sha(p.read_bytes())) for p in pages],
 native_jobs=jobs,latex_layout_warnings=[l for l in log.splitlines() if 'Overfull' in l or 'Underfull' in l],
 desktop_compiler='Previous purpose-built compile tool returned success for this same source; this native build exports the submission PDF.',
 manuscript_pending_adversarial_review=True)
out=P/'BUILD_RECEIPT.json';assert not out.exists();out.write_text(json.dumps(j,indent=2)+'\n');print(json.dumps(j,indent=2))
