#!/usr/bin/env python3
"""PR399 additional actual-helper controls; synthetic boundaries, never providers."""
import copy
from contextlib import ExitStack,redirect_stdout
import io
import json
from pathlib import Path
import socket
import subprocess
import sys
import tempfile
from unittest.mock import patch
import zipfile
HERE=Path(__file__).resolve().parent
AUDIT=HERE.parent
sys.path.insert(0,str(AUDIT))
import ops_binding as B
import prepublication_check as P
import publication_live_gates as G
import repository_integration as I
import publication_lifecycle as L
import verify_published_files as V
CASES=[]
PROVIDERS=[]

def check(value,message):
    if not value:raise RuntimeError('CONTROL CHECK FAILED: '+message)

def forbidden(*a,**k):
    PROVIDERS.append(True);raise RuntimeError('ACTUAL PROVIDER FORBIDDEN')

def expect(label,fn,ok=False):
    try:fn()
    except Exception as ex:
        CASES.append({'case':label,'expected':'accept' if ok else 'reject','actual':'reject','exception':type(ex).__name__,'reason':str(ex)[:400]})
        check(not ok,label+' unexpectedly rejected '+str(ex))
    else:
        CASES.append({'case':label,'expected':'accept' if ok else 'reject','actual':'accept'})
        check(ok,label+' unexpectedly accepted')

def write(p,v):
    p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,ensure_ascii=False)+'\n')

def package(work):
    raw=(B.PUBLICATION/'free-product-tensor-core-verification.zip').read_bytes()
    with zipfile.ZipFile(io.BytesIO(raw)) as z:contents={n:z.read(n) for n in z.namelist()}
    manifest=B.PREFIX+'FILES.json'
    listing=json.loads(contents[manifest])
    def altered(change):
        values=copy.deepcopy(contents);v=copy.deepcopy(listing);change(values,v)
        if v is not None:values[manifest]=json.dumps(v).encode()
        out=io.BytesIO()
        with zipfile.ZipFile(out,'w') as z:
            for name,data in values.items():z.writestr(name,data)
        return B.check_zip(out.getvalue())
    expect('actual_82_members_81_payloads_schema1',lambda:B.check_zip(raw),True)
    for label,change in [
        ('bool_schema',lambda c,v:v.update(schema=True)),('float_schema',lambda c,v:v.update(schema=1.0)),
        ('wrong_schema',lambda c,v:v.update(schema=2)),('unknown_top_key',lambda c,v:v.update(extra=True)),
        ('missing_schema',lambda c,v:v.pop('schema')),('files_mapping',lambda c,v:v.update(files={})),
        ('short_inventory',lambda c,v:v['files'].pop()),('duplicate_payload_entry',lambda c,v:v['files'].__setitem__(1,copy.deepcopy(v['files'][0]))),
        ('bool_bytes',lambda c,v:v['files'][0].update(bytes=True)),('float_bytes',lambda c,v:v['files'][0].update(bytes=702.0)),
        ('negative_bytes',lambda c,v:v['files'][0].update(bytes=-1)),('uppercase_hash',lambda c,v:v['files'][0].update(sha256=v['files'][0]['sha256'].upper())),
        ('extra_entry_field',lambda c,v:v['files'][0].update(extra=True)),('old_280_manifest_name',lambda c,v:(c.update({B.PREFIX+'MANIFEST.json':c.pop(manifest)}),v.clear())),
        ('payload_changed_same_length',lambda c,v:c.update({B.PREFIX+'CITATION.cff':b'x'*len(c[B.PREFIX+'CITATION.cff'])}))]:
        expect('zip_'+label,lambda change=change:altered(change))
    expect('duplicate_json_key',lambda:B.strict_json('{"schema":2,"schema":1,"files":[]}'))
    for name in ['', './a','a/../b','a//b','/a','a/./b','a\\b','C:a','a\x00b',True,None]:
        expect('unsafe_path_'+repr(name),lambda name=name:B.safe_file(work,name))
    expect('safe_nested_path',lambda:B.safe_file(work,'original/review/file.json'),True)
    target=work/'binding.txt';target.write_bytes(b'x');entry={'path':'binding.txt','bytes':1,'sha256':B.sha(b'x')}
    for key,value in [('bytes',True),('bytes',1.0),('bytes',-1),('sha256',entry['sha256'].upper()),('sha256',False),('path',True)]:
        e={**entry,key:value};expect('entry_exact_type_'+key+repr(value),lambda e=e:B.verify_entries(work,[e]))
    expect('entry_exact_binding',lambda:B.verify_entries(work,[entry]),True)
    expect('entry_duplicate',lambda:B.verify_entries(work,[entry,entry]))
    intent=work/'exclusive_intent.json'
    expect('intent_exclusive_initial',lambda:B.intent_json(intent,{'synthetic':True}),True)
    body=intent.read_bytes()
    expect('intent_existing_never_overwritten',lambda:B.intent_json(intent,{'changed':True}))
    check(intent.read_bytes()==body,'existing intent unchanged')
    row=__import__('record_publication_ledger').desired_row(999)
    check(len(row)==4 and row[1]=='','existing four-column ledger schema')
    for text in ['30001179','OWR-3392-005','tensor core','ordinal','ambient independence','23333353','30001178','30001180','30001182','PR533']:
        expect('candidate_lead_pattern_'+text,lambda text=text:check(bool(B.PATTERN.search(text)),'lead detected'),True)
    for text in ['finite replay','analytic infinite-dimensional proof','no formal independent human peer','continuous field','30001178','30001180','printed pages 528–530']:
        expect('desired_row_scope_'+text,lambda text=text:check(text.lower() in ' '.join(row).lower(),'scope wording present'),True)


