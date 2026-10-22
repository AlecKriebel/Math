#!/usr/bin/env python3
"""Actual PR280 functions; synthetic providers only. Explicit checks survive python -O."""
import argparse
import copy
from contextlib import ExitStack
import datetime as dt
import hashlib
import importlib
import io
import json
from pathlib import Path
import shutil
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
import verify_published_files as V
import publication_lifecycle as L
import record_publication_ledger as D

CASES=[]
CALLS=[]

def check(value,message):
    if not value:
        raise RuntimeError('OFFLINE TEST CHECK FAILED: '+message)


def forbidden(*args,**kwargs):
    CALLS.append((str(args[:2]),str(kwargs)[:150]))
    raise RuntimeError('REAL PROVIDER ACCESS FORBIDDEN IN OFFLINE CONTROLS')


def expect(label,fn,ok=False):
    before=len(CALLS)
    try:
        result=fn()
    except Exception as ex:
        CASES.append({'case':label,'expected':'accept' if ok else 'reject','actual':'reject',
                      'exception':type(ex).__name__,'reason':str(ex)[:400]})
        check(not ok,label+' unexpectedly rejected: '+str(ex))
    else:
        CASES.append({'case':label,'expected':'accept' if ok else 'reject','actual':'accept'})
        check(ok,label+' unexpectedly accepted')
    check(len(CALLS)==before,label+' attempted actual provider access')


