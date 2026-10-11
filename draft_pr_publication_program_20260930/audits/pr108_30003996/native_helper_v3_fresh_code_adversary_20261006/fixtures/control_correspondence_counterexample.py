"""Pure exact-code correspondence counterexample; no prepare/worker/native invocation."""
import sys
sys.dont_write_bytecode=True
from pathlib import Path
import ast,json,os,datetime
import v3_guards as g
import native_assess_worker as worker
O=Path(__file__).resolve().parent.parent;D=O.parent/'native_publication_integration_plan_20261006/corrected_v3'
reviewed={'deadline_seconds':120,'cpu_seconds':2,'address_space_bytes':536870912,'file_size_bytes':33554432,'open_files':32,'memory_limit_mode':'advisory_no_hard_memory_claim'}
changed={**reviewed,'cpu_seconds':90};worker.validate_policy(reviewed)
wt=ast.parse((D/'native_assess_worker.py').read_bytes());execute=next(n for n in wt.body if isinstance(n,ast.FunctionDef) and n.name=='execute')
policy_nodes=[n for n in execute.body if n.lineno==49]
if len(policy_nodes)!=2:raise ValueError('Expected exact policy assignment/validation statements changed')
control={'worker_policy':changed};scope={'control':control,'validate_policy':worker.validate_policy}
exec(compile(ast.fix_missing_locations(ast.Module(body=policy_nodes,type_ignores=[])),'sealed_worker_policy_fragment','exec'),scope)
if scope['policy']!=changed:raise ValueError('Counterexample policy not selected')
pt=ast.parse((D/'prepare_review_bundle.py').read_bytes());prepare=next(n for n in pt.body if isinstance(n,ast.FunctionDef) and n.name=='prepare');block=next(n for n in prepare.body if isinstance(n,ast.Try))
checks=[n for n in block.body if n.lineno==345]
if len(checks)!=1:raise ValueError('Exact parent acceptance predicate changed')
inputs_sha='synthetic-review-binding-fixture';proc={'PID':12345}
result={'outcome':'success','native_assess_returned_without_exception':True,'actual_operator_PID':12345,'execution_inputs_sha256':inputs_sha,
        'requested_resource_policy':changed,'applied_limits':{'RLIMIT_CPU':[90,90],'RLIMIT_FSIZE':[33554432,33554432],'RLIMIT_NOFILE':[32,32]}}
scope={'result':result,'proc':proc,'inputs_sha':inputs_sha,'require':g.require}
exec(compile(ast.fix_missing_locations(ast.Module(body=checks,type_ignores=[])),'sealed_parent_acceptance_fragment','exec'),scope)
record={'schema':'pr108-v3-derived-worker-policy-exact-fragment-counterexample/v1','fixture_only':True,'actual_operator_PID':os.getpid(),
        'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'mode':'optimized' if not __debug__ else 'normal',
        'reviewed_worker_policy':reviewed,'changed_derived_control_policy':changed,'exact_worker_policy_fragment_validated_changed_policy':True,
        'exact_parent_success_predicate_accepted_changed_policy_with_same_inputs_sha':True,
        'synthetic_worker_success_and_applied_limits':True,'no_actual_worker_process_or_resource_setup_for_counterexample':True,
        'concurrent_edit_trigger':'WORKER_CONTROL.json CPU limit changed from2 to90 after parent construction and before worker read.',
        'extracted_exact_locations':{'worker':'native_assess_worker.py:49','parent':'prepare_review_bundle.py:345'},
        'native_prepare_assess_export_calls':0,'actual_configuration_or_gate_files_created':False,'service_calls':0}
(O/('CONTROL_CORRESPONDENCE_'+record['mode'].upper()+'.json')).write_bytes(g.canonical(record));print(json.dumps(record))
