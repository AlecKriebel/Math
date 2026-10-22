"""Exact reviewed draft/public phase compatibility; retain every original object."""
if not globals().get('_OPS17_VERIFIED',False):raise RuntimeError('Use checked17 bootstrap')
import copy,datetime,re,uuid
from urllib.parse import quote
BASE='https://zenodo.org'
def need(v,m):
    if not v:raise RuntimeError(m)
def number(v):
    need(type(v)is int and v>0 or type(v)is str and re.fullmatch('[1-9][0-9]*',v),'Invalid exact phase ID');return int(v)
def routes(role,r,c,published):
    api=BASE+'/api/records/'+str(r);dep=BASE+'/api/deposit/depositions/'+str(r);html=BASE+'/records/'+str(r)
    doi='https://doi.org/10.5281/zenodo.'+str(r);parentdoi='https://doi.org/10.5281/zenodo.'+str(c)
    if role=='legacy':
        out={'self':api if published else dep,'html':html if published else BASE+'/deposit/'+str(r),
             'files':api+'/files' if published else dep+'/files','latest_draft':dep,'latest_draft_html':BASE+'/deposit/'+str(r),
             'latest':api+'/versions/latest','latest_html':html+'/latest','doi':doi,'parent_doi':parentdoi,
             'record':api,'record_html':BASE+'/record/'+str(r),
             'badge':BASE+'/badge/doi/10.5281%2Fzenodo.'+str(r)+'.svg',
             'conceptbadge':BASE+'/badge/doi/10.5281%2Fzenodo.'+str(c)+'.svg'}
        out.update({k:dep+'/actions/'+k for k in ['publish','edit','discard','newversion']});return out
    root=api+(''if published else '/draft');iiif=BASE+'/api/iiif/'+('record:'if published else 'draft:')+str(r)
    out={'self':root,'self_html':html if published else BASE+'/uploads/'+str(r),'preview_html':html+'?preview=1',
         'reserve_doi':api+'/draft/pids/doi','self_iiif_manifest':iiif+'/manifest','self_iiif_sequence':iiif+'/sequence/default',
         'files':root+'/files','media_files':root+'/media-files','versions':api+'/versions','record':api,'record_html':html,
         'publish':api+'/draft/actions/publish','review':api+'/draft/review','draft':api+'/draft',
         'latest':api+'/versions/latest','latest_html':html+'/latest','doi':doi,'self_doi':doi,
         'self_doi_html':BASE+'/doi/10.5281/zenodo.'+str(r),'parent':BASE+'/api/records/'+str(c),
         'parent_html':BASE+'/records/'+str(c),'parent_doi':parentdoi,'parent_doi_html':BASE+'/doi/10.5281/zenodo.'+str(c)}
    out.update({k:api+'/'+suffix for k,suffix in [('access_links','access/links'),('access_grants','access/grants'),
        ('access_users','access/users'),('access_request','access/request'),('access','access'),('communities','communities'),
        ('communities-suggestions','communities-suggestions'),('quota_increase','quota-increase'),('requests','requests'),
        ('request_deletion','request-deletion'),('file_modification','file-modification')]});return out
def thumbnails(role,record,pdf):
    sizes=['10','50','100','250','750','1200']
    if role=='legacy':return {'thumb250':BASE+'/record/'+str(record)+'/thumb250','thumbs':{s:BASE+'/record/'+str(record)+'/thumb'+s for s in sizes}}
    return {'thumbnails':{s:BASE+'/api/iiif/record:'+str(record)+':'+quote(pdf,safe='')+'/full/%5E'+s+',/0/default.jpg' for s in sizes}}