def accounts():
    pr={'number':399,'state':'open','merged':False,'draft':True,
        'head':{'sha':B.ORIGINAL,'ref':B.BRANCH,'repo':{'full_name':'AlecKriebel/Math'}},
        'base':{'ref':'main','repo':{'full_name':'AlecKriebel/Math'}}}
    expect('exact_existing_branch',lambda:P.validate_pr(pr,B.ORIGINAL,'before_integration'),True)
    for label,branch in [('other_branch','different'),('missing_branch',None)]:
        v=copy.deepcopy(pr);v['head']['ref']=branch
        expect(label,lambda v=v:P.validate_pr(v,B.ORIGINAL,'before_integration'))
    class Client:
        base='https://synthetic.invalid'
        def __init__(self,identifier):self.identifier=identifier
        def request(self,*args):return {'hits':{'total':1,'hits':[{'id':self.identifier,'metadata':{},'files':[]}]}}
    for value in [True,1.0,'1',0,-1]:expect('exact_account_ID_'+repr(value),lambda value=value:P.account_search(Client(value),''))
    expect('exact_account_positive_integer_ID',lambda:P.account_search(Client(1),''),True)


def lifecycle(work):
    class Delegate:
        def __init__(self):self.calls=[];self.result={'id':999}
        def create(self,m):self.calls.append('create');return self.result
        def get(self,i):self.calls.append('get');return {'id':i}
        def upload(self,b,e):self.calls.append('upload');return {}
        def update(self,i,m):self.calls.append('update');return {}
        def publish(self,i):self.calls.append('publish');return {}
    def sequence():
        d=Delegate();events=[]
        def collect(phase,head,identifier):
            events.append((phase,head,identifier,len(d.calls)));return {'started_utc':B.stamp()},{}
        with patch.object(L,'require_release_clearance',lambda:True),patch.object(L,'collect',collect):
            c=L.GuardedLifecycleClient('stage','a'*40,delegate=d)
            c.create({});c.upload('synthetic',{});c.upload('synthetic',{});c.update(999,{})
            check([e[2] for e in events]==[None,999,999,999],'allocated ID tracked between every mutation')
            check([e[3] for e in events]==[0,1,2,3],'fresh gate occurs before each synthetic write')
            c=L.GuardedLifecycleClient('publish','a'*40,999,delegate=d);c.publish(999)
            check(events[-1][0]=='before_publish','publish-specific fresh phase')
    expect('fresh_gate_before_each_create_upload_update_publish',sequence,True)
    def rejected(label,action,identifier,method,*args):
        d=Delegate()
        with patch.object(L,'require_release_clearance',lambda:True),patch.object(L,'collect',lambda *a:({'started_utc':B.stamp()},{})):
            c=L.GuardedLifecycleClient(action,'a'*40,identifier,delegate=d)
            expect(label,lambda:getattr(c,method)(*args))
            check(not d.calls,label+' zero synthetic writes')
    rejected('publish_cannot_create','publish',999,'create',{})
    rejected('stage_cannot_publish','stage',999,'publish',999)
    rejected('publish_cannot_update','publish',999,'update',999,{})
    rejected('upload_without_allocated_ID','stage',None,'upload','synthetic',{})
    rejected('second_allocation','stage',999,'create',{})
    rejected('update_wrong_ID','stage',999,'update',998,{})
    rejected('get_wrong_ID','stage',999,'get',998)
    for mode in ['stale','rejected']:
        d=Delegate()
        def collect(*a):
            if mode=='rejected':raise RuntimeError('synthetic fresh lead')
            return {'started_utc':'2000-01-01T00:00:00+00:00'},{}
        with patch.object(L,'require_release_clearance',lambda:True),patch.object(L,'collect',collect):
            c=L.GuardedLifecycleClient('stage','a'*40,delegate=d)
            expect('lifecycle_no_write_on_'+mode,lambda:c.create({}))
            check(not d.calls,'failed gate prevents delegate mutation')
    expect('unknown_lifecycle_action',lambda:L.run_action('unexpected','a'*40))


