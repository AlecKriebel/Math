"""Run only statically reviewed submitted files, copied byte-for-byte into owned cache."""
from pathlib import Path
import datetime,hashlib,json,subprocess,sys
here=Path(__file__).resolve().parent; root=here.parent.parent
source=root/'sources/cache/extracted/verification'; target=here/'cache/quarantined_replay'
target.mkdir(parents=True,exist_ok=True)
reports=[]
for name in ('ball_exact_controls.py','kernel_controls.py','spectral_illustration.py'):
 raw=(source/name).read_bytes(); work=target/name.removesuffix('.py'); work.mkdir(exist_ok=True); (work/'private').mkdir(exist_ok=True)
 script=work/name; script.write_bytes(raw)
 assert script.read_bytes()==raw
 command=[sys.executable,str(script)]
 if name=='kernel_controls.py': command+=['--output',str(work/'result.json')]
 start=datetime.datetime.now(datetime.timezone.utc).isoformat()
 done=subprocess.run(command,cwd=work,text=True,capture_output=True,timeout=180)
 (work/'stdout.txt').write_text(done.stdout); (work/'stderr.txt').write_text(done.stderr)
 row={'script':name,'sha256':hashlib.sha256(raw).hexdigest(),'copy_byte_identical':True,'start_utc':start,'end_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'exit_code':done.returncode,'stdout_path':str((work/'stdout.txt').relative_to(here)),'stderr_path':str((work/'stderr.txt').relative_to(here))}
 if done.returncode==0:
  data=json.loads(done.stdout)
  if name=='ball_exact_controls.py':
   full=json.loads((work/'private/exact_controls_output.json').read_text()); row['exact_count']=full['count']; row['all_pass']=full['all_passed']; row['negative_trace_coefficient']=data['negative_trace_coefficient']
  elif name=='kernel_controls.py': row['exact']=data['exact']; row['illustration_rows']={'static':len(data['static_gaussian']),'dynamic':len(data['dynamic_nested'])}
  else: row['all_pass']=data['all_assertions_passed']; row['illustrative_rows']=len(data['defective_cluster_rows'])
 reports.append(row)
 if done.returncode: raise RuntimeError(row)
import numpy,sympy
out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'python':sys.version,'numpy':numpy.__version__,'sympy':sympy.__version__,'method':'Full static inspection before execution; fresh analytic derivation and independent controls completed first. Only owned byte-identical copies executed; no wrapper or prior expected/verdict result was read.','replays':reports,'limitation':'Finite exact identities and floating diagnostics support, but do not replace, the universal written proof.'}
(here/'replay_receipt.json').write_text(json.dumps(out,indent=2)+'\n'); print(json.dumps(out,indent=2))
