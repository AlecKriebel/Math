"""Adapted from sealed05 replayed04_numerical_controls.py SHA256 991c95c1cd677848f1e26cc6577929a5fe0b868a06cb1855923c7044c5f45a22. Only owned scratch/output path changes. All external clients fake.
"""
import sys
if not sys.flags.isolated or sys.flags.optimize:raise RuntimeError('Use isolated0')
import copy,hashlib,json,math,pathlib,subprocess,datetime,itertools
O=pathlib.Path('/Users/alec/Documents/Math/draft_pr_claimed_solved_900_1000_20261012/audits/pr946_6000001/reviews/full_package_06');PK=O/'private/cold';P=PK/'original/unsolved_math_prioritization/attempts/6000001';Y='/Users/alec/Documents/Math/draft_pr_claimed_solved_900_1000_20261012/audits/pr906_30006419/reviews/computation_family/tmp/venv/bin/python'
def need(c,m):
 if not c:raise RuntimeError(m)
m=json.loads((PK/'PACKAGE_MANIFEST.json').read_text());b=(PK/'tools/compare_results.py').read_bytes();need(hashlib.sha256(b).hexdigest()==m['files']['tools/compare_results.py']['sha256'],'capture')
N={'__name__':'_compare_','__file__':str(PK/'tools/compare_results.py')};exec(compile(b,N['__file__'],'exec'),N);compare=N['compare'];expected=json.loads((P/'public/VERIFICATION.json').read_text())
r=subprocess.run([Y,'-I','-B',str(P/'public/verify_math.py')],capture_output=True,text=True,timeout=120);need(r.returncode==0,r.stderr);actual=json.loads(r.stdout);diff=N['differences'](actual,expected);floatdiff=[x for x in diff if x['kind']=='float'];need(len(floatdiff)==9,'actual9 float differences');maximum=max(x['absolute_difference'] for x in floatdiff);need(maximum==2.1032064978498966e-12,'actual maximum drift');compare(actual,expected)
negatives=[]
def mutate(path,val):
 result=copy.deepcopy(expected);cursor=result
 for k in path[:-1]:cursor=cursor[k]
 cursor[path[-1]]=val;return result
def leaves(obj,path=()):
 if type(obj) is dict:
  for k,v in obj.items():yield from leaves(v,path+(k,))
 elif type(obj) is list:
  for k,v in enumerate(obj):yield from leaves(v,path+(k,))
 else:yield path,obj
for path,value in leaves(expected):
 if len(path)==1 and path[0] in N['VERSION_FIELDS']:continue
 if len(path)==3 and path[0]=='positive_hessian_completion_samples' and path[2] in N['NUMERIC_FIELDS']:continue
 altered=not value if type(value) is bool else value+1 if type(value) in (int,float) else value+'!' if type(value) is str else 'changed'
 try:compare(mutate(path,altered),expected)
 except ValueError:negatives.append({'path':list(path),'mutation':'every_exact_scalar_changed','rejected':True})
 else:raise RuntimeError('exact leaf accepted '+str(path))
for i,field in itertools.product(range(4),sorted(N['NUMERIC_FIELDS'])):
 path=('positive_hessian_completion_samples',i,field)
 bads=[('negative',-1.0),('zero',0.0)] if field=='minimum_eigenvalue' else [('below_one',math.nextafter(1.0,0.0))] if field=='lambda' else [('negative',-1e-14),('upper_boundary',1e-6)]
 for label,value in bads:
  try:compare(mutate(path,value),expected)
  except ValueError:negatives.append({'path':list(path),'mutation':label,'rejected':True})
  else:raise RuntimeError('domain accepted')
report={'status':'PASS','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'historical_strict_comparison':'FAIL','actual_differing_sample_floats':len(floatdiff),'designated_float_fields':12,'maximum_absolute_sample_difference':maximum,'all_differences':diff,'every_exact_leaf_and_domain_controls':negatives,'portable_comparison':'PASS','not_proved_roundoff':True}
print(json.dumps(report,indent=2))

