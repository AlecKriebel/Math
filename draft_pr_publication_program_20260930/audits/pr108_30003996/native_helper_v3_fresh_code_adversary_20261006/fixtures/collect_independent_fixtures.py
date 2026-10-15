import sys
sys.dont_write_bytecode=True
from pathlib import Path
import json,os,datetime
from bounded_process import BoundedRunner
from test_v3_guards import fixture_environment_policy
D=Path(__file__).resolve().parent;O=D.parent
policy={'max_process_count':4,'retain_bytes_per_stream':4096,'max_stdout_bytes':8192,'max_stderr_bytes':16384,'deadline_seconds':30,'terminate_grace_seconds':1}
output=O/'actual_fixture_processes';output.mkdir(exist_ok=False)
runner=BoundedRunner(output,D,policy,fixture_environment_policy());records=[]
for mode,extra in [('NORMAL',[]),('OPTIMIZED',['-O'])]:
 out,err,r=runner.run([sys.executable,'-E','-S','-B',*extra,str(D/'offline_adversary.py')],fixture=True,allow_failure=True)
 (output/(mode+'_STDOUT_FULL.bin')).write_bytes(out);(output/(mode+'_STDERR_FULL.bin')).write_bytes(err)
 records.append({'mode':mode,'record':r,'stdout_returned_bytes':len(out),'stderr_returned_bytes':len(err)})
 print(mode,r['PID'],r['exit_code'],r['termination_reason']);print(err.decode())
(O/'FIXTURE_PROCESS_RECEIPTS.json').write_text(json.dumps({'actual_operator_PID':os.getpid(),'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'records':records,'fixture_only':True,'native_or_service_calls':0},indent=2)+'\n')
