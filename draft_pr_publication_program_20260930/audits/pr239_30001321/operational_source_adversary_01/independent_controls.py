"""Independent SOURCE-ONLY controls. No Seed/Runtime, CLI, network, project lock,
Git operation, provider/tracker/PR/ref action or global-five write is invoked.
All constructed values and raw-commit fixtures are offline test data only.
"""
import ast, base64, copy, datetime, hashlib, json, os, re, stat, sys, types
from pathlib import Path

OWN=Path(__file__).absolute().parent
SRC=OWN.parent/'operational_source_preparation_01'

def enc(v): return (json.dumps(v,sort_keys=True,indent=2)+'\n').encode()
def pin(b): return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def module(file):
    p=SRC/file;m=types.ModuleType('offline_'+file.replace('.','_'));m.__file__=str(p)
    exec(compile(p.read_bytes(),str(p),'exec'),m.__dict__);return m

results=[]
def yes(name,fn):
    value=fn()
    if value is False: raise AssertionError(name)
    results.append({'name':name,'result':'PASS'})
def no(name,fn):
    try: fn()
    except (RuntimeError,ValueError,KeyError,TypeError,IndexError):
        results.append({'name':name,'result':'EXPECTED_REFUSAL'});return
    raise AssertionError('Unexpected acceptance: '+name)

