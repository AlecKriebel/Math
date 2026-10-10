"""Offline adversarial probes. All clients and credentials are replaced by local fakes."""
from pathlib import Path
import sys, json, copy, tempfile, contextlib, importlib.util, hashlib
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT.parent/'zenodo_deposit_tool')]
source=Path(sys.argv[1]) if len(sys.argv)>1 else ROOT/'native_metadata.py'
spec=importlib.util.spec_from_file_location('native_audit_target',source)
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
RID=21699161

def original():
    return {'id':str(RID),'pids':{'doi':{'identifier':'10.5281/zenodo.21699161','provider':'datacite'},
                               'oai':{'identifier':'oai:zenodo.org:'+str(RID),'provider':'oai'}},
      'parent':{'id':'21699160','pids':{'doi':{'identifier':'10.5281/zenodo.21699160','provider':'datacite'}}},
      'versions':{'index':2,'is_latest':True,'is_latest_draft':True},
      'access':{'record':'public','files':'public','embargo':{'active':False}},
      'custom_fields':{'code:repository':'https://github.com/example/preserved'},
      'files':{'enabled':True,'default_preview':'paper.pdf','order':['paper.pdf'],'count':1,'total_bytes':12,
               'entries':{'paper.pdf':{'id':'unchanged-file-id','key':'paper.pdf','checksum':'md5:'+'a'*32,'size':12,'access':{'hidden':False}}}},
      'metadata':{'title':'Original scientific paper title','publication_date':'2026-08-30','version':'1.1.0',
        'resource_type':{'id':'publication-preprint','title':{'en':'Preprint'}},
        'creators':[{'person_or_org':{'type':'personal','name':'Kriebel, Alec','family_name':'Kriebel','given_name':'Alec','identifiers':[{'scheme':'gnd','identifier':'preserve'}]},'affiliations':[{'id':'institution-id','name':'Preserve affiliation'}]}],
        'subjects':[{'subject':'original subject'}],
        'description':'<p>Original unrefereed, extensively AI-assisted claim with limitations.</p>',
        'dates':[{'date':'2026-08-20','type':{'id':'other','title':{'en':'Other'}},'description':'Original submitted date'}],
        'additional_descriptions':[{'description':'Original method caveat','type':{'id':'methods','title':{'en':'Methods'}}}],
        'related_identifiers':[{'identifier':'https://github.com/example/support','scheme':'url','relation_type':{'id':'issupplementedby','title':{'en':'Is supplemented by'}},'resource_type':{'id':'software','title':{'en':'Software'}}}]},
      'is_published':True,'is_draft':False}

RESULTS=[]
def record(name,passed,details=''):
    RESULTS.append({'test':name,'passed':bool(passed),'details':details})

def translate_tests():
    o=original();before=copy.deepcopy(o)
    p={'keywords':['Bell nonlocality','POVM'],'language':'eng','creators':[{'name':'Kriebel, Alec','orcid':'0009-0001-9320-500X','affiliation':None}],
       'related_identifiers':[{'identifier':'https://github.com/example/support','scheme':'url','relation':'isSupplementedBy','resource_type':'software'},{'identifier':'10.1234/example','scheme':'doi','relation':'references'}],
       'notes':'Reviewed new note'}
    target=mod.translate(o,p)
    record('translate subjects and language',target['subjects']==[{'subject':'Bell nonlocality'},{'subject':'POVM'}] and target['languages']==[{'id':'eng'}])
    ids=target['creators'][0]['person_or_org']['identifiers']
    record('translate adds ORCID without removing other identifiers or affiliations',ids==[{'scheme':'gnd','identifier':'preserve'},{'scheme':'orcid','identifier':'0009-0001-9320-500X'}] and target['creators'][0]['affiliations']==o['metadata']['creators'][0]['affiliations'])
    record('translate dates, title, version, publication date and descriptions preserved',all(target[k]==o['metadata'][k] for k in ['dates','title','version','publication_date','description']) and target['additional_descriptions'][0]==o['metadata']['additional_descriptions'][0])
    record('translate existing structured relation preserved exactly',target['related_identifiers'][0]==o['metadata']['related_identifiers'][0])
    record('translate does not mutate original',o==before)
    bad=[{}, {'doi':'10.1234/bad'}, {'version':'2'}, {'title':'Unreviewed'}, {'access_right':'restricted'}, {'files':[]}, {'language':'eng'}]
    for i,pp in enumerate(bad):
        oo=copy.deepcopy(o)
        if i==6:oo['metadata']['languages']=[{'id':'eng'}]
        try:mod.translate(oo,pp)
        except Exception:record('reject prohibited or unsafe translation '+str(i),True)
        else:record('reject prohibited or unsafe translation '+str(i),False)
    oo=copy.deepcopy(o);oo['metadata']['subjects']=[{'subject':'Controlled','id':'vocab-id'}]
    try:mod.translate(oo,{'keywords':['replacement']})
    except Exception:record('reject controlled-subject erasure',True)
    else:record('reject controlled-subject erasure',False)
    try:mod.translate(o,{'related_identifiers':[]})
    except Exception:record('reject removing existing relation',True)
    else:record('reject removing existing relation',False)
    session={'protected':mod.protected(o),'original':o,'target_metadata':o['metadata']}
    for key in ['pids','access','custom_fields','files','versions']:
        changed=copy.deepcopy(o)
        if key=='files':changed[key]['entries']['paper.pdf']['checksum']='md5:'+'b'*32
        elif key=='versions':changed[key]['index']=3
        elif key=='pids':changed[key]['doi']['identifier']='10.1234/new'
        else:changed[key]['changed']=True
        try:mod.require_state(changed,session,False)
        except Exception:record('reject '+key+' drift after session captured',True)
        else:record('reject '+key+' drift after session captured',False)
    changed=copy.deepcopy(o);changed['metadata']['title']='Drift'
    try:mod.require_state(changed,session,False)
    except Exception:record('reject scientific title drift',True)
    else:record('reject scientific title drift',False)

