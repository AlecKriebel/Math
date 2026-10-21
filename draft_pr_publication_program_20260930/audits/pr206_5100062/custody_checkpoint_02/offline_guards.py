"""Bounded offline tests of pure guards only; never run a real helper phase."""
from pathlib import Path
import ast, copy, hashlib, json, os, stat, sys, tempfile, types

D=Path(__file__).absolute().parent
source=(D/'custody206.py').read_bytes()
m=types.ModuleType('pr206_prepared_pure_guards')
m.__file__=str(D/'custody206.py')
exec(compile(source,m.__file__,'exec'),m.__dict__)
results=[]


def need(ok,message):
    if not ok:raise RuntimeError(message)


def check(name,callback):
    callback();results.append({'name':name,'pass':True})


def same(a,b):need(a==b,'Expected equality')


def reject(name,callback):
    def run():
        try:callback()
        except (RuntimeError,ValueError,FileNotFoundError,NotADirectoryError,OSError):return
        raise RuntimeError('Expected guard rejection: '+name)
    check(name,run)


def mutate(d,**kw):
    result=copy.deepcopy(d);result.update(kw);return result


check('No default authority or backend',lambda:same((m._authority_pin,m._backend),(None,None)))
reject('Missing future Root adoption fails closed',m.authority)
reject('Runtime cannot start with missing authority/backend',m.runtime)
for node in ast.walk(ast.parse(source)):
    if isinstance(node,ast.ImportFrom):need(node.module=='pathlib','Unexpected from import')
    if isinstance(node,ast.Import):need(all(x.name in {'base64','copy','datetime','hashlib','json','os','re','stat','sys','tempfile'} for x in node.names),'Unexpected import')
check('Only fixed standard-library imports',lambda:same(True,True))
check('Five separately named phase definitions',lambda:same(len([n for n in ast.parse(source).body if isinstance(n,ast.FunctionDef) and n.name in ('prepare','verify','accept','sync','pointer')]),5))
check('Exact actual205 baseline constants',lambda:same((m.BASE_COMMIT,m.BASE_TREE,m.BASE_DIGEST),('08a17b535ca650d98cf3ec2439e2865b31111e2a','28ccd52bdfa41d70c9e744d6be373cb19fcbe0c9','27784963c9e2b2d0d4140a814fc054214f4d2e0dfc5ea465af1924a14d7b4f3e')))
for bad in ('../escape','/absolute','a//b','a/./b','a/../b','a\\b','a\0b',''):
    reject('Unsafe path '+repr(bad),lambda bad=bad:m.rel(bad))
for bad in ('../gen','Upper','a-b','a'*50,'','with space'):
    reject('Unsafe generation '+repr(bad),lambda bad=bad:m.generation(bad))
reject('Boolean byte length refused',lambda:m.bytepin({'bytes':True,'sha256':'0'*64}))
reject('Extra byte-pin key refused',lambda:m.bytepin({'bytes':1,'sha256':'0'*64,'git_blob':'0'*40}))
reject('Duplicate JSON keys refused',lambda:m.decode(b'{"a":1,"a":2}'))
reject('Nonfinite JSON refused',lambda:m.decode(b'{"a":NaN}'))
reject('Oversized selected map refused',lambda:m.digest({str(i):m.bpin(b'x') for i in range(m.MAX_SELECTED+1)}))

