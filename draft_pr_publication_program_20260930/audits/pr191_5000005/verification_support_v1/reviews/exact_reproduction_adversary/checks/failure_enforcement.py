"""Adversarial optimization and failure-enforcement probes on inspected copies."""
import ast,datetime,hashlib,json,pathlib,subprocess
base=pathlib.Path(__file__).resolve().parent.parent
py='/opt/homebrew/opt/python@3.14/bin/python3.14'
cases=[('author','private_inputs/author/verify.py','check'),('reviewer','private_inputs/reviewer/check_independent.py','require'),('rational_geometry','checks/reflection_geometry.py','require'),('pentagon_geometry','checks/pentagon_geometry.py','require'),('octagon_geometry','checks/octagon_geometry.py','require')]
records=[]
for name,path,func in cases:
 script=base/path;source=script.read_text();asserts=sum(isinstance(x,ast.Assert) for x in ast.walk(ast.parse(source)))
 if asserts:raise RuntimeError(('optimization_unsafe_asserts',name,asserts))
 code="import runpy,sys; runpy.run_path(sys.argv[1],run_name='failure_probe')[sys.argv[2]](False,'injected_false_control')"
 for optimized in (False,True):
  argv=[py,'-E','-S','-B','-P']+(['-O'] if optimized else [])+['-c',code,str(script),func]
  now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
  start=now();r=subprocess.run(argv,capture_output=True,cwd=base);end=now()
  if r.returncode==0 or b'injected_false_control' not in r.stderr:raise RuntimeError(('failed_false_control',name,optimized,r.returncode))
  record={'name':name,'optimization':optimized,'argv':argv,'utc_start':start,'utc_end':end,'exit':r.returncode,'script_sha256':hashlib.sha256(script.read_bytes()).hexdigest(),'ast_assert_count':asserts,'stdout_sha256':hashlib.sha256(r.stdout).hexdigest(),'stderr_sha256':hashlib.sha256(r.stderr).hexdigest(),'detected_injected_false':True}
  records.append(record)
  (base/'results'/f'false_{name}_{"optimized" if optimized else "ordinary"}.stderr.txt').write_bytes(r.stderr)
print(json.dumps({'status':'PASS','expected_failure_runs':len(records),'unsafe_asserts':0,'records':records},indent=2))