def top_links(value,role,r,c,published,names):
    links=value.get('links');need(type(links)is dict,'Missing phase link object')
    required={'self','html'}if role=='legacy'else {'self','self_html','files','versions'}
    need(required<=set(links),'Missing authoritative phase self links')
    expected=routes(role,r,c,published)
    if role=='legacy' and not published and 'doi'not in value and 'doi'not in value.get('metadata',{}):expected['badge']=BASE+'/badge/doi/.svg'
    for key,wanted in expected.items():
        if key in links:need(type(links[key])is str and links[key]==wanted,'Wrong authoritative '+role+' link '+key)
    thumbkeys={'thumb250','thumbs'}if role=='legacy'else {'thumbnails'}
    if thumbkeys&set(links):
        pdf=[n for n in names if n.endswith('.pdf')];need(len(pdf)==1,'Thumbnail without exact intended PDF')
        wanted=thumbnails(role,r,pdf[0])
        for k in thumbkeys&set(links):need(links[k]==wanted[k] and type(links[k])is type(wanted[k]),'Contradictory target thumbnail '+k)
def content_links(value,r,name,published):
    need(type(value)is dict and {'self','content'}<=set(value),'Missing exact finalized content links')
    root=BASE+'/api/records/'+str(r)+(''if published else '/draft')+'/files/'+quote(name,safe='')
    need(value['self']==root and value['content']==root+'/content','Finalized links identify another target/file/phase')
    for key in ['commit','container']:
        if key in value:need(value[key]==root+'/'+key,'Wrong finalized '+key+' link')
    prefix=BASE+'/api/iiif/'+('record:'if published else 'draft:')+str(r)
    expected={'iiif_canvas':prefix+'/canvas/'+quote(name,safe=''),'iiif_base':prefix+':'+quote(name,safe='')}
    expected.update(iiif_info=expected['iiif_base']+'/info.json',iiif_api=expected['iiif_base']+'/full/full/0/default.png')
    for key,wanted in expected.items():
        if key in value:need(type(value[key])is str and value[key]==wanted,'Wrong finalized target IIIF '+key)
    # The original helper has no commit field and supports record: IIIF only.
    # Check every new field first; change only the compatibility copy.
    out=copy.deepcopy(value);out.pop('commit',None)
    if not published:
        for key in expected:
            if key in out:out[key]=out[key].replace('/iiif/draft:'+str(r),'/iiif/record:'+str(r),1)
    return out
def legacy_files(legacy,byname,record,published):
    # The actual legacy envelope uses filename/filesize/id/checksum and optional
    # links. Every supported duplicate alias must agree, even if the old shared
    # tool prefers a different field. Unknown file semantics require review.
    required={'filename','filesize','id','checksum'}
    aliases={'key','name','size','file_id','version_id','bucket_id','md5','links'}
    need(type(legacy['files'])is list,'Legacy files type')
    for e in legacy['files']:
        need(type(e)is dict and required<=set(e)<=required|aliases,'Unreviewed legacy file envelope')
        name=e['filename'];need(type(name)is str and name in byname,'Legacy filename lacks finalized context')
        wanted=byname[name]
        for key in ['filename','key','name']:
            if key in e:need(type(e[key])is str and e[key]==name,'Contradictory legacy filename alias '+key)
        for key in ['filesize','size']:
            if key in e:need(type(e[key])is int and e[key]==wanted['size'],'Contradictory typed legacy size alias '+key)
        for key,field in [('id','file_id'),('file_id','file_id'),('version_id','version_id'),('bucket_id','bucket_id')]:
            if key in e:need(type(e[key])is str and e[key]==wanted[field],'Contradictory legacy UUID alias '+key)
        md5=wanted['checksum'];need(type(md5)is str and re.fullmatch('md5:[0-9a-f]{32}',md5),'Finalized checksum syntax')
        need(type(e['checksum'])is str and e['checksum']in {md5,md5[4:]},'Contradictory legacy checksum')
        if 'md5'in e:need(type(e['md5'])is str and e['md5']==md5[4:],'Contradictory legacy MD5 alias')
        if 'links'in e:
            links=e['links'];api=BASE+'/api/records/'+str(record);fid=wanted['file_id']
            need(type(links)is dict and {'self','download'}<=set(links)<={'self','download','content'},'Unreviewed legacy file link envelope')
            selfroute=(api if published else BASE+'/api/deposit/depositions/'+str(record))+'/files/'+fid
            need(type(links['self'])is str and links['self']==selfroute,'Contradictory legacy file self ID/phase')
            # The actual published legacy serializer retains its draft download
            # route. Both supported routes identify this exact record and name.
            roots={api+'/files/'+quote(name,safe='')+'/content',api+'/draft/files/'+quote(name,safe='')+'/content'}
            for key in ['download','content']:
                if key in links:need(type(links[key])is str and links[key]in roots,'Contradictory legacy file content alias '+key)