q=json.loads((D.parent/m.COLLECTOR/'ORIGINAL_QUEUE_SINGLE_ROW_RECEIPT_PROPOSAL.json').read_bytes())
base=q['base_own_row']['text'].encode();head=q['original_QUEUE_row']['text'].encode()
check('Actual own BASE123 pin',lambda:same(m.pin(base),m.BASE_ROW))
check('Actual own submitted HEAD511 eligibility pin',lambda:same(m.pin(head),m.HEAD_ROW))
foreign=base.replace(b'5100062 / AMR-050-0062',b'9999999 / AMR-999-9999')
protected=base.replace(b'5100062 / AMR-050-0062',b'30004690 / AMR-999-9998')
before=b'heading\n'+base+foreign+protected
sel={m.Q:m.bpin(before),m.NATIVE+'30004690/proof.md':m.bpin(b'p')}
after=before.replace(foreign,foreign.replace(b'queued',b'claimed_solved'))
check('Unchanged QUEUE accepted',lambda:same(m.reconcile_rows(before,before,sel),[]))
check('Only unprotected foreign row reconciled',lambda:same([r['problem_id'] for r in m.reconcile_rows(before,after,sel)],['9999999']))
reject('Own HEAD row refused as MAIN preimage',lambda:m.reconcile_rows(before,before.replace(base,head),sel))
reject('Own arbitrary queued row refused',lambda:m.reconcile_rows(before,before.replace(base,base.replace(b'0/5',b'1/5')),sel))
reject('Protected native foreign row cannot change',lambda:m.reconcile_rows(before,before.replace(protected,protected.replace(b'queued',b'claimed_solved')),sel))
reject('Foreign row retargeting refused',lambda:m.reconcile_rows(before,before.replace(foreign,foreign.replace(b'9999999',b'9999998')),sel))
reject('QUEUE header mutation refused',lambda:m.reconcile_rows(before,before.replace(b'heading',b'changed'),sel))
reject('QUEUE insertion refused',lambda:m.reconcile_rows(before,before+b'new\n',sel))
reject('Duplicate own rows refused',lambda:m.reconcile_rows(base+base,base+base,sel))
reject('Missing own row refused',lambda:m.reconcile_rows(foreign,foreign,sel))

prior={'current_PR':205,'current_PR_workflow_percent':100,'fully_completed_count':48,'published_count':32,'last_completed_PR':205,'next_numeric_intake_cursor':206,'advance_to_next_PR_authorized_now':True,'current_DOI':'OLD205','current_unrecognized_gate':True,'conditional_next_numeric_intake_cursor':206,'program_snapshot_old':'OLD205','last_completed_DOI':'PRESERVE205','published_PRs':[205],'current_whole_package_review_events':['OLD205']}
case,progress=m.project(prior,'FIXED_TIME')
check('Custody10 counters and no advancement',lambda:same({k:progress[k] for k in m.COUNTS},m.COUNTS))
check('Custody10 original DAG distinction',lambda:same((case['declared_PR_base'],case['authenticated_authored_range_base'],case['original_author_commit_count']),(m.DECLARED,m.FORK,4)))
check('Prior live aliases retired to history',lambda:same((progress['current_DOI'],progress.get('current_unrecognized_gate'),progress.get('conditional_next_numeric_intake_cursor')),(None,None,None)))
check('Historical publication authority preserved',lambda:same((progress['last_completed_DOI'],progress['published_PRs']),('PRESERVE205',[205])))
check('No scientific gates or whole-package events',lambda:same((case['mathematical_clearance'],case['priority_clearance'],case['source_contract_clearance'],case['publication_ready'],case['NEW_whole_package_reviews_completed'],progress['current_whole_package_review_events']),(False,False,False,False,0,[])))
check('Projection leaves prior input unchanged',lambda:same(prior['current_DOI'],'OLD205'))
reject('Wrong prior completion refused',lambda:m.project(mutate(prior,current_PR_workflow_percent=98),'t'))
reject('Wrong prior counts refused',lambda:m.project(mutate(prior,published_count=33),'t'))

path=m.CASE+'new_evidence.md';out={path:b'original custody'};expected={path:m.bpin(out[path]),m.Q:m.bpin(before)}
r={'commit':'1'*40,'expected_main':'2'*40,'tree':'3'*40,'parent_tree':'4'*40,'changed_paths':[path]}
co={'sha':r['commit'],'parents':[{'sha':r['expected_main']}],'tree':{'sha':r['tree']},'message':m.message(m.digest(expected))}
def identity(rr=r,cc=co,changes=None,actual=None,oo=out,pt='4'*40):
    return m.check_candidate_identity(rr,cc,pt,expected,{path} if changes is None else changes,{path} if actual is None else actual,oo)
