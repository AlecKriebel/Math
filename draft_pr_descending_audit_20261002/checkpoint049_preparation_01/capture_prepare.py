"""Future outside GET-only planner recorder. Creates no authority or grant."""
from pathlib import Path
import argparse,importlib.util,json,sys
B=Path(__file__).resolve().parent
if __name__=='__main__':
    if not(sys.flags.ignore_environment and sys.dont_write_bytecode and not sys.flags.optimize):raise RuntimeError('Python -E -B without optimization')
    q=argparse.ArgumentParser();q.add_argument('--expected-main',required=True);q.add_argument('--sequence',required=True);a=q.parse_args()
    if len(a.sequence)!=2 or not a.sequence.isdigit():raise RuntimeError('literal two-digit new sequence')
    spec=importlib.util.spec_from_file_location('checkpoint049_capture',B/'native_capture.py');N=importlib.util.module_from_spec(spec);spec.loader.exec_module(N)
    run=B/('prepare_capture_'+a.sequence);run.mkdir(exist_ok=False)
    argv=[str(Path(sys.executable).resolve()),'-E','-B',str(B/'checkpoint049.py'),'prepare','--run',str(B/('read_only_prepare_'+a.sequence)),'--expected-main',a.expected_main]
    out=N.call(run,'actual_prepare',argv,B,timeout=600)
    print(json.dumps(dict(status='ACTUAL_GETONLY_PLAN_PARENT_COMPLETED_NOT_ROOT_ACCEPTED',outer_execution=N.pin(run/'private/native/actual_prepare/execution.json'),child_output=json.loads(out))))
