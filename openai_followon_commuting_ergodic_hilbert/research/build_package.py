#!/usr/bin/env python3
"""Build deterministic deposit archives from an explicit owned-file allowlist."""
from pathlib import Path
import hashlib,json,shutil,zipfile
ROOT=Path(__file__).resolve().parents[1]
KIT=ROOT/'publication/upload-kit'
KIT.mkdir(parents=True,exist_ok=True)
def archive(name,entries):
 with zipfile.ZipFile(KIT/name,'w',compression=zipfile.ZIP_DEFLATED) as z:
  for source,target in entries:
   info=zipfile.ZipInfo(target,(2026,10,6,22,0,0))
   info.compress_type=zipfile.ZIP_DEFLATED
   info.external_attr=0o644<<16
   z.writestr(info,(ROOT/source).read_bytes())
source=[('main.tex','main.tex'),('README.md','README.md'),('research/PRIORITY_REFERENCES.bib','references.bib'),('research/restriction_geometry_check.py','restriction_geometry_check.py'),('reviews/frequency_audit_computations.py','frequency_audit_computations.py'),('sources/SOURCE_HASHES.json','SOURCE_HASHES.json')]
supplement=['THEOREM_LEDGER.md','DEPENDENCY_LEDGER.md','APPROACH_TABLE.md','research/ROOT_AUDIT.md','research/restriction_independent.md','research/restriction_geometry_check.py','research/restriction_geometry_check_result.json','research/PRIORITY_AUDIT.md','research/PRIORITY_REFERENCES.bib','research/PRIORITY_EVIDENCE.json','reviews/upstream_energy_audit.md','reviews/upstream_frequency_audit.md','reviews/frequency_audit_computations.py','reviews/frequency_audit_computations.json','sources/SOURCE_HASHES.json','README.md']
archive('source.zip',source)
archive('verification-supplement.zip',[(p,p) for p in supplement])
shutil.copyfile(ROOT/'publication/paper.pdf',KIT/'paper.pdf')
shutil.copyfile(ROOT/'README.md',KIT/'README.md')
files={p.name:{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'md5':hashlib.md5(p.read_bytes()).hexdigest()} for p in sorted(KIT.iterdir()) if p.is_file()}
(ROOT/'receipts/PAYLOAD_HASHES.json').write_text(json.dumps(files,indent=2)+'\n')
print(json.dumps(files,indent=2))