def normalization_tests():
    o=original();d=copy.deepcopy(o);d['is_draft']=True;d['is_published']=False;d['pids'].pop('oai')
    before=copy.deepcopy(d);view,note=mod.normalized_draft(d,o)
    record('OAI normalization copies draft and records exact raw/original evidence',
           view['pids']==o['pids'] and d==before and note['raw_draft_pids']==before['pids'] and note['original_public_oai']==o['pids']['oai'])
    for flag in [False,None,1,'true']:
        changed=copy.deepcopy(d);changed['is_draft']=flag
        view,note=mod.normalized_draft(changed,o)
        record('OAI normalization rejects non-boolean-draft flag '+repr(flag),view==changed and note is None)
    for shape in ['wrong_record','wrong_provider','extra_oai_field','missing_other_pid']:
        oo=copy.deepcopy(o);dd=copy.deepcopy(d)
        if shape=='wrong_record':oo['pids']['oai']['identifier']='oai:zenodo.org:wrong'
        elif shape=='wrong_provider':oo['pids']['oai']['provider']='wrong'
        elif shape=='extra_oai_field':oo['pids']['oai']['unexpected']='value'
        else:oo['pids']['other']={'identifier':'preserve','provider':'external'}
        view,note=mod.normalized_draft(dd,oo)
        record('OAI normalization rejects '+shape,view==dd and note is None)
    oo=copy.deepcopy(o);dd=copy.deepcopy(d);oo['pids']['other']={'identifier':'preserve','provider':'external'};dd['pids']['other']=copy.deepcopy(oo['pids']['other'])
    view,note=mod.normalized_draft(dd,oo)
    record('OAI normalization preserves every additional PID exactly',view['pids']==oo['pids'] and note is not None)

