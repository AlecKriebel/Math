"""MIT licensed. Capture authorized authored preparation/check only, never ROOT helpers."""
import argparse, datetime, hashlib, json, os, pathlib, subprocess, sys
R=pathlib.Path(__file__).resolve().parent
ap=argparse.ArgumentParser();ap.add_argument('step',choices=['notes','admin']);a=ap.parse_args()
op=R/('prepare_source_notes.py' if a.step=='notes' else 'verify_intake_evidence.py')
cap=R/'captures'/a.step;cap.mkdir(exist_ok=False)
ob=op.read_bytes();cb=pathlib.Path(__file__).read_bytes()
(cap/'operator_prelaunch.py').write_bytes(ob);(cap/'controller_prelaunch.py').write_bytes(cb)
s=datetime.datetime.now(datetime.timezone.utc).isoformat();argv=[sys.executable,'-E','-B',str(op)]
p=subprocess.Popen(argv,cwd=R,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
out,err=p.communicate();e=datetime.datetime.now(datetime.timezone.utc).isoformat()
(cap/'stdout.bin').write_bytes(out);(cap/'stderr.bin').write_bytes(err)
def sha(b):return hashlib.sha256(b).hexdigest()
j={'schema':'pr62-owned-preparation-capture/v1','actual_execution':True,'step':a.step,
 'controller_pid':os.getpid(),'pid':p.pid,'argv':argv,'cwd':str(R),
 'started_utc':s,'finished_utc':e,'exit_code':p.returncode,
 'operator_prelaunch_sha256':sha(ob),'controller_prelaunch_sha256':sha(cb),
 'operator_unchanged':op.read_bytes()==ob,
 'local_code_imports':'Python standard library only; operator and controller bodies saved before launch.',
 'Python_environment_ignored':True,'no_O_flag':True,
 'stdout':{'path':'stdout.bin','bytes':len(out),'sha256':sha(out)},
 'stderr':{'path':'stderr.bin','bytes':len(err),'sha256':sha(err)},
 'ROOT_helper_run':False,'new_math_or_audit_credit':0}
(cap/'CAPTURE.json').write_text(json.dumps(j,sort_keys=True,indent=2)+'\n')
print(json.dumps({'step':a.step,'pid':p.pid,'controller_pid':os.getpid(),
 'exit_code':p.returncode,'stdout_bytes':len(out),'stderr_bytes':len(err)},sort_keys=True))
sys.exit(p.returncode)
