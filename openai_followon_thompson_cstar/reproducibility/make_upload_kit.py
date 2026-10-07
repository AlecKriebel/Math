#!/usr/bin/env python3
"""Freeze original project artifacts; never bundle upstream source or caches."""
from pathlib import Path
import datetime, hashlib,json,shutil,zipfile
P=Path(__file__).resolve().parents[1]; K=P/'upload-kit';K.mkdir(exist_ok=True)
def archive(name, paths):
 with zipfile.ZipFile(K/name,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for path in sorted(paths):
   p=P/path; i=zipfile.ZipInfo(path,date_time=(2026,10,6,0,0,0));i.compress_type=zipfile.ZIP_DEFLATED;i.external_attr=0o644<<16;z.writestr(i,p.read_bytes())
shutil.copyfile(P/'paper.pdf',K/'paper.pdf')
archive('thompson-cstar-source.zip',['main.tex','PUBLICATION_README.md','reproducibility/BUILD.md','sources/upstream_citation.bib'])
support=['DEPENDENCY_LEDGER.md','THEOREM_LEDGER.md','APPROACH_TABLE.md','PUBLICATION_README.md','LICENSE_CODE.txt','upstream_finite_checks.py','upstream_finite_lean_manifest.json','reproducibility/BUILD.md','sources/SOURCE_MANIFEST.json']
support += [str(p.relative_to(P)) for p in (P/'agent_notes').iterdir() if p.is_file()]
archive('thompson-cstar-verification.zip',support)
rows=[{'path':str(p.relative_to(P)),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'md5':hashlib.md5(p.read_bytes()).hexdigest()} for p in sorted(K.iterdir()) if p.is_file()]
frozen={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'files':rows,'manifest_sha256':hashlib.sha256((P/'zenodo-deposit.json').read_bytes()).hexdigest(),'third_party_content':'No upstream papers/formalization sources are redistributed; only bibliographic metadata and hashes.'}
(P/'receipts/FROZEN_PACKAGE.json').write_text(json.dumps(frozen,indent=2)+'\n');print(json.dumps(frozen,indent=2))
