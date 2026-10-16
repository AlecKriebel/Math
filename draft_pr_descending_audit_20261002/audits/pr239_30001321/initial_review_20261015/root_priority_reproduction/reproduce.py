from pathlib import Path
from datetime import datetime,timezone
import subprocess,json,hashlib,shutil,os
D=Path('/Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr239_30001321/initial_review_20261015')
R=D/'root_priority_reproduction';R.mkdir(exist_ok=False)
res=[]
for label,program,args in [
 ('historical',D/'priority_historical_01/implication_checks.py',[]),
 ('recent_integrity',D/'priority_recent_01/VERIFY_AUDIT.py',[]),
 ('local_limit_integrity',D/'priority_local_limit_01/validate_lane.py',[])]:
 W=R/label;W.mkdir()
 runpath=program
 if label=='historical':
  runpath=W/program.name;shutil.copy2(program,runpath);assert runpath.read_bytes()==program.read_bytes()
 start=datetime.now(timezone.utc).isoformat();r=subprocess.run(['python3','-I','-B',str(runpath)]+args,cwd=W,capture_output=True,timeout=300,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
 (W/'stdout.json').write_bytes(r.stdout);(W/'stderr.txt').write_bytes(r.stderr)
 assert r.returncode==0 and not r.stderr,(label,r.returncode,r.stderr)
 out=json.loads(r.stdout)
 if label=='historical':assert r.stdout==(D/'priority_historical_01/implication_checks_receipt.json').read_bytes()
 else: assert out.get('status')=='PASS' or out.get('passed') is True
 receipt={'label':label,'start_utc':start,'end_utc':datetime.now(timezone.utc).isoformat(),'returncode':r.returncode,'empty_stderr':not r.stderr,'program_sha256':hashlib.sha256(program.read_bytes()).hexdigest(),'stdout_sha256':hashlib.sha256(r.stdout).hexdigest(),'output':out}
 (W/'ROOT_REPLAY_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n');res.append(receipt)
 print(json.dumps({'label':label,'PASS':True,'output':out}),flush=True)
(R/'ROOT_REPLAYS.json').write_text(json.dumps({'utc':datetime.now(timezone.utc).isoformat(),'status':'PASS','results':res},indent=2)+'\n')
shutil.copy2('/tmp/pr239_root_priority_checks_20261015.py',R/'reproduce.py')
