__file__='/Users/alec/Documents/Math/draft_pr_claimed_solved_900_1000_20261012/audits/pr948_30004549/publication/workflow/test_base_context.py'
#!/usr/bin/env python3
"""ROOT02 base-commit amendment: synthetic status metadata only, zero services."""
import sys
if not (sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode):
    raise RuntimeError('Use Python -I -S -B')
import ast,copy,hashlib,json,traceback
from pathlib import Path
from datetime import datetime,timezone
W=Path(__file__).absolute().parent
P=W.parents[3];ROOT=P.parent
started=datetime.now(timezone.utc).isoformat()
p=P/'accept_pr948.py';raw=p.read_bytes()
N={'__name__':'_inert_base_context_','__file__':str(p)}
exec(compile(raw,str(p),'exec',dont_inherit=True,optimize=0),N)
results=[]
def must(value):
    if not value:raise RuntimeError('Condition false')
def test(name,action):
    try:action();results.append({'name':name,'status':'PASS'})
    except Exception as error:
        results.append({'name':name,'status':'FAIL','error':str(error)})
        raise
def reject(action,fragment=None):
    try:action()
    except (RuntimeError,ValueError,KeyError,TypeError,OSError) as error:
        if fragment is not None:must(fragment in str(error))
        return
    raise RuntimeError('Unsafe metadata fixture accepted')
class Patch:
    def __init__(self,**values):self.values=values
    def __enter__(self):self.old={k:N[k] for k in self.values};N.update(self.values)
    def __exit__(self,*args):N.update(self.old)
before={'number':952,'state':'OPEN','isDraft':True,'headRefOid':'e'*40,'headRefName':'inert','baseRefName':'main','baseRefOid':'d'*40,'currentBaseRefOid':'d'*40,'url':'https://example.invalid/952'}
old={'number':952,'headRefOid':'c'*40,'entries':[{'id':'111'}]}
queue=b'| 1 | 111 / OLD | old | 0 | 0 | 0 | 0 | claimed_solved | 4/5 | | | |\n| 2 | 222 / NEW | new | 0 | 0 | 0 | 0 | unsolved | 5/5 | | | |\n'
calls=[]
def service(args,*a,**kw):
    calls.append(args)
    if args[:3]==['gh','pr','view']:
        fields=args[args.index('--json')+1].split(',')
        return json.dumps({k:before[k] for k in fields})
    if args[:3]!=['gh','api','graphql']:raise RuntimeError('Unexpected external operation')
    query=next(x[6:] for x in args if x.startswith('query='))
    if 'files(first:100' in query:
        node={**before,'changedFiles':1,'files':{'nodes':[{'path':'unsolved_math_prioritization/attempts/222/proof.md'}],'pageInfo':{'hasNextPage':False,'endCursor':None}}}
        return json.dumps({'data':{'repository':{'pullRequest':node}}})
    if 'object(expression:$expr)' not in query:raise RuntimeError('Unexpected mathematics read')
    return json.dumps({'data':{'repository':{'object':{'text':queue.decode(),'isBinary':False,'byteSize':len(queue),'oid':'a'*40}}}})
def complete_live_transport(original):
    # Earlier synthetic controls intentionally had associated and live bases equal.
    # Supply the newly requested nested live pointer without adding service calls.
    latest={}
    def transport(args,*a,**kw):
        query=next((x[6:] for x in args if x.startswith('query=')),None)
        if query is not None and 'baseRef{' in query and 'files(first:' not in query:
            node={**latest,'baseRef':{'name':latest.get('baseRefName'),'target':{'oid':latest.get('currentBaseRefOid',latest.get('baseRefOid'))}}}
            return json.dumps({'data':{'repository':{'pullRequest':node}}})
        output=original(args,*a,**kw)
        if args[:3]==['gh','pr','view']:latest.clear();latest.update(json.loads(output))
        elif query is not None and 'files(first:' in query:
            data=json.loads(output);node=data['data']['repository']['pullRequest']
            node['baseRef']={'name':node.get('baseRefName'),'target':{'oid':node.get('currentBaseRefOid',node.get('baseRefOid',before['currentBaseRefOid']))}}
            output=json.dumps(data)
        return output
    return transport
