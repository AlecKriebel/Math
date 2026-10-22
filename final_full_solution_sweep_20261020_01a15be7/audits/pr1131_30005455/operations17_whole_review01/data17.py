"""Complete actual phase/public/append data checks; no provider actions."""
from pathlib import Path
import copy,datetime,hashlib,json,os,traceback,types,zipfile
ROOT=Path(__file__).resolve().parent;A=ROOT.parent;S=ROOT/'source';O=A/'operations';R=A.parent/'pr1329_30003208'
def need(v,m):
    if not v:raise RuntimeError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
need(not(ROOT/'MANIFEST.json').exists(),'Closed packet: no output overwrite')
need(os.statvfs(ROOT).f_bavail*os.statvfs(ROOT).f_frsize>=150*1024*1024,'150MiB reserve')
PINS={};CHECKS=[];CONTEXT={};EXPECTED={}
if(S/'SOURCE_MANIFEST.json').exists():
    raw=(S/'SOURCE_MANIFEST.json').read_bytes();need(sha(raw)=='623a85eca963527260367dd192bb0373f6a81972179633fa6f219c72a6237803','Final14 source anchor');EXPECTED=json.loads(raw)
    need({p.name for p in S.iterdir()}==set(EXPECTED)|{'SOURCE_MANIFEST.json'},'Final14 closure')
def read(p):
    b=p.read_bytes();pin={'bytes':len(b),'sha256':sha(b)}
    if p.parent==S and EXPECTED:need(EXPECTED[p.name]==pin,'Final14 buffer changed')
    PINS[str(p)]=pin;return b
