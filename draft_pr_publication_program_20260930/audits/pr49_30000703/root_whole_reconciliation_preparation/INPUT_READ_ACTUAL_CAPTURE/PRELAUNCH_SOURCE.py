from inspection_core import *
from datetime import datetime,timezone
F=Path(__file__).resolve().parent
q=collect();recheck(q)
q.update(schema='pr49-private-closed-whole-reconciliation-input-read/v1',status='PASS_SOURCE_PREPARATION_INPUTS_ONLY',actual_pid=os.getpid(),created_utc=datetime.now(timezone.utc).isoformat(),ROOT_record_authored=False,production_import_compile_execution=False,native_index_ref_remote_write=False)
(F/'INPUT_READ_RESULT.json').write_text(json.dumps(q,indent=2)+'\n')
print(json.dumps(dict(status=q['status'],actual_pid=os.getpid(),normalized_fixed_bindings=len(q['normalized_complete_fixed_bindings']),current_payload=1544,current_dependencies=1407,closed_whole_payload=127,whole_fixed=3083,dated_native4=4,ROOT_record_authored=False)))