check('Exact true-parent and full changed-leaf scope accepted',identity)
for label,cc in [('two parents',mutate(co,parents=[{'sha':'2'*40},{'sha':'9'*40}])),('wrong parent',mutate(co,parents=[{'sha':'9'*40}])),('wrong tree',mutate(co,tree={'sha':'9'*40})),('wrong message',mutate(co,message='forged')),('wrong commit',mutate(co,sha='9'*40))]:
    reject('Candidate '+label+' refused',lambda cc=cc:identity(cc=cc))
reject('Native parent-tree drift refused',lambda:identity(pt='9'*40))
reject('Full foreign changed-leaf addition refused',lambda:identity(actual={path,'foreign.txt'}))
reject('Prepared changed-leaf omission refused',lambda:identity(rr=mutate(r,changed_paths=[])))
reject('Duplicate prepared changed leaf refused',lambda:identity(rr=mutate(r,changed_paths=[path,path])))
for prohibited in (m.Q,m.NATIVE+'5100062/CANDIDATE.md'):
    reject('QUEUE/native mutation refused '+prohibited,lambda prohibited=prohibited:identity(rr=mutate(r,changed_paths=[prohibited]),changes={prohibited},actual={prohibited},oo={prohibited:b'x'}))
reject('Foreign overlay path refused',lambda:m.expected_map({}, {'foreign.txt':b'x'}))
reject('Inherited immutable selected overwrite refused',lambda:m.expected_map({path:m.bpin(b'old')},out))
check('Explicit global view replacement permitted',lambda:same(m.expected_map({m.VIEWS[2]:m.bpin(b'old')},{m.VIEWS[2]:b'new'})[m.VIEWS[2]],m.bpin(b'new')))
reject('Oversized overlay refused',lambda:m.expected_map({}, {m.CASE+str(i):b'x' for i in range(m.MAX_OVERLAY+1)}))
api_calls=[]
no_api=types.SimpleNamespace(api=lambda *a,**k:api_calls.append((a,k)))
for endpoint,method in [('git/refs/heads/main','PATCH'),('pulls/206','POST'),('git/refs','POST'),('users/private','GET')]:
    reject('Forbidden endpoint blocked before backend '+endpoint+method,lambda endpoint=endpoint,method=method:m.api(no_api,endpoint,method,{}))
check('Forbidden endpoint fixtures never reached injected API',lambda:same(api_calls,[]))

adopted=m.obj(m.CASE+m.CUSTODY_ADOPTION,{'bytes':7681,'sha256':'0fd72466f97cc302e61124eeac7f6fd06820e3d9f819127296bde3b77d72e12a'})
actual_material,actual_files=m.originals(({},adopted))
check('Actual Root-adopted custody35 materials and21 exact blobs read only',lambda:same((len(actual_material),len(actual_files)),(35,21)))
bad_adopted=copy.deepcopy(adopted);bad_adopted['material']['private/full_map.json']={'bytes':0,'sha256':'0'*64}
reject('Extra raw/private material cannot enter custody overlay',lambda:m.originals(({},bad_adopted)))

receipt_ack={'UTC':'2026-10-16T20:00:00+00:00','baseline_actual_commit':r['commit'],'observed_MAIN':'5'*40,'old_QUEUE':expected[m.Q],'current_QUEUE':expected[m.Q],'foreign_unprotected_row_changes':[],'own_BASE123_and_all_protected_QUEUE_bytes_unchanged':True,'custody_writes_no_QUEUE':True}
mapping={'selected_files':expected,'selected_map_sha256':m.digest(expected),'foreign_QUEUE_reconciliation_after_checkpoint':receipt_ack}
receipt={'schema':'pr206-actual-custody10-acceptance-v2','evidence_scope':'ACTUAL_HELPER_NATIVE_RECHECK','UTC':'2026-10-16T20:00:00+00:00','sole_parent':r['expected_main'],'original_head':m.HEAD,'main_observed':'5'*40,'actual_tree':'6'*40,'selected_files':len(expected),'actual_current_map_file':m.pin(m.enc(mapping)),'accepted':True,'PR':206,'case_percent':10,'checkpoint_commit':r['commit'],'every_selected_identity_checked_at_actual_observed_MAIN':True,'full_foreign_tree_scope_preserved':True,'all_overlay_body_identities_verified':True,'QUEUE_native_original_PR_unchanged':True,'mathematical_clearance':False,'source_contract_clearance':False,'priority_clearance':False,'publication_ready':False,'NEW_whole_package_reviews_completed':0,'actual_current_selected_map_sha256':m.digest(expected),**m.COUNTS}
check('Own actual full acceptance factual guard accepts fixture',lambda:m.check_acceptance(receipt,mapping,r,expected))
for key,value in [('accepted',False),('PR',205),('case_percent',5),('checkpoint_commit','9'*40),('every_selected_identity_checked_at_actual_observed_MAIN',False),('full_foreign_tree_scope_preserved',False),('all_overlay_body_identities_verified',False),('QUEUE_native_original_PR_unchanged',False),('mathematical_clearance',True),('source_contract_clearance',True),('priority_clearance',True),('publication_ready',True),('NEW_whole_package_reviews_completed',1),('fully_completed_count',49),('published_count',33),('next_numeric_intake_cursor',207),('advance_to_next_PR_authorized_now',True)]:
    reject('Acceptance drift refused '+key,lambda key=key,value=value:m.check_acceptance(mutate(receipt,**{key:value}),mapping,r,expected))
