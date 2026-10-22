#!/usr/bin/env python3
"""Assemble the publication kit from explicit own-work files only."""
from pathlib import Path
import hashlib,json,shutil,zipfile,datetime
r=Path(__file__).resolve().parent.parent
pub=r/'publication'
kit=pub/'kit'
if kit.exists():
    shutil.rmtree(kit)  # this script's generated kit, never research sources
kit.mkdir()
copy={
 'paper.pdf':r/'preprint/output/pdf/main.pdf',
 'main.tex':r/'preprint/main.tex',
 'exact_constructions.py':r/'verification/exact_constructions.py',
 'exact_constructions_result.json':r/'verification/exact_constructions_result.json',
 'README.md':pub/'README.md',
 'LICENSE.txt':pub/'LICENSE.txt',
 'source_manifest.json':r.parent.parent/'sources/manifest.json',
 'audits/initial_review.md':r/'review_initial.md',
 'audits/fresh_proof01.md':r/'reviews/fresh_proof01.md',
 'audits/priority_audit.md':r/'priority_independent.md',
 'audits/fresh_priority01.md':r/'reviews/fresh_priority01.md',
 'audits/primary_left_germ_evidence.md':r/'primary_left_germ_evidence.md',
 'audits/user_link_comparison.md':r/'user_link_comparison.md',
}
for src in sorted((r/'reviews').glob('final_package*.md')):
    copy['audits/'+src.name]=src
for name,src in copy.items():
    dst=kit/name;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dst)
files=[{'path':n,'bytes':(kit/n).stat().st_size,'sha256':hashlib.sha256((kit/n).read_bytes()).hexdigest()} for n in sorted(copy)]
(kit/'MANIFEST.json').write_text(json.dumps({'version':'1.0.0','files':files},indent=2)+'\n')
archive=pub/'source-and-verification.zip'
with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for p in sorted(kit.rglob('*')):
        if p.is_file():
            zi=zipfile.ZipInfo('kourovka-21-149/'+p.relative_to(kit).as_posix(),date_time=(2026,10,17,0,0,0))
            zi.compress_type=zipfile.ZIP_DEFLATED;zi.external_attr=0o100644<<16
            z.writestr(zi,p.read_bytes())
shutil.copyfile(kit/'paper.pdf',pub/'paper.pdf')
receipt={'generated_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'paper_sha256':hashlib.sha256((pub/'paper.pdf').read_bytes()).hexdigest(),'tex_sha256':hashlib.sha256((kit/'main.tex').read_bytes()).hexdigest(),'archive_sha256':hashlib.sha256(archive.read_bytes()).hexdigest(),'archive_bytes':archive.stat().st_size,'files':len(files)+1}
(pub/'package_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
