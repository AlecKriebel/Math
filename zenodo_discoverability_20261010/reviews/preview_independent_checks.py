"""Independent offline adversarial preview checks. No network/client credentials.

Fixture metadata/identity/files are exact saved public baselines. This script uses
only fake clients and a temporary effort-local directory for receipt writes.
"""
import copy
import hashlib
import importlib
import json
import sys
import tempfile
from pathlib import Path
from urllib.parse import urlsplit
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT.parent/'zenodo_deposit_tool'))
import preview_preservation as pp
import native_metadata as nm
import apply_reviewed as ar
import repair_owned_preview as rp
import zenodo
import metadata_updates as legacy
from baseline import PacedClient

RESULTS=[]
def save(p,v): p.write_text(json.dumps(v,indent=2)+'\n')
def check(name, fn):
    try: fn(); RESULTS.append({'name':name,'pass':True})
    except Exception as e: RESULTS.append({'name':name,'pass':False,'error':type(e).__name__+': '+str(e)})
def assert_true(v, msg='assertion failed'):
    if not v: raise AssertionError(msg)
def reject(fn, client=None):
    try: fn()
    except (RuntimeError,zenodo.DepositError,KeyError,ValueError,StopIteration):
        if client is not None: assert_true(len(client.puts)==0,'mutation occurred before guard')
        return
    raise AssertionError('unsafe state was accepted')

def fixture(rid=23203732):
    baseline=json.loads((ROOT/'receipts'/str(rid)/'before.json').read_text())
    document=json.loads((ROOT/'patches'/f'{rid}.json').read_text())
    md=document['metadata']
    orig=legacy.editable_metadata({'metadata':baseline['metadata']})
    session={'id':rid,'environment':'production','phase':'update_requested',
             'original_metadata':orig,'target_metadata':{**orig,**md},
             'native_original':copy.deepcopy(baseline['native']),'files':copy.deepcopy(baseline['files']),
             'doi':baseline['doi'],'patch_fields':list(md)}
    public={'id':str(rid),'is_draft':False,'is_published':True,
            **copy.deepcopy(baseline['native']),'files':copy.deepcopy(baseline['native_files']),
            'parent':{'id':baseline['identity']['parent_id'],'pids':copy.deepcopy(baseline['identity']['parent_pids'])},
            'versions':copy.deepcopy(baseline['identity']['versions'])}
    # Independent expected translation for primary simple-field test fixtures.
    target=copy.deepcopy(public['metadata'])
    if set(md)-{'keywords','language'}: target=pp.legacy_native_target(public,md,rid)
    else:
        if 'keywords' in md: target['subjects']=[{'subject':w} for w in md['keywords']]
        if 'language' in md: target['languages']=[{'id':md['language']}]
    draft=copy.deepcopy(public);draft.update(is_draft=True,metadata=target)
    draft['pids'].pop('oai',None)
    for entry in draft['files']['entries'].values(): entry.pop('links',None)
    draft['files'].pop('default_preview',None)
    deposit={'id':rid,'submitted':True,'state':'inprogress','doi':baseline['doi'],
             'conceptrecid':baseline['conceptrecid'],'metadata':copy.deepcopy(session['target_metadata']),
             'files':[{'filename':f['name'],'checksum':'md5:'+f['md5'],'filesize':f['size']} for f in baseline['files']]}
    versions={'hits':{'total':baseline['identity']['version_count'],
                       'hits':[{'id':i} for i in baseline['identity']['version_ids']]}}
    return baseline,document,session,public,draft,deposit,versions