class Fake:
    base='https://offline.invalid'
    def __init__(self,orig,drift=None,pending=False,fail=None,post_drift=None,draft_pid_drift=None):
        self.public=copy.deepcopy(orig);self.original_oai=copy.deepcopy(orig['pids'].get('oai'));self.draft=None;self.calls=[];self.pending=pending;self.fail=fail;self.post_drift=post_drift;self.published=False;self.post_public_reads=0;self.draft_pid_drift=draft_pid_drift
        if drift:
            key=drift
            if key=='files':self.public[key]['entries']['paper.pdf']['checksum']='md5:'+'b'*32
            elif key=='versions':self.public[key]['index']=3
            elif key=='parent':self.public[key]['id']='changed-parent'
            elif key=='pids':self.public[key]['doi']['identifier']='10.1234/new'
            elif key=='metadata':self.public[key]['title']='Drift'
            else:self.public[key]['changed']=True
    def get(self,rid):
        md=self.public['metadata'];legacy_md={k:copy.deepcopy(md[k]) for k in ['title','description','publication_date','version']}
        legacy_md.update(upload_type='publication',publication_type='preprint',license='cc-by-4.0',access_right='open')
        legacy_md['creators']=[]
        for author in md['creators']:
            person=author['person_or_org'];a={'name':person['name'],'affiliation':author.get('affiliations',[{}])[0].get('name')}
            for ident in person.get('identifiers',[]):
                if ident['scheme']=='orcid':a['orcid']=ident['identifier']
            legacy_md['creators'].append(a)
        if 'subjects' in md:legacy_md['keywords']=[d['subject'] for d in md['subjects']]
        if md.get('languages'):legacy_md['language']=md['languages'][0]['id']
        legacy_md['related_identifiers']=[{'identifier':r['identifier'],'scheme':r['scheme'],'relation':{'issupplementedby':'isSupplementedBy'}.get(r['relation_type']['id'],r['relation_type']['id']),**({'resource_type':r['resource_type']['id']} if r.get('resource_type') else {})} for r in md.get('related_identifiers',[])]
        for desc in md.get('additional_descriptions',[]):
            kind=desc['type']['id']
            if kind=='methods':legacy_md['method']=desc['description']
            elif kind=='notes':legacy_md['notes']=desc['description']
        if self.published and self.post_drift=='legacy_description':legacy_md['description']='Wrong serialized description'
        if self.published and self.post_drift=='legacy_title':legacy_md['title']='Wrong serialized title'
        return {'id':rid,'state':'inprogress' if self.pending else 'done','submitted':True,'doi':self.public['pids']['doi']['identifier'],'conceptrecid':self.public['parent']['id'],'metadata':legacy_md,'files':[{'filename':name,'checksum':entry['checksum'],'filesize':entry['size']} for name,entry in self.public['files']['entries'].items()]}
    def native_get(self,rid,draft=False):
        r=copy.deepcopy(self.draft if draft else self.public)
        if self.published and not draft:
            self.post_public_reads+=1
            if self.post_drift=='snapshot_native_date' and self.post_public_reads>=2:r['metadata']['dates'][0]['date']='2026-08-21'
            if self.post_drift=='snapshot_native_custom' and self.post_public_reads>=2:r['custom_fields']['changed']=True
            if self.post_drift=='snapshot_native_access' and self.post_public_reads>=2:r['access']['files']='restricted'
            if self.post_drift=='snapshot_native_oai' and self.post_public_reads>=2:r['pids'].pop('oai',None)
        return r
    def request(self,method,url,payload=None,**kw):
        if method=='GET' and '/versions' in url:
            self.calls.append((method,url,payload));hits=[copy.deepcopy(self.public)];hits += [{'id':'unexpected-new-version'}] if self.published and self.post_drift=='version_registry' else [];return {'hits':{'total':len(hits),'hits':hits}}
        self.calls.append((method,url,payload))
        if self.fail==len([c for c in self.calls if c[0]!='GET']):raise RuntimeError('injected uncertain operation failure')
        if method=='POST' and url.endswith('/draft'):
            self.draft=copy.deepcopy(self.public);self.draft['is_draft']=True;self.draft['is_published']=False
            if self.draft_pid_drift!='keep_oai':self.draft['pids'].pop('oai',None)
            if self.draft_pid_drift=='changed_oai':self.draft['pids']['oai']={'identifier':'oai:zenodo.org:wrong','provider':'oai'}
            if self.draft_pid_drift=='changed_doi':self.draft['pids']['doi']['identifier']='10.1234/new'
            if self.draft_pid_drift=='missing_doi':self.draft['pids'].pop('doi')
            if self.draft_pid_drift=='extra_pid':self.draft['pids']['other']={'identifier':'unexpected','provider':'unknown'}
        elif method=='PUT' and url.endswith('/draft'):
            assert set(payload)=={'metadata','custom_fields'}
            self.draft['metadata']=copy.deepcopy(payload['metadata']);self.draft['custom_fields']=copy.deepcopy(payload['custom_fields'])
        elif method=='POST' and url.endswith('/draft/actions/publish'):
            self.public=copy.deepcopy(self.draft);self.public['is_draft']=False;self.public['is_published']=True;self.published=True
            if self.original_oai:self.public['pids']['oai']=copy.deepcopy(self.original_oai)
            if self.post_drift=='native_file_auxiliary':self.public['files']['entries']['paper.pdf']['mimetype']='changed-value'
            if self.post_drift=='native_dates':self.public['metadata']['dates'][0]['date']='2026-08-21'
            if self.post_drift=='public_oai_missing':self.public['pids'].pop('oai',None)
            if self.post_drift=='public_oai_changed':self.public['pids']['oai']['identifier']='oai:zenodo.org:wrong'
        else:raise AssertionError('Unexpected mutation route: '+method+' '+url)
        return copy.deepcopy(self.draft or self.public)

