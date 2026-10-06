from pathlib import Path
import subprocess,json,hashlib,datetime,sys,platform
out=Path(__file__).resolve().parent
pin=out/'original_pin'; work=out/'ignoredtmp/verify_runs';work.mkdir(parents=True,exist_ok=True)
source=(pin/'verify.py').read_bytes();cases=[('default_runtime_initial',sys.executable,source),('system_python_repaired','/usr/bin/python3',source),('corrupt_hyperbolic_trace','/usr/bin/python3',source.replace(b"(A*B).trace()==6",b"(A*B).trace()==5")),('corrupt_generator_determinant','/usr/bin/python3',source.replace(b"[[1,2],[0,1]]",b"[[2,2],[0,1]]"))]
ledger=[]
for name,runtime,b in cases:
 d=work/name;d.mkdir(exist_ok=True);(d/'verify.py').write_bytes(b)
 v=subprocess.run([runtime,'-c','import sys;print(sys.version)'],capture_output=True,text=True)
 c=subprocess.run([runtime,str(d/'verify.py')],cwd=d,capture_output=True,text=True)
 entry={'case':name,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'runtime_path':runtime,'runtime_version':v.stdout,'source_sha256':hashlib.sha256(b).hexdigest(),'exact_original_bytes':b==source,'exit_code':c.returncode,'stdout':c.stdout,'stderr':c.stderr}
 if c.returncode==0:
  result=json.loads(c.stdout);entry.update(result=result,exact_saved_json_equality=result==json.loads((pin/'verification.json').read_text()))
 ledger.append(entry)
(out/'ORIGINAL_VERIFY_EXECUTION.json').write_text(json.dumps(ledger,indent=2)+'\n')
print(json.dumps([{'case':x['case'],'exit':x['exit_code'],'original':x['exact_original_bytes'],'saved_json_equal':x.get('exact_saved_json_equality')} for x in ledger],indent=2))
