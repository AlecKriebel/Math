"""Fresh bounded offline tests; actual administrative response fixtures only."""
import base64
from copy import deepcopy
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
from types import SimpleNamespace
from unittest.mock import patch
sys.dont_write_bytecode = True
PUBLIC = Path(__file__).resolve().parent
CASE = PUBLIC.parents[2]
PRIVATE = CASE / 'private_sources/publication_admin_helper_v3/publication_v3_software_adversary2'
SOURCE = PUBLIC.parent / 'publication_admin_v3.py'
SOURCE_SHA = '536844c63eedf31934e686d44a32c3e8564ba9aaa9c078f204ffe5488bfdea53'
ADOPTION = PUBLIC.parent / 'PROPOSED_RECOVERY_ADOPTION.json'
ADOPTION_SHA = '8edb48b705627c97e6390e05e63879924920fb2d1d590e83a61d18542f44155b'
def check(b, msg):
    if not b: raise AssertionError(msg)
check(hashlib.sha256(SOURCE.read_bytes()).hexdigest() == SOURCE_SHA, 'source changed')
check(hashlib.sha256(ADOPTION.read_bytes()).hexdigest() == ADOPTION_SHA, 'adoption changed')
sp = importlib.util.spec_from_file_location('review_v3', SOURCE)
m = importlib.util.module_from_spec(sp)
exec(compile(SOURCE.read_bytes(), str(SOURCE), 'exec'), m.__dict__)
g, v1, v2 = m.g, m.v1, m.v2
def read(p): return json.loads(p.read_bytes())
FIXTURE = [read(m.MAPPING_DIR / f'{i:04d}_response.json') for i in range(8)]
ORIGINAL = read(m.V2_STATE)
SPEC = ORIGINAL['spec']
SNAPSHOT = read(v2.ROOT_SNAPSHOT)
PROTECTED = [m.STATE, m.V2_STATE, v2.ORIGINAL_STATE, m.V2_COPY, SOURCE, ADOPTION]
INITIAL_PINS = {str(p): {'sha256':g.sha(p.read_bytes()), 'bytes':p.stat().st_size} for p in PROTECTED}
counter = 0
results = []
class Model:
    def __init__(self):
        self.data = deepcopy(FIXTURE); self.last_native = None; self.calls = []; self.rows = []
        self.target = v1.SHEET; self.gid = v1.GID; self.title = v1.TITLE; self.headers = deepcopy(v1.HEADERS)
        self.fail = None; self.append_mode = None; self.owner = None; self.durable_intent_seen = False
    def zenodo(self, method, endpoint, payload=None, file=None, **params):
        self.last_native = None
        self.calls.append(('zenodo', method, endpoint))
        check(method == 'GET', 'model Zenodo mutation reached backend')
        i = {f'/api/deposit/depositions/{m.ID}':0, f'/api/records/{m.ID}':1, f'/api/records/{m.ID}/files':2}[endpoint]
        if self.fail == 'zenodo': raise OSError('offline GET failure')
        return deepcopy(self.data[i])
    def public_json(self, ident, native=False):
        self.last_native = None
        self.calls.append(('public_json', 'GET', ident, native))
        r=deepcopy(self.data[4 if native else 3])
        self.last_native={'evidence_kind':'offline_model','fixture':'actual_administrative_response', 'body_base64':base64.b64encode(g.encoded(r)).decode()}
        return r
    def public_hash(self, ident, name):
        self.last_native = None
        self.calls.append(('public_hash', 'GET', ident, name))
        return deepcopy(self.data[5 + [f['name'] for f in SPEC['assets']].index(name)])
    def sheet(self, operation, params, payload=None):
        self.last_native = None
        self.calls.append(('sheet', operation, deepcopy(params), deepcopy(payload)))
        if operation == 'get':
            return {'spreadsheetId':self.target,'sheets':[{'properties':{'sheetId':self.gid,'title':self.title}}]}
        if operation == 'batchGet':
            rr=[]
            for r in params['ranges']:
                if r == v1.TAB+'A1:D1': values=[self.headers]
                elif r == v1.TAB+'C2:C': values=[[row[2]] for row in self.rows]
                else: values=self.rows[int(v1.canonical_range(r).split(':')[0][1:])-2:][:1]
                rr.append({'range':r,'majorDimension':'ROWS','values':deepcopy(values)})
            return {'spreadsheetId':v1.SHEET,'valueRanges':rr}
        check(operation == 'append', 'unexpected Sheet operation')
        st=read(self.owner.state_path)
        check(st['phase']=='intent_recorded' and st['append_intent'] is True and len(st['intents'])==1, 'append not durable first')
        self.durable_intent_seen=True
        if self.append_mode == 'fail_before': raise OSError('offline append unknown before effect')
        self.rows.extend(deepcopy(payload['values']))
        if self.append_mode == 'fail_after': raise OSError('offline append unknown after effect')
        row=len(self.rows)+1
        if self.append_mode == 'wrong_values': self.rows[-1][0]='offline wrong row'
        rr=v1.TAB+f'A{row}:D{row}'
        if self.append_mode == 'wrong_range': rr="'Wrong'!A2:D2"
        return {'spreadsheetId':v1.SHEET,'updates':{'spreadsheetId':v1.SHEET,'updatedRows':1,'updatedColumns':4,'updatedCells':4,'updatedRange':rr}}
