#!/usr/bin/env python3
"""Exercise real second invocations after successful or uncertain mocked actions."""
import argparse, datetime, hashlib, json, os, re, subprocess, sys
from pathlib import Path
from audit_inputs import OWN, check
from run_controls import cases, read, write

def main():
 parser=argparse.ArgumentParser()
 parser.add_argument('--run-name',default=None)
 args=parser.parse_args()
 if args.run_name is not None:check(re.fullmatch('[a-z][a-z0-9_]{0,40}',args.run_name) is not None,'invalid private run name')
 runs_root=OWN/'private_cases'/('complete_run' if args.run_name is None else 'reproduction_'+args.run_name)
 results=[]
 for mode in ['normal','optimized']:
  for name in ['baseline_apply','uncertain_patch_applied','uncertain_patch_not_applied','patch_bad_json_applied','wrong_blob_readback']:
   index=cases().index(name);root=runs_root/(mode+'_'+str(index))
   case=root/'program/audits/pr458_20000693'; statep=root/'GH_STATE.json'
   before=read(statep);check((case/'STATUS_REPAIR_OPERATION.json').exists(),'missing retained operation')
   env=dict(os.environ);env['PATH']=str(root/'bin')+os.pathsep+env.get('PATH','');env['PRIVATE_GH_STATE']=str(statep);env['PYTHONDONTWRITEBYTECODE']='1'
   if mode=='optimized':env['PYTHONOPTIMIZE']='1'
   else:env.pop('PYTHONOPTIMIZE',None)
   p=subprocess.run([sys.executable,str(root/'program/repair_pr458_status.py'),'--apply'],capture_output=True,text=True,env=env,cwd=root,timeout=30)
   (root/'repeat_stdout.txt').write_text(p.stdout);(root/'repeat_stderr.txt').write_text(p.stderr)
   after=read(statep)
   check(p.returncode!=0 and 'Prior operation: no repeated mutation' in p.stderr,'repeat guard')
   check(before==after,'repeat reached mocked API')
   results.append({'mode':mode,'initial_case':name,'returncode':p.returncode,'guard':'Prior operation: no repeated mutation','mock_api_calls_added':0,'mock_ref_patches_added':0,'stderr_sha256':hashlib.sha256(p.stderr.encode()).hexdigest()})
 write(runs_root/'REPRODUCTION_REPEATS.json' if args.run_name is not None else OWN/'REPEAT_CONTROLS.json',{'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_repeat_subprocesses':len(results),'all_reject_before_any_API':True,'runs':results})
 print(json.dumps({'repeat_subprocesses':len(results),'all_reject_before_any_API':True},indent=2))
if __name__=='__main__':main()
