#!/usr/bin/env python3
"""ROOT02 actual live branch-pointer controls; all services are explicit fakes."""
import sys
if not(sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode):raise RuntimeError('Use Python -I -S -B')
from pathlib import Path
from datetime import datetime,timezone
import copy,hashlib,json,traceback
W=Path(__file__).absolute().parent;P=W.parents[3]
p=P/'accept_pr948.py';raw=p.read_bytes();N={'__name__':'_inert_live_base_','__file__':str(p)}
exec(compile(raw,str(p),'exec',dont_inherit=True,optimize=0),N)
started=datetime.now(timezone.utc).isoformat();results=[];root_pins={}
def must(value):
    if not value:raise RuntimeError('Condition false')
def test(name,action):
    try:action();results.append({'name':name,'status':'PASS'})
    except Exception as error:
        results.append({'name':name,'status':'FAIL','error':str(error)});raise
def reject(action,fragment=None):
    try:action()
    except (RuntimeError,ValueError,KeyError,TypeError,OSError) as error:
        if fragment:must(fragment in str(error))
        return
    raise RuntimeError('Unsafe live-base fixture accepted')
class Patch:
    def __init__(self,**values):self.values=values
    def __enter__(self):self.old={k:N[k] for k in self.values};N.update(self.values)
    def __exit__(self,*a):N.update(self.old)
class Fake:
    def __init__(self,live='d'*40):
        self.metadata={'number':952,'state':'OPEN','isDraft':True,'headRefOid':'e'*40,'headRefName':'synthetic','baseRefName':'main','baseRefOid':'d'*40,'url':'https://example.invalid/952'}
        self.live=live;self.calls=[];self.change_node=None;self.change_files=None;self.advance_on_queue=False;self.pages=1
    def node(self):return {**self.metadata,'baseRef':{'name':'main','target':{'oid':self.live}}}
    def run(self,args,*a,**kw):
        if args[:3]==['gh','pr','view']:
            self.calls.append('gh_metadata')
            return json.dumps({k:self.metadata[k] for k in args[args.index('--json')+1].split(',')})
        if args[:3]!=['gh','api','graphql']:raise RuntimeError('Unexpected operation')
        query=next(v[6:] for v in args if v.startswith('query='))
        if 'object(expression:$expr)' in query:
            self.calls.append('immutable_QUEUE')
            if self.advance_on_queue:self.live='f'*40
            queue=b'| 1 | 111 / SYNTHETIC | A | 0 | 0 | 0 | 0 | claimed_solved | 4/5 | | | |\n| 2 | 222 / SYNTHETIC | B | 0 | 0 | 0 | 0 | unsolved | 5/5 | | | |\n'
            return json.dumps({'data':{'repository':{'object':{'text':queue.decode(),'byteSize':len(queue),'isBinary':False,'oid':'a'*40}}}})
        if 'baseRef{name target{oid}}' not in query:raise RuntimeError('Live pointer was not requested')
        node=self.node()
        if 'files(first:100' in query:
            self.calls.append('filenames')
            cursor=next((x for x in args if x.startswith('cursor=')),None)
            key='111' if self.live=='d'*40 else '222'
            node.update(changedFiles=self.pages,files={'nodes':[{'path':'unsolved_math_prioritization/attempts/'+key+'/proof.md' if cursor is None else 'unsolved_math_prioritization/QUEUE.md'}],'pageInfo':{'hasNextPage':self.pages==2 and cursor is None,'endCursor':'NEXT' if self.pages==2 and cursor is None else None}})
            if self.change_files:self.change_files(node,cursor)
        else:
            self.calls.append('live_metadata')
            if self.change_node:self.change_node(node)
        return json.dumps({'data':{'repository':{'pullRequest':node}}})
