"""Strict reviewed native/legacy target policy. Pure validation plus GET-only capture.
Unknown semantic fields or provider schema states fail closed for new root review.
"""
if not globals().get('_PR1131_SOURCE_VERIFIED',False):
    raise RuntimeError('Use the externally SHA-verified source bootstrap')
from urllib.parse import quote,urlsplit
import uuid
from ops_common import *

ACCESS={'record':'public','files':'public','embargo':{'active':False,'reason':None},'status':'open'}
LICENSE_DESCRIPTION_SHA='e7441778948d454a00c2eb0e1866d3738318f57b3c044ef3cdf34ec5b246bbeb'
FILE_CORE={'key','id','checksum','size','ext','mimetype','storage_class','metadata','access','links'}
COLLECTION_KEYS={'key','created','updated','mimetype','version_id','file_id','bucket_id','metadata','access','links','transfer','status','checksum','size','storage_class'}

def identifier(value):
    need(type(value) is int and value>0 or isinstance(value,str) and re.fullmatch('[1-9][0-9]*',value),'Malformed provider record ID');return int(value)
def uuid_value(value):
    need(isinstance(value,str),'Missing native content identifier')
    try:valid=str(uuid.UUID(value))==value
    except (ValueError,AttributeError):valid=False
    need(valid,'Malformed native content UUID');return value

def labels(value):
    need(isinstance(value,dict) and set(value)<={'en','de'} and all(isinstance(v,str) and v for v in value.values()),'Unknown provider vocabulary label shape')
def vocabulary(value,wanted):
    need(isinstance(value,dict) and set(value)<={'id','title'} and value.get('id')==wanted,'Wrong native vocabulary identifier')
    if 'title' in value:
        labels(value['title'])
        expected={'publication-preprint':'Preprint','eng':'English','references':'References','isderivedfrom':'Is derived from'}
        need(value['title'].get('en')==expected[wanted],'Native vocabulary English label changed')

def same_description(actual,wanted):
    if actual==wanted:return
    need(isinstance(wanted,str) and '\u2019' in wanted and re.fullmatch(r'(?:<p>[^<>]*</p>)+',wanted) is not None and actual==wanted.replace('\u2019',"'"),'Native description changed')

def metadata_projection(native,intended,legacy):
    allowed={'resource_type','creators','title','publisher','publication_date','subjects','languages','related_identifiers','version','rights','description','references'}
    need(isinstance(native,dict) and set(native)<=allowed,'Unreviewed native metadata field/override')
    vocabulary(native['resource_type'],'publication-preprint')
    need(native['title']==intended['title'] and native['publication_date']==intended['publication_date'] and native['version']==intended['version'] and native['publisher']=='Zenodo','Native title/date/version/publisher changed')
    same_description(native['description'],intended['description'])
    authors=[]
    for entry in native['creators']:
        need(isinstance(entry,dict) and set(entry)<={'person_or_org','affiliations'},'Extra native creator fields')
        person=entry['person_or_org'];need(set(person)<={'type','name','given_name','family_name','identifiers'} and person.get('type')=='personal','Unreviewed native creator type')
        name=person['name'];need(isinstance(name,str) and name.count(',')==1,'Unknown personal-name serialization')
        family,given=[x.strip() for x in name.split(',')]
        need(person.get('family_name')==family and person.get('given_name')==given,'Native creator name parts changed')
        ids=person.get('identifiers',[]);need(len(ids)==1 and set(ids[0])=={'scheme','identifier'} and ids[0]['scheme']=='orcid','Native creator identifiers changed')
        affiliations=entry.get('affiliations',[]);need(len(affiliations)==1 and set(affiliations[0])=={'name'},'Native affiliation structure changed')
        authors.append({'name':name,'orcid':ids[0]['identifier'],'affiliation':affiliations[0]['name']})
    need(authors==intended['creators'],'Native authors/ORCID/affiliation changed')
    need(native.get('subjects',[])==[{'subject':v} for v in intended['keywords']],'Native subjects changed')
    languages=native.get('languages',[])
    if legacy.get('language') is None:need(languages==[],'Unspecified legacy language differs from native')
    else:
        need(legacy['language']=='eng' and len(languages)==1,'Unreviewed default language')
        vocabulary(languages[0],'eng')
    rights=native['rights'];need(isinstance(rights,list) and len(rights)==1,'Native license inventory changed')
    right=rights[0];need(set(right)<={'id','title','description','icon','props'} and right.get('id')==intended['license'],'Native license changed')
    for k in ['title','description']:
        if k in right:need(isinstance(right[k],dict) and set(right[k])=={'en'} and isinstance(right[k]['en'],str),'Unknown license display decoration')
    if 'title' in right:need(right['title']['en']=='Creative Commons Attribution 4.0 International','Native license title override')
    if 'description' in right:need(sha(right['description']['en'].encode())==LICENSE_DESCRIPTION_SHA,'Native license description override')
    if 'props' in right:need(right['props']=={'url':'https://creativecommons.org/licenses/by/4.0/legalcode','scheme':'spdx'},'Native license URL/scheme override')
    if 'icon' in right:need(right['icon']=='cc-by-icon','Native license icon override')
    related=native.get('related_identifiers',[]);need(len(related)==len(intended['related_identifiers']),'Native related identifier count changed')
    for actual,wanted in zip(related,intended['related_identifiers']):
        need(set(actual)=={'identifier','scheme','relation_type'} and actual['identifier']==wanted['identifier'] and actual['scheme']==wanted['scheme'],'Native related identifier changed')
        vocabulary(actual['relation_type'],wanted['relation'].lower())
    need(native.get('references',[])==[{'reference':v} for v in intended['references']],'Native references changed')
    return {'title':native['title'],'authors':authors,'resource_type':'publication-preprint','publisher':'Zenodo','language':legacy.get('language'),'license':intended['license']}