def make(recover=True, backend=None):
    global counter
    counter+=1
    p=PRIVATE/f'model_{counter:03d}'
    api=backend or Model()
    e=m.Admin(api,p/'evidence',p/'STATE.json')
    api.owner=e
    if recover: e.recover(ADOPTION,ADOPTION_SHA,m.SPEC_SHA,m.NATIVE_SHA)
    return e,api
def stopped(fn):
    try: fn()
    except Exception as exc:
        check(isinstance(exc,(g.Stop,m.z.DepositError)), f'unexpected {type(exc).__name__}')
        return type(exc).__name__
    raise AssertionError('accepted adversarial input')
def run(name, fn):
    start=g.dt.datetime.now(g.dt.timezone.utc).isoformat()
    try:
        detail=fn(); results.append({'name':name,'status':'PASS','utc':start,'detail':detail})
    except Exception as exc:
        results.append({'name':name,'status':'FAIL','utc':start,'error':type(exc).__name__+': '+str(exc)})
    print(results[-1]['status'],name)
def mutate_cases(changes):
    tested=[]
    for label,change in changes:
        e,b=make(); change(b.data); stopped(lambda:e.published(SPEC,m.ID,SNAPSHOT))
        check(all(c[1] == 'GET' for c in b.calls if c[0] != 'sheet'),'mutation dispatched')
        tested.append(label)
    return tested
def setpath(data,i,path,value):
    j=data[i]
    for key in path[:-1]: j=j[key]
    j[path[-1]]=value
def mutation(i,path,value): return lambda d:setpath(d,i,path,value)
def positive():
    e,b=make(); check(len(b.calls)==8,'not eight GETs')
    check(read(e.state_path)['phase']=='published_verified' and not e.state['append_intent'],'bad recovery state')
    check(not list(e.evidence.glob('000[5-7]_native.json')),'hash inherited native body')
    check(e.kind=='offline_model','model mislabeled')
    return {'gets':8,'models':'actual eight responses','hash_native_receipts':0}
