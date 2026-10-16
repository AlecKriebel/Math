from pathlib import Path
import json,copy,datetime,os,io,zipfile,types
R=Path(__file__).parent;A=R.parents[1];P=A.parents[1];D=A/'preprint'
n={'__name__':'review07_direct_inert','__file__':str(P/'accept_pr948.py')};exec(compile((P/'accept_pr948.py').read_bytes(),str(P/'accept_pr948.py'),'exec',dont_inherit=True,optimize=0),n)
f=json.loads((D/'FREEZE.json').read_bytes());pins={'freeze':'1bbfc6c554984f8f8a4a6c467c92ff6e5e87f22b2b79d2d9d91766bf0822e68c','manifest':f['package_manifest_sha256'],'pdf':f['files'][n['PDF']]['sha256']};orig=n['original_check']();auth=json.loads((R/'AUTHENTICATION_START.json').read_bytes());cold=json.loads((R/'COLD_REPLAY.json').read_bytes());checks=[]
def test(name,fn):fn();checks.append({'name':name,'status':'PASS'})
def need(x):
 if not x:raise RuntimeError('own test condition')
def rejects(fn):
 try:fn()
 except (RuntimeError,ValueError,KeyError,TypeError,FileNotFoundError):return
 raise RuntimeError('unexpected acceptance')
def authmut(k,value):
 d=copy.deepcopy(auth);d[k]=value;rejects(lambda:n['review_authentication'](d,pins,f,orig))
for k in ['future_helpers','candidate_files','originals']:test('PASS auth missing '+k,lambda k=k:authmut(k,{}))
test('auth status boolean rejected',lambda:authmut('status',True))
test('auth unknown positive path rejected',lambda:authmut('candidate_files',{**auth['candidate_files'],'outside':{'bytes':1,'sha256':'0'*64}}))
for field,value in [('returncode',False),('observed_outer_optimization',False),('receipt',{})]:
 def check(field=field,value=value):
  d=copy.deepcopy(cold);d['modes'][0][field]=value;rejects(lambda:n['review_cold'](d,pins,f,D))
 test('cold '+field+' typed exactness',check)
def badchild():
 d=copy.deepcopy(cold);d['modes'][2]['receipt']['checker_replays'][1]['runtime']['optimize']=1;rejects(lambda:n['review_cold'](d,pins,f,D))
test('OO canonical nested checker optimization mutation',badchild)
for value in [None,{}, {'baseRefName':'main','baseRef':{'name':'main','target':{'oid':True}}},{'baseRefName':'main','baseRef':{'name':'main','target':{'oid':'F'*40}}},{'baseRefName':'main','baseRef':{'name':'other','target':{'oid':'f'*40}}}]:test('live pointer malformed '+repr(value),lambda value=value:rejects(lambda:n['live_base_pointer'](value)))
test('associated base is independent live base',lambda:need(n['live_base_pointer']({'baseRefName':'main','baseRefOid':'a'*40,'baseRef':{'name':'main','target':{'oid':'b'*40}}})=='b'*40))
oldblob=n['blob']
for value in [None,False,0,{},[],'']:
 def check(value=value):
  n['blob']=lambda parent,path:json.dumps({n['KEY']:value}).encode() if path==n['STATE'] else b''
  try:rejects(lambda:n['native_safety']('a'*40))
  finally:n['blob']=oldblob
 test('present native placeholder rejected '+repr(value),check)
def absence():
 n['blob']=lambda parent,path:b'{}' if path==n['STATE'] else b''
 try:r=n['native_safety']('a'*40);need(r['target_state_absent'] and r['historical_native_turn_count']=='UNKNOWN' and r['new_author_proof_responses']==0)
 finally:n['blob']=oldblob
test('true absence is not historical zero',absence)
for ident in [n['KEY'],int(n['KEY'])]:
 def check(ident=ident):
  n['blob']=lambda parent,path:b'{}' if path==n['STATE'] else json.dumps({'id':ident}).encode()+b'\n'
  try:rejects(lambda:n['native_safety']('a'*40))
  finally:n['blob']=oldblob
 test('target history string/int both rejected '+str(type(ident)),check)