error=None
root_pins={}
try:
    with Patch(run=complete_live_transport(service)):
        test('ROOT02_pr_view_requests_baseRefOid',lambda:must(N['pr_view'](952)['baseRefOid']==before['baseRefOid'] and 'baseRefOid' in calls[-1][-1]))
        test('ROOT02_stable_base_changed_head_new_unsolved_SKIPS',lambda:must(N['gate_next']([old])[1] is None))
        calls.clear()
        test('ROOT02_stable_base_unchanged_head_reuses_inventory',lambda:must(N['gate_next']([{**old,'headRefOid':before['headRefOid'],'currentBaseRefOid':before['currentBaseRefOid']}])[1]['problem_id']=='111' and len(calls)==3 and not any('files(first:100' in ' '.join(x) for x in calls)))
    with Patch(run=complete_live_transport(service)):
        for label,value in [('missing','MISSING'),('different','f'*40),('malformed','bad-oid'),('null',None)]:
            initial={**old,'headRefOid':before['headRefOid']}
            if value!='MISSING':initial['currentBaseRefOid']=value
            calls.clear()
            test('ROOT02_same_head_original_base_'+label+'_derives_current_unsolved',lambda initial=initial:must(N['gate_next']([initial])[1] is None and any('files(first:100' in ' '.join(x) for x in calls)))
    for label,value in [('missing','MISSING'),('null',None),('short','d'*39),('nonhex','g'*40),('uppercase','D'*40)]:
        bad=copy.deepcopy(before)
        if value=='MISSING':bad.pop('currentBaseRefOid')
        else:bad['currentBaseRefOid']=value
        test('ROOT02_before_base_'+label+'_rejects',lambda bad=bad:reject(lambda:N['next_identity'](old,bad),'base commit identity'))
    def page_change(value):
        def run(args,*a,**kw):
            data=json.loads(service(args));node=data['data']['repository']['pullRequest']
            if value=='MISSING':node.pop('baseRefOid')
            else:node['baseRefOid']=value
            return json.dumps(data)
        return run
    for label,value in [('missing','MISSING'),('null',None),('malformed','not-a-commit'),('advance','f'*40)]:
        with Patch(run=complete_live_transport(page_change(value))):
            test('ROOT02_changed_file_page_base_'+label+'_rejects',lambda:reject(lambda:N['next_identity'](old,before),'metadata changed'))
    def paged(args,*a,**kw):
        cursor=next((x for x in args if x.startswith('cursor=')),None)
        node={**before,'changedFiles':2,'files':{'nodes':[{'path':'unsolved_math_prioritization/attempts/222/proof.md' if cursor is None else 'unsolved_math_prioritization/QUEUE.md'}],'pageInfo':{'hasNextPage':cursor is None,'endCursor':'NEXT' if cursor is None else None}}}
        if cursor is not None:node['baseRefOid']='f'*40
        return json.dumps({'data':{'repository':{'pullRequest':node}}})
    with Patch(run=complete_live_transport(paged)):test('ROOT02_second_page_base_advance_rejects',lambda:reject(lambda:N['next_identity'](old,before),'metadata changed'))
    def closing_changed(args,*a,**kw):
        if args[:3]==['gh','pr','view']:
            closing_changed.views+=1
            node={**before,'baseRefOid':before['baseRefOid'] if closing_changed.views==1 else 'f'*40}
            return json.dumps({k:node[k] for k in args[args.index('--json')+1].split(',')})
        return service(args,*a,**kw)
    with Patch(run=complete_live_transport(closing_changed)):
        closing_changed.views=0
        test('ROOT02_base_only_advance_after_complete_files_rejects',lambda:reject(lambda:N['gate_next']([old]),'changed across status-only'))
        closing_changed.views=0
        test('ROOT02_unchanged_head_closing_base_advance_rejects',lambda:reject(lambda:N['gate_next']([{**old,'headRefOid':before['headRefOid'],'currentBaseRefOid':before['currentBaseRefOid']}]),'changed across status-only'))
    # Authenticate root's exact witness BEFORE executing its inert, pre-write part.
    r=W.parent/'root_status_context'
    expected={'witness.py':'5c14bc6fd8e946b743f92f6c38ab4dc63926ef3d7d35fc871221f5bdea7f32d5','WITNESS.json':'9e2cd73e5c2082863b8e3804ae02e0bc8b801c2e6b2e860a2a952bcc043eb2bf','WITNESS_UNCHANGED_HEAD.json':'de016038966703dbe13106f9172d98d406d431b27072533c39ae181a345e6a40'}
    bodies={}
    for name,pin in expected.items():
        body=(r/name).read_bytes();must(hashlib.sha256(body).hexdigest()==pin)
        bodies[name]=body;root_pins[name]={'bytes':len(body),'sha256':pin}
    witness=bodies['witness.py'].decode()
    must(witness.count('target=Path(__file__).with_name')==1)
    ns={'__name__':'_authenticated_old_DAG_witness_','__file__':str(r/'witness.py')}
    exec(compile(witness.split('target=Path(__file__).with_name')[0],'<authenticated-old-root-witness>','exec',dont_inherit=True,optimize=0),ns)
    test('ROOT02_exact_root_DAG_old_code_reproduces_wrong_claimed_target',lambda:must(ns['out']['old_merge_base']=='O' and ns['out']['new_merge_base']=='C2' and ns['out']['actual_historical_gate_selected']['problem_id']=='1000001' and ns['out']['current_comparison_problem_id']=='1000002' and ns['out']['current_comparison_status']=='unsolved'))
    ns['hidden']['base']='D';ns['calls'].clear()
    with Patch(run=complete_live_transport(ns['fake_run'])):
        test('ROOT02_exact_root_DAG_new_code_rejects_base_race',lambda:reject(lambda:N['gate_next'](ns['inventory']),'changed across status-only'))
    test('ROOT02_exact_root_DAG_requested_base_in_all_metadata',lambda:must(all(x['baseRefOid_requested'] for x in ns['calls'] if 'baseRefOid_requested' in x)))
    # Same authenticated DAG, with the base already stably advanced before reads.
    stable_calls=[]
    def stable_advanced(args,*a,**kw):
        node={**ns['metadata'],'baseRefOid':ns['oids']['M']}
        if args[:3]==['gh','pr','view']:
            stable_calls.append('metadata')
            return json.dumps({k:node[k] for k in args[args.index('--json')+1].split(',')})
        query=next(v[6:] for v in args if v.startswith('query='))
        if 'files(first:100' in query:
            stable_calls.append('filenames')
            node.update(changedFiles=1,files={'nodes':[{'path':ns['paths']['B']}],'pageInfo':{'hasNextPage':False,'endCursor':None}})
            return json.dumps({'data':{'repository':{'pullRequest':node}}})
        if 'object(expression:$expr)' not in query:raise RuntimeError('Unexpected source read')
        stable_calls.append('QUEUE')
        return json.dumps({'data':{'repository':{'object':{'text':ns['queue'].decode(),'isBinary':False,'byteSize':len(ns['queue']),'oid':'a'*40}}}})
    initial=[{**ns['inventory'][0],'headRefOid':ns['metadata']['headRefOid']}]
    ns['N']['run']=stable_advanced
    test('ROOT02_exact_stable_base_DAG_old_head_only_reuse_selects_wrong_claimed',lambda:must(ns['N']['gate_next'](initial)[1]['problem_id']=='1000001' and 'filenames' not in stable_calls))
    stable_calls.clear()
    with Patch(run=complete_live_transport(stable_advanced)):
        test('ROOT02_exact_stable_base_DAG_new_missing_initial_base_derives_unsolved',lambda:must(N['gate_next'](initial)[1] is None and 'filenames' in stable_calls))
    oldraw=(W/'history/full01_pre_fix/operations'/P.name/'accept_pr948.py').read_text()
    def functions(text):return {node.name:''.join(text.splitlines(True)[node.lineno-1:node.end_lineno]) for node in ast.parse(text).body if isinstance(node,ast.FunctionDef)}
    prior,current=functions(oldraw),functions(raw.decode())
    test('ROOT02_only_four_existing_gate_functions_changed_since_candidate1',lambda:must(all(current[name]==text for name,text in prior.items() if name not in ('result_schema','review_check','pr_view','next_identity'))))
    test('ROOT02_inherited_ID_set_stays_exact50',lambda:must(len(N['INHERITED_FINDING_IDS'])==50))
except Exception:error=traceback.format_exc()
receipt={'schema':'pr948-root02-base-context-tests-v1','started_utc':started,'completed_utc':datetime.now(timezone.utc).isoformat(),'status':'FAIL' if error else 'PASS','passed':sum(x['status']=='PASS' for x in results),'failed':sum(x['status']=='FAIL' for x in results),'tests':results,'error':error,'core_sha256':hashlib.sha256(raw).hexdigest(),'root_witness_authenticated_before_content':root_pins,'actual_functions':['pr_view','next_identity','gate_next'],'real_external_calls':0,'mathematics_source_reads':0,'real_candidate2_created':False}
print(json.dumps({'status':receipt['status'],'passed':receipt['passed'],'failed':receipt['failed'],'printed_before_receipt_write':True}))
number=len(list(W.glob('BASE_CONTEXT_ATTEMPT_*.json')))+1
target=Path('/Users/alec/Documents/Math/draft_pr_claimed_solved_900_1000_20261012/audits/pr948_30004549/reviews/full_package_07')/'INERT_BASE_CONTEXT.json'
target.write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({'receipt_saved':str(target)}))
if error:print(error,file=sys.stderr);raise SystemExit(1)
