from pathlib import Path
import datetime as dt,json,hashlib,stat,subprocess,os
A=Path(__file__).resolve().parent;R=A.parents[2];D=A/'root_fresh_input_refresh_prelaunch';D.mkdir();(D/'SOURCE.py').write_bytes(Path(__file__).read_bytes())
o=json.loads((A/'ROOT_FRESH_ACCEPTANCE_INPUT_PREIMAGES.json').read_bytes());u=dt.datetime.now(dt.timezone.utc).isoformat();o.update(created_utc=u,reason_date_utc=u[:10],reason='Actual shared main after the concurrent audit published3edc0a6032bb05175c9e32a663f89130a703b430 provides a new clean integration point; prior stopped preflight is retained and no original source epoch or earlier fresh record is rewritten.',current_head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip())
for z in o['files']:
 p=R/z['path'];b=p.read_bytes();z.update(bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),worktree_mode=stat.S_IMODE(p.stat().st_mode))
with(A/'ROOT_FRESH_ACCEPTANCE_INPUT_PREIMAGES_V2.json').open('x')as f:json.dump(o,f,indent=2);f.write('\n')
print(json.dumps({'status':'FRESH_ACTUAL13_MAIN','pid':os.getpid(),'utc':u,'head':o['current_head']}))
