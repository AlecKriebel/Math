"""Capture independent replays after a truthful ENOSPC interruption."""
from pathlib import Path
import datetime,hashlib,json,subprocess,sys
A=Path(__file__).resolve().parent;first=A/'root_independent_replays'
(A/'ROOT_REPLAY_INTERRUPTION_01.json').write_text(json.dumps({'UTC':datetime.datetime.now(datetime.UTC).isoformat(),'failed_generation':first.name,'failure':'ENOSPC while saving optimized exact-family stdout; driver did not complete all6 replays or save its aggregate receipt. Existing partial files retained; no completed Root baseline claimed. A subsequent heredoc retry failed before Python started.','existing_files':[{'path':p.name,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in first.iterdir() if p.is_file()],'repair':'Only own regenerable derivatives removed; fresh generation02 evidence capture.'},indent=2)+'\n')
out=A/'root_independent_replays_02';out.mkdir(exist_ok=False);rows=[]
for rel in ['exact_reproduction_adversary/independent_exact.py','global_geometry_adversary/EXACT_WITNESS_REPLAY.py','literal_source_adversary/independent_double_pentagon_check.py']:
 p=A/rel
 for optimize in [False,True]:
  label=p.parent.name+('_optimized' if optimize else '_normal');argv=[sys.executable,'-E','-S','-B','-P']+(['-O'] if optimize else [])+[str(p)];before=hashlib.sha256(p.read_bytes()).hexdigest()
  start=datetime.datetime.now(datetime.UTC).isoformat();r=subprocess.run(argv,capture_output=True);end=datetime.datetime.now(datetime.UTC).isoformat()
  rec={'source':rel,'source_SHA256':before,'optimized':optimize,'start_UTC':start,'end_UTC':end,'argv':argv,'exit_code':r.returncode,'stdout_SHA256':hashlib.sha256(r.stdout).hexdigest(),'stderr_SHA256':hashlib.sha256(r.stderr).hexdigest()}
  (out/(label+'.receipt.json')).write_text(json.dumps(rec,indent=2)+'\n');(out/(label+'.stdout.json')).write_bytes(r.stdout);(out/(label+'.stderr')).write_bytes(r.stderr)
  if r.returncode:raise RuntimeError(rel+' '+r.stderr.decode()[:500])
  json.loads(r.stdout)
  if hashlib.sha256(p.read_bytes()).hexdigest()!=before:raise RuntimeError('Source drift')
  rows.append(rec)
for i in [0,2,4]:
 if rows[i]['stdout_SHA256']!=rows[i+1]['stdout_SHA256']:raise RuntimeError('Optimization output difference')
(out/'ACTUAL_REPLAY_RECEIPTS.json').write_text(json.dumps(rows,indent=2)+'\n')
print(json.dumps({'actual_independent_replays':6,'all_passed':True,'source_integrity':True,'mode_output_hashes_match':True,'generation':out.name}))