class FakeClient:
    base='https://zenodo.org'
    def __init__(self, f):
        self.baseline,self.document,self.session,self.public,self.draft,self.deposit,self.versions=copy.deepcopy(f)
        self.puts=[];self.reads=[];self.after_fault=None;self.public_after_fault=None;self.public_gets=0
    def get(self,rid): return copy.deepcopy(self.deposit)
    def request(self,method,url,payload=None,**kwargs):
        path=urlsplit(url).path;rid=self.baseline['id']
        legacyroot=f'/api/deposit/depositions/{rid}'
        if path==legacyroot and method=='GET':return self.get(rid)
        if path==legacyroot and method=='PUT':
            assert_true(set(payload)=={'metadata'})
            assert_true(payload['metadata']==self.session['target_metadata'],'legacy target not frozen')
            self.deposit['metadata']=copy.deepcopy(payload['metadata']);self.deposit['state']='inprogress'
            self.draft['files'].pop('default_preview',None)
            self.legacy_puts=getattr(self,'legacy_puts',[])+[copy.deepcopy(payload)]
            return self.get(rid)
        if path==legacyroot+'/actions/publish' and method=='POST':
            self.public=copy.deepcopy(self.draft);self.public.update(is_draft=False,is_published=True)
            self.public['pids']=copy.deepcopy(self.baseline['native']['pids'])
            for name,e in self.public['files']['entries'].items():
                if 'links' in self.baseline['native_files']['entries'][name]:e['links']=copy.deepcopy(self.baseline['native_files']['entries'][name]['links'])
            self.deposit['state']='done';self.publish_count=getattr(self,'publish_count',0)+1
            return self.get(rid)
        if method=='GET':
            self.reads.append(path)
            if path==f'/api/records/{rid}/draft': return copy.deepcopy(self.draft)
            if path==f'/api/records/{rid}/versions': return copy.deepcopy(self.versions)
            if path==f'/api/records/{rid}':
                self.public_gets+=1
                if self.public_after_fault and self.puts: self.public_after_fault(self.public)
                return copy.deepcopy(self.public)
            raise AssertionError('unexpected fake read '+path)
        assert_true(method=='PUT' and path==f'/api/records/{rid}/draft','unsafe mutation route')
        assert_true(set(payload)=={'metadata','custom_fields','files'},'unsafe native payload keys')
        assert_true(set(payload['files'])=={'enabled','default_preview','order'},'unsafe files payload keys')
        assert_true(payload['files']==pp.display_file_options(self.baseline['native_files']),'display payload drift')
        assert_true('file' not in kwargs,'file upload supplied')
        self.puts.append(copy.deepcopy(payload))
        self.draft['metadata']=copy.deepcopy(payload['metadata']);self.draft['custom_fields']=copy.deepcopy(payload['custom_fields'])
        self.draft['files']['enabled']=payload['files']['enabled']
        pv=payload['files']['default_preview']
        if pv is None: self.draft['files'].pop('default_preview',None)
        else: self.draft['files']['default_preview']=pv
        # Source says order is ignored by update_draft; copied edit order survives.
        if self.after_fault: self.after_fault(self.draft)
        return copy.deepcopy(self.draft)

class Context:
    def __init__(self,rid=23203732):
        self.f=fixture(rid);self.rid=rid
    def __enter__(self):
        self.tmp=tempfile.TemporaryDirectory(prefix='preview_independent_',dir=ROOT/'reviews')
        self.home=Path(self.tmp.name);self.receipt=self.home/'receipts'/str(self.rid);self.receipt.mkdir(parents=True)
        self.patch=self.home/'patches'/f'{self.rid}.json';self.patch.parent.mkdir();self.patch.write_bytes((ROOT/'patches'/f'{self.rid}.json').read_bytes())
        digest=hashlib.sha256(self.patch.read_bytes()).hexdigest()
        save(self.home/'APPROVED_PROPOSALS.json',{'records':[{'id':self.rid,'patch_sha256':digest,'patch_fields':list(self.f[1]['metadata'])}]})
        self.client=FakeClient(self.f);self.hook=patch.object(pp,'HERE',self.home);self.hook.start()
        return self
    def __exit__(self,*args): self.hook.stop();self.tmp.cleanup()
    def run(self): return pp.repair_owned_preview(self.client,self.rid,self.client.baseline,self.patch,self.client.session,self.receipt)


def successful():
    with Context() as c:
        r=c.run();assert_true(r['state']=='preview_restored' and len(c.client.puts)==1)
        assert_true((c.receipt/'preview_repair_pre.json').exists() and (c.receipt/'preview_repair_post.json').exists())
        assert_true(c.client.puts[0]['metadata']==c.f[4]['metadata'],'rich metadata adopted differently')
        assert_true(r['native_staged']['pids']==c.client.baseline['native']['pids'],'OAI normalization absent')
        r=c.run();assert_true(r['mutations']==0 and len(c.client.puts)==1,'repeat mutation')
