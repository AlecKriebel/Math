"""Offline end-to-end independent checks of native display preservation.

Every request is handled by a fake client. Never loads real credentials or network.
"""
import copy, hashlib, json, sys, tempfile
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch
from urllib.parse import urlsplit
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT.parent/'zenodo_deposit_tool')]
import native_metadata as nm
import zenodo
import audit_receipts as audit
from preview_preservation import display_file_options

TESTS=[]
def save(p,v):p.write_text(json.dumps(v,indent=2)+'\n')
def yes(v,msg='assertion failed'):
    if not v:raise AssertionError(msg)
def check(name,fn):
    try:fn();TESTS.append({'name':name,'pass':True})
    except Exception as e:TESTS.append({'name':name,'pass':False,'error':type(e).__name__+': '+str(e)})
def rejected(fn):
    try:fn()
    except (RuntimeError,zenodo.DepositError,ValueError,KeyError):return
    raise AssertionError('unsafe state accepted')

class NativeFake:
    base='https://zenodo.org'
    def __init__(self,b,p):
        self.b=copy.deepcopy(b);self.p=copy.deepcopy(p);self.rid=b['id'];self.calls=[];self.draft=None
        self.public={'id':str(self.rid),'is_draft':False,'is_published':True,**copy.deepcopy(b['native']),
                     'files':copy.deepcopy(b['native_files']),
                     'parent':{'id':b['identity']['parent_id'],'pids':copy.deepcopy(b['identity']['parent_pids'])},
                     'versions':copy.deepcopy(b['identity']['versions'])}
        self.versions={'hits':{'total':b['identity']['version_count'],'hits':[{'id':i} for i in b['identity']['version_ids']]}}
        self.md=copy.deepcopy(b['metadata']);self.state='done';self.stage_fault=None;self.publish_fault=None
    def get(self,rid):
        yes(rid==self.rid)
        return {'id':self.rid,'state':self.state,'submitted':True,'doi':self.b['doi'],'conceptrecid':self.b['conceptrecid'],
                'metadata':copy.deepcopy(self.md),
                'files':[{'filename':f['name'],'checksum':f['md5'],'filesize':f['size']} for f in self.b['files']]}
    def native_get(self,rid,draft=False):
        yes(rid==self.rid);return copy.deepcopy(self.draft if draft else self.public)
    def request(self,method,url,payload=None,**kw):
        path=urlsplit(url).path;self.calls.append({'method':method,'path':path,'payload':copy.deepcopy(payload)})
        root=f'/api/records/{self.rid}'
        if method=='GET' and path==root+'/versions':return copy.deepcopy(self.versions)
        if method=='GET' and path==root:return copy.deepcopy(self.public)
        if method=='GET' and path==root+'/draft':return copy.deepcopy(self.draft)
        yes('file' not in kw,'file upload')
        if method=='POST' and path==root+'/draft':
            yes(payload is None,'edit payload included fields');yes(self.state=='done','reuse edit')
            self.draft=copy.deepcopy(self.public);self.draft['is_draft']=True;self.draft['pids'].pop('oai',None)
            for e in self.draft['files']['entries'].values():e.pop('links',None)
            self.state='inprogress';return copy.deepcopy(self.draft)
        if method=='PUT' and path==root+'/draft':
            yes(set(payload)=={'metadata','custom_fields','files'},'unsafe native PUT payload')
            yes(payload['files']==display_file_options(self.b['native_files']),'display option drift')
            yes(payload['custom_fields']==self.b['native']['custom_fields'],'custom fields drift')
            yes(nm.canonical(payload['metadata'])==nm.canonical(audit.expected_native(self.b['native']['metadata'],self.p)),
                'target differs from independent reconstruction')
            self.draft['metadata']=copy.deepcopy(payload['metadata']);self.draft['custom_fields']=copy.deepcopy(payload['custom_fields'])
            self.draft['files']['enabled']=payload['files']['enabled']
            if payload['files']['default_preview'] is None:self.draft['files'].pop('default_preview',None)
            else:self.draft['files']['default_preview']=payload['files']['default_preview']
            # Real component ignores order in update, keeping original edit-copy order.
            self.md={**self.md,**self.p}
            if self.stage_fault:self.stage_fault(self.draft)
            return copy.deepcopy(self.draft)
        if method=='POST' and path==root+'/draft/actions/publish':
            yes(payload is None,'publish payload included fields')
            self.public=copy.deepcopy(self.draft);self.public.update(is_draft=False,is_published=True)
            self.public['pids']=copy.deepcopy(self.b['native']['pids'])
            for name,e in self.public['files']['entries'].items():
                if 'links' in self.b['native_files']['entries'][name]:e['links']=copy.deepcopy(self.b['native_files']['entries'][name]['links'])
            self.state='done'
            if self.publish_fault:self.publish_fault(self.public)
            return copy.deepcopy(self.public)
        raise AssertionError('unsafe mutation route '+method+' '+path)

