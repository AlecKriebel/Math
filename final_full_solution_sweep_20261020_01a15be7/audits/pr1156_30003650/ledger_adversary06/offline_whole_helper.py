#!/usr/bin/env python3
"""Independent whole-helper fault matrix; no service or subprocess operations.

Run separately under normal Python, -O, and -OO. Only fixture tree bytes are
executed. Real inputs are read and SHA-pinned before/after, never modified.
Each case gets one short-lived private tree, avoiding redundant bulk retention.
"""
import argparse
import copy
import datetime as real_dt
import hashlib
import http.client
import io
import json
import os
from pathlib import Path
import shutil
import socket
import subprocess
import sys
import tempfile
import types
import urllib.request
from urllib.parse import urlsplit

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parent
ROOT = AUDIT.parents[1]
HELPER = AUDIT / 'reconcile_external_ledger_v6.py'
PLAN = AUDIT / 'LEDGER_RECONCILIATION_PLAN.json'
DEPS = ['publication_check.py', 'sweep_io.py', 'checkpoint.py',
        'audits/pr0399_30001179/ops_binding.py',
        'audits/pr0399_30001179/prepublication_check.py',
        '../zenodo_deposit_tool/zenodo.py']
MODULES = ['sweep_io', 'checkpoint', 'zenodo', 'ops_binding',
           'publication_check', 'pr1156_account_reader_final']
SOURCE_PATHS = [HELPER, PLAN, *(ROOT / p for p in DEPS),
                ROOT/'raw/pr1156/zenodo_23350364.json',
                ROOT/'rest_inventory.json', ROOT/'raw/pr1156/ledger_live.json',
                AUDIT/'ROOT_IDENTITY_AND_SCOPE_FINDING.json']
SOURCES = {str(p): p.read_bytes() for p in SOURCE_PATHS}
PIN = lambda data: hashlib.sha256(data).hexdigest()
ORIGINAL_PINS = {p: {'bytes': len(b), 'sha256': PIN(b)} for p,b in SOURCES.items()}
PLAN_BYTES = SOURCES[str(PLAN)]
BASE_PLAN = json.loads(PLAN_BYTES)
BASE_PROVIDER = json.loads(SOURCES[str(ROOT/'raw/pr1156/zenodo_23350364.json')])
BASE_ROWS = json.loads(SOURCES[str(ROOT/'raw/pr1156/ledger_live.json')])['response']['values']
BASE_PR = next(v for v in json.loads(SOURCES[str(ROOT/'rest_inventory.json')])['pull_requests'] if v['number']==1156)
PAYLOADS = {f['name']:(ROOT/'raw/pr1156'/('payload_'+f['sha256']+'.bin')).read_bytes()
            for f in BASE_PLAN['existing_publication']['files']}
for name, data in PAYLOADS.items():
    f=next(f for f in BASE_PLAN['existing_publication']['files'] if f['name']==name)
    if len(data)!=f['size'] or PIN(data)!=f['sha256'] or 'md5:'+hashlib.md5(data).hexdigest()!=f['checksum']:
        raise RuntimeError('Original public payload mismatch')
for f in BASE_PLAN['existing_publication']['files']:
    p=ROOT/'raw/pr1156'/('payload_'+f['sha256']+'.bin')
    ORIGINAL_PINS[str(p)]={'bytes':p.stat().st_size,'sha256':PIN(PAYLOADS[f['name']])}

# This hook remains active even if a stub is accidentally bypassed.
DENIED=[]
def deny_services(event,args):
    if event in {'socket.connect','socket.getaddrinfo','subprocess.Popen','os.system','os.exec','os.posix_spawn'}:
        DENIED.append(event)
        raise RuntimeError('OFFLINE BOUNDARY DENIED: '+event)
sys.addaudithook(deny_services)

PRIVATE=HERE/'private'
PRIVATE.mkdir(mode=0o700,exist_ok=True)
os.chmod(PRIVATE,0o700)

def path_write(path,data):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_bytes(data)

def json_write(path,value):
    path_write(path,(json.dumps(value,ensure_ascii=False,indent=2)+'\n').encode())

def clean_record(identifier):
    return {'id':identifier,'metadata':{'title':'Unrelated verified fixture'},'files':[],'is_published':True}

