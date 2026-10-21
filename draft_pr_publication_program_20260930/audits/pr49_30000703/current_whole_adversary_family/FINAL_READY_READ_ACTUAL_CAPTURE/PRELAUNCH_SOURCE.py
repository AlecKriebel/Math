from review_common import *
from datetime import datetime,timezone
q=inspect_complete()
assert not (F/'SELF_MANIFEST.json').exists()
out=dict(schema='pr49-whole-final-ready-private-read/v1',status='PASS_READY_WAIT_ROOT',actual_pid=os.getpid(),created_utc=datetime.now(timezone.utc).isoformat(),complete_external_rows_read=len(q['external_rows']),retained_actual_captures=q['captures'],complete_own_rows=[ref(F/n) for n in q['owned_files']],future_acceptance_approved=False,own_closure_executed=False,production_execution=False,own_row_observation_is_live_capture_prefix=True,containing_actual_capture_unfinished_during_observation=True,closure_must_read_complete_postexit_capture=True)
(F/'FINAL_READY_READ_RESULT.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(dict(status=out['status'],actual_pid=os.getpid(),external_rows=len(q['external_rows']),retained_caps=len(q['captures']),own_rows=len(q['owned_files']))))
