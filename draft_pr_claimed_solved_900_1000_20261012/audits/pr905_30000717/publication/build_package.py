#!/usr/bin/env python3
"""Deterministic allowlist source/verification archive; no primary-source copies."""
import hashlib,json,shutil,zipfile
from pathlib import Path
HERE=Path(__file__).resolve().parent; AUDIT=HERE.parent
FROZEN=AUDIT/'original/unsolved_math_prioritization/attempts/30000717'; DEST=HERE/'tmp/bundle'
REVIEW_FILES={
 'proof_family':['MANIFEST.json', *json.loads((AUDIT/'reviews/proof_family/MANIFEST.json').read_text())['artifacts']],
 'computation_family':['MANIFEST.json', *json.loads((AUDIT/'reviews/computation_family/MANIFEST.json').read_text())['files']],
 'source_model_family':['SOURCE_MODEL_REPORT.md','SOURCE_HASHES.json','SOURCE_MODEL_RESULT.json','RESEARCH_LOG.md','publisher_fetch_metadata.json','related_fetch_metadata.json','catalog_inspection_metadata.json','dataset_inspection_metadata.json'],
 'priority_family':['PRIORITY_AUDIT.md','SOURCE_MANIFEST.json','QUERY_LOG.md'],
}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 if DEST.exists():shutil.rmtree(DEST)
 DEST.mkdir(parents=True); shutil.copytree(FROZEN,DEST/'original_packet')
 for name in ['note.tex','README.md','verify_package.py','requirements.txt']:shutil.copy2(HERE/name,DEST/name)
 shutil.copy2(AUDIT/'SOURCE_CORRECTION.md',DEST/'SOURCE_CORRECTION.md')
 shutil.copy2(AUDIT/'ORIGINAL_SNAPSHOT.json',DEST/'ORIGINAL_SNAPSHOT.json')
 for family,names in REVIEW_FILES.items():
  for name in names:
   source=AUDIT/'reviews'/family/name; target=DEST/'reviews'/family/name
   if family in ['proof_family','computation_family'] and name!='MANIFEST.json':
    sealed=json.loads((AUDIT/'reviews'/family/'MANIFEST.json').read_text())
    rec=sealed['artifacts' if family=='proof_family' else 'files'][name]
    if not source.is_file() or source.stat().st_size!=rec['bytes'] or sha(source)!=rec['sha256']:raise ValueError('Review seal mismatch: '+str(source))
   if not source.is_file() or source.is_symlink():raise ValueError('Missing/nonregular allowlisted member: '+str(source))
   target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source,target)
 pdf=HERE/'output/pdf/note.pdf'; files={}
 for p in sorted(DEST.rglob('*')):
  if p.is_symlink():raise ValueError('Symlink not allowed')
  if p.is_file():files[p.relative_to(DEST).as_posix()]={'bytes':p.stat().st_size,'sha256':sha(p)}
  elif not p.is_dir():raise ValueError('Special filesystem member')
 m={'problem_id':30000717,'pr_number':905,'original_pr_head':'330a544a53b9e3e01bb0ed70817a5f4a79cc6a0a','version':'1.0','files':files,'separate_pdf':{'name':'robinson-tangency-certificates-v1.0.pdf','bytes':pdf.stat().st_size,'sha256':sha(pdf)},'claim_scope':'Classical nonnegative Robinson sextic plus every epsilon>=0 is not SOS modulo full real vanishing ideal for both explicitly defined tangency-minor and literal-product ideals.','review_status':'Unrefereed; extensive AI use; no independent human or journal peer review','priority':'First priority and continued open status through2026 not asserted; see bounded priority audit','trust_boundary':'Trusted original anchors and optional externally trusted manifest; exact controls supplement universal written proof.'}
 (DEST/'PACKAGE_MANIFEST.json').write_text(json.dumps(m,indent=2)+'\n')
 archive=HERE/'robinson-tangency-source-verification-v1.0.zip'
 with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for p in sorted(DEST.rglob('*')):
   if p.is_file():
    i=zipfile.ZipInfo(p.relative_to(DEST).as_posix(),date_time=(2026,10,12,0,0,0));i.compress_type=zipfile.ZIP_DEFLATED;i.external_attr=0o100644<<16;z.writestr(i,p.read_bytes())
 receipt={'files':len(files)+1,'archive_bytes':archive.stat().st_size,'archive_sha256':sha(archive),'pdf_sha256':sha(pdf),'manifest_sha256':sha(DEST/'PACKAGE_MANIFEST.json')}
 (HERE/'PACKAGE_BUILD.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt,indent=2))
if __name__=='__main__':main()