def file_metadata(value,extension):
    if extension=='pdf':need(isinstance(value,dict) and (not value or set(value)=={'width','height'} and all(type(v) is int and v>0 for v in value.values())),'Unreviewed native PDF metadata')
    else:need(isinstance(value,dict) and (not value or set(value)=={'zip_toc_position'} and type(value['zip_toc_position']) is int and value['zip_toc_position']>=0),'Unreviewed native ZIP metadata')
def links(value,record,name,published):
    need(isinstance(value,dict) and {'self','content'}<=set(value)<= {'self','content','container','iiif_canvas','iiif_base','iiif_info','iiif_api'},'Unknown/missing native file link fields')
    encoded=quote(name,safe='');base='https://zenodo.org/api/records/'+str(record)
    roots={base+'/files/'+encoded}
    if not published:roots.add(base+'/draft/files/'+encoded)
    need(value['self'] in roots and value['content']==value['self']+'/content','Native content link does not identify exact target filename')
    if 'container' in value:need(value['container']==value['self']+'/container','Native container link changed')
    iiif='https://zenodo.org/api/iiif/record:'+str(record)
    expected={'iiif_canvas':iiif+'/canvas/'+encoded,'iiif_base':iiif+':'+encoded,'iiif_info':iiif+':'+encoded+'/info.json','iiif_api':iiif+':'+encoded+'/full/full/0/default.png'}
    for key,url in value.items():
        if key in expected:need(url==expected[key],'Native IIIF link changed')

def legacy_concept(legacy):
    concept=identifier(legacy.get('conceptrecid'))
    if 'conceptdoi' in legacy:need(legacy['conceptdoi']=='10.5281/zenodo.'+str(concept),'Supplied legacy concept DOI contradicts verified concept ID')
    return concept