old={'number':952,'headRefOid':'c'*40,'entries':[{'id':'111'}]}
error=None
try:
    r=W.parent/'root_live_base_context'
    expected={'LIVE_BASE_OBSERVATION.json':'56c98fb9fa861ab99c394be98216197f0ffca2eeb940d153ee2e2af595cfd146','STORED_BASE_WITNESS.json':'7bf3de6e52600200ba9576e34f1223904108834ac98c96794fd61e8af41cb906','witness_stored_base.py':'0b685aadb94ff97d6d86b17e46569301fd897b6b2af384004deb90d6111a511d'}
    bodies={}
    for name,pin in expected.items():
        b=(r/name).read_bytes();must(hashlib.sha256(b).hexdigest()==pin)
        root_pins[name]={'bytes':len(b),'sha256':pin};bodies[name]=b
    observed=json.loads(bodies['LIVE_BASE_OBSERVATION.json'])
    test('LIVE_base_actual_observation_distinguishes_stored_and_current',lambda:must(observed['stored_base_ref_oid']!=observed['live_base_ref_target_oid']==observed['repository_main_oid']))
    f=Fake('f'*40)
    with Patch(run=f.run):
        test('LIVE_pr_view_preserves_associated_base_and_normalizes_live_target',lambda:must(N['pr_view'](952)['baseRefOid']=='d'*40 and N['pr_view'](952)['currentBaseRefOid']=='f'*40))
    def broken_ref(label):
        def change(node):
            if label=='missing':node.pop('baseRef')
            elif label=='null':node['baseRef']=None
            elif label=='target_null':node['baseRef']['target']=None
            elif label=='oid_missing':node['baseRef']['target'].pop('oid')
            elif label=='oid_null':node['baseRef']['target']['oid']=None
            elif label=='oid_malformed':node['baseRef']['target']['oid']='bad'
            elif label=='oid_uppercase':node['baseRef']['target']['oid']='F'*40
            elif label=='wrong_ref_name':node['baseRef']['name']='other'
        return change
    for label in ('missing','null','target_null','oid_missing','oid_null','oid_malformed','oid_uppercase','wrong_ref_name'):
        f=Fake();f.change_node=broken_ref(label)
        with Patch(run=f.run):test('LIVE_pr_view_'+label+'_rejects',lambda:reject(lambda:N['pr_view'](952)))
    for key,value in [('number',967),('state','CLOSED'),('isDraft',False),('headRefOid','a'*40),('headRefName','other'),('baseRefName','other'),('baseRefOid','a'*40),('url','https://example.invalid/other')]:
        f=Fake();f.change_node=lambda node,key=key,value=value:node.update({key:value})
        with Patch(run=f.run):test('LIVE_augmentation_binds_'+key,lambda:reject(lambda:N['pr_view'](952),'metadata changed'))
    f=Fake('f'*40)
    initial={**old,'headRefOid':f.metadata['headRefOid'],'baseRefOid':'d'*40}
    with Patch(run=f.run):
        test('LIVE_matching_stored_base_alone_does_not_authorize_reuse',lambda:must(N['gate_next']([initial])[1] is None and 'filenames' in f.calls))
        f.calls.clear()
        def consistent_reuse():
            skipped,selected=N['gate_next']([{**initial,'currentBaseRefOid':'f'*40,'entries':[{'id':'222'}]}])
            must(selected is None and skipped[0]['problem_id']=='222' and 'filenames' not in f.calls)
        test('LIVE_independently_recorded_matching_current_base_reuses_consistent_target',consistent_reuse)
        for label,value in [('malformed','bad'),('different','d'*40),('null',None)]:
            f.calls.clear()
            test('LIVE_initial_live_base_'+label+'_derives_unsolved',lambda value=value:must(N['gate_next']([{**initial,'currentBaseRefOid':value}])[1] is None and 'filenames' in f.calls))
    for label in ('missing','null','oid_malformed'):
        f=Fake();f.change_files=lambda node,cursor,label=label:broken_ref(label)(node)
        with Patch(run=f.run):test('LIVE_filename_page_'+label+'_rejects',lambda:reject(lambda:N['gate_next']([old])))
    f=Fake();f.change_files=lambda node,cursor:node['baseRef']['target'].update(oid='f'*40)
    with Patch(run=f.run):test('LIVE_page_pointer_drift_with_stored_base_unchanged_rejects',lambda:reject(lambda:N['gate_next']([old]),'metadata changed'))
    f=Fake();f.pages=2
    f.change_files=lambda node,cursor:node['baseRef']['target'].update(oid='f'*40) if cursor is not None else None
    with Patch(run=f.run):test('LIVE_second_page_pointer_drift_stored_unchanged_rejects',lambda:reject(lambda:N['gate_next']([old]),'metadata changed'))
    f=Fake();f.advance_on_queue=True
    with Patch(run=f.run):test('LIVE_status_bracket_pointer_drift_stored_unchanged_rejects',lambda:reject(lambda:N['gate_next']([old]),'changed across status-only'))
    f=Fake();f.advance_on_queue=True
    initial={**old,'headRefOid':f.metadata['headRefOid'],'currentBaseRefOid':'d'*40}
    with Patch(run=f.run):test('LIVE_reused_identity_still_rejects_closing_live_pointer_drift',lambda:reject(lambda:N['gate_next']([initial]),'changed across status-only'))
    f=Fake('f'*40)
    with Patch(run=f.run):test('LIVE_stable_live_advance_same_head_and_stored_base_derives_new_unsolved',lambda:must(N['gate_next']([{**old,'headRefOid':f.metadata['headRefOid'],'baseRefOid':'d'*40}])[1] is None and 'filenames' in f.calls))
    for label,value in [('missing','MISSING'),('null',None),('malformed','bad')]:
        before={**Fake().metadata,'currentBaseRefOid':value}
        if value=='MISSING':before.pop('currentBaseRefOid')
        test('LIVE_next_identity_'+label+'_normalized_pointer_rejects_before_reads',lambda before=before:reject(lambda:N['next_identity'](old,before),'live base commit'))
    witness=bodies['witness_stored_base.py'].decode();must(witness.count('target=Path(__file__).with_name')==1)
    ns={'__name__':'_authenticated_stored_base_witness_','__file__':str(r/'witness_stored_base.py')}
    exec(compile(witness.split('target=Path(__file__).with_name')[0],'<authenticated-root-stored-base-witness>','exec',dont_inherit=True,optimize=0),ns)
    test('LIVE_exact_old851_DAG_witness_reproduces_wrong_claimed_selection',lambda:must(ns['out']['actual_historical_gate_selected']['problem_id']=='1000001' and ns['out']['current_comparison_problem_id']=='1000002' and ns['hidden']['base']=='M'))
    ns['hidden']['base']='D';ns['calls'].clear()
    def corrected_witness_service(args,*a,**kw):
        query=next((v[6:] for v in args if v.startswith('query=')),None)
        if query is not None and 'baseRef{name target{oid}}' in query and 'files(first:100' not in query:
            node={**ns['metadata'],'baseRefOid':ns['oids']['D'],'baseRef':{'name':'main','target':{'oid':ns['oids'][ns['hidden']['base']]}}}
            return json.dumps({'data':{'repository':{'pullRequest':node}}})
        output=ns['fake_run'](args,*a,**kw)
        if query is not None and 'files(first:100' in query:
            data=json.loads(output);data['data']['repository']['pullRequest']['baseRef']={'name':'main','target':{'oid':ns['oids'][ns['hidden']['base']]}}
            output=json.dumps(data)
        return output
    with Patch(run=corrected_witness_service):test('LIVE_exact_same_DAG_corrected_gate_rejects_live_only_race',lambda:reject(lambda:N['gate_next'](ns['inventory']),'changed across status-only'))
    test('LIVE_inherited_finding_set_remains50',lambda:must(len(N['INHERITED_FINDING_IDS'])==50))
except Exception:error=traceback.format_exc()
receipt={'schema':'pr948-live-base-context-tests-v1','started_utc':started,'completed_utc':datetime.now(timezone.utc).isoformat(),'status':'FAIL' if error else 'PASS','passed':sum(x['status']=='PASS' for x in results),'failed':sum(x['status']=='FAIL' for x in results),'tests':results,'error':error,'core_sha256':hashlib.sha256(raw).hexdigest(),'root_evidence_authenticated_before_intake':root_pins,'actual_functions':['live_base_pointer','pr_view','next_identity','gate_next'],'external_service_calls':0,'mathematics_source_reads':0,'new_author_proof_responses':0,'candidate2_or_acceptance_created':False}
print(json.dumps({'status':receipt['status'],'passed':receipt['passed'],'failed':receipt['failed'],'printed_before_receipt_write':True}))
number=len(list(W.glob('LIVE_BASE_ATTEMPT_*.json')))+1;target=Path('/Users/alec/Documents/Math/draft_pr_claimed_solved_900_1000_20261012/audits/pr948_30004549/reviews/full_package_02/LIVE_BASE.json')
target.write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps({'receipt_saved':str(target)}))
if error:print(error,file=sys.stderr);raise SystemExit(1)