run('01_actual_known_ACK_recovery_eight_GETs',positive)
run('02_auth_requested12_exact_values',lambda:mutate_cases([('title',mutation(0,['metadata','title'],'wrong')),('notes',mutation(0,['metadata','notes'],'wrong'))]))
run('03_auth_publisher_exact',lambda:mutate_cases([('publisher',mutation(0,['metadata','imprint_publisher'],'wrong'))]))
run('04_auth_reserved_integer_types_DOI',lambda:mutate_cases([('integer required',mutation(0,['metadata','prereserve_doi','recid'],str(m.ID))),('doi',mutation(0,['doi'],'10.5281/zenodo.1'))]))
run('05_auth_exact15_keys_submitted',lambda:mutate_cases([('extra',mutation(0,['metadata','extra'],'wrong')),('submitted',mutation(0,['submitted'],1))]))
run('06_public_license_object_exact',lambda:mutate_cases([('scalar',mutation(3,['metadata','license'],'cc-by-4.0')),('extra',mutation(3,['metadata','license','extra'],True))]))
run('07_public_preprint_resource_exact',lambda:mutate_cases([('title',mutation(3,['metadata','resource_type','title'],'Wrong'))]))
run('08_public_first_relation_parent',lambda:mutate_cases([('parent',mutation(3,['metadata','relations','version',0,'parent','pid_value'],'1'))]))
run('09_public_exact13keys',lambda:mutate_cases([('publisher',mutation(3,['metadata','imprint_publisher'],'Zenodo'))]))
run('10_native_snapshot_exact_JSON_types',lambda:mutate_cases([('auth false becomes zero',mutation(1,['access','embargo','active'],0)),('public false becomes zero',mutation(4,['access','embargo','active'],0))]))
run('11_native_PID_identity',lambda:mutate_cases([('public DOI',mutation(4,['pids','doi','identifier'],'10.5281/zenodo.1')),('parent DOI',mutation(1,['parent','pids','doi','identifier'],'10.5281/zenodo.1'))]))
run('12_parent_only_empty_ACL_omissions',lambda:mutate_cases([('nonempty grants',mutation(1,['parent','access','grants'],[{}])),('public extra links',mutation(4,['parent','access','links'],[])),('other projection',mutation(4,['parent','id'],'1'))]))
run('13_auth_three_flags_public_two_flags',lambda:mutate_cases([('auth index bool',mutation(1,['versions','index'],True)),('auth latestdraft false',mutation(1,['versions','is_latest_draft'],False)),('public extra',mutation(4,['versions','is_latest_draft'],True))]))
def file_mutations():
    name=SPEC['assets'][0]['name']
    return mutate_cases([('auth hidden',mutation(1,['files','entries',name,'access','hidden'],True)),('public count',mutation(4,['files','count'],2)),('listing incomplete',mutation(2,['entries',0,'status'],'pending')),('public md5',mutation(4,['files','entries',name,'checksum'],'md5:'+'0'*32))])
run('14_three_completed_visible_files_MD5_size',file_mutations)
run('15_public_hash_SHA_MD5_size_URL_status',lambda:mutate_cases([(k,mutation(5,[k],v)) for k,v in [('sha256','0'*64),('md5','0'*32),('size',1),('http_status',404),('url','https://zenodo.org/wrong')]]))
def dispatch_base(base,service,op,params=None,payload=None,write=False):
    e,b=make(); before=len(b.calls)
    stopped(lambda:base.request(e,service,op,params,payload,write=write))
    check(len(b.calls)==before,'backend bypass reached')
    check(e._dispatch_grant is None,'grant survived')
    return {'backend_calls':0}
run('16_explicit_V1_Zenodo_POST_blocked',lambda:dispatch_base(v1.Admin,'zenodo',f'POST /api/deposit/depositions/{m.ID}/actions/publish',write=True))
run('17_explicit_V2_Zenodo_POST_blocked',lambda:dispatch_base(v2.Admin,'zenodo',f'POST /api/deposit/depositions/{m.ID}/actions/publish',write=True))
run('18_explicit_V1_V2_Sheet_wrong_unphased_blocked',lambda:[dispatch_base(x,'sheet','append',{'spreadsheetId':'wrong'}, {'values':[['wrong']]},True) for x in (v1.Admin,v2.Admin)])
def one_shot():
    e,b=make(); p={'id':m.ID,'native':False}
    e._dispatch_grant=g.encoded(['public_json','GET',p,None,None])
    e.api.public_json(m.ID,False)
    stopped(lambda:e.api.public_json(m.ID,False))
    check(e.api.last_native is None,'denial retained native')
    check(e._dispatch_grant is None,'grant replayable')
    return 'one grant consumed; replay denied before backend'