def main():
    h=module('native239_model.py');q=module('completion_checkpoint.py')
    t=module('ROOT_TERMINAL_INSPECTION.py');u=module('completion_consumer.py')
    c=module('native_trees_readonly.py');x=module('concurrent_get_extension.py')
    manifest_raw=(SRC/'SOURCE_MANIFEST.json').read_bytes();sm=json.loads(manifest_raw)
    yes('frozen manifest exact external pin',lambda:pin(manifest_raw)=={'bytes':3198,'sha256':'96b0b248f390f67860b435b57cde34b2d2142206b9fc5c8166417f9c98d0db6c'})
    yes('frozen seal exact external pin',lambda:pin((SRC/'EXTERNAL_SEAL.json').read_bytes())=={'bytes':390,'sha256':'4e04f1655cf7d87de5afcf23a20dca431d034a4673929d98746c9ad689379a34'})
    yes('positive finite closure19/476858',lambda:len(sm['files'])==19 and sum(r['bytes'] for r in sm['files'])==476858 and sm['total_files']==19 and sm['total_bytes']==476858)
    for row in sm['files']:
        p=SRC/row['path'];b=p.read_bytes()
        yes('payload exact bytes/mode '+row['path'],lambda p=p,b=b,row=row:pin(b)=={k:row[k] for k in ('bytes','sha256')} and p.is_file() and not p.is_symlink() and stat.S_IMODE(p.stat().st_mode)==0o444)
    refs=json.loads((SRC/'REFERENCE_PINS.json').read_text())
    for row in refs['files']+refs['new_publication_history_references']:
        yes('reference pin '+Path(row['path']).name+' '+row['sha256'][:8],lambda row=row:pin(Path(row['path']).read_bytes())=={k:row[k] for k in ('bytes','sha256')})
    # Recompute every advertised symbol AST identity, rather than trusting labels.
    provenance=json.loads((SRC/'PROVENANCE.json').read_text());counts={}
    for f in provenance['files']:
        new=ast.parse((SRC/f['current']).read_text());old=ast.parse(Path(f['reference']).read_text())
        nm={n.name:n for n in new.body if isinstance(n,(ast.FunctionDef,ast.ClassDef,ast.AsyncFunctionDef))}
        om={n.name:n for n in old.body if isinstance(n,(ast.FunctionDef,ast.ClassDef,ast.AsyncFunctionDef))}
        yes('all production symbols represented '+f['current'],lambda f=f,nm=nm,om=om:set(nm)|set(om)=={r['symbol'] for r in f['symbols']})
        for row in f['symbols']:
            def ah(node):return hashlib.sha256(ast.dump(node,include_attributes=False).encode()).hexdigest() if node else None
            yes('symbol AST hashes '+f['current']+':'+row['symbol'],lambda row=row,nm=nm,om=om:ah(nm.get(row['symbol']))==row['new_AST_SHA256'] and ah(om.get(row['symbol']))==row['old_AST_SHA256'])
            label=row['identity'];counts[label]=counts.get(label,0)+1
            if label=='exact_AST':yes('exact inherited AST '+f['current']+':'+row['symbol'],lambda row=row:row['new_AST_SHA256']==row['old_AST_SHA256'])
        yes('module AST pin '+f['current'],lambda f=f,new=new,old=old:hashlib.sha256(ast.dump(new,include_attributes=False).encode()).hexdigest()==f['new_full_module_AST_SHA256'] and hashlib.sha256(ast.dump(old,include_attributes=False).encode()).hexdigest()==f['old_full_module_AST_SHA256'])
    for phase,completed,published,last,cursor in [('merge95',55,39,218,239),('completion100',56,40,239,240)]:
        facts=h.phase_facts(phase)
        yes('phase exact accounting '+phase,lambda facts=facts,completed=completed,published=published,last=last,cursor=cursor:(facts['fully_completed_count'],facts['published_count'],facts['last_completed_PR'],facts['next_numeric_intake_cursor'])==(completed,published,last,cursor))
        yes('phase proposal never authorizes advance '+phase,lambda facts=facts:facts['advance_to_next_PR_authorized_now'] is False and facts['numeric_advance_conditional_on_actual_Root_terminal'] is True and facts['goal_complete'] is False)
    yes('phase95 memberships exact55/39',lambda:all(h.phase_memberships('merge95')[k]==v for k,v in h.source_baseline().items()))
    yes('phase100 membership exactly adds239',lambda:all(h.phase_memberships('completion100')[k]==v+[239] for k,v in h.source_baseline().items()))
    ident={'name':'Alec Kriebel','email':'me@aleckriebel.com','date':'2026-10-18T04:05:06Z'}
    for phase in ('merge95','completion100'):
        m={'phase':phase,'commit_author':ident,'commit_committer':ident,'commit_message':h.commit_message(phase)}
        parents=h.commit_parents(m,'1'*40);request,oid=h.commit_request(m,'2'*40,parents)
        raw=('tree '+'2'*40+'\n'+''.join('parent '+v+'\n' for v in parents)+'author Alec Kriebel <me@aleckriebel.com> 1792296306 +0000\ncommitter Alec Kriebel <me@aleckriebel.com> 1792296306 +0000\n\n'+h.commit_message(phase)).encode()
        # Timestamp is separately derived below, avoiding a mistaken hardcoded oracle.
        seconds=int(datetime.datetime.fromisoformat(ident['date'].replace('Z','+00:00')).timestamp())
        raw=raw.replace(b'1792296306',str(seconds).encode())
        yes('canonical raw commit and phase parent ordering '+phase,lambda raw=raw,oid=oid:h.native('commit',raw)==oid)
        no('wrong phase parents '+phase,lambda m=m,parents=parents:h.commit_request(m,'2'*40,parents+[h.CURRENT]))
        no('signature/body injection through message '+phase,lambda m=m,parents=parents:h.commit_request({**m,'commit_message':m['commit_message']+'gpgsig x\n'},'2'*40,parents))
        no('header injection author '+phase,lambda m=m,parents=parents:h.commit_request({**m,'commit_author':{**ident,'name':'A\nparent '+'3'*40}},'2'*40,parents))
    # Verify verbatim signature/message/order authentication on our own raw fixtures.
    fixture_name=sys.argv[1] if len(sys.argv)==2 else '_offline_raw_commit_03'
    if re.fullmatch('_offline_raw_commit_[0-9]{2}',fixture_name) is None:raise RuntimeError('Explicit unused offline fixture namespace required')
    fixture=OWN/fixture_name;fixture.mkdir(exist_ok=False)
    raw=b'tree '+b'2'*40+b'\nparent '+b'3'*40+b'\nparent '+b'4'*40+b'\nauthor A <a@b> 1 +0000\ncommitter A <a@b> 1 +0000\ngpgsig -----BEGIN TEST-----\n value\n \n -----END TEST-----\n\nExact message\n\n'
    path=fixture/'signed_test.txt';path.write_bytes(raw);path.chmod(0o444)
    record={'sha':h.native('commit',raw),'tree':'2'*40,'parents':['3'*40,'4'*40],'raw_commit':{'path':str(path),**pin(raw)}}
    yes('raw signed bytes authenticate verbatim',lambda:h.authenticated_commit(record) is record)
    no('raw ordered parents cannot reverse',lambda:h.authenticated_commit({**record,'parents':list(reversed(record['parents']))}))
    for name,bad in [('signature continuation',raw.replace(b'\n \n',b'\n\n')),('message final LF',raw[:-1]),('signature text',raw.replace(b' value',b' other'))]:
        p=fixture/(name.replace(' ','_')+'.txt');p.write_bytes(bad);p.chmod(0o444)
        no('raw OID rejects '+name,lambda p=p,bad=bad:h.authenticated_commit({**record,'raw_commit':{'path':str(p),**pin(bad)}}))
    own=b'|239|30001321 / OWR-4081-005|a|b|c|d|e|claimed_solved|3/5|f|g|h|\n'
    pre=own.replace(b'claimed_solved|3/5',b'queued|0/5');foreign=b'foreign CRLF\r\nforeign LF\n'
    m={'phase':'merge95','queue_pre_row_pin':pin(pre),'protected_queue_row_pin':pin(own)}
    yes('QUEUE95 own transition preserves foreign bytes',lambda:h.queue_transition(foreign+pre,foreign+own,m))
    for bad in (foreign.replace(b'\r\n',b'\n')+own,b'foreign LF\nforeign CRLF\r\n'+own,foreign+own.replace(b'3/5',b'5/5'),foreign+own+own,foreign+b' '+own):
        no('QUEUE95 invalid bytes/status/ambiguity '+hashlib.sha256(bad).hexdigest()[:8],lambda bad=bad:h.queue_transition(foreign+pre,bad,m))
    no('QUEUE100 cannot change whole body',lambda:h.queue_transition(foreign+own,b'else\n'+own,{**m,'phase':'completion100','queue_pre_row_pin':pin(own)}))
    yes('QUEUE100 exact preserved',lambda:h.queue_transition(foreign+own,foreign+own,{**m,'phase':'completion100','queue_pre_row_pin':pin(own)}))
    # Authenticated in-memory native trees exercise leaf/directory/mode preservation.
    objects={}
    def tree(rows):
        rows=sorted(rows,key=lambda r:r[0].encode()+(b'/' if r[1]=='040000' else b''));oid=c.tree_hash(rows)
        objects[oid]={'sha':oid,'truncated':False,'tree':[{'path':n,'mode':mode,'type':kind,'sha':sha} for n,mode,kind,sha in rows]};return oid
    child=tree([('foreign','100755','blob','a'*40),('selected','100644','blob','b'*40)])
    root=tree([('dir','040000','tree',child),('foreign-root','120000','blob','c'*40)])
    api=lambda method,path:copy.deepcopy(objects[path.rsplit('/',1)[-1]])
    overlay={'dir/selected':b'replacement','new/sub/file':b'new'}
    nt=c.NativeTrees(api);wanted,changed,dirs=h.expected(c,nt,root,overlay,{'dir/selected':('100644','blob','b'*40),'new/sub/file':None})
    afterchild=tree([('foreign','100755','blob','a'*40),('selected','100644','blob',h.native('blob',b'replacement'))])
    sub=tree([('file','100644','blob',h.native('blob',b'new'))]);new=tree([('sub','040000','tree',sub)])
    after=tree([('dir','040000','tree',afterchild),('foreign-root','120000','blob','c'*40),('new','040000','tree',new)])
    yes('native expected root preserves opaque foreign tuples',lambda:wanted==after)
    yes('native complete leaf/new-directory diff',lambda:nt.changes(root,after)==({'dir/selected','new/sub/file'},{'new','new/sub'},set()) and changed=={'dir/selected','new/sub/file'} and dirs=={'new','new/sub'})
    no('native wrong selected preimage fails',lambda:h.expected(c,c.NativeTrees(api),root,overlay,{'dir/selected':None,'new/sub/file':None}))
    no('native leaf ancestor collision fails',lambda:h.expected(c,c.NativeTrees(api),root,{'foreign-root/sub':b'x'},{'foreign-root/sub':None}))
    # Production local-state validator: every mixed pre/post state is resumable;
    # pre-only and all-post modes remain strict. No actual local view is read.
    views=[{'path':'v'+str(i),'preimage':pin(('pre'+str(i)).encode())} for i in range(5)]
    overlays={r['path']:('post'+str(i)).encode() for i,r in enumerate(views)}
    now={};rt=types.SimpleNamespace(m={'local_views':views},overlay=overlays,h=h,seed=types.SimpleNamespace(s=types.SimpleNamespace(read_regular=lambda p,absent=False:(now[p.name],None))))
    for mask in range(32):
        now.update({r['path']:overlays[r['path']] if mask&(1<<i) else ('pre'+str(i)).encode() for i,r in enumerate(views)})
        yes('five exact mixed recovery '+str(mask),lambda:q.local_states(rt,resume=True))
        if mask: no('pre-only rejects installed mixture '+str(mask),lambda:q.local_states(rt))
        if mask!=31:no('terminal rejects incomplete five '+str(mask),lambda:q.local_states(rt,all_post=True))
    for i in range(5):
        now.update({r['path']:overlays[r['path']] for r in views});now['v'+str(i)]=b'third state'
        no('five third state refused '+str(i),lambda:q.local_states(rt,resume=True))
    # Guard race checks with explicit in-memory dependencies, no real lock or API.
    qg=module('completion_checkpoint.py');qg.local_states=lambda rt:None;qg.parent_state=lambda rt,api:('2'*40,set(),set())
    grt=types.SimpleNamespace(admission={'parent':'1'*40,'tree':'2'*40},refresh=lambda:None)
    lock=types.SimpleNamespace(check=lambda:None)
    yes('lease holds two consistent Main observations',lambda:qg.lease_guard(grt,lambda *a:{'object':{'sha':'1'*40}},lock))
    for seq in [('3'*40,'1'*40),('1'*40,'3'*40)]:
        reads=iter(seq);no('lease race fail stop '+str(seq.index('3'*40)),lambda:qg.lease_guard(grt,lambda *a:{'object':{'sha':next(reads)}},lock))
    # Missing actual blob origin fails even if its body is correct.
    body=b'correct offline body';oid=h.native('blob',body)
    observer=lambda *a:{'sha':oid,'encoding':'base64','size':len(body),'content':base64.b64encode(body).decode()}
    no('correct blob without actual GET origin refused',lambda:h.NativeBodyProofs().get(observer,oid))
    # Terminal source-only gates and actual facts are independently typed.
    no('empty terminal source acceptance refused',lambda:t.check_source_acceptance({},pin(b's'),pin(b'm'),{}))
    no('empty consumer record refused',lambda:u.completion_proof(b'{}',pin(b'{}')))
    for raw in (enc({'schema':'pr218-root-actual-completion-verification-v1','PR':218}),enc({'schema':'pr239-root-actual-completion-verification-v1','PR':239,'phase':'merge95'}),enc({'accepted':True,'completed':True,'adopted_existing_publication':True})):
        no('consumer rejects legacy/95/adoption '+pin(raw)['sha256'][:8],lambda raw=raw:u.completion_proof(raw,pin(raw)))
    no('consumer externally wrong pin refused',lambda:u.completion_proof(b'{}',pin(b'{ }')))
    report={'schema':'pr239-independent-operational-source-controls-v1','source_only':True,'operational_authority':False,'producer_controls_not_reexecuted':True,'timestamp_UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_manifest_pin':pin(manifest_raw),'AST_class_counts':counts,'count':len(results),'results':results,'limits':['No production Seed/Runtime or terminal inspect execution.','No synthetic gate/receipt was accepted as actual authority.','No actual API, stable project lock, provider, tracker, PR, ref or five-file effect.']}
    (OWN/'INDEPENDENT_CONTROL_RESULTS.json').write_bytes(enc(report))
    print(json.dumps({'controls':len(results),'AST_class_counts':counts,'result':'PASS'}))

if __name__=='__main__':main()
