from pathlib import Path
import os,sys,subprocess,json,datetime,hashlib,time
A=Path(__file__).resolve().parent.parent;M=A/'publication_package_v1/materials';D=A/'package_build_01'/(sys.argv[1] if len(sys.argv)>1 else 'portable_replay_01');D.mkdir()
env=dict(os.environ);env['PYTHONPATH']=str(A.parent/'pr200_5100007/math_algebra_family_01/runtime_packages');env['PYTHONDONTWRITEBYTECODE']='1'
runner=M/'verification/run_checks.py';results=[]
for name,opts,args in [('exact_normal',[],[]),('exact_optimized',['-O'],[]),('full_physical_normal',[],['--full-physical'])]:
 started=time.time();r=subprocess.run([sys.executable,'-B']+opts+[str(runner)]+args,env=env,capture_output=True,text=True)
 (D/(name+'.stdout')).write_text(r.stdout);(D/(name+'.stderr')).write_text(r.stderr)
 if r.returncode:raise ValueError(name+': '+r.stderr)
 g=json.loads(r.stdout);results.append({'name':name,'exit':r.returncode,'elapsed_seconds':time.time()-started,'result':g})
 print(json.dumps({'completed':name,'status':g['status']}),flush=True)
for opts in [[],['-O']]:
 r=subprocess.run([sys.executable,'-B']+opts+[str(runner),'--guard-false'],env=env,capture_output=True,text=True)
 if r.returncode==0 or 'DELIBERATE FALSE CONDITION' not in r.stderr:raise ValueError('failure guard disabled')
r={'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'PR':201,'all_jobs_passed':True,'ordinary_optimized_failure_guard_passed':True,'checks':results,'software':{'python':sys.version.split()[0],'sympy':'1.14.0','mpmath':'1.3.0'},'code_portable_env':'PYTHONPATH points to existing dependency software for this local replay only; no software copied into payload.','no_universal_proof_claim':True}
f=D/'ROOT_REPLAY_RECEIPT.json';f.write_text(json.dumps(r,indent=2)+'\n');f.chmod(0o444);(M/'verification/ROOT_PORTABLE_REPLAY_RECEIPT.json').write_bytes(f.read_bytes())
print(json.dumps({'all_jobs_passed':True,'receipt_sha256':hashlib.sha256(f.read_bytes()).hexdigest()}),flush=True)
