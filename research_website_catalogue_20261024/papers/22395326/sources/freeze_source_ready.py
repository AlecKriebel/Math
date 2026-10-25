"""Freeze source custody, source/reader identity and actual unchanged API objects."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,re
from pypdf import PdfReader
S=Path(__file__).resolve().parent
if (S/'SOURCE_READY.json').exists():raise RuntimeError('preserve_existing_ready')
def now():return datetime.now(timezone.utc).isoformat()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def row(p):return {'path':str(p),'bytes':p.stat().st_size,'sha256':sha(p)}
def save(n,x):(S/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
api=json.loads((S/'record.raw.json').read_text());latest=json.loads((S/'latest.raw.json').read_text());versions=json.loads((S/'versions.raw.json').read_text());assets=json.loads((S/'actual-assets.json').read_text());inventory=json.loads((S/'archive-members.json').read_text());meta=api['metadata']
J=S/'published-source/Symmetry-Stratified_Level2_Journal_TeX.zip/Symmetry-Stratified_Level2_Journal_TeX';R=S/'published-source/Symmetry-Stratified_Level2_Reproducibility.zip/Symmetry-Stratified_Level2_Reproducibility'
comparisons=[]
for p in sorted(J.rglob('*.tex')):
 rel=p.relative_to(J);q=R/'source'/('supplement/supplement.tex' if str(rel)=='supplement.tex' else rel)
 if p.read_bytes()!=q.read_bytes():raise RuntimeError('different_actual_source_editions:'+str(rel))
 comparisons.append({'journal':row(p),'reproducibility':row(q),'byte_identical':True})
readers=[]
for asset in assets:
 name=asset['original_api_file_object']['key']
 if name.endswith('.pdf'):
  p=S/name;q=R/'manuscript'/name
  if p.read_bytes()!=q.read_bytes():raise RuntimeError('embedded_reader_differs')
  readers.append({'published':row(p),'embedded':row(q),'pages':len(PdfReader(p).pages),'byte_identical':True})
for line in (S/'ARCHIVES.sha256').read_text().splitlines():
 h,name=line.split(None,1)
 if sha(S/name.strip())!=h:raise RuntimeError('actual_published_archive_checksum_file')
ready={'utc':now(),'status':'SOURCE_READY_FRESH_COMPLETE_PUBLIC_ASSETS','record_id':22395326,'sheet_row':104,'title':meta['title'],'version':meta['version'],'publication_date':meta['publication_date'],'created':api['created'],'updated':api['updated'],'doi':meta['doi'],'conceptrecid':api['conceptrecid'],'latest_record_id':latest['id'],'versions_total':versions['hits']['total'],'all_assets':assets,'actual_API_asset_order_preserved':True,'transport_receipt_path':str(S/'api-receipts.json'),'transport_receipt_sha256':sha(S/'api-receipts.json'),'raw_API_record':row(S/'record.raw.json'),'archive_inventory':row(S/'archive-members.json'),'archive_containers':inventory['container_count'],'safe_regular_member_occurrences':inventory['safe_regular_member_occurrences'],'expanded_bytes_all_depths':inventory['expanded_bytes_all_depths'],'all_ZIP_CRC_payloads_read':True,'selected_readers':readers,'controlling_main_TeX':row(J/'main.tex'),'controlling_section_sources':[row(p) for p in sorted((J/'sections').glob('*.tex'))],'controlling_supplement_TeX':row(J/'supplement.tex'),'all_TeX_candidates':[row(p) for p in sorted((S/'published-source').rglob('*.tex'))],'full_TeX_editions_compared':comparisons,'printed_manuscript_date':'September 2026','printed_manuscript_version':None,'API_version_not_claimed_as_printed_manuscript_label':True,'originals_now_immutable':True,'historical_or_current_review_opinions_or_foreign_primary_bodies_read_before_independent_mechanism':False,'intake_executed_source_programs':False,'mathematical_verdict':None}
save('normalized-metadata.json',{'utc':now(),'derivative_not_raw_API':True,'record_id':api['id'],'metadata':meta,'created':api['created'],'updated':api['updated'],'all_original_API_file_objects':api['files'],'all_assets':assets,'edition_identity_comparison':{'readers':readers,'TeX':comparisons}})
save('SOURCE_READY.json',ready)
files=[p for p in S.rglob('*') if p.is_file() and '__pycache__'not in p.parts]
save('SOURCE_READY_MANIFEST.json',{'utc':now(),'status':'FROZEN_SOURCE_READY_ORIGINALS','file_count':len(files),'files':[{'path':str(p.relative_to(S)),'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(files)]})
save('SOURCE_READY_SEAL.json',{'utc':now(),'status':'IMMUTABLE_SOURCE_READY','manifest':row(S/'SOURCE_READY_MANIFEST.json'),'ready':row(S/'SOURCE_READY.json'),'frozen_file_count':len(files)})
print(json.dumps({'ready':row(S/'SOURCE_READY.json'),'manifest':row(S/'SOURCE_READY_MANIFEST.json'),'seal':row(S/'SOURCE_READY_SEAL.json'),'assets':len(assets),'readers':[x['pages'] for x in readers],'source_bindings':len(files)},indent=2))
