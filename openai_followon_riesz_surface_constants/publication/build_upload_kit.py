#!/usr/bin/env python3
"""Deterministic explicit-file packaging, excluding credentials and third-party source copies."""
from pathlib import Path
import hashlib,json,shutil,zipfile
ROOT=Path(__file__).resolve().parents[1]
FILES=['publication/main.tex','publication/README.md','publication/LICENSE.md','publication/abstract.txt',
 'THEOREM_LEDGER.md','DEPENDENCY_LEDGER.md','APPROACH_TABLE.md','proofs/FINITE_TRANSFER.md',
 'reproducibility/README.md','reproducibility/reproduce.py','sources/UPSTREAM_MANIFEST.json','sources/UPSTREAM_CITATIONS.md',
 'sources/classical/SOURCE_MANIFEST.json','sources/classical/README.md','sources/priority/EVIDENCE_MANIFEST.json','sources/priority/upstream_citations.bib',
 'agent_notes/upstream_main_audit.md','agent_notes/atomic_audit.md','agent_notes/formal_audit.md','agent_notes/classical_scope.md','agent_notes/priority_audit.md',
 'audit_runs/upstream_main/certificate_results/numeric_balls_results.json','audit_runs/upstream_main/certificate_results/arithmetic_bounds.json',
 'verification/atomic_checker_execution.json','verification/atomic_independent_checks.py','verification/atomic_independent_checks_result.json',
 'verification/formal_source_manifest.json','verification/formal_source_audit_results.json']
def sha(b):return hashlib.sha256(b).hexdigest()
kit=ROOT/'publication/upload-kit';kit.mkdir(exist_ok=True)
rows=[]
with zipfile.ZipFile(kit/'source-and-verification.zip','w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for name in FILES:
  q=ROOT/name;assert q.is_file() and not q.is_symlink(),name
  b=q.read_bytes();rows.append({'path':name,'bytes':len(b),'sha256':sha(b)})
  i=zipfile.ZipInfo(name,date_time=(2026,10,6,12,0,0));i.compress_type=zipfile.ZIP_DEFLATED;i.external_attr=0o100644<<16;z.writestr(i,b)
 i=zipfile.ZipInfo('PACKAGE_CONTENTS.json',date_time=(2026,10,6,12,0,0));i.compress_type=zipfile.ZIP_DEFLATED;i.external_attr=0o100644<<16
 z.writestr(i,json.dumps({'files':rows,'third_party_source_copies_included':False,'credentials_included':False},indent=2)+'\n')
shutil.copyfile(ROOT/'publication/paper.pdf',kit/'paper.pdf')
items=rows+[{'path':'publication/upload-kit/paper.pdf','bytes':(kit/'paper.pdf').stat().st_size,'sha256':sha((kit/'paper.pdf').read_bytes())}, {'path':'publication/upload-kit/source-and-verification.zip','bytes':(kit/'source-and-verification.zip').stat().st_size,'sha256':sha((kit/'source-and-verification.zip').read_bytes())}, {'path':'zenodo-deposit.json','bytes':(ROOT/'zenodo-deposit.json').stat().st_size,'sha256':sha((ROOT/'zenodo-deposit.json').read_bytes())}]
identity=sha(json.dumps(items,sort_keys=True,separators=(',',':')).encode())
(ROOT/'publication/CANDIDATE_MANIFEST.json').write_text(json.dumps({'package_identity_sha256':identity,'files':items,'archive_contents':rows},indent=2)+'\n')
print(json.dumps({'package_identity_sha256':identity,'archive_files':len(rows),'files_to_deposit':2}))
