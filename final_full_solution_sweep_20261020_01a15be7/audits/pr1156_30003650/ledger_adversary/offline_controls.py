#!/usr/bin/env python3
"""Offline copies only: all service commands are replaced before calling main."""
import sys
sys.dont_write_bytecode = True
import contextlib, copy, hashlib, importlib.util, io, json, re, types
from pathlib import Path

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parent
ROOT = AUDIT.parents[1]
PLAN_BYTES = (AUDIT/'LEDGER_RECONCILIATION_PLAN.json').read_bytes()
HELPER_BYTES = (AUDIT/'reconcile_external_ledger.py').read_bytes()
PLAN = json.loads(PLAN_BYTES)
BASE_BYTES = (ROOT/'raw/pr1156/zenodo_23350364.json').read_bytes()
BASE = json.loads(BASE_BYTES)
INVENTORY = next(p for p in json.loads((ROOT/'rest_inventory.json').read_text())['pull_requests'] if p['number']==1156)
PAYLOADS = {f['name']:(ROOT/'raw/pr1156'/('payload_'+f['sha256']+'.bin')).read_bytes() for f in PLAN['existing_publication']['files']}
sys.path.insert(0,str(ROOT))
REAL_SPEC = importlib.util.spec_from_file_location
RESULTS=[]

class Loader:
    def __init__(self, account): self.account=account
    def create_module(self,spec):return None
    def exec_module(self,module):
        module.verify_destination=lambda:None
        module.zenodo=types.SimpleNamespace(ZenodoClient=lambda *a:None,token_for=lambda *a:'OFFLINE_NOT_A_CREDENTIAL')
        module.account_search=lambda *a:copy.deepcopy(self.account)


def scenario(name, alter=None, expected='pass', retry=False):
    base=HERE/'private'/'fixtures'/name
    audit=base/'audits/pr1156_30003650'
    audit.mkdir(parents=True,exist_ok=False)
    (audit/'private').mkdir()
    (base/'raw/pr1156').mkdir(parents=True)
    (audit/'LEDGER_RECONCILIATION_PLAN.json').write_bytes(PLAN_BYTES)
    source=audit/'reconcile_external_ledger.py';source.write_bytes(HELPER_BYTES)
    (base/'raw/pr1156/zenodo_23350364.json').write_bytes(BASE_BYTES)
    (base/'rest_inventory.json').write_text(json.dumps({'pull_requests':[INVENTORY]}))
    (audit/'ROOT_LEDGER_REVIEW_ACCEPTANCE.json').write_text(json.dumps({'ready_for_existing_publication_record':True,'helper_sha256':hashlib.sha256(HELPER_BYTES).hexdigest(),'plan_sha256':hashlib.sha256(PLAN_BYTES).hexdigest(),'review_pins':[]}))
    spec=REAL_SPEC('offline_'+name,source)
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    row=copy.deepcopy(PLAN['proposed_row'])
    state={'rows':[PLAN['schema_columns'],['independent unrelated result','','10.5281/zenodo.1','unrelated']], 'append_calls':0,'get_calls':0,'pr_calls':0,'account':{'records':[],'total':0,'pages':1},'row':row,'pr':{'head':{'sha':PLAN['head']},'base':{'sha':PLAN['base']},'body':INVENTORY['body'],'state':'open','merged':False,'draft':True}}
    if alter:alter(state,audit)
    def fake_get(url):
        if url=='https://zenodo.org/api/records/23350364':return json.dumps(BASE).encode(),{'status':200,'final_url':url}
        if url==row[2]:return b'',{'status':200,'final_url':'https://zenodo.org/records/23350364'}
        for f in BASE['files']:
            if url==f['links']['self']:return PAYLOADS[f['key']],{'status':200,'final_url':url}
        raise RuntimeError('Unmocked network URL')
    def fake_cli(args):
        if args[0]=='gh':
            if args[-1].endswith('pulls/1156'):
                state['pr_calls']+=1
                p=copy.deepcopy(state['pr'])
                if state.get('change_pr') and state['pr_calls']>1:p['head']['sha']='f'*40
                return p
            return {'object':{'sha':'a'*40}}
        if args[:5]==['gws','sheets','spreadsheets','values','get']:
            state['get_calls']+=1
            if state.get('concurrent') and state['get_calls']==2:state['rows'].append(['concurrent unrelated','','',''])
            return {'values':copy.deepcopy(state['rows'])}
        if args[:5]==['gws','sheets','spreadsheets','values','append']:
            state['append_calls']+=1
            if state.get('unknown_before_commit'):raise RuntimeError('OFFLINE unknown append outcome')
            state['rows'].append(copy.deepcopy(row))
            if state.get('unknown_after_commit'):raise RuntimeError('OFFLINE response lost after commit')
            return {'updates':{'updatedRows':1,'updatedColumns':4,'updatedData':{'values':[copy.deepcopy(row)]}}}
        raise RuntimeError('Unmocked command; never execute')
    loader=Loader(state['account'])
    m.importlib=types.SimpleNamespace(util=types.SimpleNamespace(spec_from_file_location=lambda *a:importlib.util.spec_from_loader('offline_reader',loader),module_from_spec=importlib.util.module_from_spec))
    m.subprocess=types.SimpleNamespace(check_output=lambda *a,**kw:'main\n')
    m.cli=fake_cli;m.get=fake_get
    verdict=[]
    for attempt in range(2 if retry else 1):
        try:
            with contextlib.redirect_stdout(io.StringIO()):m.main()
            verdict.append({'status':'accepted'})
        except Exception as error:verdict.append({'status':'blocked','reason':str(error)})
    observed=verdict[-1]['status']
    expected_status='accepted' if expected=='pass' else 'blocked'
    RESULTS.append({'name':name,'expected':expected_status,'observed':observed,'expectation_met':observed==expected_status,'append_calls':state['append_calls'],'attempts':verdict,'scope':'Exact helper copy, mocked services; no real mutation'})

