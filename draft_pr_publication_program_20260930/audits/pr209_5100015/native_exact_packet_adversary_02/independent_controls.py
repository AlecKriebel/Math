"""Independent PR209 native source/packet audit, offline and no authority.

Imports inert reviewed modules. Only writes its owned results. Does not invoke
the executor CLI, service transport, production journal, gates or local views.
"""
import ast
import base64
import copy
import datetime
import hashlib
import itertools
import json
from pathlib import Path
import stat
import types

OWN = Path(__file__).absolute().parent
BASE = OWN.parent/'native_integration_preparation_01'
RECORDS = []

def require(condition, message):
    if not condition:
        raise AssertionError(message)

def check(label, function):
    function()
    RECORDS.append({'control':label,'result':'PASS'})

def refuse(label, function):
    try:
        function()
    except (RuntimeError, ValueError, KeyError, TypeError):
        RECORDS.append({'control':label,'result':'PASS_REFUSED'})
        return
    raise AssertionError('Adversarial input was accepted: '+label)

def digest(raw):
    return {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}

def load(filename):
    path = BASE/filename
    module = types.ModuleType('independent_'+filename.replace('.','_'))
    module.__file__ = str(path)
    exec(compile(path.read_bytes(),str(path),'exec'),module.__dict__)
    return module

H = load('native209_model.py')
C = load('native_trees_readonly.py')
E = load('native209_future_executor.py')

# An independent serializer, deliberately not the production helper.
def independent_object(kind, body):
    wire = kind.encode('ascii')+b' '+str(len(body)).encode('ascii')+b'\0'+body
    return hashlib.sha1(wire).hexdigest()

def independent_tree(entries):
    wire = b''
    for name,mode,kind,oid in sorted(entries,key=lambda r:r[0].encode('utf-8')+(b'/' if r[2]=='tree' else b'')):
        wire += str(int(mode)).encode('ascii')+b' '+name.encode('utf-8')+b'\0'+bytes.fromhex(oid)
    return independent_object('tree',wire)

def source_closure():
    source_manifest = json.loads((BASE/'SOURCE_MANIFEST.json').read_bytes())
    require(len(source_manifest['source_files']) == source_manifest['total_files'],'manifest source count')
    require(sum(row['bytes'] for row in source_manifest['source_files']) == source_manifest['total_bytes'],'manifest source bytes')
    for row in source_manifest['source_files']:
        path = BASE/row['path']
        require(digest(path.read_bytes()) == {k:row[k] for k in ('bytes','sha256')},'source pin '+row['path'])
        require(stat.S_IMODE(path.stat().st_mode) == 0o444,'source mode '+row['path'])
    require(digest((BASE/'native209_model.py').read_bytes()) == E.MODEL_PIN,'executor pinned model')
    require(digest((BASE/'native_trees_readonly.py').read_bytes()) == H.CORE_PIN,'model pinned core')
    for name,pin in H.REFERENCE_PINS.items():
        require(digest((BASE/name).read_bytes()) == pin,'fixed reference '+name)
check('current_frozen_source_manifest_closure_and_cross_pins',source_closure)

FACTS95 = {'active_PR':209,'case_workflow_estimate_percent':95,'fully_completed_count':50,
 'published_count':35,'last_completed_PR':207,'next_numeric_intake_cursor':209,
 'advance_to_next_PR_authorized_now':False,'completed':False,'publication_ready':True,'goal_complete':False}
FACTS100 = dict(FACTS95,case_workflow_estimate_percent=100,fully_completed_count=51,
 last_completed_PR=209,next_numeric_intake_cursor=210,advance_to_next_PR_authorized_now=True,completed=True)
check('merge95_fixed_facts',lambda: require(H.phase_facts('merge95') == FACTS95,'facts95'))
check('completion100_fixed_facts',lambda: require(H.phase_facts('completion100') == FACTS100,'facts100'))
for bad in ('done','merge100',None,95,True):
    refuse('bad_phase_'+repr(bad),lambda bad=bad:H.phase_facts(bad))
for left,right in [(True,1),(False,0),(95,95.0),({'a':True},{'a':1}),([1],[1.0])]:
    check('exact_types_'+repr((left,right)),lambda left=left,right=right:require(not H.exact(left,right),'type identity'))

