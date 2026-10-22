from pathlib import Path
from unittest.mock import patch
import sys,json,copy,tempfile,subprocess
R=Path(__file__).resolve().parent;A=R.parents[1];E=A.parents[1];P=E/'private/pr0280_package_adversary_03';sys.path.insert(0,str(A))
import ops_binding as B,publication_live_gates as G
known=E/'private/pr0280_ops/prepublication_f62b765e920248c58f9f2f09371afed9'
root=json.loads((A/'ROOT_PREPUBLICATION_LEAD_RECONCILIATION.json').read_text());gate=json.loads((known/'gate.json').read_text());account=json.loads((known/'account_complete.json').read_text());ledger=json.loads((known/'ledger.json').read_text())
record=next(v for v in account['records'] if int(v['id'])==23137834)
req=lambda v,m: (_ for _ in ()).throw(RuntimeError(m)) if not v else None
req(B.digest(B.identity_projection(record))==root['account_leads'][0]['metadata_and_files_sha256'],'record projection')
req(B.digest(ledger['values'][20])==root['ledger_leads'][0]['values_sha256'],'entire ledger row21')
state=B.REPO/root['unrelated_local_state_exemptions'][0]['path'];before=state.read_bytes();req(B.sha(before)==root['unrelated_local_state_exemptions'][0]['sha256'],'state identity')
cases=[]
def attempt(label,g,ok):
 try:result=G.reconcile(g,'before_integration',B.ORIGINAL)
 except Exception as ex:
  cases.append({'case':label,'accepted':False,'error':str(ex)});req(not ok,'unexpected rejection')
 else:
  cases.append({'case':label,'accepted':True,'accepted_unrelated_states':result['unrelated_local_states_exactly_root_bound']});req(ok,'unexpected acceptance')
attempt('actual_historical_gate_expired',gate,False)
with tempfile.TemporaryDirectory(dir=P,prefix='historical_readonly_replay_') as td:
 out=Path(td);raw=copy.deepcopy(account);(out/'account_complete.json').write_text(json.dumps(raw))
 g=copy.deepcopy(gate);g.update(started_utc=B.stamp(),completed_utc=B.stamp(),raw_receipts=str(out),receipt=str(out/'gate.json'),account_complete_sha256=B.sha((out/'account_complete.json').read_bytes()));(out/'gate.json').write_text(json.dumps(g))
 attempt('historical_identity_synthetic_fresh_timestamps_not_live_clearance',g,True)
 rec=next(v for v in raw['records'] if int(v['id'])==23137834);rec['files'][-1]['size']+=1;(out/'account_complete.json').write_text(json.dumps(raw));g['account_complete_sha256']=B.sha((out/'account_complete.json').read_bytes());attempt('last_file_of_known_full_projection_changed',g,False)
 raw=copy.deepcopy(account);next(v for v in raw['records'] if int(v['id'])==23137834)['metadata']['language']='changed';(out/'account_complete.json').write_text(json.dumps(raw));g['account_complete_sha256']=B.sha((out/'account_complete.json').read_bytes());attempt('non_title_metadata_known_projection_changed',g,False)
 raw=copy.deepcopy(account);(out/'account_complete.json').write_text(json.dumps(raw));g['account_complete_sha256']=B.sha((out/'account_complete.json').read_bytes());g['ledger_matches'][0]['values'][3]+=' changed';attempt('known_entire_ledger_notes_changed',g,False)
req(state.read_bytes()==before,'unrelated state changed')
try:B.require_release_clearance()
except FileNotFoundError:clearance='FAIL_CLOSED_MISSING_ROOT_CLEARANCE_AS_INTENDED'
else:raise RuntimeError('Unexpected root clearance appeared; binding changed')
res={'timestamp':B.stamp(),'root_reconciliation_sha256':B.sha((A/'ROOT_PREPUBLICATION_LEAD_RECONCILIATION.json').read_bytes()),'historical_gate_sha256':B.sha((known/'gate.json').read_bytes()),'all_account_records':len(account['records']),'all_sheet_rows':len(ledger['values']),'full_known_record_metadata_and_entire_file_projection_match':True,'entire_row21_matches':True,'known_lead_semantic_assessment':'Distinct pentagon fifth-torsion/division-field problem20000450/PR329, not fixed triangular-map cycle distribution. Full matching metadata and both file entries plus complete row read.','unrelated_state_sha256_before_and_after':B.sha(before),'cases':cases,'root_clearance':clearance,'scope':'Private cached historical read-only evidence, no current live assertion. Fresh timestamps are a synthetic local replay only. No actual providers or state changes.'}
(R/'ROOT_LEAD_VALIDATION.json').write_text(json.dumps(res,indent=2)+'\n');print(json.dumps(res,indent=2))
