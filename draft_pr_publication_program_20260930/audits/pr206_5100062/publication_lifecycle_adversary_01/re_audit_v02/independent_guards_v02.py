"""Independent bounded leaf and fake-native attacks on exact sealed v01 sources.
No author test imports, project runtime, live APIs, or actual receipts.
"""
from pathlib import Path
import base64, copy, hashlib, json, os, stat, sys, tempfile, types

HERE = Path(__file__).absolute().parent
SOURCES = {}
def load(name):
    path = HERE / 'sealed_source' / name
    raw = path.read_bytes()
    SOURCES[name] = {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}
    module = types.ModuleType('adversary_' + name[:-3])
    module.__file__ = str(path)
    exec(compile(raw, str(path), 'exec'), module.__dict__)
    return module
S, R, L, N = (load(n) for n in ('support206.py', 'ready206.py', 'lifecycle206.py', 'make_native206.py'))
N.configure(S); R.configure(S); L.configure(S, R, N)
RESULTS = []
def run(name, function, reject=False, predicate=None):
    try:
        value = function()
        ok = not reject and (predicate is None or bool(predicate(value)))
        observed = 'accepted'
        error = None
    except Exception as exc:
        value = None
        ok = reject
        observed = 'rejected'
        error = type(exc).__name__ + ': ' + str(exc)
    RESULTS.append({'case': name, 'expected': 'reject' if reject else 'accept',
                    'observed': observed, 'pass': ok, 'error': error})
    return value
class Patch:
    def __init__(self, target, **values): self.target, self.values = target, values
    def __enter__(self):
        self.old = {key: getattr(self.target, key) for key in self.values}
        for key, val in self.values.items(): setattr(self.target, key, val)
        return self
    def __exit__(self, *unused):
        for key, val in self.old.items(): setattr(self.target, key, val)

def checked_frozen(raw):
    def take(name,expected=None,readonly=True):
        if expected is not None:S.need(S.pin(raw)==expected,'Independent synthetic frozen byte pin')
        return raw
    return take

STAMP = '2026-10-16T20:00:00+00:00'
PIN = S.pin(b'synthetic')
DATA = {'gate_pin': PIN, 'package': 'publication_package_SYNTHETIC', 'package_seal': PIN,
        'whole_package_reviews_completed': 2, 'DOI': '10.5281/zenodo.123456',
        'record_id': 123456, 'tracker_range': "'Math Puzzles'!A100:D100"}
for phase in S.PHASES:
    for actual in (False, True):
        run('phase_counts_' + phase + '_' + str(actual), lambda p=phase, a=actual: S.counts(p,a),
            predicate=lambda value,p=phase,a=actual: value == (S.DONE_COUNTS if p=='completion' and a else S.BASE_COUNTS))
        f = R.facts(DATA, actual) if phase=='ready' else L.facts(phase, DATA, actual)
        run('phase_facts_' + phase + '_' + str(actual), lambda f=f: f,
            predicate=lambda value,p=phase,a=actual: value['completed'] is (p=='completion' and a)
              and all(type(value[k]) is type(v) and value[k]==v for k,v in (S.DONE_COUNTS if p=='completion' and a else S.BASE_COUNTS).items()))
for phase in ('merge','factual','completion'):
    run('parents_' + phase, lambda p=phase: L.parents(p,'a'*40),
        predicate=lambda value,p=phase: value == (['a'*40,S.HEAD] if p=='merge' else ['a'*40]))
for bad in ('', '/abs', '../a', 'a/../b', 'a//b', 'a/./b', 'a\\b', 'a\0b'):
    run('unsafe_path_' + repr(bad), lambda v=bad:S.rel(v), True)
for bad in ({'bytes':True,'sha256':'0'*64}, {'bytes':1,'sha256':'A'*64},
            {'bytes':1.0,'sha256':'0'*64}, {'bytes':1,'sha256':'0'*64,'extra':0}):
    run('bad_bytepin_' + repr(bad), lambda v=bad:S.bytepin(v), True)
for raw in (b'{"a":1,"a":2}', b'{"a":NaN}', b'{"a":Infinity}'):
    run('bad_json_' + raw.decode(), lambda v=raw:S.decode(v), True)
