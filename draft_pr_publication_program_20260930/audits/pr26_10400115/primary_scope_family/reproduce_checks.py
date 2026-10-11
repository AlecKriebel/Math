from pathlib import Path
import datetime, hashlib, json, shutil, subprocess, sys
P=Path(__file__).resolve().parent
S=P.parent/'source_snapshot'
R=P/'isolated_reproduction_v1'
if R.exists():raise SystemExit('Preserve existing run; do not overwrite.')
R.mkdir();(R/'review').mkdir()
receipts=[]
for script,receipt in [('verify.py','verification.json'),('review/independent_checks.py','review/independent_results.json')]:
 shutil.copy2(S/script,R/script)
 result=subprocess.run([sys.executable,str(R/script)],cwd=R,capture_output=True,text=True)
 (R/(Path(script).stem+'_stdout.txt')).write_text(result.stdout)
 (R/(Path(script).stem+'_stderr.txt')).write_text(result.stderr)
 produced=(R/receipt).read_bytes() if (R/receipt).exists() else b''
 old=(S/receipt).read_bytes()
 receipts.append({'script':script,'receipt':receipt,'exit':result.returncode,'python':sys.executable,'stdout_sha256':hashlib.sha256(result.stdout.encode()).hexdigest(),'script_sha256':hashlib.sha256((R/script).read_bytes()).hexdigest(),'recorded_receipt_sha256':hashlib.sha256(old).hexdigest(),'fresh_receipt_sha256':hashlib.sha256(produced).hexdigest(),'byte_identical':old==produced,'checks_result':json.loads(produced) if produced else None})
out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'read_only_source':str(S),'isolated_run':str(R),'results':receipts,'all_passed':all(x['exit']==0 and x['byte_identical'] for x in receipts)}
(P/'reproduction_receipt.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
