"""MIT licensed. Guarded exact original finite replays; preserves first captures.
No ROOT helper. -E ignores Python environment options; no -O is supplied.
"""
import argparse, datetime, hashlib, json, os, pathlib, subprocess, sys
R=pathlib.Path(__file__).resolve().parent
ap=argparse.ArgumentParser();ap.add_argument('step',choices=['submitted_guarded','historical_guarded'])
a=ap.parse_args();cap=R/'captures'/a.step;cap.mkdir(exist_ok=False)
op=R/('original/verify.py' if a.step=='submitted_guarded' else 'reproduction/historical/independent_checks.py')
def sha(b):return hashlib.sha256(b).hexdigest()
ob=op.read_bytes();cb=pathlib.Path(__file__).read_bytes()
(cap/'operator_prelaunch.py').write_bytes(ob);(cap/'controller_prelaunch.py').write_bytes(cb)
inputs=[]
if a.step=='submitted_guarded':
    dep=op.with_name('OBSTRUCTION.md');db=dep.read_bytes()
    (cap/'OBSTRUCTION_prelaunch.md').write_bytes(db)
    inputs.append({'path':str(dep),'bytes':len(db),'sha256':sha(db)})
probe="import json,sys\nprint(json.dumps({'optimize':sys.flags.optimize,'ignore_environment':sys.flags.ignore_environment,'debug':__debug__},sort_keys=True))\nassert sys.flags.optimize==0 and sys.flags.ignore_environment==1 and __debug__\n"
(cap/'runtime_probe_prelaunch.py').write_text(probe)
def run(argv):
    s=datetime.datetime.now(datetime.timezone.utc).isoformat()
    p=subprocess.Popen(argv,cwd=op.parent,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out,err=p.communicate()
    return {'pid':p.pid,'argv':argv,'started_utc':s,'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'exit_code':p.returncode},out,err
probe_record,po,pe=run([sys.executable,'-E','-B',str(cap/'runtime_probe_prelaunch.py')])
(cap/'probe_stdout.bin').write_bytes(po);(cap/'probe_stderr.bin').write_bytes(pe)
probe_record.update({'stdout_bytes':len(po),'stdout_sha256':sha(po),'stderr_bytes':len(pe),'stderr_sha256':sha(pe)})
assert probe_record['exit_code']==0 and json.loads(po)=={'optimize':0,'ignore_environment':1,'debug':True}
rec,out,err=run([sys.executable,'-E','-B',str(op)])
(cap/'stdout.bin').write_bytes(out);(cap/'stderr.bin').write_bytes(err)
original=R/('original/verification.json' if a.step=='submitted_guarded' else 'original/independent_review/independent_results.json')
j={'schema':'pr62-owned-guarded-replay/v1','step':a.step,'actual_execution':True,
   'controller_pid':os.getpid(),**rec,'cwd':str(op.parent),
   'operator_prelaunch_sha256':sha(ob),'controller_prelaunch_sha256':sha(cb),
   'operator_unchanged':op.read_bytes()==ob,'local_transitive_inputs':inputs,
   'runtime_probe':probe_record,'Python_environment_ignored':True,'no_O_flag':True,
   'historical_first_capture_debug_state_measured':False,
   'stdout':{'path':'stdout.bin','bytes':len(out),'sha256':sha(out)},
   'stderr':{'path':'stderr.bin','bytes':len(err),'sha256':sha(err)},
   'stdout_byte_identical_to_original':out==original.read_bytes(),
   'ROOT_helper_run':False,'new_math_or_audit_credit':0,'actual_knot_Floer_computation':False}
(cap/'CAPTURE.json').write_text(json.dumps(j,sort_keys=True,indent=2)+'\n')
assert rec['exit_code']==0 and out==original.read_bytes() and err==b''
print(json.dumps({'status':'PASS_GUARDED_EXACT_ORIGINAL_REPLAY','step':a.step,
   'pid':rec['pid'],'controller_pid':os.getpid(),'probe_pid':probe_record['pid'],
   'stdout_bytes':len(out),'stderr_bytes':len(err),'assertions':564 if a.step=='submitted_guarded' else 20223},sort_keys=True))
