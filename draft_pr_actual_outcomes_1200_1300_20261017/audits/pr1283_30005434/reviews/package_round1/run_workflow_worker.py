#!/usr/bin/env python3
"""Run exact frozen worker with its report root redirected in memory to our scratch.
All external socket connections and direct service subprocesses are forbidden.
"""
from pathlib import Path
import importlib.util,json,socket,subprocess,sys,time
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent
A=R.parent.parent
path=A/'publication/workflow_regression.py'
spec=importlib.util.spec_from_file_location('package_round1_frozen_workflow',path)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
m.REPORT_ROOT=R/'_local/workflow_tooling'
def blocked_socket(*args,**kwargs):raise RuntimeError('External sockets forbidden in package review')
socket.socket.connect=blocked_socket
original_run=subprocess.run
original_output=subprocess.check_output
def check(args):
 if isinstance(args,(list,tuple)) and args and Path(str(args[0])).name in {'gh','gws','git'}:raise RuntimeError('Unmocked external service/Git command forbidden: '+str(args[0]))
def run(args,*a,**kw):check(args);return original_run(args,*a,**kw)
def output(args,*a,**kw):check(args);return original_output(args,*a,**kw)
subprocess.run=run;subprocess.check_output=output
start=time.monotonic();result=m.worker()
result['independent_run_safeguards']={'network_connections_blocked':True,'direct_git_gh_gws_subprocesses_blocked':True,'only_runtime_override':'REPORT_ROOT redirected to reviewer-owned _local/workflow_tooling','elapsed_seconds':round(time.monotonic()-start,3)}
print(json.dumps(result,sort_keys=True))
