"""Log the exact argv, timestamp, return code and raw textual child output."""
from pathlib import Path
import datetime,json,os,subprocess,sys,time
here=Path(__file__).resolve().parent.parent
label=sys.argv[1];argv=sys.argv[2:]
if not label.replace('_','').isalnum():raise ValueError('label')
env=dict(os.environ);env.update(TMPDIR=str(here/'tmp'),TMP=str(here/'tmp'),TEMP=str(here/'tmp'),PYTHONDONTWRITEBYTECODE='1')
start=datetime.datetime.now(datetime.timezone.utc).isoformat();t=time.monotonic()
try:
 p=subprocess.run(argv,cwd=here,env=env,capture_output=True,timeout=300)
 rc,out,err=p.returncode,p.stdout,p.stderr
except subprocess.TimeoutExpired as e:rc,out,err='TIMEOUT',e.stdout or b'',e.stderr or b''
result=dict(label=label,launch_utc=start,elapsed_seconds=time.monotonic()-t,argv=argv,cwd=str(here),returncode=rc,
            stdout=out.decode(errors='replace'),stderr=err.decode(errors='replace'),
            temp_environment={k:env[k] for k in ['TMPDIR','TMP','TEMP']})
(here/'receipts'/(label+'_launch.json')).write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
sys.exit(0 if rc==0 else 1)
