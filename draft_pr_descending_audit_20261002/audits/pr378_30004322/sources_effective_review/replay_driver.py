from pathlib import Path
import hashlib,json,os,subprocess,sys,time
from datetime import datetime,timezone
own=Path(__file__).resolve().parent
candidate=own.parent/'snapshot'/'problems/30004322_arrangement_seshadri'
outputs=own/'private_replay_outputs';outputs.mkdir(exist_ok=True)
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
commands=[(f'author_turn_{i}',candidate/f'check_turn_{i}.py',[],candidate/f'TURN_{i}_CHECKS.json') for i in range(1,6)]
commands += [('author_wrapper',candidate/'REPLAY_ALL.py',[],None),('old_independent_checks',candidate/'review'/'independent_checks.py',[],candidate/'review'/'INDEPENDENT_CHECKS.json'),('old_review_wrapper',candidate/'review'/'verify_review.py',['--author-dir',str(candidate)],None)]
receipts=[]
for name,path,args,expected in commands:
 start=time.monotonic();out=subprocess.run([sys.executable,str(path),*args],cwd=candidate,env=env,capture_output=True)
 (outputs/(name+'.stdout')).write_bytes(out.stdout);(outputs/(name+'.stderr')).write_bytes(out.stderr)
 rec={'name':name,'script_path':str(path),'command':[sys.executable,str(path),*args],'exit_code':out.returncode,'duration_seconds':time.monotonic()-start,'stdout_sha256':hashlib.sha256(out.stdout).hexdigest(),'stderr_sha256':hashlib.sha256(out.stderr).hexdigest(),'stdout_bytes':len(out.stdout),'stderr_bytes':len(out.stderr),'expected_receipt':str(expected) if expected else None,'complete_stdout_byte_equal':out.stdout==expected.read_bytes() if expected else None}
 if out.returncode==0:rec['complete_parsed_stdout']=json.loads(out.stdout)
 receipts.append(rec)
 (own/'replay_receipt.json').write_text(json.dumps({'started_at_utc':datetime.now(timezone.utc).isoformat(),'runtime':sys.version,'sympy_version':__import__('sympy').__version__,'candidate_source_directory_present':(candidate/'sources').is_dir(),'results':receipts},indent=2)+'\n')
 print(name,out.returncode,rec['complete_stdout_byte_equal'],rec['duration_seconds'],flush=True)
 assert out.returncode==0,name
 if expected:assert rec['complete_stdout_byte_equal'],name
print('REPLAY COMPLETE',flush=True)