for value in (1, 'true', None):
    run('nonbool_phase_actual_' + repr(value), lambda v=value:S.counts('completion',v), True)
run('authority_absent', S.authority, True)
if sys.flags.optimize:
    run('optimized_real_runtime_refused', S.runtime, True)

# Full-size synthetic expected map, independently defined without baseline bytes.
def qrow(identifier, marker, note):
    return ('|'.join(['',' 1 ',f' {identifier} / {marker} ']+[' '+note+' ']*10+[''])+'\n').encode()
OWN = qrow('5100062','AMR-050-0062','own')
PROTECTED = qrow('777','OTHER-777','protected')
UNPROTECTED = qrow('999','OTHER-999','old')
Q0 = OWN + PROTECTED + UNPROTECTED
Q1 = OWN + PROTECTED + qrow('999','OTHER-999','changed1')
Q2 = OWN + PROTECTED + qrow('999','OTHER-999','changed2')
EXPECTED = {S.CASE+f'synthetic_fixture/f{i:04d}.txt':S.bpin(f'synthetic {i}'.encode()) for i in range(4413)}
EXPECTED[S.Q] = S.bpin(Q0)
EXPECTED[S.ALL_NATIVE+'777/proof.md'] = S.bpin(b'protected777')
EXPECTED[S.NATIVE+'CURRENT_STATUS.json'] = S.bpin(b'own-current')
if len(EXPECTED) != 4416: raise RuntimeError('Independent fixture extent error')
PREP = {'commit':'a'*40,'tree':'1'*40,'expected_main':'9'*40,'parent_tree':'8'*40}
FACTS = R.facts(DATA,True)
def receipt_for(mapping):
    a={'schema':'pr206-lifecycle-actual-acceptance-v1','evidence_scope':'ACTUAL_ROOT_RECEIPT',
       'UTC':STAMP,'PR':206,'phase':'ready','accepted':True,'case_percent':90,
       'checkpoint_commit':PREP['commit'],'parents':[PREP['expected_main']],
       'sole_parent':PREP['expected_main'],'main_observed':'b'*40,'actual_tree':'2'*40,
       'original_head':S.HEAD,'selected_files':len(mapping['selected_files']),
       'selected_map_sha256':S.digest(EXPECTED),
       'actual_current_selected_map_sha256':S.digest(mapping['selected_files']),
       'actual_current_map_file':S.pin(S.enc(mapping)),
       'every_selected_identity_checked_at_actual_observed_MAIN':True,
       'all_overlay_body_identities_verified':True,'full_foreign_tree_scope_preserved':True,
       'original_native_custody_retained':True,'actual_original_PR_head':S.HEAD,
       'actual_original_PR_is_draft':True,'actual_original_PR_state':'open','facts':copy.deepcopy(FACTS)}
    for key in S.RECEIPT_ALIASES:a[key]=copy.deepcopy(FACTS[key])
    return a
BASE_MAP={'selected_files':copy.deepcopy(EXPECTED),'selected_map_sha256':S.digest(EXPECTED),
          'foreign_QUEUE_reconciliation_after_checkpoint':{}}
def check_map(mapping,receipt=None):
    return S.check_acceptance('ready', receipt or receipt_for(mapping),mapping,PREP,EXPECTED,FACTS,[PREP['expected_main']])
run('complete_4416_map_baseline',lambda:check_map(copy.deepcopy(BASE_MAP)))
for label, mutate in (
    ('truncated', lambda m:m['selected_files'].pop(next(iter(m['selected_files'])))),
    ('queue_only', lambda m:m.update(selected_files={S.Q:m['selected_files'][S.Q]})),
    ('extra',lambda m:m['selected_files'].update({S.CASE+'synthetic_fixture/extra':S.bpin(b'extra')})),
    ('substituted',lambda m:m['selected_files'].__setitem__(next(iter(m['selected_files'])),S.bpin(b'substitution'))),
    ('extra_map_key',lambda m:m.update(extra=True)),
):
    m=copy.deepcopy(BASE_MAP);mutate(m)
    # Rehash attacker-controlled maps and receipts; rejection cannot rely on a stale digest.
    if m['selected_files']:m['selected_map_sha256']=S.digest(m['selected_files'])
    run('rehash_map_'+label,lambda m=m:check_map(m),True)
