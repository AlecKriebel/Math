#!/usr/bin/env python3
"""Construct an exact allowlisted publication kit; never uploads anything."""
import argparse,hashlib,json,pathlib,shutil,zipfile,datetime
R=pathlib.Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--version',required=True);a=p.parse_args()
if not a.version.replace('_','').isalnum():raise SystemExit('Invalid version')
files={
'main.tex':'publication/main.tex','references.bib':'publication/references.bib',
'README.md':'publication/README.md','REPRODUCE.md':'publication/REPRODUCE.md','LICENSE.txt':'publication/LICENSE.txt',
'DEPENDENCY_LEDGER.md':'DEPENDENCY_LEDGER.md','PRIORITY_AUDIT.md':'reviews/priority_final/REPORT.md',
'PRELIMINARY_PRIORITY_AUDIT.md':'agent_notes/priority_primary/REPORT.md',
'PRIORITY_SEARCH_LOG.json':'sources/priority_final/SEARCH_LOG.json',
'PRELIMINARY_PRIORITY_SEARCH_LOG.json':'agent_notes/priority_primary/SEARCH_LOG.json',
'PINNED_SOURCE.json':'sources/PINNED_SOURCE.json',
'SUPPLEMENT_PAIR_IDENTITY.md':'derivations/multispecies_derivation/PAIR_IDENTITY.md',
'SUPPLEMENT_TRANSFER_LEMMA.md':'derivations/multispecies_derivation/TRANSFER_LEMMA.md',
'SUPPLEMENT_UNIFORM_LEMMA_CHAIN.md':'agent_notes/occupation_bootstrap/UNIFORM_LEMMA_CHAIN.md',
'SUPPLEMENT_OCCUPATION_AUDIT.md':'agent_notes/occupation_bootstrap/AUDIT.md',
'SUPPLEMENT_LOCAL_THEORY.md':'agent_notes/continuation_alternative/LOCAL_THEORY.md',
'exact_kernel_certificate.py':'checks/kernel_audit/exact_kernel_certificate.py',
'rational_selection_certificate.py':'checks/occupation_bootstrap/rational_selection_certificate.py',
'verify_pair_identity.py':'derivations/multispecies_derivation/verify_pair_identity.py',
'FORMAL_SCOPE_AUDIT.md':'agent_notes/formal_scope/REPORT.md',
'FORMAL_BUILD_LIMITATIONS.json':'checks/formal_scope/build_receipt.json',
'FORMAL_SOURCE_INVENTORY.json':'checks/formal_scope/source_inventory.json',
'FORMAL_STATIC_SCAN.json':'checks/formal_scope/static_scan.json',
'PRIMARY_REFERENCE_PROVENANCE.md':'sources/continuation_alternative/README.md',
'ORIGINAL_CONTINUATION_ATTRIBUTION.json':'receipts/original_continuation_attribution.json'
}
packet=R/'reviews'/('package_'+a.version);packet.mkdir(exist_ok=False)
source=packet/'source-and-verification';source.mkdir()
for name,path in files.items():
 b=(R/path).read_bytes()
 if name.endswith('.md'):
  txt=b.decode()
  substitutions={'PAIR_IDENTITY.md':'SUPPLEMENT_PAIR_IDENTITY.md',
   'LOCAL_THEORY.md':'SUPPLEMENT_LOCAL_THEORY.md',
   'UNIFORM_LEMMA_CHAIN.md':'SUPPLEMENT_UNIFORM_LEMMA_CHAIN.md'}
  for old,new in substitutions.items():
   if name!=new:txt=txt.replace('`'+old+'`','`'+new+'`')
  if name=='SUPPLEMENT_UNIFORM_LEMMA_CHAIN.md':txt=txt.replace('`AUDIT.md`','`SUPPLEMENT_OCCUPATION_AUDIT.md`')
  if name=='FORMAL_SCOPE_AUDIT.md':
   txt='> Archive provenance note: original project paths below identify historical evidence. The provided formal inventory, scan and failed-build receipt use FORMAL_ filenames. The project-local reproduction script and Lean checkout are intentionally excluded; obtain the pinned upstream sources and follow their documented build instructions. No formal build succeeded. See ARCHIVE_MAP.json.\n\n'+txt
   txt=txt.replace('`checks/formal_scope/source_inventory.json`','`FORMAL_SOURCE_INVENTORY.json`')
   txt=txt.replace('`static_scan.json`','`FORMAL_STATIC_SCAN.json`')
   txt=txt.replace('`build_receipt.json`','`FORMAL_BUILD_LIMITATIONS.json`')
  b=txt.encode()
 (source/name).write_bytes(b)
# Historical project paths in audit reports identify reviewed files, rather than
# pretending that excluded third-party source caches are redistributed.
archive_map={'original_project_paths':files,'omitted_inputs':{
 'sources/upstream_pinned/':'Fetch exact pinned public OpenAI repository; see PINNED_SOURCE.json.',
 'checks/formal_scope/lean/':'Fetch pinned upstream Lean sources; failed build is documented, not certified.',
 'sources/priority_primary/ PDFs':'Third-party reading copies excluded; source URLs/hashes are in the priority/provenance records.'},
 'note':'Some historical audit reports retain project-local evidence paths. This map identifies supplied counterparts. Internal supplement basename references were normalized for this archive; substantive audit text was preserved.'}
(source/'ARCHIVE_MAP.json').write_text(json.dumps(archive_map,indent=2)+'\n')
checks={name:hashlib.sha256((source/name).read_bytes()).hexdigest() for name in sorted([*files,'ARCHIVE_MAP.json'])}
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
receipt={'version':a.version,'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'packet_directory':str(packet),'files':inv,'third_party_cache_included':False,'publication_state':'review package, not staged or published'}
(packet/'REVIEW_INVENTORY.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({'packet':str(packet),'files':len(inv),'pdf_sha256':hashlib.sha256((kit/'paper.pdf').read_bytes()).hexdigest(),'zip_sha256':hashlib.sha256((kit/'source-and-verification.zip').read_bytes()).hexdigest()}))
