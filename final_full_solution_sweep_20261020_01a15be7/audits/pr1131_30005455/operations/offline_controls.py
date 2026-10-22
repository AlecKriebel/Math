"""No-network repair controls; loaded only through the externally anchored bootstrap.
Real mutation modules are source-checked before loading; all provider writes below
are memory events. Every file write stays below operations/private/ or runtime/.
"""
if not globals().get('_PR1131_SOURCE_VERIFIED',False):
    raise RuntimeError('Use the externally SHA-verified source bootstrap')
import argparse,contextlib,copy,hashlib,importlib.util,io,json,marshal,os,shutil,socket,ssl,struct,subprocess,sys,types,uuid
from pathlib import Path
from types import SimpleNamespace
import http.client,urllib.request
NETWORK=[]
def blocked(*a,**k):
    NETWORK.append('forbidden external call');raise RuntimeError('Offline controls forbid services/processes')
socket.socket=blocked;socket.create_connection=blocked;subprocess.run=blocked;subprocess.Popen=blocked
from ops_common import *
import ops_common as c
import collect_live as live
import integrate_remote as integration
import publish_and_ledger as publication
import native_policy as native

RESULTS=[]
@contextlib.contextmanager
def patch(*changes):
    old=[]
    try:
        for obj,key,value in changes:old.append((obj,key,getattr(obj,key)));setattr(obj,key,value)
        yield
    finally:
        for obj,key,value in reversed(old):setattr(obj,key,value)
def reject(fn):
    try:fn()
    except Exception as exc:return type(exc).__name__
    raise RuntimeError('Fault was accepted')
def test(name,fn):
    try:detail=fn();RESULTS.append({'name':name,'status':'PASS','detail':detail})
    except Exception as exc:RESULTS.append({'name':name,'status':'FAIL','detail':type(exc).__name__+': '+str(exc)})
def newdir(label):
    root=PRIVATE/('repair_'+label+'_'+uuid.uuid4().hex);root.mkdir(mode=0o700);return root

def valid_pr(head,body=None,title=None,merged=False):
    reviewed_title,reviewed_body=reviewed_description(head)
    return {'number':1131,'head':{'sha':head,'ref':BRANCH,'repo':{'full_name':REPOSITORY}},'base':{'ref':'main','repo':{'full_name':REPOSITORY}},'merged':merged,'state':'closed' if merged else 'open','draft':not merged,'body':reviewed_body if body is None else body,'title':reviewed_title if title is None else title,'node_id':'MOCK_NODE'}

def ready_control(field=None,post=False):
    head='a'*40;state=valid_pr(head);root=newdir('ready');(root/'INTEGRATION_VERIFIED.json').write_text(json.dumps({'head':head}));writes=[]
    def gate(*a,**kw):
        if field and not post:state[field]='UNREVIEWED'
        return {'at_start':stamp(),'private_capture':'offline'},None,None
    def command(*a,**kw):
        writes.append('ready');state['draft']=False
        if field and post:state[field]='UNREVIEWED'
        return {'data':{}}
    with patch((integration,'RUNTIME',root),(c,'RUNTIME',root),(integration,'require_action',lambda *a:{}),(integration,'gh',lambda *a:copy.deepcopy(state)),(integration,'collect',gate),(integration,'command',command)):
        if field:reject(lambda:integration.mark_ready(SimpleNamespace(expected_pr_head=head)))
        else:need(integration.mark_ready(SimpleNamespace(expected_pr_head=head))=={'draft':False},'Ready positive failed')
    need(len(writes)==(1 if post or field is None else 0),'Ready mutation count wrong')
    need((root/'READY_VERIFIED.json').exists() is (field is None),'Ready falsely verified changed description')
    return {'writes':len(writes),'fault_rejected':field is not None,'verified_receipt':(root/'READY_VERIFIED.json').exists()}

