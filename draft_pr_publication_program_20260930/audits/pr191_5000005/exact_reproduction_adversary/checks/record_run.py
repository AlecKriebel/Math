"""Run an inspected local checker and preserve execution evidence in this effort only."""
import argparse, datetime, hashlib, json, pathlib, subprocess, sys
p=argparse.ArgumentParser()
p.add_argument('label');p.add_argument('script');p.add_argument('--opt',action='store_true')
a=p.parse_args()
base=pathlib.Path(__file__).resolve().parent.parent
script=(base/a.script).resolve()
if not script.is_relative_to(base):raise RuntimeError('script outside ownfolder')
argv=['/opt/homebrew/opt/python@3.14/bin/python3.14','-E','-S','-B','-P']+(['-O'] if a.opt else [])+[str(script)]
now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
sha=lambda b:hashlib.sha256(b).hexdigest()
start=now();r=subprocess.run(argv,cwd=script.parent,capture_output=True);end=now()
for name,data in [('stdout',r.stdout),('stderr',r.stderr)]:
 (base/'results'/f'{a.label}.{name}.txt').write_bytes(data)
report={'argv':argv,'cwd':str(script.parent),'utc_start':start,'utc_end':end,'exit':r.returncode,'script_sha256':sha(script.read_bytes()),'stdout_sha256':sha(r.stdout),'stderr_sha256':sha(r.stderr)}
try:report['result']=json.loads(r.stdout)
except (ValueError,UnicodeDecodeError):pass
(base/'results'/f'{a.label}.run.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
display=dict(report)
if 'result' in display:
 display['result']={k:v for k,v in display['result'].items() if k!='records'}
print(json.dumps(display,indent=2,sort_keys=True))
sys.exit(r.returncode)
