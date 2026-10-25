from pathlib import Path
from datetime import datetime,timezone
import subprocess,sys,hashlib,json,time,os

ROOT=Path(__file__).resolve().parent
CACHE=ROOT/'cache/replay-v2'
scripts=['verify_release_metadata.py','verify_construction.py','cleanroom/verify_v1_cleanroom.py','family/verify_family.py','strengthening/clean_rates_stability_verifier.py','minimality/verify_complexity_arithmetic.py','audit_v2/verify_v2_independent.py','source/verify_v2_claims.py']
results=[]
for i,rel in enumerate(scripts):
    start=datetime.now(timezone.utc).isoformat();clock=time.monotonic()
    with (ROOT/f'replay-{i+1:02d}.stdout.txt').open('w') as out,(ROOT/f'replay-{i+1:02d}.stderr.txt').open('w') as err:
        proc=subprocess.run([sys.executable,'-B',str(CACHE/rel)],cwd=CACHE,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'),stdout=out,stderr=err)
    result={'script':rel,'script_sha256':hashlib.sha256((CACHE/rel).read_bytes()).hexdigest(),'started_utc':start,'completed_utc':datetime.now(timezone.utc).isoformat(),'seconds':time.monotonic()-clock,'exit_code':proc.returncode,'stdout':f'replay-{i+1:02d}.stdout.txt','stderr':f'replay-{i+1:02d}.stderr.txt'}
    results.append(result)
    (ROOT/'submitted-replay.json').write_text(json.dumps({'runtime':sys.executable,'mode':'Existing exact pinned dependencies; all eight published checks run individually, no pip/environment installation or source edits.','results':results,'complete':len(results)==len(scripts),'status':'PASS' if len(results)==len(scripts) and all(x['exit_code']==0 for x in results) else 'IN_PROGRESS_OR_FAILED'},indent=2)+'\n')
    print(rel,proc.returncode,round(result['seconds'],2),flush=True)
    if proc.returncode:raise SystemExit(proc.returncode)
