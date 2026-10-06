from pathlib import Path
import json,datetime,os
A=Path(__file__).resolve().parent;P=A.parents[1];C=A.parents[2]
UTC=datetime.datetime.now(datetime.timezone.utc).isoformat()
agents=['pr104_priority_exact_formula_history_20261006','pr104_priority_garcia_wustholz_20261006','pr104_priority_classical_mechanism_20261006']
progress=json.loads((P/'CURRENT_PROGRESS.json').read_text())
if progress['current_PR']!=104 or not progress['current_mathematical_clearance']:raise RuntimeError('math gate not closed')
progress.update({'UTC':UTC,'updated_UTC':UTC,'current_fresh_priority_agents':agents,'current_priority_audit_percent':5,
 'current_PR_workflow_percent':30,'current_workflow_estimate_percent':30,
 'remaining_current_step':'Close independent priority families and adjudicate exact prior contributions before preprint preparation.',
 'next_step':'Independent deep priority families running for104.'})
(P/'CURRENT_PROGRESS.json').write_text(json.dumps(progress,indent=2,sort_keys=True)+'\n')
record={'UTC':UTC,'actual_operator_PID':os.getpid(),'agents':agents,'mathematical_gate_closed_before_priority_start':True,
 'mathematics_percent':100,'priority_percent':5,'workflow_percent':30,'program_completed':14,'dated_denominator':99,
 'priority_clearance':False,'publication_clearance':False,'original_budget':'1/5','new_central_proof_search_turns':0}
(A/'PRIORITY_AUDIT_START_20261006.json').write_text(json.dumps(record,indent=2,sort_keys=True)+'\n')
entry=UTC+' — Three independent priority families launched after the clean mathematical gate: exact formula/question history, Garcia-Wustholz announcement and subsequent evidence, and classical mechanism comparison. Mathematics100%, priority5%, PR104workflow30%; program14/99=14.14%. Original1/5, extra central proof-search0. No novelty or publication clearance.\n'
for path in [A/'RESEARCH_LOG.md',P/'RESEARCH_LOG.md']:
 with path.open('a') as f:f.write('\n'+entry)
selection=A/'MATH_CHECKPOINT_SELECTION_20261006.json';data=json.loads(selection.read_text())
data['paths']=sorted(set(data['paths']+[str((A/name).relative_to(C)) for name in ['PRIORITY_AUDIT_START_20261006.json','record_priority_start.py']]))
selection.write_text(json.dumps(data,indent=2,sort_keys=True)+'\n')
print(json.dumps(record))
