"""Offline adversarial preview recovery tests using actual reviewed baselines."""
from pathlib import Path
import contextlib, copy, hashlib, importlib.util, json, sys, tempfile
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT.parent/'zenodo_deposit_tool')]
import preview_preservation as h
import repair_owned_preview as cli
import native_metadata as n
import apply_reviewed as w

TESTS=[]
def check(name,passed,details=None):TESTS.append({'test':name,'passed':bool(passed),'details':details})

def fixture(rid=23203732):
    b=json.loads((ROOT/'receipts'/str(rid)/'before.json').read_text())
    p=json.loads((ROOT/'patches'/f'{rid}.json').read_text())
    original=n.legacy.editable_metadata({'metadata':b['metadata']})
    session={'id':rid,'environment':'production','phase':'update_requested','doi':b['doi'],
             'files':b['files'],'original_metadata':original,'target_metadata':{**original,**p['metadata']},
             'native_original':b['native'],'patch_fields':list(p['metadata'])}
    public={**copy.deepcopy(b['native']),'files':copy.deepcopy(b['native_files']),
            'id':b['identity']['id'],'parent':{'id':b['identity']['parent_id'],'pids':b['identity']['parent_pids']},
            'versions':b['identity']['versions'],'is_draft':False,'is_published':True}
    target=h.legacy_native_target(public,p['metadata'],rid)
    return b,p,session,public,target

class Fake:
    base='https://offline.invalid'
    def __init__(self,b,s,public,target,already=False,no_preview=False,drift=None,after=None,fail=False):
        self.b=b;self.s=s;self.public=copy.deepcopy(public);self.draft=copy.deepcopy(public);self.draft['is_draft']=True;self.draft['is_published']=False
        self.draft['metadata']=copy.deepcopy(target);self.draft['pids'].pop('oai',None)
        for entry in self.draft['files']['entries'].values():entry.pop('links',None)
        if not already:self.draft['files'].pop('default_preview',None)
        self.calls=[];self.after=after;self.fail=fail;self.target=target
        if drift:
            entry=next(iter(self.draft['files']['entries'].values()))
            if drift=='order':self.draft['files']['order']=['wrong-file.pdf']
            elif drift=='checksum':entry['checksum']='md5:'+'b'*32
            elif drift=='uuid':entry['id']='different-file-id'
            elif drift=='file_metadata':entry['metadata']={'unexpected':'value'}
            elif drift=='file_access':entry['access']['hidden']=True
            elif drift=='file_count':self.draft['files']['count']+=1
            elif drift=='extra_file':self.draft['files']['entries']['unexpected.pdf']=copy.deepcopy(entry)
            elif drift=='missing_file':self.draft['files']['entries'].pop(next(iter(self.draft['files']['entries'])))
            elif drift=='changed_preview':self.draft['files']['default_preview']='another.pdf'
            elif drift=='native_patched_extra':self.draft['metadata']['subjects'][0]['unexpected']='extra'
            elif drift=='native_unpatched':self.draft['metadata']['creators'][0]['unexpected']='extra'
            elif drift=='doi':self.draft['pids']['doi']['identifier']='10.1234/new'
            elif drift=='custom':self.draft['custom_fields']['unexpected']='value'
            elif drift=='access':self.draft['access']['files']='restricted'
            elif drift=='public_files':self.public['files']['count']+=1
            elif drift=='public_metadata':self.public['metadata']['title']='changed'
            elif drift=='versions':self.public['versions']['index']+=1
            elif drift=='version_registry':self.version_extra=True
        self.version_extra=getattr(self,'version_extra',False)
    def get(self,rid):
        return {'id':rid,'state':'inprogress','submitted':True,'doi':self.b['doi'],
                'conceptrecid':self.b['conceptrecid'],'metadata':copy.deepcopy(self.s['target_metadata']),
                'files':[{'filename':f['name'],'checksum':f['md5'],'filesize':f['size']} for f in self.b['files']]}
    def request(self,method,url,payload=None,**kw):
        self.calls.append((method,url,copy.deepcopy(payload)))
        if method=='GET':
            if '/api/deposit/depositions/' in url:return self.get(self.b['id'])
            if '/versions?' in url:
                ids=self.b['identity']['version_ids']+(['newversion'] if self.version_extra else [])
                return {'hits':{'total':len(ids),'hits':[{'id':rid} for rid in ids]}}
            return copy.deepcopy(self.draft if url.endswith('/draft') else self.public)
        if method=='PUT' and url==self.base+f'/api/records/{self.b["id"]}/draft':
            h.validate_display_payload(payload,self.b)
            if self.fail:raise RuntimeError('uncertain injected PUT response')
            self.draft['metadata']=copy.deepcopy(payload['metadata']);self.draft['custom_fields']=copy.deepcopy(payload['custom_fields']);self.draft['files'].update(copy.deepcopy(payload['files']))
            if not self.draft['files'].get('default_preview'):self.draft['files'].pop('default_preview',None)
            if self.after=='preview':self.draft['files'].pop('default_preview',None)
            elif self.after=='checksum':next(iter(self.draft['files']['entries'].values()))['checksum']='md5:'+'b'*32
            elif self.after=='metadata':self.draft['metadata']['subjects'][0]['unexpected']='extra'
            elif self.after=='public':self.public['files']['order']=['wrong.pdf']
            return copy.deepcopy(self.draft)
        if method=='PUT' and url==self.base+f'/api/deposit/depositions/{self.b["id"]}':
            assert set(payload)=={'metadata'} and payload['metadata']==self.s['target_metadata']
            self.draft['metadata']=copy.deepcopy(self.target);self.draft['files'].pop('default_preview',None)
            return self.get(self.b['id'])
        raise AssertionError('Unexpected mutation route '+method+' '+url)