scenario('nominal')
scenario('exact_already_present',lambda s,a:s['rows'].append(copy.deepcopy(s['row'])))
scenario('existing_mismatch',lambda s,a:s['rows'].append([s['row'][0],'',s['row'][2],'different note']),expected='block')
scenario('duplicate_exact',lambda s,a:s['rows'].extend([copy.deepcopy(s['row']),copy.deepcopy(s['row'])]),expected='block')
scenario('prior_intent_absent_row',lambda s,a:(a/'LEDGER_RECONCILIATION_INTENT.json').write_text('{}'),expected='block')
scenario('concurrent_change',lambda s,a:s.update(concurrent=True),expected='block')
scenario('pr_change_before_append',lambda s,a:s.update(change_pr=True),expected='block')
scenario('account_alias_lead',lambda s,a:s.update(account={'records':[{'id':10,'metadata':{'description':'OWR-15957-003'},'files':[]}],'total':1,'pages':1}),expected='block')
scenario('unknown_before_commit',lambda s,a:s.update(unknown_before_commit=True),expected='block',retry=True)
scenario('unknown_after_commit',lambda s,a:s.update(unknown_after_commit=True),retry=True)
scenario('concept_doi_existing',lambda s,a:s['rows'].append(['','','https://doi.org/10.5281/zenodo.23350363','Existing external theorem']),expected='block')
scenario('encoded_doi_existing',lambda s,a:s['rows'].append(['','','https://doi.org/10.5281/zenodo.%32%33%33%35%30%33%36%34','Existing external theorem']),expected='block')
scenario('wide_schema_row',lambda s,a:s['rows'].append(['unrelated','','','','unexpected fifth cell']),expected='block')
scenario('account_content_hash_lead',lambda s,a:s.update(account={'records':[{'id':10,'metadata':{'title':'Untitled draft'},'files':[{'key':'source.zip','checksum':PLAN['existing_publication']['files'][2]['checksum']}]}],'total':1,'pages':1}),expected='block')
(HERE/'OFFLINE_CONTROL_RESULTS.json').write_text(json.dumps({'helper_sha256':hashlib.sha256(HELPER_BYTES).hexdigest(),'controls':RESULTS},indent=2)+'\n')
print(json.dumps(RESULTS,indent=2))
