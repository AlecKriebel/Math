from pathlib import Path
import subprocess,sys,os,signal,time,json,hashlib
P=Path(__file__).resolve().parent
root=P.parents[3]
runs=[('independent',str(root/'tmp/shared-math-runtime/bin/python'),[str(P/'independent_falsification.py')]),('supplied_kit',sys.executable,['-I','-B',str(P.parents[1]/'sources/support/scripts/verify_kit.py'),'--archive',str(P.parents[1]/'sources/pr1032_supportkit_v1.1.zip')])]
record=[]
for name,python,args in runs:
    start=time.monotonic()
    proc=subprocess.Popen([python,*args],stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True)
    timeout=False
    try:
        out,err=proc.communicate(timeout=25)
    except subprocess.TimeoutExpired:
        timeout=True
        os.killpg(proc.pid,signal.SIGKILL)
        out,err=proc.communicate()
    finally:
        try:os.killpg(proc.pid,signal.SIGKILL)
        except ProcessLookupError:pass
    (P/(name+'_stdout.txt')).write_bytes(out)
    (P/(name+'_stderr.txt')).write_bytes(err)
    record.append({'name':name,'timeout_seconds':25,'timed_out':timeout,'returncode':proc.returncode,'seconds':round(time.monotonic()-start,4),'stdout_sha256':hashlib.sha256(out).hexdigest(),'stderr_bytes':len(err),'cleanup':'isolated process group SIGKILL attempted in finally; absent group is expected on normal completion'})
(P/'bounded_check_runs.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record,indent=2))