def legacy_root(legacy,native,record,published,intended):
    known={'id','record_id','conceptrecid','conceptdoi','doi','doi_url','owner','title','state','submitted','created','modified','metadata','links','files'}
    need(type(legacy)is dict and set(legacy)<=known,'Unreviewed legacy root semantics')
    need(type(legacy['id'])is int and legacy['id']==record,'Legacy root record identity/type')
    if 'record_id'in legacy:need(type(legacy['record_id'])is int and legacy['record_id']==record,'Legacy duplicate record identity/type')
    concept=legacy['conceptrecid'];need(type(concept)is str and re.fullmatch('[1-9][0-9]*',concept) and number(native['parent']['id'])==int(concept),'Legacy root family alias/type')
    owner=legacy['owner'];need(type(owner)is int and owner>0 and native['parent']['access']['owned_by']['user']==str(owner),'Legacy root owner alias/type')
    need(type(legacy['submitted'])is bool and legacy['submitted']is published and type(legacy['state'])is str and legacy['state']==('done'if published else'unsubmitted'),'Legacy root state aliases/type')
    need(native['is_published']is published and native['is_draft']is(not published) and native['status']==('published'if published else'draft'),'Legacy/native publication-state contradiction')
    title=intended['title'];need(type(title)is str and legacy['metadata']['title']==title==native['metadata']['title'],'Legacy metadata/native/intended title mismatch')
    if 'title'in legacy:need(type(legacy['title'])is str and legacy['title']==title,'Legacy duplicate root title contradicts intended/native title')
    for key,native_key in [('created','created'),('modified','updated')]:
        if key in legacy:need(timestamp(legacy[key])==timestamp(native[native_key]),'Legacy/native root timestamp alias '+key)
    doi='10.5281/zenodo.'+str(record);family='10.5281/zenodo.'+concept
    for key,wanted in [('doi',doi),('doi_url','https://doi.org/'+doi),('conceptdoi',family)]:
        if key in legacy:need(type(legacy[key])is str and legacy[key]==wanted,'Legacy root DOI/family alias '+key)
    links=legacy['links'];allowed=set(routes('legacy',record,int(concept),published))|{'bucket','thumb250','thumbs'}
    need(type(links)is dict and set(links)<=allowed,'Unreviewed legacy root link semantics')
