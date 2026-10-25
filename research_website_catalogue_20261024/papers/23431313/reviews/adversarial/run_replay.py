from pathlib import Path
from datetime import datetime,timezone
import os,subprocess,shutil,hashlib,json
r=Path(__file__).resolve().parent;p=r.parents[1];project=p/'sources/published-source';dst=r/'cache/replay-source';shutil.copytree(project,dst)
def inv(root):return {str(x.relative_to(root)):hashlib.sha256(x.read_bytes()).hexdigest() for x in root.rglob('*') if x.is_file()}
original=inv(project);mirror=inv(dst);runs=[]
py='/Users/alec/Documents/Math/research_website_catalogue_20261024/papers/22089373/reviews/adversarial/cache/venv/bin/python'
for mode,flags in [('normal',[]),('optimized',['-O']),('docstrings_removed',['-OO'])]:
 start=datetime.now(timezone.utc).isoformat();out=r/('published_replay_'+mode+'.json');err=r/('published_replay_'+mode+'.stderr.log')
 with out.open('w') as o,err.open('w') as e:
  z=subprocess.run([py,*flags,'-B',str(dst/'scripts/run_checks.py')],stdout=o,stderr=e,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
 value=json.loads(out.read_bytes()) if z.returncode==0 else None
 runs.append({'mode':mode,'started_utc':start,'completed_utc':datetime.now(timezone.utc).isoformat(),'exit_code':z.returncode,'result':value,'stderr':err.read_text(),'stdout_sha256':hashlib.sha256(out.read_bytes()).hexdigest()})
 if z.returncode:break
receipt={'python':py,'python_version':subprocess.check_output([py,'--version'],text=True).strip(),'program_sha256':hashlib.sha256((project/'scripts/run_checks.py').read_bytes()).hexdigest(),'runs':runs,'source_unchanged':inv(project)==original,'mirror_unchanged':inv(dst)==mirror,'status':'PASS' if len(runs)==3 and all(x['exit_code']==0 and x['result']['status']=='PASS' for x in runs) else 'FAIL'}
(r/'published_replay_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt,indent=2))