def case(name,rid=23203732,drift=None,session_drift=None,approval=None,already=False,after=None,fail=False,save_fail=False,pre_existing=False):
    with tempfile.TemporaryDirectory(prefix='preview_probe_',dir=ROOT/'reviews') as temp:
        d=Path(temp);b,p,s,pub,t=fixture(rid);pp=d/'patch.json';pp.write_text(json.dumps(p))
        if session_drift:
            if session_drift=='phase':s['phase']='published'
            elif session_drift=='id':s['id']=123
            elif session_drift=='environment':s['environment']='sandbox'
            elif session_drift=='target':s['target_metadata']['keywords']=['unreviewed']
            elif session_drift=='original':s['original_metadata']['title']='unreviewed'
            elif session_drift=='native_original':s['native_original']=copy.deepcopy(s['native_original']);s['native_original']['metadata']['title']='unreviewed'
            elif session_drift=='files':s['files']=[]
            elif session_drift=='doi':s['doi']='10.1234/new'
            elif session_drift=='patch_fields':s['patch_fields']=[]
        approved={'records':[{'id':rid,'patch_sha256':hashlib.sha256(pp.read_bytes()).hexdigest()}]}
        if approval=='hash':approved['records'][0]['patch_sha256']='unreviewed'
        if approval=='missing':approved['records']=[]
        (d/'APPROVED_PROPOSALS.json').write_text(json.dumps(approved));receipt=d/'receipts';receipt.mkdir()
        if pre_existing:(receipt/'preview_repair_pre.json').write_text('{}')
        f=Fake(b,s,pub,t,already=already,drift=drift,after=after,fail=fail);exc=None;result=None
        real_save=h.zenodo.save_state
        def saver(path,value):
            if save_fail:raise OSError('injected receipt persistence failure')
            return real_save(path,value)
        with patch.object(h,'HERE',d),patch.object(h.zenodo,'save_state',saver):
            try:result=h.repair_owned_preview(f,rid,b,pp,s,receipt)
            except Exception as e:exc=str(e)
        mutations=[c for c in f.calls if c[0]!='GET'];reject=drift or session_drift or approval or save_fail or pre_existing
        if reject:passed=bool(exc) and len(mutations)==0
        elif after or fail:passed=bool(exc) and len(mutations)==1 and not (receipt/'preview_repair_post.json').exists()
        elif already:passed=not exc and not mutations and result['state']=='preview_already_preserved'
        else:passed=not exc and len(mutations)==1 and result['state']=='preview_restored' and (receipt/'preview_repair_post.json').exists() and f.public==pub
        check(name,passed,{'error':exc,'mutations':[c[:2] for c in mutations]})

case('one scoped PUT restores original preview without public/file/PID/version changes')
case('already preserved preview is fully verified and never rewritten',already=True)
for rid in [22770864,22929556]:case('exact frozen legacy correction repaired '+str(rid),rid=rid)
for key in ['order','checksum','uuid','file_metadata','file_access','file_count','extra_file','missing_file','changed_preview','native_patched_extra','native_unpatched','doi','custom','access','public_files','public_metadata','versions','version_registry']:
    case('reject pre-repair drift '+key,drift=key)
for key in ['phase','id','environment','target','original','native_original','files','doi','patch_fields']:
    case('reject non-owned reviewed session '+key,session_drift=key)
for key in ['hash','missing']:case('reject approval '+key,approval=key)
for key in ['preview','checksum','metadata','public']:case('reject post-repair drift '+key,after=key)
case('uncertain PUT stops without retries or success receipt',fail=True)
case('durable receipt failure prevents mutation',save_fail=True)
case('existing request receipt prevents mutation retry',pre_existing=True)