def case_run(case):
    cfg=case.get('cfg',{})
    calls=[]
    state={'append':0,'reads':0,'pr_reads':0,'directory_fsync':0,'file_fsync':0,'exclusive_intents':0,
           'account_gets':0,'public_gets':0,'network':0,'subprocess':0,'snapshot_replacements':0}
    with tempfile.TemporaryDirectory(prefix='case-',dir=PRIVATE) as folder:
        top=Path(folder);root=top/'sweep';audit=root/'audits/pr1156_30003650'
        audit.mkdir(parents=True)
        fixture_helper=audit/HELPER.name
        path_write(fixture_helper,SOURCES[str(HELPER)])
        fixture_plan=copy.deepcopy(BASE_PLAN)
        cfg.get('adopt_fixture_plan_change',lambda v:None)(fixture_plan)
        fixture_plan_bytes=(json.dumps(fixture_plan,ensure_ascii=False,indent=2)+'\n').encode() if cfg.get('adopt_fixture_plan_change') else PLAN_BYTES
        path_write(audit/PLAN.name,fixture_plan_bytes)
        for rel in DEPS:path_write(root/rel,SOURCES[str(ROOT/rel)])
        path_write(root/'raw/pr1156/zenodo_23350364.json',SOURCES[str(ROOT/'raw/pr1156/zenodo_23350364.json')])
        json_write(root/'rest_inventory.json',{'pull_requests':[BASE_PR]})
        path_write(audit/'MOCK_REVIEW.txt',b'OFFLINE REVIEW FIXTURE ONLY\n')
        acceptance={'ready_for_existing_publication_record':True,'helper_sha256':PIN(SOURCES[str(HELPER)]),
                    'plan_sha256':PIN(fixture_plan_bytes),
                    'dependency_pins':{p:PIN(SOURCES[str(ROOT/p)]) for p in DEPS},
                    'review_pins':[{'path':'MOCK_REVIEW.txt','sha256':PIN(b'OFFLINE REVIEW FIXTURE ONLY\n')}]}
        cfg.get('edit_acceptance',lambda v:None)(acceptance)
        acceptance_path=audit/'ROOT_LEDGER_REVIEW06_ACCEPTANCE.json'
        json_write(acceptance_path,acceptance)
        acceptance_sha=PIN(acceptance_path.read_bytes())
        cfg.get('edit_plan_file',lambda p:None)(audit/PLAN.name)
        if cfg.get('edit_dependency'):
            p=root/cfg['edit_dependency'];p.write_bytes(p.read_bytes()+b'\n# changed unreviewed fixture\n')
        if cfg.get('dependency_symlink'):
            p=root/DEPS[0];backup=p.with_suffix('.source');p.rename(backup);p.symlink_to(backup)
        if cfg.get('review_changed'):path_write(audit/'MOCK_REVIEW.txt',b'changed\n')
        if cfg.get('provider_baseline_changed'):
            p=root/'raw/pr1156/zenodo_23350364.json';p.write_bytes(p.read_bytes()+b' ')
        if cfg.get('existing_intent'):json_write(audit/'LEDGER_RECONCILIATION_INTENT.json',{'unknown':True})
        rows=copy.deepcopy(BASE_ROWS)
        cfg.get('edit_rows',lambda r:None)(rows)
        record=copy.deepcopy(BASE_PROVIDER)
        cfg.get('edit_record',lambda r:None)(record)
        account=[clean_record(23408971),clean_record(90000001),clean_record(90000002)]
        cfg.get('edit_account',lambda r:None)(account)
        pr={'head':{'sha':BASE_PLAN['head']},'base':{'sha':BASE_PLAN['base']},
            'body':BASE_PR['body'],'state':'open','merged':False,'draft':True}
        cfg.get('edit_pr',lambda r:None)(pr)
        originals={'run':subprocess.run,'check_output':subprocess.check_output,
                   'HTTPSConnection':http.client.HTTPSConnection,'urlopen':urllib.request.urlopen,
                   'open':os.open,'fsync':os.fsync,'read_bytes':Path.read_bytes,
                   'datetime':real_dt.datetime,'argv':sys.argv[:],'path':sys.path[:],
                   'env_token':os.environ.get('ZENODO_TOKEN')}
        oldmodules={n:sys.modules.get(n) for n in MODULES}
        fsync_fds={}
        if cfg.get('shadow_modules'):
            shadow=top/'shadow';shadow.mkdir()
            for n in MODULES:
                path_write(shadow/(n+'.py'),b'raise RuntimeError("UNREVIEWED SOURCE SHADOW EXECUTED")\n')
                (shadow/'__pycache__').mkdir(exist_ok=True)
                path_write(shadow/'__pycache__'/(n+'.cpython-313.pyc'),b'UNREVIEWED INVALID PYC')
                sys.modules[n]=types.ModuleType(n)
            sys.path.insert(0,str(shadow))
        def fake_run(args,*a,**kw):
            args=list(args);calls.append(args[:5])
            if args[0]=='git':
                if 'get-url' not in args:raise RuntimeError('Unexpected Git command')
                out='https://github.com/AlecKriebel/Math.git\n'
            elif args[:2]==['gh','api']:
                if args[2].endswith('/pulls/1156'):
                    state['pr_reads']+=1;obj=copy.deepcopy(pr)
                    if state['pr_reads']==2:cfg.get('edit_final_pr',lambda r:None)(obj)
                    out=json.dumps(obj)
                elif args[2].endswith('/git/ref/heads/main'):out=json.dumps({'object':{'sha':'a'*40}})
                else:raise RuntimeError('Unexpected GitHub read')
            elif args[:4]==['gws','sheets','spreadsheets','get']:
                obj={'spreadsheetId':BASE_PLAN['spreadsheet_id'],
                     'sheets':[{'properties':{'sheetId':1254632077,'title':'Math Puzzles'}}]}
                cfg.get('edit_sheet_identity',lambda r:None)(obj);out=json.dumps(obj)
            elif args[:5]==['gws','sheets','spreadsheets','values','get']:
                state['reads']+=1
                if state['reads']==2:cfg.get('edit_immediate_rows',lambda r:None)(rows)
                if state['reads']>=3:cfg.get('edit_after_rows',lambda r:None)(rows)
                obj={'majorDimension':'ROWS','range':"'Math Puzzles'!A1:AQ1177",'values':copy.deepcopy(rows)}
                cfg.get('edit_read',lambda r,n:None)(obj,state['reads']);out=json.dumps(obj)
            elif args[:5]==['gws','sheets','spreadsheets','values','append']:
                state['append']+=1
                if state['exclusive_intents']!=1 or state['file_fsync']<1 or state['directory_fsync']<1:
                    raise RuntimeError('Append reached before durable exclusive intent')
                submitted=json.loads(args[args.index('--json')+1]);params=json.loads(args[args.index('--params')+1])
                if submitted!={'majorDimension':'ROWS','values':[BASE_PLAN['proposed_row']]}:raise RuntimeError('Unexpected simulated mutation body')
                if params!={'spreadsheetId':BASE_PLAN['spreadsheet_id'],'range':BASE_PLAN['range'],
                            'valueInputOption':'RAW','insertDataOption':'INSERT_ROWS','includeValuesInResponse':True}:
                    raise RuntimeError('Unexpected simulated mutation parameters')
                rows.append(copy.deepcopy(submitted['values'][0]))
                if cfg.get('lost_response'):raise RuntimeError('Simulated lost append response')
                ran="'Math Puzzles'!A"+str(len(rows))+':D'+str(len(rows))
                obj={'spreadsheetId':BASE_PLAN['spreadsheet_id'],
                     'updates':{'spreadsheetId':BASE_PLAN['spreadsheet_id'],'updatedCells':4,
                     'updatedRows':1,'updatedColumns':4,'updatedRange':ran,
                     'updatedData':{'majorDimension':'ROWS','range':ran,'values':copy.deepcopy(submitted['values'])}}}
                cfg.get('edit_response',lambda r:None)(obj);out=json.dumps(obj)
            else:raise RuntimeError('Unexpected external process boundary: '+repr(args[:5]))
            return subprocess.CompletedProcess(args,0,out if kw.get('text') else out.encode(),'' if kw.get('text') else b'')
        def fake_check_output(args,*a,**kw):
            if list(args)!=['git','branch','--show-current']:raise RuntimeError('Unexpected check_output')
            return 'main\n' if kw.get('text') else b'main\n'
        class FakeHTTP:
            def __init__(self,host,timeout=None):
                if host!='zenodo.org':raise RuntimeError('Unexpected API host')
            def putrequest(self,method,target):
                if method!='GET':raise RuntimeError('Account mutation attempted')
                self.target=target;state['account_gets']+=1
            def putheader(self,*a):pass
            def endheaders(self):pass
            def send(self,*a):raise RuntimeError('Unexpected account request payload')
            def getresponse(self):
                n=state['account_gets'];items=copy.deepcopy(account[n-1:n])
                count=len(account)
                obj={'hits':{'total':{'value':count,'relation':'eq'},'hits':items},
                     'links':{'next':('https://zenodo.org/api/user/records?page='+str(n+1)) if n<count else None}}
                cfg.get('edit_page',lambda r,n:None)(obj,n)
                blob=json.dumps(obj).encode()
                return types.SimpleNamespace(status=200,read=lambda amount:blob)
            def close(self):pass
        class FakeURLResponse:
            def __init__(self,body,status=200,url=None):self.body=body;self.status=status;self.url=url
            def __enter__(self):return self
            def __exit__(self,*a):pass
            def read(self):return self.body
        def fake_urlopen(request,*a,**kw):
            url=request.full_url;state['public_gets']+=1
            if url=='https://zenodo.org/api/records/23350364':return FakeURLResponse(json.dumps(record).encode(),url=url)
            if url=='https://doi.org/10.5281/zenodo.23350364':
                return FakeURLResponse(b'',cfg.get('doi_status',200),cfg.get('doi_url','https://zenodo.org/records/23350364'))
            for f in BASE_PROVIDER['files']:
                if url==f['links']['self']:
                    data=PAYLOADS[f['key']]
                    if cfg.get('bad_payload')==f['key']:data=data[:-1]+bytes([data[-1]^1])
                    return FakeURLResponse(data,url=url)
            raise RuntimeError('Unexpected public URL: '+url)
        def tracked_open(path,flags,*a,**kw):
            if cfg.get('intent_race') and str(path)==str(audit/'LEDGER_RECONCILIATION_INTENT.json'):
                path_write(Path(path),b'{"concurrent_operation":"offline_fixture"}\n')
            fd=originals['open'](path,flags,*a,**kw)
            if str(path)==str(audit/'LEDGER_RECONCILIATION_INTENT.json'):
                if flags & (os.O_EXCL|os.O_CREAT)!=(os.O_EXCL|os.O_CREAT):raise RuntimeError('Nonexclusive intent')
                state['exclusive_intents']+=1;fsync_fds[fd]='file'
            elif str(path)==str(audit):fsync_fds[fd]='directory'
            return fd
        def tracked_fsync(fd):
            kind=fsync_fds.get(fd)
            if kind:
                state[kind+'_fsync']+=1
                if cfg.get('fsync_error')==kind:raise OSError('Simulated '+kind+' fsync failure')
            return originals['fsync'](fd)
        replacements=set()
        def tracked_read_bytes(path):
            data=originals['read_bytes'](path)
            if cfg.get('replace_snapshots_after_read'):
                candidates=[audit/PLAN.name,*[root/p for p in DEPS]]
                if path in candidates and path not in replacements:
                    replacements.add(path);state['snapshot_replacements']+=1
                    path.write_bytes(b'raise RuntimeError("UNREVIEWED SNAPSHOT REOPENED")\n')
            return data
        class SimulatedClock(real_dt.datetime):
            count=0
            base=originals['datetime'].now(real_dt.timezone.utc)
            @classmethod
            def now(cls,tz=None):
                cls.count+=1
                if 'exact_age' in cfg:
                    return cls.base+real_dt.timedelta(seconds=cfg['exact_age'] if cls.count>=3 else 0)
                value=originals['datetime'].now(tz)
                if cfg.get('expired') and cls.count>=3:return value+real_dt.timedelta(seconds=181)
                if cfg.get('future_clock') and cls.count>=3:return value-real_dt.timedelta(seconds=1)
                return value
        subprocess.run=fake_run;subprocess.check_output=fake_check_output
        http.client.HTTPSConnection=FakeHTTP;urllib.request.urlopen=fake_urlopen
        os.open=tracked_open;os.fsync=tracked_fsync;Path.read_bytes=tracked_read_bytes
        if cfg.get('expired') or cfg.get('future_clock') or 'exact_age' in cfg:real_dt.datetime=SimulatedClock
        os.environ['ZENODO_TOKEN']='OFFLINE_FIXTURE_NOT_A_TOKEN'
        sys.argv=[str(fixture_helper),'--acceptance-sha256',cfg.get('acceptance_argument',acceptance_sha)]
        ns={'__file__':str(fixture_helper),'__name__':'__main__'}
        error=None;receipt=None;recovery=None
        try:
            capture=io.StringIO()
            prior_stdout=sys.stdout
            try:
                sys.stdout=capture;exec(compile(SOURCES[str(HELPER)],str(fixture_helper),'exec'),ns)
                receipt=json.loads(capture.getvalue())
            finally:sys.stdout=prior_stdout
        except BaseException as exc:error=type(exc).__name__+': '+str(exc)
        finally:
            subprocess.run=originals['run'];subprocess.check_output=originals['check_output']
            http.client.HTTPSConnection=originals['HTTPSConnection'];urllib.request.urlopen=originals['urlopen']
            os.open=originals['open'];os.fsync=originals['fsync'];Path.read_bytes=originals['read_bytes']
            real_dt.datetime=originals['datetime'];sys.argv=originals['argv'];sys.path[:]=originals['path']
            if originals['env_token'] is None:os.environ.pop('ZENODO_TOKEN',None)
            else:os.environ['ZENODO_TOKEN']=originals['env_token']
            for n,m in oldmodules.items():
                if m is None:sys.modules.pop(n,None)
                else:sys.modules[n]=m
        intent_exists=(audit/'LEDGER_RECONCILIATION_INTENT.json').exists()
        if cfg.get('lost_response'):
            # Both safe recovery routes are checked in separate fresh invocations:
            # exact existing row is adopted; absent row plus prior intent blocks.
            recovery={'intent_retained':intent_exists,'simulated_row_present':rows[-1]==BASE_PLAN['proposed_row']}
        want=case['expect']
        okay=((error is None) if want=='pass' else (error is not None)) and state['append']==case.get('appends',0)
        if receipt is not None:
            okay=okay and receipt['read_back_exact'] is True and receipt['values']==BASE_PLAN['proposed_row']
        if cfg.get('replace_snapshots_after_read'):okay=okay and state['snapshot_replacements']==7
        if cfg.get('lost_response'):okay=okay and recovery['intent_retained'] and recovery['simulated_row_present']
        return {'case':case['name'],'expected':want,'passed':okay,'error':error,'state':state,
                'intent_retained':intent_exists,'receipt_saved':receipt is not None,
                'recovery':recovery,'simulated_ledger_rows':len(rows),'boundary_calls':len(calls)}