class Context:
    def __init__(self,rid):self.rid=rid
    def __enter__(self):
        self.tmp=tempfile.TemporaryDirectory(prefix='native_preview_independent_',dir=ROOT/'reviews');self.home=Path(self.tmp.name)
        self.b=json.loads((ROOT/'receipts'/str(self.rid)/'before.json').read_text())
        self.p=json.loads((ROOT/'patches'/f'{self.rid}.json').read_text())['metadata']
        self.dest=self.home/'receipts'/str(self.rid);self.dest.mkdir(parents=True);save(self.dest/'before.json',self.b)
        self.path=self.home/'patches'/f'{self.rid}.json';self.path.parent.mkdir();self.path.write_bytes((ROOT/'patches'/f'{self.rid}.json').read_bytes())
        save(self.home/'APPROVED_PROPOSALS.json',{'records':[{'id':self.rid,'patch_sha256':hashlib.sha256(self.path.read_bytes()).hexdigest()}]})
        self.state=self.home/'state';self.state.mkdir();self.client=NativeFake(self.b,self.p)
        self.hooks=[patch.object(nm,'HERE',self.home),patch.object(zenodo,'STATE_DIR',self.state),
                    patch.object(zenodo,'token_for',lambda *a:'offline-unused'),
                    patch.object(nm,'PacedClient',lambda *a:self.client)]
        for h in self.hooks:h.start()
        return self
    def __exit__(self,*a):
        for h in reversed(self.hooks):h.stop()
        self.tmp.cleanup()
    def stage(self):return nm.run(self.rid,self.path)
    def publish(self):return nm.run(self.rid,self.path,True)

eligible=json.loads((ROOT/'reviews/PREVIEW_NATIVE_ELIGIBILITY.json').read_text())['records']
ids=[x['id'] for x in eligible if x['eligible'] and not x['active_owned_legacy_stage']]
for rid in ids:
    def t(rid=rid):
        with Context(rid) as c:
            r=c.stage();yes(r['state']=='ready_to_publish_metadata')
            s=json.loads((c.state/f'native-metadata-{rid}-production.json').read_text());yes(s['phase']=='staged')
            yes(s['target_metadata']==audit.expected_native(c.b['native']['metadata'],c.p))
            r=c.publish();yes(r['state']=='published')
            a=json.loads((c.dest/'after.json').read_text())
            for k in ['identity','doi','conceptrecid','files','native_files']:yes(a[k]==c.b[k],'protected '+k+' drift')
            for k in ['pids','access','custom_fields']:yes(a['native'][k]==c.b['native'][k])
            yes([x['method']+' '+x['path'] for x in c.client.calls if x['method']!='GET']==
                [f'POST /api/records/{rid}/draft',f'PUT /api/records/{rid}/draft',f'POST /api/records/{rid}/draft/actions/publish'])
    check('native_full_stage_publish_exact_preservation_'+str(rid),t)

for name,fn in [('preview',lambda d:d['files'].pop('default_preview',None)),('order',lambda d:d['files'].update(order=['unexpected'])),
                ('file_metadata',lambda d:next(iter(d['files']['entries'].values()))['metadata'].update(unreviewed=1)),
                ('metadata',lambda d:d['metadata'].update(description='unreviewed')),
                ('doi',lambda d:d['pids']['doi'].update(identifier='10.5281/zenodo.999')),
                ('access',lambda d:d['access'].update(record='restricted'))]:
    def t(fn=fn):
        with Context(21699069) as c:
            c.client.stage_fault=fn;rejected(c.stage)
            s=json.loads((c.state/f'native-metadata-{c.rid}-production.json').read_text());yes(s['phase']!='staged')
            yes(not any(x['path'].endswith('publish') for x in c.client.calls))
    check('native_stage_'+name+'_drift_stops_before_publish',t)