check('exact_owned_preview_loss_restored_once_then_idempotent_read',successful)

def no_preview():
    # 23271172 has no original default_preview key and a keywords/language patch.
    with Context(23271172) as c:
        r=c.run();assert_true(r['state']=='preview_already_preserved' and len(c.client.puts)==0)
check('original_preview_absence_remains_absent_without_write',no_preview)

def preserved_preview():
    with Context() as c:
        c.client.draft['files']['default_preview']=c.client.baseline['native_files']['default_preview']
        r=c.run();assert_true(r['mutations']==0)
check('already_preserved_populated_preview_no_write',preserved_preview)

for key,value in [('id',999),('environment','sandbox'),('phase','prepared'),('phase','edit_requested'),('phase','publish_requested'),('phase','published'),('phase','discarded'),('doi','10.5281/zenodo.999'),('files',[]),('patch_fields',[]),('original_metadata',{}),('target_metadata',{}),('native_original',{})]:
    def t(key=key,value=value):
        with Context() as c: c.client.session[key]=value;reject(c.run,c.client)
    check('owned_session_reject_'+key+'_'+str(value)[:24],t)

def bad_patch():
    with Context() as c:
        d=json.loads(c.patch.read_text());d['metadata']['keywords'].append('unreviewed');save(c.patch,d);reject(c.run,c.client)
check('content_frozen_patch_hash_mismatch_no_write',bad_patch)

public_faults={
 'metadata':lambda r:r['metadata'].update(description='unreviewed'),
 'access':lambda r:r['access'].update(record='restricted'),
 'custom_fields':lambda r:r['custom_fields'].update(unreviewed='x'),
 'doi':lambda r:r['pids']['doi'].update(identifier='10.5281/zenodo.999'),
 'parent_pid':lambda r:r['parent']['pids'].clear(),
 'version_index':lambda r:r['versions'].update(index=99),
 'preview':lambda r:r['files'].pop('default_preview',None),
 'file_metadata':lambda r:next(iter(r['files']['entries'].values()))['metadata'].update(unreviewed=1),
 'file_links':lambda r:next(iter(r['files']['entries'].values()))['links'].update(content='https://invalid.example'),
}
for name,fn in public_faults.items():
    def t(fn=fn):
        with Context() as c: fn(c.client.public);reject(c.run,c.client)
    check('public_'+name+'_drift_no_write',t)

def bad_registry():
    with Context() as c: c.client.versions['hits']['hits'].append({'id':'999'});reject(c.run,c.client)
check('full_version_registry_drift_no_write',bad_registry)

draft_faults={
 'not_pending':lambda c:c.deposit.update(state='done'),
 'legacy_target':lambda c:c.deposit['metadata'].update(description='unreviewed'),
 'legacy_doi':lambda c:c.deposit.update(doi='10.5281/zenodo.999'),
 'legacy_files':lambda c:c.deposit['files'][0].update(filesize=1),
 'legacy_concept':lambda c:c.deposit.update(conceptrecid=999),
 'draft_id':lambda c:c.draft.update(id='999'),
 'not_draft':lambda c:c.draft.update(is_draft=False),
 'draft_doi':lambda c:c.draft['pids']['doi'].update(identifier='10.5281/zenodo.999'),
 'extra_pid':lambda c:c.draft['pids'].update(unreviewed={'identifier':'x'}),
 'version_index':lambda c:c.draft['versions'].update(index=99),
 'parent_pid':lambda c:c.draft['parent']['pids'].clear(),
 'access':lambda c:c.draft['access'].update(record='restricted'),
 'custom_fields':lambda c:c.draft['custom_fields'].update(unreviewed='x'),
 'unpatched_metadata':lambda c:c.draft['metadata'].update(description='unreviewed'),
 'patched_native_extra_subject':lambda c:c.draft['metadata']['subjects'].append({'subject':'unreviewed'}),
 'file_id':lambda c:next(iter(c.draft['files']['entries'].values())).update(id='new'),
 'file_checksum':lambda c:next(iter(c.draft['files']['entries'].values())).update(checksum='md5:'+'0'*32),
 'file_size':lambda c:next(iter(c.draft['files']['entries'].values())).update(size=1),
 'file_metadata':lambda c:next(iter(c.draft['files']['entries'].values()))['metadata'].update(unreviewed=1),
 'file_access':lambda c:next(iter(c.draft['files']['entries'].values()))['access'].update(hidden=True),
 'file_extra_key':lambda c:next(iter(c.draft['files']['entries'].values())).update(unreviewed=1),
 'file_generated_link_changed':lambda c:next(iter(c.draft['files']['entries'].values())).update(links={'self':'unreviewed'}),
 'order':lambda c:c.draft['files'].update(order=['paper.pdf']),
 'enabled':lambda c:c.draft['files'].update(enabled=False),
 'wrong_preview':lambda c:c.draft['files'].update(default_preview='cost-betti-source-and-verification.zip'),
}
for name,fn in draft_faults.items():
    def t(fn=fn):
        with Context() as c: fn(c.client);reject(c.run,c.client)
    check('draft_'+name+'_drift_no_write',t)