run('19_exact_transport_one_shot_grant',one_shot)
def denied_stale():
    e,b=make(); e.request('public_json','GET',{'id':m.ID,'native':False}); check(e.api.last_native is not None,'no previous native')
    i=e.count; before=len(b.calls)
    stopped(lambda:v1.Admin.request(e,'zenodo',f'POST /api/deposit/depositions/{m.ID}/actions/publish',write=True))
    check(len(b.calls)==before,'denial reached backend')
    check(not (e.evidence/f'{i:04d}_native.json').exists(),'stale HTTP decorated denied call')
    check(e.api.last_native is None,'transport stale')
    return 'failed ancestor call has error receipt and no stale native receipt'
run('20_denied_ancestor_custody_no_stale_HTTP',denied_stale)
def hash_reset():
    e,b=make(); e.request('public_json','GET',{'id':m.ID,'native':True}); i=e.count
    e.request('public_hash','GET',{'id':m.ID,'name':SPEC['assets'][0]['name']})
    check(b.last_native is None and e.api.last_native is None and not (e.evidence/f'{i:04d}_native.json').exists(),'stale hash receipt')
    return 'production-shaped public_hash reset and defensive transport reset checked'
run('21_public_hash_fresh_custody',hash_reset)
def gws_error():
    e,b=make(backend=v1.Production(),recover=False); e.kind='offline_model'
    actual_run=subprocess.run
    def offline_process(*args,**kwargs):
        return actual_run([sys.executable,'-c','import sys; print("offline fresh stdout"); print("offline fresh stderr",file=sys.stderr); sys.exit(7)'],capture_output=True)
    b.last_native={'body_base64':base64.b64encode(b'old HTTP').decode()}
    with patch.object(v1.subprocess,'run',side_effect=offline_process):
        stopped(lambda:e.request('sheet','get',{'spreadsheetId':v1.SHEET,'fields':'spreadsheetId,sheets.properties'}))
    receipt=read(e.evidence/'0000_native.json')
    check(receipt['returncode']==7 and base64.b64decode(receipt['stdout_base64'])==b'offline fresh stdout\n' and base64.b64decode(receipt['stderr_base64'])==b'offline fresh stderr\n','fresh process custody lost')
    check('body_base64' not in receipt,'old HTTP inherited')
    return 'exact Production.sheet code; actual offline process stdout/stderr retained, no real GWS'
run('22_fresh_Production_sheet_error_stdout_stderr',gws_error)
def append_positive():
    e,b=make(); r=e.tracker(m.SPEC_SHA,m.ID,m.NATIVE_SHA)
    check(r['status']=='tracker_verified' and b.durable_intent_seen,'append not verified')
    app=[c for c in b.calls if c[0]=='sheet' and c[1]=='append']; check(len(app)==1,'not one append')
    p=app[0][2]; check(p['spreadsheetId']==v1.SHEET and p['valueInputOption']=='RAW' and p['insertDataOption']=='INSERT_ROWS','append options')
    check(app[0][3]['values']==[[SPEC['tracker']['original_problem'],SPEC['tracker']['solution_chat'],'https://doi.org/'+m.DOI,SPEC['tracker']['notes']]],'four cells')
    stopped(lambda:e.tracker(m.SPEC_SHA,m.ID,m.NATIVE_SHA)); check(len([c for c in b.calls if c[0]=='sheet' and c[1]=='append'])==1,'retry')
    return 'one exact RAW INSERT_ROWS append; durable intent precedes backend; second tracker rejected'
run('23_one_exact_phased_tracker_append',append_positive)
def existing_duplicate():
    e,b=make(); row=[SPEC['tracker']['original_problem'],SPEC['tracker']['solution_chat'],'https://doi.org/'+m.DOI,SPEC['tracker']['notes']]
    b.rows=[row]; check(e.tracker(m.SPEC_SHA,m.ID,m.NATIVE_SHA)['status']=='tracker_already_exact','existing row')
    check(not any(c[0]=='sheet' and c[1]=='append' for c in b.calls),'existing appended')
    e,b=make(); b.rows=[deepcopy(row),deepcopy(row)]; stopped(lambda:e.tracker(m.SPEC_SHA,m.ID,m.NATIVE_SHA))
    check(not any(c[0]=='sheet' and c[1]=='append' for c in b.calls),'duplicate appended')
    check(v1.doi_key(' HTTP://DX.DOI.ORG/'+m.DOI.upper()+' ')==m.DOI,'DOI normalization')
    return 'exact existing dedup; duplicate stop; DOI-only normalized identity'
