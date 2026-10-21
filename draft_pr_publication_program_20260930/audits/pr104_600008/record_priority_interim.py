from pathlib import Path
import json, hashlib, datetime, os
A=Path(__file__).resolve().parent
P=A.parents[1]
UTC=datetime.datetime.now(datetime.timezone.utc).isoformat()
F=A/'priority_garcia_wustholz_20261006'
M=json.loads((F/'MANIFEST.json').read_text())
pins=[]
for row in M['input_pins']+M['files']:
    path=(F/row['path']).resolve()
    if not path.is_relative_to(A): raise RuntimeError('pin outside effort')
    data=path.read_bytes()
    if len(data)!=row['bytes'] or hashlib.sha256(data).hexdigest()!=row['sha256']:
        raise RuntimeError('manifest body mismatch: '+row['path'])
    pins.append({'path':str(path.relative_to(A)), 'sha256':row['sha256'], 'bytes':row['bytes']})
record={'schema':'pr104-priority-interim/v1','UTC':UTC,'actual_operator_PID':os.getpid(),
    'mathematical_clearance':True,'priority_clearance':False,'publication_clearance':False,
    'bare_already_solved_historical_classification_cleared':False,
    'priority_audit_progress_estimate_percent':60,'workflow_estimate_percent':40,
    'garcia_wustholz_family_manifest_authenticated':True,'authenticated_pins':pins,
    'original_budget':'1/5','extra_central_proof_search_turns':0,
    'pending_families':['exact_formula_history','classical_mechanism_followup','fresh_prior_solution_claim_adversary'],
    'actual_PR_live_readback':json.loads((A/'actual_operations/priority_live_pr_readback/stdout.bin').read_text()),
    'actual_remote_main_readback':(A/'actual_operations/priority_remote_main_readback/stdout.bin').read_text().strip()}
if record['actual_PR_live_readback']['headRefOid']!='4d8ba8e9438c9c8a463721adc1102dee821b11df':
    raise RuntimeError('PRheadchanged')
(A/'ROOT_PRIORITY_INTERIM_RECEIPT_20261006.json').write_text(json.dumps(record,indent=2)+'\n')
progress=json.loads((P/'CURRENT_PROGRESS.json').read_text())
if progress['current_PR']!=104:raise RuntimeError('wrongPR')
progress.update({'UTC':UTC,'updated_UTC':UTC,'current_priority_audit_percent':60,
    'current_PR_workflow_percent':40,'current_workflow_estimate_percent':40,
    'current_mathematical_checkpoint':'9da776b5cf530ef9af6bd5b183ae05e5730a7565',
    'current_mathematical_checkpoint_remote_verified':True,
    'current_priority_interim_record':'audits/pr104_600008/ROOT_PRIORITY_INTERIM_RECEIPT_20261006.json',
    'remaining_current_step':'Adjudicate fresh prior-solution comparison and remaining priority families before disposition or publication.',
    'next_step':'Finish bounded priority comparison for104; no novelty clearance.'})
(P/'CURRENT_PROGRESS.json').write_text(json.dumps(progress,indent=2,sort_keys=True)+'\n')
entry=f'{UTC} — PR104 priority interim: central metric and period identity classical; recovered DR2019/2020 explicitly claims original problem, but limiting surface criterion/count mapping still under independent review. Garcia–Wustholz manifest body authentication passed. Source100%, mathematics100%, priority-audit progress60%, workflow40%; program14/99=14.14%. No historical already_solved or novelty/publication clearance. Original1/5, extra central proof-search0.\n'
for path in [A/'RESEARCH_LOG.md',P/'RESEARCH_LOG.md']:
    with path.open('a') as f:f.write('\n'+entry)
print(json.dumps({k:v for k,v in record.items() if k!='authenticated_pins'}))