def merge_control(field,post=False):
    head='b'*40;main='c'*40;tree='d'*40;commit='e'*40;state=valid_pr(head);state['draft']=False;root=newdir('merge');writes=[]
    checked={'main':main,'head':head,'tree':tree,'test_merge':'f'*40}
    def gate(*a,**kw):
        if not post:state[field]='UNREVIEWED'
        return {'at_start':stamp(),'main':main,'private_capture':'offline'},None,None
    def gh(endpoint):
        if endpoint=='pulls/1131':return copy.deepcopy(state)
        if endpoint=='git/ref/heads/main':return {'object':{'sha':main}}
        return {'sha':commit,'parents':[{'sha':main},{'sha':head}],'tree':{'sha':tree}}
    def command(*a,**kw):
        writes.append('merge');state['merged']=True;state['state']='closed'
        if post:state[field]='UNREVIEWED'
        return {'merged':True,'sha':commit}
    with patch((integration,'RUNTIME',root),(c,'RUNTIME',root),(integration,'require_action',lambda *a:{}),(integration,'test_merge',lambda *a:(copy.deepcopy(state),checked)),(integration,'collect',gate),(integration,'gh',gh),(integration,'command',command),(integration,'verify',lambda *a:{'main':main,'commit':commit})):
        reject(lambda:integration.merge(SimpleNamespace(expected_pr_head=head)))
    need(len(writes)==(1 if post else 0),'Merge description guard/write count wrong');need(not (root/'MERGE_VERIFIED.json').exists(),'Merge falsely verified changed description')
    return {'writes':len(writes),'fault_rejected':True,'verified_receipt':False}

class Provider:
    """Valid synthetic schema from separately observed native API shapes; no service."""
    base='https://zenodo.org'
    def __init__(self,uploads,metadata,complete=True,published=False):
        self.uploads=uploads;self.metadata=metadata;self.published=published;self.present={e['name']:e for e in uploads} if complete else {};self.fault=None;self.after_fault=None;self.calls={'create':0,'upload':0,'update':0,'publish':0};self.lost=False
        self.file_ids={e['name']:str(uuid.UUID(int=100+i)) for i,e in enumerate(uploads)}
    def records(self):
        md={**copy.deepcopy(self.metadata),'doi':'10.5281/zenodo.777','access_right':'open','imprint_publisher':'Zenodo','prereserve_doi':{'doi':'10.5281/zenodo.777','recid':777}}
        lg={'id':777,'record_id':777,'submitted':self.published,'state':'done' if self.published else 'unsubmitted','doi':'10.5281/zenodo.777','doi_url':'https://doi.org/10.5281/zenodo.777','conceptrecid':'778','owner':1789874,'metadata':md,'files':[],'links':{'bucket':'https://zenodo.org/api/files/'+str(uuid.UUID(int=50))}}
        authors=[]
        for creator in self.metadata['creators']:
            family,given=[x.strip() for x in creator['name'].split(',')];authors.append({'person_or_org':{'type':'personal','name':creator['name'],'family_name':family,'given_name':given,'identifiers':[{'scheme':'orcid','identifier':creator['orcid']}]},'affiliations':[{'name':creator['affiliation']}]})
        nm={'resource_type':{'id':'publication-preprint'},'creators':authors,'title':self.metadata['title'],'publisher':'Zenodo','publication_date':self.metadata['publication_date'],'subjects':[{'subject':v} for v in self.metadata['keywords']],'related_identifiers':[{'identifier':v['identifier'],'scheme':v['scheme'],'relation_type':{'id':v['relation'].lower()}} for v in self.metadata['related_identifiers']],'version':self.metadata['version'],'rights':[{'id':self.metadata['license']}],'description':self.metadata['description'],'references':[{'reference':v} for v in self.metadata['references']]}
        nt={'id':'777','is_published':self.published,'is_draft':not self.published,'status':'published' if self.published else 'draft','metadata':nm,'custom_fields':{},'access':copy.deepcopy(native.ACCESS),'pids':{'doi':{'identifier':'10.5281/zenodo.777','provider':'datacite','client':'datacite'}},'versions':{'is_latest':True,'index':1},'parent':{'id':'778','pids':{'doi':{'identifier':'10.5281/zenodo.778','provider':'datacite','client':'datacite'}},'communities':{},'access':{'owned_by':{'user':'1789874'},'settings':{'allow_user_requests':False,'allow_guest_requests':False,'accept_conditions_text':None,'secret_link_expiration':0}}},'files':{'enabled':True,'order':[],'count':len(self.present),'total_bytes':sum(e['size'] for e in self.present.values()),'entries':{}},'media_files':{'enabled':False,'order':[],'count':0,'total_bytes':0,'entries':{}}}
        if self.published:nt['pids']['oai']={'identifier':'oai:zenodo.org:777','provider':'oai'}
        fc={'enabled':True,'links':{},'entries':[],'default_preview':None,'order':[]}
        for i,(name,e) in enumerate(self.present.items()):
            fid=self.file_ids[name];extension=name.rsplit('.',1)[-1];mime='application/pdf' if extension=='pdf' else 'application/zip';link={'self':'https://zenodo.org/api/records/777/files/'+name,'content':'https://zenodo.org/api/records/777/files/'+name+'/content'}
            lg['files'].append({'filename':name,'id':fid,'checksum':e['md5'],'filesize':e['size']})
            nt['files']['entries'][name]={'key':name,'id':fid,'checksum':'md5:'+e['md5'],'size':e['size'],'ext':extension,'mimetype':mime,'storage_class':'L','metadata':{},'access':{'hidden':False},'links':link}
            fc['entries'].append({'key':name,'created':'2026-10-22T00:00:00Z','updated':'2026-10-22T00:00:00Z','mimetype':mime,'version_id':str(uuid.UUID(int=200+i)),'file_id':fid,'bucket_id':str(uuid.UUID(int=50)),'metadata':{},'access':{'hidden':False},'links':link,'transfer':{'type':'L'},'status':'completed','checksum':'md5:'+e['md5'],'size':e['size'],'storage_class':'L'})
        if self.fault:self.fault(lg,nt,fc)
        return lg,nt,fc
    def get(self,record):return self.records()[0]
    def native_get(self,record,draft=False):return self.records()[1]
    def request(self,method,url):need(method=='GET','Offline provider attempted unexpected method');return self.records()[2]
    def create(self,metadata):self.calls['create']+=1;return self.get(777)
    def upload(self,bucket,entry):self.calls['upload']+=1;self.present[entry['name']]=entry;return {}
    def update(self,record,metadata):self.calls['update']+=1;return self.get(record)
    def publish(self,record):
        self.calls['publish']+=1;self.published=True
        if self.after_fault:self.fault=self.after_fault
        if self.lost:raise c.zenodo.DepositError('Offline lost publish response')
        return self.get(record)