def prepare(legacy,native,collection,record,published,intended):
    need(type(record)is int and record>0 and type(published)is bool,'Bad phase context')
    legacy_root(legacy,native,record,published,intended)
    need(number(legacy.get('id'))==record==number(native.get('id')),'Cross-target phase identity')
    concept=number(legacy.get('conceptrecid'));need(number(native['parent']['id'])==concept and concept!=record,'Cross-family phase identity')
    doi='10.5281/zenodo.'+str(record);parentdoi='10.5281/zenodo.'+str(concept)
    for obj,key,wanted in [(legacy,'doi',doi),(legacy,'doi_url','https://doi.org/'+doi),(legacy,'conceptdoi',parentdoi),(legacy['metadata'],'doi',doi)]:
        if key in obj:need(type(obj[key])is str and obj[key]==wanted,'Contradictory optional draft DOI '+key)
    need(legacy['metadata'].get('prereserve_doi')=={'doi':doi,'recid':record},'Exact original reservation required')
    access=native['parent']['access'];need(type(access)is dict and {'owned_by','settings'}<=set(access)<= {'owned_by','settings','grants','links'},'Unreviewed parent access semantics')
    for key in ['grants','links']:
        if key in access:need(type(access[key])is list and not access[key],'Nonempty/malformed parent access '+key)
    L=copy.deepcopy(legacy);N=copy.deepcopy(native);F=copy.deepcopy(collection)
    for key in ['grants','links']:N['parent']['access'].pop(key,None)
    expected={'doi':{'identifier':doi,'provider':'datacite','client':'datacite'}}
    parent={'doi':{'identifier':parentdoi,'provider':'datacite','client':'datacite'}}
    if not published:
        need(native.get('pids')in [{},expected] and type(native.get('pids'))is dict,'Contradictory draft record PID')
        need(native['parent'].get('pids')in [{},parent] and type(native['parent'].get('pids'))is dict,'Contradictory draft parent PID')
        need(native.get('versions')=={'index':1,'is_latest':False,'is_latest_draft':True},'Unreviewed initial draft version state')
        if 'expires_at'in native:
            need(type(native['expires_at'])is str,'Wrong draft expiry type')
            try:expiry=datetime.datetime.fromisoformat(native['expires_at'].replace('Z','+00:00'))
            except ValueError:raise RuntimeError('Malformed draft expiry')
            need(expiry.tzinfo is not None,'Naive draft expiry')
        L['doi']=doi;L['metadata']['doi']=doi;N['pids']=expected;N['parent']['pids']=parent;N['versions']={'index':1,'is_latest':True}
    else:
        need('expires_at'not in native,'Unreviewed published expiry state')
        if 'is_latest_draft'in native['versions']:
            need(type(native['versions']['is_latest_draft'])is bool and native['versions']['is_latest_draft']is True,'Wrong published latest-draft flag')
            N['versions'].pop('is_latest_draft')
    if 'deletion_status'in native:
        d=native['deletion_status'];need(type(d)is dict and set(d)=={'is_deleted','status'} and d['is_deleted']is False and d['status']=='P','Deleted/unreviewed native object state')
    if 'swh'in native:need(type(native['swh'])is dict and not native['swh'],'Unreviewed software-heritage decoration')
    names=set(native['files']['entries'])
    top_links(legacy,'legacy',record,concept,published,names);top_links(native,'native',record,concept,published,names)
    need(type(collection.get('links'))is dict and collection['links'].get('self')==BASE+'/api/records/'+str(record)+(''if published else '/draft')+'/files','Finalized collection self identifies another target')
    byname={e['key']:e for e in collection['entries']};need(len(byname)==len(collection['entries']),'Duplicate finalized filename')
    legacy_files(legacy,byname,record,published)
    bucket=legacy['links'].get('bucket');prefix=BASE+'/api/files/'
    need(type(bucket)is str and bucket.startswith(prefix),'Missing exact target bucket')
    try:bucket_id=str(uuid.UUID(bucket[len(prefix):]))
    except (ValueError,AttributeError):raise RuntimeError('Malformed target bucket')
    need(bucket==prefix+bucket_id and all(e['bucket_id']==bucket_id for e in byname.values()),'Finalized bucket differs from exact legacy target')
    for entry in F['entries']:entry['links']=content_links(byname[entry['key']]['links'],record,entry['key'],published)
    for name,entry in N['files']['entries'].items():
        raw=native['files']['entries'][name]
        if 'links'not in raw:
            need(not published and name in byname and raw['id']==byname[name]['file_id'],'Missing/unbound embedded draft links')
            entry['links']=copy.deepcopy(next(e['links']for e in F['entries']if e['key']==name))
        else:entry['links']=content_links(raw['links'],record,name,published)
    return L,N,F
