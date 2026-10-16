from pathlib import Path
from datetime import datetime,timezone
from pypdf import PdfReader
import hashlib,json,subprocess
A=Path(__file__).resolve().parent;D=A/'root_sources_private/supplement001'
D.mkdir(parents=True,exist_ok=False)
sha=lambda b:hashlib.sha256(b).hexdigest()
rows=[]
for name,p,indices,url in [
    ('fisher195',A/'root_sources_private/fisher001/fisher2001.pdf',[26],'https://ems.press/content/serial-article-files/31488'),
    ('sutherland5',A/'division_polynomial/private_input_evidence/sutherland2023_lecture5.pdf',list(range(9,14)),'https://math.mit.edu/classes/18.783/2023/LectureNotes5.pdf'),
    ('sutherland23',A/'arithmetic/sutherland2023_lecture23.pdf',[11,12,13],'https://math.mit.edu/classes/18.783/2023/LectureNotes23.pdf')]:
    reader=PdfReader(p);texts=[]
    for i in indices:
        t=reader.pages[i].extract_text();(D/f'{name}_physical{i+1}.txt').write_text(t+'\n');texts.append(t)
    if name=='fisher195':print('Fisher printed195, physical27:\n'+texts[0])
    rows.append({'name':name,'PDF_path':str(p.relative_to(A)),'PDF_bytes':p.stat().st_size,'PDF_sha256':sha(p.read_bytes()),
        'official_URL':url,'physical_pages': [i+1 for i in indices],
        'reading_scope':'Fisher195 is read from this native full extraction. MIT5 sections5.5-5.6 and MIT23 pages12-14 were already completely read from their full native pdftotext records; this independently binds their PDF and selected page texts. No complete-book reading or independent proof of every standard theorem is asserted.'})
args=['pdftoppm','-f','27','-l','27','-scale-to','1800','-png',str(A/'root_sources_private/fisher001/fisher2001.pdf'),str(D/'fisher195')]
start=datetime.now(timezone.utc).isoformat();r=subprocess.run(args,capture_output=True)
for k,b in [('stdout',r.stdout),('stderr',r.stderr)]: (D/(k+'.bin')).write_bytes(b)
native={'argv':args,'started_utc':start,'ended_utc':datetime.now(timezone.utc).isoformat(),'exit_code':r.returncode,'stdout_sha256':sha(r.stdout),'stderr_sha256':sha(r.stderr)}
(D/'render.json').write_text(json.dumps(native,indent=2)+'\n');assert r.returncode==0
j={'utc':datetime.now(timezone.utc).isoformat(),'sources':rows,'render':native,'public_primary_redistribution':False}
(A/'ROOT_PRIMARY_SUPPLEMENT_CAPTURE.json').write_text(json.dumps(j,indent=2)+'\n')
print(json.dumps(j,indent=2))
