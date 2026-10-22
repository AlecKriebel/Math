import sys,json,copy,math,importlib.util
from pathlib import Path
sys.dont_write_bytecode=True
R=Path('/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/audits/pr1071_30002170/root_reproduction/whole05_20261016');P=Path('/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/audits/pr1071_30002170/NEWpreprint_v1_0')
sys.path.insert(0,str(P/'scripts'))
import check as c
def need(ok,msg):
 if not ok:raise RuntimeError(msg)
baseline=json.loads((P/'checks/original_expected.json').read_text())
records=[]
def rejected(label,fn):
 try:fn()
 except RuntimeError as e:records.append({'case':label,'rejected':True,'reason':str(e)});return
 raise RuntimeError('Adversary escaped '+label)
coverage=c.result_guard(baseline,baseline)
need(coverage=={'exact_nonfloat_leaves':115,'exact_float':34,'derived_relative':25,'covariance_absolute':84},'Leaf contract')
def leaves(v,path=()):
 if type(v)is dict:
  for k,x in v.items():
   if path or k!='utc':yield from leaves(x,path+(k,))
 elif type(v)is list:
  for k,x in enumerate(v):yield from leaves(x,path+(k,))
 else:yield path,v
def change(path,value):
 d=copy.deepcopy(baseline);cur=d
 for key in path[:-1]:cur=cur[key]
 cur[path[-1]]=value;return d
for path,v in leaves(baseline):
 label='/'.join(map(str,path))
 if type(v)is float:
  rel,abs_,policy=c.float_policy(path)
  wrong=(v+16*abs_)if abs_ else v*(1+16*rel)if rel else math.nextafter(v,math.inf)
  if wrong==v:wrong=math.nextafter(v,math.inf)
  rejected('bad-value/'+label,lambda p=path,w=wrong:c.result_guard(change(p,w),baseline))
  for w in [float('nan'),float('inf'),float('-inf')]:rejected('nonfinite/'+str(w)+'/'+label,lambda p=path,w=w:c.result_guard(change(p,w),baseline))
  rejected('wrong-type/'+label,lambda p=path:c.result_guard(change(p,'0'),baseline))
 else:
  w=not v if type(v)is bool else v+1 if type(v)is int else v+'-changed' if type(v)is str else 'changed'
  rejected('bad-exact/'+label,lambda p=path,w=w:c.result_guard(change(p,w),baseline))
  rejected('wrong-type/'+label,lambda p=path:c.result_guard(change(p,None),baseline))
bad=copy.deepcopy(baseline);bad['extra']=1;rejected('extra-root-field',lambda:c.result_guard(bad,baseline))
bad2=copy.deepcopy(baseline);del bad2['exact_area_pairing'];rejected('missing-root-field',lambda:c.result_guard(bad2,baseline))
for key,value in baseline.items():
 if type(value)is list:
  altered=copy.deepcopy(baseline);altered[key]=value[:-1];rejected('list-length/'+key,lambda d=altered:c.result_guard(d,baseline))
# Within-envelope but inconsistent covariance residual must reject independently.
altered=copy.deepcopy(baseline);altered['finite_covariance_identity_float_cross_checks'][0]['difference']+=c.COVARIANCE_ABS_TOL/4
rejected('in-envelope-inconsistent-residual',lambda:c.result_guard(altered,baseline))
tex=(P/'paper.tex').read_text();q=(P/'custody/ROOT_CURRENT_SOURCE_QUALIFICATION.md').read_text();add=(P/'custody/ROOT_SOURCE_VERSION_ADDENDUM_20261014.md').read_text()
c.source_guard(tex,q,add)
for name,t,q_,a in [('conjugation',tex.replace(r'\overline{\widehat h(\xi)}','removed'),q,add),('journal-tail',tex,q,add.replace('Eq30','removed')),('rough-allH',tex.replace(r'H\in(1/4,1)','removed'),q,add),('pairing',tex.replace(r'na\Delta^{2H}','removed'),q,add)]:
 rejected('source/'+name,lambda t=t,q_=q_,a=a:c.source_guard(t,q_,a))
out={'runtime':sys.version,'optimized':not __debug__,'coverage':coverage,'total_nonUTC_leaves':sum(coverage.values()),'all_adversaries_unconditional':True,'rejections':len(records),'records':records,'tolerances_are_finite_acceptance_policy_not_interval_error_bounds':True}
name='GUARDS_'+sys.argv[1]+'.json';(R/name).write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:out[k]for k in ['runtime','optimized','coverage','rejections']}))
