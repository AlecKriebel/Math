import pathlib,json,copy,hashlib,datetime
R=pathlib.Path('/Users/alec/Documents/Math');P=R/'draft_pr_claimed_solved_900_1000_20261012';A=P/'audits/pr948_30004549';D=A/'preprint';O=A/'reviews/full_package_02';core=P/'accept_pr948.py';N={'__name__':'_inert_independent_probe_','__file__':str(core)};exec(compile(core.read_bytes(),str(core),'exec',dont_inherit=True,optimize=0),N)
rows=[]
def yes(v):
 if not v:raise RuntimeError('condition false')
def test(name,f):
 try:f();rows.append({'name':name,'status':'PASS'})
 except Exception as e:rows.append({'name':name,'status':'FAIL','error':repr(e)});raise
def reject(f,fragment=None):
 try:f()
 except (RuntimeError,OSError,ValueError,KeyError,TypeError) as e:
  yes(fragment is None or fragment in str(e));return
 raise RuntimeError('unexpected acceptance')
class Patch:
 def __init__(self,**d):self.d=d
 def __enter__(self):self.old={k:N[k] for k in self.d};N.update(self.d)
 def __exit__(self,*a):N.update(self.old)
res=json.loads((A/'reviews/full_package_01/RESULT.json').read_text())
f=copy.deepcopy(res);f['full_reproducer_completed']=False;f['entire_package_review']=False;f['clean_for_preprint']=False;f['nonclean_history']={'status':'incomplete','explanation':'Actual interruption; no fabricated result.','checks_not_passed':['full_reproducer','entire_package_review']}
test('honest_incomplete_schema_preserves_false_completion',lambda:yes(N['result_schema'](f) is False))
bad=copy.deepcopy(f);bad.pop('nonclean_history');test('missing_nonclean_explanation_rejects',lambda:reject(lambda:N['result_schema'](bad)))
bad=copy.deepcopy(f);bad['clean_for_preprint']=True;test('incomplete_cannot_claim_clean',lambda:reject(lambda:N['result_schema'](bad)))
ctx=N['capture_inventory']('500866df6a5c92a38f133dbe7088da956bc52b54ade02b3fa258a07c3af4e002');B=D/'reviewed_candidates/candidate01';old=json.loads((B/'FREEZE.json').read_text());pin='65add90a6ac3a539cacdc41152cea5828c95cad95608a95e2dad054341a37c02';key=(A/'source_record_private.txt').relative_to(R).as_posix();target=B/'evidence'/key;realread=N['read_regular'];profilecalls=[]
def no_profile(*a,**k):profilecalls.append(1);raise RuntimeError('PROFILE_REACHED')
for label,tamper in [('missing',False),('tampered',True)]:
 def fake(path,*a,**k):
  if pathlib.Path(path)==target:
   if not tamper:raise FileNotFoundError('own simulated missing historical evidence')
   v=realread(path,*a,**k)+b'tamper';N['need'](N['fingerprint'](v)==k['pin'],'simulated historical evidence fingerprint changed');return v
  return realread(path,*a,**k)
 with Patch(read_regular=fake,frozen_profile=no_profile):test('actual_historical_private_'+label+'_rejects_before_profile',lambda:reject(lambda:N['freeze_check']((B/'FREEZE.json').read_bytes(),pin,ctx,B,historical=True)))
yes(not profilecalls)
# All following services are fake dicts/strings. No gh, Git, Sheets, Zenodo or real next-PR reads.
base='b'*40;advanced='c'*40;head='a'*40
meta={'number':949,'state':'OPEN','isDraft':True,'headRefOid':head,'headRefName':'synthetic','baseRefName':'main','baseRefOid':'d'*40,'currentBaseRefOid':base,'url':'https://example.invalid/synthetic'}
oldinv={'number':949,'headRefOid':head,'entries':[{'id':'111'}]};calls=[]
def service(args,**kwargs):
 calls.append(args);return json.dumps({'data':{'repository':{'pullRequest':{**{k:v for k,v in meta.items() if k!='currentBaseRefOid'},'baseRef':{'name':'main','target':{'oid':base}},'changedFiles':1,'files':{'nodes':[{'path':'unsolved_math_prioritization/attempts/222/README.md'}],'pageInfo':{'hasNextPage':False,'endCursor':None}}}}}})
