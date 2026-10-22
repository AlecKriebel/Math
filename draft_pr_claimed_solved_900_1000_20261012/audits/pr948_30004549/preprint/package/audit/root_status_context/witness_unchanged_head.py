"""Companion historical-code witness; preserves the earlier actual receipt."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json
S=Path(__file__).with_name('witness.py')
source=S.read_text()
if source.count('inventory=[')!=1:raise ValueError('Exact historical setup prefix')
n={'__name__':'_unchanged_head_witness_','__file__':str(S)}
exec(compile(source.split('inventory=[',1)[0],str(S),'exec',dont_inherit=True,optimize=0),n)
n['hidden']['base']='M'
inventory=[{'number':952,'headRefOid':n['metadata']['headRefOid'],'entries':[{'id':n['ids']['A']}]}]
skipped,selected=n['N']['gate_next'](inventory)
if skipped or selected['problem_id']!=n['ids']['A'] or any(x['request']=='changed filenames' for x in n['calls']):
    raise ValueError('Expected historical unknown-base reuse witness')
out={'utc':datetime.now(timezone.utc).isoformat(),'status':'HISTORICAL_UNSAFE_REUSE_REPRODUCED',
     'finding_id':'R948-WORKFLOW-ROOT-02','amendment':'BASE_REF_OID_BINDING_AFTER_FULL01',
     'source_core_sha256':n['source_pin'],'setup_sha256':hashlib.sha256(S.read_bytes()).hexdigest(),
     'same_initial_and_current_head':True,'unknown_initial_base_context':True,
     'current_base_stably_advanced':'M','initial_target':n['ids']['A'],
     'current_comparison_target':n['ids']['B'],'current_comparison_status':'unsolved',
     'actual_old_selected':selected,'actual_old_calls':n['calls'],'actual_service_calls':0,
     'limitation':'Synthetic exact-code witness, no real excluded problem or retarget event.'}
target=Path(__file__).with_name('WITNESS_UNCHANGED_HEAD_REPLAY.json')
with target.open('x') as f:json.dump(out,f,indent=2);f.write('\n')
print(json.dumps({'status':out['status'],'utc':out['utc'],'actual_service_calls':0}))