def case(name,drift=None,pending=False,fail=None,publish=False,save_fail=False,post_drift=None,approval=None,draft_pid_drift=None):
    with tempfile.TemporaryDirectory(prefix='native_probe_',dir=ROOT/'reviews') as temp:
        d=Path(temp);rd=d/'receipts'/str(RID);rd.mkdir(parents=True)
        o=original();versions={'hits':{'total':1,'hits':[o]}}
        baseline=mod.snapshot(Fake(o),RID)
        (rd/'before.json').write_text(json.dumps(baseline))
        pp=d/'patch.json';pp.write_text(json.dumps({'metadata':{'keywords':['Bell nonlocality','POVM']}}))
        approved={'records':[{'id':RID,'patch_sha256':hashlib.sha256(pp.read_bytes()).hexdigest()}]}
        if approval=='hash':approved['records'][0]['patch_sha256']='incorrect-reviewed-hash'
        if approval=='missing':approved['records']=[]
        (d/'APPROVED_PROPOSALS.json').write_text(json.dumps(approved))
        client=Fake(o,drift,pending,fail,post_drift,draft_pid_drift);exc=None;result=None
        real_save=mod.zenodo.save_state
        def save(path,value):
            if save_fail:raise OSError('injected persistence failure')
            real_save(path,value)
        with patch.object(mod,'HERE',d), patch.object(mod.zenodo,'STATE_DIR',d/'states'),patch.object(mod.zenodo,'token_for',lambda e:'offline-dummy'),patch.object(mod,'PacedClient',lambda e,t:client),patch.object(mod.legacy,'record_lock',lambda *a:contextlib.nullcontext()),patch.object(mod.zenodo,'save_state',save):
            try:
                result=mod.run(RID,pp)
                if publish:result=mod.run(RID,pp,True)
            except Exception as e:exc=type(e).__name__+': '+str(e)
        mut=[c for c in client.calls if c[0]!='GET']
        if drift or pending or save_fail or approval:
            passed=bool(exc) and not mut
        elif post_drift:
            passed=bool(exc) and len(mut)==3 and not (rd/'after.json').exists()
        elif fail:
            passed=bool(exc) and len(mut)==fail and not any('/newversion' in c[1] or '/pids/' in c[1] or '/files/' in c[1] for c in mut)
        elif draft_pid_drift not in (None,'keep_oai'):
            passed=bool(exc) and len(mut)==1
        else:
            want=3 if publish else 2
            passed=(len(mut)==want and not exc and mod.protected(client.public)==mod.protected(o))
            if publish:passed=passed and client.public['metadata']['subjects']==[{'subject':'Bell nonlocality'},{'subject':'POVM'}]
            else:passed=passed and client.public==o
        record(name,passed,{'error':exc,'mutations':[c[:2] for c in mut],'result':result})

translate_tests()
normalization_tests()
case('successful OAI-omitting draft stage keeps public metadata and all protected fields')
case('successful same-record publish restores exact public OAI and preserves IDs, DOI, version, files, access, custom',publish=True)
case('successful same-record stage with exact original draft PIDs',draft_pid_drift='keep_oai')
for f in ['changed_oai','changed_doi','missing_doi','extra_pid']:
    case('reject unexpected draft PID shape '+f,draft_pid_drift=f)
for f in ['metadata','pids','files','access','custom_fields','versions','parent']:
    case('preflight rejects saved-baseline '+f+' drift before mutation',drift=f)
case('pre-existing pending draft rejected before mutation',pending=True)
case('persistence failure stops before mutation',save_fail=True)
for f in [1,2,3]:case('uncertain mutation '+str(f)+' fails without retry or later mutation',fail=f,publish=True)
case('reject changed reviewed patch hash before mutation',approval='hash')
case('reject unapproved record before mutation',approval='missing')
for f in ['version_registry','native_file_auxiliary','legacy_description','legacy_title','native_dates','snapshot_native_date','snapshot_native_custom','snapshot_native_access','snapshot_native_oai','public_oai_missing','public_oai_changed']:
    case('reject publication read-back drift '+f,publish=True,post_drift=f)
out={'source':str(source),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'offline_only':True,'tests':RESULTS,
     'passed':sum(r['passed'] for r in RESULTS),'failed':sum(not r['passed'] for r in RESULTS)}
out['related_source_sha256']={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in ['native_views.py','apply_reviewed.py','baseline.py']}
dest=ROOT/'reviews'/('NATIVE_WORKFLOW_PROBE_INITIAL.json' if 'audited_initial' in source.name else 'NATIVE_FINAL_AUDIT.json')
dest.write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'source_sha256':out['source_sha256'],'passed':out['passed'],'failed':out['failed'],'failures':[r['test'] for r in RESULTS if not r['passed']]},indent=2))
sys.exit(bool(out['failed']))