for name,fn in [('metadata',lambda d:d['metadata'].update(description='unreviewed')),
                ('file_access',lambda d:next(iter(d['files']['entries'].values()))['access'].update(hidden=True)),
                ('extra_pid',lambda d:d['pids'].update(unreviewed={'identifier':'x'})),
                ('parent',lambda d:d['parent'].update(id='999'))]:
    def t(fn=fn):
        with Context(21699069) as c:
            c.stage();fn(c.client.draft);rejected(c.publish)
            yes(not any(x['path'].endswith('publish') for x in c.client.calls))
    check('native_prepublication_'+name+'_drift_stops_before_publish',t)

def hashbad():
    with Context(21699069) as c:
        c.path.write_text(c.path.read_text()+' ');rejected(c.stage)
        yes(not c.client.calls,'hash mismatch made request')
check('native_frozen_patch_hash_mismatch_before_request',hashbad)

def pending():
    with Context(21699069) as c:
        c.client.state='inprogress';rejected(c.stage);yes(not c.client.calls)
check('native_unowned_pending_edit_rejected',pending)

def versionsbad():
    with Context(21971507) as c:
        c.client.versions['hits']['hits'].append({'id':'999'});rejected(c.stage)
        yes(not any(x['method']!='GET' for x in c.client.calls))
check('native_complete_version_registry_drift_before_edit',versionsbad)

def tampered_staged_target():
    with Context(21699069) as c:
        c.stage()
        place=c.state/f'native-metadata-{c.rid}-production.json'
        session=json.loads(place.read_text())
        session['target_metadata']['description']='unreviewed'
        c.client.draft['metadata']['description']='unreviewed'
        save(place,session)
        rejected(c.publish)
        yes(not any(x['path'].endswith('publish') for x in c.client.calls),'unreviewed target reached publish')
check('native_tampered_staged_target_rejected_before_publish',tampered_staged_target)

for label,fn in [('session_id',lambda s:s.update(id=999)),('original_metadata',lambda s:s['original']['metadata'].update(description='unreviewed')),('protected_snapshot',lambda s:s['protected'].update(id='999'))]:
    def t(fn=fn):
        with Context(21699069) as c:
            c.stage();place=c.state/f'native-metadata-{c.rid}-production.json';saved=json.loads(place.read_text());fn(saved);save(place,saved)
            rejected(c.publish);yes(not any(x['path'].endswith('publish') for x in c.client.calls),'inconsistent saved session reached publish')
    check('native_staged_integrity_'+label+'_rejected_before_publish',t)

for label,fn in [('version_registry',lambda c:c.versions['hits']['hits'].append({'id':'999'})),('public_rich_metadata',lambda c:c.public['metadata'].update(description='unreviewed')),('public_full_files',lambda c:next(iter(c.public['files']['entries'].values()))['metadata'].update(unreviewed=1))]:
    def t(fn=fn):
        with Context(21699069) as c:
            c.stage();fn(c.client);rejected(c.publish)
            yes(not any(x['path'].endswith('publish') for x in c.client.calls),'public drift reached publish')
    check('native_prepublication_original_'+label+'_drift_rejected',t)

def postfiles():
    with Context(21699069) as c:
        c.stage();c.client.publish_fault=lambda d:next(iter(d['files']['entries'].values())).update(size=1)
        rejected(c.publish);yes(not (c.dest/'after.json').exists())
check('native_publication_file_drift_no_verified_after_receipt',postfiles)

out={'utc':datetime.now(timezone.utc).isoformat(),'offline_only':True,'network_requests':0,'credentials_loaded':False,
     'direct_native_records':ids,'tests':TESTS,'passed':sum(x['pass'] for x in TESTS),'failed':sum(not x['pass'] for x in TESTS),
     'code_sha256':{n:hashlib.sha256((ROOT/n).read_bytes()).hexdigest() for n in ['native_metadata.py','native_views.py','preview_preservation.py','baseline.py']}}
save(ROOT/'reviews/NATIVE_PREVIEW_INDEPENDENT_CHECKS.json',out)
print(json.dumps({'record_count':len(ids),'passed':out['passed'],'failed':out['failed'],'failures':[x for x in TESTS if not x['pass']]},indent=2))
