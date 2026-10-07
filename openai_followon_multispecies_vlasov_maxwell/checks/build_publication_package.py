#!/usr/bin/env python3
"""Construct an exact allowlisted publication kit; never uploads anything."""
import argparse,hashlib,json,pathlib,shutil,zipfile,datetime
R=pathlib.Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--version',required=True);a=p.parse_args()
if not a.version.replace('_','').isalnum():raise SystemExit('Invalid version')
files={
'main.tex':'publication/main.tex','references.bib':'publication/references.bib',
'README.md':'publication/README.md','REPRODUCE.md':'publication/REPRODUCE.md','LICENSE.txt':'publication/LICENSE.txt',
'DEPENDENCY_LEDGER.md':'DEPENDENCY_LEDGER.md','PRIORITY_AUDIT.md':'agent_notes/priority_primary/REPORT.md',
'PRIORITY_SEARCH_LOG.json':'agent_notes/priority_primary/SEARCH_LOG.json',
'PINNED_SOURCE.json':'sources/PINNED_SOURCE.json',
'SUPPLEMENT_PAIR_IDENTITY.md':'derivations/multispecies_derivation/PAIR_IDENTITY.md',
'SUPPLEMENT_TRANSFER_LEMMA.md':'derivations/multispecies_derivation/TRANSFER_LEMMA.md',
'SUPPLEMENT_UNIFORM_LEMMA_CHAIN.md':'agent_notes/occupation_bootstrap/UNIFORM_LEMMA_CHAIN.md',
'SUPPLEMENT_LOCAL_THEORY.md':'agent_notes/continuation_alternative/LOCAL_THEORY.md',
'exact_kernel_certificate.py':'checks/kernel_audit/exact_kernel_certificate.py',
'rational_selection_certificate.py':'checks/occupation_bootstrap/rational_selection_certificate.py',
'verify_pair_identity.py':'derivations/multispecies_derivation/verify_pair_identity.py',
'FORMAL_SCOPE_AUDIT.md':'agent_notes/formal_scope/REPORT.md',
'FORMAL_BUILD_LIMITATIONS.json':'checks/formal_scope/build_receipt.json',
'PRIMARY_REFERENCE_PROVENANCE.md':'sources/continuation_alternative/README.md'
}
packet=R/'reviews'/('package_'+a.version);packet.mkdir(exist_ok=False)
source=packet/'source-and-verification';source.mkdir()
for name,path in files.items():
 b=(R/path).read_bytes();(source/name).write_bytes(b)
checks={name:hashlib.sha256((source/name).read_bytes()).hexdigest() for name in sorted(files)}
(source/'SHA256SUMS.json').write_text(json.dumps(checks,indent=2)+'\n')
kit=R/'publication'/'upload-kit';kit.mkdir(exist_ok=True)
shutil.copyfile(R/'publication'/'main.pdf',kit/'paper.pdf')
shutil.copyfile(R/'publication'/'README.md',kit/'README.md')
with zipfile.ZipFile(kit/'source-and-verification.zip','w',zipfile.ZIP_DEFLATED) as z:
 for f in sorted(source.iterdir()):
  i=zipfile.ZipInfo('source-and-verification/'+f.name,(2026,10,6,0,0,0));i.external_attr=0o100644<<16;i.compress_type=zipfile.ZIP_DEFLATED
  z.writestr(i,f.read_bytes())
(packet/'upload-kit').mkdir()
for f in kit.iterdir():shutil.copyfile(f,packet/'upload-kit'/f.name)
shutil.copyfile(R/'zenodo-deposit.json',packet/'zenodo-deposit.json')
review_files=list((packet/'source-and-verification').iterdir())+list((packet/'upload-kit').iterdir())+[packet/'zenodo-deposit.json']
inv={str(f.relative_to(packet)):{'bytes':f.stat().st_size,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()} for f in sorted(review_files)}
receipt={'version':a.version,'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'packet_directory':str(packet),'files':inv,'third_party_cache_included':False,'publication_state':'candidate, not staged or published'}
(packet/'REVIEW_INVENTORY.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({'packet':str(packet),'files':len(inv),'pdf_sha256':hashlib.sha256((kit/'paper.pdf').read_bytes()).hexdigest(),'zip_sha256':hashlib.sha256((kit/'source-and-verification.zip').read_bytes()).hexdigest()}))
