import copy,datetime,hashlib,json,pathlib,sys
O=pathlib.Path(__file__).parent; R=O.parents[4]; P=R/'draft_pr_claimed_solved_900_1000_20261012'; A=P/'audits/pr948_30004549'; D=A/'preprint'; W=A/'publication/workflow'
core=P/'accept_pr948.py'; raw=core.read_bytes(); assert hashlib.sha256(raw).hexdigest()=='3be81538c4e17e6b220208992a8d56422218f37773f84c8a690a4ab10a41d823'
N={'__name__':'_inert_full05_independent_','__file__':str(core)}; exec(compile(raw,str(core),'exec',dont_inherit=True,optimize=0),N)
events=[]
def yes(name,f):
 v=f(); events.append({'name':name,'status':'PASS'}); return v
def reject(name,f):
 try:f()
 except (RuntimeError,ValueError,KeyError,TypeError,OSError) as ex:events.append({'name':name,'status':'REJECTED','message':str(ex)});return
 raise RuntimeError(name+' unexpectedly accepted')
invpin='500866df6a5c92a38f133dbe7088da956bc52b54ade02b3fa258a07c3af4e002'; context=yes('actual seven-source capture',lambda:N['capture_inventory'](invpin))
fpin='1bbfc6c554984f8f8a4a6c467c92ff6e5e87f22b2b79d2d9d91766bf0822e68c'; freeze=yes('actual current freeze validator',lambda:N['freeze_check']((D/'FREEZE.json').read_bytes(),fpin,context))
old=D/'reviewed_candidates/candidate01'; oldraw=(old/'FREEZE.json').read_bytes(); oldpin=hashlib.sha256(oldraw).hexdigest(); oldfreeze=yes('actual historical freeze validator',lambda:N['freeze_check'](oldraw,oldpin,context,old,historical=True))
source=yes('cached local main exact SQLite/source identity (not fresh remote main)',lambda:N['source_gate'](N['run'](['git','rev-parse','HEAD']).strip()))
native=yes('cached local main native baseline (not historical count)',lambda:N['native_safety'](N['run'](['git','rev-parse','HEAD']).strip()))
privatekey=(A/'source_record_private.txt').relative_to(R).as_posix(); target=old/'evidence'/privatekey
fixture=O/'private_fixture';fixture.mkdir(exist_ok=True); tamper=fixture/'tampered.txt';tamper.write_bytes(target.read_bytes()+b'changed')
read=N['read_regular']; profile=N['frozen_profile']; calls=[]
def counted(*args,**kw):calls.append(True);return profile(*args,**kw)
N['frozen_profile']=counted
for label,replacement in [('missing',fixture/'absent.txt'),('tampered',tamper)]:
 def redirected(path,*args,**kw):return read(replacement if pathlib.Path(path)==target else path,*args,**kw)
 N['read_regular']=redirected; calls.clear()
 reject('actual historical private '+label+' rejects using archived authority',lambda:N['freeze_check'](oldraw,oldpin,context,old,historical=True))
 if calls:raise RuntimeError('profile reached before private evidence rejection')
 events.append({'name':'historical '+label+' rejected before profile','status':'PASS'})
N['read_regular']=read;N['frozen_profile']=profile
blob=N['blob']
for value in [None,{},False,0,[],'']:
 N['blob']=lambda ref,name:json.dumps({N['KEY']:value}).encode() if name==N['STATE'] else b''
 reject('present native placeholder '+repr(value),lambda:N['native_safety']('inert'))
N['blob']=lambda ref,name:b'{}' if name==N['STATE'] else b''
yes('true native absence remains UNKNOWN',lambda: N['need'](N['native_safety']('inert')['historical_native_turn_count']=='UNKNOWN','unknown baseline'))
N['blob']=blob
yes('live base pointer ignores stale associated base',lambda:N['need'](N['live_base_pointer']({'baseRefName':'main','baseRefOid':'a'*40,'baseRef':{'name':'main','target':{'oid':'b'*40}}})=='b'*40,'live pointer'))
for val in [None,{},False,0]:reject('invalid actual live base target '+repr(val),lambda:N['live_base_pointer']({'baseRefName':'main','baseRefOid':'a'*40,'baseRef':{'name':'main','target':val}}))
launchers={}; baseline=None
for name,action in [('merge_pr948.py','merge'),('run_pr948_zenodo.py','zenodo'),('append_pr948_tracker.py','tracker'),('update_pr948_publication_ledger.py','native'),('finalize_pr948_and_gate_next.py','finalize')]:
 text=(P/name).read_text(); suffix="entry('"+action+"')";assert text.count(suffix)==1; normalized=text.replace(suffix,"entry('ACTION')");assert baseline is None or normalized==baseline;baseline=normalized;launchers[name]={'selector':action,'sha256':hashlib.sha256(text.encode()).hexdigest()}
events.append({'name':'all five launcher bodies identical except exact action selectors','status':'PASS'})
descriptor,uploads=N['descriptor_check'](freeze);yes('exact descriptor two upload names',lambda:N['need']({x['name'] for x in uploads}=={N['PDF'],N['ZIP']} and len(uploads)==2,'upload closure'))
yes('actual notes have no normalization escape preimage',lambda:N['need']('Python>=3.11' not in descriptor['metadata']['notes'],'preimage'))
reject('changed actual descriptor notes rejected',lambda:N['normalize_notes']({'metadata':{'notes':descriptor['metadata']['notes']+' changed'}},descriptor['metadata']))
out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','count':len(events),'events':events,'actual_current_freeze_files':len(freeze['files']),'actual_historical_frozen_files':len(oldfreeze['files']),'actual_historical_evidence':len(oldfreeze['evidence_files']),'source':source,'native':native,'launchers':launchers,'external_mutations':0,'limits':'Actual validators plus owned local evidence redirects and in-memory fakes; no production action function called. Regression suites are inherited designs; these probes independently target authority and exact absence distinctions.'}
(O/'INDEPENDENT_OPERATIONS.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'count':out['count']}))