def reset(a,b,key):
    if key in a:b[key]=copy.deepcopy(a[key])
    else:b.pop(key,None)
def timestamp(v):
    need(type(v)is str,'Publication timestamp type')
    try:t=datetime.datetime.fromisoformat(v.replace('Z','+00:00'))
    except ValueError:raise RuntimeError('Malformed publication timestamp')
    need(t.tzinfo is not None,'Naive publication timestamp');return t
def upload_ack(value,entry,bucket,verified):
    """Actual bucket-file acknowledgement; it is not a legacy deposition."""
    fields={'created','updated','version_id','key','size','mimetype','checksum','is_head','delete_marker','links'}
    need(type(value)is dict and set(value)==fields,'Unreviewed upload acknowledgement envelope')
    name=entry['name'];need(name in verified['files'],'Upload acknowledgement lacks finalized intended file')
    wanted=verified['files'][name];file=next(e for e in verified['semantic17']['file_collection']['entries']if e['key']==name)
    need(type(value['key'])is str and value['key']==name,'Upload acknowledgement filename mismatch')
    need(type(value['size'])is int and value['size']==entry['size']==wanted['size'],'Upload acknowledgement exact size mismatch')
    need(type(value['checksum'])is str and value['checksum']=='md5:'+entry['md5']==wanted['checksum'],'Upload acknowledgement checksum mismatch')
    need(type(value['version_id'])is str and value['version_id']==wanted['version_id'],'Upload acknowledgement version identity mismatch')
    need(type(value['mimetype'])is str and value['mimetype']==file['mimetype'],'Upload acknowledgement MIME mismatch')
    need(value['is_head']is True and value['delete_marker']is False,'Upload acknowledgement head/deletion flags')
    need(timestamp(value['created'])==timestamp(file['created']),'Upload acknowledgement finalized creation mismatch')
    # Actual PDF/ZIP ACKs precede finalization by 52.637/31.2ms. Keep both raw
    # timestamps: same immutable version/creation, monotonically later finalized
    # update, rather than requiring equality or discarding timestamp semantics.
    need(timestamp(value['created'])<=timestamp(value['updated'])<=timestamp(file['updated']),'Upload acknowledgement/finalization timestamp order')
    route=bucket+'/'+quote(name,safe='')
    wanted_links={'self':route,'version':route+'?version_id='+wanted['version_id'],'uploads':route+'?uploads=1'}
    need(type(value['links'])is dict and set(value['links'])==set(wanted_links),'Upload acknowledgement link envelope')
    for key,url in wanted_links.items():need(type(value['links'][key])is str and value['links'][key]==url,'Upload acknowledgement wrong bucket/file/version link')
def initialized_stats(v):
    need(type(v)is dict and set(v)=={'this_version','all_versions'},'Unreviewed initialized statistics groups')
    for group in v.values():
        need(type(group)is dict and set(group)=={'views','unique_views','downloads','unique_downloads','data_volume'},'Unreviewed initialized statistic')
        for key,x in group.items():
            need(type(x)in ({int,float}if key=='data_volume'else {int}) and x>=0,'Malformed initialized statistic type/value')
