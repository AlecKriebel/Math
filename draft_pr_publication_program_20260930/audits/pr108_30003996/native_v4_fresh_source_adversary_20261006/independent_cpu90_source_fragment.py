"""Pure exact numeric-guard CPU2 to CPU90 replay; no worker execute/resource call."""
import sys
sys.dont_write_bytecode=True
from pathlib import Path
import ast,copy,datetime,hashlib,importlib.util,json,os
D=Path(__file__).resolve().parent
S=D.parent/'native_publication_integration_plan_20261006/corrected_v4'
spec=importlib.util.spec_from_file_location('guards',S/'v3_guards.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
tree=ast.parse((S/'native_assess_worker.py').read_text());function=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='validate_policy')
namespace={'require':g.require};exec(compile(ast.Module(body=[function],type_ignores=[]),str(S/'native_assess_worker.py'),'exec'),namespace)
ns={'__file__':str(D/'independent_control_tests.py'),'__name__':'pure_replay_setup'}
# Build setup only from the own independent fixture, stopping before its mutations.
own=ast.parse((D/'independent_control_tests.py').read_text());prefix=[]
# Stop at the initial control assignment; never run the fixture's check loops.
for node in own.body:
    prefix.append(node)
    if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='control' for t in node.targets):break
exec(compile(ast.Module(body=prefix,type_ignores=[]),str(D/'independent_control_tests.py'),'exec'),ns)
changed=copy.deepcopy(ns['control']);changed['worker_policy']['cpu_seconds']=90
namespace['validate_policy'](changed['worker_policy'])
try:g.validate_worker_control(changed,ns['execution'],ns['execution_bytes'],ns['output'],ns['manifest'])
except ValueError as error:rejection=str(error)
else:raise RuntimeError('CPU90 exact numeric bounds passed and unreviewed control was accepted')
result={'schema':'pr108-fresh-v4-exact-cpu90-replay/v1','UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'PID':os.getpid(),'optimized':not __debug__,'numeric_CPU90_policy_passes':True,'reviewed_CPU2_changed_CPU90_control_rejects':True,'rejection':rejection,'numeric_guard_AST_sha256':hashlib.sha256(ast.dump(function,include_attributes=False).encode()).hexdigest(),'native_prepare_execute_assess_or_resource_setup_calls':0,'actual_control_config_gate_files_created':0}
(D/('CPU90_OPTIMIZED_RESULT.json' if not __debug__ else 'CPU90_NORMAL_RESULT.json')).write_bytes(g.canonical(result))
print(json.dumps(result,sort_keys=True))