def repository(work):
    original=I.originals();selected=I.selection()
    root=work/'repository';root.mkdir()
    head='a'*40;main='b'*40;test='c'*40;actual='d'*40
    def fixture():
        all_selected={**original,**{n:('100644','blob',I.blob_sha(v)) for n,v in selected.items()}}
        old={'retained.txt':('100644','blob','same')}
        leaves={main:old,test:{**old,**all_selected},actual:{**old,**all_selected}}
        queues={main:b'other\n'+I.BASELINE_ROW,test:b'other\n'+I.DESIRED_ROW,actual:b'other\n'+I.DESIRED_ROW,
                head:I.DESIRED_ROW,B.ORIGINAL:I.DESIRED_ROW,B.ORIGINAL_PARENT:I.BASELINE_ROW}
        return leaves,queues
    def run(label,mutation=lambda c,l,q:None,action='merge',ok=False,writes=0,intent=None):
        for path in root.glob('*.json'):path.unlink()
        if intent:write(root/intent,{'prior_uncertain_operation':True})
        pr={'number':399,'state':'open','merged':False,'draft':False,'mergeable':True,'merge_commit_sha':test,
            'head':{'sha':head,'ref':B.BRANCH,'repo':{'full_name':'AlecKriebel/Math'}},
            'base':{'ref':'main','repo':{'full_name':'AlecKriebel/Math'}}}
        cfg={'pr':pr,'test_parents':[main,head],'actual_parents':[main,head],'main_reads':[main]*5,'merged':True}
        leaf,queue=fixture();mutation(cfg,leaf,queue);calls=[];main_values=iter(cfg['main_reads'])
        def api(endpoint,method='GET',body=None):
            if endpoint=='pulls/399':return copy.deepcopy(cfg['pr'])
            if endpoint=='git/ref/heads/main':return {'object':{'sha':next(main_values)}}
            if endpoint=='git/commits/'+B.ORIGINAL:return {'parents':[{'sha':B.ORIGINAL_PARENT}]}
            if endpoint in {'git/commits/'+test,'git/commits/'+actual}:
                which='test_parents' if endpoint.endswith(test) else 'actual_parents'
                return {'sha':test if which=='test_parents' else actual,'parents':[{'sha':v} for v in cfg[which]],'tree':{'sha':'synthetic'}}
            if endpoint=='pulls/399/merge' and method=='PUT':
                check(body['sha']==head and body['merge_method']=='merge','exact head passed to actual merge')
                check((root/'PR_MERGE_INTENT.json').exists(),'durable intent before merge')
                calls.append(body);return {'merged':cfg['merged'],'sha':actual}
            raise RuntimeError('Unexpected synthetic API '+endpoint)
        def subtree(commit,path,recursive=True):
            if path=='':return {'unsolved_math_prioritization':{'mode':'040000','type':'tree','sha':commit},'other':{'mode':'100644','type':'blob','sha':'unchanged'}}
            if path=='unsolved_math_prioritization':return {'attempts':{'mode':'040000','type':'tree','sha':commit},'QUEUE.md':{'mode':'100644','type':'blob','sha':commit},'sibling':{'mode':'100644','type':'blob','sha':'unchanged'}}
            return {'30001179':{'mode':'040000','type':'tree','sha':commit},'sibling':{'mode':'040000','type':'tree','sha':'unchanged'}}
        with patch.object(I,'AUDIT',root),patch.object(I,'api',api),patch.object(I,'verify_destination',lambda:True),\
             patch.object(I,'originals',lambda:original),patch.object(I,'require_release_clearance',lambda:True),patch.object(I,'collect',lambda *a:({'receipt':'synthetic','started_utc':B.stamp()},{})),\
             patch.object(I,'leaves',lambda c,p:leaf[c]),patch.object(I,'blob',lambda c,p:queue[c]),patch.object(I,'subtree',subtree),\
             patch.object(sys,'argv',['repository_integration.py',action,'--expected-pr-head',head]):
            with redirect_stdout(io.StringIO()):expect(label,I.main,ok)
        check(len(calls)==writes,label+' exact merge-write count')
        if writes and not ok:check((root/'PR_MERGE_INTENT.json').exists(),'uncertain merge intent preserved')
    run('test_merge_actual_preservation',action='verify-test-merge',ok=True)
    run('actual_merge_exact_parents_and_preservation',ok=True,writes=1)
    run('test_merge_wrong_parent',lambda c,l,q:c.update(test_parents=[head,main]))
    run('test_merge_extra_parent',lambda c,l,q:c.update(test_parents=[main,head,'e'*40]))
    run('stale_test_merge',lambda c,l,q:c.update(test_parents=['e'*40,head]))
    run('concurrent_main_during_check',lambda c,l,q:c.update(main_reads=[main,'e'*40]))
    run('concurrent_main_before_merge',lambda c,l,q:c.update(main_reads=[main,main,'e'*40]))
    run('unmergeable_PR',lambda c,l,q:c['pr'].update(mergeable=False))
    run('draft_PR_cannot_merge',lambda c,l,q:c['pr'].update(draft=True))
    run('test_merge_candidate_missing',lambda c,l,q:l[test].pop(next(iter(original))))
    run('test_merge_other_queue_changed',lambda c,l,q:q.update({test:q[test]+b'changed'}))
    run('actual_merge_parent_wrong',lambda c,l,q:c.update(actual_parents=[head,main]),writes=1)
    run('actual_merge_candidate_changed',lambda c,l,q:l[actual].update({next(iter(original)):('100644','blob','changed')}),writes=1)
    run('actual_merge_queue_changed',lambda c,l,q:q.update({actual:q[actual]+b'changed'}),writes=1)
    run('merge_unconfirmed_no_retry',lambda c,l,q:c.update(merged=False),writes=1)
    run('prior_merge_intent_no_blind_retry',intent='PR_MERGE_INTENT.json')
    # The branch intent blocks before object or ref writes, even while PR is still original.
    write(root/'PUBLICATION_BRANCH_PUSH_INTENT.json',{'uncertain':True})
    pr={'number':399,'state':'open','merged':False,'draft':True,'head':{'sha':B.ORIGINAL,'ref':B.BRANCH,'repo':{'full_name':'AlecKriebel/Math'}},'base':{'ref':'main','repo':{'full_name':'AlecKriebel/Math'}}}
    with patch.object(I,'AUDIT',root),patch.object(I,'verify_destination',lambda:True),patch.object(I,'api',lambda *a,**k:pr),\
         patch.object(sys,'argv',['repository_integration.py','commit','--expected-pr-head',B.ORIGINAL]):
        expect('prior_ref_intent_no_object_or_ref_retry',I.main)