reject('Acceptance current selected digest drift refused',lambda:m.check_acceptance(receipt,mutate(mapping,selected_map_sha256='0'*64),r,expected))

# V1 adversary's truncation, extension, non-QUEUE mutation and missing-field witnesses.
full_prepared={**expected,m.NATIVE+'30004690/proof.md':m.bpin(b'protected proof')}
full_mapping={**mapping,'selected_files':full_prepared,'selected_map_sha256':m.digest(full_prepared)}
full_receipt={**receipt,'selected_files':len(full_prepared),'actual_current_selected_map_sha256':m.digest(full_prepared),'actual_current_map_file':m.pin(m.enc(full_mapping))}
check('V2 complete three-path prepared map accepted',lambda:m.check_acceptance(full_receipt,full_mapping,r,full_prepared))
for label,forged in [('QUEUE-only truncation',{m.Q:full_prepared[m.Q]}),('extra selected path',{**full_prepared,m.CASE+'extra.md':m.bpin(b'rogue')}),('changed non-QUEUE native pin',{**full_prepared,m.NATIVE+'30004690/proof.md':m.bpin(b'changed protected proof')})]:
    forged_mapping={**full_mapping,'selected_files':forged,'selected_map_sha256':m.digest(forged)}
    forged_receipt={**full_receipt,'selected_files':len(forged),'actual_current_selected_map_sha256':m.digest(forged),'actual_current_map_file':m.pin(m.enc(forged_mapping))}
    reject('V1 forged map witness rejected: '+label,lambda a=forged_receipt,b=forged_mapping:m.check_acceptance(a,b,r,full_prepared))
for field in sorted(full_receipt):
    incomplete={k:v for k,v in full_receipt.items() if k!=field}
    reject('Missing acceptance field rejected: '+field,lambda a=incomplete:m.check_acceptance(a,full_mapping,r,full_prepared))
for key,value in [('schema','pr206-actual-custody10-acceptance-v1'),('evidence_scope','PREPARATION_ONLY'),('sole_parent','9'*40),('original_head','9'*40),('main_observed','not-a-native-SHA'),('actual_tree','not-a-native-SHA'),('selected_files',1),('selected_files',True),('NEW_whole_package_reviews_completed',False),('advance_to_next_PR_authorized_now',0)]:
    reject('Strict receipt binding/type rejected: '+key+repr(value),lambda key=key,value=value:m.check_acceptance(mutate(full_receipt,**{key:value}),full_mapping,r,full_prepared))
reject('Extra receipt field rejected',lambda:m.check_acceptance(mutate(full_receipt,unadopted_extra=True),full_mapping,r,full_prepared))
reject('Extra acceptance-map record field rejected',lambda:m.check_acceptance(full_receipt,mutate(full_mapping,extra=True),r,full_prepared))