MARK95 = b'<!-- PR209_NATIVE_PHASE_FACTS '+json.dumps(FACTS95,sort_keys=True,separators=(',',':')).encode()+b' -->'
MARK100 = b'<!-- PR209_NATIVE_PHASE_FACTS '+json.dumps(FACTS100,sort_keys=True,separators=(',',':')).encode()+b' -->'
history = b'# Owned log\n\nInitial historical record.\n'
log95 = history+b'\n95 percent checkpoint; no advance.\n'+MARK95+b'\n'
log100 = log95+b'\n100 percent checkpoint; actual completion separately evidenced.\n'+MARK100+b'\n'
check('real_append_log95',lambda:H.markdown_current(log95,'merge95',True))
check('real_append_log100_keeps95prefix',lambda:(require(log100.startswith(log95),'append prefix'),H.markdown_current(log100,'completion100',True)))
check('completion_current_md_without_history',lambda:H.markdown_current(b'# Current\n'+MARK100+b'\n','completion100',False))
for name,body,phase,log in [
 ('completion_log_loses95',history+MARK100+b'\n','completion100',True),
 ('completion_history_reversed',history+MARK100+b'\n'+MARK95+b'\n','completion100',True),
 ('duplicate95',log95+MARK95+b'\n','merge95',True),
 ('duplicate100',log100+MARK100+b'\n','completion100',True),
 ('old95_is_terminal',log95,'completion100',True),
 ('inline_marker',history+b'prefix '+MARK95+b'\n','merge95',True),
 ('trailing_prose',log100+b'Unqualified current state\n','completion100',True),
 ('unsupported_phase_marker',history+MARK95.replace(b'95',b'96')+b'\n','merge95',True),
 ('completion_95_100_95',log100+MARK95+b'\n','completion100',True),
 ('95_contains100history',history+MARK100+b'\n'+MARK95+b'\n','merge95',True),
    ('indented_marker',history+b' '+MARK95+b'\n','merge95',True),
]:
    refuse('phase_marker_'+name,lambda body=body,phase=phase,log=log:H.markdown_current(body,phase,log))

for index,malformed in enumerate((
    b'<!-- PR209_NATIVE_PHASE_FACTS_UNKNOWN {} -->',
    b'<!-- PR209_NATIVE_PHASE_FACTS{} -->',
    b'<!-- PR209_NATIVE_PHASE_FACTS\t{} -->',
    b'<!-- PR209_NATIVE_PHASE_FACTS',
    b'<!-- PR209_NATIVE_PHASE_FACTS  {} -->',
)):
    refuse('malformed_reserved_namespace_'+str(index),lambda malformed=malformed:H.markdown_current(history+malformed+b'\n'+MARK95+b'\n','merge95',True))

# Verify the real frozen native QUEUE preimage to proposed95 postimage, then
# independently enumerate all changed line and cell positions.
snapshot = OWN.parent/'root_native_snapshot_01'
old_queue = (snapshot/'bodies/unsolved_math_prioritization/QUEUE.md').read_bytes()
new_queue = (BASE/'packet95/QUEUE.md').read_bytes()
def queue_control():
    H.queue_change(old_queue,new_queue,'merge95')
    before,after = old_queue.splitlines(keepends=True),new_queue.splitlines(keepends=True)
    changed = [i for i,(a,b) in enumerate(zip(before,after)) if a != b]
    require(len(before)==len(after) and len(changed)==1,'exact own line changed')
    a,b = before[changed[0]].split(b'|'),after[changed[0]].split(b'|')
    require([i for i,(x,y) in enumerate(zip(a,b)) if x != y] == [8,9,11,12],'exact four own cells')
    require(b'5100015 / AMR-050-0015' in after[changed[0]],'own identity')
check('actual_frozen_QUEUE_exact_own_line_four_cells_only',queue_control)
check('completion_QUEUE_exact_noop',lambda:H.queue_change(new_queue,new_queue,'completion100'))
refuse('QUEUE_foreign_prefix_byte',lambda:H.queue_change(old_queue,b'X'+new_queue,'merge95'))
refuse('QUEUE_foreign_suffix_byte',lambda:H.queue_change(old_queue,new_queue+b'X','merge95'))
refuse('QUEUE_changed_effort',lambda:H.queue_change(old_queue,new_queue.replace(b'claimed_solved | 1/5',b'claimed_solved | 2/5'),'merge95'))
refuse('completion_QUEUE_rewinds',lambda:H.queue_change(new_queue,old_queue,'completion100'))