def main():
    with ExitStack() as guards:
        guards.enter_context(patch.object(subprocess,'run',forbidden));guards.enter_context(patch.object(V,'urlopen',forbidden))
        guards.enter_context(patch.object(socket,'socket',forbidden))
        for name in ['request','create','upload','update','publish','get']:guards.enter_context(patch.object(B.zenodo.ZenodoClient,name,forbidden))
        with tempfile.TemporaryDirectory(prefix='candidate_',dir=HERE) as temp:
            work=Path(temp);package(work);accounts();lifecycle(work);repository(work)
    check(not PROVIDERS,'zero actual provider attempts')
    result={'timestamp_utc':B.stamp(),'optimization':sys.flags.optimize,'all_controls_passed':True,'controls':len(CASES),
            'accepted':sum(v['actual']=='accept' for v in CASES),'rejected':sum(v['actual']=='reject' for v in CASES),
            'actual_provider_access_attempts':len(PROVIDERS),'release_manifest_sha256':B.RELEASE_SHA,'cases':CASES,
            'scope':'Actual candidate-specific helper functions, actual frozen local release, synthetic account/ledger/GitHub/Zenodo boundaries only; no live outcomes.'}
    write(HERE/('CANDIDATE_CONTROLS_OPTIMIZED.json' if sys.flags.optimize else 'CANDIDATE_CONTROLS.json'),result)
    print(json.dumps({k:v for k,v in result.items() if k!='cases'},indent=2))
if __name__=='__main__':main()
