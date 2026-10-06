"""Prepare an exact public-safe checkpoint; do not mutate shared tracked/Git files."""
import datetime
import hashlib
import json
from pathlib import Path

R = Path('/Users/alec/Documents/Math')
P = R / 'draft_pr_publication_program_20260930'
A = P / 'audits/pr80_30000177'
Q = Path(__file__).resolve().parent
now = datetime.datetime.now(datetime.timezone.utc).isoformat()

def pin(p):
    b = p.read_bytes()
    return {'path': str(p.relative_to(R)), 'bytes': len(b),
            'sha256': hashlib.sha256(b).hexdigest()}

base = P / 'CURRENT_PROGRESS.json'
base_bytes = base.read_bytes()
o = json.loads(base_bytes)
assert o['current_PR'] == 73 and o['fully_completed_count'] == 9
o = {k:v for k,v in o.items() if not k.startswith('current_')}
o.update({
    'UTC': now, 'current_PR': 80, 'current_problem_id': 30000177,
    'current_original_head': 'dcfeb5d8ad68b397ec509c70e85c6fca46cd01e3',
    'current_original_literal_status': 'claimed_solved',
    'current_original_budget': '1/5', 'current_new_central_proof_search_turns': 0,
    'current_mathematical_audit_percent': 100,
    'current_mathematical_gate': str(A/'ROOT_MATHEMATICAL_GATE_20261004.md'),
    'current_fresh_math_agents': [
        '/root/pr80_primary_model_adversary_20261004',
        '/root/pr80_coding_theorem_adversary_20261004',
        '/root/pr80_channel_entropy_adversary_20261004'],
    'current_math_family_evidence_readback_complete': True,
    'current_source_authentication_complete': True,
    'current_source_authentication_record': str(A/'original_source_authentication_20261004/CUSTODY_REPORT.md'),
    'current_source_authentication_percent': 100,
    'current_priority_audit_complete': False, 'current_priority_clearance': False,
    'current_priority_audit_percent': 60,
    'current_priority_families': [
        '/root/pr80_target_priority_family_20261004',
        '/root/pr80_mechanism_priority_family_20261004'],
    'current_PR_workflow_percent': 30,
    'current_package': None, 'current_DOI': None,
    'current_publication_percent': 0,
    'current_publication_authorization': 'User authorized conditionally on mathematical, priority and whole-package gates; gates are not yet all complete.',
    'current_qualified_package_ready': False,
    'current_merge_commit': None, 'current_acceptance_commit': None,
    'current_native_integration_started': False,
    'current_last_audit_checkpoint_commit': None,
    'last_completed_scientific_checkpoint_commit': '0ef85caa41ba20ebd15786dc379f98f9f6a28293',
    'last_completed_final_audit_checkpoint_commit': '49366352ca8882c258f3acf85057a0d52a6b63a0',
    'last_completed_final_completion_readback': 'audits/pr73_2985/ROOT_POST_COMPLETION_RELEASE_READBACK_20261004.json',
    'latest_ordered_intake_record': 'ordered_intake_20261004/after_PR73/INTAKE_AFTER_PR73.json',
    'skipped_since_last_completion': [74,75,76,77,78,79],
    'next_numeric_intake_cursor': 81,
    'advance_to_next_PR_authorized_now': False,
    'remaining_current_step': 'Complete independent priority reports and ROOT adjudication for PR80. If cleared, prepare and independently review the entire preprint package before authorized publication/native merge. No advancement past PR80 before its actual completed disposition and writer release.',
    'persistent_goal_complete': False})
prepared = Q/'CURRENT_PROGRESS_PREPARED.json'
prepared.write_text(json.dumps(o, indent=2, sort_keys=True)+'\n')
files = [A/'RESEARCH_LOG_20261004.md', A/'ROOT_MATHEMATICAL_GATE_20261004.md',
         A/'ROOT_MATHEMATICAL_GATE_PINS_20261004.json',
         A/'ROOT_channel_check_20261004/check_channel.py']
for folder in ['primary_model_adversary_20261004',
               'coding_theorem_adversary_20261004',
               'channel_entropy_adversary_20261004']:
    for name in ['FIRST_SOURCE_ONLY.md','FIRST_CANDIDATE_VERDICT.md','REPORT.md','VERDICT.json']:
        files.append(A/folder/name)
files.append(A/'channel_entropy_adversary_20261004/DERIVATION.md')
receipt = A/'ROOT_channel_check_20261004/process_evidence/root_independent_channel/result.json'
if not receipt.exists():
    matches = [p for p in (A/'ROOT_channel_check_20261004/process_evidence').glob('*/result.json')
               if json.loads(p.read_text()).get('actual_PID') == 83579]
    assert len(matches)==1
    receipt=matches[0]
r = json.loads(receipt.read_text())
assert r['exit_code']==0
b = Path(r['stdout_path']).read_bytes()
assert hashlib.sha256(b).hexdigest()==r['stdout_sha256']
assert json.loads(b)['assertions']==551
(Q/'ROOT_EXACT_CHANNEL_RESULTS.json').write_bytes(b)
files += [Q/'ROOT_EXACT_CHANNEL_RESULTS.json', Q/'prepare_checkpoint.py', Q/'README.md']
rows=[pin(p) for p in files]
assert all(not any(t in v['path'] for t in ['private_sources/','process_evidence/','original_source_authentication_20261004/']) for v in rows)
packet = {'schema':'pr80-math-checkpoint-preparation/v1','UTC':now,
          'shared_writer_lease_granted':False,'shared_tracked_or_git_mutation_performed':False,
          'science':'Mathematical gate only; priority ongoing; no manuscript or publication clearance.',
          'CURRENT_PROGRESS_base_pin':pin(base),'CURRENT_PROGRESS_prepared_pin':pin(prepared),
          'public_safe_files':rows,'target_shared_progress_path':str(base.relative_to(R)),
          'requires_fresh_writer_ACK_before_application':True,
          'completed_program_count':9,'dated_eligible_denominator':99,
          'new_central_proof_search_turns':0,'original_budget':'1/5'}
(Q/'MANIFEST.json').write_text(json.dumps(packet,indent=2,sort_keys=True)+'\n')
print(json.dumps({'status':'PREPARED_ONLY','files':len(rows),
                  'manifest':pin(Q/'MANIFEST.json'),
                  'prepared_progress':pin(prepared)},indent=2))
