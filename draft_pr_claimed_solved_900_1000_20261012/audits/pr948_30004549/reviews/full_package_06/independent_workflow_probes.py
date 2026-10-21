from pathlib import Path
import json,copy,datetime,os,hashlib
P=Path('/Users/alec/Documents/Math/draft_pr_claimed_solved_900_1000_20261012');ROOT=P.parent;A=P/'audits/pr948_30004549';D=A/'preprint';W=A/'publication/workflow';R=A/'reviews/full_package_06';core=P/'accept_pr948.py';raw=core.read_bytes();assert hashlib.sha256(raw).hexdigest()=='3be81538c4e17e6b220208992a8d56422218f37773f84c8a690a4ab10a41d823'
N={'__name__':'_own06_inert_','__file__':str(core)};exec(compile(raw,str(core),'exec',dont_inherit=True,optimize=0),N);rows=[]
def check(name,fn):
 try:fn()
 except Exception as e:rows.append({'test':name,'status':'FAIL','error':repr(e)});save('INDEPENDENT_WORKFLOW_PROBES_FAILURE.json',{'utc':now(),'events':rows});raise
 rows.append({'test':name,'status':'PASS'})
def need(q):
 if not q:raise RuntimeError('unexpected probe result')
def rejects(fn,part=None):
 try:fn()
 except Exception as e:
  if part:need(part in str(e))
  return
 raise RuntimeError('malformed evidence accepted')
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def save(n,z):
 p=R/n;b=(json.dumps(z,indent=2)+'\n').encode();f=p.open('wb');f.write(b);f.flush();os.fsync(f.fileno());f.close();assert p.read_bytes()==b
F=json.loads((D/'FREEZE.json').read_bytes());pins={'freeze':hashlib.sha256((D/'FREEZE.json').read_bytes()).hexdigest(),'manifest':F['package_manifest_sha256'],'pdf':F['files'][N['PDF']]['sha256']};originals=N['original_check']();AUTH=json.loads((R/'AUTHENTICATION_START.json').read_bytes());C=json.loads((R/'COLD_REPLAY.json').read_bytes())
for field in ['utc','original_pr_head','freeze_sha256','package_manifest_sha256','future_helpers','candidate_files','originals']:
 b=copy.deepcopy(AUTH);del b[field];check('authentication_missing_'+field,lambda b=b:rejects(lambda:N['review_authentication'](b,pins,F,originals)))
for name,edit in [('mode_float_optimization',lambda c:c['modes'][1].update(observed_outer_optimization=1.0)),('mode_boolean_returncode',lambda c:c['modes'][0].update(returncode=False)),('canonical_extra_receipt_key',lambda c:c['modes'][0]['receipt'].update(review_only=True)),('canonical_missing_nested_field',lambda c:c['modes'][0]['receipt']['assertion_guard']['runtime'].pop('sympy'))]:
 b=copy.deepcopy(C);edit(b);check(name,lambda b=b:rejects(lambda:N['review_cold'](b,pins,F,D)))
blob=N['blob']
for value in [None,{},False,0,'',[],{'status':None}]:
 N['blob']=lambda ref,path,value=value:json.dumps({N['KEY']:value}).encode() if path==N['STATE'] else b''
 try:check('present_native_placeholder_'+repr(value),lambda:rejects(lambda:N['native_safety']('inert')))
 finally:N['blob']=blob
for key in [N['KEY'],int(N['KEY'])]:
 N['blob']=lambda ref,path,key=key:b'{}' if path==N['STATE'] else json.dumps({'id':key,'status':'unrelated-looking'}).encode()+b'\n'
 try:check('target_history_detected_'+type(key).__name__,lambda:rejects(lambda:N['native_safety']('inert')))
 finally:N['blob']=blob
N['blob']=lambda ref,path:b'{}' if path==N['STATE'] else b''
try:check('true_absence_retains_UNKNOWN',lambda:need(N['native_safety']('inert')['historical_native_turn_count']=='UNKNOWN'))
finally:N['blob']=blob
meta=json.loads((D/'zenodo-deposit.json').read_bytes())['metadata'];dep={'metadata':copy.deepcopy(meta)}
check('metadata_notes_noop',lambda:need(N['normalize_notes'](dep,meta)[1] is False))
for s in [meta['notes']+' ',meta['notes'].replace('3.14.6','3.14.7'),meta['notes'].replace(';','&semi;',1)]:
 b=copy.deepcopy(dep);b['metadata']['notes']=s;check('no_general_notes_normalization_'+str(len(rows)),lambda b=b:rejects(lambda:N['normalize_notes'](b,meta)))
