#!/usr/bin/env python3
"""Export the standalone source with the existing runtime; preserve native receipts."""
from pathlib import Path
import datetime, hashlib, json, shutil, subprocess, sys
HERE = Path(__file__).resolve().parent
A = HERE.parent
assert len(sys.argv) == 2 and sys.argv[1].isdigit()
OUT = A / 'root_preprint_private' / ('pdf_v'+sys.argv[1])
assert not OUT.exists()
OUT.mkdir(parents=True)
SOURCE = HERE / 'qss-self-duality-note.tex'
def utc(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def pin(p):
    data=p.read_bytes()
    return dict(bytes=len(data),sha256=hashlib.sha256(data).hexdigest())
before=pin(SOURCE)
def run(label,argv):
    start=utc()
    proc=subprocess.run(argv,cwd=HERE,capture_output=True)
    (OUT/(label+'.stdout')).write_bytes(proc.stdout)
    (OUT/(label+'.stderr')).write_bytes(proc.stderr)
    record=dict(argv=argv,cwd=str(HERE),start_utc=start,end_utc=utc(),exit_status=proc.returncode,
                orchestrator=pin(Path(__file__)),source_before=before,source_after=pin(SOURCE),
                stdout=pin(OUT/(label+'.stdout')),stderr=pin(OUT/(label+'.stderr')))
    (OUT/(label+'.receipt.json')).write_text(json.dumps(record,indent=2)+'\n')
    print(label,'actual exit',proc.returncode)
    print(proc.stdout.decode(errors='replace'))
    print(proc.stderr.decode(errors='replace'))
    assert proc.returncode==0 and pin(SOURCE)==before
pdf=HERE/'qss-self-duality-note.pdf'
for name in ('tectonic','pdfinfo','pdftoppm'): assert shutil.which(name),name
run('compile',[shutil.which('tectonic'),'--outdir',str(HERE),'--keep-logs',str(SOURCE)])
run('pdfinfo',[shutil.which('pdfinfo'),str(pdf)])
run('render',[shutil.which('pdftoppm'),'-scale-to','1400','-png',str(pdf),str(OUT/'page')])
result=dict(utc=utc(),status='PDF_EXPORTED_RENDERED_PENDING_VISUAL_REVIEW',source=before,pdf=pin(pdf),
            rendered_pages=[dict(name=p.name,**pin(p)) for p in sorted(OUT.glob('page-*.png'))])
(OUT/'SUMMARY.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