def publication_fields(a,b):
    # Publication creates the public object with its own revision counter and
    # timestamps. No identity, payload, unknown field or earlier write is reset.
    an=a['native'];bn=b['native'];epoch=timestamp(bn['created'])
    need(timestamp(b['legacy']['created'])==epoch,'Published legacy/native creation epochs differ')
    for role in ['legacy','native']:
        need(timestamp(b[role]['created'])>=timestamp(a[role]['created']),'Publication creation regressed')
    need(timestamp(bn['updated'])>=epoch and timestamp(b['legacy']['modified'])>=epoch,'Publication update predates creation')
    for obj in [an,bn]:need(type(obj['revision_id'])is int and obj['revision_id']>=0,'Publication revision type/value')
    if bn['revision_id']<an['revision_id']:need(epoch>timestamp(an['created']),'Revision reset without new publication epoch')
    for role in ['legacy','native']:reset(a[role],b[role],'created')
    reset(an,bn,'revision_id')
    for key in ['deletion_status','stats','swh']:
        if key not in an and key in bn:
            if key=='stats':initialized_stats(bn[key])
            elif key=='swh':need(type(bn[key])is dict and not bn[key],'Unreviewed new SWH semantics')
            else:need(bn[key]=={'is_deleted':False,'status':'P'} and type(bn[key]['is_deleted'])is bool,'Unreviewed deletion state initialization')
            bn.pop(key)
    old={e['key']:e for e in a['file_collection']['entries']};new={e['key']:e for e in b['file_collection']['entries']}
    need(set(old)==set(new),'Published finalized filenames changed')
    for name in old:
        need(timestamp(new[name]['created'])>=epoch and timestamp(new[name]['updated'])>=timestamp(new[name]['created']),'Published finalized creation/update ordering')
        for key in ['created','updated']:
            need(timestamp(new[name][key])>=timestamp(old[name][key]),'Published finalized timestamp regressed')
            reset(old[name],new[name],key)
    ma=an['media_files'];mb=bn['media_files'];extra=set(mb['entries'])-set(ma['entries'])
    need(set(ma['entries'])<=set(mb['entries']),'Publication lost existing derived media')
    if extra:
        ids={e['id']for e in an['files']['entries'].values()};seen=set()
        for name in extra:
            need(name.endswith('.pdf.ptif') and name[:-5]in an['files']['entries'],'Unrelated publication derivative')
            e=mb['entries'][name];base=an['files']['entries'][name[:-5]]
            need(e['processor']['source_file_id']==base['id'] and e['id']not in ids and e['id']not in seen,'Derivative content identity/source contradiction');seen.add(e['id'])
        need(mb['enabled']is True and mb['count']==len(mb['entries']) and mb['total_bytes']==0,'Derived inventory initialization contradiction')
        for name in extra:mb['entries'].pop(name)
        mb['count']=ma['count'];mb['enabled']=ma['enabled']
def normalize(a,b,transition,added,record,concept):
    if transition=='upload' and added is not None and added.endswith('.pdf'):
        for role,keys in [('legacy',['thumb250','thumbs']),('native',['thumbnails'])]:
            for key in keys:reset(a[role]['links'],b[role]['links'],key)
    if transition!='publish':return
    publication_fields(a,b)
    for key in ['doi','doi_url','conceptdoi']:reset(a['legacy'],b['legacy'],key)
    reset(a['legacy']['metadata'],b['legacy']['metadata'],'doi')
    for key in ['pids','versions','expires_at']:reset(a['native'],b['native'],key)
    reset(a['native']['parent'],b['native']['parent'],'pids')
    for key in ['grants','links']:reset(a['native']['parent']['access'],b['native']['parent']['access'],key)
    for role in ['legacy','native']:
        for key in routes(role,record,concept,True):reset(a[role]['links'],b[role]['links'],key)
    for role,field in [('legacy','files'),('file_collection','entries')]:
        old={e['filename'if role=='legacy'else 'key']:e for e in a[role][field]};new={e['filename'if role=='legacy'else 'key']:e for e in b[role][field]}
        for name in set(old)&set(new):
            if 'links'in old[name] and 'links'in new[name]:
                for key in ['self','download','content','commit','container','iiif_canvas','iiif_base','iiif_info','iiif_api']:reset(old[name]['links'],new[name]['links'],key)
    for name in set(a['native']['files']['entries'])&set(b['native']['files']['entries']):
        x=a['native']['files']['entries'][name];y=b['native']['files']['entries'][name]
        if 'links'not in x:y.pop('links',None)
        elif 'links'in y:
            for key in ['self','content','commit','container','iiif_canvas','iiif_base','iiif_info','iiif_api']:reset(x['links'],y['links'],key)