def prior_receipt():
    with Context() as c: save(c.receipt/'preview_repair_pre.json',{'prior':True});reject(c.run,c.client)
check('uncertain_prior_repair_request_not_retried',prior_receipt)

for name,fn in [('order',lambda d:d['files'].update(order=['paper.pdf'])),('metadata',lambda d:d['metadata'].update(description='unreviewed')),('entry',lambda d:next(iter(d['files']['entries'].values())).update(size=1))]:
    def t(fn=fn):
        with Context() as c:
            c.client.after_fault=fn;reject(c.run);assert_true(len(c.client.puts)==1)
            assert_true(not (c.receipt/'preview_repair_post.json').exists(),'failed result marked restored')
    check('repair_readback_'+name+'_drift_no_success_receipt',t)

def pub_after():
    with Context() as c:
        c.client.public_after_fault=lambda p:p['metadata'].update(title='unreviewed')
        reject(c.run);assert_true(len(c.client.puts)==1)
        assert_true(not (c.receipt/'preview_repair_post.json').exists())
check('public_race_after_repair_detected_no_success_receipt',pub_after)

for label,files in [('bad_enabled',{'enabled':1,'order':[],'entries':{}}),('bad_order',{'enabled':True,'order':'x','entries':{}}),('missing_preview_entry',{'enabled':True,'default_preview':'missing.pdf','order':[],'entries':{}}),('missing_order_entry',{'enabled':True,'order':['missing.pdf'],'entries':{}})]:
    check('display_options_reject_'+label,lambda files=files:reject(lambda:pp.display_file_options(files)))

for rid in [22770864,22929556]:
    def t(rid=rid):
        with Context(rid) as c:
            r=c.run();assert_true(r['state']=='preview_restored' and r['mutations']==1)
    check('exact_special_legacy_patch_preview_repair_'+str(rid),t)

# Exercise mutation-route clients without initializing or loading credentials.
def bound_client(cls):
    c=object.__new__(cls);c.record_id=23203732;c.actions=[];c.baseline=fixture()[0]
    c.base='https://zenodo.org';c.host='zenodo.org';c.token='offline-unused'
    return c
for cls in [ar.BoundClient,rp.RepairClient]:
    for method,path in [('POST','/api/records'),('POST','/api/records/23203732/versions'),('POST','/api/deposit/depositions/23203732/actions/newversion'),('PUT','/api/records/999/draft'),('POST','/api/records/23203732/draft/files'),('PUT','/api/records/23203732/draft/files/paper.pdf/content'),('DELETE','/api/records/23203732/draft')]:
        def t(cls=cls,method=method,path=path):
            with patch.object(PacedClient,'request',lambda *a,**k:{'fake':True}):reject(lambda:cls.request(bound_client(cls),method,'https://zenodo.org'+path,{}))
        check(cls.__name__+'_reject_route_'+method+'_'+path,t)
    for name,payload,kwargs in [('entries',{'metadata':{},'custom_fields':{},'files':{'entries':{}}},{}),('pids',{'metadata':{},'custom_fields':{},'pids':{}},{}),('access',{'metadata':{},'custom_fields':{},'access':{}},{}),('upload',None,{'file':Path('paper.pdf')}),('wrong_display',{'metadata':{},'custom_fields':{},'files':{'enabled':False,'default_preview':None,'order':[]}}, {})]:
        def t(cls=cls,payload=payload,kwargs=kwargs):
            with patch.object(PacedClient,'request',lambda *a,**k:{'fake':True}):reject(lambda:cls.request(bound_client(cls),'PUT','https://zenodo.org/api/records/23203732/draft',payload,**kwargs))
        check(cls.__name__+'_reject_payload_'+name,t)

