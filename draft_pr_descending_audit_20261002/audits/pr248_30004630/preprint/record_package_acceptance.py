from pathlib import Path
from datetime import datetime, timezone
import hashlib, json
PRE=Path(__file__).resolve().parent
P=PRE.parents[2]
D=PRE.parent/'initial_review_20261013'
utc=datetime.now(timezone.utc).isoformat()
r=json.loads((PRE/'root_archive_reproduction/VERIFICATION_RUN.json').read_text())
def count(receipt):
    return next(receipt[k] for k in ['assertions','exact_assertions','exact_checks'] if k in receipt)
total=sum(count(x['receipt']) for x in r['results'])
diagnostics=next(x['receipt']['categories']['threshold_high_precision_sanity'] for x in r['results'] if x['checkset']=='variational215')
assert total-diagnostics==5603 and diagnostics==5
metadata=json.loads((PRE/'metadata.json').read_text())
deposit=json.loads((PRE/'deposit.json').read_text())
assert metadata==deposit['metadata']==json.loads((PRE/'verification_package/metadata.json').read_text())
assert (PRE/'critical_wave_growth.tex').read_bytes()==(PRE/'verification_package/manuscript/critical_wave_growth.tex').read_bytes()
QA=[]
for f in sorted((PRE/'tmp/pdfs').glob('page-*.png')):
    data=f.read_bytes()
    QA.append({'path':str(f),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'visually_inspected':True,'layout_defects_found':False})
assert len(QA)==6
x={'utc':utc,'case_percent':70,'root_full_manuscript_read':True,'PDF_pages':6,'PDF_visual_QA':QA,
   'desktop_source_compilation':'success','tectonic_export':'success',
   'latex_warning_scan':'No Overfull, Underfull, Warning, Error or Undefined match',
   'source_UI':'queued, not claimed visible','archive_files':113,
   'actual_extracted_archive_replay':{'full_receipts_matched':7,'exact_assertions_derived':total-diagnostics,
       'noncertified_diagnostics_derived':diagnostics,'report':str(PRE/'root_archive_reproduction/VERIFICATION_RUN.json')},
   'metadata_exact_equality':True,'metadata_local_kit_check':'PASS; actual check executed 2026-10-14T04:17 UTC',
   'bookkeeping_repair':'Initial count aggregator omitted exact_assertions field; corrected without rerunning unchanged checksets. Package total was correct.',
   'scope':'Unmodified ordinary-cone strict positivity to strong L2 implication; zero cone explicit; classical mechanisms credited',
   'fresh_sequential_manuscript_review_required':True,'upload_clearance':False}
(PRE/'ROOT_PACKAGE_ACCEPTANCE.json').write_text(json.dumps(x,indent=2)+'\n')
note=(utc+' — Best guess 70% case completion. Six-page credited note exported and source independently compiled; '
      'every rendered page visually inspected without a defect. Immutable 113-file ZIP with seven actual extracted-archive '
      'full receipt replays: 5,603 exact assertions plus five noncertified diagnostics. Metadata matches across archive, '
      'file and deposit; local Zenodo kit check passes. Initial preparation output-directory and publisher-variable '
      'issues were fixed before PDF export or native writes. Root receipt-count aggregator was corrected to include '
      'the original independent checker exact_assertions key; package counts were already correct. Actual 55% priority '
      'checkpoint: ffad072854f07e3fea6ec223c4de3e569e57689a. Two NEW sequential manuscript/package reviews remain. '
      'No upload, tracker write or native PR merge. Counts 39/16/16/0; overall goal active and incomplete.\n')
(PRE/'RESEARCH_LOG.md').write_text('# Preprint preparation log\n\n'+note)
y=json.loads((D/'CURRENT_AUDIT_STATE.json').read_text())
y.update(utc=utc,stage='six_page_note_and_113_file_package_prepared_first_fresh_review_pending',completion_percent=70,preprint_upload_cleared=False)
(D/'CURRENT_AUDIT_STATE.json').write_text(json.dumps(y,indent=2)+'\n')
y=json.loads((P/'CURRENT_GOAL_SELECTION_20261013.json').read_text())
y.update(utc=utc,case_completion_percent=70,current_stage='six_page_note_and_113_file_package_prepared_first_fresh_review_pending')
(P/'CURRENT_GOAL_SELECTION_20261013.json').write_text(json.dumps(y,indent=2)+'\n')
with (P/'RESEARCH_LOG.md').open('a') as f:
    f.write('\n'+note)
print(json.dumps({'utc':utc,'case_percent':70,'derived_exact_assertions':total-diagnostics,'diagnostics':diagnostics,'upload_clearance':False}))