def mutate(key,value):return lambda obj:obj.__setitem__(key,value)
def nested(*path,value):
    def apply(obj):
        for k in path[:-1]:obj=obj[k]
        obj[path[-1]]=value
    return apply

def cases():
    out=[]
    def add(name,cfg=None,expect='reject',appends=0):out.append({'name':name,'cfg':cfg or {},'expect':expect,'appends':appends})
    add('clean_full_append',expect='pass',appends=1)
    add('exact_existing_row_idempotent',{'edit_rows':lambda r:r.append(copy.deepcopy(BASE_PLAN['proposed_row']))},'pass')
    add('lost_response_no_automatic_retry',{'lost_response':True},appends=1)
    add('retry_unknown_outcome_absent_row_blocks',{'existing_intent':True})
    add('concurrent_intent_creation_O_EXCL_race',{'intent_race':True})
    add('retry_known_exact_row_with_intent_is_idempotent',{'existing_intent':True,'edit_rows':lambda r:r.append(copy.deepcopy(BASE_PLAN['proposed_row']))},'pass')
    add('acceptance_bad_external_sha',{'acceptance_argument':'0'*64})
    add('acceptance_malformed_external_sha',{'acceptance_argument':'not-a-sha'})
    add('acceptance_not_ready',{'edit_acceptance':mutate('ready_for_existing_publication_record',False)})
    add('acceptance_wrong_helper',{'edit_acceptance':mutate('helper_sha256','0'*64)})
    add('acceptance_wrong_plan',{'edit_acceptance':mutate('plan_sha256','0'*64)})
    add('acceptance_missing_dependency',{'edit_acceptance':lambda r:r['dependency_pins'].pop(DEPS[0])})
    add('acceptance_extra_dependency',{'edit_acceptance':lambda r:r['dependency_pins'].__setitem__('other.py','0'*64)})
    add('review_bytes_changed',{'review_changed':True})
    for dep in DEPS:add('dependency_bytes_changed_'+dep,{'edit_dependency':dep})
    add('dependency_leaf_symlink',{'dependency_symlink':True})
    add('source_shadow_and_pyc_ignored',{'shadow_modules':True},'pass',1)
    add('all_dependency_and_plan_snapshots_remain_authoritative',{'replace_snapshots_after_read':True},'pass',1)
    for k,v in [('spreadsheet_id','wrong'),('sheet_gid',1),('range',"'Wrong'!A:D")]:
        add('plan_destination_'+k,{'edit_plan_file':lambda p,k=k,v=v:json_write(p,{**BASE_PLAN,k:v})})
    add('provider_baseline_bytes_changed',{'provider_baseline_changed':True})
    for k,v in [('state','draft'),('submitted',False),('doi','10.5281/zenodo.999'),('id',23350365),('conceptrecid','23350365')]:
        add('provider_changed_'+k,{'edit_record':mutate(k,v)})
    add('provider_metadata_changed',{'edit_record':lambda r:r['metadata'].__setitem__('title','Changed')})
    add('provider_duplicate_file',{'edit_record':lambda r:r['files'].append(copy.deepcopy(r['files'][0]))})
    add('provider_missing_file',{'edit_record':lambda r:r['files'].pop()})
    add('provider_checksum_changed',{'edit_record':lambda r:r['files'][0].__setitem__('checksum','md5:'+'0'*32)})
    for f in BASE_PLAN['existing_publication']['files']:add('provider_payload_changed_'+f['name'],{'bad_payload':f['name']})
    for url in ['http://zenodo.org/records/23350364','https://zenodo.org/records/23350363','https://example.org/records/23350364','https://zenodo.org/records/233503640','https://zenodo.org/records/23350364?x=1']:
        add('doi_wrong_destination_'+url,{'doi_url':url})
    add('doi_wrong_status',{'doi_status':404})
    for name,change in [('head',nested('head','sha',value='0'*40)),('base',nested('base','sha',value='0'*40)),('body',mutate('body','changed'))]:
        add('initial_pr_changed_'+name,{'edit_pr':change})
    for name,change in [('head',nested('head','sha',value='0'*40)),('base',nested('base','sha',value='0'*40)),('body',mutate('body','changed')),('state',mutate('state','closed')),('merged',mutate('merged',True)),('draft',mutate('draft',False))]:
        add('final_pr_changed_'+name,{'edit_final_pr':change})
    add('expired_observations_181_seconds',{'expired':True})
    add('clock_moves_before_start',{'future_clock':True})
    add('freshness_exact_180_seconds',{'exact_age':180},'pass',1)
    add('freshness_exact_zero_seconds',{'exact_age':0},'pass',1)
    add('freshness_180_point_001_seconds',{'exact_age':180.001})
    add('freshness_negative_point_001_seconds',{'exact_age':-0.001})
    add('owned_positive_control_missing',{'edit_account':lambda r:r.pop(0)})
    for field,value in [('id',23350364),('parent',{'id':'23350363'}),('pids',{'doi':{'identifier':'10.5281/zenodo.23350364'}}),('conceptdoi','10.5281/zenodo.23350363'),('arbitrary_raw_field','https://zenodo.org/records/23350364/files/archive.zip')]:
        add('account_raw_'+field,{'edit_account':lambda r,f=field,v=value:r[1].__setitem__(f,v)})
    for value in ['CP-plus rank theorem','OWR-15957-003','Dickinson separate maximal rank problem','positive-factor-rank','PR #1156','https://github.com/AlecKriebel/Math/pull/1156']:
        add('account_semantic_'+value,{'edit_account':lambda r,v=value:r[1]['metadata'].__setitem__('description',v)})
    aliases=['10.5281%2Fzenodo.23350364','https://zenodo.org/records/00023350363/files/x','https://zenodo.org/api/records/23350364/draft',
             'https://doi.org/10.5281%252Fzenodo.23350364','https://shortdoi.org/abc','https://zenodo.org/records/%ZZ',
             'https://zenodo.org:8443/records/23350364','https://zenodo.org@foreign.invalid/records/23350364']
    full_encoded=''.join('%'+format(c,'02x') for c in b'10.5281/zenodo.23350364')
    concept_encoded=''.join('%'+format(c,'02x') for c in b'https://zenodo.org/records/23350363')
    deep_encoded=full_encoded
    for _ in range(10):deep_encoded=deep_encoded.replace('%','%25')
    aliases.extend([full_encoded,concept_encoded,deep_encoded])
    for value in aliases:add('account_alias_'+value,{'edit_account':lambda r,v=value:r[1]['metadata'].__setitem__('related_identifier',v)})
    add('account_draft_lead',{'edit_account':lambda r:(r[1].__setitem__('is_published',False),r[1]['metadata'].__setitem__('description',full_encoded))})
    add('account_unrelated_draft_in_full_inventory',{'edit_account':lambda r:r[1].__setitem__('is_published',False)},'pass',1)
    for f in BASE_PLAN['existing_publication']['files']:
        for checksum in [f['checksum'],f['checksum'].upper(),f['checksum'][4:]]:
            add('account_known_md5_'+checksum,{'edit_account':lambda r,c=checksum:r[1]['files'].append({'checksum':c})})
    page_faults=[('inexact_total',lambda r,n:r['hits'].__setitem__('total',{'value':3,'relation':'gte'})),
                 ('changing_total',lambda r,n:r['hits'].__setitem__('total',3 if n==1 else 4)),
                 ('missing_page',lambda r,n:r['links'].__setitem__('next',None)),
                 ('loop',lambda r,n:r['links'].__setitem__('next','https://zenodo.org/api/user/records?page=2')),
                 ('foreign_page',lambda r,n:r['links'].__setitem__('next','https://example.org/api/user/records?page=2')),
                 ('duplicate_id',lambda r,n:r['hits']['hits'][0].__setitem__('id',23408971)),
                 ('malformed_files',lambda r,n:r['hits']['hits'][0].__setitem__('files',{}))]
    for name,fn in page_faults:add('account_pagination_'+name,{'edit_page':fn})
    for column in range(4):
        for alias in ['https://doi.org/10.5281/zenodo.23350364','https://zenodo.org/records/23350363','https://shortdoi.org/abc',full_encoded,concept_encoded,deep_encoded]:
            add('ledger_column_'+str(column)+'_'+alias,{'edit_rows':lambda r,c=column,v=alias:r.append(['' if i!=c else v for i in range(4)])})
    add('ledger_later_ambiguous_alias_not_shortcircuited',{'edit_rows':lambda r:r.append(['https://doi.org/10.5281/zenodo.23350364','','','https://shortdoi.org/abc'])})
    add('ledger_duplicate_exact_rows',{'edit_rows':lambda r:r.extend([copy.deepcopy(BASE_PLAN['proposed_row']),copy.deepcopy(BASE_PLAN['proposed_row'])])})
    add('ledger_wrong_notes_existing_identity',{'edit_rows':lambda r:r.append([*BASE_PLAN['proposed_row'][:3],'Wrong attribution'])})
    for field,value in [('spreadsheetId','wrong')]:add('sheet_identity_'+field,{'edit_sheet_identity':mutate(field,value)})
    add('sheet_gid_changed',{'edit_sheet_identity':nested('sheets',0,'properties','sheetId',value=2)})
    add('sheet_title_changed',{'edit_sheet_identity':nested('sheets',0,'properties','title',value='Other')})
    add('schema_header_changed',{'edit_rows':lambda r:r[0].__setitem__(3,'Other')})
    add('schema_fifth_header',{'edit_rows':lambda r:r[0].append('Extra')})
    add('schema_fifth_data_cell',{'edit_rows':lambda r:r[1].append('Extra')})
    add('schema_nonstr_cell',{'edit_rows':lambda r:r[1].__setitem__(0,123)})
    add('schema_wrong_major_dimension',{'edit_read':lambda r,n:r.__setitem__('majorDimension','COLUMNS')})
    add('schema_wrong_range',{'edit_read':lambda r,n:r.__setitem__('range',"'Other'!A1:AQ1177")})
    add('immediate_prefix_changed',{'edit_immediate_rows':lambda r:r[1].__setitem__(0,'Changed')})
    add('immediate_extra_row',{'edit_immediate_rows':lambda r:r.append(['unrelated','','',''])})
    for kind in ['file','directory']:add('intent_'+kind+'_fsync_failure',{'fsync_error':kind})
    response_faults=[('outer_spreadsheet',mutate('spreadsheetId','wrong')),
                     ('inner_spreadsheet',nested('updates','spreadsheetId',value='wrong')),
                     ('four_cells',nested('updates','updatedCells',value=5)),
                     ('rows',nested('updates','updatedRows',value=2)),
                     ('columns',nested('updates','updatedColumns',value=5)),
                     ('major_dimension',nested('updates','updatedData','majorDimension',value='COLUMNS')),
                     ('data_range',nested('updates','updatedData','range',value="'Math Puzzles'!A2:D2")),
                     ('updated_range',nested('updates','updatedRange',value="'Other'!A182:D182")),
                     ('changed_values',nested('updates','updatedData','values',value=[['wrong','','','']])),
                     ('same_other_row',lambda r:(r['updates'].__setitem__('updatedRange',"'Math Puzzles'!A1:D1"),r['updates']['updatedData'].__setitem__('range',"'Math Puzzles'!A1:D1")))]
    for name,fn in response_faults:add('append_response_'+name,{'edit_response':fn},appends=1)
    add('after_prefix_changed',{'edit_after_rows':lambda r:r[1].__setitem__(0,'Changed')},appends=1)
    add('after_extra_row',{'edit_after_rows':lambda r:r.append(['unrelated','','',''])},appends=1)
    add('after_duplicate_target',{'edit_after_rows':lambda r:r.append(copy.deepcopy(BASE_PLAN['proposed_row']))},appends=1)
    add('after_row_changed',{'edit_after_rows':lambda r:r[-1].__setitem__(3,'Wrong attribution')},appends=1)
    add('after_missing_row',{'edit_after_rows':lambda r:r.pop()},appends=1)
    # Exercise plan guards beyond the immutable-plan hash gate, using accepted
    # altered fixture plans (not an adoption or change to the real plan).
    for field,value in [('spreadsheet_id','wrong'),('sheet_gid',1),('range',"'Other'!A:D"),('pr',1157),('problem_ids',['30003651'])]:
        add('independent_adopted_plan_'+field,{'adopt_fixture_plan_change':mutate(field,value)})
    for column,value in [(1,'unexpected chat'),(2,'https://doi.org/10.5281/zenodo.23350363'),(3,'Wrong credit')]:
        add('independent_adopted_plan_row_'+str(column),{'adopt_fixture_plan_change':lambda p,c=column,v=value:p['proposed_row'].__setitem__(c,v)})
    # Fresh independent additions after full v5 first inspection. Resolver
    # trailing-dot authorities are conservative unresolved leads, not asserted
    # identity, redirect outcomes, or actual duplicates.
    for alias in ['//shortdoi.org/abc','//doi.org/abc','shortdoi.org/abc','doi.org/abc',
                  '//www.shortdoi.org/abc','ftp://dx.doi.org/abc','doi.org:443/abc',
                  'https://doi.org./abc','//shortdoi.org./abc','doi.org./abc',
                  'https://www.shortdoi.org./abc','//dx.doi.org.:443/abc']:
        for column in range(4):
            add('independent_resolver_column_'+str(column)+'_'+alias,
                {'edit_rows':lambda r,c=column,v=alias:r.append(['' if i!=c else v for i in range(4)])})
        add('independent_resolver_account_'+alias,
            {'edit_account':lambda r,v=alias:r[1]['metadata'].__setitem__('related_identifier',v)})
    for alias in ['doi.org','//doi.org/','https://dx.doi.org/','https://doi.org/10.4171/OWR/2017/10',
                  'https://example.org/notdoi.org/abc','https://doi.org.evil.invalid/abc']:
        add('independent_nonlead_control_'+alias,
            {'edit_rows':lambda r,v=alias:r.append([v,'','',''])},'pass',1)
    for alias in ['https%3A%2F%2Fshortdoi.org%2Fabc','%2F%2Fdoi.org%2Fabc',
                  '%2F%2Fshortdoi.org.%2Fabc']:
        add('independent_encoded_resolver_'+alias,
            {'edit_rows':lambda r,v=alias:r.append(['','','',v])})
    add('independent_no_shortcircuit_earlier_semantic_match_later_alias',
        {'edit_rows':lambda r:r.append(['PR #1156','','','//doi.org/abc'])})
    add('independent_two_owned_leads_across_pages',
        {'edit_account':lambda r:(r[1].__setitem__('pids',{'doi':{'identifier':'10.5281/zenodo.23350363'}}),r[2]['metadata'].__setitem__('related_identifier','//doi.org/abc'))})
    add('independent_pagination_negative_id',{'edit_page':lambda r,n:r['hits']['hits'][0].__setitem__('id',-1)})
    add('independent_pagination_boolean_total',{'edit_page':lambda r,n:r['hits'].__setitem__('total',True)})
    add('independent_nonrectangular_append_range',{'edit_response':lambda r:(r['updates'].__setitem__('updatedRange',"'Math Puzzles'!A181:D182"),r['updates']['updatedData'].__setitem__('range',"'Math Puzzles'!A181:D182"))},appends=1)

    # Fresh independent v6 boundary controls. No inference of DNS resolution
    # or URI equivalence is used to classify these conservative review leads.
    extra_aliases=[
        'doi.org../abc','//shortdoi.org.../abc',
        'HTTPS://WWW.SHORTDOI.ORG....:443/abc',
        'x+custom://DX.DOI.ORG..:00443/abc',
        'https:doi.org./abc','http:\\\\doi.org.\\abc',
        'doi.org.%2e%2E/abc',
        '//shortdoi%2eorg%2e%2e/abc',
        'https://%64%6f%69%2e%6f%72%67%2e/abc',
        'doi.org.:443/abc?x=1#fragment',
        '<doi.org.../abc>','[//shortdoi.org.../abc]',
        'doi.org.../abc).','doi.org.../@alias',
        'doi.org.../10.1234/','doi.org.../10.123/abc',
        'doi.org...:bad/abc','doi.org...\\abc',
        'shortdoi.org.../10.4171/OWR/2017/10',
        'doi.org'+'.'*64+'/abc',
    ]
    for alias in extra_aliases:
        for col in range(4):
            add('v6_own_resolver_col_'+str(col)+'_'+alias,
                {'edit_rows':lambda r,c=col,v=alias:r.append(['' if i!=c else v for i in range(4)])})
        add('v6_own_resolver_account_'+alias,
            {'edit_account':lambda r,v=alias:r[1].__setitem__('untyped_metadata_lead',v)})
    for alias in ['//doi.org../abc','https://WWW.SHORTDOI.ORG...:443/abc']:
        for depth in [1,2,7,8,9]:
            encoded=alias
            for _ in range(depth):
                encoded=encoded.replace('%','%25').replace('/','%2F').replace('.','%2E').replace(':','%3A')
            add('v6_own_nested_encoding_'+str(depth)+'_'+alias,
                {'edit_rows':lambda r,v=encoded:r.append(['','','',v])})
    for alias in [
        'doi.org.','//doi.org.../','https://www.doi.org../',
        'https://shortdoi.org.','https://www.shortdoi.org.../',
        'https://doi.org.../10.4171/OWR/2017/10',
        'custom://www.dx.doi.org...:443/10.4171/OWR/2017/10',
        'https://notdoi.org./abc','https://myshortdoi.org./abc',
        'https://doi.org.evil.invalid./abc','https://shortdoi.org.evil.invalid./abc',
        'sub.doi.org./abc','sub.shortdoi.org./abc',
    ]:
        add('v6_own_nonlead_boundary_'+alias,
            {'edit_rows':lambda r,v=alias:r.append([v,'','',''])},'pass',1)
    for field,value in [
        ('parent',{'id':'23350365'}),
        ('conceptdoi','10.5281/zenodo.23350365'),
        ('metadata',{'relations':{'version':[{'parent':{'pid_type':'recid','pid_value':'23350365'}}]}}),
    ]:
        add('v6_own_provider_contradictory_family_'+field,
            {'edit_record':mutate(field,value)})
    add('v6_own_ledger_late_ambiguous_after_exact_row',
        {'edit_rows':lambda r:r.extend([copy.deepcopy(BASE_PLAN['proposed_row']),['unrelated','','','doi.org.../abc']])})
    add('v6_own_account_third_page_dot_alias_draft',
        {'edit_account':lambda r:(r[2].__setitem__('is_published',False),r[2].__setitem__('links',{'resolve':'//shortdoi.org../abc'}))})
    add('v6_own_pagination_https_userinfo_host_rejected',
        {'edit_page':lambda r,n:r['links'].__setitem__('next','https://zenodo.org@foreign.invalid/api/user/records?page=2')})
    add('v6_own_pagination_total_string_rejected',
        {'edit_page':lambda r,n:r['hits'].__setitem__('total','3')})
    add('v6_own_pagination_id_boolean_rejected',
        {'edit_page':lambda r,n:r['hits']['hits'][0].__setitem__('id',True)})
    add('v6_own_postappend_alias_added',
        {'edit_after_rows':lambda r:r.append(['','','','doi.org../abc'])},appends=1)
    add('v6_own_postappend_range_column_offbyone',
        {'edit_response':lambda r:(r['updates'].__setitem__('updatedRange',"'Math Puzzles'!B182:E182"),r['updates']['updatedData'].__setitem__('range',"'Math Puzzles'!B182:E182"))},appends=1)
    return out

