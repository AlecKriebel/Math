#!/usr/bin/env python3
"""Create a separate citation-corrected distribution, preserving original bytes."""
from pathlib import Path
import difflib, hashlib,json, shutil
BASE=Path(__file__).resolve().parent
ORIGINAL=BASE.parent/'boundary_twist_11000156'
TARGET=BASE/'corrected_distribution'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def emit(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
if TARGET.exists():raise RuntimeError('refusing to replace existing corrected distribution')
shutil.copytree(ORIGINAL/'packet',TARGET/'packet')
TARGET.chmod(0o755);(TARGET/'packet').chmod(0o755)
for p in (TARGET/'packet').iterdir():p.chmod(0o644)
p=TARGET/'packet/REPORT.md';s=p.read_text()
s=s.replace('[Two-chain relation: A06 book PDF p. 132, relation (3); the obstruction is consistent with B16 Remark 4.2.]','[Two-chain relation: W06, book PDF p. 132 (displayed p. 125), relation (3), specialized to genus one; the obstruction is consistent with B16 Remark 4.2.]')
s=s.replace('- B16: R. Inanc Baykur,','- W06: Bronislaw Wajnryb, Relations in the mapping class group, in Problems on Mapping Class Groups and Related Topics, 2006. https://www.math.uchicago.edu/~farb/papers/mcgbook.pdf ; two-chain specialization of relation (3), PDF p. 132, displayed p. 125.\n- B16: R. Inanc Baykur,')
p.write_text(s)
p=TARGET/'packet/SOURCES.json';s=json.loads(p.read_text());s['inspection'].append({'source':'Wajnryb, Relations in the mapping class group, in the Farb book','locations':'PDF p. 132, displayed p. 125, relation (3), genus-one specialization','method':'independent local text inspection and public PDF source check'});emit(p,s)
patch=''.join(''.join(difflib.unified_diff((ORIGINAL/'packet'/name).read_text().splitlines(keepends=True),(TARGET/'packet'/name).read_text().splitlines(keepends=True),fromfile='a/packet/'+name,tofile='b/packet/'+name)) for name in ['REPORT.md','SOURCES.json'])
(BASE/'citation_correction.patch').write_text(patch)
m={'schema':'boundary-twist-packet-v1','files':{p.name:{'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted((TARGET/'packet').iterdir())}}
emit(TARGET/'FREEZE_MANIFEST.json',m)
b=(ORIGINAL/'bootstrap.py').read_text().replace(sha(ORIGINAL/'FREEZE_MANIFEST.json'),sha(TARGET/'FREEZE_MANIFEST.json'))
(TARGET/'bootstrap.py').write_text(b)
emit(TARGET/'BOOTSTRAP_PINS.json',{'schema':'boundary-twist-bootstrap-pins-v1','manifest_sha256':sha(TARGET/'FREEZE_MANIFEST.json'),'verifier_sha256':sha(TARGET/'packet/verify.py'),'bootstrap_sha256':sha(TARGET/'bootstrap.py'),'trust':'Retain this record outside the packet; hashes are integrity pins, not signatures.'})
for p in TARGET.rglob('*'):
 p.chmod(0o555 if p.is_dir() else 0o444)
TARGET.chmod(0o555)
print(json.dumps({'correction':'citation attribution only; no mathematical or status change','files_changed':['REPORT.md','SOURCES.json'],'manifest_sha256':sha(TARGET/'FREEZE_MANIFEST.json'),'bootstrap_sha256':sha(TARGET/'bootstrap.py')}))