for key in ('PR','selected_files','case_percent'):
    a=receipt_for(BASE_MAP);a[key]=float(a[key])
    run('acceptance_float_'+key,lambda a=a:check_map(BASE_MAP,a), key != 'case_percent')
for key in ('accepted','every_selected_identity_checked_at_actual_observed_MAIN','full_foreign_tree_scope_preserved','actual_original_PR_is_draft'):
    a=receipt_for(BASE_MAP);a[key]=1
    run('acceptance_nonbool_'+key,lambda a=a:check_map(BASE_MAP,a),True)
for alias in S.RECEIPT_ALIASES:
    a=receipt_for(BASE_MAP);a[alias]='CORRUPT'
    run('acceptance_alias_'+alias,lambda a=a:check_map(BASE_MAP,a),True)

# Native GET responses are pure in-memory records. This tests both reconstruction
# legs with real reconcile/body/_native_state/_accepted/_fresh_accepted logic.
class FakeH:
    def __init__(self, q_receipt=Q1, q_fresh=Q2):
        self.main='c'*40
        self.queues={'a'*40:Q0,'b'*40:q_receipt,'c'*40:q_fresh}
        self.trees={'a'*40:'1'*40,'b'*40:'2'*40,'c'*40:'3'*40}
        self.rows={tree:{path:('100644','blob',pin['git_blob']) for path,pin in EXPECTED.items()} for tree in self.trees.values()}
        self.blobs={}
        for commit,raw in self.queues.items():
            oid=S.bpin(raw)['git_blob'];self.rows[self.trees[commit]][S.Q]=('100644','blob',oid);self.blobs[oid]=raw
        self.pull={'head':{'sha':S.HEAD,'ref':'dot/math-5100062'},'base':{'ref':'main'},'state':'open','draft':True,'merged':False,
                   'title':'Original synthetic title','body':'Original synthetic body','created_at':'old','updated_at':'old','commits':4,'changed_files':22}
        self.m=types.SimpleNamespace(native_tree_cache={},verify_tree_object=lambda oid,rows:None)
        self.status='ahead'
    def api(self,endpoint,*args):
        if endpoint=='git/ref/heads/main':return {'object':{'sha':self.main}}
        if endpoint.startswith('compare/'):
            before,after=endpoint[8:].split('...');return {'status':'identical' if before==after else self.status}
        if endpoint.startswith('git/commits/'):
            oid=endpoint[12:];return {'sha':oid,'tree':{'sha':self.trees[oid]}}
        if endpoint.startswith('git/blobs/'):
            oid=endpoint[10:];raw=self.blobs[oid];return {'sha':oid,'encoding':'base64','content':base64.b64encode(raw).decode(),'size':len(raw)}
        if endpoint=='pulls/206':return copy.deepcopy(self.pull)
        raise RuntimeError('Unexpected synthetic endpoint '+endpoint)
    def lookup(self,tree,path):return self.rows[tree].get(path)
class FakeC:
    def selected_current(self,h,commit,selected,parent_tree):
        tree=h.trees[commit]
        S.need(all(h.lookup(tree,path)==('100644','blob',value['git_blob']) for path,value in selected.items()),'Synthetic every-selected mismatch')
        return tree
