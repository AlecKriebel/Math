import sys
if not sys.flags.safe_path:raise SystemExit('safe startup')
import pathlib,json,subprocess,os,hashlib,datetime
R=pathlib.Path('/Users/alec/Documents/Math');A=R/'draft_pr_claimed_solved_900_1000_20261012/audits/pr946_6000001';W=A/'reviews/full_package_01';P=W/'private/cold/package'
PYTHON=R/'draft_pr_claimed_solved_900_1000_20261012/audits/pr906_30006419/reviews/computation_family/tmp/venv/bin/python'
PIN='52165ba2410fa32238244feef20820e5bca9971f60c90542a2360f4d44e6c4ec';V='1896614c7b163e8fd69fa15c82c4d2a77e1ca46f4e4ada407d9ea5b52c2a2d2d'
if hashlib.sha256((P/'verify_package.py').read_bytes()).hexdigest()!=V:raise ValueError('external verifier pin')
rows=[]
for mode,flags,opt in [('normal',['-I','-B'],0),('O',['-I','-B','-O'],1),('OO',['-I','-B','-OO'],2),('env2',['-P','-B'],2)]:
 env={k:v for k,v in os.environ.items() if not k.upper().startswith('PYTHON')}
 if mode=='env2':env['PYTHONOPTIMIZE']='2'
 cmd=[str(PYTHON),*flags,str(P/'verify_package.py'),'--package',str(P),'--manifest-sha256',PIN,'--runtime-receipt',str(W/'private'/('runtime_'+mode+'.json'))]
 r=subprocess.run(cmd,env=env,cwd=W/'private',capture_output=True,text=True,timeout=1200)
 (W/('REPLAY_'+mode+'.stdout')).write_text(r.stdout);(W/('REPLAY_'+mode+'.stderr')).write_text(r.stderr)
 if r.returncode:raise RuntimeError(mode+' '+r.stderr)
 receipt=json.loads(r.stdout);expected=json.loads((A/'preprint'/('PACKAGE_REPLAY_'+mode+'.json')).read_text())
 if receipt!=expected or receipt['observed_outer_optimization']!=opt:raise ValueError(mode+' receipt mismatch')
 rows.append({'mode':mode,'observed_outer_optimization':opt,'returncode':r.returncode,'receipt':receipt,'exact_canonical_match':True})
 print(mode,'PASS exact entire receipt; observed outer',opt,flush=True)
result={'status':'PASS','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'cold_extraction':True,'typed_float_policy_verified':True,'historical_strict_failure_preserved':True,'package_manifest_sha256':PIN,'externally_pinned_verifier_sha256':V,'normalized_fields_ignored':[],'modes':rows,'runtime':{'python':'3.14.6','sympy':'1.14.0','numpy':'2.3.5'},'limits':'Finite consistency and transport replay only, no universal proof or priority certification. Each receipt compared in full against the frozen canonical object with no ignored fields. Detailed runtime provenance is separate.'}
(W/'COLD_REPLAY.json').write_text(json.dumps(result,indent=2)+'\n')
