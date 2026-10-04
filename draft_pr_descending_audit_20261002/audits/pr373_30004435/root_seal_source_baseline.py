"""Seal the original-source reconstruction before reading candidate mathematics."""
from pathlib import Path
import datetime,hashlib,json
A=Path(__file__).resolve().parent
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
d=json.loads((A/'root_render_receipt.json').read_text())
for f in d['files']:f['visually_inspected']=True
d.update(visual_inspection_pending=False,inspection_utc=now)
(A/'root_render_receipt.json').write_text(json.dumps(d,indent=2)+'\n')
source=json.loads((A/'root_primary_source_receipt.json').read_text())
source.update(source_passages_and_render_check_pending=False,direct_source_read_utc=now,read_passages={'owr':'PDF32-33, Steif Question C','alnajjar_shmaya':'PDF13-14, Theorem5.2 and Example6.1','lemanczyk':'PDF111-116 AppendixB.1-B.3','bressaud_fernandez_galves':'PDF1-9 definitions and complete maximal coupling/agreement-length proof'},direct_visual_inspection_pages=d['files'])
(A/'root_primary_source_receipt.json').write_text(json.dumps(source,indent=2)+'\n')
failure={'recorded_utc':now,'stage':'render-inspection metadata updater, before any write','exit':1,'failure_kind':'IndentationError','stderr':'  File "<stdin>", line 6\n    dumm=0\nIndentationError: unexpected indent\n','candidate_mathematics_failure':False,'correction':'Remove stray indented temporary assignment; use saved root_seal_source_baseline.py. Failed inline command parsed no statements and wrote no files.'}
(A/'root_metadata_updater_failure.json').write_text(json.dumps(failure,indent=2)+'\n')
names=['ROOT_SOURCE_FIRST_BASELINE.md','root_primary_source_receipt.json','root_render_receipt.json']
seal={'utc':now,'workflow_percent':15,'unrestricted_method_resolution_percent':0,'source_first':True,'candidate_prose_code_receipts_old_review_and_sibling_proofs_read_before_seal':False,'prior_routing_exposure':'Live draft body, filenames, source locator/hash metadata only. No PR373 mathematical candidate or review prose opened. Primary proofs reconstructed independently. PR374 is still at its final live metadata gate.','files':{name:sha(A/name) for name in names},'frozen_candidate_manifest_sha256':sha(A/'snapshot_manifest.json'),'private_primary_pdf_hashes':{p.name:sha(p) for p in sorted((A/'raw_sources').glob('*.pdf'))},'new_full_resolution_claim':False}
(A/'root_source_first_seal.json').write_text(json.dumps(seal,indent=2)+'\n')
with (A/'RESEARCH_LOG.md').open('a') as f:f.write(f'\n{now}: workflow15%, full original method resolution0%. Four fresh pinned PDFs and all designated source passages read directly; four critical pages visually inspected. Independent finite/HMM/coupling/finitary/mixture boundary baseline sealed before candidate prose/program/old review. Metadata-updater syntax failure before writes preserved in root_metadata_updater_failure.json; corrected saved updater. PR374 disposition still pending live cached-merge refresh; this is PR373 preparation only.\n')
print(json.dumps({'status':'PASS_SOURCE_FIRST_SEAL','utc':now,'baseline_sha256':seal['files']['ROOT_SOURCE_FIRST_BASELINE.md'],'workflow':15}))