def guarded_provider(fault=None,action='publish',post=False,complete=True,published=False):
    metadata,uploads=c.zenodo.load_manifest(publication.MANIFEST);provider=Provider(uploads,metadata,complete,published)
    guard=publication.GuardedClient(SimpleNamespace(expected_pr_head='1'*40),action,777,delegate=provider)
    return provider,guard

def publication_control(fault=None,where='publish',post=False):
    provider,guard=guarded_provider(action='stage' if where in {'upload','update'} else 'publish',complete=where!='upload')
    real_observe=native.observe
    def observe(*a,**kw):return real_observe(*a,**kw,capture=False)
    def gate(*a,**kw):
        if fault and not post:provider.fault=fault
        if fault and post:provider.after_fault=fault
        return {'at_start':stamp()}, {777:provider.get(777)}, []
    with patch((publication,'require_action',lambda *a:{}),(publication,'collect',gate),(publication,'observe_target',observe)):
        guard.get(777)
        call=(lambda:guard.upload(provider.get(777)['links']['bucket'],guard.uploads[0])) if where=='upload' else (lambda:guard.update(777,guard.metadata)) if where=='update' else (lambda:guard.publish(777))
        if fault:reject(call)
        else:call()
    expected=1 if post or fault is None else 0
    need(provider.calls[where]==expected,'Fault reached unexpected provider write')
    return {'write':where,'calls':provider.calls[where],'fault_rejected':fault is not None,'native_and_legacy_checked':True}

def fault_legacy(key,value):return lambda l,n,f:l['metadata'].__setitem__(key,value)
def fault_native(key,value):return lambda l,n,f:n.__setitem__(key,value)
def pending(l,n,f):f['entries'][0]['status']='pending'
def replace_content(l,n,f):
    fid=str(uuid.UUID(int=999));l['files'][0]['id']=fid;name=l['files'][0]['filename'];n['files']['entries'][name]['id']=fid;f['entries'][0]['file_id']=fid

