from pathlib import Path
import os,sys,subprocess,json,shutil,hashlib,datetime,importlib.util,zipfile,ast
R=Path(__file__).resolve().parent; A=R.parent.parent; P=A/'publication'; TMP=R/'tmp'; EX=TMP/'extracted'; PY=sys.executable
sys.dont_write_bytecode=True
results={}
def sha(d):return hashlib.sha256(d).hexdigest()
def run(key,args,cwd=None,env=None):
 q=subprocess.run(args,cwd=cwd,env=env,capture_output=True)
 (R/(key+'.stdout')).write_bytes(q.stdout); (R/(key+'.stderr')).write_bytes(q.stderr)
 results[key]={'returncode':q.returncode,'stdout_sha256':sha(q.stdout),'stderr_sha256':sha(q.stderr)}
 return q
for label,flags,optimization in [('normal',[],None),('optimized',['-O'],None),('inherited',[],'2')]:
 env=os.environ.copy(); env['TMPDIR']=str(TMP)
 if optimization:env['PYTHONOPTIMIZE']=optimization
 else:env.pop('PYTHONOPTIMIZE',None)
 q=run('replay_'+label,[PY,*flags,str(EX/'verify_package.py')],EX,env)
 if q.returncode:raise RuntimeError(label+' replay failed')
 results['replay_'+label]['output']=json.loads(q.stdout)
# Rebuild from original builder code, relocated to this review only.
BA=TMP/'rebuild_audit'; BP=BA/'publication'; BP.mkdir(parents=True,exist_ok=True)
script=(P/'build_package.py').read_bytes(); tree=ast.parse(script)
ns={'__file__':str(BP/'build_package.py'),'__name__':'independent_builder'}
exec(compile(script,str(BP/'build_package.py'),'exec'),ns)
(BP/'build_package.py').write_bytes(script)
for n in ['gns_generation_counterexample.pdf','gns_generation_counterexample.tex','verify_package.py','requirements.txt','CURRENT_PRIORITY_AND_STATUS.md','PACKAGE_README.md']:shutil.copyfile(P/n,BP/n)
shutil.copytree(A/'native',BA/'native',dirs_exist_ok=True)
for family,names in ns['FAMILIES'].items():
 for n in names:
  dest=BA/'reviews'/family/n;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(A/'reviews'/family/n,dest)
for n in ['PR_PUBLIC_CHRONOLOGY.json','PROOF_COMMIT_CHRONOLOGY.txt','ROOT_PRIMARY_SOURCE_CHECK.json','ROOT_ORIGINAL_REPLAY.json','ROOT_INTEGRITY_CONTROLS.txt','ROOT_OPERATOR_REPLAY.json','ROOT_SCOPE_REPLAY.json','ROOT_PRIORITY_REPLAY.json','ROOT_CLASSICAL_REPLAY.json','ROOT_REPRODUCTION_ENVIRONMENT.json','MATH_GATE_ACCEPTANCE.json','PRIORITY_GATE_ACCEPTANCE.json']:shutil.copyfile(A/n,BA/n)
q=run('builder_replay',[PY,str(BP/'build_package.py')],BP)
results['builder_replay']['zip_sha256']=sha((BP/'gns_verification.zip').read_bytes())
results['builder_replay']['byte_identical']=((BP/'gns_verification.zip').read_bytes()==(P/'gns_verification.zip').read_bytes())
if not results['builder_replay']['byte_identical']:raise RuntimeError('rebuild differs')
# Supplied mock regression controls, with fixture and temporary output paths relocated.
OPS=TMP/'ops';OPS.mkdir(exist_ok=True)
for family,name in [('operations_01','check_helpers.py'),('operations_02','check_repairs.py')]:
 s=(A/'reviews'/family/name).read_text().replace('AUDIT = HERE.parents[1]',f'AUDIT = Path({str(A)!r})')
 if name=='check_repairs.py':s=s.replace("fixture = AUDIT / 'reviews/operations_01/check_helpers.py'","fixture = HERE / 'check_helpers.py'")
 (OPS/name).write_text(s)
for label,flags in [('normal',[]),('optimized',['-O'])]:
 q=run('operations_'+label,[PY,*flags,str(OPS/'check_repairs.py')],OPS)
 if q.returncode:raise RuntimeError('ops '+label+' failed')
 results['operations_'+label]['output']=json.loads(q.stdout)
# Current payload binding independently invokes the read-only gate, without receipt mutation/live calls.
spec=importlib.util.spec_from_file_location('pr623_read_only',A/'prepare_integration.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
original,frozen=m.load_snapshot(A/'native'/m.PREFIX)
pub={n:(P/n).read_bytes() for n in m.PUB_NAMES};source=(P/'CURRENT_PRIORITY_AND_STATUS.md').read_bytes()
results['actual_archive_binding']=m.archive_binding(pub['gns_verification.zip'],original,pub,source)
results['native29_manifested']={n:sha(d) for n,d in original.items()}
results['native29_archive_identical']=all((EX/'candidate'/n).read_bytes()==d for n,d in original.items())
(R/'CHECK_RESULTS.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps({k:(v.get('returncode') if type(v)is dict else v) for k,v in results.items()},indent=2))