# Canonical small native repository includes a preserved executable, symlink,
# submodule and nested opaque foreign tree, and newly added nested own leaves.
OBJECTS = {}
def tree(rows):
    ordered = sorted(rows,key=lambda r:r[0].encode()+(b'/' if r[2]=='tree' else b''))
    oid = independent_tree(ordered)
    OBJECTS[oid] = {'sha':oid,'truncated':False,'tree':[
        {'path':n,'mode':m,'type':k,'sha':o} for n,m,k,o in ordered]}
    return oid
oid_a = independent_object('blob',b'old-a')
oid_b = independent_object('blob',b'old-b')
foreign = tree([('run','100755','blob',oid_a),('sym','120000','blob',oid_b),('submodule','160000','commit','1'*40)])
owned = tree([('change.md','100644','blob',oid_a),('keep.md','100644','blob',oid_b)])
root = tree([('own','040000','tree',owned),('foreign','040000','tree',foreign),('own.txt','100644','blob',oid_b)])
overlay = {'own/change.md':b'new-a','own/new/nested.md':b'new-b'}
pre = {'own/change.md':('100644','blob',oid_a),'own/new/nested.md':None}
calls = []
def observe(method,path):
    require(method=='GET' and path.startswith('git/trees/'),'pure native GET tree')
    calls.append(path)
    return copy.deepcopy(OBJECTS[path.rsplit('/',1)[1]])
expected_nested = tree([('nested.md','100644','blob',independent_object('blob',b'new-b'))])
expected_owned = tree([('change.md','100644','blob',independent_object('blob',b'new-a')),
 ('keep.md','100644','blob',oid_b),('new','040000','tree',expected_nested)])
independent_expected_root = tree([('own','040000','tree',expected_owned),('foreign','040000','tree',foreign),('own.txt','100644','blob',oid_b)])
def scope_control():
    trees = C.NativeTrees(observe)
    modeled,leaves,dirs = H.expected(C,trees,root,overlay,pre)
    require(modeled == independent_expected_root,'independent canonical tree equality')
    require(leaves == set(overlay) and dirs == {'own/new'},'exact own scope')
    require('git/trees/'+foreign not in calls,'foreign subtree remained opaque')
    delta = C.NativeTrees(observe).changes(root,modeled)
    require(delta == (set(overlay),{'own/new'},set()),'independent native delta')
    require(C.NativeTrees(observe).lookup(modeled,'foreign') == ('040000','tree',foreign),'opaque foreign identity')
check('independent_canonical_rebuild_exact_own_scope_foreign_modes_opaque',scope_control)
refuse('stale_native_preimage',lambda:H.expected(C,C.NativeTrees(observe),root,overlay,dict(pre,**{'own/change.md':None})))
refuse('ancestor_leaf_collision',lambda:H.expected(C,C.NativeTrees(observe),root,{'own.txt/nested':b'x'},{'own.txt/nested':None}))
refuse('overlay_leaf_then_descendant_collision',lambda:H.expected(C,C.NativeTrees(observe),root,{'x':b'a','x/y':b'b'},{'x':None,'x/y':None}))
refuse('overlay_descendant_then_leaf_collision',lambda:H.expected(C,C.NativeTrees(observe),root,{'x/y':b'b','x':b'a'},{'x':None,'x/y':None}))
for name,mutate in [
 ('truncated',lambda j:j.update(truncated=True)),
 ('wrong_sha',lambda j:j.update(sha='f'*40)),
 ('unsorted',lambda j:j['tree'].reverse()),
 ('duplicate',lambda j:j['tree'].append(copy.deepcopy(j['tree'][0]))),
 ('bad_mode',lambda j:j['tree'][0].update(mode='100600')),
 ('tree_slash',lambda j:j['tree'][0].update(path='bad/name')),
]:
    altered = copy.deepcopy(OBJECTS[root]);mutate(altered)
    refuse('canonical_tree_'+name,lambda altered=altered:C.NativeTrees(lambda *unused:copy.deepcopy(altered)).get(root,0))

# Deterministic commit prediction is independently reconstructed from bytes.
identity = {'name':'Alec Kriebel','email':'me@aleckriebel.com','date':'2026-10-17T00:57:34Z'}
commit_input = {'commit_author':identity,'commit_committer':identity,'commit_message':'Audit PR209 conditional checkpoint\n'}
def commit_control():
    req,oid = H.commit_request(commit_input,root,['a'*40,'b'*40])
    epoch = int(datetime.datetime(2026,10,17,0,57,34,tzinfo=datetime.timezone.utc).timestamp())
    who = 'Alec Kriebel <me@aleckriebel.com> '+str(epoch)+' +0000'
    raw = ('tree '+root+'\nparent '+'a'*40+'\nparent '+'b'*40+'\nauthor '+who+'\ncommitter '+who+'\n\nAudit PR209 conditional checkpoint\n').encode()
    require(oid == independent_object('commit',raw),'native commit independent prediction')
    require(req['parents']==['a'*40,'b'*40],'merge parent order')
