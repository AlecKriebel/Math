from pathlib import Path
import sys,json,copy,importlib,shutil,subprocess,os
O=Path(__file__).resolve().parent;V=O/'extracted/k605a_outer_focal_pedal_product/verification'
M=O/'mutant_copy';shutil.copytree(V,M,dirs_exist_ok=True)
sys.path.insert(0,str(M))
h=importlib.import_module('run_verification');iv=importlib.import_module('integrity');rv=importlib.import_module('validate_payloads')
rows=[]
def check(name,fun):
 try:ok=bool(fun());assert ok
 except Exception as e:raise AssertionError((name,repr(e))) from e
 rows.append({'name':name,'pass':True})
def rejected(fun):
 try:fun()
 except (ValueError,RuntimeError,FileNotFoundError,AssertionError,KeyError):return True
 return False
check('bool_int_type',lambda:bool(h.differences({'a':True},{'a':1})))
check('int_float_type',lambda:bool(h.differences({'a':1},{'a':1.0})))
for key in ['python','runtime','utc','utc_start']:
 a={'python':'old','nested':{key:'science'}};b=copy.deepcopy(a);b['python']='new';b['nested'][key]='altered science'
 check('nested_'+key+'_not_excluded',lambda a=a,b=b:bool(h.differences(h.normalize(a,'source_domain'),h.normalize(b,'source_domain'))))
check('list_order',lambda:bool(h.differences([1,2],[2,1])))
check('extra_key',lambda:bool(h.differences({'a':1},{'a':1,'b':2})))
check('tiny_scientific_residual_change',lambda:bool(h.differences({'error':'1e-100'},{'error':'1.00000000000000000000000001e-100'})))
check('missing_exclusion_refused',lambda:rejected(lambda:h.normalize({'nested':{'python':'x'}},'source_domain')))
a={'python':'build','nested':{'value':[1,2]}};b=copy.deepcopy(a);h.normalize(a,'source_domain');check('normalize_does_not_mutate',lambda:a==b)
for token in ['NaN','Infinity','-Infinity','1e100']:
 check('nonfinite_or_large_'+token,lambda token=token:rejected(lambda:rv.small(token,'1e-60')))
physical=json.loads((M/'audits/physical_geometry_adversary_01/results.json').read_text());physical['cases'][0]['max_errors']['boundary']='NaN'
check('nested_row_nan_refused',lambda:rejected(lambda:rv.result_checks('physical_geometry',physical)))
base=iv.verify()
p=M/'README.md';old=p.read_bytes();p.write_bytes(old+b' ')
check('single_byte_payload_mutation',lambda:rejected(iv.verify));p.write_bytes(old)
p=M/'extra.txt';p.write_text('extra');check('extra_file',lambda:rejected(iv.verify));p.unlink()
p=M/'private';p.mkdir();check('empty_forbidden_directory',lambda:rejected(iv.verify));p.rmdir()
p=M/'link';p.symlink_to('README.md');check('symlink',lambda:rejected(iv.verify));p.unlink()
trial=O/'bad_trial_manifest.json';d=json.loads((M/'MANIFEST.json').read_text());d['schema']='wrong';trial.write_text(json.dumps(d));check('unknown_schema',lambda:rejected(lambda:iv.verify(trial)))
assert iv.verify()==base
commands=[('optimized_O',[sys.executable,'-B','-O',str(V/'run_verification.py'),'--integrity-only'],'Refusing -O/-OO'),('optimized_OO',[sys.executable,'-B','-OO',str(V/'run_verification.py'),'--integrity-only'],'Refusing -O/-OO'),('sealed_receipt',[sys.executable,'-B',str(V/'run_verification.py'),'--integrity-only','--receipt',str(V/'forbidden_receipt.json')],'Receipt must be outside sealed package')]
wrong=O/'wrong_primary';wrong.mkdir(exist_ok=True)
for name in rv.PRIMARY_HASHES:(wrong/name).write_bytes(b'%PDF-FAKE-primary-mutation')
commands.extend([('wrong_primary_file',[sys.executable,'-B',str(V/'run_verification.py'),'--run','meromorphic_divisor','--primary-dir',str(wrong)],'Primary PDF hash mismatch'),('missing_primary_file',[sys.executable,'-B',str(V/'run_verification.py'),'--run','meromorphic_divisor','--primary-dir',str(O/'missing_primary')],'FileNotFoundError')])
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(O/'replay_temp'))
for name,args,text in commands:
 p=subprocess.run(args,cwd=O,env=env,capture_output=True,text=True);assert p.returncode!=0 and text in p.stderr,(name,p.stdout,p.stderr)
 rows.append({'name':name,'pass':True,'exit_code':p.returncode,'expected_error':text,'stderr_tail':p.stderr[-1100:]})
# Main refuses wrong scientific dependencies before executing a single job.
from types import SimpleNamespace
save={k:sys.modules.get(k) for k in ['sympy','mpmath']};oldargv=sys.argv
sys.modules['sympy']=SimpleNamespace(__version__='0.0.0');sys.modules['mpmath']=SimpleNamespace(__version__='1.3.0');sys.argv=[str(M/'run_verification.py'),'--run','author']
check('wrong_scientific_library_version',lambda:rejected(h.main))
sys.argv=oldargv
for k,v in save.items():
 if v is None:sys.modules.pop(k,None)
 else:sys.modules[k]=v
check('mutant_copy_integrity_restored',lambda:iv.verify()==base)
assert not (V/'forbidden_receipt.json').exists()
(O/'HARNESS_MUTANT_RESULTS.json').write_text(json.dumps({'tests':rows,'count':len(rows),'all_passed':True,'action_helpers_executed':False,'mutations_only_own_copy':True},indent=2)+'\n')
shutil.rmtree(M);shutil.rmtree(wrong);trial.unlink()
print('PASS',len(rows),'harness controls; own mutable copies removed')
