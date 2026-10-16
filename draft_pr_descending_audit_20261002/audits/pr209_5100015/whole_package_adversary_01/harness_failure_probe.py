"""Test unmodified actual harness run() AST with synthetic child failures.
No scientific candidate program is executed. Only copied own-folder inputs and
lossless controlled failure results are written; candidate remains read-only.
"""
from pathlib import Path
from datetime import datetime,timezone
import ast,hashlib,json,shutil,subprocess,types,traceback
B=Path('/Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr209_5100015/preprint');O=B.parent/'whole_package_adversary_01';V=B/'verification';OUT=O/'harness_failure_probe'
OUT.mkdir(exist_ok=False)
raw=(V/'run_checks.py').read_bytes();tree=ast.parse(raw);run_node=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='run');module=ast.Module(body=[run_node],type_ignores=[])
rows=[]
for mode in ['ordinary_nonzero_exit','timeout_with_partial_output','launch_error']:
 def fake(command,**kwargs):
  if mode=='ordinary_nonzero_exit':return subprocess.CompletedProcess(command,17,b'partial stdout marker\x00\xff\n',b'partial stderr marker\x00\xfe\n')
  if mode=='timeout_with_partial_output':raise subprocess.TimeoutExpired(command,kwargs['timeout'],output=b'partial timeout stdout\x00\xff\n',stderr=b'partial timeout stderr\x00\xfe\n')
  raise FileNotFoundError('synthetic executable lookup failure')
 ns=dict(V=V,OUT=OUT,shutil=shutil,subprocess=types.SimpleNamespace(run=fake),datetime=datetime,timezone=timezone,hashlib=hashlib,json=json,sys=__import__('sys'))
 exec(compile(module,str(V/'run_checks.py'),'exec'),ns)
 row={'mode':mode,'synthetic_child_failure':True}
 try:row['returned_receipt']=ns['run']((mode,'audits/priority_classical_general_01/bridge_verify.py',None,'bridge_results.json','audits/priority_classical_general_01/bridge_results.json',[]))
 except Exception as exc:
  row.update(exception_type=type(exc).__name__,exception_text=str(exc),traceback=traceback.format_exc())
  if isinstance(exc,subprocess.TimeoutExpired):
   # Preserve the bytes the tested harness discards, without decoding loss.
   (OUT/(mode+'.partial_stdout.bin')).write_bytes(exc.output or b'');(OUT/(mode+'.partial_stderr.bin')).write_bytes(exc.stderr or b'')
  (OUT/(mode+'.exception.txt')).write_text(row['traceback'])
 folder=OUT/mode;row['files_created_by_actual_run_function']=sorted(p.name for p in folder.iterdir());row['stdout_saved_by_harness']=(folder/'stdout.txt').exists();row['stderr_saved_by_harness']=(folder/'stderr.txt').exists();row['receipt_saved_by_harness']=(folder/'REPLAY_RECEIPT.json').exists();rows.append(row)
assert rows[0]['receipt_saved_by_harness'] and rows[0]['returned_receipt']['status']=='FAIL'
assert not rows[1]['stdout_saved_by_harness'] and not rows[1]['stderr_saved_by_harness'] and not rows[1]['receipt_saved_by_harness']
assert not rows[2]['receipt_saved_by_harness']
result=dict(utc=datetime.now(timezone.utc).isoformat(),tested_program='verification/run_checks.py',tested_sha256=hashlib.sha256(raw).hexdigest(),method='Execute exact parsed run() function with controlled subprocess.run failures; scientific programs never executed.',finding='subprocess.run(timeout=900) is outside the exception handler. Supported timeout and launch failures escape without stdout/stderr/per-suite failure receipt; timeout partial bytes exist in exception but are not retained by the harness.',rows=rows)
(O/'HARNESS_FAILURE_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
