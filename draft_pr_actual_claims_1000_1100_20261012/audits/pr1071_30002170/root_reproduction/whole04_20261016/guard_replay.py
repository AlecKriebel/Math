import sys,json,copy,math,importlib.util
from pathlib import Path
sys.dont_write_bytecode=True
OWN=Path('/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/audits/pr1071_30002170/root_reproduction/whole04_20261016');P=Path('/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/audits/pr1071_30002170/NEWpreprint_v1_0')
def need(x,s):
 if not x:raise RuntimeError(s)
def save(n,v):(OWN/n).write_text(json.dumps(v,indent=2,allow_nan=False)+'\n')
sys.path.insert(0,str(P/'scripts'));spec=importlib.util.spec_from_file_location('candidate_check',P/'scripts/check.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
expected=json.loads((P/'checks/original_expected.json').read_text()); leaves=[];containers=[]
def walk(v,path=()):
 if type(v) in (dict,list):
  containers.append((path,v))
  for k,w in (v.items() if type(v) is dict else enumerate(v)):
   if path or k!='utc':walk(w,path+(k,))
 else:leaves.append((path,v))
walk(expected)
def altered(path,value,delete=False):
 d=copy.deepcopy(expected);q=d
 for k in path[:-1]:q=q[k]
 if delete:del q[path[-1]]
 else:q[path[-1]]=value
 return d
controls=[]
def fault(label,d):
 try:m.result_guard(d,expected)
 except RuntimeError as e:controls.append({'label':label,'rejected':True,'reason':str(e)});return
 raise RuntimeError('finite fault escaped '+label)
coverage=m.result_guard(expected,expected);need(len(leaves)==sum(coverage.values())==258,'leaf coverage')
for path,v in leaves:
 label='/'.join(map(str,path));fault('leaf deletion '+label,altered(path,None,True))
 fault('leaf type '+label,altered(path, [] if type(v) is not list else {}))
 if type(v) is float:
  for bad,n in [(float('nan'),'nan'),(float('inf'),'+inf'),(float('-inf'),'-inf')]:fault(n+' '+label,altered(path,bad))
  rel,absolute,_=m.float_policy(path)
  step=max(absolute,rel*abs(v),math.ulp(v))*4
  for sign in [-1,1]:fault('beyond tolerance '+str(sign)+' '+label,altered(path,v+sign*step))
 else:
  bad=not v if type(v) is bool else v+1 if type(v) is int else str(v)+' altered'
  fault('exact leaf value '+label,altered(path,bad))
for path,v in containers:
 if type(v) is dict:
  d=copy.deepcopy(v);d['unexpected_shape_control']=0
 else:d=copy.deepcopy(v)+[None]
 if path:fault('container shape '+str(path),altered(path,d))
 else:fault('root shape',d)
# Mathematical correlation corruption that keeps direct-grouped residual coherent.
d=copy.deepcopy(expected)
for r in d['finite_covariance_identity_float_cross_checks']:
 r['direct']*=1.000001;r['grouped']*=1.000001;r['difference']=r['direct']-r['grouped']
fault('coherent covariance scaling with internally exact residual',d)
d=copy.deepcopy(expected)
for r in d['constant_float_checks']:
 r['D_H']*=2;r['c_H']/=2
fault('coherent normalization and inverse constant factor two',d)
save('GUARD_'+sys.argv[1]+'.json',{'status':'PASS','coverage':coverage,'leaves':len(leaves),'containers':len(containers),'rejections':len(controls),'controls':controls,'note':'Floating acceptance is a declared finite policy; within-envelope changes are allowed. Independent mathematical checks below do not use candidate guards.'})

print(json.dumps({'status':'PASS','rejections':len(controls),'coverage':coverage}))