def actual_bound_update():
    with Context() as c:
        state=c.home/'state';state.mkdir()
        save(state/f'metadata-{c.rid}-production.json',c.client.session)
        save(c.receipt/'before.json',c.client.baseline)
        with patch.object(ar,'HERE',c.home),patch.object(zenodo,'STATE_DIR',state),patch.object(zenodo,'token_for',lambda *a:'offline-unused'),patch.object(PacedClient,'request',lambda self,*a,**kw:c.client.request(*a,**kw)):
            bound=ar.BoundClient(c.rid,c.client.baseline);bound.first_deposit=False;bound.first_native=False
            bound.update(c.rid,c.client.session['target_metadata'])
            assert_true(len(c.client.legacy_puts)==1 and len(c.client.puts)==1)
            assert_true([x['path'] for x in bound.actions]==[f'/api/deposit/depositions/{c.rid}',f'/api/records/{c.rid}/draft'])
check('actual_BoundClient_update_legacy_PUT_then_one_verified_display_PUT',actual_bound_update)

def recovery_and_publish():
    with Context() as c:
        state=c.home/'state';state.mkdir();place=state/f'metadata-{c.rid}-production.json'
        save(place,c.client.session);save(c.receipt/'before.json',c.client.baseline)
        raw_guard={'raw':'must remain exact'};save(c.receipt/'staging_guard_stop_details.json',raw_guard)
        with patch.object(rp,'HERE',c.home),patch.object(ar,'HERE',c.home),patch.object(zenodo,'STATE_DIR',state),patch.object(zenodo,'token_for',lambda *a:'offline-unused'),patch.object(rp,'RepairClient',lambda *a:c.client),patch.object(PacedClient,'request',lambda self,*a,**kw:c.client.request(*a,**kw)):
            result=rp.run(c.rid);assert_true(result['state']=='preview_restored')
            assert_true(json.loads((c.receipt/'preview_repair_original_session.json').read_text())==c.f[2])
            assert_true(json.loads((c.receipt/'staging_guard_stop_details.json').read_text())==raw_guard)
            marker=json.loads((c.receipt/'preview_repair_recovery.json').read_text())
            assert_true(marker['baseline_sha256']==hashlib.sha256((c.receipt/'before.json').read_bytes()).hexdigest())
            result=rp.run(c.rid);assert_true(result['mutations']==0 and len(c.client.puts)==1)
            ar.run_one(c.rid)
            assert_true(c.client.publish_count==1 and len(c.client.puts)==1)
            after=json.loads((c.receipt/'after.json').read_text())
            for k in ['identity','doi','conceptrecid','files','native_files']:assert_true(after[k]==c.client.baseline[k],'final '+k+' changed')
check('actual_owned_recovery_marker_idempotence_then_same_record_publish',recovery_and_publish)

def recovery_tampered_target():
    with Context() as c:
        state=c.home/'state';state.mkdir();place=state/f'metadata-{c.rid}-production.json'
        save(place,c.client.session);save(c.receipt/'before.json',c.client.baseline)
        with patch.object(rp,'HERE',c.home),patch.object(ar,'HERE',c.home),patch.object(zenodo,'STATE_DIR',state),patch.object(zenodo,'token_for',lambda *a:'offline-unused'),patch.object(rp,'RepairClient',lambda *a:c.client),patch.object(PacedClient,'request',lambda self,*a,**kw:c.client.request(*a,**kw)):
            rp.run(c.rid)
            c.client.draft['metadata']['subjects'].append({'subject':'unreviewed'})
            saved=json.loads(place.read_text());saved['native_staged']['metadata']['subjects'].append({'subject':'unreviewed'});save(place,saved)
            markerpath=c.receipt/'preview_repair_recovery.json';marker=json.loads(markerpath.read_text());marker['native_staged']=copy.deepcopy(saved['native_staged']);save(markerpath,marker)
            reject(lambda:ar.run_one(c.rid))
            assert_true(getattr(c.client,'publish_count',0)==0,'unreviewed staged subject reached publish')