def validate_target(legacy,native,file_collection,intended,uploads,record,published,required_names=None):
    """required_names=None permits a checked subset during initial staging only."""
    need(type(record) is int and record>0 and type(published) is bool,'Exact target identity/state required')
    zenodo.validate_record(legacy,record)
    need(legacy['submitted'] is published and legacy.get('state')==('done' if published else 'unsubmitted'),'Target publication/edit state changed')
    doi='10.5281/zenodo.'+str(record);need(legacy.get('doi')==doi,'Top-level intended DOI changed')
    if 'doi_url' in legacy:need(legacy['doi_url']=='https://doi.org/'+doi,'Legacy DOI URL changed')
    if 'record_id' in legacy:need(identifier(legacy['record_id'])==record,'Legacy record_id changed')
    md=legacy['metadata'];allowed=set(intended)|{'doi','access_right','imprint_publisher','language','prereserve_doi','relations','custom'}
    need(set(md)<=allowed,'Unreviewed extra legacy metadata/override')
    need(md.get('doi')==doi and md.get('access_right')=='open' and md.get('imprint_publisher','Zenodo')=='Zenodo' and md.get('language') in {None,'eng'} and md.get('custom',{})=={},'Unreviewed legacy DOI/access/publisher/language/custom override')
    need(md.get('prereserve_doi')=={'doi':doi,'recid':record},'Missing/wrong provider-intended DOI reservation')
    need(identifier(native.get('id'))==record and native.get('is_published') is published and native.get('is_draft') is (not published) and native.get('status')==('published' if published else 'draft'),'Native target identity/publication state changed')
    need(native.get('access')==ACCESS and native.get('custom_fields')=={},'Native access/embargo/custom fields changed')
    pids=native.get('pids');expected={'doi':{'identifier':doi,'provider':'datacite','client':'datacite'}}
    if published:expected['oai']={'identifier':'oai:zenodo.org:'+str(record),'provider':'oai'}
    need(pids==expected,'Native DOI provider/client/reservation/OAI changed')
    parent=native['parent'];concept=legacy_concept(legacy);need(identifier(parent['id'])==concept and concept!=record,'Native concept/version parent changed')
    need(parent.get('pids')=={'doi':{'identifier':'10.5281/zenodo.'+str(concept),'provider':'datacite','client':'datacite'}} and parent.get('communities')=={},'Native parent DOI/community override')
    owner=identifier(legacy.get('owner'));need(parent.get('access')=={'owned_by':{'user':str(owner)},'settings':{'allow_user_requests':False,'allow_guest_requests':False,'accept_conditions_text':None,'secret_link_expiration':0}},'Native owner/sharing settings changed')
    need(native.get('versions')=={'is_latest':True,'index':1},'Unreviewed version/reuse state')
    if 'relations' in md:
        rel=md['relations'];need(isinstance(rel,dict) and set(rel)<= {'version'},'Legacy semantic relation override')
        for version in rel.get('version',[]):need(version=={'index':0,'is_last':True,'parent':{'pid_type':'recid','pid_value':str(concept)}},'Legacy version-parent relation changed')
    native_meta=metadata_projection(native['metadata'],intended,md)
    targets={e['name']:e for e in uploads};remote=zenodo.server_files(legacy);names=set(remote)
    need(names<=set(targets) and (required_names is None or names==set(required_names)),'Legacy target file inventory changed')
    # Existing verifier checks every intended metadata value with only its narrow
    # entity/apostrophe/omitted-null-affiliation allowances, and all present files.
    zenodo.verify(legacy,intended,[targets[n] for n in sorted(names)])
    fs=native.get('files');need(isinstance(fs,dict) and set(fs)=={'enabled','order','count','total_bytes','entries'} and fs['enabled'] is True and fs['order']==[] and fs['count']==len(names) and fs['total_bytes']==sum(targets[n]['size'] for n in names) and set(fs['entries'])==names,'Native file inventory/enablement changed')
    need(isinstance(file_collection,dict) and set(file_collection)=={'enabled','links','entries','default_preview','order'} and file_collection['enabled'] is True and file_collection['order']==[] and file_collection['default_preview'] is None,'Native finalized-file collection semantics changed')
    collection=file_collection['entries'];need(isinstance(collection,list) and len(collection)==len(names),'Native collection count changed')
    entries={v['key']:v for v in collection};need(len(entries)==len(collection) and set(entries)==names,'Native file collection duplicate/extras')
    fingerprints={}
    for name in sorted(names):
        wanted=targets[name];entry=fs['entries'][name];file=entries[name];extension=name.rsplit('.',1)[-1];mime='application/pdf' if extension=='pdf' else 'application/zip'
        need(set(entry)==FILE_CORE and entry['key']==name and entry['checksum']=='md5:'+wanted['md5'] and type(entry['size']) is int and entry['size']==wanted['size'] and entry['ext']==extension and entry['mimetype']==mime and entry['storage_class']=='L' and entry['access']=={'hidden':False},'Native file bytes/type/visibility changed')
        need(set(file)==COLLECTION_KEYS and file['key']==name and file['status']=='completed' and file['checksum']=='md5:'+wanted['md5'] and type(file['size']) is int and file['size']==wanted['size'] and file['mimetype']==mime and file['storage_class']=='L' and file['transfer']=={'type':'L'} and file['access']=={'hidden':False},'Native upload is not exact/finalized/local/visible')
        uuid_value(entry['id']);need(remote[name].get('id')==entry['id']==uuid_value(file['file_id']),'Legacy/native file content IDs disagree')
        uuid_value(file['version_id']);uuid_value(file['bucket_id']);file_metadata(entry['metadata'],extension);file_metadata(file['metadata'],extension);links(entry['links'],record,name,published);links(file['links'],record,name,published)
        for metadata in [entry['metadata'],file['metadata']]:
            if 'zip_toc_position' in metadata:need(metadata['zip_toc_position']<wanted['size'],'ZIP index position exceeds exact file size')
        fingerprints[name]={k:file[k] for k in ['file_id','version_id','bucket_id','checksum','size']}
    media=native.get('media_files');need(isinstance(media,dict) and set(media)=={'enabled','order','count','total_bytes','entries'} and type(media['enabled']) is bool and media['order']==[] and media['count']==len(media['entries']) and media['total_bytes']==0,'Unreviewed derived-media inventory')
    pdf_ids={v['file_id'] for n,v in fingerprints.items() if n.endswith('.pdf')}
    for name,entry in media['entries'].items():
        need(name in {n+'.ptif' for n in names if n.endswith('.pdf')} and set(entry)=={'id','ext','size','mimetype','storage_class','key','metadata','access','processor','links'} and entry['key']==name and entry['ext']=='ptif' and entry['size']==0 and entry['mimetype']=='application/octet-stream' and entry['storage_class']=='L' and entry['metadata'] is None and entry['access']=={'hidden':True},'Unreviewed/visible derived media')
        uuid_value(entry['id']);processor=entry['processor'];need(set(processor)=={'type','status','source_file_id'} and processor['type']=='image-tiles' and processor['status'] in {'queued','running','finished','failed'} and processor['source_file_id'] in pdf_ids,'Unreviewed derived-media processor/source');links(entry['links'],record,name,published)
    bucket=legacy.get('links',{}).get('bucket')
    if not published:
        parsed=urlsplit(bucket or '');need(parsed.scheme=='https' and parsed.netloc=='zenodo.org' and parsed.path.startswith('/api/files/') and not parsed.query and not parsed.fragment,'Invalid target upload bucket')
        bucket_id=uuid_value(parsed.path.removeprefix('/api/files/'));need(all(v['bucket_id']==bucket_id for v in fingerprints.values()),'Native upload bucket disagrees with exact target')
    return {'record':record,'concept':concept,'owner':owner,'doi':doi,'published':published,'native_metadata':native_meta,'files':fingerprints,'bucket':bucket}

