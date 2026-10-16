"""Read-only actual production-schema/chain checks against this review."""
from pathlib import Path
import json,hashlib,sys,datetime,subprocess,os
R=Path(__file__).resolve().parent;A=R.parents[1];P=A.parents[1];D=A/'preprint';CORE=P/'accept_pr952.py'
def need(c,m):
 if not c:raise RuntimeError(m)
def load(p):return json.loads(p.read_bytes())
raw=CORE.read_bytes();need(hashlib.sha256(raw).hexdigest()=='14ac4e7009a1f4973f81aed776d5c6afd344dea93ff369dd65175427e0492eec','external core pin')
n={'__name__':'_full03_readonly_actual_production_validation_','__file__':str(CORE)};exec(compile(raw,str(CORE),'exec',dont_inherit=True,optimize=sys.flags.optimize),n);n['READ_ONLY']=True
ip='9650f0baf87ac6d83a5a7eb934d212cc66ea67dea4c8758813bec47f5a24cc05';fp='ab027971f0245481783e2afa106292543c41f06a93c3c83a0cf8dcea4cff9d77'
context=n['capture_inventory'](ip);f=n['freeze_check']((D/'FREEZE.json').read_bytes(),fp,context);orig=n['original_check']()
pins={'freeze':fp,'manifest':f['package_manifest_sha256'],'pdf':f['files'][n['PDF']]['sha256']}
start=n['utc'](load(R/'private/START_BOUNDARY.json')['timestamp']);now=n['utc_now']();end=n['utc'](now)
ok,ts=n['review_authentication'](load(R/'AUTHENTICATION_START.json'),pins,f,orig);need(ok,'START pass')
cold,tc=n['review_cold'](load(R/'COLD_REPLAY.json'),pins,f,D);need(cold,'type-sensitive canonical cold pass')
attack=n['review_own_attack'](load(R/'PRIOR_ASSESSMENT_INTAKE.json'),(R/'INITIAL_ATTACK.md').read_bytes(),start,end);need(attack,'actual first attack chronology')
need(start<=ts<=tc<=end,'actual current chronology')
inherited=load(R/'INHERITED_DISPOSITIONS_VERIFIED.json')['dispositions'];prior=load(R/'PRIOR_ISSUES_VERIFIED.json')['dispositions']
need(set(inherited)==n['INHERITED_FINDING_IDS'] and len(inherited)==28,'exact28 inherited')
need(set(prior)=={'R952-OPS-ROOT-01','R952-FULL01-PROC-01','R952-FULL01-OPS-01','R952-FULL01-ED-01','R952-FULL02-OPS-01'},'all earlier required/optional/root')
need(all(v.get('verified') is True and type(v.get('evidence')) is str and v['evidence'].strip() for m in [inherited,prior] for v in m.values()),'each own evidence')
row={'utc':now,'phase':sys.argv[1],'actual_core_compile_optimization':sys.flags.optimize,'current_freeze_actual_validation':True,'original33_production_validation':True,'START_production_authentication':ok,'COLD_production_recursive_type_sensitive_exact_all_fields':cold,'own_attack_production_chronology':attack,'inherited_exact28':True,'prior_and_root_exact5':True,'service_or_Git_mutations':0}
if sys.argv[1]=='pre':
 work=R/'private/hostile_final';work.mkdir();(work/'json.py').write_text("raise RuntimeError('FULL03_HOSTILE_IMPORT_POSITIVE_CONTROL')\n")
 env=os.environ.copy();env.update(PYTHONOPTIMIZE='2',PYTHONPATH=str(work),PYTHONUSERBASE=str(work));cmd=[sys.executable,'-S','-B','-c','import json'];t0=n['utc_now']();p=subprocess.run(cmd,cwd=work,env=env,capture_output=True);t1=n['utc_now']()
 for suffix,value in [('stdout.raw',p.stdout),('stderr.raw',p.stderr)]:(R/('COLD_hostile_positive_recorded.'+suffix)).write_bytes(value)
 launch={'start':t0,'end':t1,'argv':cmd,'cwd':str(work),'environment_overrides':{k:env[k] for k in ['PYTHONOPTIMIZE','PYTHONPATH','PYTHONUSERBASE']},'returncode':p.returncode,'actual_unisolated_positive_control':True};(R/'COLD_hostile_positive_recorded.launch.json').write_text(json.dumps(launch,indent=2)+'\n');need(p.returncode!=0 and b'FULL03_HOSTILE_IMPORT_POSITIVE_CONTROL' in p.stderr,'functioning actual hostile positive')
 row['repeated_hostile_positive_with_actual_launch_record']=True
elif sys.argv[1]=='chain':
 result=load(R/'RESULT.json');complete=n['result_schema'](result)
 need(complete or result.get('report_release_status')=='PROVISIONAL_UNSEALED_FORMAT_TEST_NOT_FINAL_VERDICT','actual honest provisional result schema')
 prospective=dict(result);prospective.update(clean_for_preprint=True,entire_package_review=True);prospective.pop('nonclean_history',None)
 need(n['result_schema'](prospective),'prospective final complete schema is valid; no premature emitted clean verdict')
 end_ok,te=n['review_authentication'](load(R/'AUTHENTICATION_END.json'),pins,f,orig);need(end_ok and ts<=tc<=te<=n['utc'](result['completed_utc']),'actual END production schema')
 need(n['exact'](result['inspected_helper_hashes'],f['future_helpers']),'entire inspected helper pins')
 specs=['01:c17f8f4c8812685a2b4a6442695ad99d84359750ab8a13467a21d71d8244e9d9','02:a131470b039f4e75b967d476a705c144258dbc29d8393da1f50eff10b01aef8a','03:'+hashlib.sha256((R/'MANIFEST.json').read_bytes()).hexdigest()]
 try:n['review_check'](specs,f,fp,context)
 except RuntimeError as e:
  need(str(e)=='PR952 guard: at least TWO fresh clean ENTIRE current-package reviews after every fix','unexpected actual review-chain failure: '+str(e));row.update(actual_result_schema_complete=complete,prospective_final_result_schema_complete=True,actual_END_production_authentication=True,actual_review_check_external_specs=specs,actual_review_check_outcome='EXPECTED_REJECT_TWO_REQUIRED',actual_review_check_error=str(e),all_current_rounds_and_individual_records_validated_before_final_two_clean_guard=True,review03_snapshot_scope='Honest incomplete provisional format-test snapshot, never issued as this review verdict, before deliberately repeated final END. Final metadata and final external SHA are independently reauthenticated by parent.')
 else:raise RuntimeError('single clean03 incorrectly accepted by actual chain')
else:raise RuntimeError('phase')
out=R/('REPORT_VALIDATION_'+sys.argv[1]+'.json');out.write_text(json.dumps(row,indent=2)+'\n');print(json.dumps(row,sort_keys=True))
