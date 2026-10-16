#!/usr/bin/env python3
"""Explicit authored-file allowlist; no raw sources or mutable upload receipts."""
import hashlib,json,pathlib,shutil,zipfile
P=pathlib.Path(__file__).resolve().parent
A=P.parent
WORK=P/'tmp'/'packet'
if WORK.exists():shutil.rmtree(WORK)
WORK.mkdir(parents=True)
def copy(src,name):
    target=WORK/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,target)
for name in ['low_exponent_supersolvability.pdf','low_exponent_supersolvability.tex',
             'verify_package.py','requirements.txt','CURRENT_PRIORITY_AND_STATUS.md']:
    copy(P/name,name)
copy(P/'PACKAGE_README.md','README.md')
candidate=A/'native/unsolved_math_prioritization/attempts/30004609'
doc=json.loads((candidate/'PUBLICATION_MANIFEST.json').read_text())
for name in [e['path'] for e in doc['files']]+['PUBLICATION_MANIFEST.json']:
    copy(candidate/name,'candidate/'+name)
for family in ['incidence_01','algebra_01','priority_01']:
    source=A/'reviews'/family
    for f in sorted(source.iterdir()):
        if f.is_file() and f.suffix in {'.md','.json','.py'}:copy(f,'reviews/'+family+'/'+f.name)
for name in ['PR_PUBLIC_CHRONOLOGY.json','REPOSITORY_PUBLIC_VISIBILITY.json','PROOF_COMMIT_CHRONOLOGY.txt',
             'ROOT_ORIGINAL_REPLAY.json','ROOT_INCIDENCE_REPLAY.json','ROOT_INCIDENCE_NONFANO_REPLAY.json',
             'ROOT_ALGEBRA_REPLAY.json','ROOT_REPRODUCTION_ENVIRONMENT.json','MATH_GATE_ACCEPTANCE.json',
             'PRIORITY_GATE_ACCEPTANCE.json']:
    copy(A/name,'chronology_and_reproduction/'+name)
entries=[]
for f in sorted(WORK.rglob('*')):
    if f.is_file():
        data=f.read_bytes();entries.append({'path':f.relative_to(WORK).as_posix(),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
manifest={'schema':1,'file_count':len(entries),'files':entries,'raw_third_party_fulltexts_included':False}
(WORK/'PACKAGE_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
out=P/'low_exponent_verification.zip'
with zipfile.ZipFile(out,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for f in sorted(WORK.rglob('*')):
        if f.is_file():
            info=zipfile.ZipInfo(f.relative_to(WORK).as_posix(),date_time=(2026,10,13,0,0,0))
            info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16
            z.writestr(info,f.read_bytes())
receipt={'files':len(entries)+1,'zip_bytes':out.stat().st_size,'zip_sha256':hashlib.sha256(out.read_bytes()).hexdigest(),
         'pdf_sha256':hashlib.sha256((P/'low_exponent_supersolvability.pdf').read_bytes()).hexdigest()}
(P/'PACKAGE_BUILD_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
