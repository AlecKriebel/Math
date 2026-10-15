"""Record fresh command/source/output hashes without retaining primary-body extracts."""
from pathlib import Path
import datetime,hashlib,json,subprocess
R=Path(__file__).resolve().parent;A=R.parent
sources=[('Fuchs definitions',A/'root_primary_sources_private/fuchs2021.pdf','9','14'),('Fuchs conjecture',A/'root_primary_sources_private/fuchs2021.pdf','22','23'),('AAH cover and virtual midpoint',A/'root_primary_sources_private/platonic181104131v2.pdf','15','18'),('AAH 10.2.1',A/'root_primary_sources_private/platonic181104131v2.pdf','43','43'),('Troubetzkoy full v3',A/'current_literature_priority_adversary/private_sources/troub_2202.04892v3.pdf','1','5'),('Ferudun conventions',A/'current_literature_priority_adversary/private_sources/ferudun_paper_current.pdf','2','3'),('Ferudun Section7',A/'current_literature_priority_adversary/private_sources/ferudun_paper_current.pdf','23','26')]
def digest(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
rows=[]
for name,p,a,b in sources:
    argv=['/opt/homebrew/bin/pdftotext','-f',a,'-l',b,'-layout',str(p),'-'];start=datetime.datetime.now(datetime.timezone.utc).isoformat();r=subprocess.run(argv,capture_output=True)
    rows.append({'scope':name,'UTC_start':start,'UTC_end':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_argv':argv,'exit':r.returncode,'source':digest(p.read_bytes()),'stdout_not_retained':digest(r.stdout),'stderr_not_retained':digest(r.stderr),'note':'Fresh hashed reread receipt; initial primary reading occurred before FIRST_ANALYTICAL_ASSESSMENT_SEAL. No source extraction saved.'})
    if r.returncode:raise ValueError(name)
for pagenum in [10,11]:
    p=A/'root_primary_sources_private/fuchs2021.pdf';argv=['/opt/homebrew/bin/pdftoppm','-f',str(pagenum),'-l',str(pagenum),'-singlefile','-scale-to','1200','-png',str(p)];start=datetime.datetime.now(datetime.timezone.utc).isoformat();r=subprocess.run(argv,capture_output=True)
    rows.append({'scope':'Fuchs complete primary figure page, personally viewed before first assessment','printed_page':492+pagenum,'actual_argv':argv,'UTC_start':start,'UTC_end':datetime.datetime.now(datetime.timezone.utc).isoformat(),'exit':r.returncode,'source':digest(p.read_bytes()),'PNG_not_retained':digest(r.stdout),'stderr_not_retained':digest(r.stderr)})
    if r.returncode:raise ValueError('Fuchs render')
(R/'SOURCE_READ_RECEIPTS.json').write_text(json.dumps({'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'runs':rows,'external_programs_executed':False,'body_extractions_retained':False},indent=2)+'\n');print('Nine source read/render receipts written; no primary extracts retained.')