with Patch(run=service):
 test('same_head_missing_initial_livepin_derives_target222',lambda:yes(N['next_identity'](oldinv,meta)=='222' and len(calls)==1))
 calls.clear();test('same_head_valid_matching_livepin_reuses111_without_pages',lambda:yes(N['next_identity']({**oldinv,'currentBaseRefOid':base},meta)=='111' and calls==[]))
 calls.clear();test('stable_live_advance_with_stored_base_fixed_derives222',lambda:yes(N['next_identity']({**oldinv,'currentBaseRefOid':advanced},meta)=='222' and len(calls)==1))
for malformed in [None,'',True,'A'*40,'a'*39]:
 bad={**meta,'currentBaseRefOid':malformed}
 with Patch(run=service):test('malformed_current_livepin_rejects_'+repr(malformed),lambda bad=bad:reject(lambda:N['next_identity'](oldinv,bad)))
def race_service(args,**kw):
 d=json.loads(service(args));d['data']['repository']['pullRequest']['baseRef']['target']['oid']=advanced;return json.dumps(d)
with Patch(run=race_service):test('filename_page_live_only_race_rejects_before_selection',lambda:reject(lambda:N['next_identity'](oldinv,meta),'metadata changed'))
count=[0]
def fakepr(number):
 count[0]+=1;return {**meta,'currentBaseRefOid':base if count[0]==1 else advanced}
def queue_service(args,**kw):
 if any('files(first:100' in x for x in args):return service(args)
 q='| 1 | 222 / SYNTHETIC | title | 0 | 0 | 0 | 0 | unsolved | 0/5 | | | |\n';return json.dumps({'data':{'repository':{'object':{'text':q,'isBinary':False,'byteSize':len(q.encode()),'oid':'e'*40}}}})
with Patch(run=queue_service,pr_view=fakepr):test('final_status_bracket_live_only_race_rejects',lambda:reject(lambda:N['gate_next']([oldinv]),'changed across status-only'))
# Metadata augmentation independently binds gh fields to GraphQL, with stored/live separated.
node={k:v for k,v in meta.items() if k!='currentBaseRefOid'};node['baseRef']={'name':'main','target':{'oid':advanced}}
def views(args,**kw):return json.dumps({k:v for k,v in meta.items() if k!='currentBaseRefOid'}) if args[:3]==['gh','pr','view'] else json.dumps({'data':{'repository':{'pullRequest':node}}})
with Patch(run=views):test('pr_view_normalizes_live_branch_separately_from_stored_base',lambda:yes(N['pr_view'](949)['currentBaseRefOid']==advanced and N['pr_view'](949)['baseRefOid']=='d'*40))
for label,change in [('null_target',lambda n:n['baseRef'].update(target=None)),('missing_base',lambda n:n.pop('baseRef')),('wrong_bound_head',lambda n:n.update(headRefOid='f'*40))]:
 before=copy.deepcopy(node);change(node)
 with Patch(run=views):test('pr_view_'+label+'_rejects',lambda:reject(lambda:N['pr_view'](949)))
 node=before
with Patch(blob=lambda parent,name:b'{"30004549":null}' if name==N['STATE'] else b''):
 test('explicit_native_null_never_means_absent',lambda:reject(lambda:N['native_safety']('fake')))
with Patch(blob=lambda parent,name:b'{}' if name==N['STATE'] else b''):
 test('true_native_absence_retains_UNKNOWN_history',lambda:yes(N['native_safety']('fake')['target_state_absent'] is True and N['native_safety']('fake')['historical_native_turn_count']=='UNKNOWN'))
obj={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','tests':rows,'passed':len(rows),'real_external_service_calls':0,'private_source_body_copied':False,'old_archive_mutated':False,'source_sha256':hashlib.sha256(core.read_bytes()).hexdigest(),'limits':'New inert direct probes supplement complete known regression suites; they do not perform production actions or certify hostile-OS races.'};(O/'INDEPENDENT_PROBES.json').write_text(json.dumps(obj,indent=2)+'\n');print(json.dumps({'status':'PASS','passed':len(rows)}))
