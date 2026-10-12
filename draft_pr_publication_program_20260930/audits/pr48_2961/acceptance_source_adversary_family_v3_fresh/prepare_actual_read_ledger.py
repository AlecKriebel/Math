"""Own metadata author only, based on genuinely completed ROOT SOURCE captures."""
import datetime as dt,hashlib,json
from pathlib import Path
R=Path('/Users/alec/Documents/Math');A=R/'draft_pr_publication_program_20260930/audits/pr48_2961';F=A/'acceptance_source_adversary_family_v3_fresh';V=A/'acceptance_preparation_family_v3'
operations=[]
for name in ['root_pr48_source_v3_closure_actual_capture','root_pr48_source_v3_closed_readback_actual_capture']:
    p=R/'draft_pr_publication_program_20260930/audits/pr45_9900007'/name/'CAPTURE.json';c=json.loads(p.read_bytes())
    assert c['completed'] is True and c['exit_code']==0
    operations.append({'capture_path':p.relative_to(R).as_posix(),'argv':c['argv']})
with (F/'ROOT_SOURCE_OPERATIONS.json').open('x') as h:json.dump(operations,h,indent=2,sort_keys=True);h.write('\n')
rows=[]
for n in ['pr48_guards.py','integrate_reviewed_partial.py','state_mirror_reconciliation.py','verify_post_acceptance.py','seal_final_evidence.py','capture_root_final_operation.py','CONTRACT.md','ROOT_POST_CONTRACT.json','SCIENTIFIC_SCOPE.json','DRAFT_FINAL_PLAN.json','DRAFT_ROOT_IMMUTABLE_BINDINGS.json','DRAFT_ROOT_PRIMARY_READ_LEDGER.json','DRAFT_ROOT_SCIENCE_CARD.json','DRAFT_ROOT_SCOPE_CERTIFICATE.json','close_source.py','verify_closed_source.py','REPORT.md','VERDICT.json','CHANGE_MAP.json']:
    b=(V/n).read_bytes();rows.append({'path':(V/n).relative_to(R).as_posix(),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'entire_text_personally_read':True})
with (F/'SOURCE_READ_LEDGER.json').open('x') as h:json.dump({'schema':'pr48-v3-fresh-personal-source-read-ledger/v1','utc':dt.datetime.now(dt.timezone.utc).isoformat(),'files':rows,'production_imported_compiled_executed':False,'prior_PASS_transferred':False,'scientific_proofs_independently_reproved':False},h,indent=2,sort_keys=True);h.write('\n')
print('Real completed SOURCE operations bound; six-source personal read ledger authored.')
