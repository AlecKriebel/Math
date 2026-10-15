"""Reexecute the frozen runner while retaining actual full receipts locally."""
from pathlib import Path
import tempfile,subprocess,runpy,json,hashlib,sys,contextlib,io,datetime
HERE=Path(__file__).resolve().parent
PKG=HERE/'extracted/odd-origin-area-product-verification'
(HERE/'scratch').mkdir(exist_ok=True);tempfile.tempdir=str(HERE/'scratch')
(HERE/'actual_receipts').mkdir(exist_ok=True)
jobs={Path(x['script']).name:x for x in json.loads((PKG/'CHECKSETS.json').read_text())}
orig=subprocess.run;rows=[]
def sha(data):return hashlib.sha256(data).hexdigest()
def capture(*args,**kwargs):
 result=orig(*args,**kwargs)
 script=Path(args[0][1]);job=jobs[script.name]
 if result.returncode==0:
  data=(script.parent/job['result_file']).read_bytes() if job['result_file'] else result.stdout
  actual=json.loads(data);expected_data=(PKG/job['expected']).read_bytes();expected=json.loads(expected_data)
  ignored=[]
  for key in ('utc','elapsed_seconds'):
   if key in actual or key in expected:ignored.append(key)
   actual.pop(key,None);expected.pop(key,None)
  assert actual==expected
  dst=HERE/'actual_receipts'/(job['name']+'.json');dst.write_bytes(data)
  normalized=json.dumps(actual,sort_keys=True,separators=(',',':')).encode()
  rows.append({'name':job['name'],'actual_path':str(dst.relative_to(HERE)),'actual_bytes':len(data),'actual_sha256':sha(data),'expected_path':job['expected'],'expected_bytes':len(expected_data),'expected_sha256':sha(expected_data),'normalized_receipt_sha256':sha(normalized),'ignored_top_level_keys':ignored,'complete_receipt_match':True,'source_sha256':sha(script.read_bytes())})
 return result
subprocess.run=capture
output=io.StringIO()
with contextlib.redirect_stdout(output):runpy.run_path(str(PKG/'run_verification.py'),run_name='__main__')
runner=output.getvalue();(HERE/'RUNNER_OUTPUT.json').write_text(runner)
import sympy,mpmath
receipt={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','python':sys.version,'sympy':sympy.__version__,'mpmath':mpmath.__version__,'exact_frozen_runner_used':True,'only_ignored_keys':['utc','elapsed_seconds'],'complete_receipts':sorted(rows,key=lambda x:x['name']),'runner_output_sha256':sha(runner.encode())}
(HERE/'REPRODUCTION.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({'status':receipt['status'],'checksets':len(rows),'python':receipt['python'],'sympy':receipt['sympy'],'mpmath':receipt['mpmath']}))
