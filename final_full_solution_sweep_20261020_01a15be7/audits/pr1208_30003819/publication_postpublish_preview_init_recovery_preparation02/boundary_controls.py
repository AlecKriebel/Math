"""No-action delegate restrictions and inherited-method identities; no live effects."""
from pathlib import Path
import json,os
P=Path(__file__).resolve().parent
ns={'__name__':'control_library','__file__':str(P/'controls.py')};exec(compile((P/'controls.py').read_bytes(),str(P/'controls.py'),'exec',dont_inherit=True),ns)
H=ns['H'];A=ns['A'];life=ns['life'];pr=ns['pr'];out=P/'private/BOUNDARY_RESULTS.json';reads=P/'private/empty_boundary_reads';reads.mkdir(mode=0o700);base=H['A']['provider_class'](pr,reads);Provider=A['provider_class'](base);p=Provider();results=[]
def reject(label,fn):
 try:fn()
 except RuntimeError as error:results.append({'case':label,'expected_HOLD':True,'error':str(error)});return
 raise RuntimeError('False delegate reached: '+label)
for name in ['git_write','ready','install_state_absent','bind_state','private_state_receipt','tool_context','append_row']:reject('direct_'+name,lambda name=name:getattr(p,name)(None))
for method in ['POST','PUT','DELETE','PATCH']:reject('native_'+method,lambda method=method:p.client().request(method,'https://zenodo.org/api/deposit/depositions/23578142/actions/publish'))
Engine=A['engine_class'](life,lambda e:None,{})
for name in ['gate','observe','family','receipt','edge','record','verify_public','ledger','append_observation','reconcile_ledger_append','assert_shared_state','check_cursor']:
 assert getattr(Engine,name) is getattr(life.Engine,name);results.append({'case':'inherited_core_'+name,'function_object_identical':True})
for name in ['owned_page','search_page','fetch','sheet','states','state_snapshot','get_state','verify_state']:
 assert getattr(Provider,name) is getattr(pr.RealProvider,name);results.append({'case':'inherited_provider_'+name,'function_object_identical':True})
for name in ['capture','maybe_blob','verify_captures']:assert getattr(Provider,name) is getattr(base,name)
assert not H['attempted'];out.write_text(json.dumps({'status':'PASS','cases':results,'count':len(results),'inherited_recovery_capture_methods_identical':True,'actual_external_calls':0,'readiness':False},indent=2)+'\n');out.chmod(0o600);print('BOUNDARIES',len(results),'PASS')