with tempfile.TemporaryDirectory(prefix='preview_hook_probe_',dir=ROOT/'reviews') as temp:
    d=Path(temp);rid=23203732;b,p,s,pub,t=fixture(rid);(d/'patches').mkdir();rd=d/'receipts'/str(rid);rd.mkdir(parents=True)
    pp=d/'patches'/f'{rid}.json';pp.write_text(json.dumps(p));(rd/'before.json').write_text(json.dumps(b));sp=d/'session.json';sp.write_text(json.dumps(s))
    (d/'APPROVED_PROPOSALS.json').write_text(json.dumps({'records':[{'id':rid,'patch_sha256':hashlib.sha256(pp.read_bytes()).hexdigest()}]}))
    f=Fake(b,s,pub,t,already=True);client=w.BoundClient.__new__(w.BoundClient)
    client.record_id=rid;client.baseline=b;client.base=f.base;client.actions=[];client.native_normalizations=[];client.first_deposit=False
    with patch.object(w,'HERE',d),patch.object(h,'HERE',d),patch.object(w.updates,'snapshot_path',lambda *a:sp),patch.object(w.PacedClient,'request',f.request):
        client.update(rid,s['target_metadata'])
    mut=[c for c in f.calls if c[0]!='GET']
    check('BoundClient.update performs one legacy PUT then one verified preserving native PUT',len(mut)==2 and mut[0][1].endswith('/depositions/'+str(rid)) and mut[1][1].endswith('/records/'+str(rid)+'/draft') and f.public==pub)
    class LostRepair(Fake):
        def request(self,method,url,payload=None,**kw):
            value=super().request(method,url,payload,**kw)
            if method=='PUT' and '/api/records/' in url:raise n.zenodo.DepositError('injected lost repair response')
            return value
    (rd/'preview_repair_pre.json').unlink();(rd/'preview_repair_post.json').unlink();sp.write_text(json.dumps(s));lost=LostRepair(b,s,pub,t,already=True);exc=None
    with patch.object(w,'HERE',d),patch.object(h,'HERE',d),patch.object(w.updates,'snapshot_path',lambda *a:sp),patch.object(w.PacedClient,'request',lost.request):
        try:n.legacy.mutate_and_read(client,rid,lambda:client.update(rid,s['target_metadata']),'inprogress',lambda remote:n.legacy.verify_metadata(remote,s['target_metadata'],s))
        except Exception as e:exc=e
    check('legacy recovery cannot swallow preserving repair error and continue',isinstance(exc,RuntimeError) and len([c for c in lost.calls if c[0]!='GET'])==2 and not (rd/'preview_repair_post.json').exists())
    forged=Fake(b,s,pub,t,already=True,drift='native_patched_extra');client.first_native=False;exc=None
    with patch.object(w,'HERE',d),patch.object(w.PacedClient,'request',forged.request):
        try:client.native_get(rid,draft=True)
        except Exception as e:exc=e
    check('wrapper rejects extra patched native fields even when legacy target matches',isinstance(exc,RuntimeError) and not any(c[0]!='GET' for c in forged.calls))
    sibling=Fake(b,s,pub,t,already=True,drift='version_registry');exc=None
    with patch.object(w,'HERE',d),patch.object(w.PacedClient,'request',sibling.request):
        try:client.publish(rid)
        except Exception as e:exc=e
    check('wrapper rechecks complete public version registry before publish',isinstance(exc,RuntimeError) and not any(c[0]!='GET' for c in sibling.calls))
    # Recovery CLI starts from another owned raw pending stage, without edit/publish.
    f=Fake(b,s,pub,t);sp.write_text(json.dumps(s));(rd/'preview_repair_pre.json').unlink()
    with patch.object(cli,'HERE',d),patch.object(h,'HERE',d),patch.object(cli.legacy,'snapshot_path',lambda *a:sp),patch.object(cli.legacy,'record_lock',lambda *a:contextlib.nullcontext()),patch.object(cli,'RepairClient',lambda *a:f):
        cli.run(rid);first=json.loads((rd/'preview_repair_original_session.json').read_text());cli.run(rid)
    saved=json.loads(sp.read_text());guard=json.loads((rd/'preview_repair_recovery.json').read_text())
    check('generic recovery preserves raw original session and idempotently fills verified staged marker',first==s and saved['phase']=='staged' and saved['native_staged']==guard['native_staged'] and len([c for c in f.calls if c[0]!='GET'])==1)

out={'offline_only':True,'source_sha256':{p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in ['preview_preservation.py','repair_owned_preview.py','native_metadata.py','apply_reviewed.py']},
     'tests':TESTS,'passed':sum(t['passed'] for t in TESTS),'failed':sum(not t['passed'] for t in TESTS)}
(ROOT/'reviews/PREVIEW_PRESERVATION_PROBE.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'passed':out['passed'],'failed':out['failed'],'failures':[t for t in TESTS if not t['passed']]},indent=2))
raise SystemExit(bool(out['failed']))
