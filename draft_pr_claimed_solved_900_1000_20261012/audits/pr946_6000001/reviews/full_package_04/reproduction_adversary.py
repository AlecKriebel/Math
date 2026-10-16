import sys
if not sys.flags.isolated or sys.flags.optimize:raise RuntimeError('Use nonoptimized -I')
from pathlib import Path
import base64,copy,datetime,hashlib,json,math,os,shutil,subprocess
R=Path('/Users/alec/Documents/Math');A=R/'draft_pr_claimed_solved_900_1000_20261012/audits/pr946_6000001';O=A/'reviews/full_package_04';S=O/'private/cold';PK=S/'package';P=PK/'original/unsolved_math_prioritization/attempts/6000001';Y=R/'draft_pr_claimed_solved_900_1000_20261012/audits/pr906_30006419/reviews/computation_family/tmp/venv/bin/python'
def h(b):return hashlib.sha256(b).hexdigest()
def need(t,m):
 if not t:raise RuntimeError(m)
m=json.loads((PK/'PACKAGE_MANIFEST.json').read_bytes());need(h((PK/'PACKAGE_MANIFEST.json').read_bytes())=='52165ba2410fa32238244feef20820e5bca9971f60c90542a2360f4d44e6c4ec','manifest external pin')
def captured(name):
 b=(PK/name).read_bytes();r=m['files'][name];need(len(b)==r['bytes'] and h(b)==r['sha256'],'capture '+name);return b
BOOT='import sys,base64;raw=base64.b64decode(sys.argv[1],validate=True);p=sys.argv[2];sys.argv=sys.argv[2:];exec(compile(raw,p,"exec"),dict(__name__="__main__",__file__=p))'
env={k:v for k,v in os.environ.items() if not k.upper().startswith('PYTHON')};env['TMPDIR']=str(O/'private/temp');records=[]
def run(name,args,flags=('-I','-B'),timeout=180):
 b=captured(name);return subprocess.run([str(Y),*flags,'-c',BOOT,base64.b64encode(b).decode(),str(PK/name),*map(str,args)],capture_output=True,text=True,env=env,cwd=O,timeout=timeout)
# The actual frozen selftest is executed from captured bytes, with own scratch root.
r=run('package_selftests.py',['--package',PK,'--manifest-sha256',h((PK/'PACKAGE_MANIFEST.json').read_bytes())]);need(r.returncode==0,r.stderr);j=json.loads(r.stdout);(O/'PACKAGE_SELFTESTS_REPLAY.json').write_text(json.dumps(j,indent=2)+'\n');records.append({'case':'package_transport_selftests','count':len(j['controls']),'pass':True})
# Historical exact floating comparison remains a real failure on this runtime.
r=run('original/unsolved_math_prioritization/attempts/6000001/verify_publication.py',['29cb50b07af6a65b633516b5d86eed1dae93d57cf2abfb264b18eb9555a29903',P],('-I','-S','-B'))
need(r.returncode!=0 and 'Fresh replay differs from frozen result: public/verify_math.py' in r.stderr,'strict historical failure absent');(O/'private/strict_wrapper.stderr').write_text(r.stderr);records.append({'case':'historical_strict_float_wrapper','returncode':r.returncode,'expected_failure':True,'reason':r.stderr.strip()})
# Old audit A is assertion based and must never be relied on in optimized mode.
bad=O/'private/historical_bad';shutil.copytree(P,bad);(bad/'public/PROOF.md').write_bytes((bad/'public/PROOF.md').read_bytes()+b'\ncontrolled corruption\n')
script='original/unsolved_math_prioritization/attempts/6000001/independent_global_audit/public/verify_audit_packet.py';b=captured(script)
for label,flags,want in [('normal',['-I','-B'],False),('O',['-I','-B','-O'],True),('OO',['-I','-B','-OO'],True)]:
 logical=bad/'independent_global_audit/public/verify_audit_packet.py';r=subprocess.run([str(Y),*flags,'-c',BOOT,base64.b64encode(b).decode(),str(logical),'--author-public',str(bad/'public')],env=env,capture_output=True,text=True,timeout=20,cwd=O)
 need((r.returncode==0)==want,'historical optimized diagnostic changed');records.append({'case':'historical_corruptproof_auditA_'+label,'returncode':r.returncode,'false_PASS':want})