check('legacy_recovery_matching_tampered_staged_marker_rejected_before_publish',recovery_tampered_target)

for label,fn in [('version_registry',lambda c:c.versions['hits']['hits'].append({'id':'999'})),('public_files',lambda c:next(iter(c.public['files']['entries'].values()))['metadata'].update(unreviewed=1)),('public_rich_metadata',lambda c:c.public['metadata'].update(description='unreviewed'))]:
    def t(fn=fn):
        with Context() as c:
            state=c.home/'state';state.mkdir();place=state/f'metadata-{c.rid}-production.json'
            save(place,c.client.session);save(c.receipt/'before.json',c.client.baseline)
            with patch.object(rp,'HERE',c.home),patch.object(ar,'HERE',c.home),patch.object(zenodo,'STATE_DIR',state),patch.object(zenodo,'token_for',lambda *a:'offline-unused'),patch.object(rp,'RepairClient',lambda *a:c.client),patch.object(PacedClient,'request',lambda self,*a,**kw:c.client.request(*a,**kw)):
                rp.run(c.rid);fn(c.client);reject(lambda:ar.run_one(c.rid))
                assert_true(getattr(c.client,'publish_count',0)==0,'public drift reached publish')
    check('legacy_recovery_prepublication_'+label+'_drift_rejected',t)

def helper_error_not_swallowed():
    with Context() as c:
        state=c.home/'state';state.mkdir();save(state/f'metadata-{c.rid}-production.json',c.client.session)
        with patch.object(ar,'HERE',c.home),patch.object(zenodo,'STATE_DIR',state),patch.object(zenodo,'token_for',lambda *a:'offline-unused'),patch.object(PacedClient,'request',lambda self,*a,**kw:c.client.request(*a,**kw)),patch.object(ar,'repair_owned_preview',side_effect=zenodo.DepositError('fake preserving read failed')):
            bound=ar.BoundClient(c.rid,c.client.baseline);bound.first_deposit=False
            try:bound.update(c.rid,c.client.session['target_metadata'])
            except RuntimeError:return
            raise AssertionError('repair failure not wrapped to fatal RuntimeError')
check('legacy_repair_DepositError_cannot_be_swallowed_by_mutate_and_read',helper_error_not_swallowed)

# Known exceptional frozen legacy proposals must be accepted by the verifier.
for rid in [22770864,22929556]:
    def t(rid=rid):
        b,d,s,p,dr,dep,v=fixture(rid)
        target=pp.legacy_native_target(p,d['metadata'],rid)
        if rid==22770864:
            old=copy.deepcopy(p['metadata']['creators'][0]); old['person_or_org'].update(name='Kriebel, Alec',given_name='Alec',family_name='Kriebel')
            assert_true(target['creators']==[old],'creator structures not preserved')
        else:
            assert_true(target['resource_type']=={'id':'publication-preprint'})
            assert_true(target['description']==d['metadata']['description'])
        for key in set(p['metadata'])-set(legacy.PATCH_NATIVE_KEYS[k] for k in d['metadata']):
            assert_true(target[key]==p['metadata'][key],'unpatched native field '+key)
    check('legacy_special_patch_native_target_'+str(rid),t)

OUTPUT={'utc':__import__('datetime').datetime.now(__import__('datetime').timezone.utc).isoformat(),
        'offline_only':True,'network_requests':0,'credentials_loaded':False,
        'tests':RESULTS,'passed':sum(x['pass'] for x in RESULTS),'failed':sum(not x['pass'] for x in RESULTS),
        'code_sha256':{name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in ['preview_preservation.py','repair_owned_preview.py','apply_reviewed.py','native_metadata.py','native_views.py']}}
save(ROOT/'reviews/PREVIEW_INDEPENDENT_CHECKS.json',OUTPUT)
print(json.dumps({'passed':OUTPUT['passed'],'failed':OUTPUT['failed'],'failures':[x for x in RESULTS if not x['pass']]},indent=2))