native_receipt_commit={'sha':full_receipt['main_observed'],'tree':{'sha':full_receipt['actual_tree']}}
check('Native receipted MAIN/tree and checkpoint ancestry accepted',lambda:m.check_receipted_commit(full_receipt,r,native_receipt_commit,'ahead'))
reject('Receipted native commit SHA mismatch rejected',lambda:m.check_receipted_commit(full_receipt,r,mutate(native_receipt_commit,sha='9'*40),'ahead'))
reject('Receipted native tree mismatch rejected',lambda:m.check_receipted_commit(full_receipt,r,mutate(native_receipt_commit,tree={'sha':'9'*40}),'ahead'))
for status in ('diverged','behind','unrelated'):
    reject('Receipted checkpoint ancestry rejected: '+status,lambda status=status:m.check_receipted_commit(full_receipt,r,native_receipt_commit,status))

# V1 bad->bad receipt-baseline laundering passed its continuity guard. V2 must
# always begin at the original checkpoint's full protected map and good QUEUE.
bad_protected_queue=before.replace(protected,protected.replace(b'queued',b'claimed_solved'))
check('Historical bad-to-bad laundering mechanism preserved as evidence',lambda:same(m.reconcile_rows(bad_protected_queue,bad_protected_queue,full_prepared),[]))
reject('Original checkpoint good-to-receipted bad protected QUEUE rejected',lambda:m.reconcile_rows(before,bad_protected_queue,full_prepared))
check('Original checkpoint good-to-receipted permitted foreign row accepted',lambda:same([x['problem_id'] for x in m.reconcile_rows(before,after,full_prepared)],['9999999']))
check('Receipt map matches independently derived complete map',lambda:m.check_receipted_map(full_mapping,full_prepared,receipt_ack))
forged_q_map={**full_mapping,'selected_files':{**full_prepared,m.Q:m.bpin(bad_protected_queue)}}
reject('Supplied bad QUEUE pin cannot replace independently reconstructed state',lambda:m.check_receipted_map(forged_q_map,full_prepared,receipt_ack))
reject('Forged recorded QUEUE continuity acknowledgement rejected',lambda:m.check_receipted_map({**full_mapping,'foreign_QUEUE_reconciliation_after_checkpoint':{**receipt_ack,'foreign_unprotected_row_changes':['forged']}},full_prepared,receipt_ack))

accepted_node=next(n for n in ast.parse(source).body if isinstance(n,ast.FunctionDef) and n.name=='_accepted_context')
accepted_text=ast.unparse(accepted_node)
check('Accepted context binds full prepared expected map before reconstruction',lambda:same('check_acceptance(receipt, mapping, r, expected)' in accepted_text,True))
check('Accepted context reconstructs starting at original checkpoint full expected',lambda:same("{'commit': r['commit'], 'tree': r['tree'], 'selected_files': expected}" in accepted_text,True))
check('Accepted context passes independently reconstructed complete map to fresh checks',lambda:same("_actual(c, h, material, r, reconstructed, received, receipt['actual_tree'])" in accepted_text,True))
actual_node=next(n for n in ast.parse(source).body if isinstance(n,ast.FunctionDef) and n.name=='_actual')
check('Subsequent fresh MAIN must retain authenticated receipt ancestry',lambda:same("'compare/' + base_commit + '...' + main" in ast.unparse(actual_node),True))