def metadata_faults():
    metadata,_=c.zenodo.load_manifest(publication.MANIFEST);count=0
    for key in metadata:
        publication_control(fault_legacy(key,'UNREVIEWED'));count+=1
    return {'every_supplied_metadata_key_rejected_before_POST':count}

def native_faults():
    cases={
      'access':fault_native('access',{'record':'restricted','files':'restricted'}),
      'external_doi':fault_native('pids',{'doi':{'identifier':'10.1000/unreviewed','provider':'external'}}),
      'wrong_doi':lambda l,n,f:l.__setitem__('doi','10.1000/unreviewed'),
      'wrong_reservation':fault_legacy('prereserve_doi',{'doi':'10.5281/zenodo.888','recid':888}),
      'legacy_access':fault_legacy('access_right','restricted'),
      'legacy_extra':fault_legacy('embargo_date','2030-01-01'),
      'native_license_title':lambda l,n,f:n['metadata']['rights'][0].__setitem__('title',{'en':'Restricted'}),
      'native_license_description':lambda l,n,f:n['metadata']['rights'][0].__setitem__('description',{'en':'UNREVIEWED'}),
      'native_vocabulary_label':lambda l,n,f:n['metadata']['resource_type'].__setitem__('title',{'en':'Dataset'}),
      'native_extra':lambda l,n,f:n['metadata'].__setitem__('copyright','Unreviewed semantic override'),
      'native_custom':fault_native('custom_fields',{'code:codeRepository':'https://unreviewed.invalid'}),
      'native_identity':fault_native('id','888'),
      'native_parent':lambda l,n,f:n['parent'].__setitem__('id','999'),
      'native_state':fault_native('is_published',True),
      'pending_file':pending,
      'wrong_checksum':lambda l,n,f:f['entries'][0].__setitem__('checksum','md5:'+'0'*32),
      'wrong_content_link':lambda l,n,f:f['entries'][0]['links'].__setitem__('content','https://zenodo.org/api/records/777/files/OTHER/content'),
      'hidden_upload':lambda l,n,f:n['files']['entries'][l['files'][0]['filename']].__setitem__('access',{'hidden':True}),
      'content_replaced_same_bytes':replace_content,
      'extra_upload':lambda l,n,f:l['files'].append({**l['files'][0],'filename':'UNREVIEWED.pdf'})}
    for name,fn in cases.items():publication_control(fn)
    return {'native_semantic_or_content_faults_rejected_before_POST':list(cases)}

def staged_faults():
    fault=fault_native('access',{'record':'restricted','files':'restricted'})
    publication_control(fault,where='upload');publication_control(fault,where='update');publication_control(pending,where='update')
    provider,guard=guarded_provider(action='stage')
    with patch((publication,'require_action',lambda *a:{}),(publication,'collect',lambda *a,**k:(_ for _ in ()).throw(RuntimeError('Unexpected gate')))):
        reject(lambda:guard.update(777,{**guard.metadata,'title':'UNREVIEWED'}))
    need(provider.calls['update']==0,'Unreviewed update argument reached provider')
    return {'stage_upload_update_native_checks':'PASS','supplied_update_override_rejected':True}

def public_semantics():
    provider,guard=guarded_provider(published=True);legacy,nt,fc=provider.records()
    verified=native.validate_target(legacy,nt,fc,guard.metadata,guard.uploads,777,True,{v['name'] for v in guard.uploads})
    public=copy.deepcopy(legacy);public['status']='published';public['owners']=[1789874];public['conceptdoi']='10.5281/zenodo.778'
    md=public['metadata'];md.pop('upload_type');md.pop('publication_type');md['resource_type']={'type':'publication','subtype':'preprint','title':'Preprint'};md['license']={'id':guard.metadata['license']};md['relations']={'version':[{'index':0,'is_last':True,'parent':{'pid_type':'recid','pid_value':'778'}}]}
    c.zenodo.verify(native.public_projection(public,guard.metadata,verified),guard.metadata,guard.uploads)
    faults=[('access_right','restricted'),('doi','10.1000/other'),('copyright','Unreviewed'),('language','fra'),('resource_type',{'type':'dataset'}),('relations',{'version':[{'index':1}]})]
    for key,value in faults:
        changed=copy.deepcopy(public);changed['metadata'][key]=value;reject(lambda changed=changed:native.public_projection(changed,guard.metadata,verified))
    return {'positive_public_projection':True,'public_semantic_overrides_rejected':len(faults),'zero_based_public_version_mapping_checked':True}