def native_scenario(label,q_receipt=Q1,q_fresh=Q2,mutator=None,status='ahead',fresh=True):
    h=FakeH(q_receipt,q_fresh);h.status=status;c=FakeC()
    with Patch(S, now=lambda:STAMP,queue_rows=lambda:(None,OWN,OWN)):
        try:
            _,ack=S.reconcile(c,h,{'commit':'a'*40,'tree':'1'*40,'selected_files':EXPECTED},'b'*40,OWN,STAMP)
        except Exception:
            ack={'UTC':STAMP,'baseline_actual_commit':'a'*40,'observed_MAIN':'b'*40,'old_QUEUE':S.bpin(Q0),'current_QUEUE':S.bpin(q_receipt),'foreign_unprotected_row_changes':[],'own_and_all_protected_rows_unchanged':True}
        m=copy.deepcopy(BASE_MAP);m['selected_files'][S.Q]=S.bpin(q_receipt);m['selected_map_sha256']=S.digest(m['selected_files']);m['foreign_QUEUE_reconciliation_after_checkpoint']=ack
        a=receipt_for(m)
        if mutator:mutator(a,m,h)
        files={'G/ACCEPTANCE.json':S.enc(a),'G/ACCEPTANCE_CURRENT_SELECTED_MAP.json':S.enc(m)}
        def fake_obj(path,expected=None):
            raw=files[path]
            if expected is not None:S.need(S.pin(raw)==expected,'Synthetic pinned file identity')
            return S.decode(raw)
        d=S.driver('ready')
        with Patch(S,_prepared=lambda phase,name:(c,h,DATA,d,'G/',PREP,{},EXPECTED),obj=fake_obj,
                   original_native=lambda h:None,frozen=checked_frozen(S.enc(h.pull)),ORIGINAL_METADATA=S.pin(S.enc(h.pull))):
            return S._fresh_accepted('ready','x') if fresh else S._accepted('ready','x')
run('real_two_leg_foreign_queue_reconstruction',lambda:native_scenario('baseline'))
run('protected_queue_laundering_checkpoint_to_receipt',lambda:native_scenario('bad',q_receipt=OWN+qrow('777','OTHER-777','BAD')+UNPROTECTED),True)
run('protected_queue_laundering_receipt_to_fresh',lambda:native_scenario('bad',q_fresh=OWN+qrow('777','OTHER-777','BAD')+UNPROTECTED),True)
run('own_queue_laundering',lambda:native_scenario('bad',q_receipt=qrow('5100062','AMR-050-0062','BAD')+PROTECTED+UNPROTECTED),True)
run('queue_ack_scope_mutation',lambda:native_scenario('bad',mutator=lambda a,m,h:m['foreign_QUEUE_reconciliation_after_checkpoint'].update(observed_MAIN='d'*40)),True)
run('receipt_nonqueue_laundering',lambda:native_scenario('bad',mutator=lambda a,m,h:m['selected_files'].__setitem__(next(iter(EXPECTED)),S.bpin(b'BAD'))),True)
for status in ('behind','diverged'):
    run('native_ancestry_'+status,lambda st=status:native_scenario('bad',status=st),True)

# Original90 guard: no current project bytes are read.
h=FakeH()
original=copy.deepcopy(h.pull)
with Patch(S,frozen=checked_frozen(S.enc(original)),ORIGINAL_METADATA=S.pin(S.enc(original))):
    run('original90_baseline',lambda:R.original(h,DATA))
    for key,value in (('draft',False),('state','closed'),('merged',True),('title','changed'),('body','changed'),('updated_at','changed'),('commits',5),('changed_files',61)):
        h.pull=copy.deepcopy(original);h.pull[key]=value
        run('original90_mutation_'+key,lambda:R.original(h,DATA),True)
    h.pull=copy.deepcopy(original);h.pull['head']['sha']='f'*40
    run('original90_wrong_head',lambda:R.original(h,DATA),True)

# Exact publication and tracker validation, with only ready-context/file boundary
# injection. Every receipt here is artificial and marked SYNTHETIC in metadata.
UPLOADS={'note.tex':S.pin(b'tex'),'note.pdf':S.pin(b'pdf'),'note.zip':S.pin(b'zip')}
G={'metadata':{'title':'SYNTHETIC ONLY','creators':[{'name':'Synthetic'}],'description':'Synthetic fixture'},
   'package':'publication_package_SYNTHETIC','package_safe_files':copy.deepcopy(UPLOADS),'intended_upload_files':copy.deepcopy(UPLOADS)}
CTX={'gate_pin':PIN,'ready_pointer_pin':PIN,'ready_acceptance_pin':PIN,'checkpoint_commit':'a'*40,
     'package':G['package'],'package_seal':PIN,'manifest_pin':PIN}
