from pathlib import Path
import subprocess,sys,os,json,hashlib,datetime
D=Path(__file__).resolve().parents[1]
P=D.parent/'scope_repaired_snapshot/problems/30003853_thompson_subgroup_abelianization'
O=D/'replays';O.mkdir(exist_ok=True)
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
rs=[]
for name,args,cwd in [('author',[sys.executable,str(P/'REPLAY_ALL.py')],P),('historical_independent',[sys.executable,str(P/'independent_review/independent_check.py')],P/'independent_review'),('current_publication',[sys.executable,str(P/'verify_publication.py')],P)]+[(f'turn{t}',[sys.executable,str(P/f'verify_turn{t}.py')],P) for t in range(1,6)]:
 r=subprocess.run(args,cwd=cwd,env=env,capture_output=True)
 (O/(name+'.stdout.txt')).write_bytes(r.stdout);(O/(name+'.stderr.txt')).write_bytes(r.stderr)
 q={'name':name,'returncode':r.returncode,'stdout_bytes':len(r.stdout),'stdout_sha256':hashlib.sha256(r.stdout).hexdigest(),'stderr_bytes':len(r.stderr)}
 if name.startswith('turn'):q['exact_historical_stdout']=r.stdout==(P/(name.upper().replace('TURN','TURN_')+'_CHECKS.json')).read_bytes()
 if name=='historical_independent':q['exact_historical_stdout']=r.stdout==(P/'independent_review/INDEPENDENT_CHECKS.json').read_bytes()
 if name=='author':
  old=json.loads((P/'FINAL_REPLAY.json').read_text());old['local_source_bindings']=0;q['historical_after_explicit_source_qualification']=json.loads(r.stdout)==old
 rs.append(q)
 print(name, 'exit',r.returncode,'stdout',r.stdout.decode().strip(),'stderr',r.stderr.decode().strip())
(O/'FULL_REPLAY.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'candidate_head':'83862044e1bb334d582b2082bf8b63c6b0eee4c5','PYTHONDONTWRITEBYTECODE':True,'runs':rs},indent=2)+'\n')
assert all(r['returncode']==0 for r in rs)
assert all(r.get('exact_historical_stdout',True) for r in rs)
