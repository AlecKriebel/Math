from pathlib import Path
import json, datetime, os
A=Path(__file__).resolve().parent; P=A.parents[1]; C=P.parent
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
def write(q,x):q.write_text(json.dumps(x,indent=2,sort_keys=True)+'\n')
progress=json.loads((P/'CURRENT_PROGRESS.json').read_text())
progress={k:v for k,v in progress.items() if not k.startswith('current_')}
progress.update({
 'UTC':now,'updated_UTC':now,'current_PR':108,'current_problem_id':30003996,
 'current_original_head':'3526d46bf143b08e5055ffa7728c6278e9f958ea',
 'current_original_literal_status':'claimed_solved','current_original_budget':'2/5',
 'current_original_budget_provenance':'incoming QUEUE row and research-log approaches; no submitted machine-readable turn ledger',
 'current_new_central_proof_search_turns':0,'current_source_authentication_complete':True,
 'current_source_authentication_percent':100,
 'current_source_authentication_record':'audits/pr108_30003996/original_source_authentication_20261006/ORIGINAL_BLOB_MANIFEST.json',
 'current_sourcepair_record':'audits/pr108_30003996/original_source_authentication_20261006/SOURCEPAIR_AUTHENTICATION.json',
 'current_primary_sources_record':'audits/pr108_30003996/primary_sources_20261006/PRIMARY_CUSTODY_MANIFEST.json',
 'current_fresh_math_agents':['pr108_all_trees_threshold_adversary_20261006','pr108_independent_reproduction_adversary_20261006','pr108_source_scope_complexity_adversary_20261006'],
 'current_mathematical_audit_percent':30,'current_mathematical_clearance':False,
 'current_priority_audit_percent':0,'current_priority_clearance':False,'current_novelty_established':False,
 'current_publication_ready':False,'current_publication_percent':0,'current_DOI':None,
 'current_tracker_range':None,'current_merge_commit':None,'current_native_integration_complete':False,
 'current_PR_workflow_percent':10,'current_workflow_estimate_percent':10,
 'current_human_disposition_question_pending':False,
 'advance_to_next_PR_authorized_now':False,'next_eligible_order_requires_fresh_status_check':False,
 'next_numeric_intake_cursor':108,'next_eligible_PR_after_current_completion':None,
 'latest_ordered_intake_record':'ordered_intake_20261006/after_PR107/INTAKE_AFTER_PR107.json',
 'next_step':'Complete and authenticate PR108 fresh mathematical families and checker repair; then independent priority audit.',
 'remaining_current_step':'Fresh family final reports, explicit -O-safe checker guards, current actual reproductions.',
 'skipped_since_last_completion':[],
 'persistent_goal_status':'active','persistent_goal_complete':False,
})
write(P/'CURRENT_PROGRESS.json',progress)
note=f'\n{now} — PR108 exact claimed_solved2/5 head/source-pair authenticated; original structured turn ledger absent, QUEUE/prose provenance preserved. Full literal all-root Problem1 and independent root threshold reconstruction checked. Three fresh math families pending final readback; guard repair pending. Source100%, mathematics30%, priority0%, PR108workflow10%; program16/99=16.16%. No novelty/publication clearance. PR107 closure completion metadata/cleanup readback included in this checkpoint.\n'
for q in [A/'RESEARCH_LOG.md',P/'RESEARCH_LOG.md']:
 with q.open('a') as f:f.write(note)
paths=set()
def add(q):
 if not q.is_file() or q.is_symlink():raise RuntimeError('not regular: '+str(q))
 paths.add(str(q.relative_to(C)))
def directory(q):
 for p in sorted(q.rglob('*')):
  if p.is_file():add(p)
for q in [P/'CURRENT_PROGRESS.json',P/'RESEARCH_LOG.md']:
 add(q)
for name in ['authenticate_original_source.py','authenticate_source_pair.py','prepare_primary_source_custody.py','record_cli.py','scoped_checkpoint.py','RESEARCH_LOG.md','ROOT_INDEPENDENT_RECONSTRUCTION_20261006.md','prepare_intake_checkpoint.py']:
 add(A/name)
S=A/'original_source_authentication_20261006'
directory(S/'original_attempt')
for q in S.glob('*.json'):add(q)
add(A/'primary_sources_20261006/PRIMARY_CUSTODY_MANIFEST.json')
for label in ['authenticate_original_source','authenticate_source_pair','primary_source_custody']:
 directory(A/'actual_operations'/label)
directory(P/'ordered_intake_20261006/after_PR107')
B=P/'audits/pr107_30003997'
for name in ['ROOT_CLOSURE_RELEASE_ACTUAL_READBACK_20261006.json','record_closure_release_readback.py','intake_after_PR107.py','PRIVATE_BACKEND_CLEANUP_RECEIPT_20261006.json','cleanup_private_backend.py','RESEARCH_LOG.md','MATH_CHECKPOINT_SELECTION_20261006.json']:
 add(B/name)
for label in ['completion_release_actual_readback','ordered_intake_after_PR107','cleanup_private_backend','completion_release']:
 directory(B/'actual_operations'/label)
directory(B/'actual_completion_release_readback_20261006')
for name in ['RECEIPT.json','PROCESS_JOURNAL.json']:add(B/'actual_checkpoints/completion_release'/name)
write(A/'INTAKE_CHECKPOINT_SELECTION_20261006.json',{'paths':sorted(paths),'UTC':now,'actual_preparation_PID':os.getpid(),'third_party_PDFs_excluded':True,'evolving_agent_outputs_excluded':True})
print(json.dumps({'UTC':now,'actual_preparation_PID':os.getpid(),'selected_regular_paths':len(paths),'source_percent':100,'math_percent':30,'priority_percent':0,'PR108_workflow_percent':10,'program_completed':16,'dated_total':99}))
