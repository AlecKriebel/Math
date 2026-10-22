import importlib.util,json,sys,os
from pathlib import Path
R=Path(__file__).resolve().parent;P=R.parents[3];A=R.parents[1];T=R/'private'/('finalizer_auth_'+os.environ.get('REVIEW_MODE','initial'));T.mkdir(parents=True,exist_ok=False);Q=T/'publication';Q.mkdir();sys.dont_write_bytecode=True
spec=importlib.util.spec_from_file_location('review04_finalizer',P/'finalize_pr938_and_gate_next.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
for name in ['ZENODO_PUBLISH.json']:(Q/name).write_text('{}')
for name in ['PR_MERGE_RECEIPT.json','TRACKER_RECEIPT.json','NATIVE_PUBLICATION_RECEIPT.json','ACCEPTANCE.json']:(T/name).write_text('{}')
(Q/'PREPUBLICATION_FREEZE.json').write_bytes((A/'publication/PREPUBLICATION_FREEZE.json').read_bytes())
marker=T/'EXECUTED_BEFORE_AUTHENTICATION.txt'
(T/'append_pr938_tracker.py').write_text('from pathlib import Path\nPath('+repr(str(marker))+').write_text("Controlled private marker only")\n')
m.P=T;m.A=T;m.D=Q
m.run=lambda *args:(_ for _ in ()).throw(RuntimeError('Forbidden external call'))
reason=''
try:m.verify_completed()
except RuntimeError as error:reason=str(error)
if reason!='Reviewed receipt checker changed' or not marker.is_file():raise RuntimeError('Unexpected result '+reason)
result={'actual_parent_optimization':sys.flags.optimize,'status':'ADVERSE_FINDING_REPRODUCED','issue_id':'R7','actual_function':'finalize_pr938_and_gate_next.verify_completed','authenticated_dependency_before_execution':False,'controlled_private_marker_executed_before_hash_rejection':True,'hash_guard_eventually_rejected':True,'rejection':reason,'external_operations':0,'actual_operational_main_called':False,'candidate_changed':False}
print(json.dumps(result))