check('deterministic_commit_independent_serializer_exact_merge_parent_order',commit_control)
for name,edit in [('message_no_newline',{'commit_message':'x'}),('message_nul',{'commit_message':'x\0\n'}),('message_cr',{'commit_message':'x\r\n'}),
                  ('identity_newline',{'commit_author':dict(identity,name='Alec\nKriebel')}),('date_unfixed',{'commit_committer':dict(identity,date='2026-10-17T00:57:34+00:00')})]:
    refuse('commit_'+name,lambda edit=edit:H.commit_request(dict(commit_input,**edit),root,['a'*40]))

# Exercise memory-only immutable cache against an inert fake process runner.
# No transport or production files are used. Cache must clone objects, preserve
# immutable response pins and never cache ref, PR, compare or POST responses.
journal_records,transport_calls = [],[]
E.put = lambda directory,name,value:journal_records.append((name,copy.deepcopy(value)))
def fake_run(argv,request):
    path = argv[-1].split('repos/AlecKriebel/Math/',1)[1] if request is None else argv[-3].split('repos/AlecKriebel/Math/',1)[1]
    transport_calls.append((argv[argv.index('--method')+1],path,request))
    value = {'sha':path.rsplit('/',1)[1],'nested':{'value':len(transport_calls)}}
    if path == 'git/ref/heads/main':value={'object':{'sha':'a'*40}}
    if path == 'pulls/209':value={'number':209}
    if path.startswith('compare/'):value={'status':'ahead'}
    return types.SimpleNamespace(returncode=0,stdout=json.dumps(value).encode(),stderr=b'')
E.run_bounded = fake_run
api = E.API(H,OWN,mutate=False)
def cache_control():
    first = api('GET','git/blobs/'+'a'*40)
    first['nested']['value'] = -999
    second = api('GET','git/blobs/'+'a'*40)
    require(second['nested']['value']==1 and len(transport_calls)==1,'fresh cache decode, one immutable GET')
    for path in ('git/ref/heads/main','pulls/209','compare/'+'a'*40+'...'+'b'*40):
        before=len(transport_calls);api('GET',path);api('GET',path)
        require(len(transport_calls)==before+2,'mutable route never cached '+path)
    require(len(api._immutable_cache)==1,'only one immutable cache row')
    clone = E.API(H,OWN,mutate=False)
    before=len(transport_calls);clone('GET','git/blobs/'+'a'*40)
    require(len(transport_calls)==before+1,'independent instance does fresh GET')
check('immutable_cache_clone_mutable_fresh_cross_instance_fresh',cache_control)
refuse('cache_route_ref_mutation_refused',lambda:api('POST','git/refs/heads/main',{'sha':'a'*40},expected_oid='a'*40))
refuse('cache_route_service_publish_refused',lambda:api('POST','releases',{},expected_oid='a'*40))

RESULT = {'schema':'pr209-independent-native-source-controls-v1',
 'evidence_scope':'OFFLINE_INDEPENDENT_TESTS_NOT_ROOT_AUTHORITY','controls':RECORDS,
 'control_count':len(RECORDS),'all_passed':True,'source_manifest':digest((BASE/'SOURCE_MANIFEST.json').read_bytes()),
 'model':digest((BASE/'native209_model.py').read_bytes()),'executor':digest((BASE/'native209_future_executor.py').read_bytes()),
 'core':digest((BASE/'native_trees_readonly.py').read_bytes()),
 'actual_provider_calls':0,'production_CLI_invoked':False,'Root_gates_created':False,
 'native_objects_or_refs_created':False,'publication_or_tracker_actions':False,'local_five_modified':False,
 'limits':'Source controls only. Exact packet audit follows and remains conditional; no actual native candidate, CAS or synchronization is established.'}
(OWN/'INDEPENDENT_CONTROLS_RESULT.json').write_text(json.dumps(RESULT,sort_keys=True,indent=2)+'\n')
print(json.dumps({k:v for k,v in RESULT.items() if k != 'controls'},sort_keys=True))