original_root=m.ROOT
with tempfile.TemporaryDirectory(prefix='offline_guard_fixture_',dir=D) as dirname:
    m.ROOT=Path(dirname)
    for name in m.VIEWS:(m.ROOT/name).parent.mkdir(parents=True,exist_ok=True)
    def reset():
        for index,name in enumerate(m.VIEWS):
            f=m.ROOT/name
            if f.is_symlink() or f.is_file():f.unlink()
            elif f.exists():f.rmdir()
            if index:
                f.write_bytes(('old'+str(index)).encode());f.chmod(0o644)
    def images():
        return [(name,None if index==0 else m.pin(('old'+str(index)).encode()),('post'+str(index)).encode()) for index,name in enumerate(m.VIEWS)]
    reset()
    check('Absent new CURRENT and preexisting own-log atomic five sync',lambda:same(len(m.sync_images(images())),5))
    check('All five postimages are readonly regular files',lambda:same(all(stat.S_ISREG((m.ROOT/n).lstat().st_mode) and stat.S_IMODE((m.ROOT/n).lstat().st_mode)==0o444 for n in m.VIEWS),True))
    check('Per-file sync retry allows exact postimages',lambda:same(len(m.sync_images(images())),5))
    for kind in ('symlink','dangling_symlink','directory','fifo'):
        reset();bad=m.ROOT/m.VIEWS[-1];bad.unlink()
        if kind=='symlink':bad.symlink_to(m.ROOT/m.VIEWS[1])
        elif kind=='dangling_symlink':bad.symlink_to(m.ROOT/'absent')
        elif kind=='directory':bad.mkdir()
        else:os.mkfifo(bad)
        reject('All-five precheck rejects '+kind,lambda:m.sync_images(images()))
        check('No earlier view replacement on '+kind,lambda:same(((m.ROOT/m.VIEWS[0]).exists(),(m.ROOT/m.VIEWS[1]).read_bytes()),(False,b'old1')))
        if kind=='directory':bad.rmdir()
        else:bad.unlink()
    reset()
    reject('Stale per-file preimage refused',lambda:m.atomic(m.VIEWS[1],b'new',m.pin(b'stale')))
    check('Stale per-file refusal preserves bytes',lambda:same((m.ROOT/m.VIEWS[1]).read_bytes(),b'old1'))
    reset();real_replace=m.os.replace;count=[0]
    def failing_replace(src,dst):
        count[0]+=1
        if count[0]==2:raise OSError('Synthetic second replacement failure')
        return real_replace(src,dst)
    m.os.replace=failing_replace
    try:reject('Mid-sync failure produces no successful result',lambda:m.sync_images(images()))
    finally:m.os.replace=real_replace
    check('Explicit per-file atomicity limit preserves completed first write',lambda:same((m.ROOT/m.VIEWS[0]).read_bytes(),b'post0'))
    check('No abandoned temporary file after failure',lambda:same([f.name for f in Path(dirname).rglob('*') if '.pr206_' in f.name],[]))
    reset()
    fake_h=types.SimpleNamespace(api=lambda *a,**k:(_ for _ in ()).throw(RuntimeError('Unexpected API')))
    remote={name:None if index<2 else ('old'+str(index)).encode() for index,name in enumerate(m.VIEWS)}
    auth=({'initial_local_case_views':{m.VIEWS[0]:None,m.VIEWS[1]:m.pin(b'old1')}},{})
    real_body=m.body;m.body=lambda h,path,parent:remote[path]
    try:
        check('New-case localNone and adopted Root log preimages accepted',lambda:same(m.local_preimages(fake_h,'parent',auth)[m.VIEWS[0]],None))
        (m.ROOT/m.VIEWS[-1]).write_bytes(b'drift')
        reject('Global third preimage drift refused before any write',lambda:m.local_preimages(fake_h,'parent',auth))
        reset();(m.ROOT/m.VIEWS[1]).write_bytes(b'unadopted Root log')
        reject('Unadopted preexisting own Root log refused',lambda:m.local_preimages(fake_h,'parent',auth))
    finally:m.body=real_body
m.ROOT=original_root

report={'schema':'pr206-custody10-pure-offline-guards-v1','optimization':sys.flags.optimize,'checks':len(results),'all_pass':all(x['pass'] for x in results),'results':results,'limits':['No real phase function, actual backend import/injection, API, adapter, ref, PR, MAIN, global five or pointer operation executed.','Filesystem guard fixtures exist only in an automatically removed fresh subfolder of custody_checkpoint_02.','Synthetic factual guards do not certify a future Root dispatcher, six aliases, cache cleanup, remote lease/CAS or native transport.','Atomicity is per file; a mid-sync failure can leave earlier valid postimages. No success receipt is written by the guard primitive.','Actual Root adoption, complete native candidate/acceptance checks and external expected-SHA nonforce CAS remain mandatory.'],'source':{'bytes':len(source),'sha256':hashlib.sha256(source).hexdigest()}}
print(json.dumps(report,indent=2,sort_keys=True))
