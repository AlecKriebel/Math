from pathlib import Path
from datetime import datetime,timezone
import subprocess,json,hashlib
from pypdf import PdfReader
A=Path(__file__).resolve().parent;D=A/'root_sources_private/fisher001'
pdf=D/'fisher2001.pdf';reader=PdfReader(pdf);assert len(reader.pages)==33
selected=[3,4,10,11,12,13,25]
for index in selected:
    text=reader.pages[index].extract_text();(D/f'page_{index+1:02}.txt').write_text(text+'\n')
    print('Physical page'+str(index+1)+' / printed'+str(169+index)+'\n'+text+'\n')
for index in [3,10,11,12,25]:
    args=['pdftoppm','-f',str(index+1),'-l',str(index+1),'-scale-to','1600','-png',str(pdf),str(D/f'render_{index+1:02}')]
    started=datetime.now(timezone.utc).isoformat();r=subprocess.run(args,capture_output=True)
    for k,b in [('stdout',r.stdout),('stderr',r.stderr)]: (D/f'render_{index+1:02}.{k}.bin').write_bytes(b)
    j={'argv':args,'started_utc':started,'ended_utc':datetime.now(timezone.utc).isoformat(),'exit_code':r.returncode,
       'stdout_sha256':hashlib.sha256(r.stdout).hexdigest(),'stderr_sha256':hashlib.sha256(r.stderr).hexdigest()}
    (D/f'render_{index+1:02}.json').write_text(json.dumps(j,indent=2)+'\n');assert r.returncode==0
pins=[]
for p in sorted(D.glob('*')):
    if p.is_file():pins.append({'path':str(p.relative_to(A)),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
j={'utc':datetime.now(timezone.utc).isoformat(),'source':'Fisher JEMS3(2001),169-201, DOI10.1007/s100970100030',
   'read_scope':'Full operative printed172,173,179-182,194 extracted; rendered172,179-181,194 separately inspected by root after this capture. All33pages retained, unrelatedrank/Selmer sections not claimed fully read.',
   'PDF_sha256':hashlib.sha256(pdf.read_bytes()).hexdigest(),'files':pins,'public_raw_primary_redistribution':False}
(A/'ROOT_FISHER_SOURCE_CAPTURE.json').write_text(json.dumps(j,indent=2)+'\n')
