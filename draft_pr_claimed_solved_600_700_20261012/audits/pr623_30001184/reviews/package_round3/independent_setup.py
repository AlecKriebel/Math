from pathlib import Path
import hashlib,json,datetime,zipfile,urllib.request
R=Path(__file__).resolve().parent
A=R.parent.parent
S=A/'publication'
files=[*S.glob('*'),A/'prepare_integration.py',A/'record_tracker.py',A/'PACKAGE_ROUND2_REPAIRS.json',A/'INTEGRATION_HELPER_NOTES.md',A/'INTEGRATION_HELPER_CHECKS.json']
files += [p for p in (A/'native').rglob('*') if p.is_file()]
report={str(p.relative_to(A)):{'size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in files if p.is_file()}
(R/'INPUT_SHA256.json').write_text(json.dumps(report,indent=2)+'\n')
(R/'RESEARCH_LOG.md').write_text('# Round 3 independent research log\n\n'+datetime.datetime.now(datetime.UTC).isoformat()+' — 10%: Read applicable root and queue instructions; snapshotted final publication, helper and native bytes. Mathematical derivation begun before earlier package review conclusions. No Git/index/live mutations authorized or performed.\n')
with zipfile.ZipFile(S/'gns_verification.zip') as z:
 names=z.namelist()
 if len(names)!=len(set(names)) or any(n.startswith('/') or '..' in Path(n).parts for n in names): raise ValueError('unsafe ZIP')
 z.extractall(R/'tmp/extracted')
 report={'count':len(names),'manifest':json.loads(z.read('PACKAGE_MANIFEST.json')),'names':names,'compressed_total':sum(i.compress_size for i in z.infolist()),'uncompressed_total':sum(i.file_size for i in z.infolist())}
 (R/'ARCHIVE_INSPECTION.json').write_text(json.dumps(report,indent=2)+'\n')
for label,url in [('BFH_v2','https://arxiv.org/pdf/2010.00279v2'),('DMB_v3','https://arxiv.org/pdf/1503.01010v3'),('Shalit_Skeide_v3','https://arxiv.org/pdf/2003.05166v3'),('vom_Ende_v3','https://arxiv.org/pdf/2211.08351v3'),('Skeide_Sumesh_v2','https://arxiv.org/pdf/1210.7491v2')]:
 p=R/'tmp/private_sources'/f'{label}.pdf'
 with urllib.request.urlopen(url,timeout=45) as q: p.write_bytes(q.read())
 print(label,p.stat().st_size,hashlib.sha256(p.read_bytes()).hexdigest())
