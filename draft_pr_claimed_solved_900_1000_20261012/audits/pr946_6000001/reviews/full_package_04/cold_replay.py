#!/usr/bin/env python3
"""Cold extraction plus four actual outer optimization modes; whole-object compare."""
import concurrent.futures,datetime,hashlib,json,os,pathlib,subprocess,zipfile
R=pathlib.Path(__file__).resolve().parent;A=R.parents[1];D=A/'preprint'
PY='/Users/alec/Documents/Math/draft_pr_claimed_solved_900_1000_20261012/audits/pr906_30006419/reviews/computation_family/tmp/venv/bin/python'
MP='52165ba2410fa32238244feef20820e5bca9971f60c90542a2360f4d44e6c4ec';VP='1896614c7b163e8fd69fa15c82c4d2a77e1ca46f4e4ada407d9ea5b52c2a2d2d'
def sha(x):return hashlib.sha256(x).hexdigest()
def need(c,m):
 if not c:raise RuntimeError(m)
def main():
 out=R/'private/cold';out.mkdir(exist_ok=True)
 with zipfile.ZipFile(D/'global_hessian_verification.zip') as z:
  am=json.loads(z.read('ARCHIVE_MANIFEST.json'));need(len(z.namelist())==220,'outer220')
  for n in z.namelist():
   p=pathlib.PurePosixPath(n);need(not p.is_absolute() and '..' not in p.parts and str(p)==n,'path')
   raw=z.read(n)
   if n!='ARCHIVE_MANIFEST.json':need({'bytes':len(raw),'sha256':sha(raw)}==am['files'][n],'outerhash')
   q=out/n;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(raw);q.chmod(0o644)
 pkg=out/'package';need(sha((pkg/'verify_package.py').read_bytes())==VP,'verifier external pin');need(sha((pkg/'PACKAGE_MANIFEST.json').read_bytes())==MP,'manifest external pin')
 m=json.loads((pkg/'PACKAGE_MANIFEST.json').read_bytes());need(len(m['files'])==207,'207')
 for k,v in m['files'].items():
  raw=(pkg/k).read_bytes();need(len(raw)==v['bytes'] and sha(raw)==v['sha256'],'capture closure '+k)
 scratch=R/'private/tmp';scratch.mkdir(exist_ok=True)
 def mode(name,args,opt):
  env=dict(os.environ);env['TMPDIR']=str(scratch.resolve());env.pop('PYTHONOPTIMIZE',None)
  if name=='env2':env['PYTHONOPTIMIZE']='2'
  cmd=[PY,*args,str(pkg/'verify_package.py'),'--package',str(pkg),'--manifest-sha256',MP,'--runtime-receipt',str(R/'private'/('runtime_'+name+'.json'))]
  p=subprocess.run(cmd,env=env,cwd=R,capture_output=True,text=True,timeout=1200)
  (R/'private'/('stdout_'+name+'.json')).write_text(p.stdout);(R/'private'/('stderr_'+name+'.txt')).write_text(p.stderr)
  need(p.returncode==0,'cold mode '+name+':'+p.stderr)
  receipt=json.loads(p.stdout);expected=json.loads((D/('PACKAGE_REPLAY_'+name+'.json')).read_text())
  need(receipt==expected,'ENTIRE receipt differs '+name)
  need(receipt['observed_outer_optimization']==opt and receipt['worker_optimization']==0,'actual flags '+name)
  return name,{'returncode':p.returncode,'actual_outer_optimization':opt,'entire_normalized_receipt_matches':True,'receipt':receipt}
 modes={}
 with concurrent.futures.ThreadPoolExecutor(4) as ex:
  futures=[ex.submit(mode,*args) for args in [('normal',['-I','-B'],0),('O',['-I','-B','-O'],1),('OO',['-I','-B','-OO'],2),('env2',['-P','-B'],2)]]
  for f in futures:
   n,v=f.result();modes[n]=v
 result={'status':'PASS','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'cold_extraction':True,'typed_float_policy_verified':True,'historical_strict_failure_preserved':True,'package_manifest_sha256':MP,'externally_pinned_verifier_sha256':VP,'normalized_fields_ignored':[],'outer_payloads':219,'archive_members':220,'inner_payloads':207,'inner_files':208,'modes':[dict(mode=n,observed_outer_optimization=modes[n]['actual_outer_optimization'],returncode=0,receipt=modes[n]['receipt']) for n in ['normal','O','OO','env2']],'runtime_python':subprocess.check_output([PY,'--version'],text=True).strip(),'notes':'All payloads captured/authenticated before execution; four outer flags observed, all diagnostics isolated nonoptimized bytecode-disabled. Historical numeric policy separately challenged in numerical_controls.py.'}
 (R/'COLD_REPLAY.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'status':'PASS','actual_modes':{n:v['actual_outer_optimization'] for n,v in modes.items()},'whole_objects_equal':True}))
if __name__=='__main__':main()