# Compare the old FIFO defect with current v2 prompt rejection, using captured functions.
fifo=O/'private/fifo_input';os.mkfifo(fifo)
for label,name,hang in [('v1','reviews/reproducibility/portable_gate.py',True),('v2','tools/portable_gate.py',False)]:
 b=captured(name);code='import base64,sys;from pathlib import Path;b=base64.b64decode(sys.argv[1]);n={"__name__":"_fifo_test_","__file__":sys.argv[2]};exec(compile(b,sys.argv[2],"exec"),n);n["anchored"](Path(sys.argv[3]),"a"*64)'
 try:r=subprocess.run([str(Y),'-I','-S','-B','-c',code,base64.b64encode(b).decode(),str(PK/name),str(fifo)],capture_output=True,text=True,env=env,timeout=1.5)
 except subprocess.TimeoutExpired:need(hang,'current v2 blocked');records.append({'case':label+'_FIFO','timeout':True,'historical_defect_preserved':True})
 else:need(not hang and r.returncode!=0 and 'regular' in r.stderr,'v2 FIFO not promptly rejected');records.append({'case':label+'_FIFO','returncode':r.returncode,'prompt_rejection':True})
fifo.unlink()
# All 12 numerical fields retain exact types, finiteness, domains and tight tolerances.
b=captured('tools/compare_results.py');N={'__name__':'_typed_policy_','__file__':str(PK/'tools/compare_results.py')};exec(compile(b,N['__file__'],'exec'),N);compare=N['compare'];ex=json.loads((P/'public/VERIFICATION.json').read_bytes());compare(ex,ex);typed=[]
for i in range(4):
 for field in ['lambda','minimum_eigenvalue','H_df_minus_dphi_max_abs']:
  for label,value in [('nan',float('nan')),('inf',float('inf')),('bool',True),('int',1),('str','1'),('null',None)]:
   v=copy.deepcopy(ex);v['positive_hessian_completion_samples'][i][field]=value
   try:compare(v,ex)
   except ValueError:typed.append({'sample':i,'field':field,'mutation':label,'rejected':True})
   else:raise RuntimeError('wrong float accepted')
  value=copy.deepcopy(ex);value['positive_hessian_completion_samples'][i][field]+=1e-3
  try:compare(value,ex)
  except ValueError:typed.append({'sample':i,'field':field,'mutation':'material_change','rejected':True})
  else:raise RuntimeError('large drift accepted')
for label,mut in [('int_count_to_bool',lambda v:v.update(exact_residuals_checked=True)),('extra',lambda v:v.update(units='scaled')),('point',lambda v:v['positive_hessian_completion_samples'][1]['point'].__setitem__(0,1000.0)),('determinant',lambda v:v.update(two_dimensional_derivative_jet_determinant='575'))]:
 v=copy.deepcopy(ex);mut(v)
 try:compare(v,ex)
 except ValueError:typed.append({'mutation':label,'rejected':True})
 else:raise RuntimeError('exact field changed accepted')
for i in range(4):
 v=copy.deepcopy(ex);v['positive_hessian_completion_samples'][i]['lambda']+=1e-14;compare(v,ex)
records.append({'case':'typed_exact12_policy','negative_controls':len(typed),'all_rejected':True,'bounded_drift_positive_controls':4,'versions_only_nonmathematical_exception':['python','sympy','numpy'],'not_roundoff_certificate':True})
(O/'TYPED_FLOAT_CONTROLS.json').write_text(json.dumps({'status':'PASS','controls':typed,'policy':'Exactly 12 named sample fields; other mathematical fields exact and typed.'},indent=2)+'\n')
result={'status':'PASS','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'records':records,'typed_float_policy_verified':True,'historical_strict_failure_preserved':True,'external_mutations':0,'canonical_changes':0};(O/'REPRODUCTION_ADVERSARY.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'status':'PASS','records':len(records),'typed_negatives':len(typed)}))
