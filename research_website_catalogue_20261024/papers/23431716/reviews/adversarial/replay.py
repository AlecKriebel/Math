"""Replay only current mathematical finite controls, not archived verdict logic."""
from pathlib import Path
import subprocess,sys,json,hashlib,time
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parent
SOURCE=ROOT.parents[1]/'sources/published-source'
script=SOURCE/'code/run_checks.py'
out={'started_utc':datetime.now(timezone.utc).isoformat(),'runtime':sys.executable,'source_script_sha256':hashlib.sha256(script.read_bytes()).hexdigest(),'runs':[]}
for label,args,good in [('normal',[],True),('optimized',['-O'],True),('invalid',['--invalid'],False)]:
    cmd=[sys.executable,'-B']+(args if label=='optimized' else [])+[str(script)]+(args if label=='invalid' else [])
    start=time.monotonic();p=subprocess.run(cmd,capture_output=True,text=True)
    (ROOT/('replay-'+label+'.stdout.txt')).write_text(p.stdout)
    (ROOT/('replay-'+label+'.stderr.txt')).write_text(p.stderr)
    assert (p.returncode==0)==good
    if good:assert json.loads(p.stdout)['status']=='PASS'
    out['runs'].append({'label':label,'command':cmd,'seconds':time.monotonic()-start,'exit_code':p.returncode,'expected_success':good})
    (ROOT/'replay.json').write_text(json.dumps(out,indent=2)+'\n')
    print(label,p.returncode,flush=True)
out['completed_utc']=datetime.now(timezone.utc).isoformat();out['status']='PASS'
(ROOT/'replay.json').write_text(json.dumps(out,indent=2)+'\n')