PUB={'schema':'pr206-root-publication-receipt-v1','evidence_scope':'ACTUAL_ROOT_RECEIPT','PR':206,'state':'published',
     'actual_publication_verified':True,'metadata_exact_verified':True,'all_three_public_download_SHA256_verified':True,
     'context':CTX,'package':G['package'],'gate_sha256':PIN['sha256'],'metadata_normalizations':[],
     'metadata':G['metadata'],'package_safe_files':G['package_safe_files'],'intended_upload_files':G['intended_upload_files'],
     'original_head':S.HEAD,'problem_id':5100062,'id':123456,'doi':'10.5281/zenodo.123456',
     'doi_url':'https://doi.org/10.5281/zenodo.123456','record_url':'https://zenodo.org/records/123456',
     'doi_resolution':{'http_status':200,'status':'resolved'},
     'files':[{'name':n,'size':v['bytes'],'sha256':v['sha256']} for n,v in UPLOADS.items()],
     'public_downloads':[{'name':n,**v,'url':'https://synthetic.invalid/'+n,'final_url':'https://synthetic.invalid/'+n} for n,v in UPLOADS.items()]}
COPIED=('id','doi','doi_url','record_url','metadata','package','package_safe_files','intended_upload_files','original_head','problem_id')
TRACK={'schema':'pr206-root-tracker-receipt-v1','evidence_scope':'ACTUAL_ROOT_RECEIPT','PR':206,
       'doi':PUB['doi'],'context':CTX,'publication_receipt':S.pin(S.enc(PUB)),'gate_sha256':PIN['sha256'],
       'row':S.tracker_row(G,PUB['doi']),'publication_facts':{key:copy.deepcopy(PUB[key]) for key in COPIED},
       'spreadsheet_id':'1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20','sheet_gid':1254632077,
       'range':"'Math Puzzles'!A100:D100",'original_preappend_baseline':{'file':'SYNTHETIC.json','pin':PIN,'row_count':99,'counter_sha256':'1'*64}}
FLAGS=('actual_tracker_row_verified','own_row_readback_verified','foreign_rows_retained','original_preappend_baseline_retained',
       'two_fresh_full_prechecks','two_fresh_full_readbacks','RAW_INSERT_ROWS','B_intentionally_blank_no_verified_chat_share_URL')
for key in FLAGS:TRACK[key]=True
def operations(p=None,t=None):
    p=copy.deepcopy(PUB if p is None else p);t=copy.deepcopy(TRACK if t is None else t)
    # Actual publication receipt pin follows this fixture's complete bytes.
    t['publication_receipt']=S.pin(S.enc(p))
    records={'ROOT_PUBLICATION_RECEIPT.json':p,'ROOT_TRACKER_RECEIPT.json':t}
    with Patch(S,ready_context=lambda:(G,CTX),artifact=lambda name,*args:copy.deepcopy(records[name]),frozen=lambda name,*args:S.enc(records[name])):
        return S.operations()
run('operations_baseline',operations)
for key in FLAGS:
    for value in (False,1,None):
        t=copy.deepcopy(TRACK);t[key]=value
        run('tracker_flag_'+key+'_'+repr(value),lambda t=t:operations(t=t),True)
    t=copy.deepcopy(TRACK);del t[key]
    run('tracker_flag_missing_'+key,lambda t=t:operations(t=t),True)
for key in ('metadata','package_safe_files','intended_upload_files','original_head','problem_id'):
    for action in ('remove','corrupt'):
        p=copy.deepcopy(PUB)
        if action=='remove':del p[key]
        elif isinstance(p[key],dict):p[key]['EXTRA']='CORRUPTION'
        else:p[key]='CORRUPTION'
        run('publication_copied_'+key+'_'+action,lambda p=p:operations(p=p),True)
for key in COPIED:
    for action in ('remove','corrupt'):
        t=copy.deepcopy(TRACK)
        if action=='remove':del t['publication_facts'][key]
        elif isinstance(t['publication_facts'][key],dict):t['publication_facts'][key]['EXTRA']='CORRUPTION'
        else:t['publication_facts'][key]='CORRUPTION'
        run('tracker_copied_'+key+'_'+action,lambda t=t:operations(t=t),True)
