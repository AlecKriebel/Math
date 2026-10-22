#!/usr/bin/env python3
"""Review06 replay; only output custody relocated. No production source changes."""
from pathlib import Path
import sys,subprocess,json,hashlib
A=Path(__file__).resolve().parents[2]
P=A.parents[1]/'private/pr0280_package06'
S=A/'final_robustness_repair_20261021'
receipts=[]
for mode in [[],['-O']]:
 for name in ['replay_final_operations.py','revision_controls.py','doi_destination_controls.py']:
  dest=P/('ops_optimized' if mode else 'ops_normal')/name[:-3];dest.mkdir(parents=True,exist_ok=True)
  code=(S/name).read_text()
  code=code.replace('HERE=Path(__file__).resolve().parent;AUDIT=HERE.parent','HERE=Path('+repr(str(dest))+');AUDIT=Path('+repr(str(A))+')')
  code=code.replace('HERE=Path(__file__).resolve().parent\nAUDIT=HERE.parent','HERE=Path('+repr(str(dest))+')\nAUDIT=Path('+repr(str(A))+')')
  if name=='doi_destination_controls.py':code=code.replace("source=HERE/'before/verify_published_files.py'","source=Path("+repr(str(S))+ ")/'before/verify_published_files.py'")
  (dest/'runner.py').write_text(code)
  result=subprocess.run([sys.executable,'-B']+mode+[str(dest/'runner.py')],capture_output=True,text=True)
  (dest/'stdout.txt').write_text(result.stdout);(dest/'stderr.txt').write_text(result.stderr)
  receipts.append({'script':name,'mode':mode,'returncode':result.returncode,'source_sha256':hashlib.sha256((S/name).read_bytes()).hexdigest(),'scratch_source_sha256':hashlib.sha256(code.encode()).hexdigest(),'output':str(dest),'stdout_tail':result.stdout[-1800:],'stderr_tail':result.stderr[-1800:]})
  (A/'reviews/package_adversary_06/OPS_REPLAY.json').write_text(json.dumps(receipts,indent=2))
  if result.returncode:raise RuntimeError(receipts[-1])
print(json.dumps(receipts,indent=2))
