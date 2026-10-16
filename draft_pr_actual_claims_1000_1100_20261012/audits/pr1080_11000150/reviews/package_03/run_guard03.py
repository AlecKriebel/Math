import subprocess,sys,json,os,datetime,time,shutil
from pathlib import Path
h=Path(__file__).resolve().parent
temp=h/'scratch/guard-temp';temp.mkdir(exist_ok=True)
env=dict(os.environ,TMPDIR=str(temp))
for optimized in [False,True]:
    cmd=[sys.executable,'-I','-B']+(['-O'] if optimized else [])+[str(h/'scratch/clean_check/verification_kit/output_guard_checks.py')]
    t=time.monotonic();utc=datetime.datetime.now(datetime.timezone.utc).isoformat()
    r=subprocess.run(cmd,capture_output=True,text=True,env=env,timeout=180)
    row={'utc':utc,'argv':cmd,'tempdir':str(temp),'returncode':r.returncode,'stdout':r.stdout,'stderr':r.stderr,'elapsed_seconds':time.monotonic()-t,'free_bytes_after':shutil.disk_usage(h).free}
    with (h/'FINAL_GUARD_COMMAND_RECEIPTS.jsonl').open('a') as f:f.write(json.dumps(row)+'\n')
    if r.returncode:raise RuntimeError(json.dumps(row))
print('PASS two actual output_guard_checks invocations, each internally normal and optimized')