t=copy.deepcopy(TRACK);t['publication_facts']['EXTRA']=True
run('tracker_copied_extra',lambda:operations(t=t),True)
for name,mutate in (
    ('bad_doi',lambda p:p.update(doi='10.5281/zenodo.999999')),
    ('not_published',lambda p:p.update(state='draft')),
    ('bad_resolver',lambda p:p['doi_resolution'].update(http_status=404)),
    ('missing_upload',lambda p:p['files'].pop()),
    ('wrong_upload',lambda p:p['files'][0].update(sha256='0'*64)),
    ('missing_download',lambda p:p['public_downloads'].pop()),
    ('wrong_download',lambda p:p['public_downloads'][0].update(sha256='0'*64)),
):
    p=copy.deepcopy(PUB);mutate(p)
    run('operations_'+name,lambda p=p:operations(p=p),True)

# Repaired API: stable owned lock, valid owned generation, and protected session.
with tempfile.TemporaryDirectory(prefix='five_owned_',dir=HERE) as folder:
    root=Path(folder);(root/'owned').mkdir();(root/'views').mkdir()
    views=tuple('views/view'+str(i) for i in range(5));serial=[0];directory=['']
    lock='owned/LOCK';(root/lock).write_bytes(S.PROGRAM_VIEW_LOCK_BYTES);(root/lock).chmod(0o444)
    with Patch(S,ROOT=root,OWN='owned/',VIEWS=views,PROGRAM_VIEW_LOCK=lock):
        def reset():
            serial[0]+=1;directory[0]='owned/g'+str(serial[0])+'/'
            (root/directory[0]).mkdir()
            for path in views:
                q=root/path
                if q.is_symlink() or q.exists():q.unlink()
                q.write_bytes(b'OLD')
        def images():return [(p,S.pin(b'OLD'),b'POST') for p in views]
        def protected_sync():
            with S.WriterOwnership(directory[0]):return S.sync_images(images(),directory[0])
        reset();run('five_success',protected_sync,predicate=lambda rows:len(rows)==5 and all((root/p).read_bytes()==b'POST' and stat.S_IMODE((root/p).stat().st_mode)==0o444 for p in views))
        reset();(root/views[-1]).unlink();(root/views[-1]).symlink_to(root/views[0])
        run('five_symlink_preflight',protected_sync,True)
        run('five_symlink_no_earlier_write',lambda:all((root/p).read_bytes()==b'OLD' for p in views[:-1]),predicate=bool)
        reset();(root/views[-1]).write_bytes(b'CONCURRENT')
        run('five_bad_preimage_preflight',protected_sync,True)
        run('five_bad_preimage_no_earlier_write',lambda:all((root/p).read_bytes()==b'OLD' for p in views[:-1]),predicate=bool)
        reset();(root/directory[0]/'existing_receipt').write_bytes(b'OTHER')
        run('receipt_already_exists',lambda:S.atomic(directory[0]+'existing_receipt',b'OURS',None),True)
        reset();calls=[];original_atomic=S.atomic
        def fail_third(path,post,prior):
            calls.append(path)
            if len(calls)==3:raise OSError('Synthetic fsync/write failure')
            return original_atomic(path,post,prior)
        with Patch(S,atomic=fail_third):run('five_partial_failure',protected_sync,True)
        run('five_partial_extent',lambda:[(root/p).read_bytes() for p in views],predicate=lambda v:v==[b'POST',b'POST',b'OLD',b'OLD',b'OLD'])
        run('five_partial_rerun',protected_sync,predicate=lambda rows:all((root/p).read_bytes()==b'POST' for p in views))

out={'schema':'pr206-independent-synthetic-guards-v1','optimized':bool(sys.flags.optimize),
     'sources':SOURCES,'test_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
     'no_author_test_or_project_runtime_import':True,'synthetic_full_map_entries':len(EXPECTED),
     'tests':len(RESULTS),'passed':sum(x['pass'] for x in RESULTS),'failed':sum(not x['pass'] for x in RESULTS),
     'outcomes':RESULTS}
print(json.dumps(out,indent=2))
raise SystemExit(0 if out['failed']==0 else 1)