name=(A/'source_record_private.txt').relative_to(P.parent).as_posix();calls=[];oldread=n['read_regular']
def missing(path,**kw):calls.append(str(path));raise FileNotFoundError(str(path))
def oldmissing():
 n['read_regular']=missing
 try:rejects(lambda:n['authenticate_evidence']({name:{'bytes':1,'sha256':'0'*64}},D/'reviewed_candidates/candidate01',True));need(len(calls)==1 and '/candidate01/evidence/' in calls[0])
 finally:n['read_regular']=oldread
test('missing historical private evidence never reads living shadow',oldmissing)
def literals():
 raw='{ "unrelated": {"text":"λ:雪", "nested":[null, false, {"x":"y"}]} , "second": 1e-07 }\n';out=n['replace_entry'](raw,n['KEY'],{'event':'test'});a=n['raw_json_members'](raw);b=n['raw_json_members'](out);need(all(a[k]['literal']==b[k]['literal'] for k in a))
test('unrelated UTF8 nested literals byte preserved',literals)
metadata=json.loads((D/'zenodo-deposit.json').read_bytes())['metadata']
def notes():
 need('Python>=3.11' not in metadata['notes']);bad={'metadata':copy.deepcopy(metadata)};bad['metadata']['notes']+=' &gt; arbitrary';rejects(lambda:n['normalize_notes'](bad,metadata))
test('actual descriptor cannot claim nonexistent notes escape preimage',notes)
expected=[{'name':'proof.pdf','size':1,'sha256':n['sha'](b'p')},{'name':'verify.zip','size':1,'sha256':n['sha'](b'z')}];pub={'id':17,'doi':'10.5281/zenodo.17'};oldget=n['bounded_public_get']
def publiccase(which):
 def fake(url,cap):
  if '/api/records/' in url:return json.dumps({'id':17,'doi':pub['doi'],'metadata':{'title':n['TITLE']},'files':[{'key':x['name']} for x in expected]}).encode(),url,200
  if 'doi.org/' in url:return b'',('https://zenodo.org/records/18' if which=='doi' else 'https://zenodo.org/records/17'),200
  return (b'p' if 'proof.pdf' in url else b'q' if which=='archive' else b'z'),url,200
 n['bounded_public_get']=fake
 try:
  if which=='good':need(n['independent_public_verify'](pub,expected)['confirmed'])
  else:rejects(lambda:n['independent_public_verify'](pub,expected))
 finally:n['bounded_public_get']=oldget
for which in ['good','archive','doi']:test('independent public bytes/DOI '+which,lambda which=which:publiccase(which))
# Actual ZIP verifier must reject implied directory case aliases before opening any member.
profile=n['frozen_profile'](f,D);out=io.BytesIO()
with zipfile.ZipFile(out,'w') as z:
 for name in ['Dir/one','dir/two']:
  info=zipfile.ZipInfo(name);info.create_system=3;info.external_attr=0o100644<<16;z.writestr(info,b'x')
reads=[]
class Spy(zipfile.ZipFile):
 def open(self,*a,**kw):reads.append(a);raise RuntimeError('decompression attempted')
oldzip=profile['zipfile'];profile['zipfile']=types.SimpleNamespace(ZipFile=Spy,ZIP_STORED=zipfile.ZIP_STORED,ZIP_DEFLATED=zipfile.ZIP_DEFLATED)
def zipcheck():
 try:rejects(lambda:profile['inspect_archive'](out.getvalue()));need(not reads)
 finally:profile['zipfile']=oldzip
test('implied ZIP directory alias rejected before decompression',zipcheck)
result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','count':len(checks),'checks':checks,'production_actions':0,'real_service_calls':0,'method':'Independently authored pure-function probes with fake in-memory service/blob replies; no action acceptance/merge/Zenodo/native/tracker/finalize function invoked.'};raw=(json.dumps(result,indent=2)+'\n').encode()
with (R/'INDEPENDENT_PROBES.json').open('wb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
assert (R/'INDEPENDENT_PROBES.json').read_bytes()==raw;print(json.dumps({'status':'PASS','count':len(checks)}))
