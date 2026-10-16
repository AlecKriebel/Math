"""New matrix and inert schema probes. Never invoke action functions."""
from pathlib import Path
import copy,datetime,hashlib,json
import sympy as s
R=Path('/Users/alec/Documents/Math');P=R/'draft_pr_claimed_solved_900_1000_20261012'
A=P/'audits/pr948_30004549';D=A/'preprint';O=A/'reviews/full_package_03'
rows=[]
def check(name,value):
 if not value:raise RuntimeError(name)
 rows.append({'name':name,'status':'PASS'})
def reject(name,call):
 try:call()
 except (RuntimeError,ValueError,KeyError,TypeError,OSError):check(name,True);return
 raise RuntimeError('Unexpected acceptance '+name)
core=P/'accept_pr948.py';raw=core.read_bytes();check('current_core_pin',hashlib.sha256(raw).hexdigest()=='3be81538c4e17e6b220208992a8d56422218f37773f84c8a690a4ab10a41d823')
N={'__name__':'_review03_inert_','__file__':str(core)};exec(compile(raw,str(core),'exec',dont_inherit=True,optimize=0),N)
f=json.loads((D/'FREEZE.json').read_text());pins={'freeze':'1bbfc6c554984f8f8a4a6c467c92ff6e5e87f22b2b79d2d9d91766bf0822e68c','manifest':f['package_manifest_sha256'],'pdf':f['files'][N['PDF']]['sha256']}
originals=N['original_check']();auth=json.loads((O/'AUTHENTICATION_START.json').read_text());cold=json.loads((O/'COLD_REPLAY.json').read_text())
check('actual_start_schema',N['review_authentication'](auth,pins,f,originals)[0]);check('actual_cold_schema',N['review_cold'](cold,pins,f,D)[0])
for label,edit in [('missing_original',lambda x:x['originals'].pop(next(iter(x['originals'])))),('archive_identity_false',lambda x:x['originals'][next(iter(x['originals']))].update(disk_and_archive_match=False)),('archive_mode_wrong',lambda x:x['originals'][next(iter(x['originals']))].update(archive_mode='0644')),('helper_subset',lambda x:x['future_helpers'].pop('merge_pr948.py'))]:
 bad=copy.deepcopy(auth);edit(bad);reject('PASS_auth_'+label,lambda bad=bad:N['review_authentication'](bad,pins,f,originals))
for label,edit in [('extra_receipt_field',lambda x:x['modes'][0]['receipt'].update(invented=True)),('bool_optimization',lambda x:x['modes'][0].update(observed_outer_optimization=False)),('missing_mode',lambda x:x['modes'].pop()),('ignored_field',lambda x:x.update(normalized_fields_ignored=['runtime'])),('wrong_order',lambda x:x['modes'].reverse())]:
 bad=copy.deepcopy(cold);edit(bad);reject('PASS_cold_'+label,lambda bad=bad:N['review_cold'](bad,pins,f,D))
partial=copy.deepcopy(auth);partial.update(status='INCOMPLETE',future_helpers={},candidate_files={},originals={},explanation='Stopped before closing checks.',observations={'checked':'none'})
check('honest_partial_no_clean_credit',N['review_authentication'](partial,pins,f,originals)[0] is False)
partial['status']='PASS';reject('partial_cannot_claim_PASS',lambda:N['review_authentication'](partial,pins,f,originals))
B=D/'reviewed_candidates/candidate01';oldraw=(B/'FREEZE.json').read_bytes();oldpin=hashlib.sha256(oldraw).hexdigest();context=N['capture_inventory']('500866df6a5c92a38f133dbe7088da956bc52b54ade02b3fa258a07c3af4e002')
read=N['read_regular'];profile=N['frozen_profile'];observed=[];target=B/'evidence'/str((A/'source_record_private.txt').relative_to(R))
def missing(path,*args,**kw):
 if Path(path)==target:raise FileNotFoundError('simulated missing private historical snapshot')
 return read(path,*args,**kw)
def counted(*args,**kw):observed.append('profile');return profile(*args,**kw)
N['read_regular']=missing;N['frozen_profile']=counted
try:reject('actual_historical_private_missing',lambda:N['freeze_check'](oldraw,oldpin,context,B,historical=True))
finally:N['read_regular']=read;N['frozen_profile']=profile
check('missing_private_before_profile',observed==[])
# Reconstruct J from independently populated skew matrices; h>0 parametrizes D.
a,c=s.symbols('a c',real=True);h=s.symbols('h',positive=True);b=1-c*c/4-h*h
Alpha=s.zeros(4);Beta=s.zeros(4)
for i,j,v in [(0,2,1),(1,3,-1)]:Alpha[i,j]=v;Alpha[j,i]=-v
for i,j,v in [(0,3,1),(1,2,1-b),(1,3,-c),(0,1,a)]:Beta[i,j]=v;Beta[j,i]=-v
Bnorm=(Beta-c*Alpha/2)/h;J=-Alpha.inv()*Bnorm;zero=lambda m:all(s.simplify(x)==0 for x in m)
check('full_cutoff_J_squared',zero(J*J+s.eye(4)));check('full_cutoff_alpha_anti',zero(J.T*Alpha*J+Alpha));check('full_cutoff_beta_anti',zero(J.T*Beta*J+Beta));check('kernel_sign',zero(J.T*Alpha+Bnorm))
check('zero_parameter_product',J.subs({a:0,c:0,h:1})==s.Matrix([[0,-1,0,0],[1,0,0,0],[0,0,0,-1],[0,0,1,0]]))
e,x=s.symbols('e x',real=True);k=1-e*x;Jcore=J.subs({a:0,c:0,h:s.sqrt(k)});coord=s.symbols('u v x t',real=True)
def bracket(U,V):return s.Matrix([sum(U[j]*s.diff(V[i],coord[j])-V[j]*s.diff(U[i],coord[j]) for j in range(4)) for i in range(4)])
U=s.eye(4)[:,0];X=s.eye(4)[:,2];tensor=bracket(Jcore*U,Jcore*X)-Jcore*bracket(Jcore*U,X)-Jcore*bracket(U,Jcore*X)
check('independent_Nijenhuis',zero(tensor+e/(2*k)*U))
for sign in [-1,1]:check('origin_sign_'+str(sign),tensor.subs({x:0,e:s.Rational(sign,10)})[0]==-s.Rational(sign,20))
check('zero_Nijenhuis_limit',zero(tensor.subs(e,0)))
obj={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','passed':len(rows),'tests':rows,'external_calls':0,'action_functions_called':False,'candidate_bytes_mutated':False,'limits':'Finite independent matrix/schema probes supplement the global proof; no action authorization or priority certificate.'}
(O/'INDEPENDENT_PROBES.json').write_text(json.dumps(obj,indent=2)+'\n');print(json.dumps({'status':'PASS','passed':len(rows)}))