def observe(client,record,published,intended,uploads,required_names=None,capture=True):
    start=stamp();legacy=client.get(record);native=client.native_get(record,draft=not published)
    suffix='/draft' if not published else ''
    files=client.request('GET',client.base+'/api/records/'+str(record)+suffix+'/files')
    raw=None
    if capture:
        raw=PRIVATE/('target_'+uuid.uuid4().hex);raw.mkdir(mode=0o700)
        for name,value in [('legacy',legacy),('native',native),('files',files)]:durable(raw/(name+'.json'),value)
    result=validate_target(legacy,native,files,intended,uploads,record,published,required_names)
    fresh(start,seconds=30)
    result['observed_at']=start
    if raw is not None:durable(raw/'verified.json',result)
    return legacy,result

def public_projection(public,intended,verified):
    """Checked compatibility-public serialization; never discard extra semantics."""
    record=verified['record'];doi=verified['doi'];concept=verified['concept']
    need(identifier(public.get('id'))==record and public.get('submitted') is True and public.get('state')=='done' and public.get('status')=='published' and public.get('doi')==doi and public.get('doi_url')=='https://doi.org/'+doi,'Public record/DOI/publication state changed')
    need(identifier(public.get('conceptrecid'))==concept and public.get('conceptdoi')=='10.5281/zenodo.'+str(concept) and public.get('owners')==[verified['owner']],'Public concept/ownership differs from native')
    md=dict(public['metadata']);allowed=set(intended)|{'resource_type','doi','access_right','imprint_publisher','language','prereserve_doi','relations','custom'}
    need(set(md)<=allowed and 'upload_type' not in md and 'publication_type' not in md,'Unreviewed public metadata override/representation')
    need(md.pop('resource_type',None)=={'type':'publication','subtype':'preprint','title':'Preprint'} and md.get('license')=={'id':intended['license']},'Unreviewed public type/license projection')
    need(md.get('doi')==doi and md.get('access_right')=='open' and md.get('imprint_publisher','Zenodo')=='Zenodo' and md.get('custom',{})=={} and md.get('language')==verified['native_metadata']['language'],'Public DOI/access/publisher/custom/language override')
    if 'prereserve_doi' in md:need(md['prereserve_doi']=={'doi':doi,'recid':record},'Public DOI reservation changed')
    if 'relations' in md:need(md['relations']=={'version':[{'index':0,'is_last':True,'parent':{'pid_type':'recid','pid_value':str(concept)}}]},'Public zero-based version-parent projection changed')
    md.update(upload_type='publication',publication_type='preprint',license=intended['license'])
    return {**public,'metadata':md}
