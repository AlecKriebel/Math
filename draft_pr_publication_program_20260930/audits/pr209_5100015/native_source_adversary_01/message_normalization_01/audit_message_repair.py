"""Targeted inert-source/message diagnostic and full595-body verifier controls."""
from pathlib import Path
import base64,hashlib,json,sys,types,tempfile,os
from datetime import datetime,timezone
BASE=Path(__file__).absolute().parent
RESULTS=[]
def pin(raw):return {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
def enc(obj):return (json.dumps(obj,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
def check(name,ok,detail=None):
    if not ok:raise RuntimeError('Targeted independent control failed: '+name+' '+str(detail))
    RESULTS.append({'name':name,'observed':detail})
def load(version):
    folder='historical_source_freeze' if version=='historical' else 'source_freeze';meta='HISTORICAL_SOURCE_FREEZE.json' if version=='historical' else 'SOURCE_FREEZE.json'
    pins=json.loads((BASE/meta).read_bytes())['files'];modules={}
    for name in ['native209_model.py','native_trees_readonly.py']:
        raw=(BASE/folder/name).read_bytes()
        if pin(raw)!=pins[name]:raise RuntimeError('Frozen source drift')
        m=types.ModuleType('audit_'+version+'_'+name.replace('.','_'));m.__file__=str(BASE/folder/name);exec(compile(raw,m.__file__,'exec'),m.__dict__);modules[name]=m
    return modules['native209_model.py'],modules['native_trees_readonly.py']
class HeaderAccepted(Exception):pass

def actual_diagnostic(version,response=None,candidate=None):
    h,c=load(version);fixture=json.loads((BASE/'FIXTURE_CANONICAL_COMMIT_INPUTS.json').read_bytes());commit=json.loads((BASE/'FIXTURE_ACTUAL_COMMIT_API.json').read_bytes()) if response is None else response
    m=fixture['manifest_inputs'];expected,oid=h.commit_request(m,fixture['tree'],fixture['parents'])
    if oid!=fixture['candidate']:raise RuntimeError('Actual deterministic fixture oid differs')
    observed=[]
    def api(method,path,body=None):
        if method!='GET' or path!='git/commits/'+fixture['candidate'] or body is not None:raise RuntimeError('Unexpected actual diagnostic request')
        observed.append(path);return commit
    h.state=lambda *args,**kwargs:{'api':api,'wanted':fixture['tree'],'parents':fixture['parents']}
    def sentinel(*args,**kwargs):raise HeaderAccepted()
    c.NativeTrees=sentinel
    try:h.verify(c,m,{}, {}, {},api,fixture['candidate'] if candidate is None else candidate)
    except HeaderAccepted:return {'accepted_header':True,'error':None,'metadata_requests':len(observed),'expected_oid':oid,'message_difference_exactly_one_LF':commit.get('message')+'\n'==m['commit_message'] if type(commit.get('message')) is str else False}
    except (RuntimeError,ValueError,KeyError,TypeError) as error:return {'accepted_header':False,'error':str(error),'metadata_requests':len(observed),'expected_oid':oid}
    raise RuntimeError('Header sentinel not reached')

class Objects:
    def __init__(self,h,c):self.h=h;self.c=c;self.trees={};self.blobs={};self.body_requests=[];self.commit=None;self.parent=None;self.candidate=""
    def blob(self,raw):
        sha=self.h.native('blob',raw);self.blobs[sha]=raw;return sha
    def tree(self,rows):
        rows=sorted(rows,key=lambda r:r[0].encode()+(b'/' if r[1]=='040000' else b''));sha=self.c.tree_hash(rows);self.trees[sha]={'sha':sha,'truncated':False,'tree':[dict(path=n,mode=md,type=k,sha=s) for n,md,k,s in rows]};return sha
    def flat(self,files):
        trie={}
        for path,body in files.items():
            node=trie;parts=path.split('/')
            for part in parts[:-1]:node=node.setdefault(part,{})
            node[parts[-1]]=body
        def build(node):return self.tree([(name,'040000','tree',build(v)) if type(v) is dict else (name,'100644','blob',self.blob(v)) for name,v in node.items()])
        return build(trie)
    def __call__(self,method,path,body=None):
        if method!='GET' or body is not None:raise RuntimeError('Synthetic provider is GET only')
        if path=='git/ref/heads/main':return {'object':{'sha':self.parent}}
        if path=='git/commits/'+self.candidate:return self.commit
        if path.startswith('git/trees/'):return self.trees[path.rsplit('/',1)[1]]
        if path.startswith('git/blobs/'):
            oid=path.rsplit('/',1)[1];raw=self.blobs[oid];self.body_requests.append(oid);return {'sha':oid,'encoding':'base64','size':len(raw),'content':base64.b64encode(raw).decode()}
        raise RuntimeError('Unexpected synthetic provider route '+path)

def full_fixture(version,observed_message=None,canonical_message='Synthetic canonical message\nSecond line\n',mutate=None):
    h,c=load(version);f=Objects(h,c);parent='1'*40;prepared='2'*40
    shared={h.SHARED+'/s/'+str(i):('synthetic unchanged body '+str(i)).encode() for i in range(228)}
    overlay={h.ATTEMPT+'f'+str(i):('synthetic own body '+str(i)).encode() for i in range(54)}
    overlay.update({path:('synthetic view '+str(i)).encode() for i,path in enumerate(h.VIEWS)})
    overlay[h.QUEUE]=b'Synthetic queue body only'
    overlay.update({h.CASE+'synthetic_selected/'+str(i):('synthetic selected body '+str(i)).encode() for i in range(367-len(overlay))})
    if len(overlay)!=367:raise RuntimeError('367 fixture cardinality')
    before=f.flat(shared);wanted=f.flat({**shared,**overlay});pre={p:None for p in overlay}
    generated,changes,dirs=h.expected(c,c.NativeTrees(f),before,overlay,pre)
    if generated!=wanted:raise RuntimeError('Synthetic independent root differs')
    h.ATTEMPT_TREE=c.NativeTrees(f).lookup(wanted,h.ATTEMPT[:-1])[2];h.SHARED_TREE=c.NativeTrees(f).lookup(wanted,h.SHARED)[2]
    m={'phase':'merge95','facts':h.phase_facts('merge95'),'expected_parent':parent,'expected_parent_tree':before,'commit_author':{'name':'Synthetic Auditor','email':'fixture@example.invalid','date':'2026-10-17T00:00:00Z'},'commit_committer':{'name':'Synthetic Auditor','email':'fixture@example.invalid','date':'2026-10-17T00:00:00Z'},'commit_message':canonical_message}
    req,oid=h.commit_request(m,wanted,[parent,prepared]);f.candidate=oid;f.parent=parent
    f.commit={'sha':oid,'tree':{'sha':wanted},'parents':[{'sha':parent},{'sha':prepared}],'message':canonical_message if observed_message is None else observed_message,'author':dict(req['author']),'committer':dict(req['committer'])}
    reused={p:{'path':p,**pin(raw),'git_blob':f.blob(raw)} for p,raw in shared.items()}
    s={'api':f,'parent':parent,'parent_tree':before,'wanted':wanted,'changed':changes,'dirs':dirs,'parents':[parent,prepared]}
    h.state=lambda *args,**kwargs:s
    candidate=oid
    if mutate is not None:
        override=mutate(h,c,f,m,overlay,reused,s)
        if override is not None:candidate=override
    try:
        result=h.verify(c,m,overlay,pre,reused,f,candidate)
        return {'accepted':True,'body_requests':len(f.body_requests),'selected_file_count':result['selected_file_count'],'result_message_fields':{k:v for k,v in result.items() if 'message' in k.lower()},'result':result}
    except (RuntimeError,ValueError,KeyError,TypeError) as error:return {'accepted':False,'body_requests':len(f.body_requests),'error':str(error)}

def run(version):
    actual=actual_diagnostic(version)
    if version=='historical':
        check('historical_actual45d_oneLF_metadata_refused',not actual['accepted_header'] and actual['metadata_requests']==1,actual)
        result=full_fixture(version,observed_message='Synthetic canonical message\nSecond line')
        check('historical_full_verifier_oneLF_metadata_refused',not result['accepted'] and result['body_requests']==0,result)
        return
    check('repaired_actual45d_oneLF_metadata_header_accepted',actual['accepted_header'] and actual['message_difference_exactly_one_LF'],actual)
    exact=full_fixture(version);one=full_fixture(version,observed_message='Synthetic canonical message\nSecond line')
    check('full_verify_exact_message_all595_bodies',exact['accepted'] and exact['body_requests']==595 and exact['selected_file_count']==595,{k:v for k,v in exact.items() if k!='result'})
    check('full_verify_oneLF_omission_all595_bodies',one['accepted'] and one['body_requests']==595 and one['selected_file_count']==595,{k:v for k,v in one.items() if k!='result'})
    check('explicit_distinct_message_readback_recorded',bool(exact['result_message_fields']) and bool(one['result_message_fields']) and exact['result_message_fields']!=one['result_message_fields'])
    canonical='Synthetic canonical message\nSecond line\n'
    for label,observed,message in [('exact',exact,canonical),('omits_exactly_one_terminal_LF',one,canonical[:-1])]:
        expected={'representation':label,'terminal_LFs_omitted':0 if label=='exact' else 1,'canonical_message_pin':pin(canonical.encode()),'metadata_message_pin':pin(message.encode())}
        check('explicit_'+label+'_representation_and_both_byte_pins',observed['result']['commit_message_readback']==expected,observed['result']['commit_message_readback'])
        check('explicit_'+label+'_canonicalOID_and_fixed_identity_verified',observed['result']['deterministic_canonical_commit_oid_verified'] is True and observed['result']['fixed_author_and_committer_metadata_verified'] is True)
    bad_messages=['Synthetic canonical message\nSecond line\n\n','Synthetic canonical messageSecond line','Synthetic canonical message\r\nSecond line','Synthetic canonical message\nSecond line ',' Synthetic canonical message\nSecond line','Synthetic canonical message\nSecond LINE','Synthetic canonical message\nSecond line\ntext','',False,17,[],{}]
    for i,value in enumerate(bad_messages):
        def change(h,c,f,m,o,r,s,value=value):f.commit['message']=value
        result=full_fixture(version,mutate=change)
        check('other_message_representation_'+str(i)+'_refused',not result['accepted'] and result['body_requests']==0,result)
    result=full_fixture(version,canonical_message='Synthetic canonical message\nSecond line\n\n',observed_message='Synthetic canonical message\nSecond line')
    check('two_terminalLF_omission_refused',not result['accepted'] and result['body_requests']==0,result)
    result=full_fixture(version,canonical_message='Synthetic canonical message\nSecond line\n\n',observed_message='Synthetic canonical message\nSecond line\n')
    check('one_of_two_terminalLF_omission_exactly_one_allowed',result['accepted'] and result['body_requests']==595)
    negatives={
        'wrong_candidateOID':lambda h,c,f,m,o,r,s:'f'*40,
        'wrong_responseSHA':lambda h,c,f,m,o,r,s:f.commit.update(sha='f'*40),
        'wrong_tree':lambda h,c,f,m,o,r,s:f.commit.update(tree={'sha':'f'*40}),
        'wrong_parent':lambda h,c,f,m,o,r,s:f.commit.update(parents=[{'sha':'f'*40},{'sha':'2'*40}]),
        'reordered_parents':lambda h,c,f,m,o,r,s:f.commit.update(parents=list(reversed(f.commit['parents']))),
        'missing_parent':lambda h,c,f,m,o,r,s:f.commit.update(parents=f.commit['parents'][:1]),
        'extra_parent':lambda h,c,f,m,o,r,s:f.commit['parents'].append({'sha':'f'*40}),
        'changed_canonical_request':lambda h,c,f,m,o,r,s:m.update(commit_message=m['commit_message']+'\n'),
    }
    for name,change in negatives.items():
        result=full_fixture(version,mutate=change);check(name+'_still_refused',not result['accepted'] and result['body_requests']==0,result)
    for role in ('author','committer'):
        for key in ('name','email','date'):
            def change(h,c,f,m,o,r,s,role=role,key=key):f.commit[role][key]='wrong synthetic '+key
            result=full_fixture(version,mutate=change);check('fixed_'+role+'_'+key+'_refused',not result['accepted'] and result['body_requests']==0,result)
        def missing(h,c,f,m,o,r,s,role=role):f.commit.pop(role)
        result=full_fixture(version,mutate=missing);check('missing_'+role+'_refused',not result['accepted'] and result['body_requests']==0,result)
    def bad_selected(h,c,f,m,o,r,s):f.blobs[h.native('blob',next(iter(o.values())))]=b'selected tampered'
    def bad_reused(h,c,f,m,o,r,s):f.blobs[next(iter(r.values()))['git_blob']]=b'reused tampered'
    def bad_native_tree(h,c,f,m,o,r,s):f.trees[s['wanted']]['tree'][0]['sha']='f'*40
    for name,change in [('selected_body',bad_selected),('reused_body',bad_reused),('native_tree_body',bad_native_tree)]:
        result=full_fixture(version,mutate=change);check(name+'_still_authenticated',not result['accepted'],result)

if __name__=='__main__':
    if not(sys.flags.ignore_environment and sys.flags.no_site and sys.dont_write_bytecode and sys.flags.safe_path):raise RuntimeError('Use Python -E -S -B -P')
    run('historical')
    if len(sys.argv)>1 and sys.argv[1]=='historical-only':status='REPRODUCED_HISTORICAL_MESSAGE_METADATA_DEFECT'
    else:run('repaired');status='PASS_TARGETED_SOURCE_REPAIR_CONDITIONAL_ONLY'
    output={'schema':'pr209-independent-message-normalization-controls-v1','UTC':datetime.now(timezone.utc).isoformat(),'status':status,'check_count':len(RESULTS),'results':RESULTS,'actual_existing_diagnostic_used':True,'full_verify_positive_fixture':'367 selected +228 reused synthetic native bodies','external_calls':0,'production_mutations':0,'actual_manifest03_accepted':False}
    dest=BASE/('HISTORICAL_REPRODUCTION.json' if status.startswith('REPRODUCED') else 'TARGETED_RESULTS.json')
    if dest.exists():
        fd,name=tempfile.mkstemp(prefix='REPLAY_'+dest.stem+'_',suffix='.json',dir=BASE)
        with os.fdopen(fd,'wb') as stream:stream.write(enc(output))
    else:dest.write_bytes(enc(output))
    print(json.dumps({'status':status,'checks':len(RESULTS)},sort_keys=True))