run('24_existing_DOI_dedup_duplicate_STOP',existing_duplicate)
def sheet_drift():
    for key,value in [('target','wrong'),('gid',0),('title','wrong'),('headers',['wrong'])]:
        e,b=make(); setattr(b,key,value); stopped(lambda:e.tracker(m.SPEC_SHA,m.ID,m.NATIVE_SHA))
        check(not any(c[0]=='sheet' and c[1]=='append' for c in b.calls),'drift appended')
    return ['spreadsheet','gid','title','four headers']
run('25_fixed_Sheet_identity_gid_title_headers',sheet_drift)
def pre_and_after_errors():
    e,b=make(); b.fail='zenodo'; stopped(lambda:e.tracker(m.SPEC_SHA,m.ID,m.NATIVE_SHA)); check(not e.state['append_intent'],'premature intent')
    for mode in ['wrong_range','wrong_values']:
        e,b=make(); b.append_mode=mode; stopped(lambda:e.tracker(m.SPEC_SHA,m.ID,m.NATIVE_SHA))
        check(read(e.state_path)['append_intent'] is True,'lost attempted flag')
        stopped(lambda:e.tracker(m.SPEC_SHA,m.ID,m.NATIVE_SHA))
        check(len([c for c in b.calls if c[0]=='sheet' and c[1]=='append'])==1,'after-error retry')
    return ['GET failure before append','wrong returned row range','wrong row values after append']
run('26_before_and_after_append_STOP_no_retry',pre_and_after_errors)
def unknown(mode):
    e,b=make(); b.append_mode=mode; stopped(lambda:e.tracker(m.SPEC_SHA,m.ID,m.NATIVE_SHA))
    st=read(e.state_path); check(st['phase']=='unknown_write' and st['append_intent'] is True,'unknown not durable')
    appendi=next(i for i in range(e.count) if (e.evidence/f'{i:04d}_intent.json').exists() and read(e.evidence/f'{i:04d}_intent.json')['intent']['operation']=='append')
    check(not (e.evidence/f'{appendi:04d}_response.json').exists(),'fabricated append receipt')
    before=len([c for c in b.calls if c[0]=='sheet' and c[1]=='append'])
    r=e.reconcile(m.SPEC_SHA,native_approval=m.NATIVE_SHA)
    check(r['read_only'] is True and ('append_response_available' not in r or r['append_response_available'] is False),'fabricated known append')
    stopped(lambda:e.tracker(m.SPEC_SHA,m.ID,m.NATIVE_SHA))
    check(len([c for c in b.calls if c[0]=='sheet' and c[1]=='append'])==before==1,'reconcile enabled retry')
    check(read(e.state_path)['phase']=='unknown_write','reconcile promoted unknown')
    return r['status']
run('27_unknown_append_before_effect_GET_only_reconcile',lambda:unknown('fail_before'))
run('28_unknown_append_after_effect_GET_only_reconcile',lambda:unknown('fail_after'))
FINAL_PINS = {str(p): {'sha256':g.sha(p.read_bytes()), 'bytes':p.stat().st_size} for p in PROTECTED}
check(INITIAL_PINS==FINAL_PINS,'protected production inputs changed')
g.durable(PRIVATE/'PROTECTED_INPUT_PINS.json',INITIAL_PINS,exclusive=True,private=True)
g.durable(PRIVATE/'TEST_RESULTS.json',{'evidence_kind':'offline_model','tests':results,'protected_unchanged':True},exclusive=True,private=True)
g.durable(PUBLIC/'TEST_SUMMARY.json',{'source_sha256':SOURCE_SHA,'adoption_sha256':ADOPTION_SHA,'tests':results,'protected_unchanged':True,'live_Zenodo_Sheet_requests':0},exclusive=True)
check(len(results)==28 and all(r['status']=='PASS' for r in results),'test failures')
print('ALL 28 PASS; protected inputs unchanged; no real Zenodo/Sheet calls')