def main():
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);args=p.parse_args()
    results=[case_run(c) for c in cases()]
    after={p:{'bytes':len(Path(p).read_bytes()),'sha256':PIN(Path(p).read_bytes())} for p in ORIGINAL_PINS}
    unchanged=after==ORIGINAL_PINS
    receipt={'schema':1,'mode':sys.flags.optimize,'helper_sha256':PIN(SOURCES[str(HELPER)]),
             'plan_sha256':PIN(PLAN_BYTES),'case_count':len(results),'all_cases_passed':all(r['passed'] for r in results),
             'originals_unchanged':unchanged,'original_pins':ORIGINAL_PINS,'denied_real_service_attempts':DENIED,
             'offline_only':True,'retained_case_fixture_trees':0,'main_entry_executed':True,'source_method':'adapted ledger_adversary05 harness only after independent first full v6 inspection; fresh v6 boundary controls appended','results':results}
    json_write(HERE/args.output,receipt)
    print(json.dumps({'mode':sys.flags.optimize,'cases':len(results),'passed':sum(r['passed'] for r in results),
                      'originals_unchanged':unchanged,'real_service_attempts':len(DENIED),
                      'failures':[r for r in results if not r['passed']]},indent=2))
    return 0 if receipt['all_cases_passed'] and unchanged and not DENIED else 1

if __name__=='__main__':raise SystemExit(main())
