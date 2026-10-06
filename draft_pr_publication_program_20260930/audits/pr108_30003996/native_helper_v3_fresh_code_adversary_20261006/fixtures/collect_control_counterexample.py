import sys
sys.dont_write_bytecode=True
from pathlib import Path
from bounded_process import BoundedRunner
from test_v3_guards import fixture_environment_policy
O=Path(__file__).resolve().parent.parent;F=O/'fixtures';P=O/'control_correspondence_actual_processes';P.mkdir(exist_ok=False)
policy={'max_process_count':2,'retain_bytes_per_stream':4096,'max_stdout_bytes':8192,'max_stderr_bytes':4096,'deadline_seconds':10,'terminate_grace_seconds':1}
r=BoundedRunner(P,F,policy,fixture_environment_policy())
for mode,extra in [('NORMAL',[]),('OPTIMIZED',['-O'])]:
 out,err,p=r.run([sys.executable,'-E','-S','-B',*extra,str(F/'control_correspondence_counterexample.py')],fixture=True)
 (P/(mode+'_STDOUT_FULL.bin')).write_bytes(out);(P/(mode+'_STDERR_FULL.bin')).write_bytes(err)
 print(mode,p['PID'],p['exit_code'],len(out),len(err))