def recovery(lost):
    provider,guard=guarded_provider(published=not lost);provider.lost=lost;metadata,uploads=c.zenodo.load_manifest(publication.MANIFEST)
    state={'manifest':str(publication.MANIFEST.resolve()),'environment':'production','id':777};real=native.observe
    with patch((publication,'require_action',lambda *a:{}),(publication,'collect',lambda *a,**k:({'at_start':stamp()},None,None)),(publication,'observe_target',lambda *a,**k:real(*a,**k,capture=False)),(c.zenodo,'local_state',lambda *a:(PRIVATE/'OFFLINE_STATE.json',state)),(c.zenodo,'save_state',lambda *a:None),(c.zenodo,'doi_status',lambda *a:{'status':'not_checked_offline'})):
        result=c.zenodo.run(SimpleNamespace(command='publish',manifest=publication.MANIFEST,sandbox=False,confirm_id=777,check_doi=True),client=guard)
    need(result['state']=='published' and result['doi']=='10.5281/zenodo.777' and provider.calls['publish']==(1 if lost else 0),'Published recovery repeated/wrong target')
    return {'publish_POSTs':provider.calls['publish'],'recovered_published_exact_native':True}

def stage_happy():
    metadata,uploads=c.zenodo.load_manifest(publication.MANIFEST);provider=Provider(uploads,metadata,complete=False)
    guard=publication.GuardedClient(SimpleNamespace(expected_pr_head='1'*40),'stage',None,delegate=provider);real=native.observe
    with patch((publication,'require_action',lambda *a:{}),(publication,'collect',lambda *a,**k:({'at_start':stamp()},None,None)),(publication,'observe_target',lambda *a,**k:real(*a,**k,capture=False)),(c.zenodo,'local_state',lambda *a:(PRIVATE/'OFFLINE_STAGE.json',None)),(c.zenodo,'save_state',lambda *a:None)):
        result=c.zenodo.run(SimpleNamespace(command='stage',manifest=publication.MANIFEST,sandbox=False,confirm_id=None,check_doi=False),client=guard)
    need(result['state']=='ready_to_publish' and provider.calls=={'create':1,'upload':2,'update':1,'publish':0},'Positive staged native sequence failed')
    return {'mocked_writes':provider.calls,'each_upload_update_native_pre_and_postflight':True}


