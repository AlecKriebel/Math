"""Accept the independently cleared, byte-bound final correction without changing it."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, stat
A = Path(__file__).resolve().parent
F = A/'priority_correction_finalization_review'
D = A/'priority_correction_packet'
sha = lambda b: hashlib.sha256(b).hexdigest()
pin = lambda p: {'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())}
def require(c,label):
    if not c:
        raise RuntimeError(label)
manifest = json.loads((F/'FINALIZATION_REVIEW_MANIFEST.json').read_bytes())
require(pin(F/'FINALIZATION_REVIEW.md')['sha256'] == 'e7322f2a10babb5f938dfc10c69a8381aaf5d90d2df1ec463477cbd62ca27b79','Report changed')
require(pin(F/'FINALIZATION_REVIEW_MANIFEST.json')['sha256'] == 'b0995748c9e1b4658c8d4b26f035e31ca8f03de83b2b3e43cfdfe5ec38af88af','Manifest changed')
require(manifest['status'] == 'PASS_BOUNDED_FINALIZATION_RECHECK' and manifest['no_remaining_concerns_within_scope'],'Independent recheck not cleared')
bound = {}
for name, expected in manifest['files'].items():
    require(pin(F/name) == expected,'Review artifact changed: '+name)
    bound[name] = dict(expected, observed_mode=oct(stat.S_IMODE((F/name).stat().st_mode)))
for name, expected in manifest['bound_input_receipts'].items():
    require(pin(A/name) == expected,'Root receipt changed: '+name)
final = json.loads((A/'PRIORITY_CORRECTION_FINALIZATION.json').read_bytes())
require(manifest['final_six'] == final['final_packet'],'Final pins differ')
for name, expected in final['final_packet'].items():
    require(pin(D/name) == expected,'Packet changed')
require((F/'executions/validation.stdout').read_bytes() == (F/'executions/finalization_validation.json').read_bytes(),'Complete output differs')
require(not (F/'executions/validation.stderr').read_bytes(),'Bounded validation stderr nonempty')
validation = json.loads((F/'executions/validation.stdout').read_bytes())
require(validation['bookkeeping_assertions'] == 249 and not validation['scientific_tests_run'],'Unexpected validation scope')
intent = json.loads((A/'PRIORITY_CORRECTION_PUSH_INTENT.json').read_bytes())
require(intent['packet'] == final['final_packet'] and len(intent['expected_scope']) == 20 and len(intent['preserved_historical_files']) == 15,'Prepared integration scope differs')
snapshot = json.loads((A/'priority_corrected_snapshot_manifest.json').read_bytes())
require(snapshot['head'] == intent['head'] and snapshot['base'] == intent['parents'][1],'Prepared head differs')
for e in snapshot['files']:
    p = A/'priority_corrected_snapshot'/e['path']
    require(pin(p) == {k:e[k] for k in ['bytes','sha256']},'Corrected snapshot changed')
Q = 'unsolved_math_prioritization/QUEUE.md'
lines = (A/'priority_corrected_snapshot'/Q).read_bytes().splitlines()
row = lines[intent['queue_row']-1]
require(row.decode()+'\n' == intent['new_row'] and [row.split(b'|')[j].strip() for j in [8,9]] == [b'already_solved',b'1/5'],'Own corrected row differs')
out = {'utc':datetime.now(timezone.utc).isoformat(),'status':'PASS_FINAL_PRIORITY_CORRECTION_READY_FOR_BRANCH_UPDATE',
    'final_packet':final['final_packet'],'accepted_finalization_report':pin(F/'FINALIZATION_REVIEW.md'),
    'accepted_finalization_manifest':pin(F/'FINALIZATION_REVIEW_MANIFEST.json'),'bound_review_files':bound,
    'accepted_original_report_sha256':manifest['accepted_original_report_sha256'],
    'accepted_original_manifest_sha256':manifest['accepted_original_manifest_sha256'],
    'bookkeeping_controls':249,'scientific_tests_rerun':False,
    'root_semantic_reads':['Complete original correction report previously read','Complete finalization report/log/manifest/code/full output read','Original and final six files authored/read with exact bounded replacements','Prepared integration own QUEUE row and all20 pins checked'],
    'integration_intent':pin(A/'PRIORITY_CORRECTION_PUSH_INTENT.json'),'prepared_commit':intent['head'],
    'operational_status':'already_solved','author_turns':'1/5','math_percent':100,'bounded_priority_percent':100,
    'workflow_percent':90,'remote_state_clearance_pending':True,'branch_update_ready':True,
    'paper':False,'merge':False,'close':False,'zenodo':False,'tracker':False}
p = A/'ROOT_FINAL_CORRECTION_ACCEPTANCE.json'
require(not p.exists(),'Acceptance exists')
p.write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':out['status'],'prepared_commit':intent['head'],'scope_paths':20,'preserved_files':15,'workflow_percent':90},indent=2))