def main():
    ns={'__file__':str(O/'bootstrap.py'),'__name__':'old_checked_data'};b=read(O/'bootstrap.py')
    need(sha(b)=='960b33e83135968ab40ef069b1b8876df47b70d1c4ef528bf0d8c836213ac58b','Immutable05 bootstrap')
    exec(compile(b,str(O/'bootstrap.py'),'exec',dont_inherit=True,optimize=0),ns)
    load,_=ns['load_verified'](O,'eab69e53e9d32510bbf00d74c1b94b70542a8b29cf326c42f5d974e510f09d00',sha(b))
    model=load('full_controls');c=load('ops_common');pl=load('publish_and_ledger');old=load('native_policy')
    def module(name,extra):
        p=S/(name+'.py');m=types.ModuleType(name);m.__dict__.update(_OPS17_VERIFIED=True,**extra)
        exec(compile(read(p),str(p),'exec',dont_inherit=True,optimize=0),m.__dict__);return m
    phase=module('phase17',{});sheet=module('sheet17',{});sheet.C=c
    policy=module('native17',{'SCHEMA':json.loads(read(S/'NATIVE_SCHEMA17.json')),'PHASE':phase});policy.install(c,pl,old,sheet.typed_equal)
    manifest=R/'publication_preparation_01/release/zenodo-deposit.json';read(manifest)
    metadata,uploads=c.zenodo.load_manifest(manifest)
    for e in uploads:read(e['path'])
    names={e['name']for e in uploads};record=23567720
    path=R/'root_publication_action01'
    mapping={'initial_l':'LEGACY_AFTER_CREATE.json','initial_n':'NATIVE_DRAFT_AFTER_CREATE.json','draft_l':'BEFORE_PUBLISH06_LEGACY.json','draft_n':'BEFORE_PUBLISH06_NATIVE.json','draft_f':'BEFORE_PUBLISH06_FINALIZED_FILES.json','public_l':'AFTER_PUBLISH_LEGACY.json','public_n':'AFTER_PUBLISH_NATIVE.json','public_f':'AFTER_PUBLISH_FINALIZED_FILES.json','public_envelope':'PUBLIC_RECORD_VERIFIED_CAPTURE.json'}
    data={k:json.loads(read(path/n))for k,n in mapping.items()};CONTEXT['actual_data']=data
    empty=copy.deepcopy(data['draft_f']);empty['entries']=[]
    initial=old.validate_target(data['initial_l'],data['initial_n'],empty,metadata,uploads,record,False,set())
    before=old.validate_target(data['draft_l'],data['draft_n'],data['draft_f'],metadata,uploads,record,False,names)
    published=old.validate_target(data['public_l'],data['public_n'],data['public_f'],metadata,uploads,record,True,names)
    policy.compare(before,published,transition='publish')
    pdf_path=R/'root_publication_observation02'
    pdf_l=json.loads(read(pdf_path/'LEGACY.json'));pdf_n=json.loads(read(pdf_path/'NATIVE.json'));pdf_f=json.loads(read(pdf_path/'FINALIZED_FILES.json'))
    pdf_names={n for n in names if n.endswith('.pdf')};zip_names=names-pdf_names
    need(len(pdf_names)==len(zip_names)==1,'Actual phase expected one PDF and ZIP')
    pdf=old.validate_target(pdf_l,pdf_n,pdf_f,metadata,uploads,record,False,pdf_names)
    policy.compare(initial,pdf,transition='upload',added=next(iter(pdf_names)))
    policy.compare(pdf,before,transition='upload',added=next(iter(zip_names)))
    CHECKS.extend([{'name':'actual_afterPDF_complete_three_views','pass':True},{'name':'actual_initial_to_afterPDF_upload_transition','pass':True},{'name':'actual_afterPDF_to_fullZIP_upload_transition','pass':True}])
    CHECKS.extend([{'name':'actual_initial_two_views_explicit_hypothetical_empty_third_view','pass':True},
                   {'name':'actual_complete_draft_three_views','pass':True},{'name':'actual_complete_published_three_views','pass':True},
                   {'name':'actual_complete_raw_draft_to_published_transition','pass':True}])
    p=copy.deepcopy(data['public_envelope']);projection=pl.public_projection(p,metadata,published);c.zenodo.verify(projection,metadata,uploads)
    need(sheet.typed_equal(p,data['public_envelope']),'Raw public object changed')
    CHECKS.append({'name':'actual_complete_public_envelope_aliases_and_metadata_files','pass':True})
    for label,filename,native_view,finalized_view,pub,names14 in [
      ('actual_original_create_response','ZENODO_CREATE_RESPONSE.json',data['initial_n'],empty,False,set()),
      ('actual_original_publish_response','ZENODO_PUBLISH_RESPONSE.json',data['public_n'],data['public_f'],True,names)]:
        raw=json.loads(read(path/filename))
        old.validate_target(raw,native_view,finalized_view,metadata,uploads,record,pub,names14)
        CHECKS.append({'name':label,'pass':True})
    for label,filename,verified in [('PDF','PDF_UPLOAD_RESPONSE.json',pdf),('ZIP','SOURCE_ZIP_UPLOAD_RESPONSE.json',before)]:
        raw=json.loads(read(path/filename));entry=next(e for e in uploads if e['name']==raw['key'])
        bucket='https://zenodo.org/api/files/'+verified['files'][entry['name']]['bucket_id']
        phase.upload_ack(raw,entry,bucket,verified);CHECKS.append({'name':'actual_'+label+'_bucket_upload_ack','pass':True})
        for tag,change in [
          ('size_bool',lambda v:v.__setitem__('size',True)),('size_wrong',lambda v:v.__setitem__('size',0)),
          ('key_wrong',lambda v:v.__setitem__('key','foreign.pdf')),('version_wrong',lambda v:v.__setitem__('version_id','00000000-0000-0000-0000-000000009999')),
          ('checksum_wrong',lambda v:v.__setitem__('checksum','md5:'+'0'*32)),('head_integer',lambda v:v.__setitem__('is_head',1)),
          ('deleted_integer',lambda v:v.__setitem__('delete_marker',0)),('unknown_field',lambda v:v.__setitem__('id',999)),
          ('foreign_link',lambda v:v['links'].__setitem__('self','https://zenodo.org/api/files/foreign/file')),
          ('timestamp_wrong',lambda v:v.__setitem__('created','2000-01-01T00:00:00+00:00'))]:
            v=copy.deepcopy(raw);change(v)
            try:phase.upload_ack(v,entry,bucket,verified)
            except Exception as error:CHECKS.append({'name':label+'_ack_'+tag,'pass':True,'rejected':True,'error':str(error)})
            else:CONTEXT['unexpected_upload_ack']=v;raise RuntimeError('Upload ACK contradiction accepted '+label+'/'+tag)
    for tag,published_phase in [('draft',False),('public',True)]:
        original_l=data[tag+'_l'];original_n=data[tag+'_n'];original_f=data[tag+'_f']
        aliases=copy.deepcopy(original_l);aliases.update(doi='10.5281/zenodo.'+str(record),doi_url='https://doi.org/10.5281/zenodo.'+str(record),conceptdoi='10.5281/zenodo.'+str(original_l['conceptrecid']))
        aliases['links'].update(phase.routes('legacy',record,int(original_l['conceptrecid']),published_phase))
        old.validate_target(aliases,original_n,original_f,metadata,uploads,record,published_phase,names)
        CHECKS.append({'name':tag+'_all_supported_consistent_legacy_root_and_route_aliases','pass':True})
        root_cases=[
          ('id_wrong',lambda l:l.__setitem__('id',999)),('id_bool',lambda l:l.__setitem__('id',True)),
          ('record_id_wrong',lambda l:l.__setitem__('record_id',999)),('record_id_bool',lambda l:l.__setitem__('record_id',True)),
          ('family_wrong',lambda l:l.__setitem__('conceptrecid','999')),('family_bool',lambda l:l.__setitem__('conceptrecid',True)),
          ('family_leadingzero',lambda l:l.__setitem__('conceptrecid','0'+l['conceptrecid'])),
          ('owner_wrong',lambda l:l.__setitem__('owner',999)),('owner_bool',lambda l:l.__setitem__('owner',True)),
          ('title_wrong',lambda l:l.__setitem__('title','Contradictory supplied legacy title')),('title_bool',lambda l:l.__setitem__('title',True)),
          ('state_wrong',lambda l:l.__setitem__('state','other')),('state_bool',lambda l:l.__setitem__('state',True)),
          ('submitted_wrong',lambda l:l.__setitem__('submitted',not published_phase)),('submitted_int',lambda l:l.__setitem__('submitted',int(published_phase))),
          ('created_wrong',lambda l:l.__setitem__('created','2000-01-01T00:00:00+00:00')),('created_bool',lambda l:l.__setitem__('created',True)),
          ('modified_wrong',lambda l:l.__setitem__('modified','2000-01-01T00:00:00+00:00')),('modified_bool',lambda l:l.__setitem__('modified',True)),
          ('doi_wrong',lambda l:l.__setitem__('doi','10.5281/zenodo.999')),('doi_bool',lambda l:l.__setitem__('doi',True)),
          ('doi_url_wrong',lambda l:l.__setitem__('doi_url','https://doi.org/10.5281/zenodo.999')),('doi_url_bool',lambda l:l.__setitem__('doi_url',True)),
          ('conceptdoi_wrong',lambda l:l.__setitem__('conceptdoi','10.5281/zenodo.999')),('conceptdoi_bool',lambda l:l.__setitem__('conceptdoi',True)),
          ('metadata_title_wrong',lambda l:l['metadata'].__setitem__('title','Foreign title')),('metadata_title_bool',lambda l:l['metadata'].__setitem__('title',True)),
          ('reservation_wrong',lambda l:l['metadata']['prereserve_doi'].__setitem__('doi','10.5281/zenodo.999')),
          ('reservation_bool',lambda l:l['metadata']['prereserve_doi'].__setitem__('recid',True)),
          ('unknown_root',lambda l:l.__setitem__('unreviewed_identity',{'id':999})),
          ('unsupported_recid_alias',lambda l:l.__setitem__('recid',str(record))),
          ('unsupported_owners_alias',lambda l:l.__setitem__('owners',[{'id':str(l['owner'])}])),
          ('unsupported_status_alias',lambda l:l.__setitem__('status','published'if published_phase else'draft')),
          ('unknown_root_link',lambda l:l['links'].__setitem__('unreviewed_identity','https://example.invalid/'))]
        for key in sorted(aliases['links']):
            root_cases.extend([(key+'_link_wrong',lambda l,k=key:l['links'].__setitem__(k,'https://zenodo.org/records/999')),
                               (key+'_link_bool',lambda l,k=key:l['links'].__setitem__(k,True))])
        for name,change in root_cases:
            l=copy.deepcopy(aliases);change(l)
            try:old.validate_target(l,original_n,original_f,metadata,uploads,record,published_phase,names)
            except Exception as error:CHECKS.append({'name':tag+'_legacy_root_'+name,'pass':True,'rejected':True,'error':str(error)})
            else:CONTEXT['unexpected_legacy_root']=l;raise RuntimeError('Contradictory legacy root accepted '+tag+'/'+name)
    for tag,published_phase in [('draft',False),('public',True)]:
        original_l=data[tag+'_l'];original_n=data[tag+'_n'];original_f=data[tag+'_f']
        l=copy.deepcopy(original_l)
        for e in l['files']:
            f=next(x for x in original_f['entries']if x['key']==e['filename'])
            e.update(key=e['filename'],name=e['filename'],size=e['filesize'],file_id=f['file_id'],version_id=f['version_id'],bucket_id=f['bucket_id'],md5=e['checksum'].removeprefix('md5:'))
            e['links']['content']=e['links']['download']
        old.validate_target(l,original_n,original_f,metadata,uploads,record,published_phase,names)
        CHECKS.append({'name':tag+'_consistent_legacy_aliases','pass':True})
        for name,change in [
          ('wrong_key',lambda e:e.__setitem__('key','a-different-paper.pdf')),
          ('wrong_name',lambda e:e.__setitem__('name','a-different-paper.pdf')),
          ('name_boolean',lambda e:e.__setitem__('name',True)),
          ('wrong_size',lambda e:e.__setitem__('size',0)),
          ('size_boolean',lambda e:e.__setitem__('size',False)),
          ('filesize_string',lambda e:e.__setitem__('filesize',str(e['filesize']))),
          ('wrong_file_id',lambda e:e.__setitem__('file_id','00000000-0000-0000-0000-000000009999')),
          ('wrong_version_id',lambda e:e.__setitem__('version_id','00000000-0000-0000-0000-000000009999')),
          ('wrong_bucket_id',lambda e:e.__setitem__('bucket_id','00000000-0000-0000-0000-000000009999')),
          ('wrong_md5',lambda e:e.__setitem__('md5','0'*32)),
          ('checksum_boolean',lambda e:e.__setitem__('checksum',False)),
          ('wrong_content',lambda e:e['links'].__setitem__('content','https://zenodo.org/api/records/999/files/foreign.pdf/content')),
          ('unknown_semantic_field',lambda e:e.__setitem__('unreviewed_identity','999')),
          ('unknown_link',lambda e:e['links'].__setitem__('unreviewed','https://example.invalid/'))]:
            l=copy.deepcopy(original_l);change(l['files'][0])
            try:old.validate_target(l,original_n,original_f,metadata,uploads,record,published_phase,names)
            except Exception as error:CHECKS.append({'name':tag+'_legacy_'+name,'pass':True,'rejected':True,'error':str(error)})
            else:CONTEXT['unexpected_legacy_alias']=l;raise RuntimeError('Contradictory legacy alias accepted '+tag+'/'+name)
    def public_reject(name,change):
        v=copy.deepcopy(data['public_envelope']);change(v)
        try:projection=pl.public_projection(v,metadata,published);c.zenodo.verify(projection,metadata,uploads)
        except Exception as error:CHECKS.append({'name':name,'pass':True,'rejected':True,'error':str(error)})
        else:CONTEXT['unexpected_public']=v;raise RuntimeError('Contradictory public alias accepted '+name)
    for name,change in [
      ('public_wrong_recid',lambda v:v.__setitem__('recid','999')),
      ('public_recid_boolean',lambda v:v.__setitem__('recid',True)),
      ('public_wrong_file_UUID',lambda v:v['files'][0].__setitem__('id','00000000-0000-0000-0000-000000009999')),
      ('public_wrong_content_URL',lambda v:v['files'][0]['links'].__setitem__('self','https://zenodo.org/api/records/999/files/foreign.pdf/content')),
      ('public_wrong_title',lambda v:v.__setitem__('title','Unrelated title')),
      ('public_wrong_key',lambda v:v['files'][0].__setitem__('key','foreign.pdf')),
      ('public_size_boolean',lambda v:v['files'][0].__setitem__('size',True)),
      ('public_wrong_checksum',lambda v:v['files'][0].__setitem__('checksum','md5:'+'0'*32)),
      ('public_wrong_owner',lambda v:v.__setitem__('owners',[{'id':'999'}])),
      ('public_wrong_DOI',lambda v:v.__setitem__('doi','10.5281/zenodo.999')),
      ('public_wrong_revision',lambda v:v.__setitem__('revision',999)),
      ('public_extra_file_field',lambda v:v['files'][0].__setitem__('unknown_identity','999'))]:public_reject(name,change)
    for name,change in [
      ('published_wrong_latest_draft_type',lambda l,n,f:n['versions'].__setitem__('is_latest_draft',1)),
      ('published_deleted_boolean_type',lambda l,n,f:n['deletion_status'].__setitem__('is_deleted',0)),
      ('published_visible_derivative',lambda l,n,f:next(iter(n['media_files']['entries'].values()))['access'].__setitem__('hidden',False)),
      ('published_wrong_derivative_source',lambda l,n,f:next(iter(n['media_files']['entries'].values()))['processor'].__setitem__('source_file_id','00000000-0000-0000-0000-000000009999')),
      ('published_unknown_native_field',lambda l,n,f:n.__setitem__('unreviewed_semantics',{'value':True})),
      ('published_unknown_initialized_stats',lambda l,n,f:n['stats'].__setitem__('unreviewed',{})),
      ('published_reset_without_new_epoch',lambda l,n,f:(l.__setitem__('created',data['draft_l']['created']),n.__setitem__('created',data['draft_n']['created'])))]:
        l=copy.deepcopy(data['public_l']);n=copy.deepcopy(data['public_n']);f=copy.deepcopy(data['public_f']);change(l,n,f)
        try:result=old.validate_target(l,n,f,metadata,uploads,record,True,names);policy.compare(before,result,transition='publish')
        except Exception as error:CHECKS.append({'name':name,'pass':True,'rejected':True,'error':str(error)})
        else:CONTEXT['unexpected_transition']={'legacy':l,'native':n,'files':f};raise RuntimeError('Bad publication transition accepted '+name)
    # API-contract compatibility is tested independently of any live workbook.
    transport=json.loads(read(R/'root_ledger_action01/APPEND_TRANSPORT.json'));reply=json.loads(transport['stdout'])
    book={'spreadsheetId':c.SHEET,'sheets':[{'properties':{'sheetId':c.SHEET_ID,'title':c.SHEET_TITLE,'sheetType':'GRID','gridProperties':{'rowCount':1177,'columnCount':43}}}]}
    snapshot={'metadata_before':book}
    for name,response in [('actual_comment_reply',reply),('old_metadata_reply',{'spreadsheetId':c.SHEET,'replies':[{}],'updatedSpreadsheet':book}),('metadata_plus_comment_reply',{**reply,'updatedSpreadsheet':book})]:
        sheet.append_response(response,snapshot);CHECKS.append({'name':name,'pass':True})
    for name,response in [('wrong_comment_value',{**reply,'commentUpdateState':'UPDATED'}),('comment_boolean',{**reply,'commentUpdateState':True}),('extra_reply_field',{**reply,'unknown':True})]:
        try:sheet.append_response(response,snapshot)
        except Exception as error:CHECKS.append({'name':name,'pass':True,'rejected':True,'error':str(error)})
        else:raise RuntimeError('Unreviewed append response accepted '+name)
    need(not model.ATTEMPTS,'Real escape attempted')
    out={'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_frozen':bool(EXPECTED),'source_pins':{p.name:{'bytes':len(p.read_bytes()),'sha256':sha(p.read_bytes())}for p in S.iterdir()},'input_pins':PINS,'checks':CHECKS,'actual_three_draft_and_published_views':True,'initial_third_view_explicitly_hypothetical':True,'metadata_and_upload_MD5_size_from_independent_root_release_manifest':True,'unrelated_PR1329_is_not1131_target_or_authority':True,'no_weakened_or_rewritten_actual_published_view':True,'actual_requests_or_mutations':0,'publication_ready':False}
    (ROOT/'private/DATA_RESULTS.json').write_text(json.dumps(out,sort_keys=True,indent=2)+'\n');print(json.dumps({'checks':len(CHECKS),'all_pass':all(x['pass']for x in CHECKS),'source_frozen':bool(EXPECTED),'actual_requests_or_mutations':0,'publication_ready':False}))
try:main()
except BaseException:
    index=1
    while(ROOT/'private'/('DEV_FAILURE_'+str(index)+'.zip')).exists():index+=1
    p=ROOT/'private'/('DEV_FAILURE_'+str(index)+'.zip')
    with zipfile.ZipFile(p,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=9)as z:
        for f in S.iterdir():z.writestr('source/'+f.name,f.read_bytes())
        z.writestr('data12.py',Path(__file__).read_bytes())
        z.writestr('EVIDENCE.json',json.dumps({'input_pins':PINS,'partial_checks':CHECKS,'context':CONTEXT,'traceback':traceback.format_exc()},sort_keys=True,indent=2)+'\n')
    raise