def source_faults():
    root=newdir('source');mirror=root/'Math'/AUDIT.relative_to(REPO)/'operations';mirror.mkdir(parents=True)
    raw=(OPS/'OPERATIONS_MANIFEST.json').read_bytes();manifest=strict_json(raw);ops_sha=sha(raw);boot_sha=_PR1131_EXECUTION['bootstrap_sha256']
    for name in [*manifest['files'],'OPERATIONS_MANIFEST.json']:
        target=mirror/name;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes((OPS/name).read_bytes())
    dependency=root/'Math/zenodo_deposit_tool/zenodo.py';dependency.parent.mkdir(parents=True);dependency.write_bytes((REPO/'zenodo_deposit_tool/zenodo.py').read_bytes())
    marker=root/'UNTRUSTED_CODE_RAN';old=dependency.read_bytes();dependency.write_bytes(old+b'\nfrom pathlib import Path\nPath('+repr(str(marker)).encode()+b').write_text("BAD")\n')
    reject(lambda:_PR1131_BOOTSTRAP(mirror,ops_sha,boot_sha));need(not marker.exists(),'Changed dependency executed before pin failure');dependency.write_bytes(old)
    source=mirror/'ops_common.py';original=source.read_bytes();source.write_bytes(original+b'\nfrom pathlib import Path\nPath('+repr(str(marker)).encode()+b').write_text("BAD")\n')
    reject(lambda:_PR1131_BOOTSTRAP(mirror,ops_sha,boot_sha));need(not marker.exists(),'Changed operation source executed');source.write_bytes(original)
    paths=[mirror/'bootstrap.py',*[mirror/n for n in ['ops_common.py','collect_live.py','integrate_remote.py','publish_and_ledger.py','native_policy.py','check_package.py','offline_controls.py']],dependency]
    for path in paths:
        stat=path.stat();cache=Path(importlib.util.cache_from_source(str(path),optimization='' if not sys.flags.optimize else str(sys.flags.optimize)));cache.parent.mkdir(exist_ok=True)
        poison=compile('from pathlib import Path\nPath('+repr(str(marker))+').write_text("BAD")\n',str(path),'exec',optimize=sys.flags.optimize)
        cache.write_bytes(importlib.util.MAGIC_NUMBER+struct.pack('<III',0,int(stat.st_mtime),stat.st_size)+marshal.dumps(poison))
    # Copy exact scientific inputs too, so the poisoned-cache control also
    # passes the complete fixed-package verifier using only checked source.
    target_audit=mirror.parent
    science=strict_json((AUDIT/'ROOT_SCIENTIFIC_CLEARANCE.json').read_bytes())
    for name in ['PACKAGE_FREEZE_01.json','ROOT_SCIENTIFIC_CLEARANCE.json','reviews/package01/FINAL_REVIEW_MANIFEST.json','reviews/package02/MANIFEST.json',*science['root_acceptance_pins']]:
        target=target_audit/name;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes((AUDIT/name).read_bytes())
    inventory=strict_json((PUBLICATION/'SOURCE_MANIFEST.json').read_bytes());freeze=strict_json((AUDIT/'PACKAGE_FREEZE_01.json').read_bytes())
    for name in set(inventory)|set(freeze['frozen_six'])|{'SOURCE_MANIFEST.json'}:
        target=target_audit/'publication'/name;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes((PUBLICATION/name).read_bytes())
    # External launcher semantics: verify raw bootstrap, compile those bytes,
    # then let it verify/compile every other checked source. No normal import.
    def external_boot(source,expected):
        need(sha(source)==expected,'External bootstrap digest changed before execution')
        namespace={'__name__':'offline_checked_bootstrap','__file__':str(mirror/'bootstrap.py')}
        exec(compile(source,str(mirror/'bootstrap.py'),'exec'),namespace);return namespace
    bootbytes=(mirror/'bootstrap.py').read_bytes();namespace=external_boot(bootbytes,boot_sha)
    load,_=namespace['load_verified'](mirror,ops_sha,boot_sha)
    for name in ['ops_common','collect_live','integrate_remote','publish_and_ledger','native_policy','check_package','offline_controls']:load(name)
    load('ops_common').package()
    need(not marker.exists(),'A valid unsealed cache executed')
    # Direct helpers fail before importing project code; the public documented
    # path is the external verifier, never normal project imports.
    direct=reject(lambda:exec(compile(original,str(source),'exec'),{'__file__':str(source),'__name__':'direct_unsupported'}))
    altered=bootbytes+b'\nPath('+repr(str(marker)).encode()+b').write_text("BAD")\n'
    reject(lambda:external_boot(altered,boot_sha));need(not marker.exists(),'Changed bootstrap executed before external anchor check')
    with patch((sys,'flags',SimpleNamespace(isolated=0,no_site=1))):reject(lambda:_PR1131_BOOTSTRAP(mirror,ops_sha,boot_sha))
    return {'nonisolated_load_rejected':True,'dependency_prepin_effect_blocked':True,'operation_prepin_effect_blocked':True,'valid_unsealed_caches_ignored':len(paths),'source_pin_pass_with_no_marker':True,'direct_helper_rejected':direct,'changed_bootstrap_rejected_by_external_digest':True}

