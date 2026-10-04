#!/usr/bin/env python3
"""Render/extract the hash-bound final PDF; no TeX compilation or PDF mutation."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess

here=Path(__file__).resolve().parent
pdf=here/'private/frozen/common_tangent_nullness.pdf'
out=here/'private/final_pdf';out.mkdir(exist_ok=False)
sha=lambda b:hashlib.sha256(b).hexdigest()
want='80b3fc3e8cb470a22a1226b960467de9e67dd8c3ccf054b42133d9ba0ce9d327'
if sha(pdf.read_bytes())!=want:raise RuntimeError('Final PDF identity mismatch')
commands=[('pdfinfo',['/opt/homebrew/bin/pdfinfo',str(pdf)]),
 ('pdftotext',['/opt/homebrew/bin/pdftotext','-layout',str(pdf),str(out/'paper.txt')]),
 ('render',['/opt/homebrew/bin/pdftoppm','-r','145','-png',str(pdf),str(out/'page')])]
records=[]
for name,argv in commands:
    cap=here/'pdf_actual_captures'/name;cap.mkdir(parents=True,exist_ok=False)
    source=Path(__file__).read_bytes();(cap/'PRELAUNCH_SOURCE.py').write_bytes(source)
    start=datetime.datetime.now(datetime.timezone.utc).isoformat()
    p=subprocess.Popen(argv,cwd=here,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    stdout,stderr=p.communicate()
    (cap/'stdout.bin').write_bytes(stdout);(cap/'stderr.bin').write_bytes(stderr)
    record={'argv':argv,'controller_pid':os.getpid(),'actual_child_pid':p.pid,'start_utc':start,'end_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'exit_code':p.returncode,'input_pdf_sha256':want,'checker_source_sha256':sha(source),'stdout_sha256':sha(stdout),'stderr_sha256':sha(stderr),'stdout_bytes':len(stdout),'stderr_bytes':len(stderr)}
    (cap/'CAPTURE.json').write_text(json.dumps(record,indent=2)+'\n');records.append(record)
    if p.returncode:raise RuntimeError(name+' failed')
pages=sorted(out.glob('page-*.png'))
if len(pages)!=8:raise RuntimeError('Expected 8 rendered pages')
receipt={'pdf_sha256':want,'rendered_pages':[{'path':str(p),'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in pages],'text_sha256':sha((out/'paper.txt').read_bytes()),'actual_commands':records,'visual_inspection_claimed_at_render_time':False}
(here/'PDF_RENDER_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
print('Final fixed PDF rendered into 8 PNG pages; visual inspection remains separate.')
