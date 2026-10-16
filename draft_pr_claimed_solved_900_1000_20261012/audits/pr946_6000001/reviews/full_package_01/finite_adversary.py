import sys
if not sys.flags.safe_path:raise SystemExit('safe startup')
import pathlib,subprocess,os,json,hashlib,copy,tempfile,shutil,datetime,math
R=pathlib.Path('/Users/alec/Documents/Math');A=R/'draft_pr_claimed_solved_900_1000_20261012/audits/pr946_6000001';W=A/'reviews/full_package_01';P=W/'private/cold/package';O=P/'original/unsolved_math_prioritization/attempts/6000001';PY=R/'draft_pr_claimed_solved_900_1000_20261012/audits/pr906_30006419/reviews/computation_family/tmp/venv/bin/python'
env={k:v for k,v in os.environ.items() if not k.upper().startswith('PYTHON')}
# Authenticating all package bytes precedes diagnostic execution.
mraw=(P/'PACKAGE_MANIFEST.json').read_bytes()
if hashlib.sha256(mraw).hexdigest()!='52165ba2410fa32238244feef20820e5bca9971f60c90542a2360f4d44e6c4ec':raise ValueError('manifest')
for name,record in json.loads(mraw)['files'].items():
 raw=(P/name).read_bytes()
 if len(raw)!=record['bytes'] or hashlib.sha256(raw).hexdigest()!=record['sha256']:raise ValueError(name)
r=subprocess.run([str(PY),'-I','-S','-B',str(O/'verify_publication.py'),'29cb50b07af6a65b633516b5d86eed1dae93d57cf2abfb264b18eb9555a29903',str(O)],env=env,capture_output=True,text=True,timeout=120)
(W/'HISTORICAL_STRICT.stderr').write_text(r.stderr)
if r.returncode==0 or 'Fresh replay differs from frozen result: public/verify_math.py' not in r.stderr:raise ValueError('historical strict failure not reproduced')
r2=subprocess.run([str(PY),'-I','-B',str(O/'public/verify_math.py')],env=env,capture_output=True,text=True,timeout=120)
if r2.returncode:raise ValueError(r2.stderr)
actual=json.loads(r2.stdout);expected=json.loads((O/'public/VERIFICATION.json').read_text());(W/'AUTHOR_MATH_FRESH.json').write_text(r2.stdout)
raw=(P/'tools/compare_results.py').read_bytes();N={'__name__':'_checked_comparator_','__file__':str(P/'tools/compare_results.py')};exec(compile(raw,N['__file__'],'exec'),N);compare=N['compare'];compare(actual,expected)
controls=[]
def negative(name,x):
 try:compare(x,expected)
 except ValueError:controls.append({'case':name,'rejected':True});return
 raise ValueError('accepted mutant '+name)
for i in range(4):
 for field in ['lambda','minimum_eigenvalue','H_df_minus_dphi_max_abs']:
  for label,value in [('nan',float('nan')),('infinity',float('inf')),('bool',True),('integer',1),('string','1'),('negative',-1.0)]:
   x=copy.deepcopy(actual);x['positive_hessian_completion_samples'][i][field]=value;negative(f'sample{i}_{field}_{label}',x)
  x=copy.deepcopy(actual);x['positive_hessian_completion_samples'][i][field]+=0.01;negative(f'sample{i}_{field}_material_drift',x)
for key,value in [('status','FAIL'),('exact_residuals_checked',True),('one_dimensional_derivative_jet_determinant','999')]:
 x=copy.deepcopy(actual);x[key]=value;negative('exact_'+key,x)
x=copy.deepcopy(actual);x['positive_hessian_completion_samples'][0]['point'][0]=1.0;negative('exact_sample_point',x)
x=copy.deepcopy(actual);x['extra']='unreviewed';negative('extra_key',x)
# Fresh old assert vulnerability demonstration confined to disposable copy.
with tempfile.TemporaryDirectory(dir=W/'private') as td:
 q=pathlib.Path(td)/'original';shutil.copytree(O,q)
 (q/'public/PROOF.md').write_text('CORRUPTED CONTROL\n')
 old=subprocess.run([str(PY),'-I','-B','-O',str(q/'independent_global_audit/public/verify_audit_packet.py'),'--author-public',str(q/'public')],env=env,capture_output=True,text=True,timeout=10)
 if old.returncode or json.loads(old.stdout).get('verdict')!='PASS':raise ValueError('old assert defect not reproduced')
 # The same old checker in mandatory optimization0 must reject tampering.
 good=subprocess.run([str(PY),'-I','-B',str(q/'independent_global_audit/public/verify_audit_packet.py'),'--author-public',str(q/'public')],env=env,capture_output=True,text=True,timeout=10)
 if good.returncode==0 or 'AssertionError' not in good.stderr:raise ValueError('nonoptimized control')
report={'status':'PASS','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'historical_strict_failure':{'returncode':r.returncode,'reason':r.stderr.strip()},'typed_policy':{'fields':12,'negative_controls':controls,'positive_fresh_comparison_pass':True,'versions_transport_only':True,'roundoff_bound_proved':False},'old_assert_vulnerability':{'mutated_author_proof':'scratch copy only','observed_optimized_false_PASS':True,'observed_nonoptimized_rejection':True},'finite_claim_limit':'No universal-manifold proof or historical novelty inferred','external_actions':0}
(W/'FINITE_ADVERSARY.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'status':'PASS','negative_controls':len(controls),'strict_failure_preserved':True,'old_optimized_false_PASS_confirmed':True}))
