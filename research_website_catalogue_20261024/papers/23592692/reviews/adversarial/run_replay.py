from pathlib import Path
import subprocess,json,shutil,datetime,hashlib,os
r=Path(__file__).resolve().parent;p=r.parent.parent
copy=r/'replay-copy';shutil.copytree(p/'sources/published-source',copy)
out=r/'replays';out.mkdir(exist_ok=True);tmp=r/'temporary';tmp.mkdir(exist_ok=True)
seal=hashlib.sha256((copy/'SOURCE_MANIFEST.json').read_bytes()).hexdigest()
env=os.environ.copy();env.update(PYTHONDONTWRITEBYTECODE='1',PYTHONHASHSEED='0',TMPDIR=str(tmp))
jobs=[('all-controls',['python3','-B','verification/run_checks.py','--manifest-sha256',seal],0),('false-manifest-anchor',['python3','-B','verification/run_checks.py','--manifest-sha256','0'*64],1)]
receipts=[]
for name,command,wanted in jobs:
    start=datetime.datetime.now(datetime.timezone.utc).isoformat()
    z=subprocess.run(command,cwd=copy,env=env,capture_output=True,timeout=180)
    (out/(name+'.stdout')).write_bytes(z.stdout);(out/(name+'.stderr')).write_bytes(z.stderr)
    if z.returncode!=wanted:raise RuntimeError((name,z.stderr[-2000:]))
    rec={'name':name,'command':command,'cwd':str(copy),'started_utc':start,'ended_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'returncode':z.returncode,'stdout_sha256':hashlib.sha256(z.stdout).hexdigest(),'stderr_sha256':hashlib.sha256(z.stderr).hexdigest()}
    if wanted==0:
        d=json.loads(z.stdout);rec.update(status=d['status'],source_payloads=d['source_payloads'],mode_suite_executions=len(d['runs']),all_source_and_copy_bytes_unchanged=d['all_source_and_copy_bytes_unchanged'])
    else:
        if b'external manifest anchor' not in z.stderr:raise RuntimeError('wrong rejection')
        rec['expected_guard_rejection']=True
    receipts.append(rec);print(json.dumps(rec),flush=True)
(r/'replay-receipts.json').write_text(json.dumps({'status':'PASS','unmodified_copy':str(copy),'receipts':receipts,'interpretation':'Mathematical finite controls and byte custody only; historical priority assertions mechanically authenticated, not independently adopted or certified.'},indent=2)+'\n')