def resolver_families():
    rejected=[]
    for authority in ['doi.org','www.doi.org','dx.doi.org','www.dx.doi.org','shortdoi.org','www.shortdoi.org','dx.shortdoi.org']:
        for prefix in ['', '//','https://','http://','ftp://','custom:']:
            for host in [authority,authority+'.',authority.replace('.', '%2e'),authority.replace('.', '%252e')]:
                value=prefix+host+'/abc';reject(lambda value=value:live.identities(value));rejected.append(value)
    # Canonical long DOI lexical identity is independent of any claim about
    # URI equivalence; generic resolver homepages carry no DOI record ID.
    accepted=['10.5281/zenodo.777','https://doi.org/10.5281/zenodo.777','//doi.org/10.5281/zenodo.777','doi.org/10.5281/zenodo.777','https://dx.doi.org/10.5281/zenodo.777']
    for value in accepted:need(live.identities(value)=={777},'Canonical long DOI lost')
    homes=['doi.org','//doi.org/','https://www.doi.org/','doi.org.','https://doi.org./','shortdoi.org','//shortdoi.org/','https://www.shortdoi.org/']
    for value in homes:need(live.identities(value)==set(),'Generic resolver homepage rejected or treated as DOI')
    need(live.identities('https://unrelated.invalid/path/doi.org/abc')==set(),'Unrelated URL path was treated as resolver authority')
    for value in ['https://doi.org./10.5281/zenodo.777','//doi.org./abc','DOI:https://doi.org./abc']:reject(lambda value=value:live.identities(value))
    captured=PRIVATE/'live_8e3a39143bb740ef9053274be751a820/ledger.json';checked_rows=None
    if captured.exists():
        rows=strict_json(captured.read_bytes())['values'];observation=strict_json((OPS/'READ_ONLY_OBSERVATIONS.json').read_bytes())
        need(digest(rows)==observation['ledger_sha256'],'Captured ledger differs from its sealed observation')
        for row in rows:live.row_ids(row)
        checked_rows=len(rows)
    return {'captured_rows_rechecked_not_live':checked_rows,'unresolved_family_forms_rejected':len(rejected)+3,'canonical_long_forms':len(accepted),'generic_homepages':len(homes),'unrelated_authority_not_equated':True}


def custody():
    p=package();_,changes=proposal();need(len(p['source'])==44 and len(p['flat'])==5 and len(changes)==8,'Fixed package changed');return {'assets':6,'source':44,'archive':45,'kit':5,'proposal_paths':8}

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
    need(PRIVATE in args.output.resolve().parents or RUNTIME in args.output.resolve().parents,'Offline output must stay in private/runtime')
    tests=[('fixed_scientific_and_proposal_custody',custody),('F1_ready_happy',lambda:ready_control()),('F1_ready_body_during_gate',lambda:ready_control('body')),('F1_ready_title_during_gate',lambda:ready_control('title')),('F1_ready_body_postflight',lambda:ready_control('body',True)),('F1_ready_title_postflight',lambda:ready_control('title',True)),('F1_merge_body_during_gate',lambda:merge_control('body')),('F1_merge_title_during_gate',lambda:merge_control('title')),('F1_merge_body_postflight',lambda:merge_control('body',True)),('F1_merge_title_postflight',lambda:merge_control('title',True)),('F2_publish_happy',lambda:publication_control()),('F2_every_supplied_metadata_after_gate',metadata_faults),('F3_native_semantics_and_file_faults',native_faults),('F3_stage_upload_update_guards',staged_faults),('F3_stage_happy_full_native_sequence',stage_happy),('F3_public_semantics',public_semantics),('F3_publish_native_postflight',lambda:publication_control(fault_native('pids',{}),post=True)),('published_ID_recovery_without_POST',lambda:recovery(False)),('lost_publish_response_one_POST',lambda:recovery(True)),('resolver_alias_families',resolver_families),('F4_verified_source_and_pyc_faults',source_faults)]
    for name,fn in tests:test(name,fn)
    result={'mode':'normal' if not sys.flags.optimize else '-O' if sys.flags.optimize==1 else '-OO','controls':RESULTS,'network_attempts':NETWORK,'external_mutations':0,'publication_ready':False,'root_operational_gate_pending':True}
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'mode':result['mode'],'controls':len(RESULTS),'failures':[r for r in RESULTS if r['status']!='PASS'],'network_attempts':NETWORK,'external_mutations':0},indent=2))
    return 1 if NETWORK or any(r['status']!='PASS' for r in RESULTS) else 0
if __name__=='__main__':raise SystemExit(main())