def write(path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')


def bind(path,root):
    data=path.read_bytes()
    return {'path':path.relative_to(root).as_posix(),'bytes':len(data),'sha256':B.sha(data)}


def mutations(base,items,fn):
    for label,mutation in items:
        value=copy.deepcopy(base)
        mutation(value)
        expect(label,lambda value=value:fn(value))


def test_package(work):
    expect('exact_current_five_file_manifest_two_uploads_zip65_payloads64',B.manifest,True)
    croot=work/'clearance';pub=croot/'preprint/publication';pub.mkdir(parents=True)
    for name in B.NAMES|{'RELEASE_FILES.json'}:
        shutil.copyfile(B.PUBLICATION/name,pub/name)
    for name in B.HELPERS:
        shutil.copyfile(AUDIT/name,croot/name)
    write(croot/'ROOT_PREPUBLICATION_LEAD_RECONCILIATION.json',{'synthetic':True})
    reviews=[]
    for n in range(2):
        for name in ['REPORT.md','SEAL.json']:
            p=croot/'reviews'/('synthetic'+str(n))/name
            p.parent.mkdir(parents=True,exist_ok=True);p.write_text('synthetic artifact\n')
        reviews.append({'reviewer':'synthetic'+str(n),'report_path':'reviews/synthetic'+str(n)+'/REPORT.md',
                        'seal_path':'reviews/synthetic'+str(n)+'/SEAL.json'})
    base={'pr':280,'problem_id':'30000156','original_head':B.ORIGINAL,'publication_ready':True,
          'unresolved_material_findings':[],'files':B.release()['files'],'release_manifest_sha256':B.RELEASE_SHA,
          'root_complete_reports_read_and_all_seals_verified':True,'sequential_new_reviewers':reviews,
          'bound_review_artifacts':[bind(croot/r[k],croot) for r in reviews for k in ['report_path','seal_path']],
          'bound_operational_files':[bind(croot/n,croot) for n in sorted(B.HELPERS|{'ROOT_PREPUBLICATION_LEAD_RECONCILIATION.json'})]}
    with patch.object(B,'AUDIT',croot),patch.object(B,'PUBLICATION',pub):
        def ccheck(c):
            write(croot/'ROOT_PUBLICATION_CLEARANCE.json',c)
            return B.require_release_clearance()
        expect('root_clearance_exact_helpers_reports_seals_package',lambda:ccheck(base),True)
        mutations(base,[('clearance_not_ready',lambda c:c.update(publication_ready=False)),
           ('clearance_wrong_problem',lambda c:c.update(problem_id='9700002')),
           ('clearance_wrong_head',lambda c:c.update(original_head='0'*40)),
           ('clearance_wrong_release_hash',lambda c:c.update(release_manifest_sha256='0'*64)),
           ('clearance_unresolved',lambda c:c.update(unresolved_material_findings=['issue'])),
           ('clearance_root_report_verification_missing',lambda c:c.pop('root_complete_reports_read_and_all_seals_verified')),
           ('clearance_one_reviewer',lambda c:c.update(sequential_new_reviewers=c['sequential_new_reviewers'][:1])),
           ('clearance_duplicate_reviewer',lambda c:c['sequential_new_reviewers'][1].update(reviewer='synthetic0')),
           ('clearance_missing_report_binding',lambda c:c['bound_review_artifacts'].pop()),
           ('clearance_missing_operational_binding',lambda c:c['bound_operational_files'].pop()),
           ('clearance_file_hash_changed',lambda c:c['files'][0].update(sha256='0'*64))],ccheck)
        for name in ['ops_binding.py','reviews/synthetic0/REPORT.md','reviews/synthetic1/SEAL.json',
                     'ROOT_PREPUBLICATION_LEAD_RECONCILIATION.json','preprint/publication/fixed-birational-cycle-nonlimit.pdf']:
            p=croot/name;old=p.read_bytes();p.write_bytes(old+b'x')
            expect('bound_changed_'+name,lambda:ccheck(base));p.write_bytes(old)
    with patch.object(B,'AUDIT',work/'missing_root_clearance'):
        expect('missing_root_clearance_fixture_blocks',B.require_release_clearance)
    expect('fresh_now',lambda:B.fresh(B.stamp()),True)
    for name,value in [('stale',(dt.datetime.now(dt.timezone.utc)-dt.timedelta(minutes=4)).isoformat()),
                       ('future',(dt.datetime.now(dt.timezone.utc)+dt.timedelta(minutes=1)).isoformat()),
                       ('naive','2026-10-21T00:00:00'),('malformed','bad')]:
        expect('gate_timestamp_'+name,lambda value=value:B.fresh(value))
    expect('sheet_four_column_full_schema',lambda:B.schema_rows({'values':[B.HEADERS,['synthetic','','','']]}),True)
    expect('actual_initial_ledger_wrapper',lambda:B.ledger_baseline(json.loads((B.ROOT/'raw/pr0280/ledger_live.json').read_text())),True)
    expect('sheet_extra_header_column',lambda:B.schema_rows({'values':[B.HEADERS+['extra']]}))
    expect('sheet_extra_data_column',lambda:B.schema_rows({'values':[B.HEADERS,['a','','','','private']]}))
    expect('sheet_wrong_wrapper',lambda:B.ledger_baseline({'response':{'values':[B.HEADERS]}}))
    raw=(B.PUBLICATION/'fixed-birational-cycle-nonlimit-verification.zip').read_bytes()
    def zipmutate(mutator):
        with zipfile.ZipFile(io.BytesIO(raw)) as archive:
            values={n:archive.read(n) for n in archive.namelist()}
        mutator(values)
        output=io.BytesIO()
        with zipfile.ZipFile(output,'w') as z:
            for n,v in values.items():z.writestr(n,v)
        return B.check_zip(output.getvalue())
    expect('zip_internal_payload_changed',lambda:zipmutate(lambda v:v.update({B.PREFIX+'paper/main.tex':b'changed'})))
    expect('zip_missing_payload',lambda:zipmutate(lambda v:v.pop(B.PREFIX+'paper/main.tex')))
    expect('zip_unsafe_payload',lambda:zipmutate(lambda v:v.update({'../escape':b'bad'})))


def test_accounts():
    class Client:
        base='https://synthetic.invalid'
        def __init__(self,pages):self.pages=iter(pages)
        def request(self,method,url):
            check(method=='GET','account method must GET')
            return next(self.pages)
    def record(i):return {'id':i,'metadata':{'title':'Synthetic'},'files':[]}
    def page(total,ids,nexturl=None):
        return {'hits':{'total':total,'hits':[record(i) for i in ids]},'links':{'next':nexturl} if nexturl else {}}
    nexturl='https://synthetic.invalid/api/user/records?page=2'
    expect('full_account_two_pages_and_exact_total',lambda:P.account_search(Client([page(2,[1],nexturl),page(2,[2])]),''),True)
    for label,pages in [('inexact_total',[page({'relation':'gte','value':1},[1])]),
        ('changing_total',[page(2,[1],nexturl),page(3,[2])]),('duplicate',[page(2,[1],nexturl),page(2,[1])]),
        ('missing_records',[page(2,[1])]),('loop',[page(2,[1],nexturl),page(2,[2],nexturl)]),
        ('bool_total',[page(True,[1])]),('negative_total',[page(-1,[])]),
        ('foreign_next',[page(2,[1],'https://evil.invalid/page2')])]:
        expect('account_'+label,lambda pages=pages:P.account_search(Client(pages),''))
    pr={'number':280,'state':'open','merged':False,'draft':True,'head':{'sha':B.ORIGINAL,'repo':{'full_name':'AlecKriebel/Math'}},
        'base':{'ref':'main','repo':{'full_name':'AlecKriebel/Math'}}}
    expect('pr_exact_open_integration',lambda:P.validate_pr(pr,B.ORIGINAL,'before_integration'),True)
    mutations(pr,[('pr_wrong_head',lambda p:p['head'].update(sha='0'*40)),
        ('pr_wrong_destination',lambda p:p['base']['repo'].update(full_name='other/Math')),
        ('pr_wrong_base',lambda p:p['base'].update(ref='different')),
        ('pr_closed_without_merge',lambda p:p.update(state='closed')),
        ('pr_already_merged_integration',lambda p:p.update(state='closed',merged=True))],
        lambda p:P.validate_pr(p,B.ORIGINAL,'before_integration'))
    expect('stage_requires_merged_pr',lambda:P.validate_pr(pr,B.ORIGINAL,'before_stage'))
    pr.update(state='closed',merged=True)
    expect('stage_accepts_exact_merged_pr',lambda:P.validate_pr(pr,B.ORIGINAL,'before_stage'),True)


def test_gates(work):
    root=work/'gate';raw=root/'raw';raw.mkdir(parents=True)
    record={'id':101,'metadata':{'title':'Synthetic birational lead independently distinct'},
            'files':[{'key':'other.pdf','size':1,'checksum':'md5:abc'}]}
    account={'total':1,'records':[record]}
    prior=['synthetic Vivaldi different model','','','Synthetic distinct object']
    recon={'pr':280,'root_identity_reconciliation_complete':True,'unresolved_leads':[],
           'release_manifest_sha256':B.RELEASE_SHA,
           'account_leads':[{'record':101,'disposition':'distinct_non_target','metadata_and_files_sha256':B.digest(B.identity_projection(record))}],
           'ledger_leads':[{'values_sha256':B.digest(prior),'disposition':'distinct_non_target'}]}
    gate={'started_utc':B.stamp(),'completed_utc':B.stamp(),'phase':'before_publish','expected_pr_head':'a'*40,
          'expected_deposit_id':None,'read_only':True,'release_manifest_sha256':B.RELEASE_SHA,
          'release_files':B.release()['files'],'account_positive_control':'PASS_23174283','raw_receipts':str(raw),
          'receipt':str(raw/'gate.json'),'account_complete_total':1,'account_complete_sha256':'set below',
          'unexpected_account_matches':[{'id':101}],'ledger_matches':[{'row':2,'values':prior}],
          'local_deposit_state_matches':[]}
    with patch.object(G,'AUDIT',root):
        def run(label,mutation=lambda a,g,c:None,ok=False,identifier=None,allow=False):
            a,g,c=copy.deepcopy(account),copy.deepcopy(gate),copy.deepcopy(recon)
            g['expected_deposit_id']=identifier
            mutation(a,g,c)
            write(raw/'account_complete.json',a);g['account_complete_sha256']=B.sha((raw/'account_complete.json').read_bytes())
            write(raw/'gate.json',g);write(root/'ROOT_PREPUBLICATION_LEAD_RECONCILIATION.json',c)
            expect(label,lambda:G.reconcile(g,'before_publish','a'*40,identifier,allow),ok)
        run('root_reconciled_full_metadata_files_exact',ok=True)
        run('new_unmatched_draft_blocks',lambda a,g,c:(a['records'].append({'id':102,'metadata':{'title':'birational draft'},'files':[]}),a.update(total=2),g.update(account_complete_total=2),g['unexpected_account_matches'].append({'id':102})))
        run('root_reconciliation_incomplete',lambda a,g,c:c.update(root_identity_reconciliation_complete=False))
        run('root_reconciliation_unresolved',lambda a,g,c:c.update(unresolved_leads=['new lead']))
        run('metadata_only_exemption_rejected',lambda a,g,c:c['account_leads'][0].pop('metadata_and_files_sha256'))
        run('implicit_non_target_disposition_rejected',lambda a,g,c:c['account_leads'][0].pop('disposition'))
        run('wrong_head_gate',lambda a,g,c:g.update(expected_pr_head='b'*40))
        run('wrong_phase_gate',lambda a,g,c:g.update(phase='before_stage'))
        run('expired_gate',lambda a,g,c:g.update(started_utc='2000-01-01T00:00:00+00:00'))
        run('malformed_gate',lambda a,g,c:g.pop('completed_utc'))
        for label,mutation in [('known_metadata_changed',lambda r:r['metadata'].update(title='changed')),
            ('known_file_name_changed',lambda r:r['files'][0].update(key='changed.pdf')),
            ('known_file_size_changed',lambda r:r['files'][0].update(size=2)),
            ('known_file_checksum_changed',lambda r:r['files'][0].update(checksum='md5:changed')),
            ('known_file_removed',lambda r:r.update(files=[])),
            ('known_file_added',lambda r:r['files'].append({'key':'new.pdf','size':0,'checksum':'md5:bad'})),
            ('known_files_schema_changed',lambda r:r.update(files={}))]:
            run(label,lambda a,g,c,mutation=mutation:mutation(a['records'][0]))
        run('reconciled_account_record_missing',lambda a,g,c:(a.update(records=[],total=0),g.update(account_complete_total=0)))
        run('new_ledger_lead',lambda a,g,c:g['ledger_matches'].append({'row':3,'values':['30000156','','','new']}))
        run('changed_ledger_lead',lambda a,g,c:g['ledger_matches'][0]['values'].append('changed'))
        run('unexpected_local_state',lambda a,g,c:g['local_deposit_state_matches'].append({'deposit_id':999}))
        run('expected_record_missing',identifier=999)
        def add_expected(a,g,c):
            a['records'].append({'id':999,'metadata':{'title':B.TITLE},'files':[]});a['total']=2;g['account_complete_total']=2
        run('exact_expected_target_allowed_with_local_state',lambda a,g,c:(add_expected(a,g,c),g['local_deposit_state_matches'].append({'deposit_id':999})),True,999)
        run('target_cannot_be_root_exempt_non_target',lambda a,g,c:(add_expected(a,g,c),c['account_leads'].append({'record':999,'disposition':'distinct_non_target','metadata_and_files_sha256':B.digest(a['records'][1])})),identifier=999)
        def add_row(a,g,c):
            add_expected(a,g,c);g['ledger_matches'].append({'row':3,'values':D.desired_row(999)})
        run('exact_target_ledger_idempotence',add_row,True,999,True)
        run('target_same_DOI_changed_notes_rejected',lambda a,g,c:(add_row(a,g,c),g['ledger_matches'][-1]['values'].__setitem__(3,'changed')),identifier=999,allow=True)
        run('duplicate_exact_target_rows_rejected',lambda a,g,c:(add_row(a,g,c),g['ledger_matches'].append(copy.deepcopy(g['ledger_matches'][-1]))),identifier=999,allow=True)


def test_collector(work):
    root=work/'collector';raw=root/'private';repo=root/'repo';repo.mkdir(parents=True)
    baseline={'checked_at':B.stamp(),'response':{'values':[B.HEADERS,['unrelated','','','']]}}
    write(root/'raw/pr0280/ledger_live.json',baseline)
    pr={'number':280,'state':'open','merged':False,'draft':True,'head':{'sha':B.ORIGINAL,'repo':{'full_name':'AlecKriebel/Math'}},
        'base':{'ref':'main','repo':{'full_name':'AlecKriebel/Math'}}}
    local_metadata,local_files=B.manifest()
    records=[{'id':201,'metadata':{'title':'Synthetic birational draft'},'files':[]},
             {'id':202,'metadata':{'title':'Synthetic unrelated filename'},'files':[{'key':'different.pdf','checksum':'md5:'+local_files[0]['md5'],'size':local_files[0]['size']}]},
             {'id':203,'metadata':{'title':'Synthetic other subject'},'files':[]}]
    class Client:
        base='https://synthetic.invalid'
        def request(self,method,url):
            check(method=='GET','collector only GET')
            return {'hits':{'total':0,'hits':[]}}
    def run(label,mutate=lambda q,p,s:None,ok=False,identifier=None):
        account=copy.deepcopy(records);live=copy.deepcopy(pr);sheet=copy.deepcopy(baseline['response'])
        mutate(account,live,sheet)
        def search(client,query):
            values=([{'id':23174283,'metadata':{'title':'Synthetic Fibonacci control'},'files':[]}] if query=='Fibonacci'
                    else account if query=='' else [])
            return {'query':query,'total':len(values),'pages':1,'records':values}
        def command(args):
            if args[0]=='gws':return sheet
            if args[-1].endswith('/pulls/280'):return live
            if args[-1].endswith('/git/ref/heads/main'):return {'object':{'sha':'b'*40}}
            raise RuntimeError('Unexpected synthetic command boundary')
        with patch.object(P,'ROOT',root),patch.object(P,'PRIVATE',raw),patch.object(P,'REPO',repo),\
             patch.object(P,'verify_destination',lambda:True),patch.object(P,'read_command',command),\
             patch.object(P,'account_search',search),patch.object(P.zenodo,'ZenodoClient',lambda *a:Client()),\
             patch.object(P.zenodo,'token_for',lambda *a:'synthetic token never used'):
            def gather():
                gate=P.gather('before_integration',B.ORIGINAL,identifier)
                check(set(gate['account_targets'])=={201,202},'whole account catches keyword-omitted model and exact file checksum draft')
                return gate
            expect(label,gather,ok)
    run('collector_keyword_omitted_new_draft_and_file_match_found',ok=True)
    run('collector_expected_draft_from_full_account',ok=True,identifier=201)
    run('collector_expected_draft_missing_blocks',identifier=999)
    run('collector_head_changed_blocks',lambda q,p,s:p['head'].update(sha='0'*40))
    run('collector_wrong_destination_blocks',lambda q,p,s:p['head']['repo'].update(full_name='other/Math'))
    run('collector_ledger_extra_column_blocks',lambda q,p,s:s['values'][0].append('extra'))


def test_integration():
    original=I.originals();selected=I.selection()
    queue=b'other row\n'+I.BASELINE_ROW+b'end\n'
    desired=b'other row\n'+I.DESIRED_ROW+b'end\n'
    def entry(sha,kind='blob'):return {'mode':'040000' if kind=='tree' else '100644','type':kind,'sha':sha}
    def fixture():
        leaves={'b':{'previous.txt':('100644','blob','previous')},'m':{'previous.txt':('100644','blob','previous'),**original,**{n:('100644','blob',I.blob_sha(v)) for n,v in selected.items()}}}
        blobs={'b':queue,'m':desired,'h':desired,B.ORIGINAL:desired,B.ORIGINAL_PARENT:queue}
        sub={}
        for c in ['b','m']:
            sub[c,'']={'unsolved_math_prioritization':entry(c+'unsolved','tree'),'other.txt':entry('same')}
            sub[c,'unsolved_math_prioritization']={'QUEUE.md':entry(c+'queue'),'attempts':entry(c+'attempts','tree'),'other.md':entry('same')}
            sub[c,'unsolved_math_prioritization/attempts']={'30000156':entry(c+'target','tree'),'other_attempt':entry('same','tree')}
        return leaves,blobs,sub
    def run(label,mutation=lambda a,b,c:None,ok=False):
        a,b,c=fixture();mutation(a,b,c)
        with patch.object(I,'leaves',lambda commit,path:a[commit]),patch.object(I,'blob',lambda commit,path:b[commit]),\
             patch.object(I,'subtree',lambda commit,path,recursive:c[commit,path]),\
             patch.object(I,'api',lambda endpoint:{'parents':[{'sha':B.ORIGINAL_PARENT}]}):
            expect(label,lambda:I.verify_integrated_tree('b','m','h'),ok)
    run('exact17_plus5_preserves_all_nested_siblings_and_other_queue',ok=True)
    run('main_has_exact_desired_row',lambda a,b,c:b.update(b=desired),True)
    name=next(iter(original))
    for label,mutation in [('concurrent_original_collision',lambda a,b,c:a['b'].update({name:('100644','blob','changed')})),
        ('integrated_original_missing',lambda a,b,c:a['m'].pop(name)),
        ('integrated_original_changed',lambda a,b,c:a['m'].update({name:('100644','blob','changed')})),
        ('publication_payload_changed',lambda a,b,c:a['m'].update({'preprint/fixed-birational-cycle-nonlimit.pdf':('100644','blob','changed')})),
        ('publication_payload_missing',lambda a,b,c:a['m'].pop('preprint/fixed-birational-cycle-nonlimit.pdf')),
        ('unselected_target_payload_lost',lambda a,b,c:a['m'].pop('previous.txt')),
        ('unselected_target_payload_added',lambda a,b,c:a['m'].update({'extra.txt':('100644','blob','extra')})),
        ('own_queue_concurrent_status',lambda a,b,c:b.update(b=queue.replace(b'| queued | 0/5 |',b'| active | 1/5 |'))),
        ('own_queue_baseline_wrong_notes',lambda a,b,c:b.update(b=queue.replace(b'|  |  |  |',b'|  | unexpected |  |'))),
        ('status_only_reconstruction_rejected',lambda a,b,c:b.update(b=desired.replace(b'| claimed_solved | 1/5 |',b'| queued | 0/5 |'))),
        ('reviewed_head_notes_changed',lambda a,b,c:b.update(h=desired.replace(b'Reviewed counterexample',b'Changed counterexample'))),
        ('original_parent_notes_changed',lambda a,b,c:b.update({B.ORIGINAL_PARENT:desired})),
        ('other_queue_bytes_changed',lambda a,b,c:b.update(m=desired.replace(b'other row',b'changed row'))),
        ('duplicate_own_queue',lambda a,b,c:b.update(m=desired+I.DESIRED_ROW)),
        ('unselected_root_changed',lambda a,b,c:c['m',''].update({'other.txt':entry('changed')})),
        ('unselected_unsolved_sibling_changed',lambda a,b,c:c['m','unsolved_math_prioritization'].update({'other.md':entry('changed')})),
        ('unselected_attempt_sibling_changed',lambda a,b,c:c['m','unsolved_math_prioritization/attempts'].update({'other_attempt':entry('changed','tree')}))]:
        run(label,mutation)


def test_repository_mutation_adapter(work):
    root=work/'repository_adapter';root.mkdir()
    original=I.originals();selected=I.selection();new='c'*40
    base_pr={'number':280,'state':'open','merged':False,'draft':True,
             'head':{'sha':B.ORIGINAL,'ref':'reviewed280','repo':{'full_name':'AlecKriebel/Math'}},
             'base':{'ref':'main','repo':{'full_name':'AlecKriebel/Math'}}}
    def run(label,mutation=lambda p:None,gate_failure=False,clearance_failure=False,ok=False,expected_ref_writes=0):
        pr=copy.deepcopy(base_pr);mutation(pr);calls=[]
        for p in root.glob('PUBLICATION_*.json'):p.unlink()
        def api(endpoint,method='GET',body=None):
            calls.append((endpoint,method,body))
            if endpoint=='pulls/280':return copy.deepcopy(pr)
            if endpoint=='git/commits/'+B.ORIGINAL:return {'tree':{'sha':'original-tree'},'parents':[{'sha':B.ORIGINAL_PARENT}]}
            if endpoint=='git/blobs' and method=='POST':
                return {'sha':I.blob_sha(__import__('base64').b64decode(body['content']))}
            if endpoint=='git/trees' and method=='POST':
                check(body['base_tree']=='original-tree','overlay uses original exact tree')
                check({e['path'] for e in body['tree']}=={B.PROBLEM+'/'+n for n in selected},'exact five overlay paths')
                return {'sha':'new-tree'}
            if endpoint=='git/commits' and method=='POST':return {'sha':new,'tree':{'sha':'new-tree'},'parents':[{'sha':B.ORIGINAL}]}
            if endpoint=='git/refs/heads/reviewed280' and method=='PATCH':
                check(body=={'sha':new,'force':False},'branch update is exact non-forced')
                check((root/'PUBLICATION_BRANCH_PUSH_INTENT.json').exists(),'durable branch intent precedes ref update')
                pr['head']['sha']=new;return {'object':{'sha':new}}
            raise RuntimeError('Unexpected synthetic API '+endpoint+' '+method)
        def collect(*args):
            if gate_failure:raise RuntimeError('synthetic dedup gate failure')
            return {'receipt':'synthetic'},{}
        def clearance():
            if clearance_failure:raise RuntimeError('synthetic missing root clearance')
            return True
        def leaves(c,p):return original if c==B.ORIGINAL else {**original,**{n:('100644','blob',I.blob_sha(v)) for n,v in selected.items()}}
        with patch.object(I,'AUDIT',root),patch.object(I,'api',api),patch.object(I,'verify_destination',lambda:True),\
             patch.object(I,'collect',collect),patch.object(I,'require_release_clearance',clearance),\
             patch.object(I,'leaves',leaves),patch.object(I,'originals',lambda:original),\
             patch.object(I,'blob',lambda c,p:I.BASELINE_ROW if c==B.ORIGINAL_PARENT else I.DESIRED_ROW),\
             patch.object(I,'subtree',lambda c,p,r:{}),\
             patch.object(sys,'argv',['repository_integration.py','commit','--expected-pr-head',B.ORIGINAL]):
            from contextlib import redirect_stdout
            with redirect_stdout(io.StringIO()):expect(label,I.main,ok)
        writes=[v for v in calls if v[1]=='PATCH']
        check(len(writes)==expected_ref_writes,label+' ref update count')
        if not ok:
            check(not any(v[1]!='GET' for v in calls),label+' no mutation before failed early gate')
    run('repository_adapter_exact5_overlay_nonforceFF_intent',ok=True,expected_ref_writes=1)
    run('repository_adapter_failed_gate_no_provider_mutation',gate_failure=True)
    run('repository_adapter_missing_clearance_no_provider_mutation',clearance_failure=True)
    run('repository_adapter_wronghead_no_provider_mutation',lambda p:p['head'].update(sha='0'*40))
    run('repository_adapter_closed_state_no_provider_mutation',lambda p:p.update(state='closed'))
    run('repository_adapter_wrong_destination_no_provider_mutation',lambda p:p['base']['repo'].update(full_name='wrong/Math'))


def test_public():
    metadata,selected=B.manifest()
    files=[{'key':v['name'],'size':v['size'],'checksum':'md5:'+v['md5']} for v in selected]
    inspection={'id':999,'state':'published','doi':'10.5281/zenodo.999','doi_url':'https://doi.org/10.5281/zenodo.999',
                'doi_resolution':{'http_status':200,'resolved_url':'https://zenodo.org/records/999'}}
    public_metadata=copy.deepcopy(metadata)
    public_metadata.pop('upload_type');public_metadata.pop('publication_type')
    public_metadata['resource_type']={'type':'publication','subtype':'preprint','title':'Preprint'}
    public_metadata['license']={'id':'cc-by-4.0'}
    public={'id':999,'doi':'10.5281/zenodo.999','metadata':public_metadata,'files':files}
    downloads={v['name']:(v['path'].read_bytes(),200,'https://synthetic.invalid/'+v['name']) for v in selected}
    def run(label,mutation=lambda p,i,d:None,ok=False):
        p,i,d=copy.deepcopy(public),copy.deepcopy(inspection),copy.deepcopy(downloads)
        mutation(p,i,d)
        expect(label,lambda:V.verify_public_record(999,metadata,selected,i,p,d,200),ok)
    run('exact_public_metadata_pdf_zip65_payloads64_DOI200',ok=True)
    for label,mutation in [('public_wrong_DOI',lambda p,i,d:p.update(doi='10.5281/zenodo.998')),
        ('public_wrong_id',lambda p,i,d:p.update(id=998)),
        ('public_wrong_resource_type',lambda p,i,d:p['metadata']['resource_type'].update(type='dataset')),
        ('public_wrong_resource_subtype',lambda p,i,d:p['metadata']['resource_type'].update(subtype='article')),
        ('public_missing_resource_type',lambda p,i,d:p['metadata'].pop('resource_type')),
        ('public_wrong_resource_title',lambda p,i,d:p['metadata']['resource_type'].update(title='Other')),
        ('public_conflicting_deposition_type',lambda p,i,d:p['metadata'].update(upload_type='publication')),
        ('public_wrong_license_id',lambda p,i,d:p['metadata']['license'].update(id='closed')),
        ('public_unexpected_license_extra',lambda p,i,d:p['metadata']['license'].update(extra='unexpected')),
        ('public_wrong_license_schema',lambda p,i,d:p['metadata'].update(license='cc-by-4.0')),('public_wrong_version',lambda p,i,d:p['metadata'].update(version='2.0')),
        ('public_changed_description',lambda p,i,d:p['metadata'].update(description='changed')),
        ('public_changed_creator',lambda p,i,d:p['metadata']['creators'][0].update(name='changed')),
        ('public_extra_file',lambda p,i,d:p['files'].append({'key':'other.pdf','size':0,'checksum':'md5:bad'})),
        ('public_duplicate_file',lambda p,i,d:p['files'].append(copy.deepcopy(p['files'][0]))),
        ('public_missing_file',lambda p,i,d:p['files'].pop()),('public_file_checksum_changed',lambda p,i,d:p['files'][0].update(checksum='md5:bad')),
        ('public_file_size_changed',lambda p,i,d:p['files'][0].update(size=1)),
        ('inspection_wrong_DOI',lambda p,i,d:i.update(doi='10.5281/zenodo.998')),
        ('inspection_unpublished',lambda p,i,d:i.update(state='ready_to_publish')),
        ('inspection_DOI404',lambda p,i,d:i['doi_resolution'].update(http_status=404)),
        ('download_pdf_changed',lambda p,i,d:d.update({'fixed-birational-cycle-nonlimit.pdf':(b'bad',200,'synthetic')})),
        ('download_zip_changed',lambda p,i,d:d.update({'fixed-birational-cycle-nonlimit-verification.zip':(b'bad',200,'synthetic')})),
        ('download_http_failure',lambda p,i,d:d.update({'fixed-birational-cycle-nonlimit.pdf':(d['fixed-birational-cycle-nonlimit.pdf'][0],404,'synthetic')}))]:
        run(label,mutation)


def test_lifecycle(work):
    root=work/'lifecycle';root.mkdir()
    merge={'merged':True,'head':'a'*40,'original_files':17,'publication_files':5,'queue_other_bytes_preserved':True,
           'all_unselected_root_unsolved_attempts_siblings_preserved':True}
    write(root/'PR_MERGE_VERIFIED.json',merge)
    gatefile=root/'gate.json';write(gatefile,{'synthetic':True})
    gate={'started_utc':B.stamp(),'receipt':str(gatefile)}
    calls=[]
    def collect(*args,**kwargs):calls.append(('gate',args));return gate,{'gate_sha256':B.sha(gatefile.read_bytes())}
    def run(args):
        check((root/('ZENODO_'+args.command.upper()+'_INTENT.json')).exists(),'intent must precede synthetic mutation')
        calls.append(('synthetic_mutation',args.command))
        return {'id':999,'state':'ready_to_publish' if args.command=='stage' else 'published'}
    def reset():
        calls.clear()
        for p in root.glob('ZENODO_*.json'):p.unlink()
    with patch.object(L,'AUDIT',root),patch.object(L,'require_release_clearance',lambda:True),\
         patch.object(L,'verify_destination',lambda:True),patch.object(L,'collect',collect),\
         patch.object(L.zenodo,'run',run):
        state={'manifest':str((L.PUBLICATION/'zenodo-deposit.json').resolve()),'environment':'production','id':999}
        with patch.object(L.zenodo,'local_state',lambda *a:(root/'state.json',None)):
            expect('lifecycle_stage_intent_before_synthetic_mutation',lambda:L.run_action('stage','a'*40),True)
            check(len([x for x in calls if x[0]=='synthetic_mutation'])==1,'one stage call')
            expect('lifecycle_stage_no_blind_retry',lambda:L.run_action('stage','a'*40))
            reset()
            expect('publish_without_saved_exact_id',lambda:L.run_action('publish','a'*40,999))
        with patch.object(L.zenodo,'local_state',lambda *a:(root/'state.json',state)):
            expect('stage_existing_draft_requires_reconciliation',lambda:L.run_action('stage','a'*40))
            expect('publish_wrong_confirm_id',lambda:L.run_action('publish','a'*40,998))
            expect('lifecycle_publish_intent_before_synthetic_mutation',lambda:L.run_action('publish','a'*40,999),True)
            expect('lifecycle_publish_no_blind_retry',lambda:L.run_action('publish','a'*40,999))
            reset()
            with patch.object(L,'collect',lambda *a,**k:(_ for _ in ()).throw(RuntimeError('synthetic new draft gate failure'))):
                expect('lifecycle_failed_gate_no_mutation',lambda:L.run_action('publish','a'*40,999))
            check(not calls,'no mutation after gate rejection')
            with patch.object(L,'verify_destination',lambda:(_ for _ in ()).throw(RuntimeError('wrong destination'))):
                expect('lifecycle_wrong_destination_no_mutation',lambda:L.run_action('publish','a'*40,999))
            check(not calls,'no mutation after destination rejection')
            changed=copy.deepcopy(merge);changed['head']='b'*40;write(root/'PR_MERGE_VERIFIED.json',changed)
            expect('lifecycle_wrong_merge_head_no_mutation',lambda:L.run_action('publish','a'*40,999))
            check(not calls,'no mutation after merge binding rejection')


def test_ledger(work):
    root=work/'ledger';root.mkdir()
    row=D.desired_row(999);base=[B.HEADERS]
    write(root/'ROOT_PREPUBLICATION_LEAD_RECONCILIATION.json',{'ledger_leads':[]})
    write(root/'ZENODO_PUBLIC_FILE_VERIFICATION.json',{'synthetic':True})
    public={'record':999,'all_public_file_bytes_match_reviewed':True,'doi_resolution':{'status':200},'release_manifest_sha256':B.RELEASE_SHA}
    append_calls=[];read_calls=[]
    def run(label,before,after,ok=False,intent=False,pubchange=None,responsechange=None,gatechange=None,expected_appends=0):
        for name in ['LEDGER_APPEND_INTENT.json','LEDGER_APPEND_RESPONSE.json','LEDGER_PUBLICATION_VERIFICATION.json']:
            if (root/name).exists():(root/name).unlink()
        if intent:write(root/'LEDGER_APPEND_INTENT.json',{'synthetic prior uncertain intent':True})
        pub=copy.deepcopy(public)
        if pubchange:pubchange(pub)
        gate={'ledger_sha256':B.digest(before),'started_utc':B.stamp(),'receipt':str(root/'gate.json')}
        if gatechange:gatechange(gate)
        reads=iter([before,after]);append_calls.clear();read_calls.clear()
        def read(*args):read_calls.append(args);return next(reads)
        def gws(action,params,body):
            check(action=='append','only synthetic append expected')
            check((root/'LEDGER_APPEND_INTENT.json').exists(),'ledger durable intent precedes mutation')
            append_calls.append(body)
            response={'updates':{'updatedRows':1,'updatedColumns':4,'updatedData':{'values':[row]}}}
            if responsechange:responsechange(response)
            return response
        with patch.object(D,'AUDIT',root),patch.object(D,'require_release_clearance',lambda:True),\
            patch.object(D,'verify_live',lambda identifier:pub),patch.object(D,'collect',lambda *a,**k:(gate,{})),\
            patch.object(D,'read',read),patch.object(D,'gws',gws):
            expect(label,lambda:D.append_verified('a'*40,999),ok)
        check(len(append_calls)==expected_appends,label+' synthetic append count')
    run('ledger_one_new_exact_append',base,base+[row],True,expected_appends=1)
    run('ledger_exact_existing_is_idempotent',base+[row],base+[row],True)
    run('ledger_exact_existing_after_uncertain_intent',base+[row],base+[row],True,intent=True)
    run('ledger_uncertain_intent_absent_row_stops',base,base,intent=True)
    changed=copy.deepcopy(row);changed[3]='changed'
    run('ledger_same_DOI_changed_row_stops',base+[changed],base+[changed])
    run('ledger_DOI_elsewhere_before_append_blocks',base+[['unrelated','','','See 10.5281/zenodo.999']],base)
    run('ledger_multiple_DOI_rows_before_append_blocks',base+[row,['unrelated','','','See 10.5281/zenodo.999']],base)
    run('ledger_duplicate_target_rows_stop',base+[row,row],base+[row,row])
    run('ledger_public_bytes_unverified_stops',base,base,pubchange=lambda p:p.update(all_public_file_bytes_match_reviewed=False))
    run('ledger_DOI_unresolved_stops',base,base,pubchange=lambda p:p['doi_resolution'].update(status=404))
    run('ledger_full_sheet_changed_since_gate_stops',base,base,gatechange=lambda g:g.update(ledger_sha256='0'*64))
    run('ledger_expired_gate_stops',base,base,gatechange=lambda g:g.update(started_utc='2000-01-01T00:00:00+00:00'))
    run('ledger_bad_response_no_retry',base,base+[row],responsechange=lambda r:r['updates'].update(updatedRows=2),expected_appends=1)
    run('ledger_bad_readback_no_retry',base,base,expected_appends=1)
    run('ledger_unrelated_row_changed_readback_stops',base+[ ['unrelated','','',''] ],base+[['changed','','',''],row],expected_appends=1)
    run('ledger_DOI_duplicate_anywhere_stops',base,base+[['unrelated','','','See 10.5281/zenodo.999'],row],expected_appends=1)


def main():
    # Prohibit every generic network/process/provider fallback globally. Individual
    # tested boundaries above replace these only with explicitly synthetic stubs.
    with ExitStack() as guards:
        guards.enter_context(patch.object(subprocess,'run',forbidden))
        guards.enter_context(patch.object(V,'urlopen',forbidden))
        for name in ['request','create','upload','update','publish','get']:
            guards.enter_context(patch.object(B.zenodo.ZenodoClient,name,forbidden))
        with tempfile.TemporaryDirectory(prefix='offline_',dir=HERE) as tmp:
            work=Path(tmp)
            test_package(work);test_accounts();test_gates(work);test_collector(work);test_integration();test_repository_mutation_adapter(work);test_public();test_lifecycle(work);test_ledger(work)
    result={'timestamp':B.stamp(),'python':sys.version,'optimization':sys.flags.optimize,
            'all_controls_passed':True,'controls':len(CASES),'accepted':sum(c['actual']=='accept' for c in CASES),
            'rejected':sum(c['actual']=='reject' for c in CASES),'actual_provider_access_attempts':len(CALLS),
            'release_manifest_sha256':B.RELEASE_SHA,'cases':CASES,
            'scope':'Actual helper functions and synthetic provider methods only; exact approved local release positive controls. No live provider/network/Git index/ref mutations.'}
    path=HERE/('OFFLINE_CONTROLS_OPTIMIZED.json' if sys.flags.optimize else 'OFFLINE_CONTROLS.json')
    write(path,result)
    print(json.dumps({k:v for k,v in result.items() if k!='cases'},indent=2))


if __name__=='__main__':
    main()
