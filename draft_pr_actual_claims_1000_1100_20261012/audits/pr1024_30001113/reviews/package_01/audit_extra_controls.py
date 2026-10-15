"""Extra falsification controls against the exact runner, on isolated archive copies."""
from pathlib import Path
import json,subprocess,sys,tempfile,zipfile,hashlib
from datetime import datetime,timezone
R=Path(__file__).resolve().parent;P=R.parent.parent/'publication';out=[]
def run(cmd,cwd):
 q=subprocess.run(cmd,cwd=cwd,capture_output=True,timeout=180)
 return {'command':cmd,'exit_code':q.returncode,'stdout':q.stdout.decode(),'stderr':q.stderr.decode()}
with tempfile.TemporaryDirectory(prefix='isolated_archive_',dir=R/'receipts') as td:
 root=Path(td)
 with zipfile.ZipFile(P/'local_deformation_devissage_source_verification_v1.zip') as z:z.extractall(root)
 base=root/'local_deformation_devissage_v1'
 for mode in ('','-O','-OO'):
  args=[sys.executable,'-I','-S','-B']+([mode] if mode else [])+[str(base/'run_checks.py')]
  row=run(args,base);row.update(test='archived runner outer '+(mode or 'normal'),expected_exit=0);out.append(row)
 modifications=[
 ('extra_stdout','checks/current/check_conjugacy.py',lambda s:'print("EXTRA OUTPUT")\n'+s),
 ('extra_stderr','checks/current/check_conjugacy.py',lambda s:'import sys\nprint("EXTRA ERROR",file=sys.stderr)\n'+s),
 ('wrong_exit','checks/check_corrected_case.py',lambda s:s.replace('return 0','return 7')),
 ('unrelated_runtime_exception','checks/current/check_conjugacy.py',lambda s:'raise RuntimeError("unrelated exception")\n'+s),
 ('missing_source_anchor','checks/current/check_conjugacy.py',lambda s:s.replace('Mprime=[[one,e^e2],[one,one]]','Mprime = [[one,e^e2],[one,one]]')),
 ('syntax_error','checks/current/check_conjugacy.py',lambda s:'if invalid syntax\n'+s),
 ('missing_source_file','checks/current/check_conjugacy.py',None),
 ('disabled_independent_guards','checks/verify_functor_identities_explicit_guards.py',lambda s:s.replace('if not test:', 'if False:')),
 ('wrong_intended_failure_reason','checks/verify_functor_identities_explicit_guards.py',lambda s:s.replace('original assertion at line 49','wrong rejection reason'))]
 for name,rel,fn in modifications:
  q=base/rel;b=q.read_bytes()
  if fn:q.write_text(fn(b.decode()))
  else:q.unlink()
  row=run([sys.executable,'-I','-S','-B','-OO',str(base/'run_checks.py')],base);row.update(test=name,expected_nonzero=True);out.append(row);q.write_bytes(b)
# Independently inspect exact JSON recursion without executing the runner's main.
g={'__file__':str(P/'run_checks.py'),'__name__':'contract_test'};exec(compile((P/'run_checks.py').read_text(),str(P/'run_checks.py'),'exec'),g)
pairs=[({'a':[True]},{'a':[1]}),({'a':[1]},{'a':[1.0]}),({'a':[1]},{'a':[1,2]}),({'a':1},{'a':1,'b':2}),({'a':'1'},{'a':1})]
strict=[not g['exact_json_equal'](a,b) for a,b in pairs]
fail=[r['test'] for r in out if (r['exit_code']!=0 if r.get('expected_exit')==0 else r['exit_code']==0)]
if not all(strict):fail.append('strict JSON recursion')
result={'utc':datetime.now(timezone.utc).isoformat(),'status':'PASS' if not fail else 'FAIL','archive_39_case_passes':3,'additional_outer_optimized_contract_rejections':9,'recursive_JSON_type_shape_value_rejections':len(strict),'failures':fail,'rows':out,'strict_json_checks':strict}
(R/'receipts/EXTRA_CONTROLS.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in ('rows','strict_json_checks')},indent=2))
if fail:sys.exit(1)
