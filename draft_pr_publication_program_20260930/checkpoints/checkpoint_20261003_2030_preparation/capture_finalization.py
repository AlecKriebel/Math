"""Capture only the own SOURCE finalizer; literal output excluded from fixed SOURCE."""
import os,subprocess,sys
from common import *
EXCLUDED_FINALIZATION_ROOT = 'actual_source_finalization_capture'
def main():
    d=N/EXCLUDED_FINALIZATION_ROOT;d.mkdir(exist_ok=False)
    op=N/'freeze_source.py';exclusive(d/'prelaunch_operator.py',op.read_bytes())
    exclusive(d/'prelaunch_controller.py',Path(__file__).read_bytes())
    inputs=[plain_ref(N/v) for v in ['common.py','selection.py','SCOPE.json','SOURCE_VERIFICATION.json']]
    exclusive(d/'PRELAUNCH_INPUTS.json',encoded(inputs))
    argv=[sys.executable,'-B',str(op)];start=now()
    c=subprocess.Popen(argv,cwd=R,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out,err=c.communicate();end=now();exclusive(d/'stdout.bin',out);exclusive(d/'stderr.bin',err)
    record=dict(schema='checkpoint1915-actual-source-finalization/v1',actual_execution=True,completed=True,operator_role='SOURCE_PREPARER',
      pid=c.pid,argv=argv,cwd=str(R),started_utc=start,finished_utc=end,exit_code=c.returncode,
      prelaunch_operator=plain_ref(d/'prelaunch_operator.py'),prelaunch_controller=plain_ref(d/'prelaunch_controller.py'),
      prelaunch_inputs=plain_ref(d/'PRELAUNCH_INPUTS.json'),operator_unchanged=op.read_bytes()==(d/'prelaunch_operator.py').read_bytes(),
      inputs_unchanged=all(plain_ref(path(z['path']))==z for z in inputs),stdout=plain_ref(d/'stdout.bin'),stderr=plain_ref(d/'stderr.bin'),
      ROOT_execution_or_approval=False,production_helpers_executed=False,output_outside_fixed_SOURCE_but_inside_owned_folder=True)
    exclusive(d/'CAPTURE.json',encoded(record));print(encoded(record).decode(),end='');need(c.returncode==0,'Actual finalizer failed; full streams retained')
if __name__=='__main__':main()
