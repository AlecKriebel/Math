"""Root whole prior state/history/proposal inspection after genuine mirror."""
import datetime as dt
import hashlib
import json
from pathlib import Path
R=Path('/Users/alec/Documents/Math');A=R/'draft_pr_publication_program_20260930/audits/pr40_2814'
def H(b):return hashlib.sha256(b).hexdigest()
def J(p):return json.loads(p.read_bytes())
i=J(A/'state_mirror_intent.json');receipt=J(A/'state_mirror_receipt.json');cap=J(A/'root_integration_mirror_actual_capture/CAPTURE.json')
assert i['status']==receipt['status']=='COMPLETED' and cap['status']=='PASS' and cap['exit_code']==0 and cap['outer_errors']==[]
old=json.loads(i['before_state_bytes']);state=J(R/'unsolved_math_prioritization/state.json');history=(R/'unsolved_math_prioritization/history.jsonl').read_bytes();prefix=i['before_history_bytes'].encode()
assert len(old)==30 and len(state)==31 and set(state)-set(old)=={'2814'} and all(state[k]==v for k,v in old.items())
assert history.startswith(prefix);suffix=history[len(prefix):];events=[json.loads(x) for x in suffix.splitlines()];assert len(events)==1
assert events[0]['id']=='2814' and events[0]['pr']==40 and events[0]['event']=='acceptance_mirror_import'
assert type(events[0]['turns_used']) is int and events[0]['turns_used']==0 and events[0]['turn_limit']==5
assert '20001896' not in state and receipt['duplicate20001896_native_acceptance_added'] is False
assert H(history)==i['history_after_sha256']==receipt['history_sha256'] and H((R/'unsolved_math_prioritization/state.json').read_bytes())==i['state_after_sha256']==receipt['state_sha256']
assert receipt['consumed_substantive_turns']==37 and receipt['current_targets']==31 and receipt['primary_acceptances']==30 and receipt['duplicate_count']==1 and receipt['new_proof_turns']==0 and receipt['negative_ledger_controls']==['bool_count','phantom_attempt','count_one','wrong_id','extra_field']
previous=J(A.parent/'pr39_9500008/state_mirror_bindings.json');current=J(A/'state_mirror_bindings.json')
assert len(previous['entries'])==29 and len(current['entries'])==30 and current['entries'][:-1]==previous['entries'] and current['duplicate_mirrors']==previous['duplicate_mirrors']
inventory=J(R/'draft_pr_publication_program_20260930/inventory.json');assert type(inventory['completed_count']) is int and inventory['completed_count']==30 and type(inventory['current_pr']) is int and inventory['current_pr']==41
for field in ['completion_estimate_percent','program_completion_estimate_percent']:assert type(inventory[field]) is float and inventory[field]==30/180*100
out=dict(status='PASS',utc=dt.datetime.now(dt.timezone.utc).isoformat(),actual_mirror_pid=cap['pid'],full_prior30_states_preserved=True,full_history_prefix_preserved=True,entire_prior29_proposal_entries_and_duplicate_accounting_preserved=True,new_event_count=1,native_targets=31,consumed_original_turns=37,primary_acceptances=30,inventory_actual_percentage=30/180*100,entire_mirror_receipt=receipt,proposal_sha256=H((A/'state_mirror_bindings.json').read_bytes()),new_substantive_attempts=0,audit_turns=0,own_prior_inspector_failure=dict(actual_pid=1011,exit_code=1,failure='Own checker treated the exact five negative-control labels as an integer count. Full receipt actually contains all five named labels. Failed before writing, no candidate/native mutation; V2 checks their entire ordered list.'))
with (A/'ROOT_ACTUAL_MIRROR_INSPECTION.json').open('x') as f:json.dump(out,f,indent=2);f.write('\n')
print(json.dumps(dict(status='PASS',actual_mirror_pid=cap['pid'],native_targets=31,turns=37,primary_acceptances=30)))
