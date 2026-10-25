from pathlib import Path
from datetime import datetime,timezone
import subprocess,os,json,hashlib,shutil,zipfile
p=Path(__file__).resolve().parents[2];r=Path(__file__).resolve().parent;src=p/'sources';project=src/'published-source/simple-brace-counterexample-source-and-verification';cache=r/'cache';dst=cache/'replay-source';shutil.copytree(project,dst)
def inv(root):return {str(x.relative_to(root)):hashlib.sha256(x.read_bytes()).hexdigest() for x in root.rglob('*') if x.is_file()}
before=inv(project);mirror_before=inv(dst)
(cache/'tmp').mkdir(exist_ok=True)
py='/Users/alec/Documents/Math/research_website_catalogue_20261024/papers/22089373/reviews/adversarial/cache/venv/bin/python'
started=datetime.now(timezone.utc).isoformat()
with (r/'published_replay.json').open('w') as out,(r/'published_replay.stderr.log').open('w') as err:
 run=subprocess.run([py,'-B',str(dst/'verification/verify_all.py')],stdout=out,stderr=err,env={**os.environ,'TMPDIR':str(cache/'tmp'),'PYTHONDONTWRITEBYTECODE':'1'})
receipt={'started_utc':started,'completed_utc':datetime.now(timezone.utc).isoformat(),'exit_code':run.returncode,'python':py,'python_version':subprocess.check_output([py,'--version'],text=True).strip(),'program_sha256':hashlib.sha256((project/'verification/verify_all.py').read_bytes()).hexdigest(),'source_unchanged':inv(project)==before,'outer_mirror_unchanged':inv(dst)==mirror_before,'stdout_sha256':hashlib.sha256((r/'published_replay.json').read_bytes()).hexdigest(),'stderr_sha256':hashlib.sha256((r/'published_replay.stderr.log').read_bytes()).hexdigest()}
(r/'published_replay_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt,indent=2))
if run.returncode==0:
 data=json.loads((r/'published_replay.json').read_bytes());print(json.dumps({'status':data['status'],'controls':data['controls'],'runs':len(data['runs'])}))
else:print((r/'published_replay.stderr.log').read_text())