# Arbitrary unrelated literal values/whitespace survive a target-only state update.
before=' { "other" : {"unicode":"Σ", "array":[1, 2]},\n "tail": false }\n';after=N['replace_entry'](before,N['KEY'],{'status':'probe'})
check('native_literal_preservation_unicode_nested',lambda:need(N['raw_json_members'](before)['other']['literal']==N['raw_json_members'](after)['other']['literal'] and N['raw_json_members'](before)['tail']['literal']==N['raw_json_members'](after)['tail']['literal']))
# No living evidence fallback, including a same-hash live shadow. Only archived target may satisfy old evidence.
B=D/'reviewed_candidates/candidate01';old=json.loads((B/'FREEZE.json').read_bytes());name=next(k for k in old['evidence_files'] if k.endswith('source_record_private.txt'));p=B/'evidence'/name;read=N['read_regular'];calls=[]
def missing(path,*args,**kw):
 calls.append(str(path))
 if Path(path)==p:raise FileNotFoundError('own simulated missing archive; live shadow exists')
 return read(path,*args,**kw)
N['read_regular']=missing
try:
 check('historical_absent_snapshot_rejects_with_live_shadow',lambda:rejects(lambda:N['authenticate_evidence']({name:old['evidence_files'][name]},B,True)))
 check('historical_no_living_source_attempted',lambda:need(calls==[str(p)]))
finally:N['read_regular']=read
# Explicit live pointer namespace/format must bind; matching associated base alone is irrelevant.
node={'baseRefName':'main','baseRef':{'name':'main','target':{'oid':'1'*40}},'baseRefOid':'2'*40}
for label,edit in [('wrong_ref_name',lambda n:n['baseRef'].update(name='trunk')),('associated_without_live',lambda n:n.pop('baseRef')),('null_live_oid',lambda n:n['baseRef']['target'].update(oid=None)),('uppercase_live',lambda n:n['baseRef']['target'].update(oid='A'*40))]:
 b=copy.deepcopy(node);edit(b);check(label,lambda b=b:rejects(lambda:N['live_base_pointer'](b)))
check('live_and_associated_pointers_distinct',lambda:need(N['live_base_pointer'](node)!=node['baseRefOid']))
# Exact public bytes and DOI resolution are separate obligations; inert substitution cannot pass.
expected=N['descriptor_check'](F)[1];pub={'id':987654321,'doi':'10.5281/zenodo.987654321'};get=N['bounded_public_get'];pdf=(D/N['PDF']).read_bytes();arc=(D/N['ZIP']).read_bytes()
def fake(url,cap):
 if '/api/records/' in url:return json.dumps({'id':pub['id'],'doi':pub['doi'],'metadata':{'title':N['TITLE']},'files':[{'key':x['name']} for x in expected]}).encode(),url,200
 if '/files/' in url:return (pdf if N['PDF'] in url else arc),url,200
 return b'',f'https://zenodo.org/records/{pub["id"]}',200
N['bounded_public_get']=fake
try:
 check('public_exact_bytes_and_record_positive',lambda:need(N['independent_public_verify'](pub,expected)['confirmed']))
 for label,which in [('PDF','pdf'),('ZIP','zip'),('DOI','doi')]:
  def changed(url,cap,which=which):
   b,final,code=fake(url,cap)
   if (which=='pdf' and '/files/'+N['PDF'] in url) or (which=='zip' and '/files/'+N['ZIP'] in url):b=b[:-1]+bytes([b[-1]^1])
   if which=='doi' and url.startswith('https://doi.org/'):final='https://zenodo.org/records/1'
   return b,final,code
  N['bounded_public_get']=changed;check('public_'+label+'_substitution_rejected',lambda:rejects(lambda:N['independent_public_verify'](pub,expected)))
finally:N['bounded_public_get']=get
save('INDEPENDENT_WORKFLOW_PROBES.json',{'utc':now(),'status':'PASS','passed':len(rows),'events':rows,'production_actions':0,'live_service_calls':0,'scope':'New direct inert probes, in addition to five inherited regression suite designs; all original dependencies loaded inertly with original absolute __file__.'});print(json.dumps({'status':'PASS','passed':len(rows)}))
